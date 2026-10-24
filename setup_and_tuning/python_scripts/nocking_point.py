import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle

# Figures are written to ../figures relative to this script (repo layout:
# <guide>/python_scripts/*.py and <guide>/figures/*.pdf).
OUT_DIR = Path(__file__).resolve().parent.parent / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "mathtext.fontset": "cm",
})

# Side view of the riser around the sight window, string on the right, arrow
# nocked and lying on the rest. Same riser as the tiller / bracing-height
# figures, cropped top and bottom. Nocking-point height exaggerated.
XLIM = (-42.0, 25.0)
YLIM = (-14.0, 27.0)

XP = -20.0
YP = 30.0
YC = 79.0
YT = 85.0
TIP_CURL = 5.0
RISER_T = 4.5
Y_BUTTON = 4.0
Y_SHELF = 0.0
Y_THROAT = -5.0
R_BUTTON = 1.3
BH = 22.0            # bracing height (button centre to string)
R_SHAFT = 0.45       # shaft half-thickness
X_BUTTON = XP - 1.6
XS = X_BUTTON + BH   # string x
X_REST = X_BUTTON - 0.8          # rest-arm tip, just ahead of the button
Y_SQUARE = Y_BUTTON - R_BUTTON - 0.2   # top of the rest arm = "square" reference


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


def bezier(p0, p1, p2, p3, n=60):
    t = np.linspace(0, 1, n)[:, None]
    return ((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1
            + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3)


def catmull_rom(pts, n_per=12):
    pts = np.asarray(pts, dtype=float)
    p = np.vstack([pts[0], pts, pts[-1]])
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for t in np.linspace(0, 1, n_per, endpoint=False):
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t
                              + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(p[-2])
    return np.array(out)


def draw_panel(ax, label, h, annotate=False, ok=False, verdict=""):
    """h: height of the underside of the nock above the square line."""
    # Riser (same outline as the other side-view figures; cropped by the axes)
    back = np.array([[XP - RISER_T, -YP], [XP - RISER_T - 1.5, -12], [XP - RISER_T - 1.5, 12],
                     [XP - RISER_T, YP]])
    belly = catmull_rom([
        [XP, YP], [XP + 0.4, 16], [XP + 2.0, Y_SHELF + 5], [XP + 3.6, Y_SHELF],
        [XP + 2.0, Y_SHELF - 3], [XP + 0.2, Y_THROAT], [XP + 2.5, Y_THROAT - 5],
        [XP + 5.5, Y_THROAT - 10], [XP + 4.6, Y_THROAT - 15], [XP + 1.2, -28.5], [XP, -YP],
    ])
    riser = np.vstack([back, belly])
    ax.add_patch(Polygon(riser, closed=True, facecolor="0.88", edgecolor="k",
                         lw=1.0, hatch="//", zorder=2))
    ax.add_patch(Circle((XP - RISER_T / 2 - 0.7, YP - 4), 1.1, facecolor="white",
                        edgecolor="k", lw=0.8, zorder=3))
    # Upper limb stub (cropped by the axes)
    p0 = np.array([XP, YP]); p1 = np.array([XP - 6, YP + 16])
    p2 = np.array([XS, YC - 20]); p3 = np.array([XS, YC])
    pts = bezier(p0, p1, p2, p3)
    ax.plot(pts[:, 0], pts[:, 1], color="k", lw=3.0, solid_capstyle="round", zorder=4)

    # Pressure button (end-on) and arrow rest (body on the riser face, arm tip
    # seen end-on just below the shaft)
    ax.add_patch(Circle((X_BUTTON, Y_BUTTON), R_BUTTON, facecolor="white",
                        edgecolor="k", lw=0.9, zorder=5))
    ax.add_patch(Circle((X_BUTTON, Y_BUTTON), 0.4, facecolor="k", zorder=5))
    ax.add_patch(Rectangle((X_BUTTON - 2.6, Y_SQUARE - 3.2), 3.0, 2.2, facecolor="white",
                           edgecolor="k", lw=0.8, zorder=5))
    ax.plot([X_REST, X_REST], [Y_SQUARE - 1.0, Y_SQUARE - 0.3], color="k", lw=1.2, zorder=5)
    ax.add_patch(Circle((X_REST, Y_SQUARE - 0.35), 0.35, facecolor="k", zorder=5))

    # String
    ax.plot([XS, XS], [YLIM[0] - 1, YLIM[1] + 1], color="k", lw=1.0, zorder=6)

    # Arrow: shaft centre-line through the rest contact and the nock centre
    y_nock = Y_SQUARE + h + R_SHAFT
    y_rest = Y_SQUARE + R_SHAFT
    slope = (y_nock - y_rest) / (XS - X_REST)
    x_left = XLIM[0] - 1
    y_left = y_rest + slope * (x_left - X_REST)
    ax.plot([x_left, XS - 1.2], [y_left, y_nock - slope * 1.2], color="k",
            lw=2.3, solid_capstyle="butt", zorder=7)
    # Nock: small block straddling the string, aligned with the shaft
    ang = np.degrees(np.arctan(slope))
    nock = Rectangle((XS - 1.3, y_nock - 0.8), 2.0, 1.6, angle=ang,
                     rotation_point=(XS, y_nock), facecolor="white", edgecolor="k",
                     lw=0.9, zorder=8)
    ax.add_patch(nock)
    # Nocking points: thickened string just above and below the nock
    for y0 in (y_nock + 1.0, y_nock - 1.0):
        sgn = 1 if y0 > y_nock else -1
        ax.plot([XS, XS], [y0, y0 + sgn * 1.3], color="k", lw=2.6,
                solid_capstyle="butt", zorder=9)

    # Square line and dimension
    ax.plot([X_REST - 1.5, XS + 2.5], [Y_SQUARE, Y_SQUARE], ls="--", lw=0.7,
            color="0.3", zorder=6)
    xd = XS + 3.0
    dim = dict(arrowstyle="<|-|>", lw=0.7, color="k", shrinkA=0, shrinkB=0,
               mutation_scale=7)
    y_nock_bottom = Y_SQUARE + h
    ax.annotate("", xy=(xd, Y_SQUARE), xytext=(xd, y_nock_bottom), arrowprops=dim, zorder=9)
    ax.plot([XS + 0.3, xd + 1.0], [y_nock_bottom, y_nock_bottom], color="0.3", lw=0.5,
            zorder=6)
    ax.text(xd + 1.0, (Y_SQUARE + y_nock_bottom) / 2, r"$h_N$", ha="left", va="center",
            fontsize=9, zorder=9)

    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0.5, -0.24, f"({label})", transform=ax.transAxes,
            ha="center", va="top", fontsize=10)
    mark(ax, ok, XLIM[0] + 1.5, YLIM[1] - 5.5, 4.0)
    if verdict:
        ax.text(0.5, -0.04, verdict, transform=ax.transAxes, ha="center",
                va="top", fontsize=9)

    if annotate:
        arr = dict(arrowstyle="-|>", lw=0.8, color="k", shrinkA=0, shrinkB=1)
        fs = 7
        bb = dict(fc="white", ec="none", pad=0.8)
        xl, xr = XLIM[0] + 1.0, XLIM[1] - 0.5
        ax.text(XP - RISER_T / 2 - 0.3, -9.5, "Riser", rotation=90, ha="center",
                va="center", fontsize=fs, bbox=bb, zorder=11)
        ax.annotate("Pressure\nbutton", xy=(X_BUTTON - R_BUTTON, Y_BUTTON + 0.6),
                    xytext=(xl, 16), ha="left", va="center", fontsize=fs,
                    arrowprops=arr, zorder=11, bbox=bb)
        ax.annotate("Arrow\nrest", xy=(X_BUTTON - 2.6, Y_SQUARE - 2.2),
                    xytext=(xl, -7), ha="left", va="center", fontsize=fs,
                    arrowprops=arr, zorder=11, bbox=bb)
        xa = XLIM[0] + 6
        ax.annotate("Arrow", xy=(xa, y_rest + slope * (xa - X_REST) + R_SHAFT),
                    xytext=(xl, 10), ha="left", va="center", fontsize=fs,
                    arrowprops=arr, zorder=11, bbox=bb)
        ax.annotate("Nock", xy=(XS - 1.3, y_nock + 0.9), xytext=(XS - 11, 19),
                    ha="center", va="center", fontsize=fs, arrowprops=arr, zorder=11, bbox=bb)
        ax.annotate("Nocking\npoints", xy=(XS + 0.4, y_nock + 1.8), xytext=(xr, 20),
                    ha="right", va="center", fontsize=fs, arrowprops=arr, zorder=11, bbox=bb)
        ax.annotate("String", xy=(XS + 0.3, -7), xytext=(xr, -10),
                    ha="right", va="center", fontsize=fs, arrowprops=arr, zorder=11, bbox=bb)
        ax.text(XS + 2.6, Y_SQUARE - 0.9, "square", ha="left", va="top", fontsize=7,
                color="0.3", zorder=11)


