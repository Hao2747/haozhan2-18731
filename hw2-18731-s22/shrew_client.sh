#!/bin/bash 

echo running iperf-client

#TODO: add your code
iperf -c 10.0.0.1 -p 5566 -t 15
iperf -c 10.0.0.1 -u -p 5001 -t 15 -l 1000
