"""Conceptual diagrams for the chapter, drawn as code (no image generators).

  python figures_src/diagrams.py framework   -> outputs/figures/fig1_framework.{png,tif}
  python figures_src/diagrams.py pipeline    -> outputs/figures/fig2_pipeline.{png,tif}

The pipeline diagram reads every count it prints from outputs/tables/collection_counts.csv and
outputs/tables/reliability_summary.csv; no number is typed by hand.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "figures"
plt.style.use(ROOT / "figures_src" / "chapter.mplstyle")
LW = 0.7


def box(ax, x, y, w, h, title, sub=None, fill="white", ls="-", title_size=9, sub_size=8, bold=True):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor="black", linewidth=LW, linestyle=ls))
    if sub:
        ax.text(x + w / 2, y + h * 0.63, title, ha="center", va="center", fontsize=title_size,
                fontweight="bold" if bold else "normal")
        ax.text(x + w / 2, y + h * 0.30, sub, ha="center", va="center", fontsize=sub_size, style="italic")
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=title_size,
                fontweight="bold" if bold else "normal", linespacing=1.25)


def arrow(ax, x1, y1, x2, y2, ls="-", lw=LW, head=7):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=head,
                                 linewidth=lw, linestyle=ls, color="black", shrinkA=0, shrinkB=0))


def save(fig, stem):
    OUT.mkdir(parents=True, exist_ok=True)
    png = OUT / f"{stem}.png"
    fig.savefig(png, dpi=300)
    plt.close(fig)
    # IGI requires .tif files; convert losslessly from the 300 dpi render.
    im = Image.open(png).convert("RGB")
    im.save(OUT / f"{stem}.tif", dpi=(300, 300), compression="tiff_lzw")
    print(f"wrote {png} and .tif ({im.size[0]}x{im.size[1]} px)")


def framework():
    fig, ax = plt.subplots(figsize=(6.3, 4.15))
    ax.set_xlim(0, 100); ax.set_ylim(0, 66); ax.axis("off")

    # column headings
    ax.text(14, 63.5, "Consumer-based brand equity", ha="center", fontsize=9, fontweight="bold")
    ax.text(14, 60.6, "(Keller, 1993; Erdem & Swait, 2004)", ha="center", fontsize=8)
    ax.text(51, 63.5, "Generative brand equity", ha="center", fontsize=9, fontweight="bold")
    ax.text(51, 60.6, "(observed in AI answers)", ha="center", fontsize=8)
    ax.text(88.5, 63.5, "Consumer response", ha="center", fontsize=9, fontweight="bold")
    ax.text(88.5, 60.6, "(not measured here)", ha="center", fontsize=8)

    rows = [  # classical construct, generative dimension, question, y
        ("Brand awareness\n(recall, recognition)", "Model awareness", "Is the brand retrieved?", 47),
        ("Top-of-mind position\nand salience", "Model prominence", "Where does it appear?", 34.5),
        ("Brand image\n(associations)", "Model image", "How is it described?", 22),
        ("Brand credibility", "Model credibility", "Which sources support it?", 9.5),
    ]
    h = 9.0
    for left, dim, q, y in rows:
        box(ax, 1.5, y, 25, h, left, bold=False, title_size=8.5)
        box(ax, 35.5, y, 31, h, dim, q)
        arrow(ax, 26.5, y + h / 2, 35.5, y + h / 2)

    # stability: cross-cutting bar spanning all four dimensions
    ax.add_patch(Rectangle((68.5, 9.5), 5.2, 46.5, facecolor="#e6e6e6", edgecolor="black", linewidth=LW))
    ax.text(71.1, 32.75, "Stability across repeated runs and platforms", rotation=90,
            ha="center", va="center", fontsize=8.5)
    for _, _, _, y in rows:
        ax.plot([66.5, 68.5], [y + h / 2, y + h / 2], color="black", linewidth=LW)

    # consumer outcomes, dashed: proposed, not tested
    box(ax, 79, 38, 19, 11, "Consideration\nset formation", ls=(0, (4, 2)), bold=False, title_size=8.5)
    box(ax, 79, 17, 19, 11, "Brand evaluation\nand choice", ls=(0, (4, 2)), bold=False, title_size=8.5)
    arrow(ax, 73.7, 43.5, 79, 43.5, ls=(0, (4, 2)))
    arrow(ax, 73.7, 22.5, 79, 22.5, ls=(0, (4, 2)))
    arrow(ax, 88.5, 38, 88.5, 28, ls=(0, (4, 2)))
    ax.text(88.5, 12.2, "Dashed: proposed link,", ha="center", fontsize=7.5, style="italic")
    ax.text(88.5, 9.6, "not tested in this chapter", ha="center", fontsize=7.5, style="italic")

    # sources feeding credibility (the observable mechanism)
    ax.text(51, 4.6, "Displayed sources classified as brand-owned, marketplace, review or community,",
            ha="center", fontsize=7.5)
    ax.text(51, 1.6, "editorial or press, encyclopaedic, video, or other", ha="center", fontsize=7.5)
    arrow(ax, 51, 6.6, 51, 9.5, head=6)
    save(fig, "fig1_framework")


def pipeline():
    import pandas as pd
    t = ROOT / "outputs" / "tables"
    cc = pd.read_csv(t / "collection_counts.csv").set_index("item")["value"]
    rel = pd.read_csv(t / "reliability_summary.csv").set_index("item")["value"] if (t / "reliability_summary.csv").exists() else None
    fmt = lambda k: f"{int(cc[k]):,}"

    fig, ax = plt.subplots(figsize=(6.3, 4.6))
    ax.set_xlim(0, 100); ax.set_ylim(0, 74); ax.axis("off")
    W = 27
    # top row
    box(ax, 1, 56, W, 15, "Prompt set",
        f"{fmt('prompts')} prompts, 2 categories,\n4 prompt types", title_size=9, sub_size=7.8)
    box(ax, 36.5, 56, W, 15, "Platforms",
        "ChatGPT, Gemini, Perplexity,\nGoogle AI Overviews", title_size=9, sub_size=7.8)
    box(ax, 72, 56, W, 15, "Raw responses",
        f"{fmt('calls')} calls: {fmt('ok')} valid,\n{fmt('no_overview')} no overview, {fmt('failed')} failed",
        title_size=9, sub_size=7.8)
    arrow(ax, 1 + W, 63.5, 36.5, 63.5)
    arrow(ax, 36.5 + W, 63.5, 72, 63.5)
    ax.text(32.25, 65.2, f"x {fmt('repetitions')} runs", ha="center", fontsize=7.5, style="italic")
    ax.text(67.75, 65.2, "APIs", ha="center", fontsize=7.5, style="italic")

    # coding row
    box(ax, 72, 31, W, 17, "Coding",
        "Deterministic alias matching;\nLLM first pass (codebook);\nhuman double-coding of sample",
        title_size=9, sub_size=7.6)
    arrow(ax, 85.5, 56, 85.5, 48)
    box(ax, 36.5, 31, W, 17, "Measures",
        "Awareness, prominence,\nimage, credibility,\nstability", title_size=9, sub_size=7.6)
    arrow(ax, 72, 39.5, 36.5 + W, 39.5)
    box(ax, 1, 31, W, 17, "Benchmarks",
        "Marketplace ratings and\nreview counts; public\nmarket-share data", title_size=9, sub_size=7.6)
    arrow(ax, 36.5, 39.5, 1 + W, 39.5)

    # outputs
    box(ax, 18, 6, 64, 14, "Findings by research question",
        "RQ1 awareness and prominence   RQ2 image and accuracy\nRQ3 sources   RQ4 stability", title_size=9, sub_size=7.6)
    arrow(ax, 50, 31, 50, 20)
    if rel is not None and "n_double_coded" in rel:
        ax.text(85.5, 27.5, f"double-coded: {int(rel['n_double_coded']):,} responses", ha="center",
                fontsize=7.5, style="italic")
    save(fig, "fig2_pipeline")


if __name__ == "__main__":
    {"framework": framework, "pipeline": pipeline}[sys.argv[1]]()
