"""Factual accuracy of model claims about study brands (RQ2).

Each factual claim extracted by the coder (price, composition/specification, origin/ownership,
other fact) is compared with data/manual/fact_sheets.csv, which holds official facts with source
URLs. The comparison is done by the same independent LLM coder, in batch, using ONLY the fact
sheet rows supplied; a claim the fact sheet cannot settle is 'unverifiable'. A random sample of
verdicts is exported for human checking.

  python src/check_claims.py submit  --tag main
  python src/check_claims.py collect --batch-id <id>
  python src/check_claims.py table   --tag main
  python src/check_claims.py sample  --tag main --n 120     -> outputs/claim_check_sample.xlsx
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import anthropic
import pandas as pd
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import INTERIM, LOGS, MANUAL, ROOT, TABLES, append_jsonl, brands_cfg, load_env, now_pair, platforms_cfg, read_jsonl  # noqa: E402

OUT = INTERIM / "claim_checks.jsonl"
SYSTEM = (
    "You check factual claims that an AI assistant made about a brand against an official fact sheet. "
    "Use ONLY the fact sheet rows provided; do not use outside knowledge. For each claim return:\n"
    "- correct: a fact sheet row confirms it. A price is correct if it is within 20% of the official MRP of the "
    "product named, or within the brand's official price range when no product is named.\n"
    "- incorrect: a fact sheet row contradicts it (for example a different concentration, a price more than 20% "
    "away from MRP, a wrong parent company, a feature the product does not have).\n"
    "- unverifiable: no row confirms or contradicts it, including claims about products not on the sheet.\n"
    "Cite the row ids you relied on. Be conservative: if in doubt, choose unverifiable."
)
SCHEMA = {
    "type": "object",
    "properties": {"verdicts": {"type": "array", "items": {
        "type": "object",
        "properties": {"claim_index": {"type": "integer"},
                       "verdict": {"type": "string", "enum": ["correct", "incorrect", "unverifiable"]},
                       "fact_row_ids": {"type": "array", "items": {"type": "integer"}},
                       "reason": {"type": "string"}},
        "required": ["claim_index", "verdict", "fact_row_ids", "reason"], "additionalProperties": False}}},
    "required": ["verdicts"], "additionalProperties": False,
}


def units(tag):
    claims = pd.read_csv(INTERIM / f"coded_claims_{tag}.csv")
    claims = claims[claims["pass"] == 1]
    ment = pd.read_csv(INTERIM / f"mentions_final_{tag}.csv")
    ment = ment[ment.mentioned.astype(str) == "True"][["response_id", "brand_id"]]
    claims = claims.merge(ment, on=["response_id", "brand_id"])  # only claims about brands actually named
    facts = pd.read_csv(MANUAL / "fact_sheets.csv")
    facts = facts.reset_index().rename(columns={"index": "row_id"})
    facts.to_csv(INTERIM / "fact_sheets_indexed.csv", index=False)
    return claims, facts


def build(claims, facts, cfg):
    names = {b["id"]: b["name"] for b in brands_cfg()["brands"]}
    reqs = []
    for (rid, bid), g in claims.groupby(["response_id", "brand_id"]):
        f = facts[facts.brand_id == bid]
        sheet = "\n".join(f"[{r.row_id}] {r.product} | {r.fact_type} | {r.fact_value}" for r in f.itertuples()) or "(no rows)"
        cl = "\n".join(f"{i}. ({c.claim_type}) {c.claim_text}" for i, c in enumerate(g.itertuples()))
        msg = f"Brand: {names[bid]}\n\nFact sheet:\n{sheet}\n\nClaims:\n{cl}\n\nReturn a verdict for every claim index."
        reqs.append(Request(custom_id=f"{rid}__{bid}", params=MessageCreateParamsNonStreaming(
            model=cfg["model"], max_tokens=8000, system=SYSTEM,
            messages=[{"role": "user", "content": msg}],
            output_config={"effort": cfg["effort"], "format": {"type": "json_schema", "schema": SCHEMA}})))
    return reqs


def submit(tag):
    load_env()
    cfg = platforms_cfg()["coder"]
    claims, facts = units(tag)
    done = {r["custom_id"] for r in read_jsonl(OUT) if r.get("result_type") == "succeeded"}
    reqs = [r for r in build(claims, facts, cfg) if r["custom_id"] not in done]
    if not reqs:
        print("nothing to submit"); return
    b = anthropic.Anthropic().messages.batches.create(requests=reqs)
    with open(LOGS / "coding_batches.csv", "a") as f:
        f.write(f"{b.id},claims_{tag},{len(reqs)},{now_pair()[1]}\n")
    print("submitted", b.id, len(reqs))


def collect(batch_id):
    load_env()
    c = anthropic.Anthropic()
    while c.messages.batches.retrieve(batch_id).processing_status != "ended":
        time.sleep(60)
    for res in c.messages.batches.results(batch_id):
        rec = {"custom_id": res.custom_id, "result_type": res.result.type, "batch_id": batch_id, "ts_ist": now_pair()[1]}
        if res.result.type == "succeeded":
            m = res.result.message
            rec.update(model=m.model, stop_reason=m.stop_reason,
                       output_text=next((b.text for b in m.content if b.type == "text"), ""))
        append_jsonl(OUT, rec)
    print("collected", batch_id)


def table(tag):
    claims, facts = units(tag)
    latest = {r["custom_id"]: r for r in read_jsonl(OUT) if r.get("result_type") == "succeeded" and r.get("stop_reason") == "end_turn"}
    rows = []
    for (rid, bid), g in claims.groupby(["response_id", "brand_id"]):
        r = latest.get(f"{rid}__{bid}")
        v = {x["claim_index"]: x for x in json.loads(r["output_text"])["verdicts"]} if r else {}
        for i, c in enumerate(g.itertuples()):
            x = v.get(i, {})
            rows.append({"claim_id": c.claim_id, "response_id": rid, "brand_id": bid, "claim_type": c.claim_type,
                         "claim_text": c.claim_text, "verdict": x.get("verdict", "not_checked"),
                         "fact_row_ids": json.dumps(x.get("fact_row_ids", [])), "reason": x.get("reason", "")})
    t = pd.DataFrame(rows)
    t.to_csv(INTERIM / f"claim_verdicts_{tag}.csv", index=False)
    resp = pd.read_csv(INTERIM / f"responses_{tag}.csv", usecols=["response_id", "platform"])
    t = t.merge(resp, on="response_id")
    bdf = pd.DataFrame([{"brand_id": b["id"], "brand": b["name"], "brand_type": b["brand_type"]} for b in brands_cfg()["brands"]])
    def summ(g):
        n_c, n_i, n_u = (g.verdict == "correct").sum(), (g.verdict == "incorrect").sum(), (g.verdict == "unverifiable").sum()
        return pd.Series({"n_claims": len(g), "correct": n_c, "incorrect": n_i, "unverifiable": n_u,
                          "accuracy_rate": n_c / (n_c + n_i) if (n_c + n_i) else float("nan"),
                          "unverifiable_share": n_u / len(g) if len(g) else float("nan")})
    t.groupby("brand_id").apply(summ).reset_index().merge(bdf, on="brand_id").to_csv(TABLES / "accuracy_by_brand.csv", index=False)
    t.groupby("platform").apply(summ).reset_index().to_csv(TABLES / "accuracy_by_platform.csv", index=False)
    t.groupby("claim_type").apply(summ).reset_index().to_csv(TABLES / "accuracy_by_claim_type.csv", index=False)
    t.merge(bdf, on="brand_id").groupby("brand_type").apply(summ).reset_index().to_csv(TABLES / "accuracy_by_brand_type.csv", index=False)
    print(t.verdict.value_counts().to_string())


def sample(tag, n):
    t = pd.read_csv(INTERIM / f"claim_verdicts_{tag}.csv")
    s = t[t.verdict != "not_checked"].sample(n=min(n, len(t)), random_state=platforms_cfg()["seed"] + 23)
    s = s[["claim_id", "brand_id", "claim_type", "claim_text", "fact_row_ids"]].assign(human_verdict="", checked_by="", note="")
    s.to_excel(ROOT / "outputs" / "claim_check_sample.xlsx", index=False)
    print("wrote outputs/claim_check_sample.xlsx with", len(s), "claims (LLM verdict hidden)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["submit", "collect", "table", "sample"])
    ap.add_argument("--tag", default="main"); ap.add_argument("--batch-id"); ap.add_argument("--n", type=int, default=120)
    a = ap.parse_args()
    {"submit": lambda: submit(a.tag), "collect": lambda: collect(a.batch_id), "table": lambda: table(a.tag),
     "sample": lambda: sample(a.tag, a.n)}[a.cmd]()
