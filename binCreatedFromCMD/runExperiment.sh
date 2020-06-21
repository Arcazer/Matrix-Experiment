#!/bin/bash
repCount=100

#server=24Cores
server=80Cores
#server=96Cores



for i in 1 2 4 6 8 10 12 14 16 18 20 24 32 40 44 48 56 64
do

  perfArguments="stat -x; -ddd -o expResults/$server/repetitions$repCount/perfOutput${i}.csv -e L1-dcache-store,L1-dcache-store-misses,LLC-store,LLC-store-misses"

  sudo perf $perfArguments java -jar repetitions$repCount/${i}ThreadsMatrixExp.jar &>>./expResults/$server/repetitions$repCount/consoleOutput$i.txt
  echo "Success$i"

done

mv *.csv expResults/$server/repetitions$repCount/
