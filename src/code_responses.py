"""First-pass LLM coding of responses, following config/codebook.md.

The coder is a Claude model (provider independent of the four audited platforms). It sees only
the shopper question and the answer text: it is blind to platform, repetition and brand type.
Output is constrained to a JSON schema that forces a decision for every study brand of the
category. Every request and every raw result is stored append-only so the coding can be audited.

Usage:
  python src/code_responses.py submit  --tag main [--recode-sample 0.10]   # Batches API (50% price)
  python src/code_responses.py collect --batch-id <id>
  python src/code_responses.py sync    --tag pilot                         # small sets, no batch
  python src/code_responses.py table   --tag main
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

import anthropic
import pandas as pd
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CONFIG, INTERIM, LOGS, append_jsonl, brands_cfg, load_env, now_pair, platforms_cfg, read_jsonl  # noqa: E402

CODING = INTERIM / "coding"
RESULTS = CODING / "results.jsonl"
CLAIM_TYPES = ["price", "composition_or_spec", "origin_or_ownership", "other_fact"]


def attribute_codes(category):
    a = pd.read_csv(CONFIG / "attribute_codes.csv")
    return a[a.category == category]


def brand_block(category):
    lines = []
    for b in brands_cfg()["brands"]:
        if b["category"] == category:
            al = sorted(set(b.get("aliases", []) + b.get("aliases_case_sensitive", [])))
            lines.append(f"- {b['id']}: {b['name']} (also written as: {', '.join(al)})")
    return "\n".join(lines)


def system_prompt(category):
    codebook = (CONFIG / "codebook.md").read_text()
    codes = attribute_codes(category)
    code_lines = "\n".join(f"- {r.code}: {r.label}. {r.definition}" for r in codes.itertuples())
    cat_label = brands_cfg()["categories"][category]["label"]
    return (
        "You are a careful content-analysis coder for an academic study. Apply the coding manual "
        "below exactly. Code only what the answer text says; never add outside knowledge.\n\n"
        f"{codebook}\n\n"
        f"## Category for this coding run: {cat_label}\n\n"
        f"### Attribute codes (B3) for this category\n{code_lines}\n\n"
        f"### Study brands for this category (code every one of them under study_brands)\n{brand_block(category)}\n\n"
        "For a study brand that the answer does not refer to, set is_brand_reference to false, stance and "
        "sentiment to \"not_present\", and leave the lists empty."
    )


def schema(category):
    codes = list(attribute_codes(category).code)
    brand_ids = [b["id"] for b in brands_cfg()["brands"] if b["category"] == category]
    brand_obj = {
        "type": "object",
        "properties": {
            "is_brand_reference": {"type": "boolean"},
            "stance": {"type": "string", "enum": ["recommended", "mentioned_neutral", "discouraged", "not_present"]},
            "attributes": {"type": "array", "items": {"type": "string", "enum": codes}},
            "sentiment": {"type": "string", "enum": ["positive", "neutral", "mixed", "negative", "not_present"]},
            "factual_claims": {"type": "array", "items": {
                "type": "object",
                "properties": {"type": {"type": "string", "enum": CLAIM_TYPES}, "text": {"type": "string"}},
                "required": ["type", "text"], "additionalProperties": False}},
            "products": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["is_brand_reference", "stance", "attributes", "sentiment", "factual_claims", "products"],
        "additionalProperties": False,
    }
    return {
        "type": "object",
        "properties": {
            "all_brands": {"type": "array", "items": {"type": "string"}},
            "answer_form": {"type": "string", "enum": ["list", "single", "comparison", "no_recommendation"]},
            "top_pick": {"type": "string"},
            "truncated": {"type": "boolean"},
            "study_brands": {"type": "object", "properties": {bid: brand_obj for bid in brand_ids},
                             "required": brand_ids, "additionalProperties": False},
        },
        "required": ["all_brands", "answer_form", "top_pick", "truncated", "study_brands"],
        "additionalProperties": False,
    }


def user_message(question, answer):
    return (f"Shopper question:\n<question>\n{question}\n</question>\n\n"
            f"Answer to code:\n<answer>\n{answer}\n</answer>\n\n"
            "Return the coding as JSON. For top_pick give the brand name, or \"none\".")


def build_params(row, cfg):
    return MessageCreateParamsNonStreaming(
        model=cfg["model"],
        max_tokens=16000,
        system=[{"type": "text", "text": system_prompt(row.category), "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_message(row.prompt_text, row.text)}],
        output_config={"effort": cfg["effort"], "format": {"type": "json_schema", "schema": schema(row.category)}},
    )


def load_responses(tag):
    df = pd.read_csv(INTERIM / f"responses_{tag}.csv", keep_default_na=False, dtype={"text": str})
    df["valid"] = df["valid"].astype(str).str.lower().eq("true")
    prompts = pd.read_csv(CONFIG / "prompts.csv", dtype=str).set_index("prompt_id")
    df["prompt_text"] = df.prompt_id.map(prompts["text"])
    return df[df.valid]


def coded_ids(pass_no=1):
    return {r["custom_id"].split("__")[0] for r in read_jsonl(RESULTS)
            if r.get("result_type") == "succeeded" and r.get("pass") == pass_no}


def _store_result(custom_id, pass_no, batch_id, result_type, msg=None, error=None):
    rec = {"custom_id": custom_id, "response_id": custom_id.split("__")[0], "pass": pass_no,
           "batch_id": batch_id, "result_type": result_type, "ts_ist": now_pair()[1]}
    if msg is not None:
        rec["model"] = msg.model
        rec["stop_reason"] = msg.stop_reason
        rec["usage"] = msg.usage.model_dump() if msg.usage else None
        text = next((b.text for b in msg.content if b.type == "text"), "")
        rec["output_text"] = text
    if error is not None:
        rec["error"] = str(error)[:2000]
    append_jsonl(RESULTS, rec)


def submit(tag, recode_sample):
    load_env()
    cfg = platforms_cfg()["coder"]
    client = anthropic.Anthropic()
    df = load_responses(tag)
    done1 = coded_ids(1)
    reqs, meta = [], []
    for row in df.itertuples():
        if row.response_id not in done1:
            reqs.append(Request(custom_id=f"{row.response_id}__p1", params=build_params(row, cfg)))
    if recode_sample:
        rng = random.Random(platforms_cfg()["seed"] + 7)
        ids = sorted(df.response_id)
        sample = set(rng.sample(ids, round(len(ids) * recode_sample)))
        done2 = coded_ids(2)
        for row in df.itertuples():
            if row.response_id in sample and row.response_id not in done2:
                reqs.append(Request(custom_id=f"{row.response_id}__p2", params=build_params(row, cfg)))
    if not reqs:
        print("Nothing to submit.")
        return
    CODING.mkdir(parents=True, exist_ok=True)
    batch = client.messages.batches.create(requests=reqs)
    with open(CODING / f"requests_{batch.id}.jsonl", "w") as f:
        for r in reqs:
            f.write(json.dumps({"custom_id": r["custom_id"], "params": r["params"]}, default=str) + "\n")
    with open(LOGS / "coding_batches.csv", "a") as f:
        f.write(f"{batch.id},{tag},{len(reqs)},{now_pair()[1]}\n")
    print(f"Submitted batch {batch.id} with {len(reqs)} requests.")


def collect(batch_id):
    load_env()
    client = anthropic.Anthropic()
    while True:
        b = client.messages.batches.retrieve(batch_id)
        if b.processing_status == "ended":
            break
        print(f"{b.processing_status}: {b.request_counts}", flush=True)
        time.sleep(60)
    n = {"succeeded": 0, "errored": 0, "canceled": 0, "expired": 0}
    for res in client.messages.batches.results(batch_id):
        pass_no = 2 if res.custom_id.endswith("__p2") else 1
        t = res.result.type
        n[t] = n.get(t, 0) + 1
        if t == "succeeded":
            _store_result(res.custom_id, pass_no, batch_id, t, msg=res.result.message)
        elif t == "errored":
            _store_result(res.custom_id, pass_no, batch_id, t, error=res.result.error)
        else:
            _store_result(res.custom_id, pass_no, batch_id, t)
    print(n)


def sync(tag):
    load_env()
    cfg = platforms_cfg()["coder"]
    client = anthropic.Anthropic()
    df = load_responses(tag)
    done = coded_ids(1)
    for row in df.itertuples():
        if row.response_id in done:
            continue
        try:
            msg = client.messages.create(**build_params(row, cfg))
            _store_result(f"{row.response_id}__p1", 1, "sync", "succeeded", msg=msg)
        except anthropic.APIStatusError as e:
            _store_result(f"{row.response_id}__p1", 1, "sync", "errored", error=e)
        print(".", end="", flush=True)
    print()


def table(tag):
    df = load_responses(tag).set_index("response_id")
    resp_rows, brand_rows, claim_rows, problems = [], [], [], []
    latest = {}
    for r in read_jsonl(RESULTS):
        if r["result_type"] == "succeeded":
            latest[(r["response_id"], r["pass"])] = r  # last successful result per response and pass
    for (rid, pass_no), r in latest.items():
        if rid not in df.index:
            continue
        if r.get("stop_reason") != "end_turn":
            problems.append((rid, pass_no, f"stop_reason={r.get('stop_reason')}"))
            continue
        try:
            js = json.loads(r["output_text"])
        except json.JSONDecodeError as e:
            problems.append((rid, pass_no, f"json: {e}"))
            continue
        resp_rows.append({"response_id": rid, "pass": pass_no, "coder_model": r.get("model"),
                          "answer_form": js["answer_form"], "top_pick_raw": js["top_pick"],
                          "truncated": js["truncated"], "all_brands": json.dumps(js["all_brands"], ensure_ascii=False),
                          "n_all_brands": len(js["all_brands"])})
        for bid, v in js["study_brands"].items():
            brand_rows.append({"response_id": rid, "pass": pass_no, "brand_id": bid,
                               "llm_reference": v["is_brand_reference"], "stance": v["stance"],
                               "sentiment": v["sentiment"], "attributes": "|".join(sorted(set(v["attributes"]))),
                               "products": json.dumps(v["products"], ensure_ascii=False),
                               "n_claims": len(v["factual_claims"])})
            for i, c in enumerate(v["factual_claims"]):
                claim_rows.append({"claim_id": f"{rid}__{bid}__{i}", "response_id": rid, "pass": pass_no,
                                   "brand_id": bid, "claim_type": c["type"], "claim_text": c["text"]})
    out = INTERIM
    pd.DataFrame(resp_rows).to_csv(out / f"coded_responses_{tag}.csv", index=False)
    pd.DataFrame(brand_rows).to_csv(out / f"coded_brands_{tag}.csv", index=False)
    pd.DataFrame(claim_rows).to_csv(out / f"coded_claims_{tag}.csv", index=False)
    pd.DataFrame(problems, columns=["response_id", "pass", "problem"]).to_csv(out / f"coding_problems_{tag}.csv", index=False)
    print(f"responses coded: {len({x['response_id'] for x in resp_rows if x['pass'] == 1})} of {len(df)}; "
          f"problems: {len(problems)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("submit"); s.add_argument("--tag", required=True); s.add_argument("--recode-sample", type=float, default=0.0)
    c = sub.add_parser("collect"); c.add_argument("--batch-id", required=True)
    y = sub.add_parser("sync"); y.add_argument("--tag", required=True)
    t = sub.add_parser("table"); t.add_argument("--tag", required=True)
    a = ap.parse_args()
    {"submit": lambda: submit(a.tag, a.recode_sample), "collect": lambda: collect(a.batch_id),
     "sync": lambda: sync(a.tag), "table": lambda: table(a.tag)}[a.cmd]()
