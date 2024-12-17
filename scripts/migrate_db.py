import sqlite3

def extract_data_type(model_name: str) -> str:
    """Extract data type from model name."""
    model_lower = model_name.lower()
    if 'fp8' in model_lower:
        return 'FP8'
    elif 'bf16' in model_lower:
        return 'BF16'
    else:
        return 'Unknown'

def migrate_database(db_path: str = "results.db"):
    """Add new columns and update existing data."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Add new columns if they don't exist
    try:
        c.execute('ALTER TABLE benchmark_runs ADD COLUMN price_per_hour REAL')
    except sqlite3.OperationalError:
        pass
        
    try:
        c.execute('ALTER TABLE benchmark_runs ADD COLUMN price_per_token REAL')
    except sqlite3.OperationalError:
        pass
        
    try:
        c.execute('ALTER TABLE benchmark_runs ADD COLUMN ttft REAL')
    except sqlite3.OperationalError:
        pass

    try:
        c.execute('ALTER TABLE benchmark_runs ADD COLUMN data_type TEXT')
    except sqlite3.OperationalError:
        pass
    
    # Update data_type for existing entries
    c.execute('SELECT id, model FROM benchmark_runs WHERE data_type IS NULL')
    rows = c.fetchall()
    for row_id, model in rows:
        data_type = extract_data_type(model)
        c.execute('UPDATE benchmark_runs SET data_type = ? WHERE id = ?', 
                 (data_type, row_id))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_database() 