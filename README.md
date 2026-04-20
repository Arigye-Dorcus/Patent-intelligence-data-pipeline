# Global Patent Intelligence Data Pipeline

A data pipeline that collects, cleans, stores, and analyzes real-world patent data from the USPTO PatentsView dataset.

## Project Structure

```
patent-pipeline/
├── data/
│   ├── raw/          # Downloaded USPTO files (not committed to git)
│   └── clean/        # Cleaned CSV outputs
├── scripts/
│   ├── download_data.py   # Phase 2: Download raw data
│   ├── clean_data.py      # Phase 3: Clean with pandas
│   ├── load_db.py         # Phase 4: Load into SQLite
│   ├── queries.sql        # Phase 4: All SQL queries (Q1–Q7)
│   └── report.py          # Phase 5: Generate reports
├── database/
│   └── schema.sql         # Table definitions
├── reports/               # Generated output files
├── requirements.txt
└── README.md
```

## How to Run (Reproducible Steps)

### 1. Clone the repo and install dependencies
```bash
git clone <your-repo-url>
cd patent-pipeline
pip install -r requirements.txt
```

### 2. Download the data
```bash
python scripts/download_data.py
```

### 3. Clean the data
```bash
python scripts/clean_data.py
```

### 4. Load into database
```bash
python scripts/load_db.py
```

### 5. Generate reports
```bash
python scripts/report.py
```

## Data Source

PatentsView Granted Patent Disambiguated Data  
https://data.uspto.gov/bulkdata/datasets/pvgpatdis

## Outputs

- `data/clean/clean_patents.csv`
- `data/clean/clean_inventors.csv`
- `data/clean/clean_companies.csv`
- `reports/top_inventors.csv`
- `reports/top_companies.csv`
- `reports/country_trends.csv`
- `reports/report.json`
