import numpy as np
import pandas as pd
import re
import os
import glob
import sys

# final_output_file = 'results80CorePreProcessedPerf.csv'
base_path = '../80Cores/repetitions100/'
exp_duration_file = 'results-2'+ base_path.replace('.','').replace('/','-') + 'ExpDuration.csv'
processed_perf_file = 'results-3' + base_path.replace('.','').replace('/','-') + 'ProcessedPerf.csv'
final_output_file = 'results-4' + base_path.replace('.','').replace('/','-') + 'CpuDemand.csv'
# perf_file_base_name = 'perfOutput'
csv_file_ending = '.csv'
df_array = []

core_l1_bandwidth = -1
l1_l2_bandwidth = -1
l2_l3_bandwidth = -1
l3_dram_bandwidth =-1
# 1. evaluate input args as latencies
if len(sys.argv) < 5:
    print('No latency was specified. Set them to -1')
else:
    core_l1_bandwidth = float(sys.argv[1])
    l1_l2_bandwidth = float(sys.argv[2])
    l2_l3_bandwidth = float(sys.argv[3])
    l3_dram_bandwidth = float(sys.argv[4])
    print('Bandwidth',sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4] )

# 2. add latency columns
df = pd.read_csv(processed_perf_file, sep=',', header=0)

df.insert(len(df.columns),'Core-L1-Bandwidth',value=core_l1_bandwidth)
df.insert(len(df.columns),'L1-L2-Bandwidth',value=l1_l2_bandwidth)
df.insert(len(df.columns),'L2-L3-Bandwidth',value=l2_l3_bandwidth)
df.insert(len(df.columns),'L3-DRAM-Bandwidth',value=l3_dram_bandwidth)

# 3. get mean exp duration of the 1 Thread run and add to our data frame

df_exp_duration = pd.read_csv(exp_duration_file, sep=',', header=0)
# add exception if row with 1 thread or mean is not found ?
mean_single_thread_run_series = df_exp_duration.loc[df_exp_duration['Threads'] == 1,'Mean']
mean_single_thread_run = mean_single_thread_run_series[0]
df.insert(len(df.columns),'Mean-Runtime-1-Thread-With-Memory-Hierarchy',value=mean_single_thread_run)

# add exception if row with 1 thread or mena is not found ?

print(mean_single_thread_run_series[0])
# 4.calculate single thread run
# core_l1_write_time = #TODO
# l1_l2_write_time = 
# l2_l3_write_time = 
# l3_dram_write_time = 

row_single_thread = df.loc[df['Threads'] == 1]
print(row_single_thread['L1-dcache-load'][0].dtype)
core_l1_read_time = (float(row_single_thread['L1-dcache-load'][0])*4) / float(row_single_thread['Core-L1-Bandwidth'][0])
l1_l2_read_time = (float(row_single_thread['L2-dcache-load'][0])*4) / float(row_single_thread['L1-L2-Bandwidth'][0])
l2_l3_read_time = (float(row_single_thread['LLC-load'][0])*4) / float(row_single_thread['L2-L3-Bandwidth'][0])
l3_dram_read_time = (float(row_single_thread['LLC-load-misses'][0])*4) / float(row_single_thread['L3-DRAM-Bandwidth'][0])

#todo add time columns ?
# df.insert(len(df.columns),'Last',value=core_l1_read_time)
print(core_l1_read_time)
print(l1_l2_read_time)
print(l2_l3_read_time)
print(l3_dram_read_time)

mean_single_thread_run_without_mem_hierarchy = mean_single_thread_run - core_l1_read_time - l1_l2_read_time - l2_l3_read_time -l3_dram_read_time
print('CPU-Without-MemoryHierarchy', mean_single_thread_run_without_mem_hierarchy)
df.insert(len(df.columns),'Mean-Runtime-1-Thread-WithOUT-Memory-Hierarchy',value=mean_single_thread_run_without_mem_hierarchy)


## Threads,L1-dcache-store,L1-dcache-store-misses,LLC-store,LLC-store-misses,L1-dcache-load,L1-dcache-load-misses,LLC-load,LLC-load-misses
# print(df.info())
df.to_csv(final_output_file,float_format='%.4f', index=False)

print("Step 4 evaluate cpu demand without memory hierarchy finished")