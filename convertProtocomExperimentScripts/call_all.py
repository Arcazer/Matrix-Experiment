import numpy as np
import pandas as pd
import re
import os
import glob
import sys
import convert
import concat_bandwidth_and_physical_cores
# import calc_cpu_recalibrated


# l2_file = './L2-CalculatePrimes-openmp-measurmentslog.csv'
# l3_file = './L3-CalculatePrimes-openmp-measurmentslog.csv'
# output_dir = './resultCSVs/'
# final_output_file ='test.csv'
float_format_decimals = '%.10f'

# pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# server = '12-core'
# server = '40-core'
# server = '96-core'
default_log_name = '-openmp-measurmentslog-'

CalcPrime = {
    'name' : 'CalcPrime',
    # 'l2_file' : './' + server + '/CalculatePrimes' + default_log_name + 'L2.csv',
    # 'l3_file' : './' + server + '/CalculatePrimes' + default_log_name + 'L3.csv'
}
CountNumbers = {
    'name' : 'CountNumbers',
    # 'l2_file' : './' + server + '/CountNumbers' + default_log_name + 'L2.csv',
    # 'l3_file' : './' + server + '/CountNumbers' + default_log_name + 'L3.csv'
} 
Fibonacci = {
    'name' : 'Fibonacci',
    # 'l2_file' : './' + server + '/Fibonacci' + default_log_name + 'L2.csv',
    # 'l3_file' : './' + server + '/Fibonacci' + default_log_name + 'L3.csv'
} 
Mandelbrot = {
    'name' :'Mandelbrot',
    # 'l2_file' : './' + server + '/Mandelbrot' + default_log_name + 'L2.csv',
    # 'l3_file' : './' + server + '/Mandelbrot' + default_log_name + 'L3.csv'
} 
MultiplyMatrix = {
    'name' : 'MultiplyMatrix',
    # 'l2_file' : './' + server + '/MultiplyMatrix' + default_log_name + 'L2.csv',
    # 'l3_file' : './' + server + '/MultiplyMatrix' + default_log_name + 'L3.csv'
}
SortArray = {
    'name' : 'SortArray',
    # 'l2_file' : './' + server + '/SortArray' + default_log_name + 'L2.csv',
    # 'l3_file' : './' + server + '/SortArray' + default_log_name + 'L3.csv'
}   
# List with all algorithms
algorithm_measurements_all = [CalcPrime,CountNumbers,Fibonacci,Mandelbrot,MultiplyMatrix,SortArray]

server_12_core = {
'name':'12-core',
'resultFolderAppendix':'12CoreConverted',
'stream_scaling_dram_path':'./streamScalingDramMeassurements/streamResults24Cores.csv',
'core_l1_bandwidth':81196000,
'l1_l2_bandwidth':37816000,
'l2_l3_bandwidth':24469000,
'l3_dram_bandwidth':7873000,
'thread_sequence': [1,2,4,6,8,10,12,14,16,18,20],
'physical_cores': 12
}
server_40_core = {
'name':'40-core',
'resultFolderAppendix':'40CoreConverted',
'stream_scaling_dram_path':'./streamScalingDramMeassurements/streamResults80Cores.csv',
'core_l1_bandwidth':59858000,
'l1_l2_bandwidth':31504000,
'l2_l3_bandwidth':21966000,
'l3_dram_bandwidth':4776000,
'physical_cores': 40
}
server_96_core = {
'name':'96-core',
'resultFolderAppendix':'96CoreConverted',
'stream_scaling_dram_path':'./streamScalingDramMeassurements/streamResults96Cores.csv',
'core_l1_bandwidth':164810000,
'l1_l2_bandwidth':72590000,
'l2_l3_bandwidth':18880000,
'l3_dram_bandwidth':8207000,
'physical_cores': 96
}

# List with all servers
server_all =[server_12_core,server_40_core,server_96_core]


