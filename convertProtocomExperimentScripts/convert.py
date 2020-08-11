import numpy as np
import pandas as pd
import re
import os
import glob
import sys


# Header names of target csv that are used for matrix experiment
# Threads,L1-dcache-store,L1-dcache-store-misses,L2-dcache-store,L2-dcache-store-misses,LLC-store,LLC-store-misses,L1-dcache-load,L1-dcache-load-misses,L2-dcache-load,L2-dcache-load-misses,LLC-load,LLC-load-misses,L1-W-Hit,L2-W-Hit,L3-W-Hit,L1-R-Hit,L2-R-Hit,L3-R-Hit,Core-L1-Bandwidth,L1-L2-Bandwidth,L2-L3-Bandwidth,L3-DRAM-Bandwidth,Mean-Runtime-1-Thread-With-Memory-Hierarchy,Mean-Runtime-1-Thread-WithOUT-Memory-Hierarchy

def parse_and_restructure_L2_measurement(l2_file):
    # Header of L2 Protocom measurement csv
    # ThreadPoolSize;RunNr;Runtime;Memory;L2-Cache-Misses;L2-Cache-References;L2-Cache-Miss-Rate
    # Header of L2 Protocom measurement csv 40Core has different Header names
    # ThreadPoolSize;RunNr;Runtime;Memory;L2-cacheMisses;L2-cacheReferences;L2-cache-miss-rate
    df_l2 = pd.read_csv(l2_file, sep=';', header=0)

    # create new df that remove RunNr = 0 rows because they do not contain relevant data
    df_l2 = df_l2[df_l2.RunNr != 0]
    
    # group and keep ThreadPoolSize column, therefore as_index = false
    df_l2 = df_l2.groupby('ThreadPoolSize',as_index=False).mean()
    if 'L2-cacheMisses' in df_l2.columns:
         df_l2 = df_l2.rename({
                        'ThreadPoolSize': 'Threads-L2',
                        'RunNr': 'RunNr-L2',
                        'Memory': 'Memory-L2',
                        'Runtime': 'Mean-Runtime-1-Thread-With-Memory-Hierarchy-L2',
                        'L2-cacheReferences': 'L2-dcache-load',
                        'L2-cacheMisses': 'L2-dcache-load-misses',
                        'L2-cache-miss-rate': 'L2-R-Miss-from-orig-file'
                        },axis=1,errors='raise')
    else:
        df_l2 = df_l2.rename({
                        'ThreadPoolSize': 'Threads-L2',
                        'RunNr': 'RunNr-L2',
                        'Memory': 'Memory-L2',
                        'Runtime': 'Mean-Runtime-1-Thread-With-Memory-Hierarchy-L2',
                        'L2-Cache-References': 'L2-dcache-load',
                        'L2-Cache-Misses': 'L2-dcache-load-misses',
                        'L2-Cache-Miss-Rate': 'L2-R-Miss-from-orig-file'
                        },axis=1,errors='raise')
                    
    # df_l2.insert(len(df_l2.columns),'L2-R-Hit',value= 1- df_l2['L2-R-Miss'])
    
    return df_l2

def parse_and_restructure_L3_measurement(l3_file):
    # Header of L3 Protocom measurement csv
    # ThreadPoolSize,RunNr,Runtime,Memory,Cache-Misses,Cache-References,Cache-Miss-Rate
    # Header of L3 Protocom measurement csv 40Core has different Header names
    # ThreadPoolSize;RunNr;Runtime;Memory;L3-cacheMisses;L3-cacheReferences;L3-cache-miss-rate
    df_l3 = pd.read_csv(l3_file, sep=';', header=0)
  
    # create new df that remove RunNr = 0 rows because they do not contain relevant data
    df_l3 = df_l3[df_l3.RunNr != 0]
    
    # each file has 10 experiment runs - group by ThreadPoolSize and calcualte mean for values such as Runtime,Cache-References,...
    # as_index = false to keep ThreadPoolSize column
    df_l3 = df_l3.groupby('ThreadPoolSize',as_index=False).mean()
    if 'L3-cacheMisses' in df_l3.columns:
        df_l3 = df_l3.rename({
                        'ThreadPoolSize': 'Threads-L3',
                        'RunNr': 'RunNr-L3',
                        'Memory': 'Memory-L3',
                        'Runtime': 'Mean-Runtime-1-Thread-With-Memory-Hierarchy-L3',
                        'L3-cacheReferences': 'LLC-load',
                        'L3-cacheMisses': 'LLC-load-misses',
                        'L3-cache-miss-rate': 'L3-R-Miss-from-orig-file'
                        },axis=1,errors='raise')
    else:
        df_l3 = df_l3.rename({
                        'ThreadPoolSize': 'Threads-L3',
                        'RunNr': 'RunNr-L3',
                        'Memory': 'Memory-L3',
                        'Runtime': 'Mean-Runtime-1-Thread-With-Memory-Hierarchy-L3',
                        'Cache-References': 'LLC-load',
                        'Cache-Misses': 'LLC-load-misses',
                        'Cache-Miss-Rate': 'L3-R-Miss-from-orig-file'
                        },axis=1,errors='raise')

    # df_l3.insert(len(df_l3.columns),'L3-R-Hit',value= 1- df_l3['L3-R-Miss'])
    
    return df_l3
