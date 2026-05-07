from scapy.all import ICMP, IP, TCP, UDP, send, sr1


def scan_host(ip, port_range):
    start, end = port_range
    open_ports = {"tcp": [], "udp": []}

    for port in range(start, end + 1):
        state = tcp_syn_scan(ip, port)
        if state == "open":
            open_ports["tcp"].append(port)
        state = udp_scan(ip, port)
        if state in ("open", "open|filtered"):
            open_ports["udp"].append(port)

    return open_ports


def tcp_syn_scan(ip, port):
    packet = IP(dst=ip) / TCP(dport=port, flags="S")
    response = sr1(packet, timeout=1, verbose=0)

    if response is None:
        return "filtered"

    if response.haslayer(TCP):
        tcp_flags = response[TCP].flags
        if tcp_flags == 0x12:  # SYN-ACK
            send_rst = IP(dst=ip) / TCP(dport=port, flags="R")
            send(send_rst, verbose=0)
            return "open"
        if tcp_flags == 0x14:  # RST-ACK
            return "closed"
    return "filtered"


def udp_scan(ip, port):
    packet = IP(dst=ip) / UDP(dport=port)
    response = sr1(packet, timeout=1, verbose=0)

    if response is None:
        return "open|filtered"

    if response.haslayer(ICMP):
        icmp_type = response[ICMP].type
        icmp_code = response[ICMP].code
        if icmp_type == 3 and icmp_code in [1, 2, 3, 9, 10, 13]:
            return "closed"
    return "open|filtered"


def main():
    port_range = (1, 100)
    targets = [
        ("http", "10.12.0.10"),
        ("dns", "10.12.0.20"),
        ("ntp", "10.12.0.30"),
        ("ftp", "10.12.0.40"),
        ("internet", "10.2.0.2"),
        ("ws2", "10.1.0.2"),
        ("ws3", "10.1.0.3"),
    ]

    results = {}

    for label, ip in targets:
        print(f"Scanning {label} ({ip})...")
        result = scan_host(ip, port_range)
        results[(ip, label)] = result
        print(f"Open TCP ports: {result['tcp']}")
        print(f"Open UDP ports: {result['udp']}\n")


if __name__ == "__main__":
    main()
