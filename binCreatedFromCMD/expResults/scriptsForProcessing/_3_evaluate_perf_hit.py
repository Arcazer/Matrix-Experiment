import numpy as np
import pandas as pd
import re
import os
import glob

# output_dir = './resultCSVs/'
perf_file_base_name = 'perfOutput'
csv_file_ending = '.csv'

def evaluate_perf_hit(output_dir,base_path):
    # base_path = base_path_arg
    pre_processed_perf_file = output_dir + 'results-1' + base_path.replace('.','').replace('/','-') + 'PreProcessedPerf.csv'
    final_output_file = output_dir + 'results-3' + base_path.replace('.','').replace('/','-') + 'ProcessedPerf.csv'

    df = pd.read_csv(pre_processed_perf_file, sep=',', header=0)
    # Threads,L1-dcache-store,L1-dcache-store-misses,LLC-store,LLC-store-misses,L1-dcache-load,L1-dcache-load-misses,LLC-load,LLC-load-misses
    df = df.rename({
                    # 'L1-dcache-store': 'X',
                    # 'L1-dcache-store-misses': 'X',
                    # 'LLC-store': 'X',
                    # 'LLC-store-misses': 'X',
                    'L1-dcache-loads': 'L1-dcache-load',
                    # 'L1-dcache-load-misses': 'X',
                    'LLC-loads': 'LLC-load',
                    # 'LLC-load-misses': 'X',
                    },axis=1,errors='raise')


    df.insert(3,'L2-dcache-store',value=df['L1-dcache-store-misses'])
    df.insert(4,'L2-dcache-store-misses',value=df['LLC-store'])
    df.insert(9,'L2-dcache-load',value=df['L1-dcache-load-misses'])
    df.insert(10,'L2-dcache-load-misses',value=df['LLC-load'])

    df.insert(len(df.columns),'L1-W-Hit',value=df['L1-dcache-store']/(df['L1-dcache-store']+df['L1-dcache-store-misses']))
    df.insert(len(df.columns),'L2-W-Hit',value=df['L2-dcache-store']/(df['L2-dcache-store']+df['L2-dcache-store-misses']))
    df.insert(len(df.columns),'L3-W-Hit',value=df['LLC-store']/(df['LLC-store']+df['LLC-store-misses']))

    df.insert(len(df.columns),'L1-R-Hit',value=df['L1-dcache-load']/(df['L1-dcache-load']+df['L1-dcache-load-misses']))
    df.insert(len(df.columns),'L2-R-Hit',value=df['L2-dcache-load']/(df['L2-dcache-load']+df['L2-dcache-load-misses']))
    df.insert(len(df.columns),'L3-R-Hit',value=df['LLC-load']/(df['LLC-load']+df['LLC-load-misses']))

    df.to_csv(final_output_file, float_format='%.4f', index=False)

    print("Step 3 evaluate perf hit-rate finished")