import pandas as pd
import numpy as np
import json
import os
import time
from datetime import datetime

# MySQL import (optional)
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

# Paths
RAW_DATA_PATH = 'data/raw/mercedes_sales_raw.csv'
CLEANED_DATA_PATH = 'data/processed/mercedes_sales_cleaned.csv'
DEMO_JSON_PATH = 'data/processed/mercedes_sales_demo.json'
QUALITY_REPORT_PATH = 'data/processed/data_quality_report.json'
ETL_SUMMARY_PATH = 'data/processed/etl_summary.json'

def setup_directories():
    os.makedirs(os.path.dirname(CLEANED_DATA_PATH), exist_ok=True)

def extract_data():
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Raw data file not found at {RAW_DATA_PATH}")
    return pd.read_csv(RAW_DATA_PATH)

def transform_data(df):
    quality_report = {
        'initial_rows': len(df),
        'missing_values_by_column': {},
        'duplicates_removed': 0,
        'invalid_dates': 0,
        'invalid_numerics': 0,
        'rejected_rows': 0,
        'rejection_reasons': []
    }
    
    # 1. Check missing values
    for col in df.columns:
        missing = int(df[col].isnull().sum())
        if missing > 0:
            quality_report['missing_values_by_column'][col] = missing
            
    # Handle missing values: drop rows with missing critical fields (e.g., sale_price, model)
    # Fill missing string categories with 'Unknown', numeric with median/mean
    initial_len = len(df)
    
    if 'color' in df.columns:
        df['color'] = df['color'].fillna('Unknown')
    if 'customer_type' in df.columns:
        df['customer_type'] = df['customer_type'].fillna('Unknown')
    if 'discount_percent' in df.columns:
        df['discount_percent'] = df['discount_percent'].fillna(0.0)
    if 'mileage_km' in df.columns:
        df['mileage_km'] = df['mileage_km'].fillna(df['mileage_km'].median())
        
    # 2. Detect and remove duplicates
    dups = df.duplicated()
    quality_report['duplicates_removed'] = int(dups.sum())
    df = df[~dups].copy()
    
    # 3. Standardize formats (e.g. string casing and stripping)
    for col in ['fuel_type', 'region', 'color', 'transmission']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
            
    # 4. Invalid dates
    # Assuming '9999-99-99' or unparseable
    df['sale_date_parsed'] = pd.to_datetime(df['sale_date'], errors='coerce')
    invalid_dates_mask = df['sale_date_parsed'].isnull()
    quality_report['invalid_dates'] = int(invalid_dates_mask.sum())
    
    # Drop rows with invalid dates as they are critical
    if quality_report['invalid_dates'] > 0:
        quality_report['rejection_reasons'].append(f"{quality_report['invalid_dates']} rows rejected due to invalid dates")
        df = df[~invalid_dates_mask].copy()
        
    df['sale_date'] = df['sale_date_parsed'].dt.strftime('%Y-%m-%d')
    df.drop(columns=['sale_date_parsed'], inplace=True)
    
    # 5. Invalid numerics (negative price or mileage)
    invalid_num_mask = (df['sale_price_inr'] < 0) | (df['mileage_km'] < 0)
    quality_report['invalid_numerics'] = int(invalid_num_mask.sum())
    if quality_report['invalid_numerics'] > 0:
        quality_report['rejection_reasons'].append(f"{quality_report['invalid_numerics']} rows rejected due to negative numerics")
        df = df[~invalid_num_mask].copy()
        
    # Calculate total rejected
    quality_report['final_rows'] = len(df)
    quality_report['rejected_rows'] = quality_report['initial_rows'] - quality_report['final_rows']
    
    return df, quality_report

def load_to_files(df, quality_report):
    df.to_csv(CLEANED_DATA_PATH, index=False)
    df.to_json(DEMO_JSON_PATH, orient='records', indent=2)
    
    with open(QUALITY_REPORT_PATH, 'w') as f:
        json.dump(quality_report, f, indent=4)

def load_to_mysql(df):
    host = os.environ.get('MYSQL_HOST', 'localhost')
    user = os.environ.get('MYSQL_USER', 'root')
    password = os.environ.get('MYSQL_PASSWORD', '')
    database = os.environ.get('MYSQL_DATABASE', 'mercedes_analytics')
    
    if not MYSQL_AVAILABLE:
        print("mysql-connector-python not installed. Skipping MySQL load.")
        return False
        
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        
        # Example: Simple create and insert. In a real scenario, use proper schema.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicle_sales (
                sale_id VARCHAR(50) PRIMARY KEY,
                sale_date DATE,
                customer_id VARCHAR(50),
                customer_type VARCHAR(50),
                model VARCHAR(100),
                vehicle_class VARCHAR(100),
                engine_size_l FLOAT,
                fuel_type VARCHAR(50),
                fuel_efficiency_mpg FLOAT,
                transmission VARCHAR(50),
                color VARCHAR(50),
                manufacturing_year INT,
                mileage_km FLOAT,
                listing_price_inr BIGINT,
                discount_percent FLOAT,
                sale_price_inr BIGINT,
                quantity INT,
                dealer_id VARCHAR(50),
                dealer_name VARCHAR(150),
                city VARCHAR(100),
                state VARCHAR(100),
                region VARCHAR(50)
            )
        """)
        
        # Clear existing data for idempotent load (or use UPSERT depending on DB support)
        cursor.execute("TRUNCATE TABLE vehicle_sales")
        
        cols = df.columns.tolist()
        placeholders = ', '.join(['%s'] * len(cols))
        sql = f"INSERT INTO vehicle_sales ({', '.join(cols)}) VALUES ({placeholders})"
        
        # Convert df to list of tuples, handling numpy types for MySQL
        data = [tuple(x) if pd.notnull(x).all() else tuple([None if pd.isnull(v) else v for v in x]) for x in df.values]
        
        cursor.executemany(sql, data)
        conn.commit()
        
        cursor.close()
        conn.close()
        print(f"Successfully loaded {len(df)} rows into MySQL.")
        return True
    except mysql.connector.Error as err:
        print(f"MySQL connection or execution failed: {err}")
        return False

def main():
    start_time = time.time()
    
    setup_directories()
    
    try:
        df = extract_data()
        print(f"Extracted {len(df)} rows from raw data.")
        
        df_clean, quality_report = transform_data(df)
        print("Data transformed successfully.")
        
        load_to_files(df_clean, quality_report)
        print("Cleaned data and quality report saved to files.")
        
        mysql_status = load_to_mysql(df_clean)
        
        end_time = time.time()
        
        etl_summary = {
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': round(end_time - start_time, 2),
            'status': 'SUCCESS',
            'records_processed': quality_report['initial_rows'],
            'records_loaded': quality_report['final_rows'],
            'mysql_load_successful': mysql_status
        }
        
        with open(ETL_SUMMARY_PATH, 'w') as f:
            json.dump(etl_summary, f, indent=4)
            
        print("ETL pipeline completed successfully.")
        
    except Exception as e:
        end_time = time.time()
        etl_summary = {
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': round(end_time - start_time, 2),
            'status': 'FAILED',
            'error': str(e)
        }
        with open(ETL_SUMMARY_PATH, 'w') as f:
            json.dump(etl_summary, f, indent=4)
        print(f"ETL pipeline failed: {e}")

if __name__ == "__main__":
    main()
