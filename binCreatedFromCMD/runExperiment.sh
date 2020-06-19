#!/bin/bash
repCount=3

#server=24Cores
server=80Cores
#server=96Cores

perfArguments=L1-dcache-store,L1-dcache-store-misses,LLC-store,LLC-store-misses

sudo perf stat -e $perfArguments -dd java -jar repetitions$repCount/1ThreadsMatrixExp.jar &>>./expResults/$server/repetitions$repCount/output1.txt
echo "Success1"

sudo perf stat -e $perfArguments -dd java -jar repetitions$repCount/2ThreadsMatrixExp.jar &>>./expResults/$server/repetitions$repCount/output2.txt
echo "Success2"

sudo perf stat -e $perfArguments -dd java -jar repetitions$repCount/4ThreadsMatrixExp.jar &>>./expResults/$server/repetitions$repCount/output4.txt
echo "Success4"

sudo perf stat -e $perfArguments -dd java -jar repetitions$repCount/8ThreadsMatrixExp.jar &>>./expResults/$server/repetitions$repCount/output8.txt
echo "Success8"

sudo perf stat -e $perfArguments -dd java -jar repetitions$repCount/16ThreadsMatrixExp.jar &>>./expResults/$server/repetitions$repCount/output16.txt
echo "Success16"

sudo perf stat -e $perfArguments -dd java -jar repetitions$repCount/32ThreadsMatrixExp.jar &>>./expResults/$server/repetitions$repCount/output32.txt
echo "Success32"
