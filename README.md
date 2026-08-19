<div align="center">

# 🌐 CompTIA Certified Network+ Training (N10-009)

**Design, implement, operate, secure and troubleshoot modern networks — and get exam-ready for CompTIA Network+ N10-009.**

[![Register](https://img.shields.io/badge/Register-Enrol%20Now-1F6FEB?style=for-the-badge)](https://www.tertiarycourses.com.sg/wsq-comptia-certified-network-training.html) [![WSQ Funded](https://img.shields.io/badge/WSQ-SkillsFuture%20Funded-10B981?style=for-the-badge)](https://www.tertiarycourses.com.sg/wsq-comptia-certified-network-training.html)

![Course Code](https://img.shields.io/badge/Course%20Code-TGS--2025054472-555) ![Duration](https://img.shields.io/badge/Duration-5%20Days%20·%2040%20Hours-1F6FEB) ![Level](https://img.shields.io/badge/Level-Beginner%20to%20Intermediate-7C3AED) ![Labs](https://img.shields.io/badge/Hands--On%20Labs-36-10B981) ![Exam](https://img.shields.io/badge/Exam-N10--009-F59E0B) ![Assessment](https://img.shields.io/badge/Assessment-WA%20%2B%20PP-555)

### 📝 [Register for this course →](https://www.tertiarycourses.com.sg/wsq-comptia-certified-network-training.html)

</div>

---

## About This Course

This WSQ course takes you from networking fundamentals to confident hands-on practice across all **five official CompTIA Network+ (N10-009) exam domains**. You will build, break and fix real networks in a browser-based Linux environment — subnetting, routing, VLANs, wireless, monitoring, security and structured troubleshooting.

It suits IT support staff, system administrators, helpdesk engineers and career switchers who want a recognised networking foundation. No prior certification is required. Every one of the **36 labs** runs free in the browser — nothing to install on your own machine.

> **Conducted by [Tertiary Infotech Academy Pte Ltd](https://www.tertiarycourses.com.sg/)** · UEN: 201200696W

## Learning Outcomes

| # | On completion, learners will be able to |
|---|---|
| **LO1** | Explain networking concepts — the OSI model, network appliances, cloud concepts, ports and protocols, traffic types, transmission media, transceivers and connectors, network topologies and IPv4/IPv6 addressing and subnetting. (K1, K2) |
| **LO2** | Implement networks — static and dynamic routing (BGP, EIGRP, OSPF), NAT/PAT, 802.1Q VLANs, trunking, spanning tree, link aggregation, wireless devices and physical installation considerations. (K3, A1, A2) |
| **LO3** | Operate and maintain networks — documentation and IPAM, life-cycle and change management, configuration backup and baselines, SNMP/flow/log monitoring, disaster recovery, DHCP/DNS/NTP network services and secure access methods. (K4, A3, A4) |
| **LO4** | Secure networks — encryption and PKI, IAM/MFA/SSO, RADIUS/TACACS+, physical security, deception technologies, segmentation, common attacks and defence features such as hardening, NAC, ACLs and screened subnets. (K5, A5) |
| **LO5** | Troubleshoot networks — apply the CompTIA troubleshooting methodology with the right tools to cabling, interface, switching, routing, service and performance issues. (K6, A6) |

## Course Topics & Labs

The course follows the five N10-009 exam domains and their official weightings. **Each lab lives in its own folder** with a README carrying the full step-by-step commands.

| Domain | Exam weighting | Labs |
|---|---|---|
| **1.0 — Networking Concepts** | 23% | Labs 1–7 |
| **2.0 — Network Implementation** | 20% | Labs 8–14 |
| **3.0 — Network Operations** | 19% | Labs 15–20 |
| **4.0 — Network Security** | 14% | Labs 21–27 |
| **5.0 — Network Troubleshooting** | 24% | Labs 28–36 |

<details>
<summary><b>Domain 1.0 — Networking Concepts (23%)</b> · 7 labs</summary>

| # | Lab | Tools |
|---|-----|-------|
| 1 | [OSI Model Packet Inspection](labs/lab-01-osi-packet-inspection/README.md) | tcpdump, curl, Killercoda Ubuntu, TIS PCAP Analyzer (alfredang.github.io/pcapanalyzer) |
| 2 | [IPv4 Subnetting and CIDR](labs/lab-02-ipv4-subnetting/README.md) | TIS IP Calculator (alfredang.github.io/ipcalculator), iproute2, Killercoda Ubuntu |
| 3 | [IPv6 Addressing and Link-Local](labs/lab-03-ipv6-slaac/README.md) | TIS IP Calculator (alfredang.github.io/ipcalculator), iproute2, ping6, Killercoda |
| 4 | [Common Ports and Protocols](labs/lab-04-common-ports/README.md) | nmap, ss, net-tools (netstat), getent, Killercoda Ubuntu |
| 5 | [DNS Record Types](labs/lab-05-dns-records/README.md) | dig, nslookup, host (dnsutils), Killercoda Ubuntu |
| 6 | [DHCP Lease Capture (DORA)](labs/lab-06-dhcp-capture/README.md) | isc-dhcp-client (dhclient), tcpdump, Killercoda Ubuntu |
| 7 | [Simulating a Cloud VPC with Namespaces](labs/lab-07-cloud-vpc-namespaces/README.md) | iproute2 (ip netns, ip link, veth, bridge), Killercoda Ubuntu |

</details>

<details>
<summary><b>Domain 2.0 — Network Implementation (20%)</b> · 7 labs</summary>

| # | Lab | Tools |
|---|-----|-------|
| 8 | [Static Routing Between Two Subnets](labs/lab-08-static-routing/README.md) | iproute2, ip netns, sysctl |
| 9 | [802.1Q VLAN Tagging](labs/lab-09-vlan-tagging/README.md) | iproute2, 8021q module, tcpdump |
| 10 | [Link Aggregation (LACP Bond)](labs/lab-10-link-aggregation/README.md) | ifenslave, bonding module, iproute2 |
| 11 | [Wireless Concepts and Channel Survey](labs/lab-11-wireless-concepts/README.md) | iw, wavemon, WiFi Analyzer (Windows), Wireless Diagnostics (macOS) |
| 12 | [NAT and PAT with iptables](labs/lab-12-nat-pat/README.md) | iptables, conntrack, iproute2, curl |
| 13 | [DHCP Server with isc-dhcp-server](labs/lab-13-dhcp-server/README.md) | isc-dhcp-server, iproute2, systemd |
| 14 | [Authoritative DNS with BIND9](labs/lab-14-bind9-dns/README.md) | bind9, dnsutils (dig), named-checkzone |

</details>

<details>
<summary><b>Domain 3.0 — Network Operations (19%)</b> · 6 labs</summary>

| # | Lab | Tools |
|---|-----|-------|
| 15 | [SNMP Monitoring](labs/lab-15-snmp-monitoring/README.md) | snmpd, snmpwalk, snmpget, snmp-mibs-downloader |
| 16 | [NetFlow Analysis with nfdump](labs/lab-16-netflow/README.md) | fprobe, nfcapd, nfdump, curl, ping |
| 17 | [Centralised Logging with Rsyslog](labs/lab-17-syslog/README.md) | rsyslog, logger, ss, grep -E, TIS Regex Generator |
| 18 | [Time Synchronisation with Chrony](labs/lab-18-ntp/README.md) | chrony, chronyc |
| 19 | [Configuration Backup with Git](labs/lab-19-config-backup/README.md) | git |
| 20 | [Performance Baseline with iperf3](labs/lab-20-iperf3/README.md) | iperf3 |

</details>

<details>
<summary><b>Domain 4.0 — Network Security (14%)</b> · 7 labs</summary>

| # | Lab | Tools |
|---|-----|-------|
| 21 | [Host Firewall with UFW](labs/lab-21-host-firewall/README.md) | ufw, iptables |
| 22 | [TLS Certificate with OpenSSL and Nginx](labs/lab-22-tls-certificate/README.md) | openssl, nginx, curl |
| 23 | [SSH Hardening with Key Authentication](labs/lab-23-ssh-hardening/README.md) | openssh-server, openssh-client, ssh-keygen |
| 24 | [Site-to-Site VPN with WireGuard](labs/lab-24-wireguard-vpn/README.md) | wireguard, wireguard-tools, iproute2 |
| 25 | [Port Scanning and Service Hardening](labs/lab-25-port-scanning/README.md) | nmap, ss, systemctl |
| 26 | [Intrusion Detection with Suricata](labs/lab-26-suricata-ids/README.md) | suricata, suricata-update, jq, curl, TIS Cybersecurity Simulator |
| 27 | [Building an ACL with iptables](labs/lab-27-iptables-acl/README.md) | iptables, netcat, iptables-persistent |

</details>

<details>
<summary><b>Domain 5.0 — Network Troubleshooting (24%)</b> · 9 labs</summary>

| # | Lab | Tools |
|---|-----|-------|
| 28 | [Layer 1/2 Diagnostics with ip and ethtool](labs/lab-28-layer1-2-diagnostics/README.md) | ethtool, iproute2, Killercoda Ubuntu playground |
| 29 | [Reachability with ping, traceroute and mtr](labs/lab-29-ping-traceroute-mtr/README.md) | iputils-ping, traceroute, mtr-tiny |
| 30 | [DNS Troubleshooting with dig and resolvectl](labs/lab-30-dns-troubleshooting/README.md) | dnsutils (dig), systemd-resolved (resolvectl) |
| 31 | [ARP and the IPv6 Neighbour Table](labs/lab-31-arp-neighbor/README.md) | iputils-arping, iproute2, ndisc6 |
| 32 | [Packet Capture with tcpdump and TIS PCAP Analyzer](labs/lab-32-packet-capture/README.md) | tcpdump, tshark, TIS PCAP Analyzer (alfredang.github.io/pcapanalyzer) |
| 33 | [MTU and Path-MTU Discovery](labs/lab-33-mtu-pmtud/README.md) | iputils-ping, iproute2 |
| 34 | [Diagnosing Routing Problems](labs/lab-34-routing-issues/README.md) | iproute2, traceroute |
| 35 | [Simulating Slow and Lossy Links with tc](labs/lab-35-tc-network-emulation/README.md) | iproute2 (tc/netem/tbf), iperf3 |
| 36 | [Service Reachability Triage with curl, nc and openssl](labs/lab-36-service-triage/README.md) | curl, netcat-openbsd, openssl |

</details>

## Tools

Everything is **free and browser-based** — no installation on your own machine.

| Tool | Purpose |
|---|---|
| [Killercoda Ubuntu Playground](https://killercoda.com/playgrounds/scenario/ubuntu) | Disposable Ubuntu VM in your browser — every Linux lab runs here |
| [TIS IP Calculator](https://alfredang.github.io/ipcalculator/) | CIDR / VLSM subnet planning and verification |
| [TIS PCAP Analyzer](https://alfredang.github.io/pcapanalyzer/) | Dissect packet captures layer by layer |
| [TIS Cybersecurity Simulator](https://alfredang.github.io/cybersecuritysimulator/) | Practise recognising network attacks safely |
| [TIS Regex Generator](https://alfredang.github.io/regexgenerator/) | Build regular expressions for log filtering |

Command-line tools used inside the playground (installed with `apt`): `tcpdump`, `tshark`, `nmap`, `dig`, `ip`, `iptables`, `iperf3`, `snmpd`, `nfdump`, `rsyslog`, `chrony`, `bind9`, `isc-dhcp-server`, `suricata`, `wireguard`, `openssl`, `nginx`, `ethtool`, `mtr`, `traceroute`.

## Repository Structure

```
├── courseware/                 # Slide deck, Lesson Plan, Learner Guide (+ PDFs)
│   ├── CompTIA Network+ (N10-009)-v2.0.pptx / .pdf
│   ├── LP-CompTIA Network+ (N10-009).docx / .pdf
│   ├── LG-CompTIA Network+ (N10-009).docx / .pdf
│   └── archive/                # Superseded versions
├── labs/                       # 36 hands-on labs, one folder each
│   ├── README.md               # Lab index by exam domain
│   ├── lab-01-osi-packet-inspection/README.md
│   └── ...
├── LG-CompTIA Network+ (N10-009).md       # Learner Guide (Markdown mirror)
└── README.md
```

> **Note:** the confidential WSQ **assessment** materials (Written Assessment, Practical Performance and their answer keys) are intentionally **not** published to this repository.

## Course Details

| | |
|---|---|
| **Course Title** | CompTIA Certified Network+ Training (N10-009) |
| **WSQ Course Reference** | TGS-2025054472 |
| **Duration** | 5 days · 8 training hours per day (40 hours) |
| **Daily Timing** | 9:30 am – 6:30 pm (1-hour lunch; tea breaks within training time) |
| **Mode** | Instructor-led, hands-on labs |
| **Assessment** | Written Assessment (SAQ, 1 hr) + Practical Performance (PP, 90 min) — both open book |
| **Certification target** | CompTIA Network+ N10-009 (Pearson VUE) |
| **Trainer** | Dr. Alfred Ang |
| **Training Provider** | Tertiary Infotech Academy Pte Ltd (UEN: 201200696W) |

### Funding

This course is **WSQ / SkillsFuture funded**. A minimum **75% attendance** and a **Competent** assessment outcome are required for funding eligibility. See the [course page](https://www.tertiarycourses.com.sg/wsq-comptia-certified-network-training.html) for current fees, subsidy levels and upcoming dates.

## Exam Preparation

Sharpen your readiness with the Tertiary Infotech practice exam: **[CompTIA Network+ practice exam →](https://exams.tertiaryinfotech.com/practice-exams/comptia/comptia-network-plus)**

## Building the Courseware

All artifacts are generated from a single source (`course_data.py` + `data_domain1..5.py`), so the deck, Lesson Plan, Learner Guide and lab index can never drift apart.

```bash
# everything: PPT + LP + LG (DOCX + PDF, with page-numbered TOCs)
bash .claude/skills/courseware-build/build/build_courseware.sh

# or individually
python3 .claude/skills/courseware-build/build/build_slides.py
python3 .claude/skills/courseware-build/build/build_lesson_plan.py
python3 .claude/skills/courseware-build/build/build_learner_guide.py
python3 .claude/skills/courseware-build/build/build_labs_index.py
```

## Contact

- 🌐 **Course page:** https://www.tertiarycourses.com.sg/wsq-comptia-certified-network-training.html
- ✉️ **Email:** enquiry@tertiaryinfotech.com
- ☎️ **Tel:** +65 6100 0613
- 🎓 **LMS / TMS:** https://lms-tms.tertiaryinfotech.com

---

<div align="center">

### Ready to build your networking career?

[![Register Now](https://img.shields.io/badge/Register%20Now-Enrol%20for%20this%20course-1F6FEB?style=for-the-badge)](https://www.tertiarycourses.com.sg/wsq-comptia-certified-network-training.html)

© 2026 Tertiary Infotech Academy Pte Ltd · UEN 201200696W

</div>
