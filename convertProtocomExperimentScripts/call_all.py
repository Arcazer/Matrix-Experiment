import numpy as np
import pandas as pd
import re
import os
import glob
import sys
import convert

# l2_file = './L2-CalculatePrimes-openmp-measurmentslog.csv'
# l3_file = './L3-CalculatePrimes-openmp-measurmentslog.csv'
output_dir = './resultCSVs/'
final_output_file ='test.csv'
float_format_decimals = '%.10f'

# pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# server = '12-core'
# server = '40-core'
server = '96-core'
default_log_name = '-openmp-measurmentslog-'

CalcPrime = {
    'server' : server,
    'name' : 'CalcPrime',
    'l2_file' : './' + server + '/CalculatePrimes' + default_log_name + 'L2.csv',
    'l3_file' : './' + server + '/CalculatePrimes' + default_log_name + 'L3.csv'
}
CountNumbers = {
    'server' : server,
    'name' : 'CountNumbers',
    'l2_file' : './' + server + '/CountNumbers' + default_log_name + 'L2.csv',
    'l3_file' : './' + server + '/CountNumbers' + default_log_name + 'L3.csv'
} 
Fibonacci = {
    'server' : server,
    'name' : 'Fibonacci',
    'l2_file' : './' + server + '/Fibonacci' + default_log_name + 'L2.csv',
    'l3_file' : './' + server + '/Fibonacci' + default_log_name + 'L3.csv'
} 
Mandelbrot = {
    'server' : server,
    'name' :'Mandelbrot',
    'l2_file' : './' + server + '/Mandelbrot' + default_log_name + 'L2.csv',
    'l3_file' : './' + server + '/Mandelbrot' + default_log_name + 'L3.csv'
} 
MultiplyMatrix = {
    'server' : server,
    'name' : 'MultiplyMatrix',
    'l2_file' : './' + server + '/MultiplyMatrix' + default_log_name + 'L2.csv',
    'l3_file' : './' + server + '/MultiplyMatrix' + default_log_name + 'L3.csv'
}
SortArray = {
    'server' : server,
    'name' : 'SortArray',
    'l2_file' : './' + server + '/SortArray' + default_log_name + 'L2.csv',
    'l3_file' : './' + server + '/SortArray' + default_log_name + 'L3.csv'
}   

algorithm_measurements_all = [CalcPrime,CountNumbers,Fibonacci,Mandelbrot,MultiplyMatrix,SortArray]




#1 load two csv files
#2 reformat und restructure csv
#3 concat btoh csv to one

# Header names of target csv that are used for matrix experiment
# Threads,L1-dcache-store,L1-dcache-store-misses,L2-dcache-store,L2-dcache-store-misses,LLC-store,LLC-store-misses,L1-dcache-load,L1-dcache-load-misses,L2-dcache-load,L2-dcache-load-misses,LLC-load,LLC-load-misses,L1-W-Hit,L2-W-Hit,L3-W-Hit,L1-R-Hit,L2-R-Hit,L3-R-Hit,Core-L1-Bandwidth,L1-L2-Bandwidth,L2-L3-Bandwidth,L3-DRAM-Bandwidth,Mean-Runtime-1-Thread-With-Memory-Hierarchy,Mean-Runtime-1-Thread-WithOUT-Memory-Hierarchy


    
if __name__ == "__main__":
    for alg in  algorithm_measurements_all:
        print(alg['name'])
        l2_file = alg['l2_file']
        l3_file = alg['l3_file']
        
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
            
            
            # 1-miss/total
            df_concat['L2-R-Hit'] = 1 - df_concat['L2-dcache-load-misses']/df_concat['L2-dcache-load']
            df_concat['L3-R-Hit'] = 1 - df_concat['LLC-load-misses'] /df_concat['LLC-load']          
            
            # df_concat['LLC-load'] = pd.to_numeric( df_concat['LLC-load'],errors='coerce') 
            
            # reorder columns 
            column_order = ['Threads','L2-dcache-load','L2-dcache-load-misses','LLC-load','LLC-load-misses','L2-R-Hit','L3-R-Hit','Mean-Runtime-1-Thread-With-Memory-Hierarchy-L2','Mean-Runtime-1-Thread-With-Memory-Hierarchy-L3','L2-R-Miss-from-orig-file','L3-R-Miss-from-orig-file']
            df_concat = df_concat.reindex(columns=column_order)
            
            print(df_concat)
            final_output_file = alg['server'] + '-'+ alg['name'] + '.csv'
            df_concat.to_csv(final_output_file,float_format=float_format_decimals, index=False)  
  
