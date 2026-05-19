# Databricks notebook source
# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_stations,
# MAGIC     SUM(NbBikes) AS total_bikes,
# MAGIC     SUM(NbDocks) AS total_docks,
# MAGIC     ROUND(AVG(occupancy_rate), 2) AS avg_occupancy
# MAGIC FROM bikepoint_gold

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     station_name,
# MAGIC     NbBikes,
# MAGIC     NbDocks,
# MAGIC     occupancy_rate
# MAGIC FROM bikepoint_gold
# MAGIC WHERE NbDocks > 0
# MAGIC ORDER BY occupancy_rate DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     station_name,
# MAGIC     NbBikes,
# MAGIC     NbDocks
# MAGIC FROM bikepoint_gold
# MAGIC ORDER BY NbBikes ASC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     station_name,
# MAGIC     NbEmptyDocks,
# MAGIC     NbDocks,
# MAGIC     empty_rate
# MAGIC FROM bikepoint_gold
# MAGIC ORDER BY empty_rate DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     station_name,
# MAGIC     lat,
# MAGIC     lon,
# MAGIC     NbBikes,
# MAGIC     NbDocks,
# MAGIC     occupancy_rate
# MAGIC FROM bikepoint_gold
# MAGIC WHERE occupancy_rate > 0.8
# MAGIC AND NbDocks >= 15
# MAGIC ORDER BY occupancy_rate DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     CASE
# MAGIC         WHEN occupancy_rate >= 0.8 THEN 'High Utilisation'
# MAGIC         WHEN occupancy_rate >= 0.5 THEN 'Medium Utilisation'
# MAGIC         ELSE 'Low Utilisation'
# MAGIC     END AS utilisation_band,
# MAGIC     COUNT(*) AS station_count
# MAGIC FROM bikepoint_gold
# MAGIC GROUP BY 1
# MAGIC ORDER BY station_count DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     station_name,
# MAGIC     NbDocks
# MAGIC FROM bikepoint_gold
# MAGIC ORDER BY NbDocks DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     ROUND(lat, 2) AS lat_zone,
# MAGIC     ROUND(lon, 2) AS lon_zone,
# MAGIC     COUNT(*) AS station_count,
# MAGIC     ROUND(AVG(occupancy_rate), 2) AS avg_occupancy
# MAGIC FROM bikepoint_gold
# MAGIC GROUP BY 1,2
# MAGIC ORDER BY avg_occupancy DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM bikepoint_gold
# MAGIC WHERE NbBikes > NbDocks

# COMMAND ----------

