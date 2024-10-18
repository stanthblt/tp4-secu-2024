from scapy.all import *

Ip_req = IP(dst='8.8.8.8')

port_req = UDP(dport=53)

dns_req = DNS(rd=1, qd=DNSQR(qname='www.ynov.com'))    
    
final_req = Ip_req/port_req/dns_req

answer = sr1(final_req, verbose=0)

print(answer[DNS].summary())