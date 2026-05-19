# Databricks notebook source
df_bronze = spark.table("bikepoint_bronze")

# COMMAND ----------

display(df_bronze.limit(5))

# COMMAND ----------

df_bronze.printSchema()

# COMMAND ----------

silver = df_bronze.select(
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

silver = silver.filter(
    "lat IS NOT NULL AND lon IS NOT NULL"
)

# COMMAND ----------

silver = silver.dropDuplicates(["id"])

# COMMAND ----------

silver = silver.withColumnRenamed("commonName", "station_name")

# COMMAND ----------

display(silver.limit(5))

# COMMAND ----------

print(f"Silver row count: {silver.count()}")

# COMMAND ----------

spark.sql("DROP TABLE IF EXISTS bikepoint_silver")

# COMMAND ----------

silver.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("bikepoint_silver")

# COMMAND ----------

display(spark.table("bikepoint_silver"))

# COMMAND ----------

assert silver.filter("lat IS NULL").count() == 0
assert silver.filter("lon IS NULL").count() == 0

# COMMAND ----------

print("Silver transformation completed successfully")