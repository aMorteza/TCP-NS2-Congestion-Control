#!/usr/bin/python3
import sys
import os
from pprint import pprint
import average_cwnd
import goodput

iterations = int(sys.argv[1])
algorithms = [sys.argv[2], sys.argv[3], sys.argv[4]]
average_gp_flow0 = []
average_gp_flow1 = []

for algorithm in algorithms:
	time, average_cwnd_0, average_cwnd_1 = average_cwnd.get_cwnd(iterations, algorithm)
	average_cwnd.plot_flows_cwnd(time, average_cwnd_0, average_cwnd_1, algorithm)
	gp_flow0, gp_flow1 = goodput.get_goodputs(iterations, algorithm, time_lenght = 1)
	average_gp_flow0.append(gp_flow0)
	average_gp_flow1.append(gp_flow1)
	print("Average goodput:\n", algorithm, gp_flow1, gp_flow2)
goodput.plot_goodputs(average_gp_flow0, average_gp_flow1, algorithms)