A comparsion on network congestion control algorithms on TCP connection using ns2 simulation
====================
If the traffic in the network exceeds the network capacity, congestion is introduced in the network which creates packet loss.
While tcp connection is used for data transmission, congestion is controlled through automatic adjustment of the data transmission rate.
Here plot the average congestion window size change (CWND), goodput, packet loss rate and round trip time (RTT) for two TCP traffic payloads during 1000 ms for 10 iterations. 

![topology](img/topology.png)

### NS2 Installation on mint17
Nam is also needed to install. Nam (Network Animator) is an animation tool to graphically represent the network and packet 
traces.

```
sudo apt-get install -y nam
sudo apt-get install -y ns2
```

* Tcl (Tool Command Language) used for ns2 simulation. 

```
sudo apt install tclsh 
```
 

### To run simulation:

`./start.sh`

* Network simulation iteration numbers is configurable in start.sh file.
* The .png flows plots stored in /img folders.
* The .tr trace files stored in /traces used to calculate congestion parameters.
* The .nam trace files stored in /nams used for network animator.

* Uncomment line 51 in sim.tcl (finish function) to get ns2 topology animations.

`51 # exec nam ${nam_path}${simtype}.nam &`

![nam](img/nam.png)

* Average characteristics (CWND, Goodput, Loss rate and RTT) plots auto saved in /img.

![loss](img/loss/bar.png)

* There is loss fairness for the flow pairs, but congestion avoidance algorithm is effective, for example "Vegas" has a loss rate of zero, simply because it never overflows the queue.

* Any question? feel free to mail amh.morteza@gmail.com 
 
