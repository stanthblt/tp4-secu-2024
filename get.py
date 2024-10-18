import scapy.all as scapy 

def get_mac(ip):
    request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    final_packet = broadcast / request
    answer = scapy.srp(final_packet, timeout=2, verbose=False)[0]
    mac = answer[0][1].hwsrc
    return mac

answer = get_mac("10.33.73.226")

print(answer)