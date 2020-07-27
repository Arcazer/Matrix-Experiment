import numpy as np
import pandas as pd
import re
import os
import glob
import sys

output_dir = './resultCSVs/'
csv_file_ending = '.csv'
df_array = []

def evaluate_cpu_demand(output_dir,base_path, core_l1_bandwidth, l1_l2_bandwidth, l2_l3_bandwidth, l3_dram_bandwidth,float_format_decimals,cache_line_size):
    exp_duration_file = output_dir + 'results-2'+ base_path.replace('.','').replace('/','-') + 'ExpDuration.csv'
    processed_perf_file = output_dir + 'results-3' + base_path.replace('.','').replace('/','-') + 'ProcessedPerf.csv'
    final_output_file =output_dir + 'results-4' + base_path.replace('.','').replace('/','-') + 'CpuDemand.csv'
 

    # 1. add bandwidth columns
    df = pd.read_csv(processed_perf_file, sep=',', header=0)

    df.insert(len(df.columns),'Core-L1-Bandwidth',value=core_l1_bandwidth)
    df.insert(len(df.columns),'L1-L2-Bandwidth',value=l1_l2_bandwidth)
    df.insert(len(df.columns),'L2-L3-Bandwidth',value=l2_l3_bandwidth)
    df.insert(len(df.columns),'L3-DRAM-Bandwidth',value=l3_dram_bandwidth)

    # 2. get mean exp duration of the 1 Thread run and add to our data frame
    df_exp_duration = pd.read_csv(exp_duration_file, sep=',', header=0)
    # TODO add exception if row with 1 thread or mean is not found ?
    mean_single_thread_run_series = df_exp_duration.loc[df_exp_duration['Threads'] == 1,'Mean']
    mean_single_thread_run = mean_single_thread_run_series[0]
    df.insert(len(df.columns),'Mean-Runtime-1-Thread-With-Memory-Hierarchy',value=mean_single_thread_run)


    # 3.1.calculate single thread run - WRITE TODO
    # core_l1_write_time = 
    # l1_l2_write_time = 
    # l2_l3_write_time = 
    # l3_dram_write_time = 

    # 3.2.1 get single thread row and calculate cpu demand without memory hierarchy - READ
    row_single_thread = df.loc[df['Threads'] == 1]
    core_l1_read_time = (float(row_single_thread['L1-dcache-load'][0])*4) / float(row_single_thread['Core-L1-Bandwidth'][0])
    l1_l2_read_time = (float(row_single_thread['L2-dcache-load'][0])*4) / float(row_single_thread['L1-L2-Bandwidth'][0])
    l2_l3_read_time = (float(row_single_thread['LLC-load'][0])*4) / float(row_single_thread['L2-L3-Bandwidth'][0])
    l3_dram_read_time = (float(row_single_thread['LLC-load-misses'][0])*4) / float(row_single_thread['L3-DRAM-Bandwidth'][0])
    
    # 3.2.1 get single thread row and calculate cpu demand without memory hierarchy and cache line size - READ
    core_l1_read_time_cache_line = (float(row_single_thread['L1-dcache-load'][0])*4) / float(row_single_thread['Core-L1-Bandwidth'][0])
    l1_l2_read_time_cache_line = (float(row_single_thread['L2-dcache-load'][0])*cache_line_size) / float(row_single_thread['L1-L2-Bandwidth'][0])
    l2_l3_read_time_cache_line = (float(row_single_thread['LLC-load'][0])*cache_line_size) / float(row_single_thread['L2-L3-Bandwidth'][0])
    l3_dram_read_time_cache_line = (float(row_single_thread['LLC-load-misses'][0])*cache_line_size) / float(row_single_thread['L3-DRAM-Bandwidth'][0])

    #TODO add time columns ?
    # df.insert(len(df.columns),'Last',value=core_l1_read_time)

    # 4. calcuate single run time without memory hierarchy and append it to csv
    mean_single_thread_run_without_mem_hierarchy = mean_single_thread_run - core_l1_read_time - l1_l2_read_time - l2_l3_read_time -l3_dram_read_time
    mean_single_thread_run_without_mem_hierarchy_cache_line = mean_single_thread_run - core_l1_read_time_cache_line - l1_l2_read_time_cache_line - l2_l3_read_time_cache_line -l3_dram_read_time_cache_line
    print('-- Single-CPU-With-MemoryHierarchy', mean_single_thread_run)
    print('-- core-1-read-time: ',core_l1_read_time,', core-1-read-time-cache-line: ',core_l1_read_time_cache_line)
    print('-- l1-l2-read-time: ',l1_l2_read_time, ', l1-l2-read-time-cache-line: ',l1_l2_read_time_cache_line)
    print('-- l2-l3-read-time: ',l2_l3_read_time, ', l2-l3-read-time-cache-line: ',l2_l3_read_time_cache_line)
    print('-- l3-dram-read-time: ',l3_dram_read_time, ', l3-dram-read-time-cache-line: ',l3_dram_read_time_cache_line)
    print('-- Single-CPU-Without-Memory-Hierarchy', mean_single_thread_run_without_mem_hierarchy)
    print('-- Single-CPU-Without-Memory-Hierarchy-Cache-Line', mean_single_thread_run_without_mem_hierarchy_cache_line)
    df.insert(len(df.columns),'Mean-Runtime-1-Thread-Without-Memory-Hierarchy',value=mean_single_thread_run_without_mem_hierarchy)
    df.insert(len(df.columns),'Mean-Runtime-1-Thread-Without-Memory-Hierarchy-Cache-Line',value=mean_single_thread_run_without_mem_hierarchy_cache_line)
    


    ## Threads,L1-dcache-store,L1-dcache-store-misses,LLC-store,LLC-store-misses,L1-dcache-load,L1-dcache-load-misses,LLC-load,LLC-load-misses

    df.to_csv(final_output_file,float_format=float_format_decimals, index=False)

    print("Step 4 evaluate cpu demand without memory hierarchy finished")