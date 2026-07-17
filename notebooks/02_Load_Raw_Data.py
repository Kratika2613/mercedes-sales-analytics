# Databricks notebook source
df = spark.table("workspace.default.mercedes_sales_raw")

# COMMAND ----------

display(df)

# COMMAND ----------

df.count()

# COMMAND ----------

len(df.columns)

# COMMAND ----------

df.columns

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df.show(10,truncate=False)

# COMMAND ----------

display(df)

# COMMAND ----------

df.select("model").show()

# COMMAND ----------

df.select("model", "sale_price_inr").show()

# COMMAND ----------

df.show()

# COMMAND ----------

df.filter(df.sale_price_inr > 8000000).show()

# COMMAND ----------

df.filter(
    (df.region == "West") &
    (df.sale_price_inr > 7000000)
).show()

# COMMAND ----------

df.select("model").distinct().show()

# COMMAND ----------

df.orderBy(df.sale_price_inr.desc()).show()

# COMMAND ----------

df.orderBy(df.sale_price_inr.asc()).show()

# COMMAND ----------

df.groupBy("model").count().show()

# COMMAND ----------

from pyspark.sql.functions import avg

# COMMAND ----------

df.groupBy("model").agg(
    avg("sale_price_inr")
).show()

# COMMAND ----------

from pyspark.sql.functions import max

# COMMAND ----------

df.select(
    max("sale_price_inr")
).show()

# COMMAND ----------

from pyspark.sql.functions import min

# COMMAND ----------

df.select(
    min("sale_price_inr")
).show()

# COMMAND ----------

df.withColumnRenamed(
    "sale_price_inr",
    "selling_price"
).show()

# COMMAND ----------

df.filter(
    df.color.isNull()
).show()

# COMMAND ----------

df.count()

# COMMAND ----------

df.dropDuplicates().count()

# COMMAND ----------

df.count()

# COMMAND ----------

len(df.columns)

# COMMAND ----------

df.columns

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df.show(10, truncate=False)

# COMMAND ----------

df.select("model").distinct().show()

# COMMAND ----------

df.select("region").distinct().show()

# COMMAND ----------

df.groupBy("region").count().show()

# COMMAND ----------

df.groupBy("model").count().orderBy("count", ascending=False).show()

# COMMAND ----------

# MAGIC %md
# MAGIC **Average selling price by model**

# COMMAND ----------

from pyspark.sql.functions import avg

# COMMAND ----------

df.groupBy("model") \
    .agg(avg("sale_price_inr").alias("average_sale_price")) \
    .orderBy("average_sale_price", ascending=False) \
    .show()


# COMMAND ----------

# MAGIC %md
# MAGIC **Highest sale price**

# COMMAND ----------

from pyspark.sql.functions import max

# COMMAND ----------

df.select(
    max("sale_price_inr").alias("highest_sale_price")
).show()

# COMMAND ----------

# MAGIC %md
# MAGIC **Lowest sale price**

# COMMAND ----------

from pyspark.sql.functions import min

# COMMAND ----------

df.select(
    min("sale_price_inr").alias("lowest_sale_price")
).show()

# COMMAND ----------

# MAGIC %md
# MAGIC **Region-wise sales count**

# COMMAND ----------

df.groupBy("region") \
    .count() \
    .orderBy("count", ascending=False) \
    .show()

# COMMAND ----------

# MAGIC %md
# MAGIC **Missing color check**

# COMMAND ----------

df.filter(df.color.isNull()).show()

# COMMAND ----------

# MAGIC %md
# MAGIC **Duplicate check**

# COMMAND ----------

print("Original rows:", df.count())
print("Rows after removing duplicates:", df.dropDuplicates().count())