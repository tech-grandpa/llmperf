import sqlite3

def fix_gpu_names(db_path: str = "results.db"):
    """Fix GPU naming conventions in the database."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # First show current unique GPU names
    print("\nCurrent GPU names:")
    c.execute('SELECT DISTINCT gpu_info FROM benchmark_runs ORDER BY gpu_info')
    current = c.fetchall()
    for row in current:
        print(row[0])
    
    # Update the names
    c.execute('''
        UPDATE benchmark_runs 
        SET gpu_info = 'RTX A6000'
        WHERE gpu_info = 'RTX 6000'
    ''')
    
    c.execute('''
        UPDATE benchmark_runs 
        SET gpu_info = 'RTX 6000 Ada'
        WHERE gpu_info = 'RTX A6000 Ada'
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
    fix_gpu_names() 