import sqlite3
import pandas as pd
import numpy as np

def inspect_rtx6000_data(db_path: str = "results.db"):
    """Examine RTX 6000 entries in detail."""
    conn = sqlite3.connect(db_path)
    
    # Get all RTX 6000 entries with detailed metrics
    query = '''
        SELECT id, timestamp, model, data_type,
               ttft, mean_latency, overall_throughput,
               mean_input_tokens, mean_output_tokens,
               raw_results
        FROM benchmark_runs 
        WHERE gpu_info = 'RTX 6000'
        ORDER BY timestamp DESC
    '''
    
    df = pd.read_sql_query(query, conn)
    
    print("\nRTX 6000 TTFT Statistics:")
    print(f"Number of runs: {len(df)}")
    print(f"Mean TTFT: {df['ttft'].mean():.3f}s")
    print(f"Std TTFT: {df['ttft'].std():.3f}s")
    print(f"Min TTFT: {df['ttft'].min():.3f}s")
    print(f"Max TTFT: {df['ttft'].max():.3f}s")
    
    print("\nDetailed view of each run:")
    for _, row in df.iterrows():
        print(f"\nRun ID: {row['id']}")
        print(f"Timestamp: {row['timestamp']}")
        print(f"Model: {row['model']}")
        print(f"Data Type: {row['data_type']}")
        print(f"TTFT: {row['ttft']:.3f}s")
        print(f"Mean Latency: {row['mean_latency']:.3f}s")
        print(f"Throughput: {row['overall_throughput']:.2f} tokens/s")
        print(f"Input/Output tokens: {row['mean_input_tokens']:.0f}/{row['mean_output_tokens']:.0f}")
    
    conn.close()

if __name__ == "__main__":
    inspect_rtx6000_data() 