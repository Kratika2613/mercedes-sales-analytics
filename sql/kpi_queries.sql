-- Mercedes-Benz Sales Analytics
-- Business KPI Queries


-- 1. Total Sales Revenue
SELECT
   SUM(sale_price_inr) AS total_sales_revenue
FROM gold_fact_sales;

-- 2. Total Quantity Sold
SELECT
   SUM(quantity) AS total_quantity_sold
FROM gold_fact_sales;

-- 3. Total Customers
SELECT
   COUNT(DISTINCT customer_id) AS total_customers
FROM gold_fact_sales;

-- 4. Total Dealers
SELECT
   COUNT(DISTINCT dealer_id) AS total_dealers
FROM gold_fact_sales;

-- 5. Total Vehicle Models
SELECT
   COUNT(DISTINCT model_id) AS total_models
FROM gold_fact_sales;

-- 6. Total Sales Transactions
SELECT
   COUNT(DISTINCT sale_id) AS total_sales_transactions
FROM gold_fact_sales;

-- 7. Average Sale Price
SELECT
   ROUND(AVG(sale_price_inr), 2) AS average_sale_price
FROM gold_fact_sales;

-- 8. Average Discount Percentage
SELECT
   ROUND(AVG(discount_percent), 2) AS average_discount_percent
FROM gold_fact_sales;

-- 9. Sales by Transmission Type
SELECT
   transmission,
   SUM(sale_price_inr) AS total_sales
FROM gold_fact_sales
GROUP BY transmission
ORDER BY total_sales DESC;

-- 10. Sales by Manufacturing Year
SELECT
   manufacturing_year,
   SUM(sale_price_inr) AS total_sales
FROM gold_fact_sales
GROUP BY manufacturing_year
ORDER BY manufacturing_year;

-- 11. Model-wise Sales and Quantity
SELECT
   m.model,
   SUM(f.sale_price_inr) AS total_sales,
   SUM(f.quantity) AS total_quantity_sold
FROM gold_fact_sales f
JOIN gold_dim_model m
   ON f.model_id = m.model_id
GROUP BY m.model
ORDER BY total_sales DESC;

-- 12. Sales by Fuel Type
SELECT
   m.fuel_type,
   SUM(f.sale_price_inr) AS total_sales
FROM gold_fact_sales f
JOIN gold_dim_model m
   ON f.model_id = m.model_id
GROUP BY m.fuel_type
ORDER BY total_sales DESC;

-- 13. Sales by Vehicle Class
SELECT
   m.vehicle_class,
   SUM(f.sale_price_inr) AS total_sales
FROM gold_fact_sales f
JOIN gold_dim_model m
   ON f.model_id = m.model_id
GROUP BY m.vehicle_class
ORDER BY total_sales DESC;

-- 14. Average Engine Size by Model
SELECT
   model,
   ROUND(AVG(engine_size_l), 2) AS average_engine_size_l
FROM gold_dim_model
GROUP BY model
ORDER BY average_engine_size_l DESC;

-- 15. Average Fuel Efficiency by Model
SELECT
   model,
   ROUND(AVG(fuel_efficiency_mpg), 2) AS average_fuel_efficiency_mpg
FROM gold_dim_model
GROUP BY model
ORDER BY average_fuel_efficiency_mpg DESC;

-- 16. Sales by Region
SELECT
   d.region,
   SUM(f.sale_price_inr) AS total_sales
FROM gold_fact_sales f
JOIN gold_dim_dealer d
   ON f.dealer_id = d.dealer_id
GROUP BY d.region
ORDER BY total_sales DESC;

-- 17. Sales by State
SELECT
   d.state,
   SUM(f.sale_price_inr) AS total_sales
FROM gold_fact_sales f
JOIN gold_dim_dealer d
   ON f.dealer_id = d.dealer_id
GROUP BY d.state
ORDER BY total_sales DESC;

-- 18. Dealer-wise Sales
SELECT
   d.dealer_name,
   d.city,
   d.state,
   SUM(f.sale_price_inr) AS total_sales
FROM gold_fact_sales f
JOIN gold_dim_dealer d
   ON f.dealer_id = d.dealer_id
GROUP BY
   d.dealer_name,
   d.city,
   d.state
ORDER BY total_sales DESC;

-- 19. Monthly Sales Trend
SELECT
   dt.year,
   dt.month_number,
   dt.month_name,
   SUM(f.sale_price_inr) AS total_sales
FROM gold_fact_sales f
JOIN gold_dim_date dt
   ON f.date_id = dt.date_id
GROUP BY
   dt.year,
   dt.month_number,
   dt.month_name
ORDER BY
   dt.year,
   dt.month_number;

-- 20. Quarterly Sales Trend
SELECT
   dt.year,
   dt.quarter,
   SUM(f.sale_price_inr) AS total_sales
FROM gold_fact_sales f
JOIN gold_dim_date dt
   ON f.date_id = dt.date_id
GROUP BY
   dt.year,
   dt.quarter
ORDER BY
   dt.year,
   dt.quarter;

-- 21. Sales by Customer Type
SELECT
   c.customer_type,
   SUM(f.sale_price_inr) AS total_sales,
   COUNT(DISTINCT f.customer_id) AS total_customers
FROM gold_fact_sales f
JOIN gold_dim_customer c
   ON f.customer_id = c.customer_id
GROUP BY c.customer_type
ORDER BY total_sales DESC;

-- 22. Average Mileage by Model
SELECT
   m.model,
   ROUND(AVG(f.mileage_km), 2) AS average_mileage_km
FROM gold_fact_sales f
JOIN gold_dim_model m
   ON f.model_id = m.model_id
GROUP BY m.model
ORDER BY average_mileage_km;

-- 23. Average Listing Price and Sale Price
SELECT
   m.model,
   ROUND(AVG(f.listing_price_inr), 2) AS average_listing_price,
   ROUND(AVG(f.sale_price_inr), 2) AS average_sale_price
FROM gold_fact_sales f
JOIN gold_dim_model m
   ON f.model_id = m.model_id
GROUP BY m.model
ORDER BY average_sale_price DESC;

-- 24. Fact Table Row Count Validation
SELECT
   COUNT(*) AS fact_table_row_count
FROM gold_fact_sales;

-- 25. Duplicate Sale ID Validation
SELECT
   sale_id,
   COUNT(*) AS duplicate_count
FROM gold_fact_sales
GROUP BY sale_id
HAVING COUNT(*) > 1;

-- 26. NULL Value Validation
SELECT
   SUM(CASE WHEN sale_id IS NULL THEN 1 ELSE 0 END) AS null_sale_ids,
   SUM(CASE WHEN date_id IS NULL THEN 1 ELSE 0 END) AS null_date_ids,
   SUM(CASE WHEN model_id IS NULL THEN 1 ELSE 0 END) AS null_model_ids,
   SUM(CASE WHEN dealer_id IS NULL THEN 1 ELSE 0 END) AS null_dealer_ids,
   SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_ids,
   SUM(CASE WHEN sale_price_inr IS NULL THEN 1 ELSE 0 END) AS null_sale_prices
FROM gold_fact_sales;