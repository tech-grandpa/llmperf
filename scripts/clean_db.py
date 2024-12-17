import sqlite3

def clean_database(db_path: str = "results.db"):
    """Remove the anomalous H200 SXM BF16 run with low throughput (around 108.51 tokens/s)."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Delete the specific run with low throughput on H200 SXM
    c.execute('''
        DELETE FROM benchmark_runs 
        WHERE gpu_info = 'H200 SXM' 
        AND data_type = 'BF16'
        AND overall_throughput < 200
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    clean_database() 