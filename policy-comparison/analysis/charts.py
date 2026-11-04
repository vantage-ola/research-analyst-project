"""Draw the comparison matrix (documents x criteria) from data/matrix.csv.

Usage: uv run --no-project --with matplotlib python -I charts.py
Writes output/chart_matrix.png and .svg.

Scores are ordinal (0, 1, 2), so one blue ramp, light to dark, validated with the dataviz
skill's --ordinal check. Every cell also prints its number, so colour is never the only cue.
"""
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
RAMP = {0: "#86b6ef", 1: "#3987e5", 2: "#184f95"}
LABEL = {0: "0  missing", 1: "1  partly", 2: "2  fully"}
CRITERIA = [("binding_force", "Legal force"), ("responsible_body", "Who's in charge"), ("funding", "Money"),
            ("measurable_targets", "Targets with dates"), ("jobs_workforce", "Jobs"), ("risk_safety", "Risk and safety"),
            ("data_protection", "Data protection"), ("enforcement", "Enforcement"), ("local_language", "Local languages"),
            ("monitoring_evaluation", "Monitoring")]

plt.rcParams.update({"font.family": "sans-serif",
                     "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"], "font.size": 10})


def main():
    OUT.mkdir(exist_ok=True)
    rows = list(csv.DictReader(open(ROOT / "data" / "matrix.csv", newline="")))
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    fig.subplots_adjust(left=0.17, right=0.985, top=0.66, bottom=0.15)
    gap = 0.06
    for i, r in enumerate(rows):
        for j, (key, _) in enumerate(CRITERIA):
            v = int(r[key])
            ax.add_patch(FancyBboxPatch((j + gap, i + gap), 1 - 2 * gap, 1 - 2 * gap,
                                        boxstyle="round,pad=0,rounding_size=0.08", facecolor=RAMP[v], edgecolor="none"))
            ax.text(j + 0.5, i + 0.5, str(v), ha="center", va="center", fontsize=10.5,
                    color=INK if v == 0 else "#ffffff", fontweight="bold")
        ax.text(len(CRITERIA) + 0.15, i + 0.5, f"{r['total_of_20']}", ha="left", va="center", fontsize=10, color=INK2)
    ax.text(len(CRITERIA) + 0.15, -0.35, "of 20", ha="left", va="center", fontsize=8.5, color=MUTED)
    ax.set_xlim(0, len(CRITERIA) + 0.75)
    ax.set_ylim(len(rows), -0.6)
    ax.set_yticks([i + 0.5 for i in range(len(rows))], [r["country"] for r in rows], color=INK)
    ax.set_xticks([j + 0.5 for j in range(len(CRITERIA))], [c[1] for c in CRITERIA], rotation=35, ha="left",
                  rotation_mode="anchor", color=INK2, fontsize=9.5)
    ax.xaxis.tick_top()
    ax.tick_params(length=0, pad=4)
    for s in ax.spines.values():
        s.set_visible(False)

    fig.text(0.025, 0.965, "None of these AI strategies is law, and all leave enforcement for later",
             fontsize=13, fontweight="bold", ha="left", va="top", color=INK)
    fig.text(0.025, 0.9, "Score per criterion from 0 to 2, from the documents' own text. Every score cites a page.",
             fontsize=9.5, color=INK2, ha="left", va="top")
    x = 0.17
    for v in (0, 1, 2):
        fig.patches.append(FancyBboxPatch((x, 0.035), 0.018, 0.04, boxstyle="round,pad=0,rounding_size=0.004",
                                          transform=fig.transFigure, facecolor=RAMP[v], edgecolor="none"))
        fig.text(x + 0.025, 0.055, LABEL[v], fontsize=9, color=INK2, va="center")
        x += 0.12
    fig.text(0.985, 0.055, "Sources: national AI strategies of Nigeria, Kenya, Rwanda, Egypt; AU Continental AI Strategy",
             fontsize=7.5, color=MUTED, ha="right", va="center")
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"chart_matrix.{ext}", dpi=220, facecolor=SURFACE)
    print("wrote output/chart_matrix.png")


if __name__ == "__main__":
    main()
