
GPU order based on FP8 TTFT:
1. RTX 3090: 0.052s
2. RTX A5000: 0.054s
3. RTX A4000: 0.080s
4. (runpod) RTX 3090: 0.160s
5. (runpod) RTX A6000: 0.361s
6. (runpod) RTX A6000 Ada: 0.445s

Summary Statistics:

Average Throughput by GPU and Data Type:
data_type                     BF16          FP8
gpu_info                                       
RTX 3090                725.658680   973.071248
RTX A5000               680.434282   906.812645
RTX A4000                      NaN   650.544572
(runpod) RTX 3090       705.710029   941.857958
(runpod) RTX A6000      675.038595   677.279391
(runpod) RTX A6000 Ada  802.219533  1016.453067

Average TTFT by GPU and Data Type:
data_type                   BF16       FP8
gpu_info                                  
RTX 3090                0.071104  0.051613
RTX A5000               0.079568  0.053621
RTX A4000                    NaN  0.080250
(runpod) RTX 3090       0.179345  0.159933
(runpod) RTX A6000      0.416368  0.361002
(runpod) RTX A6000 Ada  0.471486  0.445083

Average Price per Token by GPU and Data Type:
data_type                       BF16           FP8
gpu_info                                          
RTX 3090                4.489130e-08  3.348284e-08
RTX A5000               4.787804e-08  3.592341e-08
RTX A4000                        NaN  5.007582e-08
(runpod) RTX 3090       4.616062e-08  3.458701e-08
(runpod) RTX A6000      4.826372e-08  5.616325e-08
(runpod) RTX A6000 Ada  4.060753e-08  3.204847e-08

Average Token per Second by GPU and Data Type:
data_type                    BF16        FP8
gpu_info                                    
RTX 3090                33.290098  56.296055
RTX A5000               30.391613  48.315925
RTX A4000                     NaN  28.801071
(runpod) RTX 3090       33.205843  50.500663
(runpod) RTX A6000      29.511456  37.346855
(runpod) RTX A6000 Ada  37.614885  53.502662
