#qsize=$1
echo set iperf-server

#TODO: add your code
iperf -s -p 5566 -i 1
