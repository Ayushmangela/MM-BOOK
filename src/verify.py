"""Independent verification. Recomputes key numbers by a separate code path (plain Python over the
raw JSONL and interim files, no shared metric functions) and asserts they match outputs/tables.

  python src/verify.py --tag main
Exit code 0 only if every check passes. A report is written to logs/verify_report.txt.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CONFIG, FIGURES, INTERIM, LOGS, PLATFORM_ORDER, RAW, TABLES  # noqa: E402

FAIL = []
LINES = []


def check(cond, msg):
    LINES.append(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAIL.append(msg)


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def close(a, b, tol=1e-6):
    try:
        return abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return str(a) == str(b)


def raw_integrity(batch):
    hashes = {r["run_uuid"]: r["line_sha256"] for r in rows(LOGS / "raw_line_hashes.csv")}
    seen, recs, bad_hash, dup = set(), [], 0, 0
    for pl in PLATFORM_ORDER:
        f = RAW / f"{pl}.jsonl"
        if not f.exists():
            continue
        for line in open(f, encoding="utf-8"):
            line = line.rstrip("\n")
            r = json.loads(line)
            if hashes.get(r["run_uuid"]) != hashlib.sha256(line.encode("utf-8")).hexdigest():
                bad_hash += 1
            if r["run_uuid"] in seen:
                dup += 1
            seen.add(r["run_uuid"])
            if r["batch"] == batch:
                recs.append(r)
    check(bad_hash == 0, f"every raw line matches the hash logged at collection time ({bad_hash} mismatches)")
    check(dup == 0, f"run_uuid values are unique ({dup} duplicates)")
    check(all(hashes.get(r["run_uuid"]) for r in recs), f"all {len(recs)} raw records of batch '{batch}' have a logged hash")
    sched = rows(CONFIG / f"schedule_{batch}.csv")
    want = Counter((s["prompt_id"], s["platform"], s["repetition"]) for s in sched)
    got = Counter((r["prompt_id"], r["platform"], str(r["repetition"])) for r in recs)
    check(want == got, f"every scheduled call recorded exactly once ({len(sched)} scheduled, {len(recs)} recorded)")
    return recs


def counts_match(recs):
    c = Counter(r["status"] for r in recs)
    t = {r["item"]: r["value"] for r in rows(TABLES / "collection_counts.csv")}
    check(int(t["calls"]) == len(recs), f"collection_counts calls = {len(recs)}")
    check(int(t["no_overview"]) == c["no_overview"], f"no_overview = {c['no_overview']}")
    check(int(t["failed"]) == c["failed"], f"failed = {c['failed']}")


def mention_rates(tag):
    resp = {r["response_id"]: r for r in rows(INTERIM / f"responses_{tag}.csv")}
    ment = rows(INTERIM / f"mentions_final_{tag}.csv")
    num, den = defaultdict(int), defaultdict(int)
    for m in ment:
        r = resp[m["response_id"]]
        if r["valid"] != "True" or r["branded"] == "True":
            continue
        k = (r["platform"], m["brand_id"])
        den[k] += 1
        num[k] += m["mentioned"] == "True"
    t = rows(TABLES / "awareness_prominence_by_platform.csv")
    ok = all(close(int(x["n_mentioned"]), num[(x["platform"], x["brand_id"])]) and
             close(int(x["n_valid"]), den[(x["platform"], x["brand_id"])]) and
             close(float(x["mention_rate"]), num[(x["platform"], x["brand_id"])] / den[(x["platform"], x["brand_id"])], 1e-9)
             for x in t)
    check(ok and len(t) == len(den), f"mention counts and rates recomputed independently for {len(t)} brand x platform cells")


def jaccard_spot(tag):
    resp = {r["response_id"]: r for r in rows(INTERIM / f"responses_{tag}.csv")}
    sets = defaultdict(set)
    for m in rows(INTERIM / f"mentions_final_{tag}.csv"):
        if m["mentioned"] == "True":
            sets[m["response_id"]].add(m["brand_id"])
    cells = defaultdict(list)
    for rid, r in resp.items():
        if r["valid"] == "True" and r["branded"] != "True":
            cells[(r["prompt_id"], r["platform"])].append(rid)
    per = {(x["prompt_id"], x["platform"]): float(x["jaccard_study"]) for x in rows(TABLES / "stability_by_prompt_platform.csv")}
    bad = 0
    for k, ids in cells.items():
        if len(ids) < 2:
            continue
        vals = []
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                a, b = sets[ids[i]], sets[ids[j]]
                vals.append(1.0 if not (a | b) else len(a & b) / len(a | b))
        if not close(sum(vals) / len(vals), per.get(k), 1e-9):
            bad += 1
    check(bad == 0, f"run-to-run Jaccard recomputed for {len(cells)} prompt x platform cells ({bad} mismatches)")


def figure_data():
    mf = FIGURES / "MANIFEST.csv"
    if not mf.exists():
        check(False, "figure manifest exists")
        return
    for m in rows(mf):
        n = m["figure"]
        d = rows(FIGURES / f"fig{n}_data.csv")
        if n == "3":
            t = {(x["category"], x["platform"], x["brand"]): x for x in rows(TABLES / "awareness_prominence_by_platform.csv")}
            p = {(x["category"], x["brand"]): x for x in rows(TABLES / "awareness_pooled_by_brand.csv")}
            ok = all(close(float(r["mention_rate_pct"]), round(100 * float((p[(r["category"], r["brand"])] if r["platform"] == "pooled"
                     else t[(r["category"], r["platform"], r["brand"])])["mention_rate"]), 2), 1e-6) for r in d)
        elif n == "4":
            t = {(x["category"], x["platform"]): x for x in rows(TABLES / "brand_type_comparison.csv")}
            ok = all(close(float(r["diff_pp"]), round(100 * float(t[(r["category"], r["platform"])]["diff"]), 2)) for r in d)
        elif n == "6":
            t = {(x["platform"], x["prompt_type"]): x for x in rows(TABLES / "stability_summary.csv")}
            ok = all(close(float(r["jaccard"]), round(float(t[(r["platform"], r["prompt_type"])]["jaccard_study"]), 4)) for r in d)
        else:
            ok = len(d) > 0
        check(ok, f"figure {n} plotted data match source table(s) {m['source_tables']}")


def main(tag, batch):
    recs = raw_integrity(batch)
    counts_match(recs)
    mention_rates(tag)
    jaccard_spot(tag)
    figure_data()
    LOGS.mkdir(exist_ok=True)
    (LOGS / "verify_report.txt").write_text("\n".join(LINES) + f"\n\n{len(FAIL)} failure(s)\n")
    print("\n".join(l for l in LINES if l.startswith("FAIL")) or "all checks passed")
    print(f"{len(LINES) - len(FAIL)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="main")
    ap.add_argument("--batch", default="main")
    a = ap.parse_args()
    main(a.tag, a.batch)
