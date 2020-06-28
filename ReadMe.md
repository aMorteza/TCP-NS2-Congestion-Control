A comparsion on network congestion control algorithms on TCP connection using ns2 simulation
====================

Here we plot average congestion window size change (CWND), Goodput, Packet Loss rate and RTT for two traffic flows with TCP connection during 1000 ms for 10 iterations. 

![topology](img/topology.png)


### To start simulation run:

`./start.sh`

* Network simulation iteration numbers is configurable in start.sh file.
* The .png flows plots stored in /img folders.
* The .tr trace files stored in /traces used to calculate congestion parameters.
* The .nam trace files stored in /nams used for network animator.

* Uncomment line 51 in sim.tcl (finish function) to get ns2 topology animations.

`51 # exec nam ${nam_path}${simtype}.nam &`

![nam](img/nam.png)

- Any question? feel free to mail 
 [Amirhosein_Morteza@yahoo.com](https://Amirhosein_Morteza@yahoo.com) 
