import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse
import json

def create_plots_dir(db_path, prefix=None):
    """Create plots directory relative to database path with optional prefix."""
    # Get the directory where the database file is located
    db_dir = os.path.dirname(os.path.abspath(db_path))
    
    # Create plots folder name with optional prefix
    plots_dir = f'{prefix}_plots' if prefix else 'plots'
    
    # Create full path for plots directory
    plots_path = os.path.join(db_dir, plots_dir)
    
    if not os.path.exists(plots_path):
        os.makedirs(plots_path)
    
    return plots_path

def get_gpu_order_by_fp8_ttft(df):
    """Get GPU order based on FP8 TTFT values."""
    fp8_ttft = df[df['data_type'] == 'FP8'].groupby('gpu_info')['ttft'].mean()
    return fp8_ttft.sort_values().index.tolist()

def get_gpu_order_by_fp8_gpu_name(df):
    """Get GPU order based on gpu_info values."""
    # Get unique GPU names from FP8 entries and sort them
    gpu_names = df[df['data_type'] == 'FP8']['gpu_info'].unique()
    return sorted(gpu_names.tolist())

def create_grouped_bar_plot(metric_name, df, title, ylabel, filename, gpu_order, plots_path, prefix=None):
    """Create a grouped bar plot with error bars."""
    # Check if dataframe is empty
    if df.empty:
        print(f"No data available for {title}")
        return
    
    # Check if we have any data for the metric
    if df[metric_name].isna().all():
        print(f"No data available for metric: {metric_name}")
        return
        
    # Get unique data types with actual data
    data_types = df[df[metric_name].notna()]['data_type'].unique()
    if len(data_types) == 0:
        print(f"No valid data types found for {metric_name}")
        return
    
    data_types = sorted(data_types)
    
    # Set up the plot with larger font sizes
    plt.rcParams.update({'font.size': 16})
    plt.figure(figsize=(14, 8))
    width = 0.35
    x = np.arange(len(gpu_order))
    
    # Create bars for each data type
    for i, dtype in enumerate(data_types):
        data = []
        errors = []
        for gpu in gpu_order:
            gpu_data = df[(df['gpu_info'] == gpu) & (df['data_type'] == dtype)]
            if not gpu_data.empty:
                # Convert to price per million input tokens if that's what we're plotting
                if metric_name == 'price_per_token':
                    value = gpu_data[metric_name].mean() * 1_000_000
                    error = gpu_data[metric_name].std() * 1_000_000
                else:
                    value = gpu_data[metric_name].mean()
                    error = gpu_data[metric_name].std()
                data.append(value)
                errors.append(error)
            else:
                data.append(0)
                errors.append(0)
        
        plt.bar(x + i*width - width/2, 
               data,
               width,
               label=dtype,
               yerr=errors,
               capsize=5)
    
    plt.xlabel('GPU', fontsize=18)
    plt.ylabel(ylabel, fontsize=18)
    plt.title(title, fontsize=20, pad=20)
    plt.xticks(x, gpu_order, rotation=45, ha='right', fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(fontsize=16)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Modify the save path to include the prefix if provided
    save_filename = f'{prefix}_{filename}.png' if prefix else f'{filename}.png'
    plt.savefig(os.path.join(plots_path, save_filename), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Reset font size for subsequent plots
    plt.rcParams.update({'font.size': plt.rcParamsDefault['font.size']})

def plot_metrics_by_gpu(df, db_path, prefix=None):
    """Create various performance metric plots."""
    if df.empty:
        print("No data found in the database. Please run benchmarks first.")
        return
        
    plots_path = create_plots_dir(db_path, prefix)
    
    # Get GPU order based on FP8 TTFT
    gpu_order_by_ttft = get_gpu_order_by_fp8_ttft(df)
    gpu_order_by_gpu_info = get_gpu_order_by_fp8_gpu_name(df)
    print("\nGPU order based on FP8 TTFT:")
    for i, gpu in enumerate(gpu_order_by_ttft, 1):
        fp8_ttft = df[(df['data_type'] == 'FP8') & (df['gpu_info'] == gpu)]['ttft'].mean()
        print(f"{i}. {gpu}: {fp8_ttft:.3f}s")
    
    # Plot metrics using consistent GPU order and adding plots_path
    create_grouped_bar_plot('ttft',
                          df,
                          'Time To First Token by GPU and Data Type',
                          'Seconds',
                          'ttft_by_gpu',
                          gpu_order_by_ttft,
                          plots_path,
                          prefix)
    
    create_grouped_bar_plot('overall_throughput', 
                          df,
                          'Token Generation Throughput by GPU and Data Type',
                          'Tokens/second',
                          'overall_throughput_by_gpu',
                          gpu_order_by_gpu_info,
                          plots_path,
                          prefix)

    create_grouped_bar_plot('request_output_throughput',
                          df,
                          'Token/Second per Request by GPU and Data Type',
                          'Tokens/second',
                          'overall_tokenpersecond_by_gpu',
                          gpu_order_by_gpu_info,
                          plots_path,
                          prefix)

    # create_grouped_bar_plot('price_per_token',
    #                       df,
    #                       'Price per million input Tokens by GPU and Data Type',
    #                       'USD per million input Tokens',
    #                       'price_per_token_by_gpu',
    #                       gpu_order_by_gpu_info,
    #                       plots_path,
    #                       prefix)

def print_summary_stats(df):
    """Print summary statistics for the benchmark results."""
    print("\nSummary Statistics:")
    
    # Get GPU order for consistent presentation
    gpu_order = get_gpu_order_by_fp8_ttft(df)
    
    metrics = {
        'Throughput': 'overall_throughput',
        'TTFT': 'ttft',
        'Price per Token': 'price_per_token',
        'Token per Second': 'request_output_throughput'
    }
    
    for metric_name, column in metrics.items():
        print(f"\nAverage {metric_name} by GPU and Data Type:")
        stats = df.pivot_table(
            values=column,
            index='gpu_info',
            columns='data_type',
            aggfunc='mean'
        ).reindex(gpu_order)
        print(stats)

# Function to check if a column exists in a table
def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [col[1] for col in cursor.fetchall()]
    return column_name in columns

def main():
    parser = argparse.ArgumentParser(description='Visualize LLM benchmark results')
    parser.add_argument('--db-path', 
                       type=str,
                       default='results.db',
                       help='Path to the SQLite database (default: results.db)')
    parser.add_argument('--prefix',
                       type=str,
                       default=None,
                       help='Prefix to add to output filenames')
    
    args = parser.parse_args()
    
    conn = sqlite3.connect(args.db_path)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS benchmark_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gpu_info TEXT,
            data_type TEXT,
            overall_throughput REAL,
            ttft REAL,
            price_per_token REAL,
            mean_latency REAL,
            raw_results TEXT,
            request_output_throughput REAL
        )
    ''')
    conn.commit()

    # Add new columns if they don't exist
    if not column_exists(cursor, "benchmark_runs", "request_output_throughput"):
        cursor.execute("ALTER TABLE benchmark_runs ADD COLUMN request_output_throughput REAL DEFAULT NULL;")

    # Commit the changes to ensure table schema is updated
    conn.commit()

    # Load data
    df = pd.read_sql_query('''
        SELECT gpu_info, data_type, overall_throughput, ttft, 
               price_per_token, mean_latency, raw_results, id
        FROM benchmark_runs
    ''', conn)

    # Iterate over rows to extract and update the JSON data
    for index, row in df.iterrows():
        raw_results = row['raw_results']
        rowid = row['id']  # Use rowid to identify the row uniquely

        if raw_results:
            try:
                raw_results_json = json.loads(raw_results)
                throughput_data = raw_results_json.get("results", {}).get("request_output_throughput_token_per_s", {})
                mean_value = throughput_data.get("mean", None)

                # Update the database with the extracted values
                cursor.execute('''
                    UPDATE benchmark_runs 
                    SET request_output_throughput = ?
                    WHERE id = ?
                ''', (mean_value, rowid))
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing JSON for row {index}: {e}")

    # Commit the updates
    conn.commit()

    # Load data
    df = pd.read_sql_query('''
        SELECT gpu_info, data_type, overall_throughput, ttft, 
               price_per_token, mean_latency, raw_results, request_output_throughput
        FROM benchmark_runs
    ''', conn)

    # Generate plots with prefix and db_path
    plot_metrics_by_gpu(df, args.db_path, args.prefix)
    
    # Print summary statistics
    print_summary_stats(df)
    
    conn.close()

if __name__ == "__main__":
    main() 