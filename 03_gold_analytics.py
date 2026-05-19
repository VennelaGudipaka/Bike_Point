# Databricks notebook source
df_silver = spark.table("bikepoint_silver")

# COMMAND ----------

display(df_silver.limit(5))

# COMMAND ----------

df_silver.printSchema()

# COMMAND ----------

spark.sql("DROP TABLE IF EXISTS bikepoint_gold")

# COMMAND ----------

from pyspark.sql.functions import expr

# COMMAND ----------

gold = df_silver.select(
    "id",
    "station_name",
    "lat",
    "lon",
    "placeType",
    "url",
    "ingestion_timestamp",

    expr("""
        CAST(
            filter(additionalProperties, x -> x.key = 'NbBikes')[0].value
            AS INT
        )
    """).alias("NbBikes"),

    expr("""
        CAST(
            filter(additionalProperties, x -> x.key = 'NbDocks')[0].value
            AS INT
        )
    """).alias("NbDocks"),

    expr("""
        CAST(
            filter(additionalProperties, x -> x.key = 'NbEmptyDocks')[0].value
            AS INT
        )
    """).alias("NbEmptyDocks")
)

# COMMAND ----------

display(gold.limit(5))

# COMMAND ----------

gold = gold.withColumn(
    "occupancy_rate",
    expr("NbBikes / NbDocks")
).withColumn(
    "empty_rate",
    expr("NbEmptyDocks / NbDocks")
)

# COMMAND ----------

display(gold.limit(10))

# COMMAND ----------

assert gold.filter("NbBikes > NbDocks").count() == 0
assert gold.filter("lat IS NULL").count() == 0
assert gold.filter("lon IS NULL").count() == 0

# COMMAND ----------

gold.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("bikepoint_gold")

# COMMAND ----------

display(spark.table("bikepoint_gold"))

# COMMAND ----------

print(f"Gold row count: {gold.count()}")

# COMMAND ----------

print("Gold analytics completed successfully")