import sqlite3

def recalculate_prices(db_path: str = "results.db"):
    """Recalculate price per token for all entries using the new formula."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Get all relevant data
    c.execute('''
        SELECT 
            id,
            price_per_hour,
            overall_throughput,
            mean_input_tokens,
            mean_output_tokens
        FROM benchmark_runs
    ''')
    rows = c.fetchall()
    
    print("\nRecalculating prices:")
    for row in rows:
        id, price_per_hour, output_throughput, mean_input_tokens, mean_output_tokens = row
        
        # Calculate new price per token
        if output_throughput and mean_input_tokens and mean_output_tokens:
            token_ratio = mean_input_tokens / mean_output_tokens
            input_throughput = output_throughput * token_ratio
            input_tokens_per_hour = input_throughput * 3600
            price_per_token = price_per_hour / input_tokens_per_hour
        else:
            price_per_token = 0
            
        # Update the database
        c.execute('''
            UPDATE benchmark_runs 
            SET price_per_token = ? 
            WHERE id = ?
        ''', (price_per_token, id))
        
        print(f"\nRun ID: {id}")
        print(f"Old throughput (output tokens/s): {output_throughput:.2f}")
        print(f"New throughput (input tokens/s): {input_throughput:.2f}")
        print(f"Price per token: ${price_per_token:.8f}")
        print(f"Price per 1M tokens: ${price_per_token * 1_000_000:.4f}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    recalculate_prices() 