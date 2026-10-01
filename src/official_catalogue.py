"""Snapshot official product catalogues from brands' own Shopify storefronts (public /products.json).

These are the brands' own official sites, used only as the reference for checking factual claims
(price, ingredients, specifications). One paginated request series per brand, with a pause between
pages. Raw JSON is kept unchanged in data/manual/official_catalogues/; a flat table is derived.

  python src/official_catalogue.py
"""
from __future__ import annotations

import html
import json
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import MANUAL, now_pair  # noqa: E402

SITES = {"minimalist": "https://beminimalist.co", "dermaco": "https://thedermaco.com", "plum": "https://plumgoodness.com",
         "lakme": "https://www.lakmeindia.com", "boat": "https://www.boat-lifestyle.com", "noise": "https://www.gonoise.com",
         "boult": "https://www.boultaudio.com"}
UA = {"User-Agent": "Mozilla/5.0 (academic research; brand fact verification)"}


def strip(h):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h or "", flags=re.S | re.I)
    t = re.sub(r"<br\s*/?>|</p>|</li>|</h\d>", "\n", t, flags=re.I)
    return re.sub(r"[ \t]+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).strip()


def main():
    out_dir = MANUAL / "official_catalogues"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts_utc, ts_ist = now_pair()
    day = ts_ist[:10]
    rows = []
    for bid, base in SITES.items():
        products, page = [], 1
        while True:
            r = requests.get(f"{base}/products.json", params={"limit": 250, "page": page}, headers=UA, timeout=60)
            r.raise_for_status()
            batch = r.json().get("products", [])
            if not batch:
                break
            products += batch
            page += 1
            time.sleep(2)
        (out_dir / f"{bid}_{day}.json").write_text(json.dumps({"retrieved_utc": ts_utc, "source": f"{base}/products.json",
                                                                 "products": products}, ensure_ascii=False))
        for p in products:
            desc = strip(p.get("body_html"))
            for v in p.get("variants", []):
                price = float(v["price"]) if v.get("price") else None
                cap = float(v["compare_at_price"]) if v.get("compare_at_price") else None
                rows.append({"brand_id": bid, "product": p["title"], "variant": v.get("title"),
                             "product_type": p.get("product_type"), "url": f"{base}/products/{p['handle']}",
                             "selling_price": price, "compare_at_price": cap,
                             "mrp_assumed": cap if cap and price and cap >= price else price,
                             "tags": ";".join(p.get("tags", []) if isinstance(p.get("tags"), list) else [p.get("tags", "")]),
                             "description": desc[:4000], "retrieved_ist": ts_ist})
        print(f"{bid}: {len(products)} products")
    pd.DataFrame(rows).to_csv(out_dir / f"official_catalogue_flat_{day}.csv", index=False)


if __name__ == "__main__":
    main()
