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

# Side profile, riser vertical, string on the right (archer's side), viewed from
# the sight-window side so the pressure button is seen end-on. Same bow as the
# tiller figure, with symmetric tiller and a varying bracing height. Units ~ cm,
# differences exaggerated.
XLIM = (-50.0, 22.0)
YLIM = (-96.0, 96.0)

XP = -20.0        # x of the limb pocket (where limb meets riser)
YP = 30.0         # +/- y of the limb pockets
YT = 85.0         # +/- y of the limb tips
YC = 79.0         # +/- y of the string contact point on the limb
TIP_CURL = 5.0
RISER_T = 4.5
Y_BUTTON = 4.0    # pressure button, a little above centre between the pockets
Y_SHELF = 0.0     # widest point of the riser belly, just below the button
Y_THROAT = -5.0   # grip throat (pivot point)
R_BUTTON = 1.3


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


def draw_panel(ax, label, bh, annotate=False, ok=False, verdict=""):
    """bh: drawn bracing height, button centre to string."""
    x_button = XP - 1.6          # button at the riser mid-thickness
    xs = x_button + bh           # string x (vertical, symmetric tiller)

    # Riser
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
    for y in (YP - 4, -(YP - 4)):
        ax.add_patch(Circle((XP - RISER_T / 2 - 0.7, y), 1.1, facecolor="white",
                            edgecolor="k", lw=0.8, zorder=3))
    # Pressure button, seen end-on
    ax.add_patch(Circle((x_button, Y_BUTTON), R_BUTTON, facecolor="white",
                        edgecolor="k", lw=0.9, zorder=6))
    ax.add_patch(Circle((x_button, Y_BUTTON), 0.4, facecolor="k", edgecolor="k",
                        lw=0.5, zorder=6))

    # Limbs: more bend for a higher bracing height
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

    for sgn in (+1, -1):
        pts = limb_pts(sgn, xs)
        ax.plot(pts[:, 0], pts[:, 1], color="k", lw=3.0, solid_capstyle="round", zorder=4)

    # String and nocking points (just above the button height)
    ax.plot([xs, xs], [-YC, YC], color="k", lw=1.0, zorder=5)
    for y in (Y_BUTTON + 2.0, Y_BUTTON + 4.4):
        ax.plot([xs, xs], [y - 0.55, y + 0.55], color="k", lw=3.0,
                solid_capstyle="butt", zorder=7)

    # Dimension line: button centre to string
    dim = dict(arrowstyle="<|-|>", lw=0.7, color="k", shrinkA=0, shrinkB=0,
               mutation_scale=7)
    ax.annotate("", xy=(x_button + R_BUTTON, Y_BUTTON), xytext=(xs, Y_BUTTON),
                arrowprops=dim, zorder=8)
    ax.text((x_button + xs) / 2, Y_BUTTON - 1.6, r"$B$", ha="center", va="top",
            fontsize=9, zorder=8)

    # Bracing-height gauge on the correct panel: clip on the string, arm to the button
    if annotate:
        clip_w, clip_h = 1.6, 13.0
        ax.add_patch(Rectangle((xs - clip_w / 2, Y_BUTTON - 1.5), clip_w, clip_h,
                               facecolor="white", edgecolor="k", lw=0.8, zorder=5.5))
        arm_top = Y_BUTTON + 2.8
        ax.add_patch(Rectangle((x_button + R_BUTTON + 0.3, arm_top - 2.0),
                               xs - clip_w / 2 - (x_button + R_BUTTON + 0.3), 2.0,
                               facecolor="white", edgecolor="k", lw=0.8, zorder=5.5))
        for i, xg in enumerate(np.arange(xs - clip_w / 2, x_button + R_BUTTON + 0.3, -1.0)):
            ax.plot([xg, xg], [arm_top, arm_top - (0.9 if i % 5 == 0 else 0.5)],
                    color="k", lw=0.5, zorder=5.6)

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
        bb = dict(fc="white", ec="none", pad=1.0)
        ax.text(XP - RISER_T / 2 - 0.3, -17, "Riser", rotation=90, ha="center",
                va="center", fontsize=fs, bbox=bb, zorder=9)
        ax.annotate("String", xy=(xs + 0.2, -52), xytext=(XLIM[1] - 0.5, -60),
                    ha="right", va="center", fontsize=fs, arrowprops=arr, zorder=9)
        ax.annotate("Pressure button", xy=(x_button - R_BUTTON, Y_BUTTON + 0.4),
                    xytext=(XLIM[0] + 1, 26), ha="left", va="center", fontsize=fs,
                    arrowprops=arr, zorder=9, bbox=bb)
        ax.annotate("Nocking points", xy=(xs + 0.5, Y_BUTTON + 3.2),
                    xytext=(XLIM[1] - 0.5, 44), ha="right", va="center", fontsize=fs,
                    arrowprops=arr, zorder=9, bbox=bb)
        ax.annotate("BH gauge", xy=(xs + 0.9, Y_BUTTON - 1.0),
                    xytext=(XLIM[1] - 0.5, -14), ha="right", va="center", fontsize=fs,
                    arrowprops=arr, zorder=9, bbox=bb)


# Layout: three tall panels side by side
PANEL_H_IN = 4.6
PANEL_W_IN = PANEL_H_IN * (XLIM[1] - XLIM[0]) / (YLIM[1] - YLIM[0])
GAP_IN = 0.35
W_IN = 3 * PANEL_W_IN + 2 * GAP_IN + 0.2
H_IN = PANEL_H_IN + 0.5
fig = plt.figure(figsize=(W_IN, H_IN))
PW, PH = PANEL_W_IN / W_IN, PANEL_H_IN / H_IN
GAP = GAP_IN / W_IN
x0 = (1 - 3 * PW - 2 * GAP) / 2
y0 = 0.4 / H_IN

ax_a = fig.add_axes([x0, y0, PW, PH])
ax_b = fig.add_axes([x0 + PW + GAP, y0, PW, PH])
ax_c = fig.add_axes([x0 + 2 * (PW + GAP), y0, PW, PH])

draw_panel(ax_a, "a", bh=15.0, verdict="Too low")
draw_panel(ax_b, "b", bh=22.0, annotate=True, ok=True, verdict="In range")
draw_panel(ax_c, "c", bh=29.0, verdict="Too high")

for ext in ("pdf", "svg", "png"):
    fig.savefig(OUT_DIR / f"bracing_height.{ext}", bbox_inches="tight", pad_inches=0.05,
                **({"dpi": 200} if ext == "png" else {}))
print("done")
