import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def create_plots_dir():
    if not os.path.exists('plots'):
        os.makedirs('plots')

def create_grouped_bar_plot(metric_name, df, title, ylabel, filename):
    """Create a grouped bar plot with error bars."""
    # Get unique GPUs and data types
    gpus = df['gpu_info'].unique()
    data_types = sorted(df['data_type'].unique())  # Sort to ensure consistent ordering
    
    # Set up the plot
    plt.figure(figsize=(10, 6))
    width = 0.35  # Width of bars
    x = np.arange(len(gpus))
    
    # Create bars for each data type
    for i, dtype in enumerate(data_types):
        # Get data for this type, maintaining GPU order
        data = []
        errors = []
        for gpu in gpus:
            gpu_data = df[(df['gpu_info'] == gpu) & (df['data_type'] == dtype)]
            if not gpu_data.empty:
                data.append(gpu_data[metric_name].mean())
                errors.append(gpu_data[metric_name].std())
            else:
                data.append(0)
                errors.append(0)
        
        plt.bar(x + i*width - width/2, 
               data,
               width,
               label=dtype,
               yerr=errors,
               capsize=5)
    
    plt.xlabel('GPU')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(x, gpus, rotation=45)
    plt.legend()
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(f'plots/{filename}.png')
    plt.close()

def plot_metrics_by_gpu(df):
    """Create various performance metric plots."""
    create_plots_dir()
    
    # Plot overall throughput
    create_grouped_bar_plot('overall_throughput', 
                          df,
                          'Token Generation Throughput by GPU and Data Type',
                          'Tokens/second',
                          'overall_throughput_by_gpu')
    
    # Plot TTFT (Time To First Token)
    create_grouped_bar_plot('ttft',
                          df,
                          'Time To First Token by GPU and Data Type',
                          'Seconds',
                          'ttft_by_gpu')
    
    # Plot price per token
    create_grouped_bar_plot('price_per_token',
                          df,
                          'Price per Token by GPU and Data Type',
                          'USD per Token',
                          'price_per_token_by_gpu')

def print_summary_stats(df):
    """Print summary statistics for the benchmark results."""
    print("\nSummary Statistics:")
    print("\nAverage Throughput by GPU and Data Type:")
    print(df.groupby(['gpu_info', 'data_type'])['overall_throughput'].mean())
    
    print("\nAverage TTFT by GPU and Data Type:")
    print(df.groupby(['gpu_info', 'data_type'])['ttft'].mean())
    
    print("\nAverage Price per Token by GPU and Data Type:")
    print(df.groupby(['gpu_info', 'data_type'])['price_per_token'].mean())

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