# Mercedes-Benz Sales Performance Analytics (Enterprise Edition)

## Project Overview
This project is an end-to-end Enterprise Data Engineering and BI solution analyzing Mercedes-Benz vehicle sales. It demonstrates the complete lifecycle of data from extraction and validation to transformation, database loading, and interactive visualization.

> **Note on Data:** This project uses a reproducibly generated **synthetic automotive dataset** simulating realistic transaction patterns. It does *not* contain actual or confidential Mercedes-Benz sales data.

## Key Features
- **Synthetic Data Generation**: Reproducible Python script to generate 3000+ realistic transaction records with controlled data-quality issues for robust pipeline testing.
- **Python Data Pipeline (ETL)**: A local Pandas-based ETL pipeline that validates schemas, normalizes formats, handles missing values, and drops duplicates while generating an extensive JSON quality report.
- **Data Modeling & MySQL**: Star schema modeling with fact and dimension tables, structured via parameterized Python queries for safe and idempotent loads.
- **Interactive Enterprise React Dashboard**: A responsive Vite-powered React dashboard displaying sales performance, model analytics, technical comparisons, and real-time ETL pipeline monitoring, designed with modern dark-navy aesthetics.
- **Static GitHub Pages Demo**: A recruiter-accessible, serverless static deployment of the React dashboard utilizing the processed demo JSON dataset.
- **Automated Testing**: CI/CD-ready pytest suite verifying reproducibility, pipeline integrity, and data schema conformity.
- **Optional FastAPI Backend**: A modular Python FastAPI layer providing analytical endpoints.

## Live Demo
Check out the static Recruiter Demo on GitHub Pages:
[Live Demo Link (Update after GitHub Pages setup)](https://Kratika2613.github.io/mercedes-sales-analytics/)

## Technology Stack
- **Data Engineering**: Python, Pandas, NumPy
- **Database / SQL**: MySQL, Parameterized Queries, ANSI SQL Analytics
- **Web Frontend**: React, Vite, Recharts, Lucide React, Custom Vanilla CSS
- **Backend**: FastAPI
- **BI / Visualization**: Power BI
- **DevOps**: GitHub Actions, Pytest

## Setup Instructions

### 1. Data Generation and ETL Pipeline
```bash
# Generate raw synthetic data (creates data/raw/mercedes_sales_raw.csv)
python python/generate_synthetic_data.py

# Run the ETL pipeline (cleans data, generates JSON reports, creates demo JSON)
python python/run_pipeline.py
```

### 2. Viewing the Local React Dashboard
```bash
cd dashboard
npm install
npm run dev
# The application will run locally on http://localhost:5173
```

### 3. Running the FastAPI Backend
```bash
uvicorn python.api:app --reload
```

### 4. Running the Tests
```bash
pytest tests/
```

## Project Architecture
1. **Raw Data**: Synthetically generated into `data/raw/`
2. **ETL Pipeline**: Transforms raw CSV, validates records, handles missing/duplicate/invalid data.
3. **Processed Data**: Cleaned data saved to `data/processed/mercedes_sales_cleaned.csv` and `data/processed/mercedes_sales_demo.json`
4. **Data Quality Reports**: Saved alongside processed data.
5. **Database**: Optional MySQL upload mapped into Star Schema definitions in `sql/schema.sql`.
6. **Frontend**: Vite/React application fetching `data.json` for static visualization or via FastAPI.

## Dashboards
- **React Web App**: See `dashboard/` directory. Contains sections for Executive Overview, Model Performance, Technical Analytics, Regional Analysis, and Data Quality Monitoring.
- **Power BI**: The repository includes `powerbi/Mercedes_Sales_Dashboard.pbix` (using legacy data, can be refreshed with the new cleaned CSV).

## Known Limitations
- The MySQL integration requires a running local instance. If unavailable, the ETL script skips DB upload but successfully outputs processed files for the static React demo.
- ServiceNow integration is modularly omitted until environment credentials are provided.

---
**Disclaimer**: Synthetic Demonstration Data. All figures, customer details, and transactions are generated purely for technical portfolio demonstration.