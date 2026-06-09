# Causal Rule Discovery for Compliance Improvement in Procurement Logs: A Case Study

This repository contains the implementation and data preparation scripts for the paper "Causal Rule Discovery for Compliance Improvement in Procurement Logs: A Case Study." It includes the source code, preprocessing steps, and analysis used to reproduce the results presented in the paper.

## Paper Context

- Title: Causal Rule Discovery for Compliance Improvement in Procurement Logs: A Case Study
- Purpose: Discover causal rules from procurement log data and use them to improve compliance processes.
- Contents: data preprocessing, causal rule discovery, uplift analysis, and activity distribution analysis.

## Reproducibility

To reproduce the experiments in this repository:

1. Install dependencies from `requirements.txt`.
2. Prepare the data by running the preprocessing scripts in `src/`.
3. Execute the main analysis scripts in the order described in the paper.
4. Use the provided `data/` files as the input dataset.

## Files and Structure

- `src/` - Python scripts for causal rule discovery, data preprocessing, log processing, and analysis.
- `data/` - Procurement log datasets used in the case study.
- `requirements.txt` - Python dependency list.

## Notes

- Large data files are managed with Git LFS.
- This repository is intended to support reproducible research and analysis based on the paper.
