import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

# Figures are written to ../figures relative to this script (repo layout:
# <guide>/python_scripts/*.py and <guide>/figures/*.pdf).
OUT_DIR = Path(__file__).resolve().parent.parent / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "mathtext.fontset": "cm",
})

# Image-space geometry (arbitrary units). View: from behind the bow, slightly
# above the arrow, eye in the plane of the string. String at x = 0, riser to the
# right (right-handed bow). Near end (nock) is low in the image, far end (point)
# high, with the shaft tapering towards the point.
XLIM = (-5.5, 11.0)
YLIM = (-9.0, 9.0)

RISER_X = 7.0        # left face of the riser section
Y_NOCK, Y_POINT = -5.5, 5.5
HW_NOCK, HW_POINT = 1.2, 0.6      # shaft half-widths at near/far end
W_POINT = 2 * HW_POINT            # apparent width of the point
T_PLUNGER = 0.45                  # fraction of the way along the shaft (image)
PL_HALF = 0.45                    # plunger half-height


def mark(ax, ok, x, y, s, sx=1):
    """Green tick or red cross; (x, y) = lower-left corner of an s x s box."""
    if ok:
        ax.plot([x, x + sx * 0.38 * s, x + sx * s], [y + 0.45 * s, y, y + 0.95 * s],
                color="#2ca02c", lw=2.2, solid_capstyle="round",
                solid_joinstyle="round", zorder=10)
    else:
        ax.plot([x, x + sx * s], [y, y + s], color="#d62728", lw=2.2,
                solid_capstyle="round", zorder=10)
        ax.plot([x, x + sx * s], [y + s, y], color="#d62728", lw=2.2,
                solid_capstyle="round", zorder=10)


def draw_panel(ax, label, point_offset, annotate=False, ok=False):
    """point_offset: x of the point's centre relative to the string, in units
       of the point's apparent width (negative = to the left of the string)."""
    xp = point_offset * W_POINT

    # Riser section (behind everything)
    ax.add_patch(Rectangle((RISER_X, YLIM[0]), XLIM[1] - RISER_X, YLIM[1] - YLIM[0],
                           facecolor="0.88", edgecolor="k", lw=1.0, hatch="//", zorder=1))

    # Shaft: tapering wedge from nock to point
    shaft = np.array([
        [-HW_NOCK, Y_NOCK], [HW_NOCK, Y_NOCK],
        [xp + HW_POINT, Y_POINT], [xp - HW_POINT, Y_POINT],
    ])
    ax.add_patch(Polygon(shaft, closed=True, facecolor="white", edgecolor="k",
                         lw=1.1, zorder=4))
    # Point (pile): small filled taper beyond the shaft end
    pile = np.array([
        [xp - HW_POINT, Y_POINT], [xp + HW_POINT, Y_POINT],
        [xp + 0.22, Y_POINT + 1.0], [xp - 0.22, Y_POINT + 1.0],
    ])
    ax.add_patch(Polygon(pile, closed=True, facecolor="0.25", edgecolor="k",
                         lw=0.8, zorder=5))

    # Plunger: from riser face to the right-hand edge of the shaft
    y_pl = Y_NOCK + T_PLUNGER * (Y_POINT - Y_NOCK)
    hw_pl = HW_NOCK + T_PLUNGER * (HW_POINT - HW_NOCK)
    x_tip = T_PLUNGER * xp + hw_pl
    ax.add_patch(Rectangle((x_tip, y_pl - PL_HALF), RISER_X - x_tip, 2 * PL_HALF,
                           facecolor="white", edgecolor="k", lw=1.0, zorder=3))

    # Nock (slightly wider than the shaft) and nocking points
    ax.add_patch(Rectangle((-HW_NOCK - 0.25, Y_NOCK - 0.55), 2 * HW_NOCK + 0.5, 1.1,
                           facecolor="white", edgecolor="k", lw=1.0, zorder=6))
    for dy in (+1.05, -1.05):
        ax.plot([0, 0], [Y_NOCK + dy - 0.2, Y_NOCK + dy + 0.2], color="k",
                lw=3.2, solid_capstyle="butt", zorder=8)

    # String (in front of everything)
    ax.plot([0, 0], [YLIM[0] + 0.4, YLIM[1] - 0.4], color="k", lw=1.2, zorder=7)

    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0.5, -0.03, f"({label})", transform=ax.transAxes,
            ha="center", va="top", fontsize=10)
    mark(ax, ok, XLIM[0] + 0.4, YLIM[1] - 2.0, 1.6)

    if annotate:
        arr = dict(arrowstyle="-|>", lw=0.8, color="k", shrinkA=0, shrinkB=1)
        ax.text(RISER_X + 2.0, -3.0, "Riser", rotation=90, ha="center", va="center",
                fontsize=9, bbox=dict(fc="white", ec="none", pad=1.5), zorder=9)
        ax.annotate("String", xy=(0.0, 7.6), xytext=(3.0, 8.2),
                    ha="left", va="center", arrowprops=arr, zorder=9)
        ax.annotate("Point", xy=(xp - 0.1, Y_POINT + 0.6), xytext=(-4.3, 5.8),
                    ha="center", va="center", arrowprops=arr, zorder=9)
        ax.annotate("Shaft", xy=(0.72 * xp - 0.5, Y_NOCK + 0.72 * (Y_POINT - Y_NOCK)),
                    xytext=(-4.3, 3.8), ha="center", va="center", arrowprops=arr, zorder=9)
        ax.annotate("Plunger button", xy=(x_tip + 2.2, y_pl + PL_HALF),
                    xytext=(5.8, 3.2), ha="center", va="bottom", arrowprops=arr, zorder=9,
                    bbox=dict(fc="white", ec="none", pad=1.5))
        ax.annotate("Nock", xy=(-HW_NOCK - 0.25, Y_NOCK), xytext=(-4.3, -5.5),
                    ha="center", va="center", arrowprops=arr, zorder=9)


# Layout: three panels side by side, same scale
PANEL_W_IN = 1.85
PANEL_H_IN = PANEL_W_IN * (YLIM[1] - YLIM[0]) / (XLIM[1] - XLIM[0])
GAP_IN = 0.25
W_IN = 3 * PANEL_W_IN + 2 * GAP_IN + 0.2
H_IN = PANEL_H_IN + 0.4
fig = plt.figure(figsize=(W_IN, H_IN))
PW, PH = PANEL_W_IN / W_IN, PANEL_H_IN / H_IN
GAP = GAP_IN / W_IN
x0 = (1 - 3 * PW - 2 * GAP) / 2
y0 = 0.3 / H_IN

ax_a = fig.add_axes([x0, y0, PW, PH])
ax_b = fig.add_axes([x0 + PW + GAP, y0, PW, PH])
ax_c = fig.add_axes([x0 + 2 * (PW + GAP), y0, PW, PH])

draw_panel(ax_a, "a", point_offset=-1.75)                  # too far out
draw_panel(ax_b, "b", point_offset=-0.25, annotate=True, ok=True)   # correct: 3/4 of point visible
draw_panel(ax_c, "c", point_offset=+0.40)                  # too far in

for ext in ("pdf", "svg", "png"):
    fig.savefig(OUT_DIR / f"centreshot.{ext}", bbox_inches="tight", pad_inches=0.05,
                **({"dpi": 200} if ext == "png" else {}))
print("done")
