"""Parse raw platform records into one tidy row per response.

Output: data/interim/responses.csv  (one row per collected call, failures included)
        data/interim/sources.csv    (one row per displayed source attached to a response)

'Displayed sources' are the sources a user of the platform would see attached to the answer:
  ChatGPT     url_citation annotations on the answer text
  Gemini      url_citation annotations on the answer text
  Perplexity  search_results returned with the answer (shown as source cards)
  AI Overview references listed in the overview panel
Sources the model consulted but did not display (ChatGPT web_search_call sources) are kept
separately as 'consulted' and are not used in the citation-mix measure.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import tldextract

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import INTERIM, PLATFORM_ORDER, RAW, prompts_df, read_jsonl  # noqa: E402

_EXTRACT = tldextract.TLDExtract(suffix_list_urls=())  # bundled snapshot, no network call
REDIRECT_HOSTS = ("vertexaisearch.cloud.google.com", "grounding-api-redirect")


def reg_domain(url: str | None, title: str | None = None) -> str | None:
    if not url:
        return None
    host = (urlparse(url).hostname or "").lower()
    if any(h in url for h in REDIRECT_HOSTS):
        # Gemini wraps sources in redirect links; the title field carries the source domain.
        host = (title or "").strip().lower()
        if " " in host or "." not in host:
            return None
    ext = _EXTRACT(host)
    d = ".".join(p for p in (ext.domain, ext.suffix) if p)
    return d or None


# ------------------------------------------------------------------ per-platform extraction

def ex_chatgpt(js):
    text_parts, cited, consulted, queries = [], [], [], []
    for item in js.get("output", []) or []:
        t = item.get("type")
        if t == "message":
            for c in item.get("content", []) or []:
                if c.get("type") == "output_text":
                    text_parts.append(c.get("text", ""))
                    for a in c.get("annotations", []) or []:
                        if a.get("type") == "url_citation":
                            cited.append({"url": a.get("url"), "title": a.get("title")})
        elif t == "web_search_call":
            act = item.get("action") or {}
            if act.get("query"):
                queries.append(act["query"])
            for q in act.get("queries", []) or []:
                queries.append(q)
            for s in act.get("sources", []) or []:
                consulted.append({"url": s.get("url"), "title": s.get("title")})
    return "\n".join(text_parts), cited, consulted, queries


def _walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from _walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from _walk(v)


def ex_gemini(js):
    text_parts, cited, queries = [], [], []
    steps = js.get("steps") or js.get("outputs") or []
    found_output = False
    for st in steps:
        if st.get("type") == "google_search_call":
            queries += (st.get("arguments") or {}).get("queries", []) or []
        if st.get("type") in ("model_output", "text"):
            found_output = True
            contents = st.get("content") if st.get("type") == "model_output" else [st]
            for c in contents or []:
                if c.get("type") == "text":
                    text_parts.append(c.get("text", ""))
                    for a in c.get("annotations", []) or []:
                        if a.get("type") == "url_citation":
                            cited.append({"url": a.get("url"), "title": a.get("title")})
    if not found_output:  # defensive fallback for an unexpected envelope
        for d in _walk(js):
            if d.get("type") == "text" and isinstance(d.get("text"), str):
                text_parts.append(d["text"])
                for a in d.get("annotations", []) or []:
                    if a.get("type") == "url_citation":
                        cited.append({"url": a.get("url"), "title": a.get("title")})
    return "\n".join(text_parts), cited, [], queries


def ex_perplexity(js):
    text = js.get("output_text") or ""
    listed, queries, parts = [], [], []
    for item in js.get("output", []) or []:
        t = item.get("type")
        if t == "message" and not text:
            for c in item.get("content", []) or []:
                if c.get("type") in ("output_text", "text"):
                    parts.append(c.get("text", ""))
        elif t == "search_results":
            for r in item.get("results", []) or []:
                listed.append({"url": r.get("url"), "title": r.get("title"), "id": r.get("id")})
            queries += item.get("queries", []) or []
    if not text:
        text = "\n".join(parts)
    if not listed:
        for r in js.get("search_results", []) or []:
            listed.append({"url": r.get("url"), "title": r.get("title"), "id": r.get("id")})
        for u in js.get("citations", []) or []:
            if isinstance(u, str) and not any(x["url"] == u for x in listed):
                listed.append({"url": u, "title": None})
    return text, listed, [], queries


def _aio_blocks_to_text(blocks, depth=0):
    out = []
    for b in blocks or []:
        t = b.get("type")
        snip = b.get("snippet") or ""
        if t == "heading":
            out.append(snip)
        elif t == "paragraph":
            out.append(snip)
        elif t == "list":
            for it in b.get("list", []) or []:
                line = " ".join(x for x in (it.get("title"), it.get("snippet")) if x)
                out.append("  " * depth + "- " + line)
                if it.get("list"):
                    out.append(_aio_blocks_to_text([{"type": "list", "list": it["list"]}], depth + 1))
        elif t == "table":
            for row in b.get("table", []) or []:
                out.append(" | ".join(str(c) for c in row))
        elif t == "expandable":
            if snip:
                out.append(snip)
            out.append(_aio_blocks_to_text(b.get("text_blocks"), depth))
        elif t == "comparison":
            out.append(" | ".join(b.get("product_labels", []) or []))
            for row in b.get("comparison", []) or []:
                out.append(f"{row.get('feature', '')}: " + " | ".join(str(v) for v in row.get("values", []) or []))
        elif snip:
            out.append(snip)
    return "\n".join(x for x in out if x)


def ex_aio(js):
    if "ai_overview_followup" in js:
        aio = js["ai_overview_followup"].get("ai_overview") or {}
    else:
        aio = js.get("ai_overview") or {}
    text = _aio_blocks_to_text(aio.get("text_blocks"))
    refs = [{"url": r.get("link"), "title": r.get("title"), "source": r.get("source")}
            for r in aio.get("references", []) or []]
    return text, refs, [], []


EXTRACT = {"chatgpt": ex_chatgpt, "gemini": ex_gemini, "perplexity": ex_perplexity, "aio": ex_aio}


def parse_all(batches=("main",)):
    prompts = prompts_df().set_index("prompt_id")
    rows, srcs = [], []
    for pl in PLATFORM_ORDER:
        for r in read_jsonl(RAW / f"{pl}.jsonl"):
            if r["batch"] not in batches:
                continue
            text, shown, consulted, queries = "", [], [], []
            if r["status"] == "ok":
                text, shown, consulted, queries = EXTRACT[pl](r["raw_response"] or {})
            p = prompts.loc[r["prompt_id"]]
            rows.append({
                "response_id": r["run_uuid"], "batch": r["batch"], "prompt_id": r["prompt_id"],
                "category": p["category"], "prompt_type": p["prompt_type"], "branded": bool(p["branded"]),
                "platform": pl, "repetition": r["repetition"], "status": r["status"],
                "valid": r["status"] == "ok" and bool(text.strip()),
                "model_returned": r.get("model_returned"), "ts_ist_start": r["ts_ist_start"],
                "attempts": r["attempts"], "n_words": len(text.split()),
                "n_sources_displayed": len(shown), "n_sources_consulted": len(consulted),
                "searched": bool(queries or shown or consulted) if pl != "aio" else True,
                "search_queries": json.dumps(queries, ensure_ascii=False), "text": text,
            })
            for i, s in enumerate(shown):
                srcs.append({"response_id": r["run_uuid"], "platform": pl, "kind": "displayed", "rank": i + 1,
                             "url": s.get("url"), "title": s.get("title"),
                             "domain": reg_domain(s.get("url"), s.get("title") or s.get("source"))})
            for i, s in enumerate(consulted):
                srcs.append({"response_id": r["run_uuid"], "platform": pl, "kind": "consulted", "rank": i + 1,
                             "url": s.get("url"), "title": s.get("title"),
                             "domain": reg_domain(s.get("url"), s.get("title"))})
    resp = pd.DataFrame(rows)
    src = pd.DataFrame(srcs, columns=["response_id", "platform", "kind", "rank", "url", "title", "domain"])
    return resp, src


if __name__ == "__main__":
    batches = tuple(sys.argv[1].split(",")) if len(sys.argv) > 1 else ("main",)
    resp, src = parse_all(batches)
    tag = "_".join(batches)
    INTERIM.mkdir(parents=True, exist_ok=True)
    resp.to_csv(INTERIM / f"responses_{tag}.csv", index=False)
    src.to_csv(INTERIM / f"sources_{tag}.csv", index=False)
    print(resp.groupby(["platform", "status"]).size().to_string())
    print(f"{len(resp)} responses, {len(src)} source rows -> data/interim/responses_{tag}.csv")
