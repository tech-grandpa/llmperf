import sqlite3

def remove_last_entry(db_path: str = "results.db"):
    """Remove the last entry from the benchmark_runs table."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Get the max ID
    c.execute('SELECT MAX(id) FROM benchmark_runs')
    max_id = c.fetchone()[0]
    
    if max_id:
        # Delete the last entry
        c.execute('DELETE FROM benchmark_runs WHERE id = ?', (max_id,))
        print(f"Removed entry with id {max_id}")
    
    # Show remaining entries
    c.execute('''
        SELECT id, timestamp, model, gpu_info, overall_throughput 
        FROM benchmark_runs 
        ORDER BY id DESC 
        LIMIT 5
    ''')
    print("\nLast 5 entries:")
    for row in c.fetchall():
        print(f"ID: {row[0]}, Time: {row[1]}, Model: {row[2]}, GPU: {row[3]}, Throughput: {row[4]}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    remove_last_entry() 