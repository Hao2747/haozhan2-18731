# CMU 18731 HW2
# Code referenced from: git@bitbucket.org:huangty/cs144_bufferbloat.git
# Edited by: Soo-Jin Moon, Deepti Sunder Prakash

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
    def build(self, n=6, bw_net=100, delay='20ms', bw_host=10, maxq=1000):
    #TODO: Add your code to create topology
	Host1 = self.addHost( 'hl1' )
        Host2 = self.addHost( 'hl2' )
        Host3 = self.addHost( 'a1' )
        Host4 = self.addHost( 'hr1' )
        Host5 = self.addHost( 'hr2' )
        Host6 = self.addHost( 'a2' )
        Switch1 = self.addSwitch('s1')
        Switch2 = self.addSwitch('s2')
        # Add links
        self.addLink(Host1,Switch1,bw= bw_host,delay = delay)

        self.addLink( Host1, Switch1, bw=bw_host, delay = delay)
        self.addLink( Host2, Switch1, bw=bw_host, delay = delay)
        self.addLink( Host3, Switch1, bw=bw_host, delay = delay)
        self.addLink( Host4, Switch2, bw=bw_host, delay = delay)
        self.addLink( Host5, Switch2, bw=bw_host, delay = delay)
        self.addLink( Host6, Switch2, bw=bw_host, delay = delay)
        self.addLink( Switch1, Switch2,bw=bw_net, delay = delay )
		
	
def bbnet():
    "Create network and run shrew  experiment"
    print "starting mininet ...."
    topo = DumbbellTopo(n=args.n, bw_net=args.bw_net,
                    delay='%sms' % (args.delay),
                    bw_host=args.bw_host, maxq=int(args.maxq))

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink,
                  autoPinCpus=True)
    net.start()
    dumpNodeConnections(net.hosts)

    #TODO: Add your code to test reachability of hosts
    net.pingAll()
    #TODO: Add yoour code to start long lived TCP flows 
    hl1, hr1 = net.get('hl1','hr1')
    net.iperf((hl1,hr1), port=5001) 

    hl2, hr2 = net.get('hl2','hr2')
    net.iperf((hl2,hr2), port=5002) 
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    bbnet()
