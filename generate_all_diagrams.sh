#!/usr/bin/env bash
#
# This script generates all diagrams and statistics from the results folder
#
# Used Models from hugging face in these scripts:
# - unsloth/Meta-Llama-3.1-8B-Instruct
# - neuralmagic/Meta-Llama-3.1-8B-Instruct-FP8 (used in most cases)
# - Qwen/Qwen2.5-Coder-14B-Instruct
# - wordslab-org/Qwen2.5-Coder-14B-Instruct-FP8-Dynamic
# - NousResearch/Hermes-3-Llama-3.2-3B
#

# Various runs with different models and quantization
#
# run against cloud and homelab instances (each at a time) with different models (large and small as well as in BF16 and FP8 quantized)
uv run python scripts/visualize_results.py --prefix various_models_mixed --db-path ./results/results_various_models_mixed.db > ./results/various_models_mixed_statistics.md
# run against cloud and homelab instances (each at a time) with one small model in different quants (BF16 and FP8)
uv run python scripts/visualize_results.py --prefix small_all --db-path ./results/results_small_all.db > ./results/small_all_statistics.md
# same as above (small_all), but removed first run in each iteration of a gpu due to bad ttft
uv run python scripts/visualize_results.py --prefix small_all_corrected --db-path ./results/results_small_all_corrected.db > ./results/small_all_corrected_statistics.md

# Single runs with only one model
#
# run against cloud instances, each at a time (no parallelism) with one small model and only FP8
uv run python scripts/visualize_results.py --prefix cloud_single --db-path ./results/results_cloud_single.db > ./results/cloud_single_statistics.md
# run against homelab instances, each at a time (no parallelism) with one small model and only FP8
uv run python scripts/visualize_results.py --prefix homelab_single --db-path ./results/results_homelab_single.db > ./results/homelab_single_statistics.md
# combined the both runs above (homelab_single + cloud_single) in one db
uv run python scripts/visualize_results.py --prefix cloud+home_single_combined --db-path ./results/results_cloud+home_single_combined.db > ./results/cloud+home_single_combined_statistics.md
# same as above (cloud+home_single_combined), but removed first run of the A5000 due to bad ttft
uv run python scripts/visualize_results.py --prefix cloud+home_single_combined_corrected --db-path ./results/results_cloud+home_single_combined_corrected.db > ./results/cloud+home_single_combined_corrected_statistics.md
# time passed and the parallel test started, however now the old single run showed the new ones differ regarding performance :-/
uv run python scripts/visualize_results.py --prefix results_homelab_single+old_single --db-path ./results/results_homelab_single+old_single.db > ./results/results_homelab_single+old_single.md



# Parallel runs start here 
#
# run against cloud instances in parallel within the test script with one small model and only FP8
uv run python scripts/visualize_results.py --prefix cloud_parallel --db-path ./results/results_cloud_parallel.db > ./results/cloud_parallel_statistics.md
# combine the cloud_parallel and cloud_single data to see the performance gap -> there shouldn't be any
uv run python scripts/visualize_results.py --prefix cloud_parallel+single --db-path ./results/results_cloud_parallel+single.db > ./results/cloud_parallel+single_statistics.md
# run against a single homelab machine (running multiple model instances on various gpus with each one small model and only FP8) in parallel within the test script 
uv run python scripts/visualize_results.py --prefix homelab_parallel --db-path ./results/results_homelab_parallel.db > ./results/homelab_parallel_statistics.md
# combine the cloud_parallel and cloud_single data to see the performance gap -> there shouldn't be any
uv run python scripts/visualize_results.py --prefix homelab_parallel+single --db-path ./results/results_homelab_single+parallel_combined.db > ./results/homelab_single+parallel_combined.md
