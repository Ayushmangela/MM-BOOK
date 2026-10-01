"""Results figures. Every plotted value is read from outputs/tables/*.csv and written back out as
outputs/figures/figN_data.csv so the chart can be checked against the numbers.

  python src/figures.py --all
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from PIL import Image  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import FIGURES, PLATFORM_LABEL, PLATFORM_ORDER, ROOT, TABLES  # noqa: E402

STYLE = Path(__file__).resolve().parents[1] / "figures_src" / "chapter.mplstyle"
plt.style.use(STYLE)
MARK = {"chatgpt": "o", "gemini": "s", "perplexity": "^", "aio": "D"}
FILL = {"chatgpt": "black", "gemini": "white", "perplexity": "#7f7f7f", "aio": "white"}
CAT = {"skincare": "Skincare", "audio": "Wireless earbuds"}
TYPE = {"d2c_origin": "D2C-origin", "incumbent": "Incumbent"}
MANIFEST = []


def git_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=Path(__file__).resolve().parents[1],
                                       text=True).strip()
    except Exception:  # noqa: BLE001
        return "uncommitted"


def save(fig, n, caption, data: pd.DataFrame, sources):
    FIGURES.mkdir(parents=True, exist_ok=True)
    png = FIGURES / f"fig{n}.png"
    fig.savefig(png, dpi=300)
    plt.close(fig)
    Image.open(png).convert("RGB").save(FIGURES / f"fig{n}.tif", dpi=(300, 300), compression="tiff_lzw")
    data.to_csv(FIGURES / f"fig{n}_data.csv", index=False)
    MANIFEST.append({"figure": n, "caption": caption, "file": png.name, "script": "src/figures.py",
                     "data_file": f"fig{n}_data.csv", "source_tables": ";".join(sources), "commit": git_commit()})


def fig_mention_dots(n):
    """Mention rate per brand: one marker per platform, line = cross-platform range, bar = pooled."""
    t = pd.read_csv(TABLES / "awareness_prominence_by_platform.csv")
    pooled = pd.read_csv(TABLES / "awareness_pooled_by_brand.csv")
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 3.6), sharex=True)
    data = []
    for ax, cat in zip(axes, ["skincare", "audio"]):
        p = pooled[pooled.category == cat].copy()
        p["order"] = p.brand_type.map({"incumbent": 0, "d2c_origin": 1}) * 10 + p.mention_rate.rank()
        p = p.sort_values("order")
        ylab = []
        for y, row in enumerate(p.itertuples()):
            g = t[(t.category == cat) & (t.brand_id == row.brand_id)].set_index("platform")
            vals = [100 * g.loc[pl, "mention_rate"] for pl in PLATFORM_ORDER if pl in g.index]
            ax.plot([min(vals), max(vals)], [y, y], color="#9a9a9a", linewidth=0.8, zorder=1)
            for pl in PLATFORM_ORDER:
                if pl in g.index:
                    v = 100 * g.loc[pl, "mention_rate"]
                    ax.scatter(v, y, marker=MARK[pl], s=22, facecolor=FILL[pl], edgecolor="black", linewidth=0.6, zorder=3)
                    data.append({"category": cat, "brand": row.brand, "brand_type": row.brand_type, "platform": pl,
                                 "mention_rate_pct": round(v, 2), "n_valid": int(g.loc[pl, "n_valid"])})
            ax.plot([100 * row.mention_rate] * 2, [y - 0.28, y + 0.28], color="black", linewidth=1.4, zorder=2)
            data.append({"category": cat, "brand": row.brand, "brand_type": row.brand_type, "platform": "pooled",
                         "mention_rate_pct": round(100 * row.mention_rate, 2), "n_valid": int(row.n_valid)})
            ylab.append(row.brand)
        ax.set_yticks(range(len(ylab)))
        ax.set_yticklabels(ylab)
        n_inc = int((p.brand_type == "incumbent").sum())
        ax.axhline(n_inc - 0.5, color="black", linewidth=0.4, linestyle=(0, (2, 2)))
        for lab_, y0, y1 in (("Incumbent", -0.4, n_inc - 0.6), ("D2C-origin", n_inc - 0.4, len(p) - 0.6)):
            ax.text(1.02, (y0 + y1) / 2, lab_, transform=ax.get_yaxis_transform(), rotation=270,
                    ha="left", va="center", fontsize=7.5, style="italic")
        ax.set_title(CAT[cat], fontsize=9, loc="left")
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.6, len(ylab) - 0.4)
    fig.supxlabel("Mention rate (% of valid responses to non-branded prompts)", fontsize=9, y=0.03)
    handles = [Line2D([], [], marker=MARK[pl], linestyle="none", markerfacecolor=FILL[pl], markeredgecolor="black",
                      markersize=4.5, label=PLATFORM_LABEL[pl]) for pl in PLATFORM_ORDER]
    handles.append(Line2D([], [], color="black", linewidth=1.4, label="All platforms pooled"))
    fig.legend(handles=handles, loc="upper center", ncol=5, bbox_to_anchor=(0.5, 1.02), handletextpad=0.3, columnspacing=1.0)
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    cap = "Mention rate by brand and platform"
    save(fig, n, cap, pd.DataFrame(data), ["awareness_prominence_by_platform.csv", "awareness_pooled_by_brand.csv"])


def fig_type_forest(n):
    t = pd.read_csv(TABLES / "brand_type_comparison.csv")
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.5), sharex=True)
    data = []
    rows = PLATFORM_ORDER + ["all"]
    lab = [PLATFORM_LABEL[p] for p in PLATFORM_ORDER] + ["All platforms"]
    for ax, cat in zip(axes, ["skincare", "audio"]):
        g = t[t.category == cat].set_index("platform")
        for y, pl in enumerate(rows[::-1]):
            if pl not in g.index:
                continue
            d, lo, hi = 100 * g.loc[pl, "diff"], 100 * g.loc[pl, "diff_lo"], 100 * g.loc[pl, "diff_hi"]
            ax.plot([lo, hi], [y, y], color="black", linewidth=0.8)
            ax.scatter(d, y, marker="D" if pl == "all" else "o", s=24 if pl == "all" else 18,
                       facecolor="black" if pl == "all" else "white", edgecolor="black", linewidth=0.7, zorder=3)
            data.append({"category": cat, "platform": pl, "diff_pp": round(d, 2), "ci_lo_pp": round(lo, 2), "ci_hi_pp": round(hi, 2)})
        ax.axvline(0, color="black", linewidth=0.5, linestyle=(0, (3, 2)))
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels(lab[::-1])
        ax.set_title(CAT[cat], fontsize=9, loc="left")
    fig.supxlabel("Difference in mention rate, D2C-origin minus incumbent (percentage points, 95% CI)", fontsize=9, y=0.02)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, n, "D2C-origin minus incumbent mention rate", pd.DataFrame(data), ["brand_type_comparison.csv"])


SRC_ORDER = ["brand_owned", "marketplace", "review_comparison", "community_ugc", "editorial_press", "encyclopaedic", "video", "other"]
SRC_LABEL = {"brand_owned": "Brand-owned", "marketplace": "Marketplace", "review_comparison": "Review/comparison",
             "community_ugc": "Community/UGC", "editorial_press": "Editorial/press", "encyclopaedic": "Encyclopaedic",
             "video": "Video", "other": "Other"}
SRC_FILL = {"brand_owned": ("black", ""), "marketplace": ("#555555", ""), "review_comparison": ("#8c8c8c", ""),
            "community_ugc": ("white", "////"), "editorial_press": ("#c8c8c8", ""), "encyclopaedic": ("white", "...."),
            "video": ("white", "xxx"), "other": ("white", "")}


def fig_source_mix(n):
    pl = pd.read_csv(TABLES / "sources_by_platform.csv").set_index("platform")
    bt = pd.read_csv(TABLES / "sources_by_brand_type.csv").set_index("brand_type")
    rows = [(PLATFORM_LABEL[p], pl.loc[p]) for p in PLATFORM_ORDER if p in pl.index and pl.loc[p, "n_sources"] > 0]
    rows += [(f"{TYPE[b]} brands", bt.loc[b]) for b in ["d2c_origin", "incumbent"] if b in bt.index]
    fig, ax = plt.subplots(figsize=(6.3, 2.9))
    data = []
    for y, (name, r) in enumerate(rows[::-1]):
        left = 0.0
        tot = sum(r.get(s, 0) for s in SRC_ORDER)
        for s in SRC_ORDER:
            w = 100 * r.get(s, 0) / tot if tot else 0
            fc, h = SRC_FILL[s]
            ax.barh(y, w, left=left, height=0.62, color=fc, hatch=h, edgecolor="black", linewidth=0.5)
            data.append({"row": name, "source_type": s, "share_pct": round(w, 2), "n_sources": int(r["n_sources"])})
            left += w
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([f"{n_} (n = {int(r['n_sources']):,})" for n_, r in rows[::-1]])
    n_pl = sum(1 for _ in rows) - 2
    ax.axhline(1.5, color="black", linewidth=0.4)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of displayed sources (%)")
    ax.legend(handles=[Patch(facecolor=SRC_FILL[s][0], hatch=SRC_FILL[s][1], edgecolor="black", linewidth=0.5,
                             label=SRC_LABEL[s]) for s in SRC_ORDER],
              loc="upper center", bbox_to_anchor=(0.45, 1.27), ncol=4, handlelength=1.4, columnspacing=0.9)
    fig.tight_layout()
    save(fig, n, "Displayed sources by type", pd.DataFrame(data), ["sources_by_platform.csv", "sources_by_brand_type.csv"])


def fig_stability(n):
    s = pd.read_csv(TABLES / "stability_summary.csv")
    fig, ax = plt.subplots(figsize=(6.3, 2.5))
    data = []
    ptm = {"generic": ("o", "white"), "use_case": ("s", "white"), "price_band": ("^", "white")}
    for y, pl in enumerate(PLATFORM_ORDER[::-1]):
        a = s[(s.platform == pl) & (s.prompt_type == "all")]
        if a.empty:
            continue
        a = a.iloc[0]
        ax.plot([a.js_lo, a.js_hi], [y, y], color="black", linewidth=0.8)
        ax.scatter(a.jaccard_study, y, marker="D", s=26, color="black", zorder=3)
        data.append({"platform": pl, "prompt_type": "all", "jaccard": round(a.jaccard_study, 4), "lo": round(a.js_lo, 4), "hi": round(a.js_hi, 4)})
        for k, (pt, (mk, fc)) in enumerate(ptm.items()):
            b = s[(s.platform == pl) & (s.prompt_type == pt)]
            if not b.empty:
                ax.scatter(b.jaccard_study.iloc[0], y + 0.22, marker=mk, s=16, facecolor=fc, edgecolor="black", linewidth=0.6, zorder=3)
                data.append({"platform": pl, "prompt_type": pt, "jaccard": round(b.jaccard_study.iloc[0], 4), "lo": None, "hi": None})
    ax.set_yticks(range(4))
    ax.set_yticklabels([PLATFORM_LABEL[p] for p in PLATFORM_ORDER[::-1]])
    ax.set_xlim(0, 1)
    ax.set_xlabel("Mean pairwise Jaccard similarity of study brands named across five runs (0 = no overlap, 1 = identical)")
    h = [Line2D([], [], marker="D", color="black", linestyle="-", linewidth=0.8, markersize=4, label="All non-branded prompts (95% CI)")]
    h += [Line2D([], [], marker=mk, linestyle="none", markerfacecolor="white", markeredgecolor="black", markersize=4,
                 label=pt.replace("_", "-").capitalize()) for pt, (mk, _) in ptm.items()]
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, 1.22), ncol=4, handletextpad=0.3, columnspacing=1.0)
    fig.tight_layout()
    save(fig, n, "Run-to-run stability by platform", pd.DataFrame(data), ["stability_summary.csv"])


def fig_benchmark(n):
    f = TABLES / "benchmark_comparison.csv"
    if not f.exists():
        print("benchmark_comparison.csv missing; skipping benchmark figure")
        return
    b = pd.read_csv(f).dropna(subset=["log10_reviews", "mention_rate"])
    fig, ax = plt.subplots(figsize=(4.6, 3.3))
    for r in b.itertuples():
        mk = "o" if r.brand_type == "d2c_origin" else "s"
        fc = "black" if r.category == "audio" else "white"
        ax.scatter(r.log10_reviews, 100 * r.mention_rate, marker=mk, s=24, facecolor=fc, edgecolor="black", linewidth=0.7)
        ax.annotate(r.brand, (r.log10_reviews, 100 * r.mention_rate), xytext=(3, 3), textcoords="offset points", fontsize=7.5)
    ax.set_xlabel("Marketplace review count of best-selling product (log10)")
    ax.set_ylabel("Pooled mention rate (%)")
    h = [Line2D([], [], marker="o", linestyle="none", markerfacecolor="white", markeredgecolor="black", label="D2C-origin"),
         Line2D([], [], marker="s", linestyle="none", markerfacecolor="white", markeredgecolor="black", label="Incumbent"),
         Line2D([], [], marker="o", linestyle="none", markerfacecolor="black", markeredgecolor="black", label="Earbuds (filled)")]
    ax.legend(handles=h, loc="best")
    fig.tight_layout()
    save(fig, n, "Model visibility against marketplace review volume", b, ["benchmark_comparison.csv"])


FIGS = {3: fig_mention_dots, 4: fig_type_forest, 5: fig_source_mix, 6: fig_stability, 7: fig_benchmark}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--fig", type=int)
    a = ap.parse_args()
    for k, fn in FIGS.items():
        if a.all or a.fig == k:
            fn(k)
    if MANIFEST:
        mf = FIGURES / "MANIFEST.csv"
        old = pd.read_csv(mf) if mf.exists() else pd.DataFrame()
        new = pd.DataFrame(MANIFEST)
        if len(old):
            old = old[~old.figure.isin(new.figure)]
        pd.concat([old, new]).sort_values("figure").to_csv(mf, index=False)
        print(f"wrote {len(MANIFEST)} figures; manifest updated")
