import _1_convert_perf_output as one
import _2_evaluate_exp_duration as two
import _3_evaluate_perf_hit as three
import _4_evaluate_cpu_demand as four
import _5_concat_scaling_l3_dram_bandwidth as five
import _6_concat_additional_information as six
import os

e1 = {
'base_path':'../80Cores/repetitions100/',
'resultFolderAppendix':'80Core',
'stream_scaling_dram_path':'./streamScalingDramMeassurements/streamResults80Cores.csv',
'repetitions': 100,
'core_l1_bandwidth':59858000,
'l1_l2_bandwidth':31504000,
'l2_l3_bandwidth':21966000,
'l3_dram_bandwidth':4776000,
'thread_sequence': [1,2,4,6,8,10,12,14,16,18,20,24,28,32,36,40,48,56,64,72,80],
'physical_cores': 40
}

e2 = {
'base_path':'../80Cores7000/repetitions50/',
'resultFolderAppendix':'80Core7000',
'stream_scaling_dram_path':'./streamScalingDramMeassurements/streamResults80Cores.csv',
'repetitions': 50,
'core_l1_bandwidth':59858000,
'l1_l2_bandwidth':31504000,
'l2_l3_bandwidth':21966000,
'l3_dram_bandwidth':4776000,
'thread_sequence': [1,2,4,6,8,10,12,14,16,18,20,24,28,32,36,40,48,56,64,72,80],
'physical_cores': 40
}

e3 = {
'base_path':'../96Cores/repetitions100/',
'resultFolderAppendix':'96Core',
'stream_scaling_dram_path':'./streamScalingDramMeassurements/streamResults96Cores.csv',
'repetitions': 100,
'core_l1_bandwidth':164810000,
'l1_l2_bandwidth':72590000,
'l2_l3_bandwidth':18880000,
'l3_dram_bandwidth':8207000,
'thread_sequence': [1,2,4,6,8,10,12,14,16,18,20,24,28,32,36,40,48,56,64,72,80,88,96,104,112,120,128,136,144,152,160,168,176,184,192],
'physical_cores': 96
}
e4 = {
'base_path':'../96Cores7000/repetitions50/',
'resultFolderAppendix':'96Core7000',
'stream_scaling_dram_path':'./streamScalingDramMeassurements/streamResults96Cores.csv',
'repetitions': 50,
'core_l1_bandwidth':164810000,
'l1_l2_bandwidth':72590000,
'l2_l3_bandwidth':18880000,
'l3_dram_bandwidth':8207000,
'thread_sequence': [1,2,4,6,8,10,12,14,16,18,20,24,28,32,36,40,48,56,64,72,80,88,96,104,112,120,128,136,144,152,160,168,176,184,192],
'physical_cores': 96
}
e5 = {
'base_path':'../24Cores/repetitions100/',
'resultFolderAppendix':'24Core',
'stream_scaling_dram_path':'./streamScalingDramMeassurements/streamResults24Cores.csv',
'repetitions': 100,
'core_l1_bandwidth':81196000,
'l1_l2_bandwidth':37816000,
'l2_l3_bandwidth':24469000,
'l3_dram_bandwidth':7873000,
'thread_sequence': [1,2,4,6,8,10,12,14,16,18,20],
'physical_cores': 12
}
e6 = {
'base_path':'../24Cores7000/repetitions50/',
'resultFolderAppendix':'24Core7000',
'stream_scaling_dram_path':'./streamScalingDramMeassurements/streamResults24Cores.csv',
'repetitions': 50,
'core_l1_bandwidth':81196000,
'l1_l2_bandwidth':37816000,
'l2_l3_bandwidth':24469000,
'l3_dram_bandwidth':7873000,
'thread_sequence': [1,2,4,6,8,10,12,14,16,18,20],
'physical_cores': 12
}

experiment_list = [e1,e2,e3,e4,e5,e6]

for e in experiment_list:

    base_path = e['base_path']
    resultFolderAppendix = e['resultFolderAppendix']
    stream_scaling_dram_path = e['stream_scaling_dram_path']
    repetitions = e['repetitions']
    core_l1_bandwidth = e['core_l1_bandwidth']
    l1_l2_bandwidth = e['l1_l2_bandwidth']
    l2_l3_bandwidth = e['l2_l3_bandwidth']
    l3_dram_bandwidth = e['l3_dram_bandwidth']
    thread_sequence = e['thread_sequence']
    physical_cores = e['physical_cores']



    # create output dir where all csvs files are stored. 
    # last argument in os.path.joint is a empty string(''), therefore a directory slash (/) is added to the path 
    output_dir = os.path.join('.','resultCSVs' , resultFolderAppendix,'')

    if not os.path.exists(output_dir):
        try:
            os.mkdir(output_dir)
        except OSError:
            print ("Creation of the directory %s failed" % output_dir)

    # variables 
    # float_format_decimals describes how many decimal places should be kept
    # cache_line_size is processor specific and describes how many bytes are transfered per cache line 
    float_format_decimals = '%.10f'
    cache_line_size = 64
    
    print('\n PROCESSING ' + resultFolderAppendix)

    one.convert_perf_output(output_dir,base_path,repetitions)
    two.evaluate_exp_duration(output_dir,base_path,thread_sequence,float_format_decimals)
    three.evaluate_perf_hit(output_dir,base_path,float_format_decimals)
    four.evaluate_cpu_demand(output_dir,base_path,core_l1_bandwidth,l1_l2_bandwidth,l2_l3_bandwidth,l3_dram_bandwidth,float_format_decimals,cache_line_size)
    five.concat_scaling_l3_dram_bandwidth(output_dir,base_path,float_format_decimals,stream_scaling_dram_path)
    six.concat_additional_information(output_dir,base_path,float_format_decimals,physical_cores)