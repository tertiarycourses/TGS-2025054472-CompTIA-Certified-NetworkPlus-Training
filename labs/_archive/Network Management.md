# Network Management

> **Lab Environment:** [Open Ubuntu Playground on Killercoda](https://killercoda.com/playgrounds/scenario/ubuntu)

---

## **Lab** – Backup and Restore Network Appliances

### Objective
Create and restore configuration backups.

### Commands

Create backup:
```bash
tar -czvf network-backup.tar.gz /etc
```

Restore backup:
```bash
tar -xzvf network-backup.tar.gz -C /
```

### Verification
Backup archive is created successfully.

### Key Learning Point
Backups help recover configurations quickly.

---

## **Lab** – Update Firmware

### Objective
Update Ubuntu packages and firmware.

### Commands

```bash
sudo apt update
sudo apt upgrade -y
```

Check firmware:
```bash
sudo fwupdmgr get-devices
```

### Verification
System packages update successfully.

### Key Learning Point
Firmware and software updates improve security and stability.

---

## **Lab** – Update Network Documentation

### Objective
Document network configuration details.

### Commands

Export IP configuration:
```bash
ip addr > network-info.txt
```

Export routes:
```bash
ip route >> network-info.txt
```

View file:
```bash
cat network-info.txt
```

### Verification
Documentation file contains network details.

### Key Learning Point
Accurate documentation simplifies troubleshooting.

---

## **Lab** – Scan Using Zenmap

### Objective
Understand graphical Nmap scanning concepts.

### Commands

Install Nmap:
```bash
sudo apt install nmap -y
```

Basic scan:
```bash
nmap localhost
```

### Verification
Open ports are displayed.

### Key Learning Point
Zenmap is the graphical interface for Nmap scanning.

---

## **Lab** – Perform Network Discovery

### Objective
Discover active devices on a network.

### Commands

```bash
sudo apt install nmap -y
```

Ping sweep:
```bash
nmap -sn 192.168.1.0/24
```

### Verification
Active hosts are identified.

### Key Learning Point
Network discovery identifies reachable systems.

---

## **Lab** – Configure SNMP

### Objective
Install and configure SNMP service.

### Commands

Install SNMP:
```bash
sudo apt install snmpd -y
```

Check service:
```bash
sudo systemctl status snmpd
```

Test SNMP:
```bash
snmpwalk -v2c -c public localhost
```

### Verification
SNMP responses are displayed.

### Key Learning Point
SNMP enables network monitoring and management.

---

## **Lab** – Configure Logging in pfSense

### Objective
Understand centralized firewall logging.

### Activity
- Review pfSense logging concepts
- Identify firewall log categories

### Verification
Firewall events can be monitored.

### Key Learning Point
Logs help detect security and connectivity issues.

---

## **Lab** – Evaluate Event Logs in pfSense

### Objective
Analyze firewall event logs.

### Commands

Ubuntu log example:
```bash
sudo journalctl
```

Filter logs:
```bash
sudo journalctl -p err
```

### Verification
Error logs are displayed.

### Key Learning Point
Event logs provide troubleshooting information.

---

## **Lab** – Auditing Device Logs on a Cisco Switch

### Objective
Review switch logging concepts.

### Commands

Linux syslog example:
```bash
sudo tail -f /var/log/syslog
```

### Verification
System log entries appear in real time.

### Key Learning Point
Auditing logs helps monitor device activity.

---

## **Lab** – Configure Logging on Linux

### Objective
Manage Linux logging services.

### Commands

Check rsyslog:
```bash
sudo systemctl status rsyslog
```

Restart service:
```bash
sudo systemctl restart rsyslog
```

### Verification
rsyslog service is active.

### Key Learning Point
Linux uses rsyslog for centralized logging.

---

## **Lab** – View Event Logs

### Objective
View and filter system logs.

### Commands

View logs:
```bash
sudo journalctl
```

View recent logs:
```bash
sudo journalctl -n 20
```

### Verification
Recent system events are displayed.

### Key Learning Point
Event logs assist with monitoring and troubleshooting.

---

## **Lab** – Configure Log Collection

### Objective
Collect centralized logs.

### Commands

Install rsyslog:
```bash
sudo apt install rsyslog -y
```

Check listening ports:
```bash
sudo netstat -tulnp | grep rsyslog
```

### Verification
Log service is operational.

### Key Learning Point
Centralized logging improves monitoring efficiency.

---

## **Lab** – Troubleshoot with Wireshark

### Objective
Capture and analyze packets.

### Commands

Install tcpdump:
```bash
sudo apt install tcpdump -y
```

Capture traffic:
```bash
sudo tcpdump -i any
```

### Verification
Packets are captured successfully.

### Key Learning Point
Packet analysis helps identify network problems.

---

## **Lab** – Configure Port Mirroring

### Objective
Understand traffic monitoring concepts.

### Commands

Capture interface traffic:
```bash
sudo tcpdump -i eth0
```

### Verification
Traffic from the selected interface is displayed.

### Key Learning Point
Port mirroring copies traffic for analysis.

---

## **Lab** – Configure QoS

### Objective
Understand traffic prioritization.

### Commands

View queue disciplines:
```bash
tc qdisc show
```

Add traffic shaping:
```bash
sudo tc qdisc add dev eth0 root tbf rate 1mbit burst 32kbit latency 400ms
```

### Verification
QoS rule appears in qdisc output.

### Key Learning Point
QoS prioritizes important network traffic.

---

## **Lab** – Configure Flow Monitoring

### Objective
Monitor network traffic flow.

### Commands

Install iftop:
```bash
sudo apt install iftop -y
```

Run monitoring:
```bash
sudo iftop
```

### Verification
Real-time traffic statistics are displayed.

### Key Learning Point
Flow monitoring helps understand network bandwidth usage.
