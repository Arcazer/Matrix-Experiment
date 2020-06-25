import _1_convert_perf_output as one
import _2_evaluate_exp_duration as two
import _3_evaluate_perf_hit as three
import _4_evaluate_cpu_demand as four
import os

# base_path='../80Cores/repetitions100/'
# repetitions = 100
# thread_sequence = [1,2,4,6,8,10,12,14,16,18,20,24,32,40,44,28,56,64]

# base_path='../96Cores/repetitions100/'
# repetitions = 100
# thread_sequence = [1,2,4,6,8,10,12,14,16,18,20,24,32,40,44,28,56,64]

base_path='../24Cores/repetitions3/'
repetitions = 3
thread_sequence = [1,2,4,6,8,10,12,14,16,18,20]



#-- create output dir where all csvs files are store. 
#-- all scripts will look use this folder to lookup 
output_dir = './resultCSVs/' 

if not os.path.exists(output_dir):
    try:
        os.mkdir(output_dir)
    except OSError:
        print ("Creation of the directory %s failed" % output_dir)


one.convert_perf_output(output_dir,base_path,repetitions)
two.evaluate_exp_duration(output_dir,base_path,thread_sequence)
three.evaluate_perf_hit(output_dir,base_path)
four.evaluate_cpu_demand(output_dir,base_path,81196000,37816000,24469000,7873000)