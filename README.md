# LINFO2347 - Project 2

## Author

- Rousseau Florent - 52461900

## Project structure

```
├── topo.py
├── firewall/
│   ├── fw-r1.nft
│   └── fw-r2.nft
├── red/
│   ├── scan.py
│   ├── ssh-bf.py
│   ├── ftp-bf.py
│   ├── arp-poison.py
│   ├── dns-rdos.py
│   └── bf/
│       ├── users.txt
│       └── passwords.txt
├── blue/
│   ├── scan-protection.nft
│   ├── ssh-br-protection.nft
│   ├── ftp-br-protection.nft
│   └── arp-antidote.nft
└── requirements.txt
```

## Network topology

Three zones: Workstations (10.1.0.0/24), DMZ (10.12.0.0/24), Internet (10.2.0.0/24). Two routers: r1 (WS to DMZ) and r2 (DMZ to Internet).

### Routing fix

DMZ servers use r2 as default gateway, which causes routing asymmetry: replies to WS go through r2 instead of r1, and get dropped by conntrack. We added a static route on each DMZ server so that traffic to 10.1.0.0/24 goes through r1.

### Launch

```bash
sudo -E python3 ~/LINFO2347/topo.py
```

## Basic firewall

- Workstations can initiate connections to any host.
- DMZ servers can only respond, never initiate.
- Internet can only initiate towards DMZ, not workstations.

Implemented with connection tracking: `ct state new` packets are filtered based on source/destination, while `established/related` packets are always accepted.

```bash
mininet> r1 nft -f firewall/fw-r1.nft
mininet> r2 nft -f firewall/fw-r2.nft
```

## Attacks and protections

### 1. Port scan

**Attack:** TCP SYN and UDP scan with Scapy. Sends a SYN to each port, a SYN-ACK means the port is open.

```bash
mininet> internet python3 red/scan.py --ports 1-255 --mode tcp --timeout 0.5
```

**Protection:** Per-IP rate limiting on r2. TCP SYN packets over 15/second are dropped. UDP from internet to DMZ is rejected.

```bash
mininet> r2 nft -f blue/scan-protection.nft
```

### 2. SSH brute-force

**Attack:** Tries all username/password combinations from wordlists against SSH using Paramiko.

```bash
mininet> internet python3 red/ssh-bf.py
```

**Protection:** Per-IP rate limit on port 22, max 2 new connections per minute. Loaded on both routers.

```bash
mininet> r1 nft -f blue/ssh-br-protection.nft
mininet> r2 nft -f blue/ssh-br-protection.nft
```

### 3. FTP brute-force

**Attack:** Same as SSH but with ftplib on port 21.

```bash
mininet> internet python3 red/ftp-bf.py
```

**Protection:** Same rate limit as SSH but on port 21. Loaded on both routers.

```bash
mininet> r1 nft -f blue/ftp-br-protection.nft
mininet> r2 nft -f blue/ftp-br-protection.nft
```

### 4. ARP poisoning

**Attack:** Sends fake ARP replies from ws2 to ws3 and r1, redirecting traffic through ws2 (MITM).

```bash
mininet> ws2 python3 red/arp-poison.py &
mininet> ws3 arp -n
```

**Protection:** nftables rule on ws3 that drops ARP replies claiming to be r1 but with a wrong MAC.

```bash
mininet> ws3 nft -f blue/arp-antidote.nft
```

Note: the MAC in `arp-antidote.nft` must be updated to match the current Mininet session since MACs change on restart.

### 5. DNS reflected DoS

**Attack:** Sends spoofed DNS queries to the DNS server with ws2's IP as source. The server replies to ws2 with amplified responses.

```bash
mininet> r2 nft flush ruleset
mininet> ws2 tcpdump -i ws2-eth0 udp &
mininet> internet python3 red/dns-rdos.py
```

**Protection:** The base firewall on r2 already blocks this. The spoofed packets have source IP 10.1.0.2 which does not match the allow rule for 10.2.0.0/24, so they get dropped.

```bash
mininet> r2 nft -f firewall/fw-r2.nft
```
