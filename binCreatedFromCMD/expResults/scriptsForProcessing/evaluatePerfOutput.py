import numpy as np
import pandas as pd
import re
import os
import glob

final_output_file = "results80CorePreProcessedPerf.csv"
base_path = '../80Cores/repetitions1/'
perf_file_base_name = 'perfOutput'
csv_file_ending = '.csv'
df_array = []

#retrieve all perf_output-files
perf_output_files = os.listdir(base_path)    
perf_output_files = list(filter(lambda f: f.endswith(csv_file_ending) and f.startswith(perf_file_base_name), perf_output_files))
print('Found following perf output files:', perf_output_files )


for file_name in perf_output_files:
    csv_path = os.path.join(base_path,file_name)
    #ignore first csv row because it contains a comment
    df = pd.read_csv(csv_path, sep=';',skiprows=1, header=None)

    #ignore not needed columns only colum 0=perfomanceCounterNumber and  2=perfomanceCounterName are needed
    df = df.drop(columns=[1,3,4,5,6])

    #ignore not needed perfomanceCounters (last 8 sth. like prefetchers and so on)
    df = df.iloc[:-8]

    # make columns to rows 
    df = df.transpose()

    #set second line as header
    df.columns = df.iloc[1]

    #remove second line from df (which is already used as new header)
    df = df.drop(index=[2])

    #extracts thread count from file name and add it to dataFrame-- maybe unstable if file name pattern is changed --
    thread_count = re.findall('\d+', file_name)
    df.insert(loc=0, column="Threads", value=thread_count)

    #print(df)
    df_array.append(df)

result_df = pd.concat(df_array)

#make Threads colum numeric and sort rows by Threads -- error='coerce' will output NaN if converting fails
result_df.Threads = pd.to_numeric(result_df.Threads,errors='coerce') 
result_df = result_df.sort_values(by ='Threads')

print(result_df)
result_df.to_csv(final_output_file, index=False)
