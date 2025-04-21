# Ecosystem Health Index (EHI)

The Ecosystem Health Index is a methodology developed by the Tech Ecosystem Institute to score the overall health and maturity of a tech ecosystem. This repository is the official open-source implementation.

## 🧠 EHI Dimensions
- Trust & Reliability
- Community Engagement
- Integration & Partnerships
- Product Momentum
- Developer Experience

## 📂 Repo Structure
- `ehi/` – Core scoring logic and config
- `scripts/` – Run EHI reports
- `data/` – Input CSVs (e.g., company data)
- `results/` – Output files
- `notebooks/` – Exploratory analysis
- `docs/` – Methodology explanation
- `tests/` – Unit tests

## 🧪 Quickstart
```bash
pip install -r requirements.txt
python scripts/run_ehi_report.py --input data/example_companies.csv
