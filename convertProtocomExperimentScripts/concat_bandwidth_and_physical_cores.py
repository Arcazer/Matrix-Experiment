import numpy as np
import pandas as pd
import re
import os
import glob
import sys


# Header names of target csv that are used for matrix experiment
# Threads,L1-dcache-store,L1-dcache-store-misses,L2-dcache-store,L2-dcache-store-misses,LLC-store,LLC-store-misses,L1-dcache-load,L1-dcache-load-misses,L2-dcache-load,L2-dcache-load-misses,LLC-load,LLC-load-misses,L1-W-Hit,L2-W-Hit,L3-W-Hit,L1-R-Hit,L2-R-Hit,L3-R-Hit,Core-L1-Bandwidth,L1-L2-Bandwidth,L2-L3-Bandwidth,L3-DRAM-Bandwidth,L3-DRAM-Bandwidth-Scaling,Mean-Runtime-1-Thread-With-Memory-Hierarchy,Mean-Runtime-1-Thread-Without-Memory-Hierarchy,Mean-Runtime-1-Thread-Without-Memory-Hierarchy-Cache-Line,Physical-Cores

def concat(df,cache_line_size,core_l1_bandwidth,l1_l2_bandwidth,l2_l3_bandwidth,l3_dram_bandwidth,stream_scaling_dram_path,physical_cores):
    df.insert(len(df.columns),'Core-L1-Bandwidth',value=core_l1_bandwidth)
    df.insert(len(df.columns),'L1-L2-Bandwidth',value=l1_l2_bandwidth)
    df.insert(len(df.columns),'L2-L3-Bandwidth',value=l2_l3_bandwidth)
    df.insert(len(df.columns),'L3-DRAM-Bandwidth',value=l3_dram_bandwidth)
    
      # 3.2.1 get single thread row and calculate cpu demand without memory hierarchy - READ
    row_single_thread = df.loc[df['Threads'] == 1]
    # core_l1_read_time = (float(row_single_thread['L1-dcache-load'][0])*4) / float(row_single_thread['Core-L1-Bandwidth'][0])
    # l1_l2_read_time = (float(row_single_thread['L2-dcache-load'][0])*4) / float(row_single_thread['L1-L2-Bandwidth'][0])
    l2_l3_read_time = (float(row_single_thread['LLC-load'][0])*4) / float(row_single_thread['L2-L3-Bandwidth'][0])
    l3_dram_read_time = (float(row_single_thread['LLC-load-misses'][0])*4) / float(row_single_thread['L3-DRAM-Bandwidth'][0])
    
    # 3.2.1 get single thread row and calculate cpu demand without memory hierarchy and cache line size - READ
    # core_l1_read_time_cache_line = (float(row_single_thread['L1-dcache-load'][0])*4) / float(row_single_thread['Core-L1-Bandwidth'][0])
    # l1_l2_read_time_cache_line = (float(row_single_thread['L2-dcache-load'][0])*cache_line_size) / float(row_single_thread['L1-L2-Bandwidth'][0])
    l2_l3_read_time_cache_line = (float(row_single_thread['LLC-load'][0])*cache_line_size) / float(row_single_thread['L2-L3-Bandwidth'][0])
    l3_dram_read_time_cache_line = (float(row_single_thread['LLC-load-misses'][0])*cache_line_size) / float(row_single_thread['L3-DRAM-Bandwidth'][0])

    # get mean runtime from L3 seems to be correct
    mean_single_thread_run_series = df.loc[df['Threads'] == 1,'Mean-Runtime-1-Thread-With-Memory-Hierarchy-L3']
    mean_single_thread_run = mean_single_thread_run_series[0]
    df.insert(len(df.columns),'Mean-Runtime-1-Thread-With-Memory-Hierarchy',value=mean_single_thread_run)
    
    # 4. calcuate single run time without memory hierarchy and append it to csv
    mean_single_thread_run_without_mem_hierarchy = mean_single_thread_run -  l2_l3_read_time - l3_dram_read_time
    mean_single_thread_run_without_mem_hierarchy_cache_line = mean_single_thread_run - l2_l3_read_time_cache_line -l3_dram_read_time_cache_line
    print('-- Single-CPU-With-MemoryHierarchy', mean_single_thread_run)
    print('-- l2-l3-read-time: ',l2_l3_read_time, ', l2-l3-read-time-cache-line: ',l2_l3_read_time_cache_line)
    print('-- l3-dram-read-time: ',l3_dram_read_time, ', l3-dram-read-time-cache-line: ',l3_dram_read_time_cache_line)
    print('-- Single-CPU-Without-Memory-Hierarchy', mean_single_thread_run_without_mem_hierarchy)
    print('-- Single-CPU-Without-Memory-Hierarchy-Cache-Line', mean_single_thread_run_without_mem_hierarchy_cache_line)
    df.insert(len(df.columns),'Mean-Runtime-1-Thread-Without-Memory-Hierarchy',value=mean_single_thread_run_without_mem_hierarchy)
    df.insert(len(df.columns),'Mean-Runtime-1-Thread-Without-Memory-Hierarchy-Cache-Line',value=mean_single_thread_run_without_mem_hierarchy_cache_line)
    
    
    # Add scaling bandwidth
    df_stream_bandwidth = pd.read_csv(stream_scaling_dram_path, sep=',', header=0)     
    #2. replace all l3-dram bandwidh except the value for single core. This should still use the values(Memtest) inserted in the call_py.script
    original_single_l3_dram_bandwidth = df['L3-DRAM-Bandwidth'].iloc[0]
    df.insert(len(df.columns)-3,'L3-DRAM-Bandwidth-Scaling',value=df_stream_bandwidth['STREAM-COPY'])
    df.loc[0,'L3-DRAM-Bandwidth-Scaling']=original_single_l3_dram_bandwidth
    
    #concat physical_cores
    df.insert(len(df.columns),'Physical-Cores',value=physical_cores)
    
    return df