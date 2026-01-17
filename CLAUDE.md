# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a personal repository for prediction tracking and scoring. It contains Jupyter notebooks for analyzing forecasting accuracy and CSV data files with predictions and their resolutions.

## Structure

- `notebooks/` - Jupyter notebooks for prediction analysis and scoring
- `data/` - CSV files containing predictions, resolutions, and external data sources
  - Subdirectories (e.g., `data/2026_predictions/`) contain related data and generated plots
- `scripts/` - Python analysis scripts organized by project (e.g., `scripts/2026_predictions/`)
- `notes/` - Markdown writeups for predictions and analysis
- `figures/` - Generated plots (gitignored, but plots are often saved alongside data instead)

## Running Code

Use `uv` to run Python scripts:
```bash
uv run python scripts/<script_name>.py
```

Notebooks use standard Python data science libraries (pandas, numpy, scipy, matplotlib, seaborn, sklearn).

To run a notebook:
```bash
jupyter notebook notebooks/<notebook_name>.ipynb
```

## Key Concepts

**Scoring functions** (defined in `notebooks/2021 Predictions Scoring.ipynb`):
- Brier score: `mean((credence - resolution)^2)` - lower is better
- Log score: `mean(-resolution*log(credence) - (1-resolution)*log(1-credence))` - lower is better

**Data format** for prediction CSVs:
- `Prediction`: Text description
- `Credence`: Probability as percentage string (e.g., "60%") or decimal
- `Category`: Topic category (Science, Tech, Politics, COVID, etc.)
- `Resolution`: Boolean outcome (True/False) or NaN if unresolved
- `Source`: Optional URL for resolution evidence

## 2026 Predictions Project

The `notes/2026_predictions/`, `scripts/2026_predictions/`, and `data/2026_predictions/` directories contain work for the forecast2026.ai survey. See `notes/2026_predictions/00_plan.md` for methodology and structure details.
