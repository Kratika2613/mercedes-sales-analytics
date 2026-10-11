-- Model-wise units sold and revenue
SELECT 
    model, 
    SUM(quantity) AS total_units_sold, 
    SUM(sale_price_inr) AS total_revenue,
    AVG(sale_price_inr) AS avg_selling_price
FROM fact_vehicle_sales
GROUP BY model
ORDER BY total_revenue DESC;

-- Monthly trends
SELECT 
    DATE_FORMAT(sale_date, '%Y-%m') AS month,
    SUM(quantity) AS units_sold,
    SUM(sale_price_inr) AS revenue
FROM fact_vehicle_sales
GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
ORDER BY month;

-- Fuel type comparison
SELECT 
    fuel_type, 
    SUM(quantity) AS units_sold,
    AVG(fuel_efficiency_mpg) AS avg_efficiency
FROM fact_vehicle_sales
GROUP BY fuel_type
ORDER BY units_sold DESC;

-- Transmission comparison
SELECT 
    transmission, 
    SUM(quantity) AS units_sold,
    SUM(sale_price_inr) AS revenue
FROM fact_vehicle_sales
GROUP BY transmission
ORDER BY units_sold DESC;

-- Regional analysis
SELECT 
    d.region, 
    SUM(f.quantity) AS units_sold, 
    SUM(f.sale_price_inr) AS revenue
FROM fact_vehicle_sales f
JOIN dim_dealer d ON f.dealer_id = d.dealer_id
GROUP BY d.region
ORDER BY revenue DESC;

-- Dealer performance
SELECT 
    d.dealer_name, 
    d.city,
    SUM(f.quantity) AS units_sold, 
    SUM(f.sale_price_inr) AS revenue
FROM fact_vehicle_sales f
JOIN dim_dealer d ON f.dealer_id = d.dealer_id
GROUP BY d.dealer_name, d.city
ORDER BY revenue DESC
LIMIT 10;
