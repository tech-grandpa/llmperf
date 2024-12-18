import sqlite3
import pandas as pd

def verify_price_calculations(db_path: str = "results.db"):
    """Verify price calculations for all entries."""
    conn = sqlite3.connect(db_path)
    
    df = pd.read_sql_query('''
        SELECT id, gpu_info, data_type, price_per_hour, 
               overall_throughput, price_per_token,
               mean_input_tokens, mean_output_tokens
        FROM benchmark_runs
        ORDER BY gpu_info, data_type
    ''', conn)
    
    print("\nVerifying price calculations:")
    for _, row in df.iterrows():
        # Convert output tokens/sec to input tokens/sec using the ratio
        token_ratio = row['mean_input_tokens'] / row['mean_output_tokens']
        input_throughput = row['overall_throughput'] * token_ratio
        input_tokens_per_hour = input_throughput * 3600
        expected_price_per_token = row['price_per_hour'] / input_tokens_per_hour
        actual_price_per_token = row['price_per_token']
        
        print(f"\n{row['gpu_info']} ({row['data_type']}):")
        print(f"  Price per hour: ${row['price_per_hour']:.2f}")
        print(f"  Output throughput: {row['overall_throughput']:.2f} tokens/second")
        print(f"  Input/Output ratio: {token_ratio:.2f}")
        print(f"  Input throughput: {input_throughput:.2f} tokens/second")
        print(f"  Input tokens per hour: {input_tokens_per_hour:,.2f}")
        print(f"  Expected price/token: ${expected_price_per_token:.8f}")
        print(f"  Actual price/token: ${actual_price_per_token:.8f}")
        
        if abs(expected_price_per_token - actual_price_per_token) > 1e-10:
            print("  WARNING: Mismatch in price calculation!")
    
    conn.close()

if __name__ == "__main__":
    verify_price_calculations() 