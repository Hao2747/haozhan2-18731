#!/bin/bash 

echo running iperf-client

#TODO: add your code
iperf -c <server ip> -p 5566 -t 15
iperf -c -u -p 5001 -t 15 -l 1000
