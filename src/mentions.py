"""Deterministic study-brand mention detection (no LLM).

For each valid response, every study brand of the response's category is searched for in the
answer text using its alias list (word boundaries; case-insensitive unless listed under
aliases_case_sensitive). URLs and citation markers are blanked first, keeping character offsets,
so a brand inside a link address is not counted. Position = order of first occurrence among
study brands found in the response.

Ambiguous brands (Minimalist, Plum, Noise, boAt) are flagged; the final mention decision for
those uses the LLM coder's B1 judgement and, where the two disagree, a human decision recorded
in data/manual/ambiguity_review.csv (see resolve_mentions in metrics.py).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import INTERIM, brands_cfg  # noqa: E402

URL_RE = re.compile(r"https?://\S+|www\.\S+|\b[\w.-]+\.(?:com|in|co|org|net|io)(?:/\S*)?\b")
MARKER_RE = re.compile(r"\[\d+(?:,\s*\d+)*\]|【[^】]*】")


def blank(text: str, pattern: re.Pattern) -> str:
    return pattern.sub(lambda m: " " * len(m.group(0)), text)


def clean_text(text: str) -> str:
    return blank(blank(text or "", URL_RE), MARKER_RE)


def compile_brand(b: dict):
    pats = []
    for a in b.get("aliases", []):
        pats.append(re.compile(r"(?<![\w-])" + re.escape(a) + r"(?![\w-])", re.IGNORECASE))
    for a in b.get("aliases_case_sensitive", []):
        pats.append(re.compile(r"(?<![\w-])" + re.escape(a) + r"(?![\w-])"))
    excl = [re.compile(p) for p in b.get("exclude_patterns", []) or []]
    return pats, excl


def find_mentions(text: str, b: dict, compiled=None):
    pats, excl = compiled or compile_brand(b)
    t = clean_text(text)
    excluded_spans = [m.span() for e in excl for m in e.finditer(t)]
    hits = []
    for p in pats:
        for m in p.finditer(t):
            s, e = m.span()
            if any(xs <= s < xe for xs, xe in excluded_spans):
                continue
            hits.append((s, m.group(0)))
    hits.sort()
    return hits


def detect(responses: pd.DataFrame) -> pd.DataFrame:
    brands = brands_cfg()["brands"]
    comp = {b["id"]: compile_brand(b) for b in brands}
    rows = []
    for r in responses[responses.valid].itertuples():
        found = []
        for b in brands:
            if b["category"] != r.category:
                continue
            hits = find_mentions(r.text, b, comp[b["id"]])
            found.append({
                "response_id": r.response_id, "brand_id": b["id"], "det_mentioned": bool(hits),
                "det_first_offset": hits[0][0] if hits else None, "det_n_hits": len(hits),
                "det_surface_forms": "|".join(sorted({h[1] for h in hits})),
                "ambiguous_brand": bool(b.get("ambiguous")),
            })
        present = sorted([f for f in found if f["det_mentioned"]], key=lambda f: f["det_first_offset"])
        for rank, f in enumerate(present, 1):
            f["det_position"] = rank
        rows += found
    out = pd.DataFrame(rows)
    if "det_position" not in out:
        out["det_position"] = None
    return out


if __name__ == "__main__":
    tag = sys.argv[1] if len(sys.argv) > 1 else "main"
    resp = pd.read_csv(INTERIM / f"responses_{tag}.csv", keep_default_na=False,
                       dtype={"text": str}).replace({"valid": {"True": True, "False": False}})
    resp["valid"] = resp["valid"].astype(str).str.lower().eq("true")
    m = detect(resp)
    m.to_csv(INTERIM / f"mentions_det_{tag}.csv", index=False)
    print(m.groupby("brand_id").det_mentioned.sum().to_string())
