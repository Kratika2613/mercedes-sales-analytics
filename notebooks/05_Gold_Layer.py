# Databricks notebook source
# MAGIC %md
# MAGIC **Mercedes-Benz Sales Analytics - Gold Layer**

# COMMAND ----------

from pyspark.sql.functions import (
    col,
    date_format,
    dayofmonth,
    month,
    quarter,
    year,
    first,
    current_timestamp,
    lit
)

from pyspark.sql.window import Window
from pyspark.sql.functions import dense_rank

# COMMAND ----------

silver_df = spark.table(
    "workspace.default.silver_mercedes_sales"
)

print("Silver rows:", silver_df.count())
print("Silver columns:", len(silver_df.columns))

# COMMAND ----------

model_window = Window.orderBy("model")

# COMMAND ----------

gold_dim_model = (
   silver_df
   .select(
       "model",
       "vehicle_class",
       "engine_size_l",
       "fuel_type",
       "fuel_efficiency_mpg"
   )
   .dropDuplicates(["model"])
   .withColumn(
       "model_id",
       dense_rank().over(model_window)
   )
   .select(
       "model_id",
       "model",
       "vehicle_class",
       "engine_size_l",
       "fuel_type",
       "fuel_efficiency_mpg"
   )
)

# COMMAND ----------

gold_dim_model.orderBy("model_id").show(truncate=False)

# COMMAND ----------

print("Model dimension rows:", gold_dim_model.count())

# COMMAND ----------

gold_dim_dealer = (
    silver_df
    .select(
        "dealer_id",
        "dealer_name",
        "city",
        "state",
        "region"
    )
    .dropDuplicates(["dealer_id"])
)

gold_dim_dealer.orderBy("dealer_id").show(truncate=False)
print("Dealer dimension rows:", gold_dim_dealer.count())

# COMMAND ----------

gold_dim_customer = (
    silver_df
    .select(
        "customer_id",
        "customer_type"
    )
    .dropDuplicates(["customer_id"])
)

gold_dim_customer.orderBy("customer_id").show(10, truncate=False)

print("Customer dimension rows:", gold_dim_customer.count())

# COMMAND ----------

gold_dim_date = (
   silver_df
   .select("sale_date")
   .dropDuplicates()
   .withColumn(
       "date_id",
       date_format(col("sale_date"), "yyyyMMdd").cast("int")
   )
   .withColumn(
       "day",
       dayofmonth(col("sale_date"))
   )
   .withColumn(
       "month_number",
       month(col("sale_date"))
   )
   .withColumn(
       "month_name",
       date_format(col("sale_date"), "MMMM")
   )
   .withColumn(
       "quarter",
       quarter(col("sale_date"))
   )
   .withColumn(
       "year",
       year(col("sale_date"))
   )
   .select(
       "date_id",
       "sale_date",
       "day",
       "month_number",
       "month_name",
       "quarter",
       "year"
   )
)

gold_dim_date.orderBy("sale_date").show(10, truncate=False)
print("Date dimension rows:", gold_dim_date.count())

# COMMAND ----------

gold_fact_sales = (

    silver_df

    .join(

        gold_dim_model.select("model_id", "model"),

        on="model",

        how="left"

    )

    .withColumn(

        "date_id",

        date_format(col("sale_date"), "yyyyMMdd").cast("int")

    )

    .select(

        "sale_id",

        "date_id",

        "model_id",

        "dealer_id",

        "customer_id",

        "manufacturing_year",

        "mileage_km",

        "transmission",

        "listing_price_inr",

        "discount_percent",

        "sale_price_inr",

        "quantity"

    )

)
 
gold_fact_sales.show(10, truncate=False)
 
print("Fact sales rows:", gold_fact_sales.count())
 

# COMMAND ----------

missing_model_ids = (
    gold_fact_sales
    .filter(col("model_id").isNull())
    .count()
)

print("Missing model IDs:", missing_model_ids)

# COMMAND ----------

duplicate_sale_ids = (
    gold_fact_sales
    .groupBy("sale_id")
    .count()
    .filter(col("count") > 1)
    .count()
)

print("Duplicate sale IDs:", duplicate_sale_ids
)

# COMMAND ----------

gold_dim_model = (
    gold_dim_model
    .withColumn("data_layer", lit("gold"))
    .withColumn("gold_processed_timestamp", current_timestamp())
)

gold_dim_dealer = (

    gold_dim_dealer

    .withColumn("data_layer", lit("gold"))

    .withColumn("gold_processed_timestamp", current_timestamp())

)
 
gold_dim_customer = (

    gold_dim_customer

    .withColumn("data_layer", lit("gold"))

    .withColumn("gold_processed_timestamp", current_timestamp())

)
 
gold_dim_date = (

    gold_dim_date

    .withColumn("data_layer", lit("gold"))

    .withColumn("gold_processed_timestamp", current_timestamp())

)
 
gold_fact_sales = (

    gold_fact_sales

    .withColumn("data_layer", lit("gold"))

    .withColumn("gold_processed_timestamp", current_timestamp())

)
 

# COMMAND ----------

gold_dim_model.write \
   .format("delta") \
   .mode("overwrite") \
   .saveAsTable("workspace.default.gold_dim_model")

# COMMAND ----------

gold_dim_dealer.write \
   .format("delta") \
   .mode("overwrite") \
   .saveAsTable("workspace.default.gold_dim_dealer")

# COMMAND ----------

gold_dim_customer.write \
   .format("delta") \
   .mode("overwrite") \
   .saveAsTable("workspace.default.gold_dim_customer")

# COMMAND ----------

gold_dim_date.write \
   .format("delta") \
   .mode("overwrite") \
   .saveAsTable("workspace.default.gold_dim_date")

# COMMAND ----------

gold_fact_sales.write \
   .format("delta") \
   .mode("overwrite") \
   .saveAsTable("workspace.default.gold_fact_sales")

# COMMAND ----------

saved_fact_df = spark.table("workspace.default.gold_fact_sales")
saved_model_df = spark.table("workspace.default.gold_dim_model")
saved_dealer_df = spark.table("workspace.default.gold_dim_dealer")
saved_customer_df = spark.table("workspace.default.gold_dim_customer")
saved_date_df = spark.table("workspace.default.gold_dim_date")

print("Fact rows:", saved_fact_df.count())
print("Model rows:", saved_model_df.count())
print("Dealer rows:", saved_dealer_df.count())
print("Customer rows:", saved_customer_df.count())
print("Date rows:", saved_date_df.count())

# COMMAND ----------

gold_fact_sales.toPandas().to_csv(
    "/tmp/gold_fact_sales.csv",
    index=False
)
print("Export completed")

# COMMAND ----------

gold_dim_model.toPandas().to_csv(
   "/tmp/gold_dim_model.csv",
   index=False
)
gold_dim_dealer.toPandas().to_csv(
   "/tmp/gold_dim_dealer.csv",
   index=False
)
gold_dim_customer.toPandas().to_csv(
   "/tmp/gold_dim_customer.csv",
   index=False
)
gold_dim_date.toPandas().to_csv(
   "/tmp/gold_dim_date.csv",
   index=False
)
print("All Gold tables exported successfully.")