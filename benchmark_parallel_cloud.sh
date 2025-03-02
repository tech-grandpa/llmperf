#!/bin/bash

# This script runs the benchmark for the cloud instances in parallel
#
# The script is not very sophisticated, it just runs the benchmark for the cloud instances in parallel. 
# You can run it with different models and different numbers of iterations, however you need to modify the script accordingly.
# The script is designed to be run from the root of the repository. The script will create a new directory called "results" 
# and save the results there. 
#
# Especially the host names of the cloud instances need to be changed in the script. Also take a look at the perfTest.sh script


export OPENAI_API_KEY=EMPTY
export TOKENIZERS_PARALLELISM=false
export TEST_MODEL="neuralmagic/Meta-Llama-3.1-8B-Instruct-FP8"

# Number of iterations to run (default: 3)
ITERATIONS=${1:-3}

for i in $(seq 1 $ITERATIONS); do
    echo "Starting iteration $i of $ITERATIONS"
    
    # Set prefix with iteration number
    export PREFIX="cloud_parallel_iter${i}_"

    ## Run pod instances

    # 3090
    env OPENAI_API_BASE="https://ixjeofi583r088-8000.proxy.runpod.net/v1" GPU_INFO="runpod_RTX_3090" ./perfTest.sh > RTX3090_runpod_iter${i}.log 2>&1 &

    # 2x 3090
    # env OPENAI_API_BASE="https://ixjeofi583r088-8000.proxy.runpod.net/v1" GPU_INFO="runpod_RTX_3090_2x" ./perfTest.sh > RTX3090_2x_runpod_iter${i}.log 2>&1 &

    # A 4000
    env OPENAI_API_BASE="https://9pjwcuml42taea-8000.proxy.runpod.net/v1" GPU_INFO="runpod_RTX_A4000" ./perfTest.sh > A4000_runpod_iter${i}.log 2>&1 &

    # A 5000
    env OPENAI_API_BASE="https://bojunq7gtawalz-8000.proxy.runpod.net/v1" GPU_INFO="runpod_RTX_A5000" ./perfTest.sh > A5000_runpod_iter${i}.log 2>&1 &

    # A 6000
    # env OPENAI_API_BASE="https://6fs3pje7ra0skj-8000.proxy.runpod.net/v1" GPU_INFO="runpod_RTX_A6000" ./perfTest.sh > A6000_runpod_iter${i}.log 2>&1 &

    # A 6000 ADA
    # env OPENAI_API_BASE="https://tfulssad4wafj9-8000.proxy.runpod.net/v1" GPU_INFO="runpod_RTX_A6000_ADA" ./perfTest.sh > A6000ada_runpod_iter${i}.log 2>&1 &

    # Wait for all background processes in this iteration to complete
    wait
    
    echo "Completed iteration $i of $ITERATIONS"
done

echo "All benchmark iterations for the cloud run are complete."

