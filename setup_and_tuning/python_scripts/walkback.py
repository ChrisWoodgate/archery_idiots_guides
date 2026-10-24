import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle

# Figures are written to ../figures relative to this script (repo layout:
# <guide>/python_scripts/*.py and <guide>/figures/*.pdf).
OUT_DIR = Path(__file__).resolve().parent.parent / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "mathtext.fontset": "cm",
})

# Target face seen from the shooting line. Sight set for the shortest
# distance; the archer aims at the mark near the top from each distance in
# turn, and the arrows walk down the face as the distance increases.
XLIM = (-10.0, 10.0)
YLIM = (-26.0, 9.5)
R_SHAFT = 0.42
VANE = 1.15
Y_MARK = 5.5
DISTANCES = (10, 15, 20, 25, 30, 40)          # metres, for labels
Y_ARROWS = (5.2, 2.6, -0.9, -5.3, -10.6, -22.0)   # drop grows ~quadratically
ROTS = (10, -25, 40, -5, 25, -35)


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
        tip = np.array([x + VANE * np.cos(a), y + VANE * np.sin(a)])
        n = np.array([-np.sin(a), np.cos(a)]) * 0.28
        root = np.array([x, y])
        ax.add_patch(Polygon(np.array([root + n, tip, root - n]), closed=True,
                             facecolor="0.35" if k == 0 else "0.75",
                             edgecolor="k", lw=0.6, zorder=5))
    ax.add_patch(Circle((x, y), R_SHAFT, facecolor="white", edgecolor="k", lw=0.9, zorder=6))
    ax.plot([x], [y], marker=".", color="k", ms=3, zorder=7)


def draw_panel(ax, label, drift, annotate=False, ok=False, verdict=""):
    """drift: horizontal displacement per 5 m of distance (units)."""
    # Target face (boss) outline and aiming mark
    ax.add_patch(Rectangle((XLIM[0] + 2.6, YLIM[0] + 2.2), XLIM[1] - XLIM[0] - 5.2,
                           YLIM[1] - YLIM[0] - 3.0, facecolor="none", edgecolor="0.6",
                           lw=0.7, zorder=1))
    ax.add_patch(Circle((0, Y_MARK), 1.2, facecolor="none", edgecolor="0.5", lw=0.8, zorder=2))
    ax.plot([-0.6, 0.6], [Y_MARK, Y_MARK], color="0.5", lw=0.6, zorder=2)
    ax.plot([0, 0], [Y_MARK - 0.6, Y_MARK + 0.6], color="0.5", lw=0.6, zorder=2)
    # Plumb line through the mark
    ax.plot([0, 0], [YLIM[0] + 2.4, YLIM[1] - 1.0], ls="--", lw=0.7, color="0.45", zorder=3)

    # Arrows, one per distance
    xs = [drift * (d - DISTANCES[0]) / 5.0 for d in DISTANCES]
    for i, (x, y, r) in enumerate(zip(xs, Y_ARROWS, ROTS)):
        fletched(ax, x, y, r)
        if annotate:
            ax.text(x + 2.0, y, f"{DISTANCES[i]}\\,m" if False else f"{DISTANCES[i]} m",
                    ha="left", va="center", fontsize=7, color="0.25", zorder=9)

    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0.5, -0.02, f"({label})", transform=ax.transAxes,
            ha="center", va="top", fontsize=10)
    mark(ax, ok, XLIM[0] + 0.3, YLIM[1] - 2.3, 1.9)
    if verdict:
        ax.text(0.5, 0.01, verdict, transform=ax.transAxes, ha="center",
                va="bottom", fontsize=8)

    if annotate:
        arr = dict(arrowstyle="-|>", lw=0.8, color="k", shrinkA=0, shrinkB=1)
        fs = 8
        bb = dict(fc="white", ec="none", pad=1.0)
        ax.annotate("Aiming mark", xy=(1.0, Y_MARK + 0.8), xytext=(2.2, Y_MARK + 3.0),
                    ha="left", va="center", fontsize=fs, arrowprops=arr, zorder=9, bbox=bb)
        ax.annotate("Plumb line", xy=(0.05, -7.5), xytext=(-6.0, -8.5),
                    ha="left", va="center", fontsize=fs, arrowprops=arr, zorder=9, bbox=bb)


# Layout: three panels side by side
PANEL_H_IN = 3.9
PANEL_W_IN = PANEL_H_IN * (XLIM[1] - XLIM[0]) / (YLIM[1] - YLIM[0])
GAP_IN = 0.35
W_IN = 3 * PANEL_W_IN + 2 * GAP_IN + 0.2
H_IN = PANEL_H_IN + 0.4
fig = plt.figure(figsize=(W_IN, H_IN))
PW, PH = PANEL_W_IN / W_IN, PANEL_H_IN / H_IN
GAP = GAP_IN / W_IN
x0 = (1 - 3 * PW - 2 * GAP) / 2
y0 = 0.32 / H_IN

ax_a = fig.add_axes([x0, y0, PW, PH])
ax_b = fig.add_axes([x0 + PW + GAP, y0, PW, PH])
ax_c = fig.add_axes([x0 + 2 * (PW + GAP), y0, PW, PH])

draw_panel(ax_a, "a", drift=-0.9, verdict="Drifting left")
draw_panel(ax_b, "b", drift=0.0, annotate=True, ok=True, verdict="Straight")
draw_panel(ax_c, "c", drift=0.9, verdict="Drifting right")

for ext in ("pdf", "svg", "png"):
    fig.savefig(OUT_DIR / f"walkback.{ext}", bbox_inches="tight", pad_inches=0.05,
                **({"dpi": 200} if ext == "png" else {}))
print("done")
