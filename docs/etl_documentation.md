# ETL Documentation

## ETL Process Overview
This project follows the ETL (Extract, Transform, Load) approach to prepare Mercedes-Benz sales data for analytics.
---

## Extract
- Source: Mercedes-Benz Sales CSV Dataset
- Data is loaded into Databricks.
---

## Transform
The following transformations are performed:
- Removed duplicate records
- Handled missing values
- Corrected data types
- Standardized column names
- Created business-ready tables
- Validated data quality
---

## Load
The transformed data is loaded into the following Gold tables:
- gold_fact_sales
- gold_dim_model
- gold_dim_dealer
- gold_dim_customer
- gold_dim_date
These business-ready tables are used for:
- SQL analysis
- KPI calculations
- Power BI dashboard development
---

## Output
The final output includes:
- Sales Performance Dashboard
- Technical Comparison Dashboard
- Geographic Analysis Dashboard