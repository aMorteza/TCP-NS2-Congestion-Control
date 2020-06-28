
#Run iteration
set interation [lindex $argv 0]

#Congestion control algorithm
set algorithm [lindex $argv 1]
set vegas [string compare ${algorithm} Vegas]
set newreno [string compare ${algorithm} NewReno]
set tahoe [string compare ${algorithm} Tahoe]

# Create a simulator object 
set ns [new Simulator] 

# Define different colors 
# for data flows (for NAM) 
$ns color 1 Blue 
$ns color 2 Red 


set simtype "tcp${interation}-${algorithm}"
set simflow0 "tcp${interation}-${algorithm}-flow0"
set simflow1 "tcp${interation}-${algorithm}-flow1"
set rttflow "tcp${interation}-${algorithm}-rtt"

puts $simtype

# Open the NAM trace file 
set trace_path "traces/"
set nam_path "nams/"
set nf [open  ${nam_path}${simtype}.nam w] 
$ns namtrace-all $nf 
set tracefile [open  ${trace_path}${simtype}.tr w]
set flowtrace0 [open  ${trace_path}${simflow0}.tr w]
set flowtrace1 [open  ${trace_path}${simflow1}.tr w]
set rtttrace [open  ${trace_path}${rttflow}.tr w]

$ns trace-all $tracefile

#Define a 'finish' procedure
proc finish {} {
  global simtype ns nf tracefile flowtrace0 flowtrace1 rtttrace
  $ns flush-trace
  # Close the trace file 
  close $tracefile 
  close $flowtrace0
  close $flowtrace1
  close $rtttrace 
  # Close the NAM file 
  close $nf 
  # Execute NAM on the trace file 
  # exec nam ${nam_path}${simtype}.nam & 
  exit 0
}

# Create six nodes
foreach i " 0 1 2 3 4 5" {
	set n$i [$ns node]
}

# Create links between the nodes 
# Node param1 → Server
# Node param2 → Router
# 100Mb → Link bandwidth
# 5ms → Propagation delay
# DropTail → Queue type
$ns duplex-link  $n0 $n2 100Mb 5ms DropTail 
$ns duplex-link  $n4 $n3 100Mb 5ms DropTail 
$ns duplex-link  $n2 $n3 100kb 1ms DropTail 

# Set variable delay 
set variable_delay [new RandomVariable/Uniform]; # delay 5-25 ms
$variable_delay set min_ 5 
$variable_delay set max_ 25
# puts [format "%-8.3f" [$variable_delay value]]

$ns duplex-link  $n1 $n2 100Mb $variable_delay DropTail 
$ns duplex-link  $n5 $n3 100Mb $variable_delay DropTail 

# Set Queue Size of links to 10 
$ns queue-limit $n1 $n2 10
$ns queue-limit $n0 $n2 10
$ns queue-limit $n2 $n3 10
$ns queue-limit $n4 $n3 10
$ns queue-limit $n5 $n3 10


# Give node position (for NAM) 
$ns duplex-link-op $n0 $n2 orient left-up
$ns duplex-link-op $n1 $n2 orient left-down
$ns duplex-link-op $n3 $n4 orient right-up
$ns duplex-link-op $n3 $n5 orient right-down

# Monitor the queue for links. (for NAM) 
$ns duplex-link-op $n0 $n2 queuePos 0.5
$ns duplex-link-op $n1 $n2 queuePos 0.5
$ns duplex-link-op $n2 $n3 queuePos 0.5
$ns duplex-link-op $n4 $n3 queuePos 0.5
$ns duplex-link-op $n5 $n3 queuePos 0.5


# TCP sending agent and attach it to n0
# nothing means Tahoe use /Vegas /newReno for Vegas and NewReno congesion control algorthims   
if { $vegas == 0 } {
   set tcp0 [new Agent/TCP/Vegas]
} elseif { $newreno == 0 } {
   set tcp0 [new Agent/TCP/Newreno]
} elseif { $tahoe == 0 } {
   set tcp0 [new Agent/TCP]
} else {
   puts "Error unknown congestion control algorithm for agent0!!!"
   exit 1 
}

$tcp0 set class_ 1
$tcp0 set window_ 100
$tcp0 set packetSize_ 1000
$tcp0 set ttl_ 64
$ns attach-agent $n0 $tcp0

# Let's trace some variables
$ns monitor-agent-trace $tcp0
$tcp0 attach $flowtrace0
$tcp0 tracevar cwnd_
$tcp0 tracevar ssthresh_
$tcp0 tracevar ack_
$tcp0 tracevar maxseq_

#Create a TCP receive agent (a traffic sink) and attach it to n4
set end0 [new Agent/TCPSink]
$ns attach-agent $n4 $end0

#Connect the traffic source with the traffic sink
$ns connect $tcp0 $end0
$tcp0 set fid_ 1


set ftp0 [new Application/FTP] 
$ftp0 attach-agent $tcp0 
# $ftp0 set type_ FTP 


# TCP sending agent and attach it to n1
# nothing means Tahoe use /Vegas /newReno for Vegas and NewReno congesion control algorthims  
if { $vegas == 0 } {
   set tcp1 [new Agent/TCP/Vegas]
} elseif { $newreno == 0 } {
   set tcp1 [new Agent/TCP/Newreno]
} elseif { $tahoe == 0 } {
   set tcp1 [new Agent/TCP]
} else {
   puts "Error unknown congestion control algorithm for agent0!!!"
   exit 1 
}

$tcp1 set class_ 2
$tcp1 set window_ 100
$tcp1 set packetSize_ 1000
$tcp1 set ttl_ 64
$ns attach-agent $n1 $tcp1

# Let's trace some variables
$ns monitor-agent-trace $tcp1
$tcp1 attach $flowtrace1
$tcp1 tracevar cwnd_
$tcp1 tracevar ssthresh_
$tcp1 tracevar ack_
$tcp1 tracevar maxseq_

#Create a TCP receive agent (a traffic sink) and attach it to n5
set end1 [new Agent/TCPSink]
$ns attach-agent $n5 $end1

#Connect the traffic source with the traffic sink
$ns connect $tcp1 $end1
$tcp1 set fid_ 2


set ftp1 [new Application/FTP] 
$ftp1 attach-agent $tcp1 


#Define a 'recv' function for the class 'Agent/Ping'
Agent/Ping instproc recv {from rtt} {
  global rtttrace algorithm
  $self instvar node_
  puts $rtttrace "$algorithm [$node_ id] $from rtt_ $rtt"
}

#Create two ping agents and attach them to the nodes n0 and n2
set p0 [new Agent/Ping]
$ns attach-agent $n0 $p0

set p4 [new Agent/Ping]
$ns attach-agent $n4 $p4

set p1 [new Agent/Ping]
$ns attach-agent $n1 $p1

set p5 [new Agent/Ping]
$ns attach-agent $n5 $p5

#Connect the two agents
$ns connect $p0 $p4
$ns connect $p1 $p5


#Schedule the connection data flow; start sending data at T=0, stop at T=1000.0
$ns at 0 "$ftp0 start"
for { set a 1}  {$a < 1001} {incr a} {
  $ns at $a "$p0 send"
  $ns at $a "$p1 send" 
}
$ns at 0 "$ftp1 start"
$ns at 1000 "$ftp1 stop"
$ns at 1000 "$ftp0 stop"
# Call the finish procedure after 1000 seconds of simulation time 
$ns at 1000 "finish"

# Run the simulation 
$ns run 
