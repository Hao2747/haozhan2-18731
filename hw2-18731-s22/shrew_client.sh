#!/bin/bash 

echo running iperf-client

#TODO: add your code
iperf -c <server ip> -p 5566 -t 15
