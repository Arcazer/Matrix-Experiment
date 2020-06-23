import numpy as np
import pandas as pd
import re
import os
import glob
import matplotlib.pyplot as plt


base_path = '../80Cores/repetitions100/' 
final_output_file = 'results-2' + base_path.replace('.','').replace('/','-') + "ExpDuration.csv"
csv_file_ending = '.csv'
df_array = []
threadCount_values=[1,2,4,6,8,10,12,14,16,18,20,24,32,40,44,28,56,64]


#1.retrieve all perf_output-files
duration_output_files = os.listdir(base_path)    
duration_output_files = list(filter(lambda f: f.endswith(csv_file_ending) and f.startswith(('1', '2', '3')), duration_output_files))
# print(duration_output_files)

for file_name in duration_output_files:

    csv_path = os.path.join(base_path,file_name)
    df = pd.read_csv(csv_path, sep=';', header=0)
    df['Timestamp'] = df['Timestamp']/1000000
    
    mean = df['Timestamp'].mean()
    std = df['Timestamp'].std(axis = 0, skipna = True)
    # print('mean: ',mean)
    # print('std: ',df['Timestamp'].std(axis = 0, skipna = True))
   
    newDf  = pd.DataFrame({'Mean':[mean],'Std':[std]})
    df_array.append(newDf)

result_df = pd.concat(df_array)
result_df.Mean = pd.to_numeric(result_df.Mean,errors='coerce') 
result_df = result_df.sort_values(by ='Mean',ascending=False)


# print(len(result_df.index))
# print(len(threadCount_values))
if(len(result_df.index) != len(threadCount_values)):
    threadCount_values='notSpecified'
    print('incorrect threadCount_values. Expected: ', len(result_df.index),', however threadCount_values only specified ', len(threadCount_values),  '. Each Threads row is filled with notSpecified')
result_df.insert(loc=0, column="Threads", value=threadCount_values)

# print(result_df.info())
result_df.to_csv(final_output_file, float_format='%.4f', index=False)

print("Step 2 evaluate experiment duration finished")
