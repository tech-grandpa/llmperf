import sqlite3
import pandas as pd

def examine_and_clean_h200_data(db_path: str = "results.db"):
    """Examine H200 SXM entries and clean up problematic data."""
    conn = sqlite3.connect(db_path)
    
    # First, let's look at all H200 entries in detail
    query = '''
        SELECT id, timestamp, model, gpu_info, data_type, 
               overall_throughput, ttft, mean_latency
        FROM benchmark_runs 
        WHERE gpu_info = 'H200 SXM'
        ORDER BY timestamp DESC
    '''
    
    df = pd.read_sql_query(query, conn)
    print("\nAll H200 SXM entries:")
    print(df)
    
    # Find potentially problematic entries (e.g., significantly different throughput)
    mean_throughput = df['overall_throughput'].mean()
    std_throughput = df['overall_throughput'].std()
    outliers = df[abs(df['overall_throughput'] - mean_throughput) > 2 * std_throughput]
    
    if not outliers.empty:
        print("\nPotentially problematic entries (outliers):")
        print(outliers)
        
        # Delete outliers
        outlier_ids = outliers['id'].tolist()
        c = conn.cursor()
        for id in outlier_ids:
            c.execute('DELETE FROM benchmark_runs WHERE id = ?', (id,))
            print(f"\nRemoved entry with id {id}")
        
        conn.commit()
    else:
        print("\nNo obvious outliers found")
    
    # Show final state
    df_after = pd.read_sql_query(query, conn)
    print("\nRemaining H200 SXM entries:")
    print(df_after)
    
    conn.close()

if __name__ == "__main__":
    examine_and_clean_h200_data() 