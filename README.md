# Anti-angiogenic therapy combined with surgery: modelling VEGF blockade to prevent post-resection metastatic growth

This repository holds a research manuscript and every piece of code needed to reproduce it.

## Manuscript files

| File | Contents |
|---|---|
| `manuscript/manuscript.docx` | Editable Word version. Equations are native Word equations; figures and tables are embedded; line numbers are on. |
| `manuscript/manuscript.pdf` | Typeset PDF (A4) |
| `manuscript/manuscript.html` | Self-contained HTML version (equations in MathML, figures embedded) |
| `manuscript/manuscript.md` | Source text that all three versions are built from |
| `manuscript/references.txt` | Reference list (Vancouver style). Numbers are assigned automatically in the order references are first cited. |
| `manuscript/figures/` | Figures 1–8 as SVG (vector) and PNG (300 dpi equivalent) |

Contents: about 6,000 words of body text, 34 numbered equations, 8 figures, 6 tables and 36 references.

## Reproducing the results

The simulations use a C++17 compiler. Everything else uses only the Python 3 standard library. Headless Chromium is used for PDF and PNG output.

```bash
g++ -O3 -march=native -fopenmp -o build/melanoma_vegf model/melanoma_vegf.cpp
python3 model/experiments.py      # all simulation experiments, written to runs/ (~40 min on 8 cores)
python3 tools/analyze.py          # outcome metrics, written to results/summary.json
python3 tools/make_figures.py     # SVG figures
python3 tools/render.py           # PNG figures
python3 tools/build_manuscript.py # HTML, PDF and DOCX
```

`model/base_params.txt` contains all baseline parameters. Any parameter can be overridden on the command line, for example `build/melanoma_vegf model/base_params.txt v_I=0.1 dose_frac=1 drug_start=393 drug_stop=758`.

## Before submission

- Fill in the author names, affiliations, funding and conflict-of-interest statements (marked `[...]`).
- The reference list was compiled without internet access. Check every entry (authors, volume and pages) against PubMed or the publisher before submission.
- Several immune and drug-transport parameters are calibrated rather than measured (see Table 2 of the manuscript).

Fonts: the DejaVu fonts in `fonts/` are used only for rendering. Their licence is in `fonts/LICENSE-dejavu.md`.

# Book chapter: Academic Identity and Professional Development

Authors: Meenu Rani and Amman Jakhar. Written for the edited volume *Higher Education Beyond Boundaries: Dynamics, Change, Challenges and Opportunities*.

| File | Contents |
|---|---|
| `chapter/chapter.docx` | Editable Word version |
| `chapter/chapter.pdf` | Typeset PDF |
| `chapter/chapter.md` | Source text |
| `chapter/references.txt` | 36 references in APA 7 style, numbered in order of first citation |
| `chapter/figures/` | Figures 1–4 as SVG and PNG |

To rebuild: `python3 tools/chapter_figures.py`, then `DOC_DIR=chapter DOC_SRC=chapter.md DOC_OUT=chapter DOC_LINENUM=0 python3 tools/build_manuscript.py`. The reference list was compiled without internet access, so check every entry before submission.

# Book chapter: Mechanical Characterization of 3D-Printed PLA–ZnO Composites

| File | Contents |
|---|---|
| `pla_zno_chapter/chapter.docx` | Editable Word version |
| `pla_zno_chapter/chapter.pdf` | Typeset PDF |
| `pla_zno_chapter/chapter.md` | Source text |
| `pla_zno_chapter/figures/` | Figures 1–6 as SVG and PNG |

The chapter has no reference list: literature citations were removed at the author's request.

To rebuild: `python3 tools/pla_zno_figures.py`, then `DOC_DIR=pla_zno_chapter DOC_SRC=chapter.md DOC_OUT=chapter DOC_LINENUM=0 python3 tools/build_manuscript.py`.

Before submission:

- Figure 2 is a placeholder. Replace `pla_zno_chapter/figures/fig2_equipment.png` with the original four-panel laboratory photograph and rebuild.
- Fill in the items in square brackets: authors, affiliation, PLA and ZnO supplier and grade, extruder model and screw speed, printer model, testing machine and durometer.
- The processing, printing and test settings (Tables 2–4 and Figures 1, 4 and 5) are typical values for PLA. Replace any that differ from what was actually used in the laboratory.
- The ethanol-assisted ZnO coating step (Section 2.3) was written to match the magnetic stirrer shown in Figure 2. Confirm it describes the actual mixing procedure.
- Table 6 is empty. Enter the measured values when testing is complete.