# Layout
PANEL_W_IN = 2.3
PANEL_H_IN = PANEL_W_IN * (YLIM[1] - YLIM[0]) / (XLIM[1] - XLIM[0])
GAP_IN = 0.25
W_IN = 3 * PANEL_W_IN + 2 * GAP_IN + 0.2
H_IN = PANEL_H_IN + 0.75
fig = plt.figure(figsize=(W_IN, H_IN))
PW, PH = PANEL_W_IN / W_IN, PANEL_H_IN / H_IN
GAP = GAP_IN / W_IN
x0 = (1 - 3 * PW - 2 * GAP) / 2
y0 = 0.6 / H_IN

ax_a = fig.add_axes([x0, y0, PW, PH])
ax_b = fig.add_axes([x0 + PW + GAP, y0, PW, PH])
ax_c = fig.add_axes([x0 + 2 * (PW + GAP), y0, PW, PH])

draw_panel(ax_a, "a", h=-3.5, verdict="Too low")
draw_panel(ax_b, "b", h=3.0, annotate=True, ok=True, verdict="In range")
draw_panel(ax_c, "c", h=9.0, verdict="Too high")

for ext in ("pdf", "svg", "png"):
    fig.savefig(OUT_DIR / f"nocking_point.{ext}", bbox_inches="tight", pad_inches=0.05,
                **({"dpi": 200} if ext == "png" else {}))
print("done")
