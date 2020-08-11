import numpy as np
import pandas as pd
import re
import os
import glob
import sys

output_dir = './resultCSVs/'


def concat_additional_information(output_dir,base_path,float_format_decimals,physical_cores):
    processed_cpu_demand_file =output_dir + 'results-4' + base_path.replace('.','').replace('/','-') + 'CpuDemand.csv'
    final_output_file = processed_cpu_demand_file
 

    df_cpu = pd.read_csv(processed_cpu_demand_file, sep=',', header=0)
    df_cpu.insert(len(df_cpu.columns),'Physical-Cores',value=physical_cores)
    

    

    df_cpu.to_csv(processed_cpu_demand_file,float_format=float_format_decimals, index=False)

    print("Step 6 concat addtional information finished")