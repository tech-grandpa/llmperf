#!/bin/bash

# This script runs the benchmark for the homelab instances in parallel
#
# The script is not very sophisticated, it just runs the benchmark for the homelab instances in parallel. 
# You can run it with different models and different numbers of iterations, however you need to modify the script accordingly.
# The script is designed to be run from the root of the repository. The script will create a new directory called "results" 
# and save the results there. 
#
# Especially the host of the homelab instances need to be changed in the script. Also take a look at the perfTest.sh script

export TOKENIZERS_PARALLELISM=false
export TEST_MODEL="neuralmagic/Meta-Llama-3.1-8B-Instruct-FP8"

# Number of iterations to run (default: 3)
ITERATIONS=${1:-3}

for i in $(seq 1 $ITERATIONS); do
    echo "Starting iteration $i of $ITERATIONS"
    
    # Set prefix with iteration number
    export PREFIX="homelab_parallel_iter${i}_"

    # side note: use 'env' to ensure the environment variable are passed along also in sub-process when using zsh
    # Run the script on Server 1
    env OPENAI_API_BASE="http://10.0.42.90:30000/v1" GPU_INFO="RTX 3090" ./perfTest.sh > RTX3090_iter${i}.log 2>&1 &

    # Run the script on Server 2
    env OPENAI_API_BASE="http://10.0.42.129:30000/v1" GPU_INFO="RTX A5000" ./perfTest.sh > A5000_iter${i}.log 2>&1 &

    # Run the script on Server 3
    env OPENAI_API_BASE="http://10.0.42.26:30000/v1" GPU_INFO="RTX A4000" ./perfTest.sh > A4000_iter${i}.log 2>&1 &

    # Wait for all background processes in this iteration to complete
    wait
    
    echo "Completed iteration $i of $ITERATIONS"
done

echo "All benchmark iterations for the homelab run are complete."

