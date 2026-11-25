# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current state

The repository contains the team plan and a code skeleton (stubs raising `NotImplementedError`) for the final AI project at UFC Campus Crateús (Prof. Wellington Franco). The assignment is `_IA__Trabalho_Final.pdf` (git-ignored). The team has 5 students and must pick **one** of ten options. **The team chose option 2 (tourist itinerary optimizer on OSM POIs in Fortaleza), switching from option 6 on 25/11/2026.** See pages 4–5 of the PDF. The team plan is in `PLANEJAMENTO.md`, the per-member backlog in `BACKLOG.md` and the definition of the final delivery in `ENTREGA_FINAL.md`. Treat all three as the source of truth for roles, module boundaries and the checklist. The branches `dados/D1-download` and `dados/D2-D6-serie-diaria` belong to option 6 and are obsolete.

Key dates: presentation on **05/12/2026** (15 min + 5 min of questions, with a live demo). Send the repo link before then, suggested by 04/12/2026 23:59 (Fortaleza time). Method parameters freeze on 01/12, code on 02/12. Create the tag `entrega-05-12-2026` on the evaluated commit and never move it.

## Repository and workflow (option 2)

Remote: https://github.com/marlonmelo12/ia_final. Python package `roteiro` with a src layout (`src/roteiro/`), a Streamlit UI with a pydeck map in `app/app.py`, pipeline scripts in `scripts/` and pytest tests in `tests/`.

```bash
pip install -r requirements.txt && pip install -e .
python scripts/baixar_dados.py          # OSMnx -> data/raw/pois_osm.geojson -> data/pois.csv (20 POIs)
python scripts/experimentos.py          # final experiment, seeds 0-4; do not run before the 02/12 freeze
streamlit run app/app.py
pytest                                   # all tests
pytest tests/test_problema.py::test_x   # single test
```

- `src/roteiro/contratos.py` holds the shared contract: paths, the assignment's constants (30 min visit, 4 km/h, budgets 120/180/240, 20 POIs), column schemas, seeds, the evaluation limit, declared parameters and exceptions. Every module imports from it. Do not change it without a `CONTRATO:` PR approved by all five members.
- Model: a route is an ordered list of `osm_id` without repetition, starting and ending at the user's point. Time = haversine legs at 4 km/h (including the return) + 30 min per visit. Utility = sum of category preferences (1–5). `problema.Avaliador` counts every objective evaluation so hill climbing and simulated annealing share the same `MAX_AVALIACOES`.
- Parameter tuning uses only seeds 100–104 (`SEMENTES_AJUSTE`); seeds 0–4 are reserved for the final experiment.
- Each file has one owner (`BACKLOG.md`, `.github/CODEOWNERS`). Work on branches named `<papel>/<ID>-desc` (`dados`, `problema`, `busca`, `interface`, `qualidade`, `docs`, `fix`), rebase on `main`, and integrate by PR with squash merge. `main` is protected. Details are in `CONTRIBUTING.md`.
- `otimizar.otimizar()` is the single execution path, used by both the experiment script and the UI (acceptance case A5). An insufficient budget returns an empty route with an explanation, not an exception.
- `data/pois.csv` and `data/cenarios.csv` are small and versioned so the demo runs offline. Raw OSM data (`data/raw/`), the OSMnx `cache/` and `execucoes.db` are git-ignored.

## The ten options (each names a required external dataset)

1. Route planner: BFS, uniform cost and A* on an OSMnx walk graph of Fortaleza (center -3.725, -38.525, radius 2000 m).
2. Tourist itinerary: hill climbing with restarts and simulated annealing vs greedy, using OSM POIs in Fortaleza.
3. Timetabling: genetic algorithm vs greedy on ITC2007 `comp01.ectt` (cut to 10/12/15/18/20 courses).
4. Cleaning agents: reactive agent vs model-based agent (BFS) on Moving AI `maze512-1-{0..4}.map` (32×32 crops).
5. Connect Four: minimax vs alpha-beta at depths 2/4/5, using 20 positions from the UCI Connect-4 dataset.
6. Energy forecast: linear regression, Ridge and persistence on UCI Household Power, 2007–2009, with a chronological split.
7. Spam detector: TF-IDF with logistic regression, decision tree and majority baseline on UCI SMS Spam.
8. Dropout risk: logistic regression, decision tree and majority baseline on UCI Students' Dropout (admission-time features only).
9. House prices: linear regression, Ridge, regression tree and mean baseline on UCI Real Estate Valuation.
10. Customer segmentation: RFM features, k-means (k=2..6) vs rule-based grouping on UCI Online Retail.

The PDF spells out per-option details: exact preprocessing, parameters, seeds, experiments and acceptance cases. Re-read the chosen option's pages before implementing.

## Requirements that shape the architecture (every option)

- **Separate layers:** interface, data preparation, AI core and persistence. The interface must be web or desktop. A notebook or terminal-only app does not count. It must cover four functions: configure input, run the method, explain the result, and query/export past runs.
- **Implement the algorithms yourself** for the search, agent, optimization and game options (1–5). Libraries may only help with I/O, visualization and graph loading. For example, OSMnx routing must not replace the team's own A*. For the ML options (6–10), scikit-learn models are allowed, but the team builds the preprocessing, validation, comparison and integration. Calling an external AI service does not satisfy the method requirement.
- **Persistence:** save inputs, parameters and results of every run (structured files or a DB), with history and export.
- **Compare at least two approaches** under equivalent conditions: same instances and the same time or evaluation budgets. For stochastic methods, run several seeds and report mean and dispersion. Label synthetic data as synthetic.
- **Supervised ML protocol** (unless the option prescribes a temporal split): hold out 20% as test, run 5-fold CV on the other 80%, stratify for classification, and dedupe or group before splitting. Fit imputation, encoding, scaling and TF-IDF inside each fold with a `Pipeline`. Use a recorded seed (e.g. 42). Never touch the test set during model or threshold selection.
- **Acceptance cases** need recorded input, expected output and evidence, via automated tests or a reproducible demo script.

## Required repository files

- `README.md`: problem, audience, members, techniques, data source, requirements, install, training (if any) and the command to start the interface.
- `DADOS.md`: dataset name, owner, URL, access date, license, files used, record counts before and after cleaning, attribute dictionary and how to reproduce the cut. Include the source commit for repo-based data and the SHA-256 for downloaded files.
- `USO_DE_FERRAMENTAS.md`: libraries, external snippets and any use of generative AI tools (including Claude).
- Declared dependencies with versions, a config example without secrets, and a data download script or allowed sample when the dataset can't live in Git.
- Experiment scripts and tables (seeds, parameters, splits/instances), and saved models or fully reproducible training.
- A technical report of 5–8 pages, with references and each member's contributions.
