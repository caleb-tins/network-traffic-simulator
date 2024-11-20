// Device Class
class Device {
    constructor(ip) {
        this.ip = ip;
    }

    sendPacket(targetIp) {
        const size = Math.floor(Math.random() * 1400) + 100; // Packet size: 100-1500 bytes
        const isMalicious = Math.random() < 0.1; // 10% chance malicious
        const packetType = ["TCP", "UDP", "ICMP"][Math.floor(Math.random() * 3)];
        const latency = Math.floor(Math.random() * 100); // Latency in ms
        const dropped = Math.random() < 0.05; // 5% chance of being dropped
        return new Packet(this.ip, targetIp, size, isMalicious, packetType, latency, dropped);
    }
}

// Packet Class
class Packet {
    constructor(sourceIp, destinationIp, size, isMalicious, packetType, latency, dropped) {
        this.sourceIp = sourceIp;
        this.destinationIp = destinationIp;
        this.size = size;
        this.isMalicious = isMalicious;
        this.packetType = packetType;
        this.latency = latency;
        this.dropped = dropped;
    }

    render() {
        const status = this.dropped
            ? "Dropped"
            : this.isMalicious
            ? "Malicious"
            : "Safe";
        const className = this.dropped
            ? "dropped"
            : this.isMalicious
            ? "malicious"
            : "safe";
        return `<div class="packet ${className}">
            <strong>Packet:</strong> ${this.sourceIp} → ${this.destinationIp} 
            | <strong>Type:</strong> ${this.packetType} 
            | <strong>Size:</strong> ${this.size} bytes 
            | <strong>Latency:</strong> ${this.latency}ms 
            | <strong>Status:</strong> ${status}
        </div>`;
    }
}

// Network Class
class Network {
    constructor() {
        this.devices = [];
    }

    addDevice(ip) {
        this.devices.push(new Device(ip));
    }

    simulateTraffic(numPackets = 10, scenario = "normal") {
        const packets = [];
        for (let i = 0; i < numPackets; i++) {
            const sender = this.devices[Math.floor(Math.random() * this.devices.length)];
            let receiver = this.devices[Math.floor(Math.random() * this.devices.length)];
            while (receiver.ip === sender.ip) {
                receiver = this.devices[Math.floor(Math.random() * this.devices.length)];
            }

            let packet;
            if (scenario === "normal") {
                packet = sender.sendPacket(receiver.ip);
            } else if (scenario === "ddos") {
                packet = new Packet(sender.ip, receiver.ip, 64, true, "TCP", Math.floor(Math.random() * 10), false);
            } else if (scenario === "streaming") {
                packet = new Packet(sender.ip, receiver.ip, Math.floor(Math.random() * 500) + 1000, false, "UDP", Math.floor(Math.random() * 50) + 20, false);
            }

            packets.push(packet);
        }
        return packets;
    }
}

// Display Packets
function displayPackets(packets) {
    const output = document.getElementById("output");
    output.innerHTML = ""; // Clear previous output

    packets.forEach(packet => {
        output.innerHTML += packet.render();
    });

    const maliciousCount = packets.filter(p => p.isMalicious).length;
    output.innerHTML += `<p><strong>Total Packets:</strong> ${packets.length}</p>`;
    output.innerHTML += `<p><strong>Malicious Packets:</strong> ${maliciousCount}</p>`;
}

// Initialize the network
const network = new Network();
network.addDevice("192.168.1.1");
network.addDevice("192.168.1.2");
network.addDevice("192.168.1.3");

document.getElementById("simulateNormal").addEventListener("click", () => {
    displayPackets(network.simulateTraffic(15, "normal"));
});

document.getElementById("simulateDDoS").addEventListener("click", () => {
    displayPackets(network.simulateTraffic(15, "ddos"));
});

document.getElementById("simulateStreaming").addEventListener("click", () => {
    displayPackets(network.simulateTraffic(15, "streaming"));
});