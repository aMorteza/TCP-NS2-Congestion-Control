#!/usr/bin/python3
import matplotlib.pyplot as plt
import sys
import numpy as np

def link_received_count(file_name, source_node,  dest_node, flow):
  count = 0
  of = open("traces/"+file_name,"r")
  lines = [i.strip().split() for i in of.readlines()]
  of.close()
  for line in lines:
    event = line[0]
    source = line[2]
    dest = line[3]
    size = line[5]
    flag = line[7]
    if event == "r" and source == str(source_node) and dest == str(dest_node) and int(size) >= 1000 and int(flag) == flow:
      # print("event:", event, "source:", source, "dest:", dest, "size:", size, "flag:", flag)
      count += 1
  return count

#T = 1000ms = 1s
#bits = count * 1000 byte = count * 1000 * 8 Mbit
def get_goodput(rec_count, packet_size=1000, time_lenght=1):
  #No need to Rip off the header
  return (float(rec_count * packet_size)/time_lenght) * (8 / 1000000)  

def get_goodputs(iterations, algorithm, time_lenght = 1):
  rec_count_0 = 0
  rec_count_1 = 0
  for i in range(1, iterations + 1):
    rec_count_0 += link_received_count("tcp"+str(i)+"-"+algorithm+".tr", 0, 2, 1)
    rec_count_0 += link_received_count("tcp"+str(i)+"-"+algorithm+".tr", 2, 3, 1)
    rec_count_0 += link_received_count("tcp"+str(i)+"-"+algorithm+".tr", 3, 4, 1)

    rec_count_1 += link_received_count("tcp"+str(i)+"-"+algorithm+".tr", 1, 2, 2)
    rec_count_1 += link_received_count("tcp"+str(i)+"-"+algorithm+".tr", 2, 3, 2)
    rec_count_1 += link_received_count("tcp"+str(i)+"-"+algorithm+".tr", 3, 5, 2)
  rec_count_0 /= iterations
  rec_count_1 /= iterations
  return get_goodput(rec_count_0), get_goodput(rec_count_1)

def plot_goodputs(flow0, flow1, labels):
  x = np.arange(len(labels))  # the label locations
  width = 0.35  # the width of the bars

  fig, ax = plt.subplots()
  rects1 = ax.bar(x - width/2, flow0, width, color="b", label='Flow0')
  rects2 = ax.bar(x + width/2, flow1, width, color="r", label='Flow1')

  def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


  ax.set_ylabel('Goodputs (Mb/s)')
  ax.set_title('Goodputs by flow and algorithm')
  ax.set_xticks(x)
  ax.set_xticklabels(labels)
  ax.legend()
  autolabel(rects1)
  autolabel(rects2)

  fig.tight_layout()
  plt.savefig("img/goodput/bar.png")
  plt.close()