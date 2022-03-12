#qsize=$1
echo set iperf-server

#TODO: add your code
#iperf -s -p 5566 -i 1 &
iperf -s -u -p 5006 -t 15 


killall -9 iperf ping
echo "end Server"