#!/bin/bash
repCount=3
sudo perf stat -e L1-dcache-store,L1-dcache-store-misses,LLC-store,LLC-store-misses -dd java -jar repetitions$repCount/1ThreadsMatrixExp.jar &>>output1.txt
echo "Success1"

sudo perf stat -e L1-dcache-store,L1-dcache-store-misses,LLC-store,LLC-store-misses -dd java -jar repetitions$repCount/2ThreadsMatrixExp.jar &>>output2.txt
echo "Success2"

sudo perf stat -e L1-dcache-store,L1-dcache-store-misses,LLC-store,LLC-store-misses -dd java -jar repetitions$repCount/4ThreadsMatrixExp.jar &>>output4.txt
echo "Success4"

sudo perf stat -e L1-dcache-store,L1-dcache-store-misses,LLC-store,LLC-store-misses -dd java -jar repetitions$repCount/8ThreadsMatrixExp.jar &>>output8.txt
echo "Success8"

sudo perf stat -e L1-dcache-store,L1-dcache-store-misses,LLC-store,LLC-store-misses -dd java -jar repetitions$repCount/16ThreadsMatrixExp.jar &>>output16.txt
echo "Success16"

sudo perf stat -e L1-dcache-store,L1-dcache-store-misses,LLC-store,LLC-store-misses -dd java -jar repetitions$repCount/32ThreadsMatrixExp.jar &>>output32.txt
echo "Success32"
