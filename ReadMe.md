#### A comparsion on network congestion control algorithms using ns2 tcl simulation,
plot congestion window size change (CWND), Goodput, Packet loss rate and RTT for two traffic flows on TCP connection during 1000 ms. 
Network simulation iteration numbers is configurable in start.sh file.

#To start simulation and run:

`./start.sh`

## .png flows plots stored in /img folders
## .tr trace files stored in /traces
## .nam topology animation files stored in /nams.

to get ns2 topology animations uncomment line 51 in sim.tcl finish function
`51 # exec nam ${nam_path}${simtype}.nam &`