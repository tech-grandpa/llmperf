import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
import warnings

def load_benchmark_data(db_path: str = "results.db") -> pd.DataFrame:
    """Load benchmark results from SQLite database."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM benchmark_runs", conn)
    conn.close()
    return df

def plot_metrics_by_gpu(df: pd.DataFrame, save_dir: str = "plots"):
    """Plot key metrics by GPU type and data type."""
    Path(save_dir).mkdir(exist_ok=True)
    plt.style.use('seaborn-v0_8')  # Use the newer style name
    
    # Color scheme for data types
    colors = {'FP8': '#1f77b4', 'BF16': '#ff7f0e', 'Unknown': '#2ca02c'}
    
    def create_grouped_bar_plot(metric, title, ylabel):
        plt.figure(figsize=(12, 6))
        
        # Calculate means and std for each GPU/data_type combination
        stats = df.groupby(['gpu_info', 'data_type'])[metric].agg(['mean', 'std']).reset_index()
        
        # Replace NaN std with 0 for single data points
        stats['std'] = stats['std'].fillna(0)
        
        # Set up bar positions
        gpus = stats['gpu_info'].unique()
        data_types = stats['data_type'].unique()
        x = np.arange(len(gpus))
        width = 0.35  # Width of bars
        
        # Plot bars for each data type
        for i, dtype in enumerate(data_types):
            mask = stats['data_type'] == dtype
            data = stats[mask]
            if not data.empty:
                plt.bar(x + i*width - width/2, 
                       data['mean'],
                       width,
                       yerr=data['std'],
                       label=dtype,
                       color=colors[dtype],
                       capsize=5)
        
        plt.xlabel('GPU Type')
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(x, gpus, rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{save_dir}/{metric}_by_gpu.png")
        plt.close()

    # Suppress runtime warnings about NaN values
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        
        # Create plots for each metric
        create_grouped_bar_plot('overall_throughput', 
                              'Token Throughput by GPU Type and Data Type',
                              'Tokens/second')
        
        create_grouped_bar_plot('price_per_token',
                              'Price per Token by GPU Type and Data Type',
                              'Price per Token ($)')
        
        create_grouped_bar_plot('ttft',
                              'Time to First Token by GPU Type and Data Type',
                              'Time (seconds)')

def print_summary_stats(df: pd.DataFrame):
    """Print summary statistics for the benchmark runs."""
    print("\nSummary Statistics:")
    print("-" * 50)
    
    metrics = ['overall_throughput', 'price_per_token', 'ttft']
    
    # Calculate stats and handle NaN values
    stats = df.groupby(['gpu_info', 'data_type'])[metrics].agg(['mean', 'std']).round(3)
    stats = stats.fillna({'std': '-'})  # Replace NaN std with '-' for better display
    
    print("\nPerformance by GPU and Data Type:")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(stats)
    
    print("\nNumber of runs by GPU and Data Type:")
    print(pd.crosstab(df['gpu_info'], df['data_type']))
    
    # Print individual run details for debugging
    print("\nIndividual Run Details:")
    for idx, row in df.iterrows():
        print(f"\nRun {idx + 1}:")
        print(f"GPU: {row['gpu_info']}")
        print(f"Data Type: {row['data_type']}")
        print(f"Throughput: {row['overall_throughput']:.2f} tokens/s")
        print(f"Price/Token: ${row['price_per_token']:.8f}")
        print(f"Price/1M Tokens: ${(row['price_per_token'] * 1_000_000):.4f}")
        print(f"TTFT: {row['ttft']:.2f}s")

def main():
    df = load_benchmark_data()
    plot_metrics_by_gpu(df)
    print_summary_stats(df)

if __name__ == "__main__":
    main() 