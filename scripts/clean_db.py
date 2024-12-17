import sqlite3

def clean_database(db_path: str = "results.db"):
    """Remove the first two runs from the database."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Delete the first two entries by ID
    c.execute('''
        DELETE FROM benchmark_runs 
        WHERE id IN (
            SELECT id 
            FROM benchmark_runs 
            ORDER BY id ASC 
            LIMIT 2
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    clean_database() 