#!/usr/bin/python3
import matplotlib.pyplot as plt

def readFile(filename):
	of = open("traces/"+filename,"r")
	lines = [i.strip().split() for i in of.readlines()]
	of.close()
	cwnd = []
	time = []
	for line in lines:
		if "cwnd_" in line:
			time.append(float(line[0]))
			cwnd.append(float(line[6]))
	return time, cwnd

def add_items(list1, list2):
	if len(list1) == 0:
		return list2
	elif len(list2) == 0:
		return list1
	else:
		res_list = [] 
		for i in range(0, len(list1)): 
			res_list.append(list1[i] + list2[i])
		return res_list

def get_cwnd(iterations, algorithm):
	time = []
	average_cwnd_0 = []
	average_cwnd_1 = []
	for i in range(1, iterations + 1):
		time, cwnd_0 = readFile("tcp"+str(i)+"-"+algorithm+"-flow0.tr")
		average_cwnd_0 = add_items(cwnd_0, average_cwnd_0)
		time, cwnd_1 = readFile("tcp"+str(i)+"-"+algorithm+"-flow1.tr")
		average_cwnd_1 = add_items(cwnd_1, average_cwnd_1)
	average_cwnd_0 = [i / iterations for i in average_cwnd_0]
	average_cwnd_1 = [i / iterations for i in average_cwnd_1]
	return time, average_cwnd_0, average_cwnd_1

def plot_flows_cwnd(time, average_cwnd_0, average_cwnd_1, algorithm):
	plt.figure(figsize = [10, 7])
	plt.title(algorithm, fontsize=16)
	plt.plot(time[0:len(average_cwnd_0)], average_cwnd_0, color="b")
	plt.plot(time[0:len(average_cwnd_1)], average_cwnd_1, color="r")
	plt.legend(['Flow1 (delay 5ms)', 'Flow2 (variable delay 5-25ms)'], loc='best')

	plt.xlabel('Time', fontsize=14) 
	plt.ylabel('CWND', fontsize=14)   
	plt.tight_layout()
	plt.savefig("img/cwnd/"+algorithm+"_cwnd.png")
	plt.close()