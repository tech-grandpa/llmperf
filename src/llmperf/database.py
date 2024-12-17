import sqlite3
from datetime import datetime
from typing import Dict, Any
import json
import numpy as np
from llmperf import common_metrics

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

class ResultsDB:
    def __init__(self, db_path: str = "llmperf_results.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Create benchmark_runs table
        c.execute('''
            CREATE TABLE IF NOT EXISTS benchmark_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                model TEXT,
                gpu_info TEXT,
                price_per_hour REAL,
                mean_input_tokens INTEGER,
                mean_output_tokens INTEGER,
                num_concurrent_requests INTEGER,
                overall_throughput REAL,
                error_rate REAL,
                completed_requests INTEGER,
                completed_requests_per_min REAL,
                mean_latency REAL,
                p99_latency REAL,
                price_per_token REAL,
                ttft REAL,
                raw_results TEXT,
                metadata TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def save_results(self, summary: Dict[str, Any], gpu_info: str, price_per_hour: float):
        """Save benchmark results to the database."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        results = summary.get('results', {})
        
        # Get e2e latency and TTFT metrics
        e2e_latency = results.get(common_metrics.E2E_LAT, {})
        ttft = results.get(common_metrics.TTFT, {}).get('mean') if results.get(common_metrics.TTFT) else None
        mean_latency = e2e_latency.get('mean') if e2e_latency else None
        p99_latency = (e2e_latency.get('quantiles', {}).get('p99') if e2e_latency else None)

        # Get throughput metrics
        output_throughput = float(results.get(common_metrics.OUTPUT_THROUGHPUT) or 
                                results.get(common_metrics.REQ_OUTPUT_THROUGHPUT) or 
                                0.0)
        
        # Calculate price per token
        # price_per_second = price_per_hour / 3600
        # price_per_token = price_per_second / output_throughput if output_throughput else 0
        tokens_per_hour = output_throughput * 3600 if output_throughput else 0
        price_per_token = price_per_hour / tokens_per_hour if tokens_per_hour else 0
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'model': summary.get('model'),
            'gpu_info': gpu_info,
            'price_per_hour': price_per_hour,
            'mean_input_tokens': summary.get('mean_input_tokens'),
            'mean_output_tokens': summary.get('mean_output_tokens'),
            'num_concurrent_requests': summary.get('num_concurrent_requests'),
            'overall_throughput': output_throughput,
            'error_rate': results.get(common_metrics.ERROR_RATE, 0.0),
            'completed_requests': results.get(common_metrics.NUM_COMPLETED_REQUESTS, 0),
            'completed_requests_per_min': results.get(common_metrics.COMPLETED_REQUESTS_PER_MIN, 0.0),
            'mean_latency': mean_latency,
            'p99_latency': p99_latency,
            'price_per_token': price_per_token,
            'ttft': ttft,
            'raw_results': json.dumps(summary, cls=NumpyEncoder),
            'metadata': json.dumps(summary.get('metadata', {}), cls=NumpyEncoder)
        }

        # Insert into database
        fields = ', '.join(data.keys())
        placeholders = ', '.join([f':{k}' for k in data.keys()])
        c.execute(f'INSERT INTO benchmark_runs ({fields}) VALUES ({placeholders})', data)

        conn.commit()
        conn.close() 