# CompTIA Certified Network+ Training (N10-009) — Lab Index

All 36 hands-on labs for the WSQ course **CompTIA Certified Network+ Training (N10-009)** (TGS-2025054472), organised by the five official N10-009 exam domains. Each lab lives in its own folder with a README containing the full step-by-step commands.

## Lab environment (all free, browser-based)

- **Killercoda Ubuntu Playground** (every Linux lab): https://killercoda.com/playgrounds/scenario/ubuntu
- **TIS IP Calculator** (subnetting): https://alfredang.github.io/ipcalculator/
- **TIS PCAP Analyzer** (packet captures): https://alfredang.github.io/pcapanalyzer/
- **TIS Cybersecurity Simulator** (attack recognition): https://alfredang.github.io/cybersecuritysimulator/
- **TIS Regex Generator** (log filtering): https://alfredang.github.io/regexgenerator/

No installs are needed on your own machine — packages are pulled with `apt` inside the throw-away VM. Lab 11 (Wireless) optionally uses your own laptop's Wi-Fi radio.

See [tools.md](tools.md) for every free tool used, with install commands.

## Domain 1.0 — Networking Concepts  (23%)

| # | Lab | Tools | Files in the lab folder |
|---|-----|-------|-------------------------|
| 1 | [OSI Model Packet Inspection](lab-01-osi-packet-inspection/README.md) | tcpdump, curl, Killercoda Ubuntu, TIS PCAP Analyzer (alfredang.github.io/pcapanalyzer) | `checklist.md`, `run.sh`, `verify.sh` |
| 2 | [IPv4 Subnetting and CIDR](lab-02-ipv4-subnetting/README.md) | TIS IP Calculator (alfredang.github.io/ipcalculator), iproute2, Killercoda Ubuntu | `answers.md`, `checklist.md`, `data/subnet-plan.csv` |
| 3 | [IPv6 Addressing and Link-Local](lab-03-ipv6-slaac/README.md) | TIS IP Calculator (alfredang.github.io/ipcalculator), iproute2, ping6, Killercoda | `answers.md`, `checklist.md`, `verify.sh` |
| 4 | [Common Ports and Protocols](lab-04-common-ports/README.md) | nmap, ss, net-tools (netstat), getent, Killercoda Ubuntu | `checklist.md`, `data/well-known-ports.csv` |
| 5 | [DNS Record Types](lab-05-dns-records/README.md) | dig, nslookup, host (dnsutils), Killercoda Ubuntu | `checklist.md`, `run.sh`, `data/dns-records.csv` |
| 6 | [DHCP Lease Capture (DORA)](lab-06-dhcp-capture/README.md) | isc-dhcp-client (dhclient), tcpdump, Killercoda Ubuntu | `checklist.md`, `cleanup.sh`, `run.sh` |
| 7 | [Simulating a Cloud VPC with Namespaces](lab-07-cloud-vpc-namespaces/README.md) | iproute2 (ip netns, ip link, veth, bridge), Killercoda Ubuntu | `checklist.md`, `cleanup.sh`, `setup.sh`, `verify.sh` |

## Domain 2.0 — Network Implementation  (20%)

| # | Lab | Tools | Files in the lab folder |
|---|-----|-------|-------------------------|
| 8 | [Static Routing Between Two Subnets](lab-08-static-routing/README.md) | iproute2, ip netns, sysctl | `checklist.md`, `cleanup.sh`, `setup.sh`, `verify.sh`, `data/routing-table.csv` |
| 9 | [802.1Q VLAN Tagging](lab-09-vlan-tagging/README.md) | iproute2, 8021q module, tcpdump | `checklist.md`, `cleanup.sh`, `setup.sh`, `verify.sh`, `data/vlan-plan.csv` |
| 10 | [Link Aggregation (LACP Bond)](lab-10-link-aggregation/README.md) | ifenslave, bonding module, iproute2 | `checklist.md`, `cleanup.sh`, `setup.sh`, `verify.sh` |
| 11 | [Wireless Concepts and Channel Survey](lab-11-wireless-concepts/README.md) | iw, wavemon, WiFi Analyzer (Windows), Wireless Diagnostics (macOS) | `checklist.md`, `data/site-survey.csv` |
| 12 | [NAT and PAT with iptables](lab-12-nat-pat/README.md) | iptables, conntrack, iproute2, curl | `checklist.md`, `cleanup.sh`, `setup.sh`, `verify.sh` |
| 13 | [DHCP Server with isc-dhcp-server](lab-13-dhcp-server/README.md) | isc-dhcp-server, iproute2, systemd | `checklist.md`, `cleanup.sh`, `dhcpd.conf`, `setup.sh`, `verify.sh` |
| 14 | [Authoritative DNS with BIND9](lab-14-bind9-dns/README.md) | bind9, dnsutils (dig), named-checkzone | `checklist.md`, `cleanup.sh`, `db.10.0.0`, `db.lab.local`, `named.conf.local`, `named.conf.local.reverse`, `setup.sh`, `verify.sh` |

## Domain 3.0 — Network Operations  (19%)

