import sqlite3
import pandas as pd
import json

# Connect to the database
conn = sqlite3.connect("results.db")

# 1. Look at all columns for the most recent run
print("\n1. Most recent run details:")
query1 = """
SELECT timestamp, model, gpu_info, overall_throughput, mean_latency, p99_latency 
FROM benchmark_runs 
ORDER BY timestamp DESC 
LIMIT 1
"""
print(pd.read_sql_query(query1, conn))

# 2. Check for NULL values in important columns
print("\n2. Count of NULL values in each column:")
query2 = """
SELECT 
    SUM(CASE WHEN overall_throughput IS NULL THEN 1 ELSE 0 END) as null_throughput,
    SUM(CASE WHEN mean_latency IS NULL THEN 1 ELSE 0 END) as null_mean_latency,
    SUM(CASE WHEN p99_latency IS NULL THEN 1 ELSE 0 END) as null_p99_latency,
    COUNT(*) as total_rows
FROM benchmark_runs
"""
print(pd.read_sql_query(query2, conn))

# 3. Look at raw results JSON for the latest run
print("\n3. Raw results from latest run:")
query3 = "SELECT raw_results FROM benchmark_runs ORDER BY timestamp DESC LIMIT 1"
raw_results = pd.read_sql_query(query3, conn).iloc[0]['raw_results']
print(json.dumps(json.loads(raw_results), indent=2)[:500] + "...") # Print first 500 chars

# 4. Check value ranges
print("\n4. Value ranges for key metrics:")
query4 = """
SELECT 
    MIN(overall_throughput) as min_throughput,
    MAX(overall_throughput) as max_throughput,
    MIN(mean_latency) as min_latency,
    MAX(mean_latency) as max_latency
FROM benchmark_runs
"""
print(pd.read_sql_query(query4, conn))

# 5. Check results grouped by model and GPU
print("\n5. Results by model and GPU:")
query5 = """
SELECT 
    model,
    gpu_info,
    COUNT(*) as num_runs,
    AVG(overall_throughput) as avg_throughput,
    AVG(mean_latency) as avg_latency
FROM benchmark_runs
GROUP BY model, gpu_info
"""
print(pd.read_sql_query(query5, conn))

# Check the raw data
print("Raw data from database:")
query = """
SELECT 
    model,
    data_type,
    gpu_info,
    price_per_hour,
    overall_throughput,
    price_per_token
FROM benchmark_runs
"""
print(pd.read_sql_query(query, conn))

conn.close()