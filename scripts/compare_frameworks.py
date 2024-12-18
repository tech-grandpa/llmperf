import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

def create_plots_dir():
    if not os.path.exists('plots'):
        os.makedirs('plots')

def get_gpu_order_by_fp8_ttft(df):
    """Get GPU order based on FP8 TTFT values."""
    fp8_ttft = df[df['data_type'] == 'FP8'].groupby('gpu_info')['ttft'].mean()
    return fp8_ttft.sort_values().index.tolist()

def create_comparison_plot(metric_name, df_base, df_vllm, title, ylabel, filename, gpu_order=None):
    """Create a grouped bar plot comparing frameworks."""
    plt.rcParams.update({'font.size': 16})
    plt.figure(figsize=(14, 8))
    
    if gpu_order is None:
        # Get all unique GPUs from both dataframes
        gpu_order = sorted(set(df_base['gpu_info'].unique()) | set(df_vllm['gpu_info'].unique()))
    
    width = 0.2  # Make bars slightly narrower to fit 4 bars
    x = np.arange(len(gpu_order))
    
    # Function to get data for a specific framework and data type
    def get_framework_data(df, gpu_list, data_type):
        data = []
        errors = []
        for gpu in gpu_list:
            gpu_data = df[(df['gpu_info'] == gpu) & (df['data_type'] == data_type)]
            if not gpu_data.empty:
                if metric_name == 'price_per_token':
                    value = gpu_data[metric_name].mean() * 1_000_000
                    error = gpu_data[metric_name].std() * 1_000_000 if len(gpu_data) > 1 else 0
                else:
                    value = gpu_data[metric_name].mean()
                    error = gpu_data[metric_name].std() if len(gpu_data) > 1 else 0
            else:
                value = 0
                error = 0
            data.append(value)
            errors.append(error)
        return data, errors
    
    # Plot bars for each framework and data type
    positions = [-width*1.5, -width/2, width/2, width*1.5]
    labels = ['SGLang FP8', 'SGLang BF16', 'vLLM FP8', 'vLLM BF16']
    
    data_configs = [
        (df_base, 'FP8'),    # SGLang FP8
        (df_base, 'BF16'),   # SGLang BF16
        (df_vllm, 'FP8'),    # vLLM FP8
        (df_vllm, 'BF16')    # vLLM BF16
    ]
    
    for pos, label, (df, dtype) in zip(positions, labels, data_configs):
        data, errors = get_framework_data(df, gpu_order, dtype)
        plt.bar(x + pos, data, width, label=label, yerr=errors, capsize=5)
    
    plt.xlabel('GPU', fontsize=18)
    plt.ylabel(ylabel, fontsize=18)
    plt.title(title, fontsize=20, pad=20)
    plt.xticks(x, gpu_order, rotation=45, ha='right', fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(fontsize=16)
    
    plt.tight_layout()
    plt.savefig(f'comparison_plots/{filename}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    plt.rcParams.update({'font.size': plt.rcParamsDefault['font.size']})

def compare_frameworks(db_path_base, db_path_vllm):
    """Compare metrics between SGLang and vLLM."""
    create_plots_dir()
    
    # Load data from both databases
    conn_base = sqlite3.connect(db_path_base)
    conn_vllm = sqlite3.connect(db_path_vllm)
    
    query = '''
        SELECT gpu_info, data_type, overall_throughput, ttft, 
               price_per_token, mean_latency
        FROM benchmark_runs
    '''
    
    df_base = pd.read_sql_query(query, conn_base)
    df_vllm = pd.read_sql_query(query, conn_vllm)
    
    # Print available data before filtering
    print("\nAvailable data in SGLang:")
    print(df_base.groupby(['gpu_info', 'data_type']).size())
    print("\nAvailable data in vLLM:")
    print(df_vllm.groupby(['gpu_info', 'data_type']).size())
    
    # Get GPUs that have FP8 data in both frameworks
    base_gpus = set(df_base[df_base['data_type'] == 'FP8']['gpu_info'])
    vllm_gpus = set(df_vllm[df_vllm['data_type'] == 'FP8']['gpu_info'])
    
    # Keep GPUs that have FP8 in both frameworks
    common_gpus = base_gpus & vllm_gpus
    
    # Filter dataframes to only include common GPUs
    df_base = df_base[df_base['gpu_info'].isin(common_gpus)]
    df_vllm = df_vllm[df_vllm['gpu_info'].isin(common_gpus)]
    
    # Get GPU order based on combined FP8 TTFT
    df_combined = pd.concat([
        df_base[df_base['data_type'] == 'FP8'],
        df_vllm[df_vllm['data_type'] == 'FP8']
    ])
    gpu_order = get_gpu_order_by_fp8_ttft(df_combined)
    
    print(f"\nComparing GPUs with FP8 data: {', '.join(gpu_order)}")
    
    # Create comparison plots
    metrics = [
        ('ttft', 'Time To First Token Comparison', 'Seconds', 'ttft_comparison'),
        ('overall_throughput', 'Token Generation Throughput Comparison', 'Tokens/second', 'throughput_comparison'),
        ('price_per_token', 'Price per Million Input Tokens Comparison', 'USD per Million Input Tokens', 'price_comparison')
    ]
    
    for metric, title, ylabel, filename in metrics:
        create_comparison_plot(metric, df_base, df_vllm, title, ylabel, filename, gpu_order)
    
    # Print summary statistics
    print("\nSummary Statistics:")
    for framework, df in [("SGLang", df_base), ("vLLM", df_vllm)]:
        print(f"\n{framework} Statistics:")
        for metric in ['overall_throughput', 'ttft', 'price_per_token']:
            stats = df.pivot_table(
                values=metric,
                index='gpu_info',
                columns='data_type',
                aggfunc=['mean', 'std']
            ).reindex(gpu_order)
            print(f"\n{metric}:")
            print(stats)
    
    conn_base.close()
    conn_vllm.close()

def main():
    parser = argparse.ArgumentParser(description='Compare SGLang and vLLM benchmark results')
    parser.add_argument('--base-db', type=str, default='results.db',
                       help='Path to the SGLang results database (default: results.db)')
    parser.add_argument('--vllm-db', type=str, default='results_vllm.db',
                       help='Path to the vLLM results database (default: results_vllm.db)')
    
    args = parser.parse_args()
    compare_frameworks(args.base_db, args.vllm_db)

if __name__ == "__main__":
    main() 