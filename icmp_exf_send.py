import sys
from scapy.all import IP, ICMP, send

def send_icmp_data(ip, char):
    packet = IP(dst=ip) / ICMP() / char.encode()
    send(packet, verbose=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python icmp_ext_send.py <destination_ip> <character>")
    else:
        destination_ip = sys.argv[1]
        character = sys.argv[2]
        send_icmp_data(destination_ip, character)