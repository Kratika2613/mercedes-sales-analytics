# Databricks notebook source
# MAGIC %md
# MAGIC **Mercedes-Benz Sales Analytics - Bronze Layer**

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

# COMMAND ----------

raw_df = spark.table("workspace.default.mercedes_sales_raw")

# COMMAND ----------

print("Raw row count:", raw_df.count())
print("Raw column count:", len(raw_df.columns))

# COMMAND ----------

bronze_df = (
    raw_df
    .withColumn("ingestion_timestamp", current_timestamp())
    .withColumn("source_system", lit("mercedes_sales_csv"))
    .withColumn("data_layer", lit("bronze"))
)

# COMMAND ----------

display(bronze_df)

# COMMAND ----------

len(bronze_df.columns)

# COMMAND ----------

bronze_df.count()

# COMMAND ----------

bronze_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.default.bronze_mercedes_sales")

# COMMAND ----------

print("Bronze table created successfully.")

# COMMAND ----------

saved_bronze_df = spark.table(
   "workspace.default.bronze_mercedes_sales"
)
print("Saved bronze rows:", saved_bronze_df.count())
print("Saved bronze columns:", len(saved_bronze_df.columns))

# COMMAND ----------

saved_bronze_df.select(
    "sale_id",
    "model",
    "ingestion_timestamp",
    "source_system",
    "data_layer"
).show(5, truncate=False)