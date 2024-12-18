import sqlite3

def inspect_and_clean_rtx3090(db_path: str = "results.db"):
    """Inspect and clean RTX 3090 data, removing BF16 entries."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # First show all RTX 3090 entries
    print("\nCurrent RTX 3090 entries:")
    c.execute('''
        SELECT id, timestamp, gpu_info, data_type, overall_throughput, ttft
        FROM benchmark_runs 
        WHERE gpu_info = 'RTX 3090'
        ORDER BY timestamp DESC
    ''')
    current = c.fetchall()
    for row in current:
        print(row)
    
    # Count entries by data type
    print("\nCount by data type:")
    c.execute('''
        SELECT data_type, COUNT(*) 
        FROM benchmark_runs 
        WHERE gpu_info = 'RTX 3090'
        GROUP BY data_type
    ''')
    counts = c.fetchall()
    for dtype, count in counts:
        print(f"{dtype}: {count} entries")
    
    # Remove BF16 entries if they exist
    c.execute('''
        DELETE FROM benchmark_runs 
        WHERE gpu_info = 'RTX 3090' AND data_type = 'BF16'
    ''')
    
    if c.rowcount > 0:
        print(f"\nRemoved {c.rowcount} BF16 entries")
        conn.commit()
    else:
        print("\nNo BF16 entries found to remove")
    
    # Show remaining entries
    print("\nRemaining RTX 3090 entries:")
    c.execute('''
        SELECT id, timestamp, gpu_info, data_type, overall_throughput, ttft
        FROM benchmark_runs 
        WHERE gpu_info = 'RTX 3090'
        ORDER BY timestamp DESC
    ''')
    remaining = c.fetchall()
    for row in remaining:
        print(row)
    
    conn.close()

if __name__ == "__main__":
    inspect_and_clean_rtx3090() 