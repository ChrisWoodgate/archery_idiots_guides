# Archery idiot's guides

Short, practical handouts for club-level recurve archers, written by
Christopher Woodgate to accompany hands-on workshops at Cleve Archers.

## Guides

| Directory | Guide |
|---|---|
| `setup_and_tuning/` | *The Idiot's Guide to Recurve Bow Setup, Tuning, and Maintenance* (Autumn 2026) |
| `fletching/` | *The Idiot's Guide to Fletching*: fletching aluminium or carbon arrows with plastic vanes and glue (older guide) |
| `maintenance/` | *The Idiot's Guide to Recurve Bow Maintenance*: a short checklist (older draft) |

Each guide is a single LaTeX file named after its directory. The two older
guides are kept for the record; the maintenance draft overlaps with the
setup and tuning guide.
Only `setup_and_tuning/` has figures, in `figures/`, with the scripts that
draw them in `python_scripts/`.

## Building

From inside a guide's directory, run pdflatex twice on its file, for
example:

```sh
cd setup_and_tuning
pdflatex setup_and_tuning.tex
pdflatex setup_and_tuning.tex
```

## Figures

Figures are generated, never hand-edited. Each script writes a PDF (used by
the document), an SVG and a PNG preview to `../figures/`:

```sh
python3 setup_and_tuning/python_scripts/tiller.py
```

Requires Python 3 with numpy and matplotlib.

## Licence

The handouts, including their figures, are licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The Python
scripts that draw the figures are licensed under the MIT License. See
`LICENSE` for details.
