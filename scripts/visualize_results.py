import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def create_plots_dir():
    if not os.path.exists('plots'):
        os.makedirs('plots')

def get_gpu_order_by_fp8_ttft(df):
    """Get GPU order based on FP8 TTFT values."""
    fp8_ttft = df[df['data_type'] == 'FP8'].groupby('gpu_info')['ttft'].mean()
    return fp8_ttft.sort_values().index.tolist()

def create_grouped_bar_plot(metric_name, df, title, ylabel, filename, gpu_order):
    """Create a grouped bar plot with error bars."""
    # Get unique data types
    data_types = sorted(df['data_type'].unique())
    
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
    
    # Save the plot with high DPI
    plt.savefig(f'plots/{filename}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Reset font size for subsequent plots
    plt.rcParams.update({'font.size': plt.rcParamsDefault['font.size']})

def plot_metrics_by_gpu(df):
    """Create various performance metric plots."""
    create_plots_dir()
    
    # Get GPU order based on FP8 TTFT
    gpu_order = get_gpu_order_by_fp8_ttft(df)
    print("\nGPU order based on FP8 TTFT:")
    for i, gpu in enumerate(gpu_order, 1):
        fp8_ttft = df[(df['data_type'] == 'FP8') & (df['gpu_info'] == gpu)]['ttft'].mean()
        print(f"{i}. {gpu}: {fp8_ttft:.3f}s")
    
    # Plot metrics using consistent GPU order
    create_grouped_bar_plot('ttft',
                          df,
                          'Time To First Token by GPU and Data Type',
                          'Seconds',
                          'ttft_by_gpu',
                          gpu_order)
    
    create_grouped_bar_plot('overall_throughput', 
                          df,
                          'Token Generation Throughput by GPU and Data Type',
                          'Tokens/second',
                          'overall_throughput_by_gpu',
                          gpu_order)
    
    create_grouped_bar_plot('price_per_token',
                          df,
                          'Price per million input Tokens by GPU and Data Type',
                          'USD per million input Tokens',
                          'price_per_token_by_gpu',
                          gpu_order)

def print_summary_stats(df):
    """Print summary statistics for the benchmark results."""
    print("\nSummary Statistics:")
    
    # Get GPU order for consistent presentation
    gpu_order = get_gpu_order_by_fp8_ttft(df)
    
    metrics = {
        'Throughput': 'overall_throughput',
        'TTFT': 'ttft',
        'Price per Token': 'price_per_token'
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

def main():
    # Connect to database
    conn = sqlite3.connect('results.db')
    
    # Load data
    df = pd.read_sql_query('''
        SELECT gpu_info, data_type, overall_throughput, ttft, 
               price_per_token, mean_latency
        FROM benchmark_runs
    ''', conn)
    
    # Generate plots
    plot_metrics_by_gpu(df)
    
    # Print summary statistics
    print_summary_stats(df)
    
    conn.close()

if __name__ == "__main__":
    main() 