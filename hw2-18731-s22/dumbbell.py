# CMU 18731 HW2
# Code referenced from: git@bitbucket.org:huangty/cs144_bufferbloat.git
# Edited by: Soo-Jin Moon, Deepti Sunder Prakash
# Author: Hao Zhang
#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

import sys
import os

# Parse arguments

parser = ArgumentParser(description="Shrew tests")
parser.add_argument('--bw-host', '-B',
                    dest="bw_host",
                    type=float,
                    action="store",
                    help="Bandwidth of host links",
                    required=True)
parser.add_argument('--bw-net', '-b',
                    dest="bw_net",
                    type=float,
                    action="store",
                    help="Bandwidth of network link",
                    required=True)
parser.add_argument('--delay',
                    dest="delay",
                    type=float,
                    help="Delay in milliseconds of host links",
                    default='10ms')
parser.add_argument('--n',
                    dest="n",
                    type=int,
                    action="store",
                    help="Number of nodes in one side of the dumbbell.",
                    required=True)

parser.add_argument('--maxq',
                    dest="maxq",
                    action="store",
                    help="Max buffer size of network interface in packets",
                    default=1000)

# Expt parameters
args = parser.parse_args()

class DumbbellTopo(Topo):
    "Dumbbell topology for Shrew experiment"
    def build(self, n=6, bw_net=100, delay='20ms', bw_host=10, maxq=None):
    #TODO: Add your code to create topology
        switch1 = self.addSwitch('s1')
        for h in range(2):
            host = self.addHost('hl%s' % (h+1))
            self.addLink(host,switch1,bw=bw_host,delay = delay, max_queue_size = max_q)
        host = self.addHost('a1')
        self.addLink(host,switch1,bw=bw_host,delay = delay, max_queue_size = max_q)

		
        switch2= self.addSwitch('s2')
        for h in range(2):
            host = self.addHost('hr%s' % (h+1))
            self.addLink(host,switch2,bw=bw_host,delay = delay, max_queue_size = max_q)
        host = self.addHost('a2')
        self.addLink(host,switch2,bw=bw_host,delay = delay, max_queue_size = max_q)

        self.addLink(switch1,switch2,bw=bw_net,delay= delay, max_queue_size = max_q)
	
def bbnet():
    "Create network and run shrew  experiment"
    print "starting mininet ...."
    topo = DumbbellTopo(n=args.n, bw_net=args.bw_net,
                    delay='%sms' % (args.delay),
                    bw_host=args.bw_host, maxq=int(args.maxq))

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink,
                  autoPinCpus=True)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing Network Connectivity")

    net.pingAll()
    #TODO: Add yoour code to start long lived TCP flows 
  
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    bbnet()
