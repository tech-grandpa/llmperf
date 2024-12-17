import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def load_benchmark_data(db_path: str = "results.db") -> pd.DataFrame:
    """Load benchmark results from SQLite database."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM benchmark_runs", conn)
    conn.close()
    return df

def plot_metrics_by_gpu(df: pd.DataFrame, save_dir: str = "plots"):
    """Plot key metrics by GPU type."""
    Path(save_dir).mkdir(exist_ok=True)
    
    # Set style for all plots
    plt.style.use('seaborn')
    
    # 1. Throughput by GPU
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='gpu_info', y='overall_throughput', 
                ci='sd', capsize=0.1)
    plt.title('Token Throughput by GPU Type')
    plt.xlabel('GPU Type')
    plt.ylabel('Tokens/second')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/throughput_by_gpu.png")
    plt.close()
    
    # 2. Price per token by GPU
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='gpu_info', y='price_per_token', 
                ci='sd', capsize=0.1)
    plt.title('Price per Token by GPU Type')
    plt.xlabel('GPU Type')
    plt.ylabel('Price per Token ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/price_per_token_by_gpu.png")
    plt.close()
    
    # 3. Time to First Token by GPU
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='gpu_info', y='ttft', 
                ci='sd', capsize=0.1)
    plt.title('Time to First Token by GPU Type')
    plt.xlabel('GPU Type')
    plt.ylabel('Time (seconds)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/ttft_by_gpu.png")
    plt.close()

def print_summary_stats(df: pd.DataFrame):
    """Print summary statistics for the benchmark runs."""
    print("\nSummary Statistics:")
    print("-" * 50)
    
    # Group by GPU and calculate mean metrics with std
    gpu_stats = df.groupby('gpu_info').agg({
        'overall_throughput': ['mean', 'std'],
        'price_per_token': ['mean', 'std'],
        'ttft': ['mean', 'std']
    }).round(4)
    
    print("\nPerformance by GPU:")
    print(gpu_stats)
    
    print("\nNumber of runs by GPU:")
    print(df['gpu_info'].value_counts())

def main():
    df = load_benchmark_data()
    plot_metrics_by_gpu(df)
    print_summary_stats(df)

if __name__ == "__main__":
    main() 