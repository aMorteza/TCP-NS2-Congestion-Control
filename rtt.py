#!/usr/bin/python3
import matplotlib.pyplot as plt
import sys
import numpy as np
import utils
#Accoring to TCP connection expect: goodput_ratio = 1/2 × (RTT_ratio)^2

def readFile(filename, source, dest):
	of = open("traces/"+filename,"r")
	lines = [i.strip().split() for i in of.readlines()]
	of.close()
	rtt = []
	for line in lines:
		if line[1] == str(source) and line[2] == str(dest):
			rtt.append(float(line[4]))
	return rtt

def get_averages(iterations, algorithm):
	average_rtt_0 = []
	average_rtt_1 = []
	for i in range(1, iterations + 1):
		rtt_0 = readFile("tcp"+str(i)+"-"+algorithm+"-rtt.tr", 0, 4)
		average_rtt_0 = utils.add_items(rtt_0, average_rtt_0)
		
		rtt_1 = readFile("tcp"+str(i)+"-"+algorithm+"-rtt.tr", 1, 5)
		average_rtt_1 = utils.add_items(rtt_1, average_rtt_1)
	average_rtt_0 = [i / iterations for i in average_rtt_0]
	average_rtt_1 = [i / iterations for i in average_rtt_1]
	return average_rtt_0, average_rtt_1

def plot_flows(rtt_0, rtt_1, algorithm):
	plt.figure(figsize = [10, 7])
	plt.title(algorithm, fontsize=16)
	plt.plot([i for i in range(0, len(rtt_0))], rtt_0, color="b")
	plt.plot([i for i in range(0, len(rtt_1))], rtt_1, color="r")
	plt.legend(['Flow1 (delay 5ms)', 'Flow2 (variable delay 5-25ms)'], loc='best')

	plt.xlabel('Time (ms)', fontsize=14) 
	plt.ylabel('Round Trip Time (ms)', fontsize=14)   
	plt.tight_layout()
	plt.savefig("img/rtt/"+algorithm+"_rtt.png")
	plt.close()