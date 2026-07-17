# Project Architecture

## Overview
This project follows a Medallion Architecture using Bronze, Silver, and Gold data layers.
The purpose of this architecture is to process raw Mercedes-Benz sales data step by step and prepare clean, structured data for analysis and reporting.

## Data Flow
Raw CSV Data  
↓  
Databricks  
↓  
Bronze Layer  
↓  
Silver Layer  
↓  
Gold Layer  
↓  
SQL Analysis  
↓  
Power BI Dashboard

## Architecture Layers

### 1. Raw Data
The original Mercedes-Benz sales CSV file is used as the source data.

### 2. Bronze Layer
The raw data is loaded into Databricks without major transformation.
This layer keeps the original data for traceability.

### 3. Silver Layer
The Bronze data is cleaned and transformed.
Main activities include:
- Handling missing values
- Removing duplicate records
- Correcting data types
- Standardizing column names
- Creating calculated columns

### 4. Gold Layer
The Silver data is converted into business-ready tables.
The Gold layer contains:
- Fact Sales table
- Customer dimension
- Dealer dimension
- Model dimension
- Date dimension

### 5. SQL Analysis
SQL queries are used to calculate KPIs and validate the Gold tables.
Examples:
- Total sales
- Total quantity sold
- Customer count
- Dealer count
- Sales by region
- Sales by manufacturing year

### 6. Power BI
Power BI connects to the Gold tables and creates interactive dashboards.
The report contains:
- Sales Performance Dashboard
- Technical Comparison
- Geographic Analysis

## Architecture Summary
The architecture provides a clear flow from raw data to business insights.
It improves data quality, makes the pipeline easier to understand, and supports reliable reporting.