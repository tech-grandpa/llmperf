#!/bin/bash

# This script runs the benchmark for a single instance
# The script does not allow to provide all arguments, it is designed to be used with the \
# benchmark_parallel_cloud.sh and benchmark_parallel_homelab.sh scripts which provide the 
# necessary arguments.

# Tweak the static parameters here as needed and modify the script accordingly if needed. 

uv run python token_benchmark_ray.py \
--model "${TEST_MODEL}" \
--gpu-info "${GPU_INFO}" \
--price-per-hour 0.01 \
--db-path "results.db" \
--results-dir "${PREFIX}result_outputs" \
--mean-input-tokens 550 \
--stddev-input-tokens 150 \
--mean-output-tokens 150 \
--stddev-output-tokens 10 \
--max-num-completed-requests 64 \
--timeout 600 \
--num-concurrent-requests 64 \
--metadata precision=FP8

