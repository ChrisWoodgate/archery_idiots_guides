# The Idiot's Guide to Recurve Bow Setup, Tuning, and Maintenance

Context for Claude Code. Read this before touching anything in this directory.

## What this is

A short LaTeX handout by Chris Woodgate to accompany a hands-on workshop at
Cleve Archers (Autumn 2026). Audience: club-level recurve archers, mostly
beginners. The tone is plain and practical; the author's stance (Section 1.2)
is that *setup* matters, *tuning* is over-rated at club level, and people
should get their bow into range and go back to practising.

The author retains authorial control. Do not rewrite prose unless asked;
proof-read and flag issues, suggest alternatives, and make the specific edits
requested. Prose is in paragraphs, not bullet points (the only remaining list is
the three definitions in Section 1.1). British spelling throughout.
Critical, polite feedback is welcome; flattery is not.

## Repository layout

```
idiots_guides/                 repository root (README.md, .gitignore)
  setup_and_tuning/            this guide
    setup_and_tuning.tex       the handout (single file, pdflatex)
    CLAUDE.md                  this file
    figures/                   generated figures (PDF for \includegraphics,
                               SVG and PNG alongside)
    python_scripts/            one matplotlib script per figure
```

Figures are *generated*: never hand-edit a file in `figures/`. Each script
writes `../figures/<name>.{pdf,svg,png}` relative to its own location, so
`python3 python_scripts/<name>.py` from anywhere regenerates that figure.
Dependencies: numpy, matplotlib (no others).

## Committing

Claude Code makes the commits. The author reviews the log afterwards, so the
history should read as an explanation of the project, one file at a time.

Procedure for the initial import (all files are already present in the
working tree; nothing needs generating):

1. Check the state first: `git status` and `git log --oneline` (the repo may
   be empty or may already have some of these files). Never commit a file
   that is already tracked and unchanged; never amend or rewrite existing
   history.
2. Add a `.gitignore` as the first commit, containing at least
   `figures/*.png`, `*.aux`, `*.log`, `*.out`, `*.synctex.gz`, `*.fdb_latexmk`,
   `*.fls`, `*.toc` and `__pycache__/`. PNGs are previews only; the PDFs are
   what the document uses.
3. Commit `CLAUDE.md` second.
4. Then the figures, in the order the document uses them (limb alignment,
   tiller, bracing height, nocking point, arrow rest, centreshot, bare shaft,
   walk-back). For each figure make **two** commits: the script
   (`python_scripts/<name>.py`) and then its outputs
   (`figures/<name>.pdf` and `figures/<name>.svg` together, since they are
   one artefact in two formats). Before committing a script, run it and
   confirm the PDF and SVG it writes are byte-for-byte what is in
   `figures/`; if they differ, stop and say so rather than guessing which
   is current.
5. Commit the `.tex` file last, once the author has placed it.

Commit messages: imperative first line under 72 characters, blank line, then
a short body explaining the *logic* of the file, not merely its existence.
For a script, say what the figure shows, what the panels are, the main
drawing decisions (viewpoint, which quantities are exaggerated and roughly by
how much, what is shared with other figures). For a figure commit, one line
referring back to the script is enough. Use the figure table below as the
source for the bodies. Example:

```
Add tiller figure script

Side profile of a strung bow, string on the archer's side, three panels:
negative, correct (0-6 mm positive) and excessive positive tiller. D_top
and D_bottom are dimensioned from the limb-pocket edge to the string;
T = D_top - D_bottom is printed under the strip. The string tilt is
exaggerated roughly sevenfold; the riser outline (shelf, throat, heel) is
shared with bracing_height.py and nocking_point.py and must be kept
identical across the three.
```

Attribution: the commit author is the repository's configured git user
(Christopher Woodgate). Claude Code should add its usual `Co-Authored-By:
Claude <...>` trailer so the history records that the commits were made with
Claude; no other trailers or attribution text. Do not push unless asked.

After the import, the same rule applies to later work: one logical change
per commit, script and regenerated outputs in separate commits, message
body states why.

## Figures

All figures share a house style, defined independently in each script (there
is deliberately no shared module, so each script is self-contained):

* black and white line drawings; riser filled light grey with `//` hatching;
* a green tick on the correct panel and a red cross on each incorrect panel,
  top-left of every panel, drawn as strokes (not font glyphs) so they survive
  font substitution;
* component labels with leader arrows on the *correct* panel only; labels
  that sit over drawn material have a white backing box;
* panels lettered (a), (b), ... beneath; where there is a one-word verdict
  ("Too low", "In range", ...) it sits between the drawing and the letter;
* geometry is exaggerated so the fault is visible at handout size; the
  caption must say so where it matters;
* right-handed bow throughout, mirrored notes in captions;
* serif font, Computer Modern math; 8-9 pt labels.