| # | Lab | Tools | Files in the lab folder |
|---|-----|-------|-------------------------|
| 15 | [SNMP Monitoring](lab-15-snmp-monitoring/README.md) | snmpd, snmpwalk, snmpget, snmp-mibs-downloader | `checklist.md`, `cleanup.sh`, `setup.sh`, `snmpd.conf.lab`, `verify.sh`, `data/device-inventory.csv` |
| 16 | [NetFlow Analysis with nfdump](lab-16-netflow/README.md) | fprobe, nfcapd, nfdump, curl, ping | `checklist.md`, `cleanup.sh`, `run.sh`, `setup.sh`, `verify.sh` |
| 17 | [Centralised Logging with Rsyslog](lab-17-syslog/README.md) | rsyslog, logger, ss, grep -E, TIS Regex Generator | `50-forward.conf`, `checklist.md`, `cleanup.sh`, `setup.sh`, `verify.sh`, `data/sample-syslog.csv`, `data/sample-syslog.log` |
| 18 | [Time Synchronisation with Chrony](lab-18-ntp/README.md) | chrony, chronyc | `checklist.md`, `chrony.conf.lab`, `verify.sh` |
| 19 | [Configuration Backup with Git](lab-19-config-backup/README.md) | git | `checklist.md`, `run.sh`, `verify.sh`, `data/change-log.csv` |
| 20 | [Performance Baseline with iperf3](lab-20-iperf3/README.md) | iperf3 | `checklist.md`, `cleanup.sh`, `run.sh`, `verify.sh`, `data/baseline-metrics.csv` |

## Domain 4.0 — Network Security  (14%)

| # | Lab | Tools | Files in the lab folder |
|---|-----|-------|-------------------------|
| 21 | [Host Firewall with UFW](lab-21-host-firewall/README.md) | ufw, iptables | `checklist.md`, `cleanup.sh`, `setup.sh`, `verify.sh`, `data/firewall-rules.csv` |
| 22 | [TLS Certificate with OpenSSL and Nginx](lab-22-tls-certificate/README.md) | openssl, nginx, curl | `checklist.md`, `cleanup.sh`, `lab-openssl.cnf`, `nginx-tls.conf`, `setup.sh`, `verify.sh` |
| 23 | [SSH Hardening with Key Authentication](lab-23-ssh-hardening/README.md) | openssh-server, openssh-client, ssh-keygen | `checklist.md`, `cleanup.sh`, `sshd_hardening.conf`, `verify.sh`, `data/hardening-checklist.csv` |
| 24 | [Site-to-Site VPN with WireGuard](lab-24-wireguard-vpn/README.md) | wireguard, wireguard-tools, iproute2 | `checklist.md`, `cleanup.sh`, `setup.sh`, `verify.sh`, `wg0-a.conf`, `wg0-b.conf` |
| 25 | [Port Scanning and Service Hardening](lab-25-port-scanning/README.md) | nmap, ss, systemctl | `checklist.md`, `run.sh`, `data/port-scan-findings.csv` |
| 26 | [Intrusion Detection with Suricata](lab-26-suricata-ids/README.md) | suricata, suricata-update, jq, curl, TIS Cybersecurity Simulator | `checklist.md`, `cleanup.sh`, `local.rules`, `setup.sh`, `verify.sh` |
| 27 | [Building an ACL with iptables](lab-27-iptables-acl/README.md) | iptables, netcat, iptables-persistent | `checklist.md`, `cleanup.sh`, `setup.sh`, `verify.sh`, `data/acl-plan.csv` |

## Domain 5.0 — Network Troubleshooting  (24%)

| # | Lab | Tools | Files in the lab folder |
|---|-----|-------|-------------------------|
| 28 | [Layer 1/2 Diagnostics with ip and ethtool](lab-28-layer1-2-diagnostics/README.md) | ethtool, iproute2, Killercoda Ubuntu playground | `checklist.md`, `run.sh`, `data/interface-errors.csv` |
| 29 | [Reachability with ping, traceroute and mtr](lab-29-ping-traceroute-mtr/README.md) | iputils-ping, traceroute, mtr-tiny | `checklist.md`, `run.sh`, `data/latency-log.csv` |
| 30 | [DNS Troubleshooting with dig and resolvectl](lab-30-dns-troubleshooting/README.md) | dnsutils (dig), systemd-resolved (resolvectl) | `break.sh`, `checklist.md`, `cleanup.sh`, `verify.sh` |
| 31 | [ARP and the IPv6 Neighbour Table](lab-31-arp-neighbor/README.md) | iputils-arping, iproute2, ndisc6 | `checklist.md`, `run.sh`, `data/arp-table.csv` |
| 32 | [Packet Capture with tcpdump and TIS PCAP Analyzer](lab-32-packet-capture/README.md) | tcpdump, tshark, TIS PCAP Analyzer (alfredang.github.io/pcapanalyzer) | `checklist.md`, `run.sh`, `verify.sh` |
| 33 | [MTU and Path-MTU Discovery](lab-33-mtu-pmtud/README.md) | iputils-ping, iproute2 | `checklist.md`, `cleanup.sh`, `run.sh` |
| 34 | [Diagnosing Routing Problems](lab-34-routing-issues/README.md) | iproute2, traceroute | `break.sh`, `checklist.md`, `cleanup.sh`, `verify.sh` |
| 35 | [Simulating Slow and Lossy Links with tc](lab-35-tc-network-emulation/README.md) | iproute2 (tc/netem/tbf), iperf3 | `checklist.md`, `cleanup.sh`, `run.sh`, `setup.sh` |
| 36 | [Service Reachability Triage with curl, nc and openssl](lab-36-service-triage/README.md) | curl, netcat-openbsd, openssl | `break.sh`, `checklist.md`, `cleanup.sh`, `run.sh`, `troubleshooting-worksheet.md` |

---

© 2026 Tertiary Infotech Academy Pte Ltd (UEN: 201200696W). Course registration: https://www.tertiarycourses.com.sg/wsq-comptia-certified-network-training.html
