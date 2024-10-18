from scapy.all import *

ping = ICMP(type=8)

packet = IP(src="10.33.67.174", dst="10.33.73.226")

frame = Ether(src="f2:39:c5:c0:07:e5", dst="c8:5e:a9:3e:3e:fb")

final_frame = frame/packet/ping

answers, unanswered_packets = srp(final_frame, timeout=10)

print(f"Pong reçu : {answers[0]}")
