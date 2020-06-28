#!/usr/bin/python3
import matplotlib.pyplot as plt
import sys
import numpy as np


def link_count(sign, file_name, source_node,  dest_node, flow):
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
    if  event == sign and source == str(source_node) and dest == str(dest_node) and int(size) >= 1000 and int(flag) == flow:
      count += 1
  return count

def bar_plot(flow0, flow1, labels, address="img/bar.png", ylabel="", title="flow and algorithm"):
  x = np.arange(len(labels))  # the label locations
  width = 0.25  # the width of the bars

  fig, ax = plt.subplots()
  rects1 = ax.bar(x - width/2, flow0, width, color="b", label='Flow0 (5ms delay)')
  rects2 = ax.bar(x + width/2, flow1, width, color="r", label='Flow1 (5-25ms var delay)')

  def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


  ax.set_ylabel(ylabel)
  ax.set_title(title)
  ax.set_xticks(x)
  ax.set_xticklabels(labels)
  ax.legend()
  autolabel(rects1)
  autolabel(rects2)

  fig.tight_layout()
  plt.savefig(address)
  plt.close()