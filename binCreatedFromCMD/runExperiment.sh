#!/bin/bash
repCount=1

server=24Cores
# server=80Cores
# server=96Cores


# for i in 1 2 4 6 8 10 12 14 16 18 20
for i in 1 2 4 6 8 10 12 14 16 18 20 24 32 40 44 48 56 64
do
  # we set perfoutput file name here, therefore perfArguments assignment must be inside the loop
  perfArguments="stat -x; -ddd -o expResults/$server/repetitions$repCount/perfOutput${i}.csv -e L1-dcache-store,L1-dcache-store-misses,LLC-store,LLC-store-misses,cycle_activity.stalls_l2_miss,cycle_activity.stalls_l3_miss,longest_lat_cache.reference,longest_lat_cache.miss"

  sudo perf $perfArguments java -jar matrix_3000X3000_ExperimentJars/repetitions$repCount/${i}ThreadsMatrixExp.jar &>>./expResults/$server/repetitions$repCount/consoleOutput$i.txt
  echo "Success$i"

done

# move all csv runTime from experiment into correct folder
mv *.csv expResults/$server/repetitions$repCount/
