-- Mercedes-Benz Sales Analytics MySQL Schema

CREATE DATABASE IF NOT EXISTS mercedes_analytics;
USE mercedes_analytics;

-- Dimension: Dealer
CREATE TABLE IF NOT EXISTS dim_dealer (
    dealer_id VARCHAR(50) PRIMARY KEY,
    dealer_name VARCHAR(150),
    city VARCHAR(100),
    state VARCHAR(100),
    region VARCHAR(50)
);

-- Dimension: Date (Can be populated dynamically or assumed part of star schema)
CREATE TABLE IF NOT EXISTS dim_date (
    date_id DATE PRIMARY KEY,
    year INT,
    quarter INT,
    month INT,
    day INT,
    month_name VARCHAR(20)
);

-- Fact: Vehicle Sales
CREATE TABLE IF NOT EXISTS fact_vehicle_sales (
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
    FOREIGN KEY (dealer_id) REFERENCES dim_dealer(dealer_id)
);
