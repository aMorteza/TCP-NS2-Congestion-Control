BEGIN {
  recvdSize = 0
  startTime = 0
  stopTime = 0
  }
   
  {
   event = $1
   time = $2
   node_id = $3
   pkt_size = $6
    
  # Update total received packets' size and store packets arrival time
  if ((event == "r") && pkt_size >= 1000) {
       if (time > stopTime) {
             stopTime = time
             }
       # Rip off the header
       #hdr_size = pkt_size % 1000
       #pkt_size -= hdr_size
       # Store received packet's size
       recvdSize += pkt_size
       }
  }
   
  END {
    printf("Average Throughput[kbps] = %.2f\t\t    StartTime=%.2f\tStopTime=%.2f\n",(recvdSize/(stopTime-startTime))*(8/1000),startTime,stopTime)
  }
