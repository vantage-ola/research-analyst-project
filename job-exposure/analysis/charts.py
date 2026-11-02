"""Draw the two charts for the brief and article from output/ranked_table.csv.

Usage: uv run --with matplotlib python -I charts.py
Writes output/chart_1_author_vs_claude.png/.svg and output/chart_2_author_vs_published.png/.svg.

Colours are the dataviz reference palette (slots 1-3, validated all-pairs in light mode).
Slot 3 is below 3:1 contrast on the surface, so every series also has its own marker shape.
"""
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "output"
SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#ecebe6"
LINK = "#d6d5ce"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 10.5, "font.weight": "normal", "text.color": INK, "axes.labelcolor": INK2,
    "xtick.color": MUTED, "ytick.color": INK2,
})


def load():
    rows = list(csv.DictReader(open(OUT / "ranked_table.csv", newline="")))
    for r in rows:
        for k in ("author_mean_0_2", "claude_mean_0_2", "ilo_mean_0_1", "aei_observed_exposure_0_1"):
            r[k] = float(r[k])
    # Highest author exposure at the top.
    return sorted(rows, key=lambda r: r["author_mean_0_2"])


def setup(title, subtitle, source, height=5.6, bottom=0.13):
    fig, ax = plt.subplots(figsize=(7.2, height))
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.tick_params(axis="both", length=0, pad=6)
    ax.grid(axis="x", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    fig.text(0.035, 0.955, title, fontsize=13.5, fontweight="bold", ha="left", va="top")
    fig.text(0.035, 0.905, subtitle, fontsize=10, color=INK2, ha="left", va="top")
    fig.text(0.035, 0.025, source, fontsize=8, color=MUTED, ha="left", va="bottom", linespacing=1.4)
    fig.subplots_adjust(left=0.36, right=0.96, top=0.78, bottom=bottom)
    return fig, ax


def legend(fig, items):
    # Legend as a single quiet row under the subtitle, left-aligned with the title.
    x = 0.035
    for label, color, marker in items:
        fig.lines.append(plt.Line2D([x + 0.006], [0.835], transform=fig.transFigure, marker=marker, color=color,
                                    markersize=6.5, linestyle="none", markeredgecolor=SURFACE, markeredgewidth=1))
        t = fig.text(x + 0.02, 0.835, label, fontsize=9.5, color=INK2, va="center", ha="left")
        fig.canvas.draw()
        bb = t.get_window_extent().transformed(fig.transFigure.inverted())
        x = bb.x1 + 0.035


def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=220, facecolor=SURFACE)
    plt.close(fig)


def chart_1(rows):
    fig, ax = setup("I rated most jobs as more exposed than my AI second rater did",
                    "Average score per job, from 0 (AI can't do it) to 2 (AI can do most of it). 7 tasks per job.",
                    "Source: my scores and Claude Opus 5.5's scores on the same 84 tasks, made separately.")
    y = list(range(len(rows)))
    tie = [abs(r["author_mean_0_2"] - r["claude_mean_0_2"]) < 1e-9 for r in rows]
    for i, r, t in zip(y, rows, tie):
        if not t:
            ax.plot([r["claude_mean_0_2"], r["author_mean_0_2"]], [i, i], color=LINK, linewidth=1.4, zorder=1,
                    solid_capstyle="round")
        else:
            ax.annotate("same", (r["author_mean_0_2"], i), xytext=(10, 0), textcoords="offset points",
                        va="center", fontsize=8.5, color=MUTED)
    ax.scatter([r["claude_mean_0_2"] for r in rows], [i - (0.13 if t else 0) for i, t in zip(y, tie)], s=38,
               color=ORANGE, marker="s", zorder=3, edgecolors=SURFACE, linewidths=1)
    ax.scatter([r["author_mean_0_2"] for r in rows], [i + (0.13 if t else 0) for i, t in zip(y, tie)], s=46,
               color=BLUE, marker="o", zorder=3, edgecolors=SURFACE, linewidths=1)
    ax.set_yticks(y, [r["category"] for r in rows])
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_xlim(0, 2.06)
    ax.set_xticks([0, 1, 2], ["0  AI can't", "1  AI can do part", "2  AI can do most"])
    for lab, ha in zip(ax.get_xticklabels(), ("left", "center", "right")):
        lab.set_ha(ha)
    legend(fig, [("Me", BLUE, "o"), ("AI second rater (Claude)", ORANGE, "s")])
    save(fig, "chart_1_author_vs_claude")


def chart_2(rows):
    fig, ax = setup("Big studies and my scores don't line up",
                    "Each measure on a 0 to 1 scale. They measure different things, so look at the order, not the size.",
                    "Sources: my scores (halved to fit 0 to 1); ILO Working Paper 140 (2025); Anthropic Economic Index.\n"
                    "Each job is matched to the closest occupation in the international job lists.",
                    height=6.0, bottom=0.16)
    y = list(range(len(rows)))
    for i in y:
        ax.axhline(i, color=GRID, linewidth=0.6, zorder=0)
    series = [
        ("Me", [r["author_mean_0_2"] / 2 for r in rows], BLUE, "o", 46),
        ("ILO study", [r["ilo_mean_0_1"] for r in rows], ORANGE, "s", 38),
        ("Anthropic: actual use of Claude", [r["aei_observed_exposure_0_1"] for r in rows], AQUA, "D", 34),
    ]
    # "Me" is drawn last so it sits on top where markers touch.
    for z, (_, xs, color, marker, size) in zip((5, 4, 3), series):
        ax.scatter(xs, y, s=size, color=color, marker=marker, zorder=z, edgecolors=SURFACE, linewidths=1.2)
    ax.set_yticks(y, [r["category"] for r in rows])
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.grid(axis="x", visible=False)
    ax.set_xlim(0, 1.03)
    ax.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
    legend(fig, [(s[0], s[2], s[3]) for s in series])
    save(fig, "chart_2_author_vs_published")


def main():
    rows = load()
    chart_1(rows)
    chart_2(rows)
    print("wrote", sorted(p.name for p in OUT.glob("chart_*")))


if __name__ == "__main__":
    main()
