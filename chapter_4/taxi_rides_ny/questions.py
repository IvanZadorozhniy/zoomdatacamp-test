import duckdb

conn = duckdb.connect("taxi_rides_ny.duckdb")  # or dev.db if using dev
result = conn.execute("SELECT COUNT(*) AS record_count FROM taxi_rides_ny.prod.fct_monthly_zone_revenue").fetchall()
print(result)

#result = conn.execute("SELECT * FROM taxi_rides_ny.prod.fct_monthly_zone_revenue limit 4").fetchall()
#print(result)

result = conn.execute("""
SELECT pickup_zone, SUM(revenue_monthly_total_amount) AS total_revenue
FROM taxi_rides_ny.prod.fct_monthly_zone_revenue 
WHERE service_type = 'Green' AND YEAR(revenue_month) = 2020
GROUP BY pickup_zone
ORDER BY total_revenue DESC
limit 1
""").fetchall()
print(result)

result = conn.execute("""
SELECT SUM(total_monthly_trips) as total_trips
FROM taxi_rides_ny.prod.fct_monthly_zone_revenue 
WHERE service_type = 'Green' AND YEAR(revenue_month) = 2019 AND MONTH(revenue_month) = 10
""").fetchall()
print(result)