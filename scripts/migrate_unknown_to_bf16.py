import sqlite3

def migrate_unknown_to_bf16(db_path: str = "results.db"):
    """One-time migration to change Unknown data type to BF16."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Update all Unknown or NULL data types to BF16
    c.execute('''
        UPDATE benchmark_runs 
        SET data_type = 'BF16' 
        WHERE data_type IS NULL 
           OR data_type = 'Unknown'
    ''')
    
    # Print the changes
    print("\nUpdated records:")
    c.execute('''
        SELECT model, data_type, COUNT(*) as count 
        FROM benchmark_runs 
        GROUP BY model, data_type
    ''')
    for row in c.fetchall():
        print(f"Model: {row[0]}, Data Type: {row[1]}, Count: {row[2]}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_unknown_to_bf16() 