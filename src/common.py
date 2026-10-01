"""Shared paths, config loading and small helpers. No secrets are ever logged."""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import yaml

# MMBOOK_ROOT lets the test harness run the pipeline on synthetic data in a scratch folder.
ROOT = Path(os.environ.get("MMBOOK_ROOT", Path(__file__).resolve().parents[1]))
CONFIG = Path(__file__).resolve().parents[1] / "config"
RAW = ROOT / "data" / "raw"
INTERIM = ROOT / "data" / "interim"
MANUAL = ROOT / "data" / "manual"
TABLES = ROOT / "outputs" / "tables"
FIGURES = ROOT / "outputs" / "figures"
LOGS = ROOT / "logs"

IST = timezone(timedelta(hours=5, minutes=30))
PLATFORM_ORDER = ["chatgpt", "gemini", "perplexity", "aio"]
PLATFORM_LABEL = {"chatgpt": "ChatGPT", "gemini": "Gemini", "perplexity": "Perplexity", "aio": "AI Overviews"}


def load_env() -> None:
    """Read KEY=VALUE lines from .env into os.environ without printing anything."""
    env = Path(__file__).resolve().parents[1] / ".env"
    if not env.exists():
        return
    for line in env.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        v = v.strip().strip('"').strip("'")
        if v:
            os.environ.setdefault(k.strip(), v)


def platforms_cfg() -> dict:
    return yaml.safe_load((CONFIG / "platforms.yaml").read_text())


def brands_cfg() -> dict:
    return yaml.safe_load((CONFIG / "brands.yaml").read_text())


def brands_df() -> pd.DataFrame:
    b = brands_cfg()["brands"]
    return pd.DataFrame([{k: x[k] for k in ("id", "name", "category", "brand_type")} for x in b])


def prompts_df() -> pd.DataFrame:
    df = pd.read_csv(CONFIG / "prompts.csv", dtype=str, keep_default_na=False)
    df["branded"] = df["branded"].str.lower().eq("true")
    return df


def now_pair() -> tuple[str, str]:
    t = datetime.now(timezone.utc)
    return t.isoformat(timespec="milliseconds"), t.astimezone(IST).isoformat(timespec="milliseconds")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def append_jsonl(path: Path, rec: dict) -> str:
    """Append one record; return the sha256 of the exact line written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(rec, ensure_ascii=False, sort_keys=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
        f.flush()
        os.fsync(f.fileno())
    return sha256_text(line)


def redact(obj, secrets: list[str]):
    """Remove any secret value that might appear inside a stored request/response."""
    s = json.dumps(obj, ensure_ascii=False)
    for sec in secrets:
        if sec:
            s = s.replace(sec, "[REDACTED]")
    return json.loads(s)