| Figure | Script | Section | Shows |
|---|---|---|---|
| `rest_position` | `rest_position.py` | 2.6 Arrow rest | Cross-section down the shaft (riser on the right, archer's view). (a) correct: plunger on the shaft centre, rest arm tip 3/4 of the way from centreline to outer edge; (b) arm too far out; (c) too far in; (d) rest too high; (e) too low. Top panel + 2x2 grid. Dashed plunger axis and dotted shaft centreline/outer edge on all panels. |
| `limb_alignment` | `limb_alignment.py` | 2.1 Limb alignment | From behind the bow, riser face-on with sight window, limb bolts and stabiliser bushing; string tip-to-tip; dashed limb centrelines. (a) upper limb out; (b) correct; (c) both limbs out the same way. Widths exaggerated x2 as well as the offsets. |
| `tiller` | `tiller.py` | 2.3 Tiller | Side profile, string on the right. D_top and D_bottom dimensioned from pocket edge to string; T = D_top - D_bottom under the strip. (a) T<0; (b) 0<=T<=6 mm; (c) T>6 mm. |
| `bracing_height` | `bracing_height.py` | 2.4 Bracing height | Same bow as tiller, symmetric. Button end-on; B dimensioned button-to-string; nocking points; BH gauge on (b). (a) too low; (b) in range; (c) too high. |
| `nocking_point` | `nocking_point.py` | 2.7 Nocking point | Side view cropped to the sight window; arrow nocked on the rest; dashed "square" line through the top of the rest arm; h_N dimensioned to the underside of the nock. (a) too low; (b) in range; (c) too high. |
| `centreshot` | `centreshot.py` | 2.8 Centreshot | From behind, slightly above; string vertical; shaft as a tapering wedge; plunger visible. (a) too far out; (b) correct (3/4 of the point visible left of the string); (c) too far in. |
| `bare_shaft` | `bare_shaft.py` | 3.1 Bare shaft | Target face, arrows nock-end-on. (a) good: bare shafts slightly low-left of fletched; (b) bare left: arrows too stiff or button too firm; (c) bare right: weak / soft; (d) bare low: nocking point too high; (e) bare high: nocking point too low. Top panel + 2x2 grid. |
| `walkback` | `walkback.py` | 3.2 Walk-back | Tall target face, aiming mark near the top, plumb line; one arrow per distance (10-30 m in 5 m steps, then 40 m) walking down. (a) drifting left: slightly stiff, soften button; (b) straight; (c) drifting right: slightly weak, stiffen button. Button *tension* only; centreshot is not touched here. |

The three side-profile figures (`tiller`, `bracing_height`, `nocking_point`)
draw the same riser (grip with shelf, throat and heel, button at y=4 between
pockets at y=+-30) from the same point lists; if the riser shape changes in
one it must change in all three.

## State of the document

The `.tex` file is the author's draft. As of 24 Oct 2026 the figures are
finished and placed, and Section 2 follows the setup procedure:

1. Limb alignment, 2. Draw weight, 3. Tiller, 4. Bracing height, 5. Arrows,
6. Arrow rest, 7. Nocking point, 8. Centreshot, 9. Pressure button tension.

Arrows come straight after bracing height because everything from there on
depends on the shaft diameter; the rest comes before the nocking point
because the nocking point is measured from the rest. Draw weight, pressure
button tension, the clicker sentence under Arrows and the clicker check in
Maintenance were drafted by Claude on 24 Oct 2026 and await the author's
edit. Things known to need doing in the `.tex`:

* Section 1.3 (Reading list) is empty.
* Section 4 (Maintenance) has three short topics (sight marks, clicker,
  string waxing), all prose; the author may want more.
* `graphicx` is loaded with `\graphicspath{{figures/}}`, so figures are
  included as `\includegraphics[width=...]{<name>.pdf}`; labels are
  `fig:rest-position`, `fig:limb-alignment`, `fig:tiller`,
  `fig:bracing-height`, `fig:nocking-point`, `fig:centreshot`,
  `fig:bare-shaft`, `fig:walkback`. The Tuning section carries
  `\label{sec:tuning}`.

## Conventions used in the text

* Bracing height ranges: 66" 210-230 mm, 68" 215-235 mm, 70" 220-240 mm.
* Tiller: 0-6 mm positive, ~3 mm starting point.
* Nocking point: top of the lower nocking point 2-8 mm above square, 4 mm
  starting point; two tied-on points, no brass.
* Centreshot: between half and one full point width visible left of the
  string (RH); figure shows three-quarters.
* Rest arm: extends past the shaft centreline but not beyond its outer
  extent.
* Bare-shaft: "good" is bare shafts slightly low and left of the fletched
  group (RH).
* Walk-back adjusts button *tension*: drift left = stiff = soften; drift
  right = weak = stiffen (RH).
