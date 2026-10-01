"""Design tables generated from the frozen config files (no hand-typed content).

outputs/tables/table1_brands.csv      study brand set
outputs/tables/table2_prompt_design.csv
outputs/tables/appendix_prompts.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CONFIG, TABLES, brands_cfg, prompts_df  # noqa: E402

TYPE_LABEL = {"d2c_origin": "Indian D2C-origin", "incumbent": "Incumbent"}
CAT_LABEL = {"skincare": "Skincare", "audio": "Wireless earbuds"}
PTYPE = {"generic": "Generic category", "use_case": "Use case", "price_band": "Price band", "comparison": "Comparison"}
PURPOSE = {"generic": "Awareness, prominence, image, sources", "use_case": "Awareness, prominence, image, sources",
           "price_band": "Awareness, prominence, image, sources", "comparison": "Image and accuracy only"}
SHORT_OWNER = {
    "minimalist": "Hindustan Unilever (90.5% since 2025)",
    "dermaco": "Honasa Consumer (listed)",
    "plum": "Founder-led, independent",
    "cetaphil": "Galderma",
    "neutrogena": "Kenvue",
    "lakme": "Hindustan Unilever",
    "boat": "Imagine Marketing (unlisted)",
    "noise": "Nexxbase (Bose minority stake)",
    "boult": "Founder-owned (GoBoult)",
    "sony": "Sony Group",
    "jbl": "Harman (Samsung)",
    "samsung": "Samsung Electronics",
}

MEASURES = [
    ("Model awareness", "Mention rate", "Valid non-branded responses naming the brand / all valid non-branded responses on that platform and category"),
    ("Model awareness", "Share of model", "Mentions of the brand / mentions of all six study brands in the category (non-branded responses)"),
    ("Model prominence", "First-mention rate", "Responses in which the brand is the first study brand named / valid non-branded responses"),
    ("Model prominence", "Top-pick rate", "Responses presenting the brand as the single best choice / valid non-branded responses"),
    ("Model prominence", "Mean position", "Mean order of first mention among all brands named, for responses that name the brand"),
    ("Model image", "Positioning recall", "Descriptions of the brand carrying at least one of its own positioning attributes / descriptions with any coded attribute"),
    ("Model image", "Sentiment", "Distribution of positive, neutral, mixed and negative descriptions of the brand"),
    ("Model image", "Accuracy rate", "Correct factual claims / (correct + incorrect) claims; unverifiable claims reported separately"),
    ("Model credibility", "Source mix", "Share of each source type among sources displayed with responses that name the brand"),
    ("Model credibility", "Own-site citation rate", "Responses naming the brand that display the brand's own website / responses naming the brand"),
    ("Stability", "Run-to-run Jaccard", "Mean pairwise Jaccard similarity J of the sets of study brands named across the five runs of a prompt (10 pairs)"),
    ("Stability", "Cross-platform spread", "Range of a brand's mention rate across the four platforms"),
]


def main():
    TABLES.mkdir(parents=True, exist_ok=True)
    codes = pd.read_csv(CONFIG / "attribute_codes.csv")
    lab = {(r.category, r.code): r.label.split(" / ")[0] for r in codes.itertuples()}
    rows = []
    for b in brands_cfg()["brands"]:
        rows.append({
            "Category": CAT_LABEL[b["category"]], "Brand": b["name"], "Type": TYPE_LABEL[b["brand_type"]],
            "Owner at collection": SHORT_OWNER[b["id"]],
            "Self-declared positioning (coded)": "; ".join(lab[(b["category"], c)] for c in b["positioning_codes"]),
        })
    t1 = pd.DataFrame(rows)
    t1.loc[t1.Category.duplicated(), "Category"] = ""  # show each category once, as in print tables
    t1.to_csv(TABLES / "table1_brands.csv", index=False)

    p = prompts_df()
    ex = {}
    for t in PTYPE:
        ex[t] = {c: p[(p.prompt_type == t) & (p.category == c)].text.iloc[0] for c in ("skincare", "audio")}
    rows = []
    for t in PTYPE:
        n = p[p.prompt_type == t].groupby("category").size()
        rows.append({"Prompt type": PTYPE[t], "Per category": int(n["skincare"]),
                     "Example (skincare)": ex[t]["skincare"], "Example (earbuds)": ex[t]["audio"],
                     "Used for": PURPOSE[t]})
    rows.append({"Prompt type": "Total", "Per category": int(p.groupby("category").size()["skincare"]),
                 "Example (skincare)": "", "Example (earbuds)": "", "Used for": ""})
    pd.DataFrame(rows).to_csv(TABLES / "table2_prompt_design.csv", index=False)

    a = p[["prompt_id", "prompt_type", "text"]].copy()
    a["prompt_type"] = a.prompt_type.map(PTYPE)
    a.columns = ["ID", "Type", "Prompt (submitted verbatim)"]
    a.to_csv(TABLES / "appendix_prompts.csv", index=False)
    pd.DataFrame(MEASURES, columns=["Dimension", "Measure", "Definition"]).to_csv(TABLES / "table3_measures.csv", index=False)
    print("wrote table1_brands.csv, table2_prompt_design.csv, appendix_prompts.csv")


if __name__ == "__main__":
    main()
