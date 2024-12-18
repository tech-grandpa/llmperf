import sqlite3
import pandas as pd

def check_database(db_path: str = "results.db"):
    """Print summary of database contents."""
    conn = sqlite3.connect(db_path)
    
    # Get overview of data
    df = pd.read_sql_query('''
        SELECT gpu_info, data_type, 
               COUNT(*) as count,
               AVG(overall_throughput) as avg_throughput,
               AVG(ttft) as avg_ttft
        FROM benchmark_runs
        GROUP BY gpu_info, data_type
    ''', conn)
    
    print("\nSummary by GPU and data type:")
    print(df)
    
    conn.close()

if __name__ == "__main__":
    check_database() 