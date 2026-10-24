import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

# Figures are written to ../figures relative to this script (repo layout:
# <guide>/python_scripts/*.py and <guide>/figures/*.pdf).
OUT_DIR = Path(__file__).resolve().parent.parent / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "mathtext.fontset": "cm",
})

# Geometry (arbitrary units, roughly mm-ish)
R = 3.0            # shaft radius
PL_LEN = 6.0       # plunger protrusion from riser face
PL_HALF = 1.6      # plunger half-height
THETA = np.radians(18.0)   # rest arm angle above horizontal
XC = PL_LEN + R    # shaft centre x (shaft touches plunger tip)

XLIM = (-9, 19)
YLIM = (-11.5, 9.5)


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


def draw_panel(ax, label, arm_end_frac=0.75, dy=0.0, annotate=False, ok=False):
    """arm_end_frac: arm tip x relative to shaft centre, in units of R
                     (0 = centreline, 1 = outer edge).
       dy: vertical offset of shaft centre relative to plunger axis."""
    yc = dy
    # Riser
    ax.add_patch(Rectangle((XLIM[0], YLIM[0]), -XLIM[0], YLIM[1] - YLIM[0],
                           facecolor="0.88", edgecolor="k", lw=1.0, hatch="//"))
    # Plunger (rectangle protruding from riser face, axis at y = 0)
    ax.add_patch(Rectangle((0, -PL_HALF), PL_LEN, 2 * PL_HALF,
                           facecolor="white", edgecolor="k", lw=1.0, zorder=3))
    # Plunger axis reference line
    ax.plot([0, XLIM[1] - 0.5], [0, 0], ls="--", lw=0.6, color="0.45", zorder=1)
    # Shaft reference lines: centreline and outer extent
    ax.plot([XC, XC], [YLIM[0] + 0.5, YLIM[1] - 0.5], ls=":", lw=0.6, color="0.45", zorder=1)
    ax.plot([XC + R, XC + R], [YLIM[0] + 0.5, YLIM[1] - 0.5], ls=":", lw=0.6, color="0.45", zorder=1)
    # Rest arm: straight wire from riser face, tangent to the underside of the shaft
    y0 = yc - (R + XC * np.sin(THETA)) / np.cos(THETA)
    x_end = XC + arm_end_frac * R
    y_end = y0 + x_end * np.tan(THETA)
    ax.plot([0, x_end], [y0, y_end], color="k", lw=1.6, solid_capstyle="round", zorder=4)
    # Rest body on riser face
    ax.add_patch(Rectangle((0, y0 - 1.3), 1.6, 2.6, facecolor="white",
                           edgecolor="k", lw=1.0, zorder=3))
    # Arrow shaft
    ax.add_patch(Circle((XC, yc), R, facecolor="white", edgecolor="k", lw=1.2, zorder=5))
    ax.plot([XC], [yc], marker="+", color="k", ms=5, mew=0.8, zorder=6)

    ax.set_xlim(XLIM[1], XLIM[0])  # mirrored: riser on the right (RH archer)
    ax.set_ylim(*YLIM)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0.5, -0.03, f"({label})", transform=ax.transAxes,
            ha="center", va="top", fontsize=10)
    mark(ax, ok, XLIM[1] - 0.6, YLIM[1] - 2.2, 1.6, sx=-1)   # top-left (x axis is mirrored)

    if annotate:
        arr = dict(arrowstyle="-|>", lw=0.8, color="k", shrinkA=0, shrinkB=1)
        ax.text(-4.5, -4, "Riser", rotation=90, ha="center", va="center",
                fontsize=9, bbox=dict(fc="white", ec="none", pad=1.5))
        ax.annotate("Plunger button", xy=(3.0, PL_HALF), xytext=(7.5, 6.0),
                    ha="center", va="bottom", arrowprops=arr)
        ax.annotate("Arrow shaft", xy=(XC + R * 0.72, yc + R * 0.7),
                    xytext=(15.8, 3.8), ha="center", va="bottom", arrowprops=arr)
        xa = XC + 0.1 * R
        ya = y0 + xa * np.tan(THETA)
        ax.annotate("Rest arm", xy=(xa, ya - 0.15), xytext=(14.5, -8.5),
                    ha="center", va="top", arrowprops=arr)


# Layout: a row of three (a, b, c) above a centred row of two (d, e), all at
# the same scale. Wider than tall so the figure shares a page with its text.
PANEL_W_IN = 2.25
PANEL_H_IN = PANEL_W_IN * (YLIM[1] - YLIM[0]) / (XLIM[1] - XLIM[0])
GAPX_IN, GAPY_IN = 0.3, 0.45
W_IN = 3 * PANEL_W_IN + 2 * GAPX_IN + 0.2
H_IN = 2 * PANEL_H_IN + GAPY_IN + 0.35
fig = plt.figure(figsize=(W_IN, H_IN))
PW, PH = PANEL_W_IN / W_IN, PANEL_H_IN / H_IN
GAPX, GAPY = GAPX_IN / W_IN, GAPY_IN / H_IN

x_mid = 0.5 - PW / 2                                   # centre column
x_left3, x_right3 = x_mid - GAPX - PW, x_mid + GAPX + PW   # outer columns, row of three
x_left2, x_right2 = 0.5 - PW - GAPX / 2, 0.5 + GAPX / 2    # row of two, centred
y_top = 1 - 0.02 - PH
y_bot = y_top - GAPY - PH

ax_a = fig.add_axes([x_left3, y_top, PW, PH])
ax_b = fig.add_axes([x_mid, y_top, PW, PH])
ax_c = fig.add_axes([x_right3, y_top, PW, PH])
ax_d = fig.add_axes([x_left2, y_bot, PW, PH])
ax_e = fig.add_axes([x_right2, y_bot, PW, PH])

draw_panel(ax_a, "a", arm_end_frac=0.75, dy=0.0, annotate=True, ok=True)   # correct
draw_panel(ax_b, "b", arm_end_frac=1.8)                          # too far out
draw_panel(ax_c, "c", arm_end_frac=-0.35)                        # too far in
draw_panel(ax_d, "d", dy=+0.55 * R)                              # too high
draw_panel(ax_e, "e", dy=-0.55 * R)                              # too low

for ext in ("pdf", "svg", "png"):
    fig.savefig(OUT_DIR / f"rest_position.{ext}", bbox_inches="tight", pad_inches=0.05,
                **({"dpi": 200} if ext == "png" else {}))
print("done")
