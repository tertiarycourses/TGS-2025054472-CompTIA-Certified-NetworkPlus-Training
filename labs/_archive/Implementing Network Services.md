# Implementing Network Services

> **Lab Environment:** [Open Ubuntu Playground on Killercoda](https://killercoda.com/playgrounds/scenario/ubuntu)

---

## **Lab** – Explore TCP Three-Way Handshake

### Objective
Understand SYN, SYN-ACK, and ACK packets.

### Commands

```bash
sudo apt update
sudo apt install tcpdump netcat -y
```

**Terminal 1:**
```bash
sudo tcpdump -i any tcp port 8080
```

**Terminal 2:**
```bash
nc -lvp 8080
```

**Terminal 3:**
```bash
nc localhost 8080
```

### Verification
Observe:
- SYN
- SYN-ACK
- ACK

### Key Learning Point
TCP establishes connections using a three-way handshake.

---

## **Lab** – View Open Ports with netstat

### Objective
Identify listening ports.

### Commands

```bash
sudo apt install net-tools -y
netstat -tulnp
```

### Verification
Check active TCP and UDP ports.

### Key Learning Point
netstat helps troubleshoot network services.

---

## **Lab** – Configure a DHCP Server

### Objective
Install and configure ISC DHCP Server.

### Commands

```bash
sudo apt install isc-dhcp-server -y
```

Edit configuration:
```bash
sudo nano /etc/dhcp/dhcpd.conf
```

Add:
```
subnet 192.168.1.0 netmask 255.255.255.0 {
  range 192.168.1.100 192.168.1.150;
  option routers 192.168.1.1;
  option domain-name-servers 8.8.8.8;
}
```

Start service:
```bash
sudo systemctl restart isc-dhcp-server
sudo systemctl status isc-dhcp-server
```

### Verification
DHCP service should be active.

### Key Learning Point
DHCP dynamically assigns IP addresses.

---

## **Lab** – Configure DHCP Server Options

### Objective
Configure DNS and gateway options.

### Commands

Edit:
```bash
sudo nano /etc/dhcp/dhcpd.conf
```

Add:
```
option domain-name "lab.local";
option domain-name-servers 8.8.8.8;
option routers 192.168.1.1;
```

Restart:
```bash
sudo systemctl restart isc-dhcp-server
```

### Verification
Clients receive DNS and gateway information.

### Key Learning Point
DHCP options automate network configuration.

---

## **Lab** – Create DHCP Exclusions

### Objective
Reserve part of the IP range.

### Commands

Configure range:
```
range 192.168.1.100 192.168.1.120;
```

Keep:
```
192.168.1.121–192.168.1.150
```
for static devices.

### Verification
Excluded IPs are not assigned.

### Key Learning Point
Exclusions prevent IP conflicts.

---

## **Lab** – Create DHCP Client Reservations

### Objective
Assign fixed IPs using MAC addresses.

### Commands

Add:
```
host client1 {
  hardware ethernet 08:00:27:12:34:56;
  fixed-address 192.168.1.200;
}
```

Restart:
```bash
sudo systemctl restart isc-dhcp-server
```

### Verification
Reserved client receives fixed IP.

### Key Learning Point
Reservations provide predictable addressing.

---

## **Lab** – Configure Client Addressing for DHCP

### Objective
Enable DHCP on Ubuntu client.

### Commands

```bash
sudo dhclient
ip addr
```

### Verification
Client receives IP automatically.

### Key Learning Point
DHCP clients request addressing dynamically.

---

## **Lab** – Explore APIPA Addressing

### Objective
Understand Automatic Private IP Addressing.

### Commands

Stop DHCP:
```bash
sudo systemctl stop isc-dhcp-server
sudo dhclient -r
sudo dhclient
```

### Verification
Client may receive:
```
169.254.x.x
```

### Key Learning Point
APIPA provides fallback addressing when DHCP fails.

---

## **Lab** – Explore APIPA in Network Modeler

### Objective
Simulate DHCP failure scenarios.

### Activity
- Disable DHCP server
- Observe automatic APIPA assignment

### Verification
Devices communicate only locally.

### Key Learning Point
APIPA is limited to local subnet communication.

---

## **Lab** – Configure a DHCP Relay Agent

### Objective
Forward DHCP requests between subnets.

### Commands

```bash
sudo apt install isc-dhcp-relay -y
```

Configure relay:
```bash
sudo nano /etc/default/isc-dhcp-relay
```

Set:
```
SERVERS="192.168.1.10"
```

Restart:
```bash
sudo systemctl restart isc-dhcp-relay
```

### Verification
Relay forwards DHCP broadcasts.

### Key Learning Point
Relay agents enable centralized DHCP services.

---

## **Lab** – Add DHCP Server on Another Subnet

### Objective
Support multiple subnets.

### Commands

Add subnet:
```
subnet 192.168.2.0 netmask 255.255.255.0 {
  range 192.168.2.100 192.168.2.150;
}
```

Restart:
```bash
sudo systemctl restart isc-dhcp-server
```

### Verification
Clients on another subnet receive IPs.

### Key Learning Point
DHCP can manage multiple subnet scopes.

---

## **Lab** – Troubleshoot Address Pool Exhaustion

### Objective
Identify exhausted DHCP ranges.

### Commands

Use small pool:
```
range 192.168.1.100 192.168.1.101;
```

Check logs:
```bash
sudo journalctl -u isc-dhcp-server
```

### Verification
New clients fail to obtain IP addresses.
