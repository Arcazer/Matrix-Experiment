import _1_convert_perf_output as one
import _2_evaluate_exp_duration as two
import _3_evaluate_perf_hit as three
import _4_evaluate_cpu_demand as four
import os

# base_path='../80Cores/repetitions100/'
# resultFolderAppendix='80Core'
# repetitions = 100
# core_l1_bandwidth=59858000
# l1_l2_bandwidth=31504000
# l2_l3_bandwidth=21966000
# l3_dram_bandwidth=4776000
# thread_sequence = [1,2,4,6,8,10,12,14,16,18,20,24,32,40,44,48,56,64]

# base_path='../96Cores/repetitions100/'
# resultFolderAppendix='96Core'
# repetitions = 100
# core_l1_bandwidth=164810000
# l1_l2_bandwidth=72590000
# l2_l3_bandwidth=18880000
# l3_dram_bandwidth=8207000
# thread_sequence = [1,2,4,6,8,10,12,14,16,18,20,24,32,40,44,48,56,64]

base_path='../24Cores/repetitions100/'
resultFolderAppendix='24Core'
repetitions = 100
core_l1_bandwidth=81196000
l1_l2_bandwidth=37816000
l2_l3_bandwidth=24469000
l3_dram_bandwidth=7873000
thread_sequence = [1,2,4,6,8,10,12,14,16,18,20]



#-- create output dir where all csvs files are store. 
#-- all scripts will look use this folder to lookup 
# last path is empty, therefore a directory / is added to the path 
output_dir = os.path.join('.','resultCSVs' , resultFolderAppendix,'')

if not os.path.exists(output_dir):
    try:
        os.mkdir(output_dir)
    except OSError:
        print ("Creation of the directory %s failed" % output_dir)

float_format_decimals = '%.10f';

one.convert_perf_output(output_dir,base_path,repetitions)
two.evaluate_exp_duration(output_dir,base_path,thread_sequence,float_format_decimals)
three.evaluate_perf_hit(output_dir,base_path,float_format_decimals)
four.evaluate_cpu_demand(output_dir,base_path,core_l1_bandwidth,l1_l2_bandwidth,l2_l3_bandwidth,l3_dram_bandwidth,float_format_decimals)