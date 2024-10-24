import sys
from scapy.all import *

def process_icmp_packet(packet):
    if ICMP in packet and packet[ICMP].type == 8: 
        data = bytes(packet[ICMP].payload) 
        if data:
            char = data.decode(errors="ignore")
            print(char)
            sys.exit(0)

def start_sniffing():
    sniff(filter="icmp", prn=process_icmp_packet)

if __name__ == "__main__":
    start_sniffing()
