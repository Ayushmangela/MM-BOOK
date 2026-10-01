"""Checks on chapter.md: style rules from the project brief, word count, and number traceability.

  python src/text_checks.py style           banned characters/phrases, sentence-length spread
  python src/text_checks.py count           words by section and total (IGI minimum 10,000 incl. references)
  python src/text_checks.py trace           every number in FINDINGS must appear in outputs/tables
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CH = ROOT / "chapter.md"

BANNED = [r"—", r"\bdelve", r"\bcrucial", r"\blandscape\b", r"\bnotably\b", r"\bpivotal\b", r"\bunderscore",
          r"\btapestry\b", r"\brealm\b", r"\bseamless", r"\bholistic\b", r"\bleverag", r"\bmultifaceted\b",
          r"\bin today's\b", r"\bplays? a (crucial|key|vital|significant) role\b", r"\bfurthermore\b", r"\bmoreover\b",
          r"\bit is (important|worth) (to note|noting)\b", r"\bgame[- ]changer\b", r"\bparadigm shift\b",
          r"\bnot (just|only|merely) [^.,;]{1,40}, but\b", r"\bnot [a-z]+ but [a-z]+\b", r"\bnavigat", r"\bcomprehensive\b",
          r"\brobust\b", r"\bboasts?\b", r"\bshowcas", r"\bintricate\b", r"\bever-(evolving|changing)\b", r"\bunlock",
          r"\bin conclusion\b", r"\bsheds? light\b", r"\bstark\b"]


def body_text():
    s = CH.read_text(encoding="utf-8")
    return s


def style():
    s = body_text()
    prose = "\n".join(l for l in s.splitlines() if not l.startswith(("@REF", "@TABLE", "@FIG", "<!--")))
    hits = []
    for pat in BANNED:
        for m in re.finditer(pat, prose, re.IGNORECASE):
            ctx = prose[max(0, m.start() - 50): m.end() + 50].replace("\n", " ")
            hits.append((pat, ctx))
    for p, c in hits:
        print(f"[{p}] ...{c}...")
    sents = [x for x in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", prose)) if len(x.split()) > 3]
    lens = pd.Series([len(x.split()) for x in sents])
    print(f"\n{len(hits)} style hits. Sentences: {len(lens)}, mean {lens.mean():.1f} words, sd {lens.std():.1f}, "
          f"min {lens.min()}, max {lens.max()}, share > 35 words {(lens > 35).mean():.1%}")
    # rhetorical triplets "X, Y and Z" in prose (flag for manual review, not all are wrong)
    tri = re.findall(r"\b\w+(?: \w+)?, \w+(?: \w+)? and \w+(?: \w+)?\b", prose)
    print(f"'A, B and C' lists: {len(tri)} (review manually; lists of named items are fine)")


def count():
    s = body_text()
    s = re.sub(r"^@(TABLE|FIG) .*$", "", s, flags=re.M)
    parts = re.split(r"^# ", s, flags=re.M)
    tot = 0
    for p in parts[1:]:
        title = p.splitlines()[0]
        text = re.sub(r"[@*#]|\bREF\b", " ", p[len(title):])
        n = len(text.split())
        tot += n
        print(f"{n:6d}  {title}")
    # tables generated from CSVs count too
    tw = 0
    for f in ["table1_brands.csv", "table2_prompt_design.csv", "table3_measures.csv", "appendix_prompts.csv"]:
        fp = ROOT / "outputs" / "tables" / f
        if fp.exists():
            tw += len(fp.read_text().replace(",", " ").split())
    print(f"{tot:6d}  TOTAL prose incl. references ({tw} more words in design tables)")


def trace():
    s = body_text()
    f = s[s.index("# FINDINGS"): s.index("# DISCUSSION")]
    nums = re.findall(r"(?<![\w.])(\d{1,3}(?:,\d{3})*(?:\.\d+)?)(%| percentage points| pp)?", f)
    pool = set()
    for csv in (ROOT / "outputs" / "tables").glob("*.csv"):
        df = pd.read_csv(csv)
        for v in df.select_dtypes("number").to_numpy().ravel():
            if pd.isna(v):
                continue
            for x in (v, 100 * v):
                for d in (0, 1, 2):
                    pool.add(f"{round(x, d):.{d}f}")
            pool.add(f"{int(round(v)):,}")
        for v in df.select_dtypes("object").to_numpy().ravel():
            pool.update(re.findall(r"\d+(?:\.\d+)?", str(v)))
    ignore = {"1", "2", "3", "4", "5", "6", "10", "20", "95", "2026", "2025", "2024", "2027"}
    missing = [(n, u) for n, u in nums if n.replace(",", "") not in {p.replace(",", "") for p in pool} and n not in ignore]
    print(f"{len(nums)} numbers in FINDINGS; {len(missing)} not found in outputs/tables:")
    for n, u in missing:
        print("   ", n, u)
    return missing


if __name__ == "__main__":
    {"style": style, "count": count, "trace": trace}[sys.argv[1]]()
