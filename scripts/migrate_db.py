import sqlite3

def migrate_database(db_path: str = "results.db"):
    """Add new columns to existing database."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Add new columns if they don't exist
    try:
        c.execute('ALTER TABLE benchmark_runs ADD COLUMN price_per_hour REAL')
    except sqlite3.OperationalError:
        pass  # Column already exists
        
    try:
        c.execute('ALTER TABLE benchmark_runs ADD COLUMN price_per_token REAL')
    except sqlite3.OperationalError:
        pass
        
    try:
        c.execute('ALTER TABLE benchmark_runs ADD COLUMN ttft REAL')
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_database() 