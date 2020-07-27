import numpy as np
import pandas as pd
import re
import os
import glob
import sys

output_dir = './resultCSVs/'


def concat_scaling_l3_dram_bandwidth(output_dir,base_path,float_format_decimals,stream_scaling_dram_path):
    processed_cpu_demand_file =output_dir + 'results-4' + base_path.replace('.','').replace('/','-') + 'CpuDemand.csv'
    final_output_file =output_dir + 'results-5' + base_path.replace('.','').replace('/','-') + 'CpuDemandWithScalingDram.csv'
 
    #1. parse cpuDemandFile that contain all necessary data to do a simulation
    # and parse stream benchmark that was meassured for multiple cores
    df_cpu = pd.read_csv(processed_cpu_demand_file, sep=',', header=0)
    df_stream_bandwidth = pd.read_csv(stream_scaling_dram_path, sep=',', header=0)
       
    #2. replace all l3-dram bandwidh except the value for single core. This should still use the values(Memtest) inserted in the call_py.script
    original_single_l3_dram_bandwidth = df_cpu['L3-DRAM-Bandwidth'].iloc[0]
    df_cpu['L3-DRAM-Bandwidth'] = df_stream_bandwidth['STREAM-COPY']
    df_cpu.loc[0,'L3-DRAM-Bandwidth']=original_single_l3_dram_bandwidth

    

    df_cpu.to_csv(final_output_file,float_format=float_format_decimals, index=False)

    print("Step 5 concat scaling dram bandwidth finished")