# Databricks notebook source
print("Hello")

# COMMAND ----------

spark

# COMMAND ----------

data = [
    ("A-Class", 4200000),
    ("C-Class", 6200000),
    ("E-Class", 8500000)
]
columns = ["Model","Price"]

df = spark.createDataFrame(data,columns)
display(df)

# COMMAND ----------

df.columns

# COMMAND ----------

df.printSchema

# COMMAND ----------

df.show()

# COMMAND ----------

df.count()

# COMMAND ----------

df.select("Model").show()

# COMMAND ----------

df.filter(df.Price > 5000000).show()