#!/bin/bash 

echo running iperf-client

#TODO: add your code
#iperf -c 10.0.0.1 -p 5566 -t 15 &
#iperf -c 10.0.0.1 -u -p 5006 -t 15 -l 100000 -i 1
#iperf -u -c 10.0.0.1 -b 10M -p 5006 -t 15
for i in {1..200}
do
    iperf -u -c 10.0.0.1 -b 10M -p 5006 -t 0.25 
    sleep 0.75
done


killall -9 iperf ping
echo "end Client"
