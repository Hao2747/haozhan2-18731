#qsize=$1
echo set iperf-server

iperf -s -u -p 5006 -t 400 

killall -9 iperf ping
echo "end Server"
