import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Configuration
NUM_RECORDS = 3000
SEED = 42
OUTPUT_FILE = 'data/raw/mercedes_sales_raw.csv'

np.random.seed(SEED)
random.seed(SEED)

def generate_data(num_records):
    # Base data domains
    models_info = {
        'A-Class': {'class': 'Hatchback', 'engine': [1.3, 2.0], 'fuel': ['Petrol', 'Diesel'], 'base_price': 4000000},
        'C-Class': {'class': 'Sedan', 'engine': [1.5, 2.0], 'fuel': ['Petrol', 'Diesel'], 'base_price': 5500000},
        'E-Class': {'class': 'Sedan', 'engine': [2.0, 3.0], 'fuel': ['Petrol', 'Diesel'], 'base_price': 7500000},
        'S-Class': {'class': 'Luxury Sedan', 'engine': [3.0, 4.0], 'fuel': ['Petrol', 'Diesel'], 'base_price': 16000000},
        'GLA': {'class': 'Compact SUV', 'engine': [1.3, 2.0], 'fuel': ['Petrol', 'Diesel'], 'base_price': 4500000},
        'GLC': {'class': 'SUV', 'engine': [2.0], 'fuel': ['Petrol', 'Diesel'], 'base_price': 7000000},
        'GLE': {'class': 'Luxury SUV', 'engine': [3.0], 'fuel': ['Petrol', 'Diesel'], 'base_price': 9000000},
        'GLS': {'class': 'Luxury SUV', 'engine': [3.0, 4.0], 'fuel': ['Petrol', 'Diesel'], 'base_price': 13000000},
        'EQB': {'class': 'Electric SUV', 'engine': [0.0], 'fuel': ['Electric'], 'base_price': 7500000},
        'EQE': {'class': 'Electric Sedan', 'engine': [0.0], 'fuel': ['Electric'], 'base_price': 14000000},
        'EQS': {'class': 'Electric Sedan', 'engine': [0.0], 'fuel': ['Electric'], 'base_price': 16500000}
    }
    
    dealers = [
        {'id': 'D001', 'name': 'Mercedes-Benz Pune', 'city': 'Pune', 'state': 'Maharashtra', 'region': 'West'},
        {'id': 'D002', 'name': 'Mercedes-Benz Mumbai', 'city': 'Mumbai', 'state': 'Maharashtra', 'region': 'West'},
        {'id': 'D003', 'name': 'Mercedes-Benz Delhi', 'city': 'Delhi', 'state': 'Delhi', 'region': 'North'},
        {'id': 'D004', 'name': 'Mercedes-Benz Gurgaon', 'city': 'Gurgaon', 'state': 'Haryana', 'region': 'North'},
        {'id': 'D005', 'name': 'Mercedes-Benz Bangalore', 'city': 'Bangalore', 'state': 'Karnataka', 'region': 'South'},
        {'id': 'D006', 'name': 'Mercedes-Benz Chennai', 'city': 'Chennai', 'state': 'Tamil Nadu', 'region': 'South'},
        {'id': 'D007', 'name': 'Mercedes-Benz Kolkata', 'city': 'Kolkata', 'state': 'West Bengal', 'region': 'East'},
        {'id': 'D008', 'name': 'Mercedes-Benz Hyderabad', 'city': 'Hyderabad', 'state': 'Telangana', 'region': 'South'},
        {'id': 'D009', 'name': 'Mercedes-Benz Ahmedabad', 'city': 'Ahmedabad', 'state': 'Gujarat', 'region': 'West'},
        {'id': 'D010', 'name': 'Mercedes-Benz Bhopal', 'city': 'Bhopal', 'state': 'Madhya Pradesh', 'region': 'Central'}
    ]
    
    colors = ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red']
    transmissions = ['Automatic', 'AMG Speedshift']
    customer_types = ['Individual', 'Corporate']
    
    records = []
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    for i in range(1, num_records + 1):
        model = random.choice(list(models_info.keys()))
        info = models_info[model]
        
        # Determine sale date
        days_between = (end_date - start_date).days
        random_number_of_days = random.randrange(days_between)
        sale_date = start_date + timedelta(days=random_number_of_days)
        
        manuf_year = sale_date.year - random.choices([0, 1, 2], weights=[0.6, 0.3, 0.1])[0]
        mileage = random.randint(100, 50000) if manuf_year < sale_date.year else random.randint(10, 5000)
        
        engine = random.choice(info['engine'])
        fuel = random.choice(info['fuel'])
        
        base_p = info['base_price']
        listing_price = int(base_p * np.random.uniform(0.95, 1.10))
        discount_pct = round(np.random.uniform(0, 10), 2)
        sale_price = int(listing_price * (1 - (discount_pct / 100)))
        
        dealer = random.choice(dealers)
        
        eff = round(np.random.uniform(20, 45), 1) if fuel != 'Electric' else 95.0
        
        records.append({
            'sale_id': f"S{str(i).zfill(5)}",
            'sale_date': sale_date.strftime('%Y-%m-%d'),
            'customer_id': f"C{str(random.randint(1, 1000)).zfill(4)}",
            'customer_type': random.choice(customer_types),
            'model': model,
            'vehicle_class': info['class'],
            'engine_size_l': engine,
            'fuel_type': fuel,
            'fuel_efficiency_mpg': eff,
            'transmission': random.choice(transmissions),
            'color': random.choice(colors),
            'manufacturing_year': manuf_year,
            'mileage_km': mileage,
            'listing_price_inr': listing_price,
            'discount_percent': discount_pct,
            'sale_price_inr': sale_price,
            'quantity': 1,
            'dealer_id': dealer['id'],
            'dealer_name': dealer['name'],
            'city': dealer['city'],
            'state': dealer['state'],
            'region': dealer['region']
        })
        
    df = pd.DataFrame(records)
    
    # Introduce intentional data quality issues for a subset of records
    # 1. Missing values
    num_missing = int(num_records * 0.05)
    missing_indices = random.sample(range(num_records), num_missing)
    for idx in missing_indices:
        col = random.choice(['color', 'mileage_km', 'customer_type', 'discount_percent'])
        df.at[idx, col] = np.nan
        
    # 2. Duplicates (duplicate 2% of rows)
    num_dups = int(num_records * 0.02)
    dup_indices = random.sample(range(num_records), num_dups)
    dups = df.iloc[dup_indices].copy()
    df = pd.concat([df, dups], ignore_index=True)
    
    # 3. Invalid numeric values (negative prices/mileage for 1% of rows)
    num_invalid_num = int(num_records * 0.01)
    invalid_num_indices = random.sample(range(num_records), num_invalid_num)
    for idx in invalid_num_indices:
        if random.choice([True, False]):
            df.at[idx, 'sale_price_inr'] = -abs(df.at[idx, 'sale_price_inr'])
        else:
            df.at[idx, 'mileage_km'] = -abs(df.at[idx, 'mileage_km'])
            
    # 4. Inconsistent formatting (spaces, cases in fuel_type or region)
    num_format = int(num_records * 0.03)
    format_indices = random.sample(range(num_records), num_format)
    for idx in format_indices:
        col = random.choice(['fuel_type', 'region'])
        val = str(df.at[idx, col])
        if random.choice([True, False]):
            df.at[idx, col] = f" {val} "
        else:
            df.at[idx, col] = val.lower() if random.choice([True, False]) else val.upper()
            
    # 5. Invalid dates
    num_invalid_dates = int(num_records * 0.01)
    invalid_date_indices = random.sample(range(num_records), num_invalid_dates)
    for idx in invalid_date_indices:
        df.at[idx, 'sale_date'] = '9999-99-99'
        
    # Shuffle dataset
    df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Successfully generated {len(df)} synthetic records (including {num_dups} duplicates) and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_data(NUM_RECORDS)
