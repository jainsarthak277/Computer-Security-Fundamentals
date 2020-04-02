#!/usr/bin/python3

import dpkt
import socket
import sys

def toStr(ip_addr):
	""" Convert ip in binary to string 
		ip_addr - ip address in binary
		return - ip address in string
		Reference: https://stackoverflow.com/questions/44502232/how-can-i-decode-print-an-ipv6-address-in-python"""

	try:
		return socket.inet_ntop(socket.AF_INET,ip_addr)
	except ValueError:
		return socket.inet_ntop(socket.AF_INET6,ip_addr)

def detect_scanners(pcap_file):
	""" read through pcap file and check for ip addr involved in port scanning
		pcap_file - pcap file to be traversed 
		Reference:  https://jon.oberheide.org/blog/2008/10/15/dpkt-tutorial-2-parsing-a-pcap-file/"""

	f = open(pcap_file, 'rb')
	pcap = dpkt.pcap.Reader(f)

	pkts_syn = {} #Contains count of TCP SYN packets sent out by each ip address
	pkts_syn_ack = {} #Contains count of TCP SYN + ACK packets received by each ip address 

	for ts,buf in pcap:
		
		#Ignore NeedData exception
		try:
			eth = dpkt.ethernet.Ethernet(buf)
		except dpkt.dpkt.NeedData:
			continue

		#Check for IP packets	
		if isinstance(eth.data, dpkt.ip.IP):
			ip = eth.data

			#Check for TCP packets
			if isinstance(ip.data, dpkt.tcp.TCP):
				tcp = ip.data

				#Check for SYN packets
				if (tcp.flags & dpkt.tcp.TH_SYN) and not(tcp.flags & dpkt.tcp.TH_ACK):
					
					if ip.src in pkts_syn:
						pkts_syn[ip.src] += 1
					else:
						pkts_syn[ip.src] = 1

				#Check for SYN + ACK packets
				if (tcp.flags & dpkt.tcp.TH_SYN) and (tcp.flags & dpkt.tcp.TH_ACK):
					if ip.dst in pkts_syn_ack:
						pkts_syn_ack[ip.dst] += 1
					else:
						pkts_syn_ack[ip.dst] = 1

	for ip_addr in pkts_syn:

		if ip_addr in pkts_syn_ack:
			if (pkts_syn[ip_addr] > 3*(pkts_syn_ack[ip_addr])):
				print(toStr(ip_addr))

		else:
			print(toStr(ip_addr)) #If IP addr sends out SYN pkt but does not receive any SYN+ACK, still counted as port scanning 

def main():
	""" main function to parse command line arguments """
	
	# Checking if pcap file is specified
	if(len(sys.argv) != 2):
		print("Few/extra arguments specified")
		sys.exit()

	detect_scanners(sys.argv[1])

if __name__ == '__main__':
    main()