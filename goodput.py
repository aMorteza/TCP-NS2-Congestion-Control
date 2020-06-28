#!/usr/bin/python3
import matplotlib.pyplot as plt
import sys
import numpy as np
import utils

#T = 1000ms = 1s
#bits = count * 1000 byte = count * 1000 * 8 Mbit
def get_received_packets_bandwidth(rec_count, packet_size=1000, time_lenght=1):
  #No need to Rip off the header
  return (float(rec_count * packet_size)/time_lenght) * (8 / 1000000)  

def get_goodputs(iterations, algorithm, time_lenght = 1):
  rec_count_0 = 0
  rec_count_1 = 0
  for i in range(1, iterations + 1):
    rec_count_0 += utils.link_count("r", "tcp"+str(i)+"-"+algorithm+".tr", 0, 2, 1)
    rec_count_0 += utils.link_count("r", "tcp"+str(i)+"-"+algorithm+".tr", 2, 3, 1)
    rec_count_0 += utils.link_count("r", "tcp"+str(i)+"-"+algorithm+".tr", 3, 4, 1)

    rec_count_1 += utils.link_count("r", "tcp"+str(i)+"-"+algorithm+".tr", 1, 2, 2)
    rec_count_1 += utils.link_count("r", "tcp"+str(i)+"-"+algorithm+".tr", 2, 3, 2)
    rec_count_1 += utils.link_count("r", "tcp"+str(i)+"-"+algorithm+".tr", 3, 5, 2)
  rec_count_0 /= iterations
  rec_count_1 /= iterations
  return get_received_packets_bandwidth(rec_count_0), get_received_packets_bandwidth(rec_count_1)
