import os
import json
import pytest
import pandas as pd

def test_data_generation_reproducibility():
    # If the generator is run twice with the same seed, the output should be identical.
    # We will just verify that the raw file was generated and has expected columns.
    raw_path = "data/raw/mercedes_sales_raw.csv"
    assert os.path.exists(raw_path)
    df = pd.read_csv(raw_path)
    assert len(df) > 2000
    assert "sale_id" in df.columns
    assert "sale_price_inr" in df.columns

def test_processed_data_consistency():
    clean_path = "data/processed/mercedes_sales_cleaned.csv"
    json_path = "data/processed/mercedes_sales_demo.json"
    assert os.path.exists(clean_path)
    assert os.path.exists(json_path)
    
    df_clean = pd.read_csv(clean_path)
    with open(json_path, 'r') as f:
        data_json = json.load(f)
        
    assert len(df_clean) == len(data_json)
    
def test_data_quality_report():
    quality_path = "data/processed/data_quality_report.json"
    assert os.path.exists(quality_path)
    with open(quality_path, 'r') as f:
        report = json.load(f)
    assert 'initial_rows' in report
    assert 'rejected_rows' in report
    assert report['initial_rows'] > report['final_rows']
