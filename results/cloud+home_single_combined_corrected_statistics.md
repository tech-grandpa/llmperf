
GPU order based on FP8 TTFT:
1. RTX A5000: 0.056s
2. RTX 3090: 0.063s
3. RTX A4000: 0.077s
4. (runpod) RTX A5000: 0.174s
5. (runpod) RTX 3090: 0.213s
6. (runpod) RTX A4000: 0.230s
7. (runpod) RTX A6000: 0.509s
8. (runpod) RTX A6000 ADA: 0.646s

Summary Statistics:

Average Throughput by GPU and Data Type:
data_type                       FP8
gpu_info                           
RTX A5000               1117.717778
RTX 3090                1219.761272
RTX A4000                803.163151
(runpod) RTX A5000      1069.406865
(runpod) RTX 3090       1088.507470
(runpod) RTX A4000       783.211167
(runpod) RTX A6000      1148.873590
(runpod) RTX A6000 ADA  1339.841260

Average TTFT by GPU and Data Type:
data_type                    FP8
gpu_info                        
RTX A5000               0.056271
RTX 3090                0.062853
RTX A4000               0.077229
(runpod) RTX A5000      0.173997
(runpod) RTX 3090       0.212707
(runpod) RTX A4000      0.230110
(runpod) RTX A6000      0.508715
(runpod) RTX A6000 ADA  0.645700

Average Price per Token by GPU and Data Type:
data_type                        FP8
gpu_info                            
RTX A5000               6.778714e-10
RTX 3090                6.211143e-10
RTX A4000               9.432560e-10
(runpod) RTX A5000      7.085326e-10
(runpod) RTX 3090       6.960620e-10
(runpod) RTX A4000      9.673973e-10
(runpod) RTX A6000      6.595032e-10
(runpod) RTX A6000 ADA  5.655961e-10

Average Token per Second by GPU and Data Type:
data_type                     FP8
gpu_info                         
RTX A5000               41.993347
RTX 3090                46.405024
RTX A4000               29.184001
(runpod) RTX A5000      40.123852
(runpod) RTX 3090       41.053701
(runpod) RTX A4000      28.479648
(runpod) RTX A6000      43.405033
(runpod) RTX A6000 ADA  51.598746
