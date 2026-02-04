import duckdb

con = duckdb.connect()

con.execute(
    """
INSTALL httpfs;
LOAD httpfs;
"""
)

con.execute(
    """
SET s3_region='us-east-1';
SET s3_access_key_id='test';
SET s3_secret_access_key='test';
SET s3_endpoint='localhost:4566';
SET s3_use_ssl=false;
SET s3_url_style='path';
"""
)

# QUESTION 2
df_2 = con.execute(
    """
SELECT COUNT(*)
FROM 's3://chapter03/yellow_tripdata_2024-*.parquet'
"""
).fetchall()

print(df_2)

# QUESTION 3
df_3 = con.execute(
    """
SELECT COUNT(DISTINCT PULocationID)
FROM 's3://chapter03/yellow_tripdata_2024-*.parquet'
"""
).fetchall()
print(df_3)

# QUESTION 4
df_4 = con.execute(
    """
SELECT PULocationID
FROM 's3://chapter03/yellow_tripdata_2024-*.parquet'
"""
).fetchall()
print(df_4)

df_4 = con.execute(
    """
SELECT PULocationID, DOLocationID
FROM 's3://chapter03/yellow_tripdata_2024-*.parquet'
"""
).fetchall()
print(df_4)

# QUESTION 5
df_5 = con.execute(
    """
SELECT COUNT(*) AS zero_fare_trips
FROM 's3://chapter03/yellow_tripdata_2024-*.parquet'
WHERE fare_amount = 0;
"""
).fetchall()
print(df_5)

# QUESTION 6
df_6 = con.execute(
    """
SELECT DISTINCT VendorID
FROM 's3://chapter03/yellow_tripdata_2024-*.parquet'
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
"""
).fetchall()
print(df_6)
