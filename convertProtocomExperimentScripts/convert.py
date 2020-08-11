import numpy as np
import pandas as pd
import re
import os
import glob
import sys

l2_file = './L2-CalculatePrimes-openmp-measurmentslog.csv'
l3_file = './L3-CalculatePrimes-openmp-measurmentslog.csv'
output_dir = './resultCSVs/'
final_output_file ='test.csv'
float_format_decimals = '%.10f'





df_l3 = pd.read_csv(l3_file, sep=';', header=0)

# ThreadPoolSize,RunNr,Runtime,Memory,Cache-Misses,Cache-References,Cache-Miss-Rate

# Threads,L1-dcache-store,L1-dcache-store-misses,L2-dcache-store,L2-dcache-store-misses,LLC-store,LLC-store-misses,L1-dcache-load,L1-dcache-load-misses,L2-dcache-load,L2-dcache-load-misses,LLC-load,LLC-load-misses,L1-W-Hit,L2-W-Hit,L3-W-Hit,L1-R-Hit,L2-R-Hit,L3-R-Hit,Core-L1-Bandwidth,L1-L2-Bandwidth,L2-L3-Bandwidth,L3-DRAM-Bandwidth,Mean-Runtime-1-Thread-With-Memory-Hierarchy,Mean-Runtime-1-Thread-WithOUT-Memory-Hierarchy

# create new df that remove alle 
df_l3 = df_l3[df_l3.RunNr != 0]
# group and keep ThreadPoolSize column, therefore as_index = false
df_l3 = df_l3.groupby('ThreadPoolSize',as_index=False).mean()

df_l3 = df_l3.rename({
                'ThreadPoolSize': 'Threads',
                'Runtime': 'Mean-Runtime-1-Thread-With-Memory-Hierarchy',
                'Cache-References': 'LLC-load',
                'Cache-Misses': 'LLC-load-misses',
                'Cache-Miss-Rate': 'L3-R-Hit'
                },axis=1,errors='raise')

df_l3['L3-R-Hit'] = 1- df_l3['L3-R-Hit']
# print(df_l3)



# print("Step 5 concat scaling dram bandwidth finished")

# ThreadPoolSize;RunNr;Runtime;Memory;L2-Cache-Misses;L2-Cache-References;L2-Cache-Miss-Rate

df_l2 = pd.read_csv(l2_file, sep=';', header=0)

# create new df that remove alle 
df_l2 = df_l2[df_l2.RunNr != 0]
# group and keep ThreadPoolSize column, therefore as_index = false
df_l2 = df_l2.groupby('ThreadPoolSize',as_index=False).mean()

df_l2 = df_l2.rename({
                'ThreadPoolSize': 'Threads',
                'Runtime': 'Mean-Runtime-1-Thread-With-Memory-Hierarchy2',
                'L2-Cache-References': 'L2-dcache-load',
                'L2-Cache-Misses': 'L2-dcache-load-misses',
                'L2-Cache-Miss-Rate': 'L2-R-Hit'
                },axis=1,errors='raise')
                
horizontal_stack = pd.concat([df_l3, df_l2], axis=1)

print(horizontal_stack)

horizontal_stack = horizontal_stack.sort_index(axis=1)
horizontal_stack.to_csv(final_output_file,float_format=float_format_decimals, index=False)
