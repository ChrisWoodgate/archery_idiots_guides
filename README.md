# Archery idiot's guides

Short, practical handouts for club-level recurve archers, written by
Christopher Woodgate to accompany hands-on workshops at Cleve Archers.

## Guides

| Directory | Guide |
|---|---|
| `setup_and_tuning/` | *The Idiot's Guide to Recurve Bow Setup, Tuning, and Maintenance* (Autumn 2026) |

Each guide is a single LaTeX file with its figures in `figures/` and the
scripts that draw them in `python_scripts/`.

## Building

From inside a guide's directory:

```sh
pdflatex setup_and_tuning.tex
pdflatex setup_and_tuning.tex
```

## Figures

Figures are generated, never hand-edited. Each script writes a PDF (used by
the document), an SVG and a PNG preview to `../figures/`:

```sh
python3 python_scripts/tiller.py
```

Requires Python 3 with numpy and matplotlib.
