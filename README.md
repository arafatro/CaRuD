# CaRuD

Reproducible code for the paper "Causal Rule Discovery for Compliance Improvement in Procurement Logs: A Case Study" accepted to IntRob'26.

## Repository

- GitHub: https://github.com/arafatro/CaRuD
- Paper: IntRob'26 (Intelligent Robotics FAIR 2026)
- Focus: reproducibility of causal rule discovery experiments on the BPI Challenge 2019 Purchase-to-Pay log

## Getting Started

### Prerequisites

- Python 3.8 or newer
- `pip`
- Git with Git LFS enabled for large data files

### Install dependencies

```bash
pip install -r requirements.txt
```

## Reproducibility workflow

### 1. Convert the raw event log

If you have the raw XES file, convert it to CSV first:

```bash
python src/convert_xes_to_csv.py --input data/BPI_Challenge_2019.xes --output data/BPI_Challenge_2019.csv
```

If you already have `data/BPI_Challenge_2019.csv`, skip this step.

### 2. Preprocess the dataset

```bash
python src/data_prep_chunked.py --input data/BPI_Challenge_2019.csv --output data/processed_data.csv
```

This generates the case-level dataset used for action rule mining and uplift modelling.

### 3. Mine action rules

```bash
python src/action_rules.py --input data/processed_data.csv --output data/action_rules.csv
```

### 4. Estimate causal uplift

```bash
python src/uplift_tree.py --input data/processed_data.csv --rules data/action_rules.csv --output data/uplift_results.csv
```

### 5. Review results

Check the produced files:

- `data/processed_data.csv`
- `data/action_rules.csv`
- `data/uplift_results.csv`

## Repository structure

- `src/` — code for conversion, preprocessing, rule mining, uplift modelling, and log processing
- `data/` — dataset files used in the experiments
- `requirements.txt` — Python dependencies
- `README.md` — reproduction instructions and citation

## Citation

```bibtex
@incollection{arafat2026causal,
  title={Causal Rule Discovery for Compliance Improvement in Procurement Logs: A Case Study},
  author={Arafat, Md Easin and Shengjie, Fan and Koren, Istv{\'a}n and Orosz, Tam{\'a}s},
  booktitle={Proceedings of the Intelligent Robotics FAIR 2026},
  pages={125--131},
  year={2026}
}
```

## Conference

- IntRob’26: Intelligent Robotics FAIR 2026
- June 18–20, 2026
- Budapest, Hungary
