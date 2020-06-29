#!/usr/bin/python3
import sys
import os
from pprint import pprint
import utils
import cwnd
import goodput
import loss
import rtt

iterations = int(sys.argv[1])
algorithms = [sys.argv[2], sys.argv[3], sys.argv[4]]
average_gp_flow0 = []
average_gp_flow1 = []
average_plr_flow0 = [] 
average_plr_flow1 = []
average_rtt_flow0 = [] 
average_rtt_flow1 = []

for algorithm in algorithms:
	#CWND
	time_0, average_cwnd_0, time_1, average_cwnd_1 = cwnd.get_time_and_averages(iterations, algorithm)
	cwnd.plot_flows(time_0, average_cwnd_0, time_1, average_cwnd_1, algorithm)
	
	#Goodput
	gp_flow0, gp_flow1 = goodput.get_averages(iterations, algorithm, time_lenght = 1)
	gp_flow0 = float("{:.3f}".format(gp_flow0))
	gp_flow1 = float("{:.3f}".format(gp_flow1))
	average_gp_flow0.append(gp_flow0)
	average_gp_flow1.append(gp_flow1)

	#Packet Loss Rate
	plr_flow0, plr_flow1 = loss.get_averages(iterations, algorithm)
	plr_flow0 = float("{:.4f}".format(plr_flow0))
	plr_flow1 = float("{:.4f}".format(plr_flow1))
	average_plr_flow0.append(plr_flow0)
	average_plr_flow1.append(plr_flow1)

	#Round Trip Time Rate
	average_rtt_0, average_rtt_1 = rtt.get_averages(iterations, algorithm) 
	rtt.plot_flows(average_rtt_0, average_rtt_1, algorithm)

	print("--------------------------\n", algorithm,"\n Goodputs:", gp_flow0, "Mb/s", gp_flow1, "Mb/s",
	"\n Loss rates:", plr_flow0, "%", plr_flow1, "%")


utils.bar_plot(average_gp_flow0, average_gp_flow1, algorithms,
	title="Goodputs on flows and algorithms", address="img/goodput/bar.png", ylabel="Goodputs (Mb/s)")

utils.bar_plot(average_plr_flow0, average_plr_flow1, algorithms,
	title="Packet Loss on flows and algorithms", address="img/loss/bar.png", ylabel="Loss Rate (%)")


