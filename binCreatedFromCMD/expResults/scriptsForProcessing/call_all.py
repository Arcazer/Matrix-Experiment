import _1_convert_perf_output as one
import _2_evaluate_exp_duration as two
import _3_evaluate_perf_hit as three
import _4_evaluate_cpu_demand as four

base_path='../80Cores/repetitions100/'

one.convert_perf_output(base_path,100)
two.evaluate_exp_duration(base_path,[1,2,4,6,8,10,12,14,16,18,20,24,32,40,44,28,56,64])
three.evaluate_perf_hit(base_path)
four.evaluate_cpu_demand(base_path,81196000,37816000,24469000,7873000)