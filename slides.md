---
marp: true
math: mathjax
theme: rose-pine
# theme: rose-pine-dawn
# theme: rose-pine-moon
---

<style lang=css>
/*
Rosé Pine theme create by RAINBOWFLESH
> www.rosepinetheme.com

palette in :root
*/

@import "default";
@import "schema";
@import "structure";

:root {
  --base: #232136;
    --surface: #2a273f;
    --overlay: #393552;
    --muted: #6e6a86;
    --subtle: #908caa;
    --text: #e0def4;
    --love: #eb6f92;
    --gold: #f6c177;
    --rose: #ea9a97;
    --pine: #3e8fb0;
    --foam: #9ccfd8;
    --iris: #c4a7e7;
    --highlight-low: #2a283e;
    --highlight-muted: #44415a;
    --highlight-high: #56526e;

  font-family: Pier Sans, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, Noto Sans,
    sans-serif, "Apple Color Emoji", "Segoe UI Emoji", Segoe UI Symbol,
    "Noto Color Emoji";
  font-weight: initial;

  background-color: var(--base);
}
/*Common style*/
h1 {
  color: var(--rose);
  padding-bottom: 2mm;
  margin-bottom: 12mm;
}
h2 {
  color: var(--rose);
}
h3 {
  color: var(--rose);
}
h4 {
  color: var(--rose);
}
h5 {
  color: var(--rose);
}
h6 {
  color: var(--rose);
}
a {
  color: var(--iris);
}
p {
  font-size: 20pt;
  font-weight: 600;
  color: var(--text);
}
code {
  color: var(--text);
  background-color: var(--highlight-muted);
}
text {
  color: var(--text);
}
ul {
  color: var(--subtle);
}
li {
  color: var(--subtle);
}
img {
  background-color: var(--highlight-low);
}
strong {
  color: var(--text);
  font-weight: inherit;
  font-weight: 800;
}
mjx-container {
  color: var(--text);
}
marp-pre {
  background-color: var(--overlay);
  border-color: var(--highlight-high);
}

/*Code blok*/
.hljs-comment {
  color: var(--muted);
}
.hljs-attr {
  color: var(--foam);
}
.hljs-punctuation {
  color: var(--subtle);
}
.hljs-string {
  color: var(--gold);
}
.hljs-title {
  color: var(--foam);
}
.hljs-keyword {
  color: var(--pine);
}
.hljs-variable {
  color: var(--text);
}
.hljs-literal {
  color: var(--rose);
}
.hljs-type {
  color: var(--love);
}
.hljs-number {
  color: var(--gold);
}
.hljs-built_in {
  color: var(--love);
}
.hljs-params {
  color: var(--iris);
}
.hljs-symbol {
  color: var(--foam);
}
.hljs-meta {
  color: var(--subtle);
}

</style>

---

# **LINFO2347: Network Attacks**

Project 2: Attacks and defenses on Mininet

Rousseau Florent

---

# 1. Port scan

#### RED

- TCP SYN + UDP scan using **Scapy**
- SYN-ACK = open, RST = closed, no reply = filtered
- Configurable port range, targets, timeout

#### BLUE

- Per-IP rate limiting on r2 (meter, 15 SYN/s max)
- UDP from internet to DMZ rejected with ICMP port-unreachable
- Large scans get most ports dropped, small scans still work

---

# 2. SSH brute-force

#### RED

- Tries username/password combinations using **Paramiko**
- Reads from wordlists (users.txt, passwords.txt)
- Stops on first valid credentials found

#### BLUE

- Per-IP rate limit on port 22: max 2 new connections/minute
- Uses nftables meter on both r1 and r2
- After a few attempts, attacker gets timed out

---

# 3. FTP brute-force

#### RED

- Same approach as SSH, using **ftplib** on port 21
- Iterates over all user/password combinations
- Stops on first successful login

#### BLUE

- Per-IP rate limit on port 21: max 2 new connections/minute
- Same meter mechanism as SSH protection
- Loaded on both r1 and r2

---

# 4. ARP cache poisoning

#### RED

- Sends forged ARP replies from ws2 using **Scapy**
- Tells ws3: "r1's IP is at my MAC"
- Tells r1: "ws3's IP is at my MAC"
- Result: MITM, all traffic goes through ws2

#### BLUE

- nftables ARP table on ws3
- Drops ARP replies claiming r1's IP with wrong MAC
- MAC must be updated per Mininet session

---

# 5. DNS reflected DoS

#### RED

- Spoofed DNS queries sent to dns server (port 5353)
- Source IP = victim (ws2), destination = DNS server
- DNS replies flood ws2 with amplified responses

#### BLUE

- Base firewall on r2 blocks this by default
- Spoofed source (10.1.0.2) does not match allow rule (10.2.0.0/24)
- Packets dropped before reaching the DNS server

---

# Thank you

**Any questions?**
