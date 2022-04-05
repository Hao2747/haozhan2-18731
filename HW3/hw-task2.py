
 
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf,TCLink
 
def aggNet():
 
    CONTROLLER_IP='127.0.0.1'
 
    net = Mininet( topo=None,link = TCLink,
                build=False)
 
    net.addController( 'c0',
                    controller=RemoteController,
                    ip=CONTROLLER_IP,
                    port=6633)
 
    h1 = net.addHost( 'h1', ip='10.1.1.1' )
    h2 = net.addHost( 'h2', ip='10.1.2.1' )
    h3 = net.addHost( 'h3', ip='10.2.1.1' )
    h4 = net.addHost( 'h4', ip='10.3.1.1' )
    h5 = net.addHost( 'h5', ip='10.3.2.1' )
    h6 = net.addHost( 'h6', ip='10.3.3.1' )
    
    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )
    s3 = net.addSwitch( 's3' )
    
    net.addLink( h1, s1 )
    net.addLink( h2, s1 )
   # net.addLink( h3, s2)
    net.addLink( h3, s2, delay = "2000ms" )
    net.addLink( h4, s3 )
    net.addLink( h5, s3 )
    net.addLink( h6, s3 )

    net.addLink( s1, s2 )
    net.addLink( s2, s3 )
 
    net.start()
    CLI( net )
    net.stop()
 
if __name__ == '__main__':
    setLogLevel( 'info' )
    aggNet()
