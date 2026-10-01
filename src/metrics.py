"""Compute every Generative Brand Equity measure from the interim tables.

Usage: python src/metrics.py --tag main [--provisional]

--provisional lets the script run before the human ambiguity review is complete (unresolved
cases fall back to the deterministic match and are counted in outputs/tables/qa_summary.csv).
The final tables for the chapter must be produced without --provisional.

All rates use valid responses as denominators. Uncertainty: cluster bootstrap over prompts
(B = 2,000, percentile 95% intervals), because the five runs of a prompt are not independent.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CONFIG, INTERIM, MANUAL, PLATFORM_LABEL, PLATFORM_ORDER, TABLES, brands_cfg, prompts_df  # noqa: E402
from mentions import clean_text, compile_brand, find_mentions  # noqa: E402

B = 2000
SEED = 20261001
SOURCE_TYPES = ["brand_owned", "marketplace", "review_comparison", "community_ugc", "editorial_press",
                "encyclopaedic", "video", "other"]
SOURCE_LABEL = {"brand_owned": "Brand-owned", "marketplace": "Marketplace or retailer",
                "review_comparison": "Review or comparison", "community_ugc": "Community or UGC",
                "editorial_press": "Editorial or press", "encyclopaedic": "Encyclopaedic", "video": "Video",
                "other": "Other"}
TYPE_LABEL = {"d2c_origin": "D2C-origin", "incumbent": "Incumbent"}


# ------------------------------------------------------------------ loading

def _bool(s):
    return s.astype(str).str.lower().isin(["true", "1", "yes"])


def load(tag):
    r = pd.read_csv(INTERIM / f"responses_{tag}.csv", keep_default_na=False, dtype={"text": str})
    r["valid"] = _bool(r["valid"])
    r["branded"] = _bool(r["branded"])
    r["repetition"] = r["repetition"].astype(int)
    src = pd.read_csv(INTERIM / f"sources_{tag}.csv", keep_default_na=False)
    det = pd.read_csv(INTERIM / f"mentions_det_{tag}.csv")
    det["det_mentioned"] = _bool(det["det_mentioned"])
    det["ambiguous_brand"] = _bool(det["ambiguous_brand"])
    cr = pd.read_csv(INTERIM / f"coded_responses_{tag}.csv", keep_default_na=False)
    cb = pd.read_csv(INTERIM / f"coded_brands_{tag}.csv", keep_default_na=False)
    cb["llm_reference"] = _bool(cb["llm_reference"])
    cr, cb = cr[cr["pass"].astype(int) == 1], cb[cb["pass"].astype(int) == 1]
    return r, src, det, cr, cb


# ------------------------------------------------------------------ mention resolution

def resolve_mentions(det, cb, provisional):
    m = det.merge(cb[["response_id", "brand_id", "llm_reference"]], on=["response_id", "brand_id"], how="left")
    m["llm_reference"] = m["llm_reference"].fillna(False).astype(bool)
    m["agree"] = m.det_mentioned == m.llm_reference
    rev_path = MANUAL / "ambiguity_review.csv"
    rev = pd.read_csv(rev_path) if rev_path.exists() else pd.DataFrame(columns=["response_id", "brand_id", "decision"])
    rev = rev[rev.decision.astype(str).str.strip().isin(["brand", "not_brand"])]
    m = m.merge(rev[["response_id", "brand_id", "decision"]], on=["response_id", "brand_id"], how="left")
    m["mentioned"] = m.det_mentioned
    dis = ~m.agree
    m.loc[dis & m.decision.eq("brand"), "mentioned"] = True
    m.loc[dis & m.decision.eq("not_brand"), "mentioned"] = False
    m["unresolved"] = dis & m.decision.isna()
    if m.unresolved.any() and not provisional:
        raise SystemExit(f"{int(m.unresolved.sum())} det/LLM disagreements lack a human decision in "
                         f"{rev_path}. Run with --provisional for a preliminary pass only.")
    return m


def export_review(m, resp, tag):
    """Write disagreements with context snippets for the human decision."""
    d = m[~m.agree].merge(resp[["response_id", "text"]], on="response_id")
    brands = {b["id"]: b for b in brands_cfg()["brands"]}
    rows = []
    for x in d.itertuples():
        b = brands[x.brand_id]
        names = b.get("aliases", []) + b.get("aliases_case_sensitive", []) + [b["name"]]
        t = x.text
        pos = min([p for p in (t.lower().find(n.lower()) for n in names) if p >= 0], default=-1)
        snip = t[max(0, pos - 160): pos + 160].replace("\n", " ") if pos >= 0 else t[:300].replace("\n", " ")
        rows.append({"response_id": x.response_id, "brand_id": x.brand_id, "det_mentioned": x.det_mentioned,
                     "llm_reference": x.llm_reference, "context": snip, "decision": "", "decided_by": "", "note": ""})
    out = INTERIM / f"ambiguity_review_todo_{tag}.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    return out


# ------------------------------------------------------------------ positions among all brands named

def _norm(n):
    n = re.sub(r"[^\w\s&]", " ", str(n).lower())
    n = re.sub(r"^the\s+", "", n.strip())
    return re.sub(r"\s+", " ", n).strip()


def positions(m, resp, cr):
    brands = {b["id"]: b for b in brands_cfg()["brands"]}
    comp = {k: compile_brand(v) for k, v in brands.items()}
    allb = cr.set_index("response_id")["all_brands"].to_dict()
    text = resp.set_index("response_id")["text"].to_dict()
    cat = resp.set_index("response_id")["category"].to_dict()
    pos_rows = []
    for rid, g in m[m.mentioned].groupby("response_id"):
        t = clean_text(text.get(rid, ""))
        offsets = {}
        study_ids = [b for b, v in brands.items() if v["category"] == cat[rid]]
        for name in json.loads(allb.get(rid, "[]") or "[]"):
            if any(find_mentions(name, brands[s], comp[s]) for s in study_ids):
                continue  # study brands are placed by their deterministic offset below
            mt = re.search(r"(?<![\w-])" + re.escape(str(name).strip()) + r"(?![\w-])", t, re.IGNORECASE)
            if mt:
                offsets[_norm(name)] = min(offsets.get(_norm(name), 1e12), mt.start())
        for x in g.itertuples():
            hits = find_mentions(text.get(rid, ""), brands[x.brand_id], comp[x.brand_id])
            if hits:
                offsets["__" + x.brand_id] = hits[0][0]
        order = sorted(offsets.items(), key=lambda kv: kv[1])
        rank = {k: i + 1 for i, (k, _) in enumerate(order)}
        for x in g.itertuples():
            pos_rows.append({"response_id": rid, "brand_id": x.brand_id,
                             "position_all": rank.get("__" + x.brand_id), "n_brands_located": len(order)})
    return pd.DataFrame(pos_rows)


# ------------------------------------------------------------------ bootstrap helpers

def _boot_ratio(num_by_cluster, den_by_cluster, rng):
    k = len(num_by_cluster)
    idx = rng.integers(0, k, size=(B, k))
    num = num_by_cluster[idx].sum(1)
    den = den_by_cluster[idx].sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        est = num / den
    return np.nanpercentile(est, [2.5, 97.5])


def rate_ci(df, col, cluster="prompt_id", rng=None):
    g = df.groupby(cluster)[col].agg(["sum", "count"])
    lo, hi = _boot_ratio(g["sum"].to_numpy(float), g["count"].to_numpy(float), rng)
    return g["sum"].sum() / g["count"].sum(), lo, hi, int(g["count"].sum())


def diff_ci(df_a, df_b, col, rng):
    """Difference in pooled rates (a - b) with prompts resampled jointly."""
    ga = df_a.groupby("prompt_id")[col].agg(["sum", "count"])
    gb = df_b.groupby("prompt_id")[col].agg(["sum", "count"])
    j = ga.join(gb, lsuffix="_a", rsuffix="_b", how="outer").fillna(0)
    arr = j.to_numpy(float)
    k = len(arr)
    idx = rng.integers(0, k, size=(B, k))
    s = arr[idx].sum(1)
    est = s[:, 0] / s[:, 1] - s[:, 2] / s[:, 3]
    point = arr[:, 0].sum() / arr[:, 1].sum() - arr[:, 2].sum() / arr[:, 3].sum()
    lo, hi = np.percentile(est, [2.5, 97.5])
    return point, lo, hi


def pct(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(100 * x, 1)


# ------------------------------------------------------------------ main computations

def awareness_prominence(base, rng):
    """base: one row per valid non-branded response x study brand with mentioned, position flags."""
    out = []
    for (cat, pl, bid), g in base.groupby(["category", "platform", "brand_id"]):
        mr, lo, hi, n = rate_ci(g, "mentioned", rng=rng)
        fr, flo, fhi, _ = rate_ci(g, "first_study", rng=rng)
        tr, tlo, thi, _ = rate_ci(g, "top_pick", rng=rng)
        pos = g.loc[g.mentioned, "position_all"].dropna()
        out.append({"category": cat, "platform": pl, "brand_id": bid, "n_valid": n,
                    "n_mentioned": int(g.mentioned.sum()), "mention_rate": mr, "mr_lo": lo, "mr_hi": hi,
                    "first_mention_rate": fr, "fm_lo": flo, "fm_hi": fhi,
                    "first_given_mentioned": g.loc[g.mentioned, "first_study"].mean() if g.mentioned.any() else np.nan,
                    "top_pick_rate": tr, "tp_lo": tlo, "tp_hi": thi,
                    "mean_position": pos.mean() if len(pos) else np.nan, "n_position": len(pos)})
    t = pd.DataFrame(out)
    tot = base.groupby(["category", "platform"]).mentioned.sum().rename("all_study_mentions")
    t = t.join(tot, on=["category", "platform"])
    t["share_of_model"] = t.n_mentioned / t.all_study_mentions
    return t


def pooled_by_brand(base, rng):
    out = []
    for (cat, bid), g in base.groupby(["category", "brand_id"]):
        mr, lo, hi, n = rate_ci(g, "mentioned", rng=rng)
        tr, tlo, thi, _ = rate_ci(g, "top_pick", rng=rng)
        per_pl = g.groupby("platform").mentioned.mean()
        out.append({"category": cat, "brand_id": bid, "n_valid": n, "n_mentioned": int(g.mentioned.sum()),
                    "mention_rate": mr, "mr_lo": lo, "mr_hi": hi, "top_pick_rate": tr, "tp_lo": tlo, "tp_hi": thi,
                    "first_mention_rate": g.first_study.mean(),
                    "mean_position": g.loc[g.mentioned, "position_all"].mean(),
                    "platform_min": per_pl.min(), "platform_max": per_pl.max(),
                    "platform_range": per_pl.max() - per_pl.min(),
                    "platform_min_name": per_pl.idxmin(), "platform_max_name": per_pl.idxmax()})
    t = pd.DataFrame(out)
    tot = base.groupby("category").mentioned.sum()
    t["share_of_model"] = t.n_mentioned / t.category.map(tot)
    return t


def by_type(base, rng, exclude=()):
    b = base[~base.brand_id.isin(exclude)]
    out = []
    for keys, g in b.groupby(["category", "platform"]):
        d = g[g.brand_type == "d2c_origin"]; i = g[g.brand_type == "incumbent"]
        dr = rate_ci(d, "mentioned", rng=rng); ir = rate_ci(i, "mentioned", rng=rng)
        diff = diff_ci(d, i, "mentioned", rng)
        dt = rate_ci(d, "top_pick", rng=rng); it = rate_ci(i, "top_pick", rng=rng)
        out.append({"category": keys[0], "platform": keys[1], "d2c_rate": dr[0], "d2c_lo": dr[1], "d2c_hi": dr[2],
                    "inc_rate": ir[0], "inc_lo": ir[1], "inc_hi": ir[2], "diff": diff[0], "diff_lo": diff[1],
                    "diff_hi": diff[2], "d2c_top": dt[0], "inc_top": it[0], "n_responses": dr[3] // max(1, d.brand_id.nunique())})
    for cat, g in b.groupby("category"):
        d = g[g.brand_type == "d2c_origin"]; i = g[g.brand_type == "incumbent"]
        dr = rate_ci(d, "mentioned", rng=rng); ir = rate_ci(i, "mentioned", rng=rng)
        diff = diff_ci(d, i, "mentioned", rng)
        dt = rate_ci(d, "top_pick", rng=rng); it = rate_ci(i, "top_pick", rng=rng)
        out.append({"category": cat, "platform": "all", "d2c_rate": dr[0], "d2c_lo": dr[1], "d2c_hi": dr[2],
                    "inc_rate": ir[0], "inc_lo": ir[1], "inc_hi": ir[2], "diff": diff[0], "diff_lo": diff[1],
                    "diff_hi": diff[2], "d2c_top": dt[0], "inc_top": it[0], "n_responses": dr[3] // max(1, d.brand_id.nunique())})
    return pd.DataFrame(out)


def gee_check(base):
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    rows = []
    for cat, g in base.groupby("category"):
        g = g.copy()
        g["d2c"] = (g.brand_type == "d2c_origin").astype(int)
        g["y"] = g.mentioned.astype(int)
        try:
            mod = smf.gee("y ~ d2c + C(platform)", groups="prompt_id", data=g,
                          family=sm.families.Binomial(), cov_struct=sm.cov_struct.Exchangeable()).fit()
            ci = mod.conf_int().loc["d2c"]
            rows.append({"category": cat, "odds_ratio_d2c": float(np.exp(mod.params["d2c"])),
                         "or_lo": float(np.exp(ci[0])), "or_hi": float(np.exp(ci[1])), "p_value": float(mod.pvalues["d2c"]),
                         "n_obs": int(mod.nobs), "n_clusters": int(g.prompt_id.nunique())})
        except Exception as e:  # noqa: BLE001
            rows.append({"category": cat, "error": str(e)[:200]})
    return pd.DataFrame(rows)


def jaccard(a, b):
    a, b = set(a), set(b)
    if not a and not b:
        return 1.0, True
    return len(a & b) / len(a | b), False


def stability(base_valid_resp, ment, cr, rng):
    """Run-to-run Jaccard of study-brand sets (and of all brands named) per prompt x platform."""
    sets = ment[ment.mentioned].groupby("response_id").brand_id.apply(set).to_dict()
    allb = {r: {_norm(x) for x in json.loads(v or "[]")} for r, v in cr.set_index("response_id").all_brands.items()}
    rows = []
    for (pid, pl), g in base_valid_resp.groupby(["prompt_id", "platform"]):
        ids = list(g.response_id)
        if len(ids) < 2:
            continue
        js, empties, jo = [], 0, []
        for a, b in combinations(ids, 2):
            j, e = jaccard(sets.get(a, set()), sets.get(b, set()))
            js.append(j); empties += e
            jo.append(jaccard(allb.get(a, set()), allb.get(b, set()))[0])
        top = g.top_pick_norm.tolist()
        modal = pd.Series(top).value_counts().iloc[0] / len(top) if top else np.nan
        rows.append({"prompt_id": pid, "platform": pl, "category": g.category.iloc[0], "prompt_type": g.prompt_type.iloc[0],
                     "n_runs": len(ids), "n_pairs": len(js), "jaccard_study": np.mean(js), "empty_pairs": empties,
                     "jaccard_all_brands": np.mean(jo), "top_pick_modal_share": modal})
    per = pd.DataFrame(rows)
    agg = []
    for keys, g in list(per.groupby(["platform"])) + list(per.groupby(["platform", "prompt_type"])):
        keys = keys if isinstance(keys, tuple) else (keys,)
        arr = g.jaccard_study.to_numpy(); arr2 = g.jaccard_all_brands.to_numpy()
        idx = rng.integers(0, len(arr), size=(B, len(arr)))
        lo, hi = np.percentile(arr[idx].mean(1), [2.5, 97.5])
        lo2, hi2 = np.percentile(arr2[idx].mean(1), [2.5, 97.5])
        agg.append({"platform": keys[0], "prompt_type": keys[1] if len(keys) > 1 else "all",
                    "n_prompt_platform_cells": len(g), "jaccard_study": arr.mean(), "js_lo": lo, "js_hi": hi,
                    "jaccard_all_brands": arr2.mean(), "ja_lo": lo2, "ja_hi": hi2,
                    "share_empty_pairs": g.empty_pairs.sum() / g.n_pairs.sum(),
                    "top_pick_modal_share": g.top_pick_modal_share.mean()})
    return per, pd.DataFrame(agg)


def cross_platform(base_valid_resp, ment, cr):
    sets = ment[ment.mentioned].groupby("response_id").brand_id.apply(set).to_dict()
    allb = {r: {_norm(x) for x in json.loads(v or "[]")} for r, v in cr.set_index("response_id").all_brands.items()}
    rows = []
    for pid, g in base_valid_resp.groupby("prompt_id"):
        u_s = {pl: set().union(*[sets.get(r, set()) for r in gg.response_id]) for pl, gg in g.groupby("platform")}
        u_a = {pl: set().union(*[allb.get(r, set()) for r in gg.response_id]) for pl, gg in g.groupby("platform")}
        for a, b in combinations(sorted(u_s), 2):
            rows.append({"prompt_id": pid, "pair": f"{a}-{b}", "jaccard_study": jaccard(u_s[a], u_s[b])[0],
                         "jaccard_all_brands": jaccard(u_a[a], u_a[b])[0]})
    t = pd.DataFrame(rows)
    return t.groupby("pair")[["jaccard_study", "jaccard_all_brands"]].mean().reset_index().assign(
        n_prompts=t.groupby("pair").size().values)


def image(ment_all, cb, resp):
    brands = {b["id"]: b for b in brands_cfg()["brands"]}
    x = ment_all[ment_all.mentioned].merge(cb, on=["response_id", "brand_id"], how="left")
    x = x.merge(resp[["response_id", "platform", "prompt_type"]], on="response_id")
    x["attr_list"] = x.attributes.fillna("").map(lambda s: [a for a in str(s).split("|") if a])
    x["n_attr"] = x.attr_list.map(len)
    x["pos_hits"] = [len(set(a) & set(brands[b]["positioning_codes"])) for a, b in zip(x.attr_list, x.brand_id)]
    rows, attr_rows = [], []
    for bid, g in x.groupby("brand_id"):
        d = g[g.n_attr > 0]
        sent = g.sentiment.value_counts(normalize=True)
        rows.append({"brand_id": bid, "n_descriptions": len(g), "n_with_attributes": len(d),
                     "positioning_recall": (d.pos_hits > 0).mean() if len(d) else np.nan,
                     "positioning_share": d.pos_hits.sum() / d.n_attr.sum() if len(d) else np.nan,
                     **{f"sent_{k}": sent.get(k, 0.0) for k in ["positive", "neutral", "mixed", "negative"]},
                     "stance_recommended": (g.stance == "recommended").mean(),
                     "stance_discouraged": (g.stance == "discouraged").mean()})
        cnt = pd.Series([a for l in d.attr_list for a in l]).value_counts()
        for code, n in cnt.items():
            attr_rows.append({"brand_id": bid, "code": code, "n": int(n), "share_of_descriptions": n / max(1, len(d)),
                              "is_positioning": code in brands[bid]["positioning_codes"]})
    return pd.DataFrame(rows), pd.DataFrame(attr_rows), x


def credibility(ment_all, src, resp, domain_types):
    s = src[src.kind == "displayed"].merge(domain_types, on="domain", how="left")
    s["source_type"] = s.source_type.fillna("UNCLASSIFIED")
    per_resp = s.groupby("response_id")
    platform_rows = []
    vr = resp[resp.valid]
    for pl, g in vr.groupby("platform"):
        ss = s[s.response_id.isin(g.response_id)]
        mix = ss.source_type.value_counts(normalize=True)
        platform_rows.append({"platform": pl, "n_valid": len(g), "share_with_sources": g.response_id.isin(ss.response_id).mean(),
                              "mean_sources": ss.groupby("response_id").size().reindex(g.response_id, fill_value=0).mean(),
                              "n_sources": len(ss), **{t: mix.get(t, 0.0) for t in SOURCE_TYPES + ["UNCLASSIFIED"]}})
    m = ment_all[ment_all.mentioned].merge(resp[["response_id", "platform"]], on="response_id")
    brands = {b["id"]: b for b in brands_cfg()["brands"]}
    rows = []
    for (bid), g in m.groupby("brand_id"):
        ss = s[s.response_id.isin(g.response_id)]
        mix = ss.source_type.value_counts(normalize=True)
        own = set(brands[bid]["official_domains"])
        own_hit = ss[ss.domain.isin(own) | ss.domain.map(lambda d: any(str(d).endswith(o) for o in own))].response_id.unique()
        with_src = g.response_id.isin(ss.response_id)
        rows.append({"brand_id": bid, "n_responses": len(g), "n_with_sources": int(with_src.sum()), "n_sources": len(ss),
                     "own_site_rate": g.response_id.isin(own_hit).sum() / max(1, with_src.sum()),
                     "n_distinct_domains": ss.domain.nunique(),
                     "n_third_party_types": int(sum(mix.get(t, 0) > 0 for t in SOURCE_TYPES if t != "brand_owned")),
                     **{t: mix.get(t, 0.0) for t in SOURCE_TYPES + ["UNCLASSIFIED"]}})
    return pd.DataFrame(platform_rows), pd.DataFrame(rows), s


def main(tag, provisional):
    rng = np.random.default_rng(SEED)
    TABLES.mkdir(parents=True, exist_ok=True)
    resp, src, det, cr, cb = load(tag)
    bdf = pd.DataFrame([{"brand_id": b["id"], "brand": b["name"], "brand_type": b["brand_type"]} for b in brands_cfg()["brands"]])
    prompts = prompts_df()

    # collection outcomes
    cc = resp.groupby(["platform", "status"]).size().unstack(fill_value=0)
    cc["valid"] = resp.groupby("platform").valid.sum()
    cc.to_csv(TABLES / "collection_by_platform.csv")
    counts = {"prompts": prompts.shape[0], "calls": len(resp), "ok": int(resp.valid.sum()),
              "no_overview": int((resp.status == "no_overview").sum()), "failed": int((resp.status == "failed").sum()),
              "repetitions": int(resp.repetition.max()),
              "ok_not_valid": int(((resp.status == "ok") & ~resp.valid).sum())}
    pd.DataFrame(list(counts.items()), columns=["item", "value"]).to_csv(TABLES / "collection_counts.csv", index=False)
    aio = resp[resp.platform == "aio"].groupby(["category", "prompt_type"]).status.apply(lambda s: (s == "ok").mean())
    aio.rename("aio_shown_rate").reset_index().to_csv(TABLES / "aio_trigger_rate.csv", index=False)

    ment = resolve_mentions(det, cb, provisional)
    todo = export_review(ment, resp, tag)
    qa = {"det_llm_agreement": ment.agree.mean(), "n_disagreements": int((~ment.agree).sum()),
          "n_unresolved": int(ment.unresolved.sum()), "review_file": str(todo.name)}
    for amb, g in ment.groupby("ambiguous_brand"):
        qa[f"agreement_{'ambiguous' if amb else 'unambiguous'}_brands"] = g.agree.mean()
    pos = positions(ment, resp, cr)
    ment = ment.merge(pos, on=["response_id", "brand_id"], how="left")
    ment = ment.merge(bdf, on="brand_id")
    ment.to_csv(INTERIM / f"mentions_final_{tag}.csv", index=False)

    # top pick: map coder's top_pick_raw onto study brands with the alias matcher
    brands = {b["id"]: b for b in brands_cfg()["brands"]}
    comp = {k: compile_brand(v) for k, v in brands.items()}
    tp = cr.set_index("response_id").top_pick_raw.to_dict()
    def top_is(rid, bid):
        t = str(tp.get(rid, "") or "")
        return bool(t) and t.lower() != "none" and bool(find_mentions(t, brands[bid], comp[bid]))
    ment["top_pick"] = [top_is(r, b) for r, b in zip(ment.response_id, ment.brand_id)]
    ment["first_study"] = ment.det_position.eq(1) & ment.mentioned
    # det_position counts only deterministic matches; recompute order among final mentions
    fo = ment[ment.mentioned].sort_values("det_first_offset").groupby("response_id").brand_id.first()
    ment["first_study"] = [bool(m_) and fo.get(r) == b for r, b, m_ in zip(ment.response_id, ment.brand_id, ment.mentioned)]

    meta = resp[["response_id", "prompt_id", "category", "prompt_type", "branded", "platform", "repetition", "valid"]]
    full = ment.merge(meta, on="response_id")
    base = full[full.valid & ~full.branded]  # awareness & prominence use non-branded prompts only

    ap = awareness_prominence(base, rng).merge(bdf, on="brand_id")
    ap.to_csv(TABLES / "awareness_prominence_by_platform.csv", index=False)
    pb = pooled_by_brand(base, rng).merge(bdf, on="brand_id")
    pb.to_csv(TABLES / "awareness_pooled_by_brand.csv", index=False)
    bt = by_type(base, rng)
    bt.to_csv(TABLES / "brand_type_comparison.csv", index=False)
    by_type(base, rng, exclude=("minimalist",)).to_csv(TABLES / "brand_type_comparison_excl_minimalist.csv", index=False)
    gee_check(base).to_csv(TABLES / "gee_brand_type.csv", index=False)
    by_ptype = base.groupby(["category", "prompt_type", "brand_type"]).mentioned.mean().unstack().reset_index()
    by_ptype.to_csv(TABLES / "mention_rate_by_prompt_type.csv", index=False)

    # open set: all brands named in non-branded valid responses (coder list, normalised)
    vr = resp[resp.valid & ~resp.branded][["response_id", "category", "platform"]].merge(cr[["response_id", "all_brands", "n_all_brands"]], on="response_id")
    ob = []
    for x in vr.itertuples():
        for n in {_norm(v) for v in json.loads(x.all_brands or "[]")}:
            ob.append({"response_id": x.response_id, "category": x.category, "platform": x.platform, "brand_norm": n})
    ob = pd.DataFrame(ob)
    if len(ob):
        open_set = (ob.groupby(["category", "brand_norm"]).response_id.nunique() /
                    ob.groupby("category").response_id.nunique().reindex(ob.category.unique())).rename("response_share")
        open_set = open_set.reset_index().sort_values(["category", "response_share"], ascending=[True, False])
        open_set.to_csv(TABLES / "open_set_brands.csv", index=False)
        vr.groupby(["category", "platform"]).n_all_brands.agg(["mean", "median"]).reset_index().to_csv(
            TABLES / "brands_per_answer.csv", index=False)

    # stability
    vresp = resp[resp.valid & ~resp.branded].copy()
    tpn = cr.set_index("response_id").top_pick_raw.map(lambda s: _norm(s) if s and str(s).lower() != "none" else "none")
    vresp["top_pick_norm"] = vresp.response_id.map(tpn).fillna("none")
    per, agg = stability(vresp, full, cr, rng)
    per.to_csv(TABLES / "stability_by_prompt_platform.csv", index=False)
    agg.to_csv(TABLES / "stability_summary.csv", index=False)
    cross_platform(vresp, full, cr).to_csv(TABLES / "stability_cross_platform.csv", index=False)

    # image (all valid responses, branded included)
    allv = full[full.valid]
    img, attrs, img_rows = image(allv, cb, resp)
    img.merge(bdf, on="brand_id").to_csv(TABLES / "image_by_brand.csv", index=False)
    attrs.merge(bdf, on="brand_id").to_csv(TABLES / "attributes_by_brand.csv", index=False)

    # credibility
    dt_path = CONFIG / "domain_types.csv"
    dtypes = pd.read_csv(dt_path) if dt_path.exists() else pd.DataFrame(columns=["domain", "source_type"])
    pl_mix, br_mix, s = credibility(allv, src, resp, dtypes[["domain", "source_type"]])
    pl_mix.to_csv(TABLES / "sources_by_platform.csv", index=False)
    br_mix.merge(bdf, on="brand_id").to_csv(TABLES / "sources_by_brand.csv", index=False)
    unk = s[s.source_type == "UNCLASSIFIED"].domain.value_counts().rename("n").reset_index()
    unk.to_csv(INTERIM / f"unclassified_domains_{tag}.csv", index=False)
    qa["n_unclassified_domains"] = int(len(unk))
    qa["unclassified_source_share"] = float((s.source_type == "UNCLASSIFIED").mean()) if len(s) else 0.0
    # brand-type source mix (sources attached to responses mentioning brands of each type)
    tm = []
    for bt_, g in allv[allv.mentioned].groupby("brand_type"):
        ss = s[s.response_id.isin(g.response_id)]
        mix = ss.source_type.value_counts(normalize=True)
        tm.append({"brand_type": bt_, "n_responses": g.response_id.nunique(), "n_sources": len(ss),
                   **{t: mix.get(t, 0.0) for t in SOURCE_TYPES}})
    pd.DataFrame(tm).to_csv(TABLES / "sources_by_brand_type.csv", index=False)

    pd.DataFrame(list(qa.items()), columns=["item", "value"]).to_csv(TABLES / "qa_summary.csv", index=False)
    print(pd.Series(counts).to_string())
    print(pd.Series(qa).to_string())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="main")
    ap.add_argument("--provisional", action="store_true")
    a = ap.parse_args()
    main(a.tag, a.provisional)
