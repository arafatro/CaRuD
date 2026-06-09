# Causal Rule Discovery for Compliance Improvement in Procurement Logs: A Case Study

This repository contains the implementation of the paper "Causal Rule Discovery for Compliance Improvement in Procurement Logs: A Case Study." It uses the BPI Challenge 2019 Purchase-to-Pay event log and combines action rule mining with uplift modelling to discover causal process changes that improve invoice clearance compliance.

Repository URL: https://github.com/arafatro/CaRuD

## What is included

- `src/convert_xes_to_csv.py` - convert the raw XES event log to CSV.
- `src/data_prep_chunked.py` - preprocess the CSV log into case-level features and outcome labels.
- `src/action_rules.py` - mine candidate action rules from stable and flexible attributes.
- `src/uplift_tree.py` - fit uplift models and validate candidate causal rules.
- `src/causal_rules.py` - additional causal rule evaluation utilities.
- `src/log_processing.py` - log filtering, feature engineering, and dataset construction.
- `requirements.txt` - Python dependencies needed to run the experiments.
- `data/` - the BPI Challenge 2019 dataset files used in this study.

## Paper summary

The paper addresses the gap between diagnostic process mining and prescriptive compliance improvement. It applies causal rule discovery to a large procurement log to identify interventions that increase the probability of invoice clearance. The main contributions are:

- Mining actionable rule candidates from procurement process attributes.
- Validating and ranking those candidates using uplift modelling.
- Generating causally-driven recommendations for the Purchase-to-Pay process.
- Demonstrating the approach on the BPI Challenge 2019 dataset.

## Reproducibility guide

Follow these steps to reproduce the experiments in this repository.

### 1. Install dependencies

```powershell
pip install -r requirements.txt
```

### 2. Prepare the data

If you have the original XES log, convert it with:

```powershell
python src/convert_xes_to_csv.py --input data/BPI_Challenge_2019.xes --output data/BPI_Challenge_2019.csv
```

Then preprocess the dataset:

```powershell
python src/data_prep_chunked.py --input data/BPI_Challenge_2019.csv --output data/processed_data.csv
```

This step produces case-level features, labels the clearance outcome, and prepares the input for causal rule mining.

### 3. Mine action rule candidates

```powershell
python src/action_rules.py --input data/processed_data.csv --output data/action_rules.csv
```

This script discovers candidate actions over stable and flexible attributes.

### 4. Estimate causal uplift

```powershell
python src/uplift_tree.py --input data/processed_data.csv --rules data/action_rules.csv --output data/uplift_results.csv
```

This step fits uplift models, validates candidate rules, and generates causal effect estimates.

### 5. Inspect results

Review the generated output files and any saved plots. The key outputs include:

- `data/action_rules.csv` - mined action rule candidates.
- `data/uplift_results.csv` - validated causal rules with uplift estimates.
- `data/processed_data.csv` - preprocessed feature dataset.

## Recommended workflow

1. Convert and preprocess the BPI 2019 log.
2. Mine candidate action rules.
3. Fit uplift models and validate causal rules.
4. Compare causal rules against correlation-based baselines.
5. Use the output rules to guide compliance improvement in procurement.

## Notes

- Large files in `data/` are managed with Git LFS.
- The repository focuses on reproducibility: all code and scripts required to reproduce the paper analysis are included.
- If you encounter memory issues, run the preprocessing script on smaller chunks or increase available RAM.

## Contact

For questions or issues, reach out to the repository owner at the GitHub URL above.
