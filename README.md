# Causal Rule Discovery for Compliance Improvement in Procurement Logs: A Case Study

This repository is intended for reproducibility only. It provides the code and data processing steps needed to reproduce the experiments for the submitted paper.

## Reproducibility instructions

### 1. Install dependencies

```powershell
pip install -r requirements.txt
```

### 2. Convert the event log (if needed)

If you have the raw XES file, convert it to CSV:

```powershell
python src/convert_xes_to_csv.py --input data/BPI_Challenge_2019.xes --output data/BPI_Challenge_2019.csv
```

### 3. Preprocess the data

```powershell
python src/data_prep_chunked.py --input data/BPI_Challenge_2019.csv --output data/processed_data.csv
```

This produces the case-level dataset and labels used for causal rule discovery.

### 4. Mine candidate action rules

```powershell
python src/action_rules.py --input data/processed_data.csv --output data/action_rules.csv
```

### 5. Estimate causal uplift

```powershell
python src/uplift_tree.py --input data/processed_data.csv --rules data/action_rules.csv --output data/uplift_results.csv
```

### 6. Check outputs

The main output files are:

- `data/processed_data.csv`
- `data/action_rules.csv`
- `data/uplift_results.csv`

## Files used for reproduction

- `src/convert_xes_to_csv.py`
- `src/data_prep_chunked.py`
- `src/action_rules.py`
- `src/uplift_tree.py`
- `data/` (BPI 2019 input files)
- `requirements.txt`

## Publication note

This code supports the reproducibility of the experiment submitted to IntRob'26.

Reference:

Md Easin Arafat, Shengjie Fan, István Koren, and Tamás Orosz. 2026. Causal Rule Discovery for Compliance Improvement in Procurement Logs: A Case Study. In Proceedings of Intelligent Robotics FAIR 2026 (IntRob’26). ACM, Budapest, Hungary, 7 pages.

IntRob’26, June 18–20, 2026, Budapest, Hungary
