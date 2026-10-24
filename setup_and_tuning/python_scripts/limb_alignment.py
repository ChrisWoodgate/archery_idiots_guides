import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle

# Figures are written to ../figures relative to this script (repo layout:
# <guide>/python_scripts/*.py and <guide>/figures/*.pdf).
OUT_DIR = Path(__file__).resolve().parent.parent / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "mathtext.fontset": "cm",
})

# View from behind the bow (archer's side), bow upright, right-handed riser so
# the sight window is cut away on the left. String drawn straight down the
# riser centreline in every panel; faults appear as limbs whose centrelines
# diverge from it. Lateral offsets exaggerated heavily.
XLIM = (-32.0, 21.0)
YLIM = (-96.0, 96.0)

YP = 30.0     # +/- y of limb pockets
YT = 88.0     # +/- y of limb tips
HW_BASE, HW_TIP = 5.0, 1.8


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


def draw_panel(ax, label, dx_top, dx_bot, annotate=False, ok=False):
    # Riser outline, seen from behind: sight window cut into the left side
    riser = np.array([
        [-6.0, -YP], [6.0, -YP], [6.5, -12], [6.5, 12], [6.0, YP],
        [-6.0, YP], [-6.0, 25], [1.5, 22], [1.5, 5], [-6.0, 2], [-6.0, -YP],
    ])
    ax.add_patch(Polygon(riser, closed=True, facecolor="0.88", edgecolor="k",
                         lw=1.0, hatch="//", zorder=2))
    # Limb bolts and stabiliser bushing on the riser centreline
    for y in (YP - 3.5, -(YP - 3.5)):
        ax.add_patch(Circle((0, y), 1.8, facecolor="white", edgecolor="k", lw=0.8, zorder=3))
    ax.add_patch(Circle((0, -10), 2.6, facecolor="white", edgecolor="k", lw=0.8, zorder=3))
    ax.add_patch(Circle((0, -10), 0.9, facecolor="k", edgecolor="k", lw=0.5, zorder=3))

    # Limbs: tapering strips, tip centre displaced by dx
    for sgn, dx in ((+1, dx_top), (-1, dx_bot)):
        limb = np.array([[-HW_BASE, sgn * YP], [HW_BASE, sgn * YP],
                         [dx + HW_TIP, sgn * YT], [dx - HW_TIP, sgn * YT]])
        ax.add_patch(Polygon(limb, closed=True, facecolor="white", edgecolor="k",
                             lw=1.1, zorder=4))
        ax.plot([0, dx], [sgn * YP, sgn * YT], ls="--", lw=0.7, color="0.35", zorder=5)

    # String: straight line between the limb tips, in front of everything
    ax.plot([dx_bot, dx_top], [-YT, YT], color="k", lw=1.2, zorder=7)

    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0.5, -0.03, f"({label})", transform=ax.transAxes,
            ha="center", va="top", fontsize=10)
    mark(ax, ok, XLIM[0] + 1.5, YLIM[1] - 7.5, 6.0)

    if annotate:
        arr = dict(arrowstyle="-|>", lw=0.8, color="k", shrinkA=0, shrinkB=1)
        fs = 8
        bb = dict(fc="white", ec="none", pad=1.0)
        xl = XLIM[0] + 1.0
        ax.annotate("Upper\nlimb", xy=(-3.4, 62), xytext=(xl, 64), ha="left",
                    va="center", fontsize=fs, arrowprops=arr, zorder=9)
        ax.annotate("Limb\nbolt", xy=(-1.8, YP - 3.5), xytext=(xl, 38), ha="left",
                    va="center", fontsize=fs, arrowprops=arr, zorder=9)
        ax.annotate("Sight\nwindow", xy=(1.2, 13), xytext=(xl, 12), ha="left",
                    va="center", fontsize=fs, arrowprops=arr, zorder=9)
        ax.annotate("Stabiliser\nbushing", xy=(-2.6, -10), xytext=(xl, -14),
                    ha="left", va="center", fontsize=fs, arrowprops=arr, zorder=9)
        ax.annotate("Lower\nlimb", xy=(-3.4, -62), xytext=(xl, -64), ha="left",
                    va="center", fontsize=fs, arrowprops=arr, zorder=9)
        ax.text(4.0, -19.5, "Riser", rotation=90, ha="center", va="center",
                fontsize=7, bbox=dict(fc="white", ec="none", pad=0.6), zorder=9)
        ax.annotate("String", xy=(0.4, 48), xytext=(XLIM[1] - 0.5, 46), ha="right",
                    va="center", fontsize=fs, arrowprops=arr, zorder=9, bbox=bb)


# Layout: three tall panels side by side
PANEL_H_IN = 4.6
PANEL_W_IN = PANEL_H_IN * (XLIM[1] - XLIM[0]) / (YLIM[1] - YLIM[0])
GAP_IN = 0.35
W_IN = 3 * PANEL_W_IN + 2 * GAP_IN + 0.2
H_IN = PANEL_H_IN + 0.45
fig = plt.figure(figsize=(W_IN, H_IN))
PW, PH = PANEL_W_IN / W_IN, PANEL_H_IN / H_IN
GAP = GAP_IN / W_IN
x0 = (1 - 3 * PW - 2 * GAP) / 2
y0 = 0.35 / H_IN

ax_a = fig.add_axes([x0, y0, PW, PH])
ax_b = fig.add_axes([x0 + PW + GAP, y0, PW, PH])
ax_c = fig.add_axes([x0 + 2 * (PW + GAP), y0, PW, PH])

draw_panel(ax_a, "a", dx_top=9.0, dx_bot=0.0)                     # one limb out
draw_panel(ax_b, "b", dx_top=0.0, dx_bot=0.0, annotate=True, ok=True)  # correct
draw_panel(ax_c, "c", dx_top=9.0, dx_bot=9.0)                     # both limbs out

for ext in ("pdf", "svg", "png"):
    fig.savefig(OUT_DIR / f"limb_alignment.{ext}", bbox_inches="tight", pad_inches=0.05,
                **({"dpi": 200} if ext == "png" else {}))
print("done")
