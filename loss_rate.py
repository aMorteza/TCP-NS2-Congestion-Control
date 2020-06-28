#!/usr/bin/python3
import matplotlib.pyplot as plt
import sys
import numpy as np

def link_dropped_count_and_sent_count(file_name, source_node,  dest_node, flow):
  dropped_count = 0
  dequeued_count = 0
  of = open("traces/"+file_name,"r")
  lines = [i.strip().split() for i in of.readlines()]
  of.close()
  for line in lines:
    event = line[0]
    source = line[2]
    dest = line[3]
    size = line[5]
    flag = line[7]
    if  source == str(source_node) and dest == str(dest_node) and int(size) >= 1000 and int(flag) == flow:
      if event == "d":
        dropped_count += 1
      elif event == "-":
        dequeued_count += 1
  return dropped_count, dequeued_count + dropped_count

# Packet Lost Ratio (P.L.R) = (P.L*100)/(Number of Sent Packet From Source in Unit of Time)
def get_rate(dropped_pck_count, sent_pck_count):
  return (float(dropped_pck_count * 100)/ sent_pck_count)


def get_loss_rates(iterations, algorithm):
  dropped_count_0 = 0
  sent_count_0 = 0
  dropped_count_1 = 0
  sent_count_1 = 0

  for i in range(1, iterations + 1):
    dropped_count_0, sent_count_0 += link_dropped_count("tcp"+str(i)+"-"+algorithm+".tr", 0, 2, 1)
    dropped_count_0, sent_count_0 += link_dropped_count("tcp"+str(i)+"-"+algorithm+".tr", 2, 3, 1)
    dropped_count_0, sent_count_0 += link_dropped_count("tcp"+str(i)+"-"+algorithm+".tr", 3, 4, 1)

    dropped_count_1, sent_count_1 += link_dropped_count("tcp"+str(i)+"-"+algorithm+".tr", 1, 2, 2)
    dropped_count_1, sent_count_1 += link_dropped_count("tcp"+str(i)+"-"+algorithm+".tr", 2, 3, 2)
    dropped_count_1, sent_count_1 += link_dropped_count("tcp"+str(i)+"-"+algorithm+".tr", 3, 5, 2)
  dropped_count_0 /= iterations
  sent_count_0 /= iterations
  dropped_count_1 /= iterations
  sent_count_1 /= iterations
  
  return get_rate(rec_count_0, sent_count_0), get_rate(dropped_count_1, sent_count_1)














# def plot_goodputs(flow0, flow1, labels):
#   x = np.arange(len(labels))  # the label locations
#   width = 0.35  # the width of the bars

#   fig, ax = plt.subplots()
#   rects1 = ax.bar(x - width/2, flow0, width, color="b", label='Flow0')
#   rects2 = ax.bar(x + width/2, flow1, width, color="r", label='Flow1')

#   def autolabel(rects):
#         """Attach a text label above each bar in *rects*, displaying its height."""
#         for rect in rects:
#             height = rect.get_height()
#             ax.annotate('{}'.format(height),
#                         xy=(rect.get_x() + rect.get_width() / 2, height),
#                         xytext=(0, 3),  # 3 points vertical offset
#                         textcoords="offset points",
#                         ha='center', va='bottom')


#   ax.set_ylabel('Goodputs (Mb/s)')
#   ax.set_title('Goodputs by flow and algorithm')
#   ax.set_xticks(x)
#   ax.set_xticklabels(labels)
#   ax.legend()
#   autolabel(rects1)
#   autolabel(rects2)

#   fig.tight_layout()
#   plt.savefig("img/goodput/bar.png")
#   plt.close()