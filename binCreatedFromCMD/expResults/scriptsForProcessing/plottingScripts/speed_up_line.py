import numpy as np
import pandas as pd
import re
import os
import glob
import matplotlib.pyplot as plt

# constant variables 
csv_file_ending = '.csv'
save_path ='./results/'

"""
Code from http://www.jesshamrick.com/2012/09/03/saving-figures-from-pyplot/ with minimal modifications
""" 
def save(path, ext='png', close=True,  x_label='', y_label='',x_max=1,y_max=1):
    # Extract the directory and filename from the given path
    directory = os.path.split(path)[0]
    filename = "%s.%s" % (os.path.split(path)[1], ext)
    if directory == '':
        directory = '.'

    # If the directory does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # The final path to save to
    savepath = os.path.join(directory, filename)
    
    plt.title('Speed-up Curve ' + filename[0:-4])
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if x_max <= 20: 
        tick_step = 2;
    elif x_max < 80:
        tick_step = 8;
    else:
        tick_step = 16;
          
    x_sequence = [1]
    # x_max + 1 else the last x-tick is skipped
    x_sequence.extend(np.arange(tick_step, x_max+1, step=tick_step))
    y_sequence = np.arange(tick_step,y_max+1,step=tick_step)

    print(x_sequence)
    print(y_sequence)

    plt.xticks(x_sequence)
    plt.yticks(y_sequence)
    # plt.show()
    plt.grid()
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -.12),
          fancybox=True, shadow=False, ncol=3, fontsize='xx-small')

    plt.savefig(savepath, bbox_inches="tight", dpi=300)

    # Close it
    if close:
        plt.close()

csv_files = os.listdir('.')    
csv_files = list(filter(lambda f: f.endswith(csv_file_ending), csv_files))

for file_name in csv_files:
    print(file_name)
    
    

    ax = plt.gca()
    csv_path = file_name
    df = pd.read_csv(csv_path, sep=',', header=0)
    # print(df.iloc[:,[3,6]])

    # row_single_thread = df.loc[df['Threads'] == 1]
    # base_single_thread_time = float(row_single_thread['Mean'])

    # speed_up_column = base_single_thread_time/df['Mean']
    # df['SpeedUpReal'] = speed_up_column
    # print(df.iloc[:,[3,6]].max().max())
    x_max = df.iloc[-1:,[0]].values[0]
    y_max = df.iloc[:,[3,6,9,12,15,18]].max().max() + 2
    
    
    df.plot(y=3, x='Threads',kind='line',marker='x',color='k',ax=ax)
    df.plot(y=6, x='Threads',kind='line',marker='.',color='r',ax=ax)
    df.plot(y=9, x='Threads',kind='line',marker='*',color='y',ax=ax)
    df.plot(y=12, x='Threads',kind='line',marker='*',color='g',ax=ax)
    df.plot(y=15, x='Threads',kind='line',marker='^',color='grey',ax=ax)
    df.plot(y=18, x='Threads',kind='line',marker='v',color='b',ax=ax)

    save( save_path + file_name[0:-4], x_label='# of threads',y_label='Speed-up factor',x_max=x_max,y_max=y_max)


    
 
