import sqlite3

def fix_h100_price(db_path: str = "results.db"):
    """Update price_per_hour for H100 SXM entries from 3.99 to 2.99."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # First show current entries
    print("\nCurrent H100 entries:")
    c.execute('''
        SELECT id, timestamp, gpu_info, price_per_hour, overall_throughput,
               mean_input_tokens, mean_output_tokens
        FROM benchmark_runs 
        WHERE gpu_info = 'H100 SXM'
    ''')
    current = c.fetchall()
    for row in current:
        print(row)
    
    # Update the price
    c.execute('''
        UPDATE benchmark_runs 
        SET price_per_hour = 2.99,
            price_per_token = (2.99 / (overall_throughput * 3600 * (mean_input_tokens / mean_output_tokens)))
        WHERE gpu_info = 'H100 SXM'
    ''')
    
    # Show updated entries
    print("\nUpdated H100 entries:")
    c.execute('''
        SELECT id, timestamp, gpu_info, price_per_hour, overall_throughput,
               price_per_token
        FROM benchmark_runs 
        WHERE gpu_info = 'H100 SXM'
    ''')
    updated = c.fetchall()
    for row in updated:
        print(row)
    
    print(f"\nUpdated {c.rowcount} entries")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_h100_price() 