import random

class Packet:
    def __init__(self, source_ip, destination_ip, size, is_malicious, packet_type, latency, dropped):
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.size = size
        self.is_malicious = is_malicious
        self.packet_type = packet_type
        self.latency = latency
        self.dropped = dropped

    def __str__(self):
        status = "Dropped" if self.dropped else ("Malicious" if self.is_malicious else "Safe")
        return (f"Packet: {self.source_ip} -> {self.destination_ip} | "
                f"Type: {self.packet_type} | Size: {self.size} bytes | "
                f"Latency: {self.latency}ms | Status: {status}")


class Device:
    def __init__(self, ip):
        self.ip = ip

    def send_packet(self, target_ip):
        size = random.randint(100, 1500)
        is_malicious = random.random() < 0.1
        packet_type = random.choice(["TCP", "UDP", "ICMP"])
        latency = random.randint(1, 100)  # Simulate latency in ms
        dropped = random.random() < 0.05  # 5% chance of being dropped
        return Packet(self.ip, target_ip, size, is_malicious, packet_type, latency, dropped)


class Network:
    def __init__(self):
        self.devices = []  # Initialize the list of devices
        self.blocked_ips = set()  # Set of blocked IPs
        self.blocked_types = set()  # Set of blocked packet types

    def add_device(self, ip):
        self.devices.append(Device(ip))  # Add a device to the network

    def block_ip(self, ip):
        self.blocked_ips.add(ip)

    def block_packet_type(self, packet_type):
        self.blocked_types.add(packet_type)

    def simulate_traffic(self, num_packets=10, scenario="normal"):
        if len(self.devices) < 2:
            print("Not enough devices to simulate traffic!")
            return []

        packets = []

        for _ in range(num_packets):
            sender = random.choice(self.devices)
            receiver = random.choice(self.devices)
            while receiver.ip == sender.ip:
                receiver = random.choice(self.devices)

            if scenario == "normal":
                packet = sender.send_packet(receiver.ip)
            elif scenario == "ddos":
                packet = Packet(sender.ip, receiver.ip, 64, True, "TCP", random.randint(1, 5), False)
            elif scenario == "streaming":
                packet = Packet(sender.ip, receiver.ip, random.randint(1000, 1500), False, "UDP", random.randint(20, 50), False)

            # Apply filtering rules
            if packet.source_ip in self.blocked_ips or packet.packet_type in self.blocked_types:
                continue  # Drop the packet if it matches any blocked rule

            packets.append(packet)
        return packets


def main():
    network = Network()

    # Add devices
    network.add_device("192.168.0.1")
    network.add_device("192.168.0.2")
    network.add_device("192.168.0.3")

    print("Welcome to the Network Traffic Simulator!")
    scenario = input("Enter the traffic scenario (normal, ddos, streaming): ").strip().lower()
    num_packets = int(input("Enter the number of packets to simulate: "))
    
    block_ip = input("Enter an IP to block (or leave blank): ").strip()
    if block_ip:
        network.block_ip(block_ip)
    
    block_type = input("Enter a packet type to block (TCP, UDP, ICMP, or leave blank): ").strip().upper()
    if block_type:
        network.block_packet_type(block_type)

    print("\nSimulating network traffic...\n")
    packets = network.simulate_traffic(num_packets, scenario)

    # Display packets
    for packet in packets:
        print(packet)

    # Analyze traffic
    malicious_packets = [p for p in packets if p.is_malicious]
    tcp_packets = [p for p in packets if p.packet_type == "TCP"]
    udp_packets = [p for p in packets if p.packet_type == "UDP"]
    icmp_packets = [p for p in packets if p.packet_type == "ICMP"]
    average_latency = sum(p.latency for p in packets) / len(packets) if packets else 0

    print(f"\nTraffic Analysis:")
    print(f"Total Packets: {len(packets)}")
    print(f"Malicious Packets: {len(malicious_packets)}")
    print(f"TCP Packets: {len(tcp_packets)}")
    print(f"UDP Packets: {len(udp_packets)}")
    print(f"ICMP Packets: {len(icmp_packets)}")
    print(f"Average Latency: {average_latency:.2f} ms")


if __name__ == "__main__":
    main()