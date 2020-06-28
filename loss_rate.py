#!/usr/bin/python3
import matplotlib.pyplot as plt
import sys
import numpy as np
import utils

# Packet Lost Ratio (P.L.R) = (P.L*100)/(Number of Sent Packet From Source in Unit of Time)
def get_rate(dropped_pck_count, sent_pck_count):
  return (float(dropped_pck_count * 100)/ sent_pck_count)


def get_averages(iterations, algorithm):
  dropped_count_0 = 0
  enqueued_count_0 = 0
  dropped_count_1 = 0
  enqueued_count_1 = 0

  for i in range(1, iterations + 1):
    dropped_count_0 +=  utils.link_count("d", "tcp"+str(i)+"-"+algorithm+".tr", 0, 2, 1)
    dropped_count_0 +=  utils.link_count("d", "tcp"+str(i)+"-"+algorithm+".tr", 2, 3, 1)
    dropped_count_0 +=  utils.link_count("d", "tcp"+str(i)+"-"+algorithm+".tr", 3, 4, 1)
    enqueued_count_0 +=  utils.link_count("+", "tcp"+str(i)+"-"+algorithm+".tr", 0, 2, 1)
    enqueued_count_0 +=  utils.link_count("+", "tcp"+str(i)+"-"+algorithm+".tr", 2, 3, 1)
    enqueued_count_0 +=  utils.link_count("+", "tcp"+str(i)+"-"+algorithm+".tr", 3, 4, 1)

    '''
    In ns-2, every arriving packet is first enqueued, even if it is immediately dequeued 
    so every number of sent packet from source in unit of time in enqueued and dropped packets count
    '''

    dropped_count_1 += utils.link_count("d", "tcp"+str(i)+"-"+algorithm+".tr", 1, 2, 2)
    dropped_count_1 += utils.link_count("d", "tcp"+str(i)+"-"+algorithm+".tr", 2, 3, 2)
    dropped_count_1 += utils.link_count("d", "tcp"+str(i)+"-"+algorithm+".tr", 3, 5, 2)
    enqueued_count_1 += utils.link_count("+", "tcp"+str(i)+"-"+algorithm+".tr", 1, 2, 2)
    enqueued_count_1 += utils.link_count("+", "tcp"+str(i)+"-"+algorithm+".tr", 2, 3, 2)
    enqueued_count_1 += utils.link_count("+", "tcp"+str(i)+"-"+algorithm+".tr", 3, 5, 2)
   
  dropped_count_0 = dropped_count_0 / iterations
  enqueued_count_0 = enqueued_count_0 / iterations
  dropped_count_1 =  dropped_count_1 / iterations
  enqueued_count_1 = enqueued_count_1 / iterations

  return get_rate(dropped_count_0, dropped_count_0 + enqueued_count_0), get_rate(dropped_count_1, dropped_count_1 + enqueued_count_1)


