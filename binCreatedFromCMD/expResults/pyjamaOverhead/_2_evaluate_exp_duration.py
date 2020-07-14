import numpy as np
import pandas as pd
import re
import os
import glob
import matplotlib.pyplot as plt

csv_file_ending = '.csv'
base_path_list=['./24Core','./80Core']
output_dir = './'
thread_sequence_values=['pyjama','sequential','pyjama','sequential','sequential','pyjama','sequential','pyjama']
float_format_decimals = '%.10f'

for base_path in base_path_list:
    final_output_file = output_dir + 'results-2' + base_path.replace('.','').replace('/','-') + "ExpDuration.csv"
    df_array = []

    #1.retrieve all perf_output-files
    duration_output_files = os.listdir(base_path)    
    duration_output_files = list(filter(lambda f: f.endswith(csv_file_ending) and f.startswith(('0','1', '2', '3')), duration_output_files))

    #2. calculate mean and std of exp duration time
    for file_name in duration_output_files:
        print(file_name)

        csv_path = os.path.join(base_path,file_name)
        df = pd.read_csv(csv_path, sep=';', header=0)

        #convert to milliseconds
        df['Timestamp'] = df['Timestamp']/1000000
        
        mean = df['Timestamp'].mean()
        std = df['Timestamp'].std(axis = 0, skipna = True)

        df_with_mean_and_std  = pd.DataFrame({'Mean':[mean],'Std':[std]})
        df_array.append(df_with_mean_and_std)

    result_df = pd.concat(df_array)
    result_df.Mean = pd.to_numeric(result_df.Mean,errors='coerce') 
    result_df = result_df.sort_values(by ='Mean',ascending=False)

    if(len(result_df.index) != len(thread_sequence_values)):
        thread_sequence_values='notSpecified'
        print('incorrect thread_sequence_values. Expected: ', len(result_df.index),', however thread_sequence_values only specified ', len(threadCount_values),  '. Each Threads row is filled with notSpecified')
    result_df.insert(loc=0, column="RunType", value=thread_sequence_values)

    result_df.to_csv(final_output_file, float_format=float_format_decimals, index=False)

print("Step 2 evaluate experiment duration finished")
