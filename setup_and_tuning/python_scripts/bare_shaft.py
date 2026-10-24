import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon

# Figures are written to ../figures relative to this script (repo layout:
# <guide>/python_scripts/*.py and <guide>/figures/*.pdf).
OUT_DIR = Path(__file__).resolve().parent.parent / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "mathtext.fontset": "cm",
})

# Target face seen from the shooting line, looking at the backs of the arrows.
# Fletched arrows: nock end with three vanes. Bare shafts: nock end only.
LIM = 10.0
R_SHAFT = 0.42
VANE = 1.15


def mark(ax, ok, x, y, s, sx=1):
    if ok:
        ax.plot([x, x + sx * 0.38 * s, x + sx * s], [y + 0.45 * s, y, y + 0.95 * s],
                color="#2ca02c", lw=2.2, solid_capstyle="round",
                solid_joinstyle="round", zorder=10)
    else:
        ax.plot([x, x + sx * s], [y, y + s], color="#d62728", lw=2.2,
                solid_capstyle="round", zorder=10)
        ax.plot([x, x + sx * s], [y + s, y], color="#d62728", lw=2.2,
                solid_capstyle="round", zorder=10)


def fletched(ax, x, y, rot=0.0):
    for k in range(3):
        a = np.radians(90 + 120 * k + rot)
        base = 0.28
        tip = np.array([x + VANE * np.cos(a), y + VANE * np.sin(a)])
        n = np.array([-np.sin(a), np.cos(a)]) * base
        root = np.array([x, y])
        poly = np.array([root + n, tip, root - n])
        ax.add_patch(Polygon(poly, closed=True, facecolor="0.35" if k == 0 else "0.75",
                             edgecolor="k", lw=0.6, zorder=5))
    ax.add_patch(Circle((x, y), R_SHAFT, facecolor="white", edgecolor="k", lw=0.9, zorder=6))
    ax.plot([x], [y], marker=".", color="k", ms=3, zorder=7)


def bare(ax, x, y):
    ax.add_patch(Circle((x, y), R_SHAFT, facecolor="white", edgecolor="k", lw=0.9, zorder=6))
    ax.plot([x], [y], marker=".", color="k", ms=3, zorder=7)


def draw_panel(ax, label, bare_offset, annotate=False, ok=False, verdict=""):
    # Target reference: gold ring and centre cross, kept faint
    for r in (3.2, 6.4):
        ax.add_patch(Circle((0, 0), r, facecolor="none", edgecolor="0.6", lw=0.7,
                            ls="-", zorder=1))
    ax.plot([-0.8, 0.8], [0, 0], color="0.6", lw=0.6, zorder=1)
    ax.plot([0, 0], [-0.8, 0.8], color="0.6", lw=0.6, zorder=1)

    # Fletched group, roughly on the centre
    for (dx, dy, rot) in ((-0.9, 0.7, 10), (0.9, 0.9, -25), (0.1, -0.9, 40)):
        fletched(ax, dx, dy, rot)
    # Bare shafts, displaced as a group
    ox, oy = bare_offset
    for (dx, dy) in ((-0.55, 0.45), (0.6, -0.4)):
        bare(ax, ox + dx, oy + dy)

    ax.set_xlim(-LIM, LIM)
    ax.set_ylim(-LIM, LIM)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0.5, -0.02, f"({label})", transform=ax.transAxes,
            ha="center", va="top", fontsize=10)
    mark(ax, ok, -LIM + 0.4, LIM - 2.2, 1.8)
    if verdict:
        ax.text(0.5, 0.01, verdict, transform=ax.transAxes, ha="center",
                va="bottom", fontsize=8)

    if annotate:
        arr = dict(arrowstyle="-|>", lw=0.8, color="k", shrinkA=0, shrinkB=1)
        fs = 8
        ax.annotate("Fletched arrows", xy=(1.3, 1.5), xytext=(6.0, 6.5), ha="center",
                    va="center", fontsize=fs, arrowprops=arr, zorder=9,
                    bbox=dict(fc="white", ec="none", pad=1.0))
        ax.annotate("Bare shafts", xy=(ox - 0.9, oy - 0.3), xytext=(-5.5, -6.5), ha="center",
                    va="center", fontsize=fs, arrowprops=arr, zorder=9,
                    bbox=dict(fc="white", ec="none", pad=1.0))


# Layout: a row of three (a, b, c) above a centred row of two (d, e). Wider
# than tall so that the figure, its caption and some text share a page.
PANEL_IN = 1.9
GAPX_IN, GAPY_IN = 0.45, 0.55
W_IN = 3 * PANEL_IN + 2 * GAPX_IN + 0.2
H_IN = 2 * PANEL_IN + GAPY_IN + 0.3
fig = plt.figure(figsize=(W_IN, H_IN))
PW, PH = PANEL_IN / W_IN, PANEL_IN / H_IN
GAPX, GAPY = GAPX_IN / W_IN, GAPY_IN / H_IN

x_mid = 0.5 - PW / 2                                   # centre column
x_left3, x_right3 = x_mid - GAPX - PW, x_mid + GAPX + PW   # outer columns, row of three
x_left2, x_right2 = 0.5 - PW - GAPX / 2, 0.5 + GAPX / 2    # row of two, centred
y_top = 1 - 0.08 / H_IN - PH
y_bot = y_top - GAPY - PH

ax_a = fig.add_axes([x_left3, y_top, PW, PH])
ax_b = fig.add_axes([x_mid, y_top, PW, PH])
ax_c = fig.add_axes([x_right3, y_top, PW, PH])
ax_d = fig.add_axes([x_left2, y_bot, PW, PH])
ax_e = fig.add_axes([x_right2, y_bot, PW, PH])

draw_panel(ax_a, "a", (-2.2, -1.8), annotate=True, ok=True, verdict="Good")
draw_panel(ax_b, "b", (-5.5, 0.0), verdict="Arrows too stiff\nor button too firm")
draw_panel(ax_c, "c", (5.5, 0.0), verdict="Arrows too weak\nor button too soft")
draw_panel(ax_d, "d", (0.0, -5.5), verdict="Nocking point too high")
draw_panel(ax_e, "e", (0.0, 5.5), verdict="Nocking point too low")

for ext in ("pdf", "svg", "png"):
    fig.savefig(OUT_DIR / f"bare_shaft.{ext}", bbox_inches="tight", pad_inches=0.05,
                **({"dpi": 200} if ext == "png" else {}))
print("done")
