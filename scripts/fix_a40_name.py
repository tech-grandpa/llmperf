import sqlite3

def fix_a40_name(db_path: str = "results_vllm.db"):
    """Rename 'NVIDIA A40' to 'A40' in the database."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # First show current unique GPU names
    print("\nCurrent GPU names:")
    c.execute('SELECT DISTINCT gpu_info FROM benchmark_runs ORDER BY gpu_info')
    current = c.fetchall()
    for row in current:
        print(row[0])
    
    # Update the name
    c.execute('''
        UPDATE benchmark_runs 
        SET gpu_info = 'A40'
        WHERE gpu_info = 'NVIDIA A40'
    ''')
    
    # Show updated unique GPU names
    print("\nUpdated GPU names:")
    c.execute('SELECT DISTINCT gpu_info FROM benchmark_runs ORDER BY gpu_info')
    updated = c.fetchall()
    for row in updated:
        print(row[0])
    
    print(f"\nUpdated {c.rowcount} entries")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_a40_name() 