# Header names of target csv that are used for matrix experiment
# Threads,L1-dcache-store,L1-dcache-store-misses,L2-dcache-store,L2-dcache-store-misses,LLC-store,LLC-store-misses,L1-dcache-load,L1-dcache-load-misses,L2-dcache-load,L2-dcache-load-misses,LLC-load,LLC-load-misses,L1-W-Hit,L2-W-Hit,L3-W-Hit,L1-R-Hit,L2-R-Hit,L3-R-Hit,Core-L1-Bandwidth,L1-L2-Bandwidth,L2-L3-Bandwidth,L3-DRAM-Bandwidth,L3-DRAM-Bandwidth-Scaling,Mean-Runtime-1-Thread-With-Memory-Hierarchy,Mean-Runtime-1-Thread-Without-Memory-Hierarchy,Mean-Runtime-1-Thread-Without-Memory-Hierarchy-Cache-Line,Physical-Cores


    
if __name__ == "__main__":
    for server in server_all:
        for alg in  algorithm_measurements_all:
            print(server['name'], ' with ',alg['name'])
            # l2_file = alg['l2_file']
            # l3_file = alg['l3_file']
            l2_file = './' + server['name'] + '/SortArray' + default_log_name + 'L2.csv'
            l3_file = './' + server['name'] + '/SortArray' + default_log_name + 'L3.csv'
            
            df_l2 = convert.parse_and_restructure_L2_measurement(l2_file)
            df_l3 = convert.parse_and_restructure_L3_measurement(l3_file)
          
                            
            df_concat = pd.concat([df_l3, df_l2], axis=1) 
            
            # csv error checks 
            has_mismatch_error = False; 
            if(not df_concat['Threads-L2'].equals(df_concat['Threads-L3'])):
                has_mismatch_error = True
                print('Thread values are not equal', + alg['l2_file'])
            if(not df_concat['RunNr-L2'].equals(df_concat['RunNr-L3'])):
                has_mismatch_error = True
                print('RunNr values are not equal', + alg['l2_file'])
                
                
            if(has_mismatch_error):
                print('Check for mismatch in ', + alg['l2_file'] + '! \n file is skipped ' )
            else:
                df_concat = df_concat.drop(columns=['RunNr-L2', 'RunNr-L3','Threads-L2','Memory-L2','Memory-L3'])
                df_concat = df_concat.rename({'Threads-L3':'Threads'},axis=1,errors='raise')
                
                # truncate all decimal places for specific columns 
                df_concat['L2-dcache-load'] = df_concat['L2-dcache-load'].astype('int64')
                df_concat['L2-dcache-load-misses'] = df_concat['L2-dcache-load-misses'].astype('int64')
                df_concat['LLC-load'] = df_concat['LLC-load'].astype('int64')
                df_concat['LLC-load-misses'] = df_concat['LLC-load-misses'].astype('int64')
                
                
                # recalculate hit rate 1-miss/total
                df_concat['L2-R-Hit'] = 1 - df_concat['L2-dcache-load-misses']/df_concat['L2-dcache-load']
                df_concat['L3-R-Hit'] = 1 - df_concat['LLC-load-misses'] /df_concat['LLC-load']          
                                
                # reorder columns 
                column_order = ['Threads','L2-dcache-load','L2-dcache-load-misses','LLC-load','LLC-load-misses','L2-R-Hit','L3-R-Hit','Mean-Runtime-1-Thread-With-Memory-Hierarchy-L2','Mean-Runtime-1-Thread-With-Memory-Hierarchy-L3','L2-R-Miss-from-orig-file','L3-R-Miss-from-orig-file']
                df_concat = df_concat.reindex(columns=column_order)
                
            
                # create output dir where all csvs files are stored. 
                # last argument in os.path.joint is a empty string(''), therefore a directory slash (/) is added to the path 
                output_dir = os.path.join('.','resultCSVs' , server['resultFolderAppendix'],'')
                
                if not os.path.exists(output_dir):
                    # print(os.path.exists(output_dir))
                    try:
                        os.makedirs(output_dir)
                    except OSError:
                        print ("Creation of the directory %s failed" % output_dir)
                
                # print(df_concat)
                
                cache_line_size = 64
                df_concat = concat_bandwidth_and_physical_cores.concat(df_concat,cache_line_size,server['core_l1_bandwidth'],server['l1_l2_bandwidth'],server['l2_l3_bandwidth'],server['l3_dram_bandwidth'],server['stream_scaling_dram_path'],server['physical_cores'])
                
                
                
                final_output_file = output_dir + alg['name'] + '.csv' 
                    
                # 'stream_scaling_dram_path':'./streamScalingDramMeassurements/streamResults96Cores.csv',
# 'core_l1_bandwidth':164810000,
# 'l1_l2_bandwidth':72590000,
# 'l2_l3_bandwidth':18880000,
# 'l3_dram_bandwidth':8207000,
# 'physical_cores': 96
                df_concat.to_csv(final_output_file,float_format=float_format_decimals, index=False)  
  
