#!/bin/bash

iterations=10
algorithms=("Tahoe" "NewReno" "Vegas")
steps=($(seq 1 1 ${iterations}));
#Creating trace files 
for i in ${algorithms[@]}
do
	for j in ${steps[@]}
	do
		ns sim.tcl $j $i
	done
done

if [ $? -eq 0 ] 
then
	python3 characteristics/plot.py $iterations ${algorithms[@]}   
fi