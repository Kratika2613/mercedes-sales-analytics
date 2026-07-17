-- Databricks notebook source
SELECT *
FROM workspace.default.gold_fact_sales
LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Total Revenue**

-- COMMAND ----------

SELECT
    SUM(sale_price_inr) AS total_revenue
FROM workspace.default.gold_fact_sales;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Total Vehicles Sold**

-- COMMAND ----------

SELECT
    SUM(sale_price_inr) AS total_veh

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Average Selling Price**

-- COMMAND ----------

SELECT
    ROUND(AVG(sale_price_inr), 2) AS average_selling_price
FROM workspace.default.gold_fact_sales;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Top Selling Models**

-- COMMAND ----------

SELECT
   m.model,
   SUM(f.quantity) AS vehicles_sold
FROM workspace.default.gold_fact_sales f
JOIN workspace.default.gold_dim_model m
   ON f.model_id = m.model_id
GROUP BY m.model
ORDER BY vehicles_sold DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Region-wise Revenue**

-- COMMAND ----------

SELECT
   d.region,
   SUM(f.sale_price_inr) AS total_revenue
FROM workspace.default.gold_fact_sales f
JOIN workspace.default.gold_dim_dealer d
   ON f.dealer_id = d.dealer_id
GROUP BY d.region
ORDER BY total_revenue DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Dealer-wise Revenue**

-- COMMAND ----------

SELECT
   d.dealer_name,
   d.city,
   SUM(f.sale_price_inr) AS total_revenue
FROM workspace.default.gold_fact_sales f
JOIN workspace.default.gold_dim_dealer d
   ON f.dealer_id = d.dealer_id
GROUP BY d.dealer_name, d.city
ORDER BY total_revenue DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Monthly Sales Trend**

-- COMMAND ----------

SELECT
   dt.year,
   dt.month_number,
   dt.month_name,
   SUM(f.sale_price_inr) AS monthly_revenue
FROM workspace.default.gold_fact_sales f
JOIN workspace.default.gold_dim_date dt
   ON f.date_id = dt.date_id
GROUP BY
   dt.year,
   dt.month_number,
   dt.month_name
ORDER BY
   dt.year,
   dt.month_number;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Average Price by Model**

-- COMMAND ----------

SELECT
   m.model,
   ROUND(AVG(f.sale_price_inr), 2) AS average_sale_price
FROM workspace.default.gold_fact_sales f
JOIN workspace.default.gold_dim_model m
   ON f.model_id = m.model_id
GROUP BY m.model
ORDER BY average_sale_price DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Mileage vs Price data**

-- COMMAND ----------

SELECT
   m.model,
   f.mileage_km,
   f.listing_price_inr,
   f.sale_price_inr
FROM workspace.default.gold_fact_sales f
JOIN workspace.default.gold_dim_model m
   ON f.model_id = m.model_id
ORDER BY f.mileage_km;

-- COMMAND ----------

DESCRIBE gold_dim_customer;