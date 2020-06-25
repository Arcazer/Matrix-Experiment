import numpy as np
import pandas as pd
import re
import os
import glob
import sys

# output_dir = './resultCSVs/' 
perf_file_base_name = 'perfOutput'
csv_file_ending = '.csv'

def convert_perf_output(output_dir,base_path,repetition_count):
    # base_path=base_path_arg
    # repetition_count=repetition_count_arg
    final_output_file = output_dir + 'results-1' + base_path.replace('.','').replace('/','-') + "PreProcessedPerf.csv"
   
    df_array = []
    #1.retrieve all perf_output-files
    perf_output_files = os.listdir(base_path)    
    perf_output_files = list(filter(lambda f: f.endswith(csv_file_ending) and f.startswith(perf_file_base_name), perf_output_files))
    # print('Found following perf output files:', perf_output_files )

    #2.extract perf output data and transform each to a better readable format
    for file_name in perf_output_files:
        csv_path = os.path.join(base_path,file_name)
        #ignore first csv row because it contains a comment
        df = pd.read_csv(csv_path, sep=';',skiprows=1, header=None)

        #ignore not needed columns only column 0=performanceCounterNumber and  2=performanceCounterName are needed
        df = df.drop(columns=[1,3,4,5,6])

        #ignore not needed performanceCounters (last 8 sth. like prefetchers and so on)
        df = df.iloc[:-8]

        # make columns to rows 
        df = df.transpose()

        #set second line as header
        df.columns = df.iloc[1]

        #remove second line from df (which is already used as new header)
        df = df.drop(index=[2])
        
        #make all columns numeric -- error='coerce' will insert NaN if converting fails
        df = df.apply(pd.to_numeric,errors='coerce')
        #we want values of a single run 
        df = df.div(repetition_count)

        #extracts thread count from file name and add it to dataFrame-- maybe unstable if file name pattern is changed --
        thread_count = re.findall('\d+', file_name)
        df.insert(loc=0, column="Threads", value=thread_count)

        #print(df)
        df_array.append(df)

    #3.concat perf output from different thread runs to one csv 
    result_df = pd.concat(df_array)

    #make Threads colum numeric and sort rows by Threads -- error='coerce' will insert NaN if converting fails
    result_df.Threads = pd.to_numeric(result_df.Threads,errors='coerce') 
    result_df = result_df.sort_values(by ='Threads')

    #make them int to remove decimal places
    result_df=result_df.astype('int64')

    # print(result_df)
    result_df.to_csv(final_output_file, index=False)

    print("Step 1 convert perf output finished")
