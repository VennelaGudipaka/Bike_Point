# Databricks notebook source
import requests
import pandas as pd
from pyspark.sql.functions import current_timestamp

# COMMAND ----------

url = "https://api.tfl.gov.uk/BikePoint/"

response = requests.get(url)

print(f"Status code: {response.status_code}")

# COMMAND ----------

raw_json = response.json()

print(f"Number of bike points: {len(raw_json)}")

# COMMAND ----------

pdf = pd.json_normalize(raw_json)

# COMMAND ----------

pdf.head()

# COMMAND ----------

df_raw = spark.createDataFrame(pdf)

# COMMAND ----------

display(df_raw.limit(5))

# COMMAND ----------

df_raw.printSchema()

# COMMAND ----------

df_bronze = df_raw.withColumn(
    "ingestion_timestamp",
    current_timestamp()
)

# COMMAND ----------

df_bronze = df_bronze.select(
    "id",
    "commonName",
    "lat",
    "lon",
    "placeType",
    "url",
    "additionalProperties",
    "ingestion_timestamp"
)

# COMMAND ----------

display(df_bronze.limit(5))

# COMMAND ----------

df_bronze.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("bikepoint_bronze")

# COMMAND ----------

print(f"Bronze row count: {spark.table('bikepoint_bronze').count()}")

# COMMAND ----------

print("Bronze ingestion completed successfully")