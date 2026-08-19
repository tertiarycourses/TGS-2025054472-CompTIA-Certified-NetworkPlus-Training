# Explaining Application Services

> **Lab Environment:** [Open Ubuntu Playground on Killercoda](https://killercoda.com/playgrounds/scenario/ubuntu)

---

## **Lab** – Configure NTP on Linux

### Objective
Configure time synchronization using NTP.

### Commands

Install Chrony:
```bash
sudo apt update
sudo apt install chrony -y
```

Check status:
```bash
chronyc tracking
chronyc sources
```

Restart service:
```bash
sudo systemctl restart chrony
```

### Verification
Time synchronization status should show active.

### Key Learning Point
NTP keeps system clocks synchronized.

---

## **Lab** – Troubleshoot Time Synchronization Issues

### Objective
Identify and fix NTP synchronization problems.

### Commands

Check service:
```bash
sudo systemctl status chrony
```

Check logs:
```bash
journalctl -u chrony
```

Test connectivity:
```bash
ping pool.ntp.org
```

Restart:
```bash
sudo systemctl restart chrony
```

### Verification
Chrony service becomes active and synchronized.

### Key Learning Point
Time synchronization depends on service status and network connectivity.

---

## **Lab** – Verify Secure Web Services

### Objective
Verify HTTPS connectivity and certificates.

### Commands

Install curl:
```bash
sudo apt install curl -y
```

Test HTTPS:
```bash
curl -I https://google.com
```

Check certificate:
```bash
openssl s_client -connect google.com:443
```

### Verification
HTTPS response and SSL certificate details appear.

### Key Learning Point
HTTPS secures web traffic using SSL/TLS.

---

## **Lab** – Scan for Web Services with Nmap

### Objective
Identify active web service ports.

### Commands

Install Nmap:
```bash
sudo apt install nmap -y
```

Scan localhost:
```bash
nmap localhost
```

Scan web ports:
```bash
nmap -p 80,443 localhost
```

### Verification
Open HTTP/HTTPS ports are displayed.

### Key Learning Point
Nmap helps identify running network services.

---

## **Lab** – Connect VoIP 1

### Objective
Verify basic VoIP connectivity.

### Commands

Test network reachability:
```bash
ping google.com
```

Check SIP port:
```bash
sudo netstat -tulnp | grep 5060
```

### Verification
SIP port information is displayed.

### Key Learning Point
VoIP commonly uses SIP protocol on port 5060.

---

## **Lab** – Connect VoIP 2

### Objective
Test VoIP-related traffic.

### Commands

Install tcpdump:
```bash
sudo apt install tcpdump -y
```

Capture SIP traffic:
```bash
sudo tcpdump -i any port 5060
```

### Verification
SIP packets are captured.

### Key Learning Point
Packet capture tools help troubleshoot VoIP traffic.

---

## **Lab** – Configure NIC Teaming

### Objective
Understand NIC bonding/teaming basics.

### Commands

View interfaces:
```bash
ip addr
```

Load bonding module:
```bash
sudo modprobe bonding
```

Check bonding module:
```bash
lsmod | grep bonding
```

### Verification
Bonding module loads successfully.

### Key Learning Point
NIC teaming improves redundancy and performance.

---

## **Lab** – Configure First Hop Redundancy

### Objective
Understand gateway redundancy concepts.

### Commands

View routing table:
```bash
ip route
```

Check gateway:
```bash
ping -c 4 8.8.8.8
```

### Verification
Default gateway connectivity is successful.

### Key Learning Point
First Hop Redundancy Protocol (FHRP) provides gateway failover capabilities.
