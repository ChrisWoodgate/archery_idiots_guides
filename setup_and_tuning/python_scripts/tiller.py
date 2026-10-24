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

# Side profile, riser vertical, string on the right (archer's side).
# Units ~ cm, but the tiller asymmetry is exaggerated by a factor ~7.
XLIM = (-50.0, 14.0)
YLIM = (-96.0, 96.0)

XP = -20.0        # x of the limb pocket (where limb meets riser)
YP = 30.0         # +/- y of the limb pockets
YT = 85.0         # +/- y of the limb tips
YC = 79.0         # +/- y of the string contact point on the limb
TIP_CURL = 5.0    # how far the tip curls away from the string
RISER_T = 4.5     # riser thickness
Y_SHELF = 0.0     # widest point of the riser belly (arrow shelf)
Y_THROAT = -5.0   # grip throat (pivot point)


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


def bezier(p0, p1, p2, p3, n=60):
    t = np.linspace(0, 1, n)[:, None]
    return ((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1
            + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3)


def catmull_rom(pts, n_per=12):
    """Smooth open curve through pts (Catmull-Rom)."""
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


def draw_panel(ax, label, d_top, d_bot, annotate=False, ok=False, verdict=""):
    # Tip positions such that the pocket-to-string distances are d_top, d_bot
    span = 2 * YC
    b_minus_a = (d_top - d_bot) * span / (2 * YP)
    a = d_bot + XP - b_minus_a * (YC - YP) / span     # lower contact point x
    b = a + b_minus_a                                   # upper tip x

    # Riser: a slightly waisted vertical band with a grip on the string side
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
    # Limb bolts
    for y in (YP - 4, -(YP - 4)):
        ax.add_patch(Circle((XP - RISER_T / 2 - 0.7, y), 1.1, facecolor="white",
                            edgecolor="k", lw=0.8, zorder=3))

    # Limbs: working section from pocket to string contact point (arriving
    # parallel to the string), then a short recurved tip curling away from it
    def limb_pts(sgn, xc):
        p0 = np.array([XP, sgn * YP])
        p1 = np.array([XP - 6, sgn * (YP + 16)])
        p2 = np.array([xc, sgn * (YC - 20)])
        p3 = np.array([xc, sgn * YC])
        work = bezier(p0, p1, p2, p3)
        q1 = np.array([xc, sgn * (YC + 3.5)])
        q2 = np.array([xc - TIP_CURL + 1.5, sgn * (YT - 1.0)])
        q3 = np.array([xc - TIP_CURL, sgn * YT])
        tip = bezier(p3, q1, q2, q3, n=20)
        return np.vstack([work, tip])

    for sgn, xc in ((+1, b), (-1, a)):
        pts = limb_pts(sgn, xc)
        ax.plot(pts[:, 0], pts[:, 1], color="k", lw=3.0, solid_capstyle="round", zorder=4)

    # String
    ax.plot([a, b], [-YC, YC], color="k", lw=1.0, zorder=5)

    # Dimension lines at the pockets
    def x_string(y):
        return a + (b - a) * (y + YC) / span

    dim = dict(arrowstyle="<|-|>", lw=0.7, color="k", shrinkA=0, shrinkB=0,
               mutation_scale=7)
    for y, txt, dyt in ((YP, r"$D_\mathrm{top}$", 2.5), (-YP, r"$D_\mathrm{bottom}$", -2.5)):
        xs = x_string(y)
        ax.annotate("", xy=(XP, y), xytext=(xs, y), arrowprops=dim, zorder=6)
        # thin extension line from the string to just past the dimension line
        ax.plot([xs, xs + 3.5], [y, y], color="0.45", lw=0.5, zorder=1)
        ax.text((XP + xs) / 2, y + dyt, txt, ha="center",
                va="bottom" if dyt > 0 else "top", fontsize=9, zorder=7)

    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0.5, -0.03, f"({label})", transform=ax.transAxes,
            ha="center", va="top", fontsize=10)
    mark(ax, ok, XLIM[0] + 1.5, YLIM[1] - 7.5, 6.0)
    if verdict:
        ax.text(0.5, 0.0, verdict, transform=ax.transAxes, ha="center",
                va="bottom", fontsize=9)

    if annotate:
        arr = dict(arrowstyle="-|>", lw=0.8, color="k", shrinkA=0, shrinkB=1)
        fs = 8
        ax.text(XP - RISER_T / 2 - 0.3, -17, "Riser", rotation=90, ha="center",
                va="center", fontsize=fs, bbox=dict(fc="white", ec="none", pad=1.0), zorder=9)
        pu = limb_pts(+1, b)[28]
        ax.annotate("Upper limb", xy=(pu[0] - 1.3, pu[1]), xytext=(XLIM[0] + 1, 70),
                    ha="left", va="center", fontsize=fs, arrowprops=arr, zorder=9)
        pl = limb_pts(-1, a)[28]
        ax.annotate("Lower limb", xy=(pl[0] - 1.3, pl[1]), xytext=(XLIM[0] + 1, -70),
                    ha="left", va="center", fontsize=fs, arrowprops=arr, zorder=9)
        ax.annotate("String", xy=(x_string(0) - 0.2, 0), xytext=(XLIM[1] - 0.5, -16),
                    ha="right", va="center", fontsize=fs, arrowprops=arr, zorder=9,
                    bbox=dict(fc="white", ec="none", pad=1.0))
        ax.annotate("Limb pocket", xy=(XP - RISER_T - 0.5, YP - 0.5), xytext=(XLIM[0] + 1, 16),
                    ha="left", va="center", fontsize=fs, arrowprops=arr, zorder=9,
                    bbox=dict(fc="white", ec="none", pad=1.0))


# Layout: three tall panels side by side, equation underneath
PANEL_H_IN = 4.6
PANEL_W_IN = PANEL_H_IN * (XLIM[1] - XLIM[0]) / (YLIM[1] - YLIM[0])
GAP_IN = 0.35
W_IN = 3 * PANEL_W_IN + 2 * GAP_IN + 0.2
H_IN = PANEL_H_IN + 0.95
fig = plt.figure(figsize=(W_IN, H_IN))
PW, PH = PANEL_W_IN / W_IN, PANEL_H_IN / H_IN
GAP = GAP_IN / W_IN
x0 = (1 - 3 * PW - 2 * GAP) / 2
y0 = 0.72 / H_IN

ax_a = fig.add_axes([x0, y0, PW, PH])
ax_b = fig.add_axes([x0 + PW + GAP, y0, PW, PH])
ax_c = fig.add_axes([x0 + 2 * (PW + GAP), y0, PW, PH])

# Drawn distances (exaggerated): real-world equivalents ~ -3 mm, +3 mm, +9 mm
draw_panel(ax_a, "a", d_top=20.0, d_bot=23.0, verdict=r"$T<0$")
draw_panel(ax_b, "b", d_top=23.0, d_bot=21.0, annotate=True, ok=True,
           verdict=r"$0\leq T\leq 6\,\mathrm{mm}$")
draw_panel(ax_c, "c", d_top=26.0, d_bot=19.0, verdict=r"$T>6\,\mathrm{mm}$")

fig.text(0.5, 0.045, r"$T = D_\mathrm{top} - D_\mathrm{bottom}$", ha="center",
         va="center", fontsize=10)

for ext in ("pdf", "svg", "png"):
    fig.savefig(OUT_DIR / f"tiller.{ext}", bbox_inches="tight", pad_inches=0.05,
                **({"dpi": 200} if ext == "png" else {}))
print("done")
