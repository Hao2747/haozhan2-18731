#qsize=$1
echo set iperf-server

#TODO: add your code
iperf -s -p 5566 -i 1
iperf -s -u -p 5001 -t 15 

