"""Collect raw responses from the four platforms.

Usage:
  python src/collect.py schedule --batch main          # build and freeze the randomised call schedule
  python src/collect.py run --batch pilot --pilot      # 2 prompts per category x 4 platforms x 1 repetition
  python src/collect.py run --batch main               # full run (resumable; skips completed calls)
  python src/collect.py models                         # list live model IDs per provider (for confirming config)

Raw records go to data/raw/<platform>.jsonl, append-only. Every line's sha256 is appended to
logs/raw_line_hashes.csv so verify.py can prove no raw line was edited afterwards.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import threading
import time
import traceback
import uuid
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (CONFIG, LOGS, PLATFORM_ORDER, RAW, append_jsonl, load_env, now_pair,  # noqa: E402
                    platforms_cfg, prompts_df, redact)

LOCK = threading.Lock()


# --------------------------------------------------------------------------- platform adapters
# Each adapter returns (status, request_record, raw_json, http_status). status is "ok",
# "no_overview" (AI Overviews only) or raises an exception for a retryable failure.

class CallFailed(Exception):
    def __init__(self, msg, http_status=None, raw=None):
        super().__init__(msg)
        self.http_status = http_status
        self.raw = raw


def _post(url, headers, body, timeout):
    r = requests.post(url, headers=headers, json=body, timeout=timeout)
    try:
        js = r.json()
    except ValueError:
        js = {"_non_json_body": r.text[:5000]}
    if r.status_code >= 400:
        raise CallFailed(f"HTTP {r.status_code}", r.status_code, js)
    return js, r.status_code


def call_chatgpt(prompt, cfg, loc, timeout):
    p = cfg["platforms"]["chatgpt"]
    body = {
        "model": p["model"],
        "input": prompt,
        "tools": [{
            "type": "web_search",
            "user_location": {"type": "approximate", "country": loc["country"], "region": loc["region"],
                              "city": loc["city"], "timezone": loc["timezone"]},
        }],
        "include": ["web_search_call.action.sources"],
    }
    headers = {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}", "Content-Type": "application/json"}
    js, code = _post(p["endpoint"], headers, body, timeout)
    if js.get("status") not in (None, "completed"):
        raise CallFailed(f"response status {js.get('status')}", code, js)
    return "ok", {"endpoint": p["endpoint"], "body": body}, js, code


def call_gemini(prompt, cfg, loc, timeout):
    p = cfg["platforms"]["gemini"]
    body = {"model": p["model"], "input": prompt, "tools": [{"type": "google_search"}]}
    headers = {"x-goog-api-key": os.environ["GEMINI_API_KEY"], "Content-Type": "application/json"}
    js, code = _post(p["endpoint"], headers, body, timeout)
    return "ok", {"endpoint": p["endpoint"], "body": body}, js, code


def call_perplexity(prompt, cfg, loc, timeout):
    p = cfg["platforms"]["perplexity"]
    body = {
        "preset": p["preset"],
        "input": prompt,
        "tools": [{"type": "web_search",
                   "user_location": {"country": loc["country"], "region": loc["region"], "city": loc["city"]}}],
    }
    headers = {"Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}", "Content-Type": "application/json"}
    js, code = _post(p["endpoint"], headers, body, timeout)
    if js.get("status") not in (None, "completed"):
        raise CallFailed(f"response status {js.get('status')}", code, js)
    return "ok", {"endpoint": p["endpoint"], "body": body}, js, code


def call_aio(prompt, cfg, loc, timeout):
    p = cfg["platforms"]["aio"]
    params = dict(p["params"])
    params["q"] = prompt
    shown = dict(params)  # api_key is added only to the live request, never stored
    r = requests.get(p["endpoint"], params={**params, "api_key": os.environ["SERPAPI_API_KEY"]}, timeout=timeout)
    try:
        js = r.json()
    except ValueError:
        raise CallFailed(f"HTTP {r.status_code} non-JSON", r.status_code, {"_non_json_body": r.text[:5000]})
    if r.status_code >= 400 or js.get("error"):
        raise CallFailed(f"HTTP {r.status_code} {js.get('error', '')}"[:300], r.status_code, js)
    record = {"endpoint": p["endpoint"], "params": shown}
    aio = js.get("ai_overview")
    if not aio:
        return "no_overview", record, js, r.status_code
    if aio.get("page_token") and not aio.get("text_blocks"):
        # Google loaded the overview separately; the token expires within about a minute.
        p2 = {"engine": "google_ai_overview", "page_token": aio["page_token"]}
        r2 = requests.get(p["endpoint"], params={**p2, "api_key": os.environ["SERPAPI_API_KEY"]}, timeout=timeout)
        js2 = r2.json()
        record["followup_params"] = {"engine": "google_ai_overview", "page_token": "[stored in raw]"}
        js = {"search": js, "ai_overview_followup": js2}
        aio2 = js2.get("ai_overview") or {}
        if r2.status_code >= 400 or js2.get("error"):
            raise CallFailed(f"follow-up HTTP {r2.status_code} {js2.get('error', '')}"[:300], r2.status_code, js)
        if not aio2.get("text_blocks"):
            return "no_overview", record, js, r2.status_code
        return "ok", record, js, r2.status_code
    if aio.get("error") and not aio.get("text_blocks"):
        raise CallFailed(f"ai_overview error: {aio.get('error')}"[:300], r.status_code, js)
    return "ok", record, js, r.status_code


ADAPTERS = {"chatgpt": call_chatgpt, "gemini": call_gemini, "perplexity": call_perplexity, "aio": call_aio}


def model_returned(platform, js):
    if platform == "aio":
        return "google-ai-overviews"
    if isinstance(js, dict):
        return js.get("model") or js.get("model_version") or js.get("modelVersion")
    return None


# --------------------------------------------------------------------------- schedule

def build_schedule(batch: str, pilot: bool):
    cfg = platforms_cfg()
    prompts = prompts_df()
    if pilot:
        # first generic and first price-band prompt of each category: 4 prompts x 4 platforms x 1 rep
        keep = ["SK-G01", "SK-P01", "AU-G01", "AU-P02"]
        prompts = prompts[prompts.prompt_id.isin(keep)]
        reps = [1]
    else:
        reps = list(range(1, cfg["repetitions"] + 1))
    rows = [(pid, pl, rep) for pid in prompts.prompt_id for pl in PLATFORM_ORDER for rep in reps]
    rng = random.Random(cfg["seed"] if not pilot else cfg["seed"] + 1)
    rng.shuffle(rows)
    df = pd.DataFrame(rows, columns=["prompt_id", "platform", "repetition"])
    df.insert(0, "order", range(1, len(df) + 1))
    out = CONFIG / f"schedule_{batch}.csv"
    if out.exists():
        old = pd.read_csv(out)
        if not old.equals(df):
            sys.exit(f"{out} exists and differs; refusing to overwrite a frozen schedule.")
        print(f"{out} already frozen ({len(df)} calls).")
        return df
    df.to_csv(out, index=False)
    print(f"Wrote {out} with {len(df)} calls (seed {cfg['seed'] if not pilot else cfg['seed'] + 1}).")
    return df


def done_keys(batch):
    keys = set()
    for pl in PLATFORM_ORDER:
        f = RAW / f"{pl}.jsonl"
        if not f.exists():
            continue
        for line in open(f, encoding="utf-8"):
            r = json.loads(line)
            if r.get("batch") == batch:
                keys.add((r["prompt_id"], r["platform"], int(r["repetition"])))
    return keys


# --------------------------------------------------------------------------- runner

def run_one(row, prompts, cfg, batch, secrets):
    pl = row.platform
    prompt_text = prompts.loc[row.prompt_id, "text"]
    attempts, errors = 0, []
    t0_utc, t0_ist = now_pair()
    start = time.time()
    status, req, js, http = "failed", None, None, None
    for attempt in range(1, cfg["max_attempts"] + 1):
        attempts = attempt
        try:
            status, req, js, http = ADAPTERS[pl](prompt_text, cfg, cfg["location"], cfg["timeout_s"])
            break
        except Exception as e:  # noqa: BLE001  (every failure is logged, then retried)
            http = getattr(e, "http_status", None)
            js = getattr(e, "raw", None)
            errors.append({"attempt": attempt, "error": f"{type(e).__name__}: {e}"[:500], "http_status": http,
                           "ts_utc": now_pair()[0]})
            status = "failed"
            if attempt < cfg["max_attempts"]:
                wait = cfg["backoff_s"][min(attempt - 1, len(cfg["backoff_s"]) - 1)]
                if http == 429:
                    wait *= 3
                time.sleep(wait)
    t1_utc, t1_ist = now_pair()
    pcfg = {k: v for k, v in cfg["platforms"][pl].items() if k != "env_key"}
    rec = {
        "run_uuid": str(uuid.uuid4()),
        "batch": batch,
        "schedule_order": int(row.order),
        "prompt_id": row.prompt_id,
        "prompt_text": prompt_text,
        "platform": pl,
        "repetition": int(row.repetition),
        "status": status,
        "attempts": attempts,
        "errors": errors,
        "http_status": http,
        "platform_config": pcfg,
        "request": req,
        "model_returned": model_returned(pl, js) if status != "failed" else None,
        "ts_utc_start": t0_utc, "ts_ist_start": t0_ist, "ts_utc_end": t1_utc, "ts_ist_end": t1_ist,
        "latency_s": round(time.time() - start, 3),
        "raw_response": js,
    }
    rec = redact(rec, secrets)
    with LOCK:
        h = append_jsonl(RAW / f"{pl}.jsonl", rec)
        with open(LOGS / "raw_line_hashes.csv", "a") as f:
            f.write(f"{rec['run_uuid']},{pl},{batch},{h}\n")
        with open(LOGS / f"collect_{batch}.log", "a") as f:
            f.write(f"{t1_ist} {pl:10s} {row.prompt_id} r{row.repetition} #{row.order} {status} "
                    f"attempts={attempts} {rec['latency_s']}s\n")
    return status


def run(batch, pilot, platforms):
    load_env()
    cfg = platforms_cfg()
    for pl in platforms:
        key = cfg["platforms"][pl]["env_key"]
        if not os.environ.get(key):
            sys.exit(f"Missing {key} in .env")
        if cfg["platforms"][pl].get("model") == "TO_CONFIRM":
            sys.exit(f"Set the {pl} model in config/platforms.yaml first (run: python src/collect.py models)")
    secrets = [os.environ.get(cfg["platforms"][pl]["env_key"], "") for pl in PLATFORM_ORDER]
    sched = build_schedule(batch, pilot)
    prompts = prompts_df().set_index("prompt_id")
    done = done_keys(batch)
    LOGS.mkdir(exist_ok=True)
    hashes = LOGS / "raw_line_hashes.csv"
    if not hashes.exists():
        hashes.write_text("run_uuid,platform,batch,line_sha256\n")

    def worker(pl):
        todo = sched[(sched.platform == pl)]
        gap = cfg["platforms"][pl].get("min_interval_s", 1.0)
        n_ok = n_fail = n_none = 0
        for row in todo.itertuples():
            if (row.prompt_id, pl, int(row.repetition)) in done:
                continue
            t = time.time()
            s = run_one(row, prompts, cfg, batch, secrets)
            n_ok += s == "ok"; n_fail += s == "failed"; n_none += s == "no_overview"
            time.sleep(max(0.0, gap - (time.time() - t)))
        print(f"[{pl}] finished: ok={n_ok} failed={n_fail} no_overview={n_none}", flush=True)

    threads = [threading.Thread(target=worker, args=(pl,)) for pl in platforms]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def list_models():
    load_env()
    out = {}
    if os.environ.get("OPENAI_API_KEY"):
        r = requests.get("https://api.openai.com/v1/models",
                         headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"}, timeout=30)
        out["openai"] = sorted(m["id"] for m in r.json().get("data", []))
    if os.environ.get("GEMINI_API_KEY"):
        r = requests.get("https://generativelanguage.googleapis.com/v1beta/models",
                         params={"pageSize": 200}, headers={"x-goog-api-key": os.environ["GEMINI_API_KEY"]}, timeout=30)
        out["gemini"] = sorted(m["name"] for m in r.json().get("models", []))
    for k, v in out.items():
        print(f"== {k} ({len(v)})")
        for m in v:
            print("  ", m)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("schedule"); s1.add_argument("--batch", required=True); s1.add_argument("--pilot", action="store_true")
    s2 = sub.add_parser("run"); s2.add_argument("--batch", required=True); s2.add_argument("--pilot", action="store_true")
    s2.add_argument("--platforms", default=",".join(PLATFORM_ORDER))
    sub.add_parser("models")
    a = ap.parse_args()
    if a.cmd == "schedule":
        build_schedule(a.batch, a.pilot)
    elif a.cmd == "run":
        try:
            run(a.batch, a.pilot, a.platforms.split(","))
        except Exception:
            traceback.print_exc()
            sys.exit(1)
    elif a.cmd == "models":
        list_models()
