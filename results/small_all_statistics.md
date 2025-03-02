
GPU order based on FP8 TTFT:
1. RTX A5000: 0.054s
2. RTX 3090: 0.403s
3. (runpod) RTX A6000 Ada: 0.461s
4. (runpod) RTX 3090: 0.470s
5. RTX A4000: 0.951s
6. (runpod) RTX A6000: 1.253s

Summary Statistics:

Average Throughput by GPU and Data Type:
data_type                     BF16         FP8
gpu_info                                      
RTX A5000               663.843187  904.539565
RTX 3090                709.034247  893.169908
(runpod) RTX A6000 Ada  778.598340  992.749314
(runpod) RTX 3090       683.751612  871.750636
RTX A4000                      NaN  598.583144
(runpod) RTX A6000      661.627592  627.307412

Average TTFT by GPU and Data Type:
data_type                   BF16       FP8
gpu_info                                  
RTX A5000               0.136458  0.053724
RTX 3090                0.224001  0.402754
(runpod) RTX A6000 Ada  0.514782  0.460927
(runpod) RTX 3090       0.373910  0.470498
RTX A4000                    NaN  0.950744
(runpod) RTX A6000      0.469187  1.253001

Average Price per Token by GPU and Data Type:
data_type                       BF16           FP8
gpu_info                                          
RTX A5000               4.913648e-08  3.601413e-08
RTX 3090                4.600809e-08  3.712837e-08
(runpod) RTX A6000 Ada  4.191889e-08  3.285206e-08
(runpod) RTX 3090       4.774467e-08  3.790155e-08
RTX A4000                        NaN  5.533548e-08
(runpod) RTX A6000      4.928118e-08  6.288164e-08

Average Token per Second by GPU and Data Type:
data_type                    BF16        FP8
gpu_info                                    
RTX A5000               27.682178  48.229000
RTX 3090                30.507998  45.270735
(runpod) RTX A6000 Ada  34.390695  50.074445
(runpod) RTX 3090       29.340104  41.513326
RTX A4000                     NaN  23.900866
(runpod) RTX A6000      27.422731  31.057517
