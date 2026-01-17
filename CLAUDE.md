# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a personal repository for prediction tracking and scoring. It contains Jupyter notebooks for analyzing forecasting accuracy and CSV data files with predictions and their resolutions.

## Structure

- `notebooks/` - Jupyter notebooks for prediction analysis and scoring
- `data/` - CSV files containing predictions, resolutions, and external data sources
- `figures/` - Generated plots (gitignored)

## Running Notebooks

Notebooks use standard Python data science libraries (pandas, numpy, scipy, matplotlib, seaborn, sklearn). No special environment setup is documented; any standard scientific Python environment should work.

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
