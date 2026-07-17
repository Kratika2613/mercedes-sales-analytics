# Databricks notebook source
# MAGIC %md
# MAGIC **Mercedes-Benz Sales Analytics - Silver Layer**

# COMMAND ----------

from pyspark.sql.functions import (
    col,
    trim,
    upper,
    when,
    current_timestamp,
    lit
)

# COMMAND ----------

bronze_df = spark.table(
    "workspace.default.bronze_mercedes_sales"
)

# COMMAND ----------

print("Bronze rows:", bronze_df.count())
print("Bronze columns:", len(bronze_df.columns))

# COMMAND ----------

duplicate_count = bronze_df.count() - bronze_df.dropDuplicates().count()
print("Duplicate rows found:", duplicate_count)

# COMMAND ----------

bronze_df.groupBy("model").count().orderBy("model").show()

# COMMAND ----------

bronze_df.filter(col("color").isNull()).show()

# COMMAND ----------

bronze_df.filter(col("mileage_km").isNull()).show()

# COMMAND ----------

bronze_df.filter(col("state").isNull()).show()

# COMMAND ----------

silver_df = bronze_df.dropDuplicates()

# COMMAND ----------

print("Rows after duplicate removal:", silver_df.count())

# COMMAND ----------

silver_df = (
   silver_df
   .withColumn("model", trim(col("model")))
   .withColumn("vehicle_class", trim(col("vehicle_class")))
   .withColumn("fuel_type", trim(col("fuel_type")))
   .withColumn("dealer_name", trim(col("dealer_name")))
   .withColumn("city", trim(col("city")))
   .withColumn("state", trim(col("state")))
   .withColumn("region", trim(col("region")))
)

# COMMAND ----------

silver_df = silver_df.withColumn(
    "model",
    when(
        upper(col("model")) == "C-CLASS",
        "C-CLASS"
    ).otherwise(col("model"))
)

# COMMAND ----------

silver_df.groupBy("model").count().orderBy("model").show()

# COMMAND ----------

silver_df = silver_df.fillna({
    "color": "Unknown",
    "state": "Unknown",
    "mileage_km": 0
})

# COMMAND ----------

silver_df = (
    silver_df
    .withColumn("data_layer", lit("silver"))
    .withColumn("silver_processed_timestamp", current_timestamp())
)

len(silver_df.columns)

# COMMAND ----------

display(silver_df)

# COMMAND ----------

print(
    "Duplicates remaining:",
    silver_df.count() - silver_df.dropDuplicates().count()
)

print(
    "Missing color rows:",
    silver_df.filter(col("color").isNull()).count(
    )
)

print(
    "Missing state rows:",
    silver_df.filter(col("state").isNull()).count()
)

print("Silver rows:", silver_df.count())
print("Silver columns:", len(silver_df.columns))

# COMMAND ----------

silver_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.default.silver_mercedes_sales")

print("Silver table created successfully.")

# COMMAND ----------

saved_silver_df = spark.table(
    "workspace.default.silver_mercedes_sales"
)

print("Saved silver rows:", saved_silver_df.count())
print("Saved silver columns:", len(saved_silver_df.columns))

# COMMAND ----------

saved_silver_df.select(
    "sale_id",
    "model",
    "color",
    "mileage_km",
    "state",
    "data_layer"
).show(10, truncate=False)