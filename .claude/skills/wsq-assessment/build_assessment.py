#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the WSQ assessment set for 'CompTIA Certified Network+ Training (N10-009)' (TGS-2025054472):
  - Written Assessment (SAQ)  — 6 open-ended KNOWLEDGE questions (K1–K6), aligned to the slides
  - Practical Performance (PP) — 4 PRACTICAL tasks (LO1–LO4), aligned to the in-class labs
Each instrument is produced as a Question Paper and a matching Answer Key (4 DOCX total),
all with the WSQ house cover page (same as the Lesson Plan / Learner Guide). Page 1 is the cover;
page 2 carries Trainee Information + Instructions + Grading; the questions/tasks begin on page 3.
Body: Arial 11.
"""
import os, sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# This script lives in the wsq-assessment skill (.claude/skills/wsq-assessment/) and runs in
# place — it detects the course repo root by walking up to the nearest dir that has a .git
# folder (or both courseware/ and assessment/). Override with env REPO=/path if needed.
def _find_repo():
    env = os.environ.get("REPO")
    if env and os.path.isdir(env):
        return os.path.abspath(env)
    d = os.path.dirname(os.path.abspath(__file__))
    while d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, ".git")) or \
           (os.path.isdir(os.path.join(d, "courseware")) and os.path.isdir(os.path.join(d, "assessment"))):
            return d
        d = os.path.dirname(d)
    return os.getcwd()

REPO = _find_repo()
# prodoc.py (WSQ cover page + version control + page numbers, same as LP/LG) ships with the
# tertiary-lesson-plan skill. Look for it at the project level first, then the user level.
for _cand in (os.path.join(REPO, ".claude/skills/tertiary-lesson-plan"),
              os.path.expanduser("~/.claude/skills/tertiary-lesson-plan")):
    if os.path.exists(os.path.join(_cand, "prodoc.py")):
        sys.path.insert(0, _cand); break
import prodoc  # cover page + version control + page numbers (same as LP/LG)

# ─── EDIT PER COURSE ────────────────────────────────────────────────────────
TITLE       = "CompTIA Certified Network+ Training (N10-009)"
COURSE_CODE = "TGS-2025054472"
# ────────────────────────────────────────────────────────────────────────────
# The cover page renders prodoc's module-level TGS constant. Override it so the
# assessment cover shows THIS course's ref (works with either prodoc version —
# the older project prodoc has no course_code kwarg).
prodoc.TGS = f"TGS Ref No: {COURSE_CODE}"
OUT   = os.path.join(REPO, "assessment")

# Logos: prefer the course's own courseware/assets, else fall back to the copies bundled
# in this skill (so the assessment builds even outside this project). Replace the course
# logo per course; the Tertiary Infotech logo is the same for every WSQ course.
def _logo(name):
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(REPO, "courseware/assets", name),
              # the courseware-build skill holds this course's badge + the org logo
              os.path.join(REPO, ".claude/skills/courseware-build/assets", name),
              os.path.join(here, "assets", name)):
        if os.path.exists(p):
            return p
    return None
ORG_LOGO    = _logo("tertiary-infotech-logo.png")
COURSE_LOGO = _logo("comptia-network-badge.png")   # None if absent → Tertiary-only cover (as LP/LG)

Q_VER, A_VER = "v4", "v4"   # single standardised version across all four files
BRAND = RGBColor(0x1F, 0x6F, 0xEB); DARK = RGBColor(0x11, 0x18, 0x27); GREY = RGBColor(0x55, 0x5B, 0x66)
# Assessments carry the cover page only — no Document Version Control Record.

# ---------------------------------------------------------------- WRITTEN (KNOWLEDGE)
# (criterion, context, question, [model-answer points]) — each traces to the course slides.
WRITTEN = [
 ("K1",
  "A network is built from interconnected components — end hosts and servers, switches, routers, firewalls, "
  "load balancers, proxies and wireless access points — joined by copper, fibre and wireless media. Every "
  "conversation between them can be described by the seven-layer OSI reference model.",
  "What are the key components of a computer network, and how does the OSI model describe the way data moves "
  "between them?",
  ["Key components: end hosts and servers; switches (Layer 2); routers (Layer 3); firewalls; wireless access "
   "points and controllers; load balancers, proxies and IDS/IPS; NAS/SAN storage; plus the transmission media "
   "(twisted pair, coax/twinax, single-mode and multimode fibre, wireless) and the transceivers and connectors "
   "(SFP/SFP+/QSFP; RJ45, LC/SC/ST/MPO) that join them. Appliances may be physical or virtual.",
   "The OSI model has seven layers — Physical (1), Data Link (2), Network (3), Transport (4), Session (5), "
   "Presentation (6), Application (7) — each with its own PDU: bits, frame, packet, segment/datagram, data.",
   "Data is encapsulated top-down (each layer adds its header as the data passes down the stack) and "
   "de-encapsulated bottom-up at the receiver. Layer 2 addresses with the 48-bit MAC inside an Ethernet frame, "
   "Layer 3 with the IP address, Layer 4 with TCP/UDP port numbers, and Layer 7 carries the application payload "
   "(e.g. an HTTP GET).",
   "Each device reads only as far up the stack as it needs: a hub repeats bits (L1), a switch forwards by MAC "
   "and breaks up collision domains (L2), a router forwards by IP between network IDs (L3), a stateful firewall "
   "filters on port and protocol (L4) and an application-aware firewall or proxy inspects L7.",
   "The model also drives fault isolation — troubleshoot by layer (bottom-to-top, top-to-bottom or "
   "divide-and-conquer) so each test rules out one layer. "
   "(Slides, Domain 1 — Networking Concepts: The Seven Layers · PDUs and Devices by Layer · Encapsulation: Data "
   "Down the Stack · Which Layer Does Each Device Read? · Core Networking Appliances · Troubleshooting by Layer.)"]),
 ("K2",
  "Hosts are located by IP address, grouped into subnets by the mask, named by DNS and configured automatically "
  "by DHCP or SLAAC. Addressing and subnetting carry the heaviest weighting on the N10-009 exam.",
  "How are IPv4 and IPv6 addresses structured and subnetted, and how do DNS and DHCP support host addressing on "
  "a network?",
  ["IPv4 is a 32-bit address written as four dotted-decimal octets with a CIDR prefix (e.g. 192.168.10.65/26). "
   "The prefix splits the address into network bits and host bits; the mask is what decides whether a "
   "destination is local (switch it) or remote (send it to the default gateway, resolving the gateway MAC by ARP).",
   "Address ranges to know: the RFC 1918 private ranges 10.0.0.0/8, 172.16.0.0/12 and 192.168.0.0/16; APIPA "
   "169.254.0.0/16 (a symptom of a failed DHCP lease); loopback 127.0.0.0/8; the historical classes A–E.",
   "Subnetting borrows host bits to make more, smaller networks — a /24 (256 addresses, 254 usable) splits into "
   "four /26s of 64 addresses / 62 usable each; VLSM right-sizes each subnet to the hosts it actually needs, and "
   "every subnet loses two addresses to the network ID and the broadcast address.",
   "IPv6 is a 128-bit address in eight hextets of hexadecimal, shortened by dropping leading zeros and using :: "
   "once for the longest run of zero hextets. Key types: global unicast (2000::/3), link-local (fe80::/10), "
   "unique local and multicast; SLAAC lets a host build its own address from the Router Advertisement prefix "
   "with no DHCP server at all.",
   "DHCP leases addresses through the DORA handshake — Discover, Offer, Request, Acknowledge — using a scope "
   "(range, mask, gateway, DNS options) with reservations and lease times; a DHCP relay forwards broadcasts "
   "across a router to a central server.",
   "DNS resolves names to addresses through a hierarchy (root → TLD → authoritative), with recursive resolvers "
   "caching answers. Record types to know: A, AAAA, CNAME, MX, NS, PTR, TXT and SOA. "
   "(Slides, Domain 1: IPv4 Address Anatomy · RFC 1918 Private Ranges · Special IPv4 Addresses · Local or "
   "Remote? The Mask Decides · CIDR: Splitting a /24 into /26s · VLSM: Right-Sizing Subnets · Shortening an IPv6 "
   "Address · Key IPv6 Address Types. Domain 3 — Network Operations: DHCP Essentials · DORA — the DHCP "
   "Handshake · SLAAC · DNS Architecture · DNS Record Types.)"]),
 ("K3",
  "Once the addressing is planned, the network is implemented — routing between subnets, switching features on "
  "the LAN, address translation at the edge, and wireless access for mobile users.",
  "What techniques are used to implement a network — routing, VLANs, NAT and wireless — and how does each work?",
  ["Routing moves packets between different network IDs. A router consults its routing table and picks the "
   "longest-prefix (most specific) match; where two sources offer the same prefix it prefers the lower "
   "administrative distance (connected 0, static 1, EIGRP 90, OSPF 110, RIP 120, eBGP 20).",
   "Static routes are manually configured — predictable and cheap, but they do not adapt to a failure. Dynamic "
   "protocols advertise and converge automatically: RIP (distance-vector, hop count, max 15), OSPF (link-state, "
   "cost, areas), EIGRP (Cisco advanced distance-vector) as IGPs, and BGP (path-vector) as the EGP that routes "
   "between autonomous systems on the Internet. FHRPs (VRRP/HSRP) give hosts a redundant virtual default gateway.",
   "802.1Q VLANs split one physical switch into several logical broadcast domains. An access port carries one "
   "untagged VLAN to an end device; a trunk port carries many VLANs, inserting a 4-byte 802.1Q tag with the VLAN "
   "ID into each frame. Traffic between VLANs needs a Layer 3 hop — router-on-a-stick with sub-interfaces, an "
   "SVI on a Layer 3 switch, or a separate router interface. Supporting features: spanning tree (STP/RSTP) to "
   "break loops, LACP link aggregation for bandwidth and redundancy, port security, and MTU / jumbo frames.",
   "NAT translates private RFC 1918 addresses to a routable public address at the edge. PAT (NAT overload) lets "
   "many internal hosts share one public IP by also rewriting the source port and tracking the mapping in the "
   "translation table — this is what `iptables ... -j MASQUERADE` does on Linux.",
   "Wireless: 802.11 uses the 2.4 GHz band (three non-overlapping channels 1, 6, 11 — longer range, more "
   "interference), 5 GHz and 6 GHz (more channels, more bandwidth, shorter range). Clients associate to an SSID "
   "forming a BSS, and multiple APs on one SSID form an ESS for roaming. Security runs WPA2/WPA3 with either a "
   "pre-shared key or Enterprise 802.1X/EAP against a RADIUS server; guest SSIDs use a captive portal. AP "
   "placement, channel width and antenna type are set from a site survey / heat map. "
   "(Slides, Domain 2 — Network Implementation: Reading a Routing Table · Static vs Dynamic Routing · "
   "Administrative Distance · Route Selection · Routing Protocols Compared · VLAN Fundamentals · Inside the "
   "802.1Q Tag · Access Ports vs Trunk Ports · InterVLAN Routing · Loops, Storms and Spanning Tree · Link "
   "Aggregation and LACP · Frequency Bands · Channels and Channel Width · Wireless Security: WEP to WPA3 · "
   "802.1X. Domain 1: How NAT Hides Private Addresses.)"]),
 ("K4",
  "A running network must be documented, monitored, logged, time-synchronised and backed up so that operators "
  "can see its health, prove a change worked and recover when it does not.",
  "What tools and protocols are used to monitor, log and maintain a network, and what does each provide?",
  ["SNMP polls managed devices for health counters through a MIB of OIDs (sysDescr, sysUpTime, ifInOctets) and "
   "receives unsolicited traps for events. v1/v2c authenticate only with a plaintext community string; SNMPv3 "
   "adds authentication and encryption (noAuthNoPriv / authNoPriv / authPriv) and is what production should use.",
   "Flow data (NetFlow / IPFIX / sFlow) summarises conversations — who talked to whom, on what port, how much — "
   "for traffic analysis and capacity planning; full packet capture (tcpdump/tshark, fed by a SPAN / port-mirror "
   "session) inspects individual packets when the flow summary is not enough.",
   "Syslog centralises log messages to a collector (rsyslog on UDP or TCP 514) tagged by facility and severity "
   "0–7 (Emergency → Debug); a SIEM aggregates and correlates those logs across devices to raise security alerts.",
   "NTP (and PTP where sub-microsecond accuracy is needed, NTS where it must be authenticated) synchronises "
   "device clocks against a stratum hierarchy — without it, correlating logs across devices is impossible.",
   "Documentation and IPAM: physical and logical diagrams, rack/MDF-IDF diagrams, cable maps, asset inventory, "
   "IP address management, wireless heat maps, and the business documents (SLA, MOU, SOW).",
   "Configuration management: keep production, backup and baseline (golden) configurations, hold them in version "
   "control such as Git so every change is diffable and revertible, and follow the change-management workflow "
   "(request → review/approval → implementation → post-change verification → documentation), with a separate "
   "path for emergency changes.",
   "Baselines and performance: iperf3 measures achievable throughput and interface counters/metrics establish "
   "the normal baseline that anomaly alerting compares against. Disaster recovery is measured by RPO, RTO, MTTR "
   "and MTBF, supported by cold/warm/hot sites and active-active or active-passive designs. "
   "(Slides, Domain 3 — Network Operations: SNMP Building Blocks · SNMP Versions · Traps vs Polls · Flow Data — "
   "NetFlow & IPFIX · Packet Capture & Port Mirroring · Log Aggregation with Syslog · Syslog Severity Levels 0-7 "
   "· SIEM · Time Services — NTP, PTP, NTS · Documenting the Network · IPAM · Change Management · Config Backup "
   "Discipline · Version Control for Configurations · Measuring Throughput with iperf3 · DR Metrics.)"]),
 ("K5",
  "Controlling who reaches what, and protecting data as it crosses the network, are the core of a secure "
  "design — built in layers rather than at a single perimeter.",
  "What are the key considerations for securing a network, and how are firewalls, encryption, VPNs and access "
  "control used?",
  ["Security is framed by the CIA triad — confidentiality, integrity, availability — and the vocabulary of risk, "
   "vulnerability, threat and exploit. Defence in depth layers independent controls so no single failure is "
   "fatal; compliance regimes (PCI DSS, GDPR, data locality) set the minimum bar.",
   "Firewalls enforce trusted vs untrusted zones, with public-facing servers placed in a screened subnet (DMZ). "
   "They range from stateless packet filters through stateful inspection (tracking the connection state) to "
   "application-aware / next-generation firewalls. ACLs — on a router, a switch or a host with iptables/UFW — "
   "permit or deny by source, destination, protocol and port, and are evaluated top-down so rule ORDER matters, "
   "with an implicit deny at the end.",
   "Encryption protects data in transit and at rest. Symmetric ciphers (AES) are fast and use one shared key; "
   "asymmetric (RSA, ECC) solves key distribution with a public/private key pair; hashes (SHA-256) give "
   "integrity. TLS combines them — the handshake authenticates the server with a PKI certificate signed by a "
   "trusted CA, then switches to a symmetric session key. Certificate faults to recognise: expired, "
   "name mismatch, self-signed / untrusted issuer, broken chain.",
   "VPNs extend the trusted zone across an untrusted one: site-to-site tunnels join two offices, client-to-site "
   "(remote access) connects a user, and technologies include IPsec, WireGuard, SSL/TLS VPNs and GRE; split "
   "versus full tunnel decides how much traffic is carried.",
   "Access control: IAM/AAA (identification, authentication, authorisation, accounting); MFA combining "
   "something you know / have / are; SSO and federation (SAML); RADIUS (open, encrypts only the password, "
   "network access) versus TACACS+ (Cisco, encrypts the whole payload, device administration); models such as "
   "RBAC, MAC and DAC with least privilege; and 802.1X NAC to authenticate a device before it reaches the LAN.",
   "Hardening and defence features: disable unused ports and default accounts, patch, harden sshd (key "
   "authentication, PasswordAuthentication no, PermitRootLogin no), URL/content filtering, network segmentation "
   "for IoT/OT/guest/BYOD, honeypots as deception, and IDS/IPS sensors (out-of-band detection vs inline "
   "prevention) to spot ARP poisoning, VLAN hopping, DoS/DDoS, evil twin, on-path and spoofing attacks. "
   "(Slides, Domain 4 — Network Security: The CIA Triad · Defense in Depth · Trusted vs Untrusted Zones · The "
   "Screened Subnet (DMZ) · Firewall Families · Stateless, Stateful, Application-Aware · Symmetric vs "
   "Asymmetric Encryption · The TLS 1.3 Handshake · Certificates and PKI · VPN Technologies Compared · "
   "Identification to Accounting (IAM / AAA) · Multifactor Authentication · RADIUS vs TACACS+ · Access Control "
   "Models · Access Control Lists (ACLs) · Device Hardening · 802.1X Network Access Control.)"]),
 ("K6",
  "When something breaks, a network professional follows a repeatable method rather than guessing, and reaches "
  "for the right diagnostic tool for the layer under suspicion.",
  "What is the CompTIA troubleshooting methodology, and which tools are used to track and diagnose network "
  "performance and faults?",
  ["The seven steps: (1) Identify the problem — gather information, question users, identify symptoms, "
   "determine whether anything changed, and duplicate the problem if possible. (2) Establish a theory of "
   "probable cause, questioning the obvious first. (3) Test the theory to determine the cause — if it is "
   "confirmed, move on; if not, establish a new theory or escalate. (4) Establish a plan of action to resolve "
   "the problem and identify potential effects. (5) Implement the solution or escalate. (6) Verify full system "
   "functionality and, if applicable, implement preventive measures. (7) Document findings, actions and outcomes.",
   "Approach the fault by OSI layer — bottom-to-top (start at cabling/link), top-to-bottom (start at the "
   "application), or divide-and-conquer (start at Layer 3 and work outwards) — so each test eliminates a layer "
   "instead of changing several things at once.",
   "Layer 1/2 tools and checks: `ip -brief link` / `ip -s link` for port status and error counters, `ethtool` "
   "for speed/duplex and link detection, cable testers, tone generators and loopback plugs, plus checks for the "
   "wrong cable type, improper termination, TX/RX transposed, signal degradation, PoE budget and transceiver "
   "mismatch.",
   "Layer 3 and path tools: `ping` for reachability, RTT and loss; `traceroute` and `mtr` for the path and where "
   "loss starts (remembering that '* * *' usually means ICMP is filtered on that hop, not a real fault); "
   "`ip route` / `ip route get` for routing-table and default-route problems; `ip neigh` / `arp` for IP-to-MAC "
   "resolution and duplicate addresses; DF-bit pings for MTU and PMTUD black holes.",
   "Service and application tools: `dig` / `nslookup` / `resolvectl` for DNS (including `dig +trace` to walk the "
   "hierarchy and response codes such as NXDOMAIN and SERVFAIL); `ss -tulpn` / `netstat` to see whether the "
   "service is actually listening; `nc -zv` for a bare TCP handshake; `openssl s_client` for certificate faults; "
   "`curl -v` for HTTP status; `tcpdump` / `tshark` (with the TIS PCAP Analyzer) for packet capture using "
   "capture and display filters; `iperf3` for throughput; and Wi-Fi analyzers for wireless interference, plus "
   "`tc` to reproduce latency and loss.",
   "Common performance causes to name: congestion and bandwidth saturation, latency and jitter, packet loss, "
   "duplex/speed mismatch, and wireless channel interference or overlap. "
   "(Slides, Domain 5 — Network Troubleshooting: CompTIA's 7-Step Troubleshooting Method · Steps 1–7 · Divide "
   "and Conquer · Symptom to Layer to First Tool · The First-Response Command-Line Kit · Reading a traceroute · "
   "Reading an mtr Report · DNS Troubleshooting Basics · Decoding DNS Response Codes · netstat and ss: Who Is "
   "Listening? · Protocol Analyzers · Reading a tcpdump Line · MTU: When Big Packets Vanish · Routing Table "
   "Issues.)"]),
]

# ---------------------------------------------------------------- PRACTICAL (ACTIVITY-BASED)
SCENARIO = (
 "NetTech Solutions, an expanding IT services provider, is opening a new branch office and must connect it to "
 "the head office while supporting a growing team of remote workers. You have been appointed the network "
 "engineer for the project. You will plan and verify the IP addressing for the new site, implement the core "
 "routed and translated network between the two offices, bring the network under monitoring and lock down "
 "management access, and finally troubleshoot a fault reported against the company web service. Each of the "
 "four tasks below mirrors a hands-on lab you completed in class on the Killercoda Ubuntu Playground "
 "(https://killercoda.com/playgrounds/scenario/ubuntu). Complete all four tasks. For each task, paste your "
 "commands / configuration and a screenshot of your output as evidence.")

# (label, criterion, task prompt, box caption, model-answer build steps citing the activity)
BOX_CAP = "Paste your commands / configuration and a screenshot of your output in the box below"
PRACTICAL = [
 ("Task 1", "LO1",
  "Plan and verify the addressing for the new branch office (Networking Concepts). "
  "Part A — Using the TIS IP Calculator (https://alfredang.github.io/ipcalculator/), subnet 192.168.10.0/24 into "
  "four equal /26 subnets. For each subnet, record the network address, first host, last host and broadcast "
  "address, and state how many usable hosts each provides. "
  "Part B — On the Killercoda terminal, assign the first usable address of subnet 2 to eth0 as a labelled "
  "secondary address and verify it is present, then remove it again. "
  "Part C — Capture HTTP traffic on eth0 with tcpdump while generating a request with curl, then state which "
  "OSI layer the MAC, IP, TCP and HTTP headers each belong to, and give the well-known port and transport "
  "protocol used by HTTP, HTTPS, SSH and DNS. (Labs 1, 2 and 4.)",
  BOX_CAP,
  "Part A - Subnet 192.168.10.0/24 into four /26 (verify each in the TIS IP Calculator):\n"
  "  Subnet 1: network 192.168.10.0    hosts .1   - .62    broadcast 192.168.10.63\n"
  "  Subnet 2: network 192.168.10.64   hosts .65  - .126   broadcast 192.168.10.127\n"
  "  Subnet 3: network 192.168.10.128  hosts .129 - .190   broadcast 192.168.10.191\n"
  "  Subnet 4: network 192.168.10.192  hosts .193 - .254   broadcast 192.168.10.255\n"
  "  Mask 255.255.255.192 - each /26 = 64 addresses, 62 usable\n"
  "  (2 lost per subnet to the network ID and the broadcast address).\n"
  "\n"
  "Part B - Assign the first usable address of subnet 2 and verify (Lab 2):\n"
  "ip addr add 192.168.10.65/26 dev eth0 label eth0:1\n"
  "ip -4 addr show eth0          # shows inet 192.168.10.65/26 ... eth0:1\n"
  "ip addr del 192.168.10.65/26 dev eth0     # clean up\n"
  "\n"
  "Part C - Capture and map the headers to OSI layers (Lab 1):\n"
  "apt update && apt install -y tcpdump curl\n"
  "ip -brief addr                            # confirm eth0 is UP\n"
  "tcpdump -i eth0 -nn -e -A -c 10 'tcp port 80' &\n"
  "curl -s http://example.com > /dev/null\n"
  "kill %1\n"
  "\n"
  "  Layer 2 (Data Link) = the link/ether MAC source+destination (shown by -e)\n"
  "  Layer 3 (Network)   = the IP source and destination addresses\n"
  "  Layer 4 (Transport) = the TCP source/destination ports and flags\n"
  "  Layer 7 (Application) = the HTTP request itself, e.g. GET / HTTP/1.1 (shown by -A)\n"
  "\n"
  "Well-known ports (Lab 4 - verify with: ss -tulnp / getent services https):\n"
  "  HTTP 80/TCP   HTTPS 443/TCP   SSH 22/TCP   DNS 53/UDP (TCP for zone transfer/large replies)\n"
  "Award the mark where the four subnets are correct, the address is assigned and shown,\n"
  "and each header is placed at the right layer with the correct port numbers."),
 ("Task 2", "LO2",
  "Implement the core network between the two offices (Network Implementation). "
  "Part A — Build a routed topology with Linux network namespaces: create namespaces for office-a, a router r1 "
  "and office-b, join them with two veth pairs, address them in two different /24 subnets, enable IP forwarding "
  "on the router, add the static routes each host needs, and prove end-to-end connectivity with ping. "
  "Part B — Segment the branch LAN: create two 802.1Q VLAN sub-interfaces (VLAN 10 for Sales and VLAN 20 for "
  "Finance) on eth0, give each its own subnet, bring them up and verify the VLAN ID, and explain the difference "
  "between an access port and a trunk port. "
  "Part C — Configure NAT/PAT with iptables so that the internal subnet reaches the Internet through the host's "
  "single public interface, and state how you would prove the translation actually happened. (Labs 8, 9 and 12.)",
  BOX_CAP,
  "Part A - Static routing across a router namespace (Lab 8):\n"
  "ip netns add a; ip netns add r1; ip netns add b\n"
  "ip link add a-r type veth peer name r-a\n"
  "ip link add b-r type veth peer name r-b\n"
  "ip link set a-r netns a;  ip link set r-a netns r1\n"
  "ip link set b-r netns b;  ip link set r-b netns r1\n"
  "ip netns exec a  ip addr add 10.1.1.2/24 dev a-r\n"
  "ip netns exec r1 ip addr add 10.1.1.1/24 dev r-a\n"
  "ip netns exec r1 ip addr add 10.2.2.1/24 dev r-b\n"
  "ip netns exec b  ip addr add 10.2.2.2/24 dev b-r\n"
  "for n in a r1 b; do ip netns exec $n ip link set lo up; done\n"
  "ip netns exec a  ip link set a-r up;  ip netns exec r1 ip link set r-a up\n"
  "ip netns exec r1 ip link set r-b up;  ip netns exec b  ip link set b-r up\n"
  "ip netns exec r1 sysctl -w net.ipv4.ip_forward=1      # a router MUST forward\n"
  "ip netns exec a ip route add 10.2.2.0/24 via 10.1.1.1\n"
  "ip netns exec b ip route add 10.1.1.0/24 via 10.2.2.1\n"
  "ip netns exec a ping -c2 10.2.2.2                     # end-to-end proof\n"
  "ip netns exec a ip route                              # show the route is installed\n"
  "\n"
  "Part B - 802.1Q VLAN sub-interfaces (Lab 9):\n"
  "modprobe 8021q && lsmod | grep 8021q\n"
  "ip link add link eth0 name eth0.10 type vlan id 10    # Sales   VLAN 10\n"
  "ip link add link eth0 name eth0.20 type vlan id 20    # Finance VLAN 20\n"
  "ip addr add 192.168.10.1/24 dev eth0.10\n"
  "ip addr add 192.168.20.1/24 dev eth0.20\n"
  "ip link set eth0.10 up; ip link set eth0.20 up\n"
  "ip -d link show eth0.10                               # -d prints the VLAN id\n"
  "tcpdump -i eth0 -nn -e vlan &                         # see the 4-byte 802.1Q tag\n"
  "  An ACCESS port carries ONE untagged VLAN to an end device;\n"
  "  a TRUNK port carries MANY VLANs, tagging each frame with its 802.1Q VLAN ID.\n"
  "  Traffic between VLAN 10 and VLAN 20 needs a Layer 3 hop (SVI / router-on-a-stick).\n"
  "\n"
  "Part C - NAT / PAT with iptables (Lab 12):\n"
  "sysctl -w net.ipv4.ip_forward=1\n"
  "iptables -t nat -A POSTROUTING -s 10.1.1.0/24 -o eth0 -j MASQUERADE\n"
  "ip netns exec a ping -c2 8.8.8.8\n"
  "ip netns exec a curl -s ifconfig.me   # prints the HOST public IP, not 10.1.1.2 -> translated\n"
  "conntrack -L | head                   # translation table: src=10.1.1.2 ... [SRC=<public-ip>]\n"
  "  MASQUERADE is dynamic source NAT that reuses the outgoing interface address and\n"
  "  tracks the source port, so many internal hosts share one public IP (PAT / overload).\n"
  "Award the mark where the ping across the router succeeds, both VLAN IDs are shown, and\n"
  "the candidate can evidence the translation (ifconfig.me or conntrack)."),
 ("Task 3", "LO3",
  "Bring the network under management and secure it (Network Operations & Security). "
  "Part A — Install and configure SNMP on the host with a read-only community, then walk the system MIB and read "
  "a specific value such as sysUpTime; state why SNMPv3 is preferred in production. "
  "Part B — Set up centralised logging: make rsyslog listen for forwarded logs, add a forwarding rule to the "
  "collector, restart the service, generate a test event with logger and prove the event arrived. "
  "Part C — Restrict access to the management port: use the UFW host firewall to deny inbound by default and "
  "permit only SSH, then write an iptables ACL that permits TCP/3306 only from 10.0.0.0/24 and drops it from "
  "everywhere else — and explain why the rule ORDER matters. (Labs 15, 17, 21 and 27.)",
  BOX_CAP,
  "Part A - SNMP monitoring (Lab 15):\n"
  "apt update && apt install -y snmpd snmp snmp-mibs-downloader\n"
  "sed -i 's/^agentaddress.*/agentaddress udp:127.0.0.1:161/' /etc/snmp/snmpd.conf\n"
  "echo 'rocommunity public 127.0.0.1' >> /etc/snmp/snmpd.conf\n"
  "systemctl restart snmpd\n"
  "snmpwalk -v2c -c public 127.0.0.1 system          # sysDescr, sysName, sysUpTime\n"
  "snmpget  -v2c -c public 127.0.0.1 sysUpTime.0     # one specific OID\n"
  "snmpwalk -v2c -c public 127.0.0.1 IF-MIB::ifInOctets   # interface counters\n"
  "  v2c authenticates with a PLAINTEXT community string; SNMPv3 adds authentication\n"
  "  and encryption (authPriv) and is what production should use.\n"
  "\n"
  "Part B - Centralised logging with rsyslog (Lab 17):\n"
  "sed -i 's/#module(load=\"imtcp\")/module(load=\"imtcp\")/' /etc/rsyslog.conf\n"
  "sed -i 's/#input(type=\"imtcp\" port=\"514\")/input(type=\"imtcp\" port=\"514\")/' /etc/rsyslog.conf\n"
  "echo '*.* @@127.0.0.1:514' > /etc/rsyslog.d/50-forward.conf   # @@ = TCP, @ = UDP\n"
  "systemctl restart rsyslog\n"
  "ss -tlnp | grep 514                               # collector is listening\n"
  "logger -p local0.info \"NetTech Solutions PP test event\"\n"
  "grep 'NetTech Solutions PP test event' /var/log/syslog        # proof it landed\n"
  "  Messages are tagged by FACILITY (local0, auth, daemon...) and SEVERITY 0-7\n"
  "  (0 Emergency -> 7 Debug); a SIEM correlates them across devices.\n"
  "\n"
  "Part C - Host firewall and ACL (Labs 21 and 27):\n"
  "apt install -y ufw\n"
  "ufw default deny incoming\n"
  "ufw default allow outgoing\n"
  "ufw allow 22/tcp                 # allow SSH BEFORE enabling, or you lock yourself out\n"
  "ufw --force enable\n"
  "ufw status verbose\n"
  "# iptables ACL - permit MySQL only from 10.0.0.0/24, drop it from anywhere else:\n"
  "iptables -I INPUT -p tcp --dport 3306 -s 10.0.0.0/24 -j ACCEPT   # -I inserts at the TOP\n"
  "iptables -A INPUT -p tcp --dport 3306 -j DROP                    # -A appends BELOW it\n"
  "iptables -L INPUT -n -v --line-numbers                           # verify the order\n"
  "nc -zv 127.0.0.1 3306                                            # blocked from other sources\n"
  "  ORDER MATTERS: an ACL is read top-down and the FIRST match wins, so the specific\n"
  "  ACCEPT must sit above the general DROP - reverse them and the permit is dead.\n"
  "Award the mark where a MIB value is actually returned, the log event is shown in\n"
  "/var/log/syslog, and the candidate explains first-match-wins ACL ordering."),
 ("Task 4", "LO4",
  "Troubleshoot a fault on the company web service (Network Troubleshooting). A user reports that "
  "web.nettech.local is unreachable from the branch office. Work the fault with the seven-step CompTIA "
  "troubleshooting methodology and show the command evidence at each stage. "
  "Part A — Identify the problem and test reachability and the path with ping and traceroute / mtr, and state "
  "what '* * *' in a traceroute really means. "
  "Part B — Establish and test a DNS theory: confirm which resolver the host is using, resolve the service name "
  "with dig / nslookup against two different resolvers, and name the response code you would see for a "
  "non-existent name. "
  "Part C — Test the transport and service layers: capture traffic to the service with tcpdump, check whether "
  "the port is listening with ss, prove the TCP handshake with nc and the certificate/HTTP response with "
  "openssl s_client and curl -v. Then state your root-cause conclusion and the last two steps of the "
  "methodology. (Labs 29, 30, 32 and 36.)",
  BOX_CAP,
  "The 7 steps: 1 Identify the problem  2 Establish a theory of probable cause\n"
  "3 Test the theory  4 Establish a plan of action  5 Implement the solution or escalate\n"
  "6 Verify full functionality and prevent recurrence  7 Document findings.\n"
  "\n"
  "Part A - Step 1-3: reachability and path (Lab 29):\n"
  "apt update && apt install -y traceroute mtr-tiny dnsutils\n"
  "ping -c5 web.nettech.local        # read time= (RTT) and the loss summary\n"
  "traceroute web.nettech.local      # one line per hop, three RTT samples\n"
  "mtr -rwc 20 web.nettech.local     # -r report mode, -w wide, sustained loss per hop\n"
  "  '* * *' normally means that hop does not REPLY to the probe (ICMP filtered/rate-limited)\n"
  "  - it is not proof of a fault unless loss continues at every hop AFTER it.\n"
  "\n"
  "Part B - DNS theory (Lab 30):\n"
  "cat /etc/resolv.conf              # 127.0.0.53 => going through systemd-resolved\n"
  "resolvectl status | head -20\n"
  "dig web.nettech.local +short\n"
  "dig @1.1.1.1 web.nettech.local +short\n"
  "dig @8.8.8.8 web.nettech.local +short   # one resolver answering, the other not = resolver fault\n"
  "dig +trace web.nettech.local            # walk root -> TLD -> authoritative\n"
  "nslookup web.nettech.local\n"
  "resolvectl flush-caches                 # rule out a stale cached answer\n"
  "  A name that does not exist returns NXDOMAIN; a broken/unreachable authoritative\n"
  "  server returns SERVFAIL.\n"
  "\n"
  "Part C - Transport and service triage (Labs 32 and 36):\n"
  "apt install -y tcpdump tshark curl netcat-openbsd openssl\n"
  "tcpdump -i eth0 -nn -w /tmp/web.pcap 'host <server-ip> and tcp port 443' -c 20 &\n"
  "curl -s https://web.nettech.local > /dev/null; wait\n"
  "tcpdump -nn -r /tmp/web.pcap | head            # SYN with no SYN-ACK = blocked/not listening\n"
  "ss -tulpn | grep -E ':(80|443)'                # is the service actually LISTENING?\n"
  "nc -zv web.nettech.local 443                   # 'succeeded' = routing+firewall+listener OK\n"
  "echo | openssl s_client -connect web.nettech.local:443 \\\n"
  "  -servername web.nettech.local 2>/dev/null | head -20    # subject=/issuer=/expiry\n"
  "curl -v https://web.nettech.local 2>&1 | head -30         # HTTP status code\n"
  "curl -w \"DNS:%{time_namelookup} TCP:%{time_connect} TLS:%{time_appconnect} \\\n"
  "TTFB:%{time_starttransfer} TOTAL:%{time_total}\\n\" -o /dev/null -s https://web.nettech.local\n"
  "\n"
  "Root-cause conclusion - isolate the fault to the layer where the FIRST test fails:\n"
  "  link/interface down -> routing or default gateway -> DNS resolution -> TCP port\n"
  "  filtered or service not listening -> TLS certificate -> HTTP application error.\n"
  "  e.g. ping to the IP succeeds but the name does not resolve => DNS fault, not the web server;\n"
  "  nc refused while ss shows nothing on :443 => the service is down, not the network.\n"
  "Steps 6 and 7: after fixing, VERIFY full functionality end-to-end (re-run curl from the\n"
  "user's host) and put a preventive measure in place, then DOCUMENT the symptom, cause,\n"
  "action and outcome in the ticket / knowledge base.\n"
  "Award the mark where the candidate follows the steps in order, shows real command\n"
  "output at each layer, and states a conclusion supported by that evidence."),
]

# ---------------------------------------------------------------- doc helpers
def base_doc():
    doc = Document()
    n = doc.styles["Normal"]; n.font.name = "Arial"; n.font.size = Pt(11)
    return doc

def para(doc, text, size=11, bold=False, italic=False, color=None, after=6, before=0, align=None):
    p = doc.add_paragraph(); r = p.add_run(text)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic
    if color: r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(before)
    if align is not None: p.alignment = align
    return p

def heading(doc, text, size=13):
    para(doc, text, size=size, bold=True, color=BRAND, after=6, before=8)

def answer_box(doc, lines=None, code=None, height_pt=90):
    """1x1 bordered box. `lines` → bullet-style model answer; `code` → monospace
    code/YAML/command block (indentation preserved); neither → empty answer space."""
    t = doc.add_table(rows=1, cols=1); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.rows[0].cells[0]
    cell.paragraphs[0].text = ""
    if code:
        run = cell.paragraphs[0].add_run("Suggestive answers (not exhaustive):")
        run.bold = True; run.font.size = Pt(10.5)
        # A long line must not wrap to column 0 (it destroys the indentation and reads
        # as a broken token across a page break). Hang the continuation under the line
        # and step the size down for the longest lines so they fit the box frame.
        for ln in code.split("\n"):
            b = cell.add_paragraph(style=None)
            b.paragraph_format.space_after = Pt(0); b.paragraph_format.space_before = Pt(0)
            b.paragraph_format.left_indent = Inches(0.22)
            b.paragraph_format.first_line_indent = Inches(-0.22)
            b.paragraph_format.keep_together = True
            b.paragraph_format.keep_with_next = True
            rr = b.add_run(ln if ln else " ")
            rr.font.name = "Consolas"
            rr.font.size = Pt(9 if len(ln) <= 78 else (8 if len(ln) <= 92 else 7.5))
            rr._element.rPr.rFonts.set(qn('w:cs'), "Consolas")
            wt = rr._element.find(qn('w:t'))
            if wt is not None: wt.set(qn('xml:space'), 'preserve')
    elif lines:
        run = cell.paragraphs[0].add_run("Suggestive answers (not exhaustive):")
        run.bold = True; run.font.size = Pt(10.5)
        for ln in lines:
            b = cell.add_paragraph(style=None); b.paragraph_format.left_indent = Inches(0.15)
            rr = b.add_run("•  " + ln); rr.font.size = Pt(10.5)
    else:
        # empty answer space
        tr = t.rows[0]._tr
        trPr = tr.get_or_add_trPr(); trh = OxmlElement('w:trHeight')
        trh.set(qn('w:val'), str(int(height_pt*20))); trh.set(qn('w:hRule'), 'atLeast'); trPr.append(trh)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

FILL_GAP = 6    # extra space below each fill-in line (paired with double line spacing for writing room)

def candidate_block(doc):
    heading(doc, "Trainee Information")
    for label in ["Trainee Name (as per NRIC): ______________________________________",
                  "Last 3 digits and alphabet of NRIC/FIN: ____________________",
                  "Date: ____________________"]:
        p = para(doc, label, size=11, after=FILL_GAP)
        p.paragraph_format.line_spacing = 2.0

# Assessment briefing (from the course slides — "Briefing for Assessment").
BRIEFING = [
    "Place phones and other materials under the table or on the floor.",
    "No photos or recording of assessment scripts.",
    "No discussion during the assessment.",
    "Use a black/blue pen for hard-copy assessments.",
    "No liquid paper / correction tape.",
    "Scripts are collected when time is up.",
]

LMS_URL = "https://lms-tms.tertiaryinfotech.com/"

def add_hyperlink(p, url, text):
    """Add a real clickable Word hyperlink (blue, underlined) to paragraph p."""
    r_id = p.part.relate_to(
        url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True)
    link = OxmlElement("w:hyperlink"); link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r"); rPr = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "22"); rPr.append(sz)  # 11pt
    color = OxmlElement("w:color"); color.set(qn("w:val"), "0563C1"); rPr.append(color)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rPr.append(u)
    run.append(rPr)
    t = OxmlElement("w:t"); t.text = text; run.append(t)
    link.append(run); p._p.append(link)
    return link

def instructions(doc, minutes_text):
    heading(doc, "Instructions to Candidate")
    # None marks the upload instruction, which carries a clickable LMS hyperlink.
    items = [
        "This is an individual exercise.",
        "This is an open-book assessment.",
        f"A total of {minutes_text} is given to complete this assessment.",
        None,
    ] + BRIEFING
    for i, s in enumerate(items, 1):
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(4)
        if s is None:
            p.add_run(f"{i}.  Complete your answers on the document provided and "
                      "upload the completed answers to the LMS at ").font.size = Pt(11)
            add_hyperlink(p, LMS_URL, LMS_URL)
            p.add_run(".").font.size = Pt(11)
        else:
            p.add_run(f"{i}.  {s}").font.size = Pt(11)

def grading(doc, what):
    heading(doc, "Grading")
    para(doc, what, size=11, after=12)
    for ln in ["Grade: _______  (C / NYC)",
               "Assessor Name: __________________________   Assessor NRIC: ________________",
               "Date: ________________________                    Signature: ____________________"]:
        p = para(doc, ln, size=11, after=FILL_GAP)
        p.paragraph_format.line_spacing = 2.0

def finish(doc, path):
    prodoc.add_page_numbers(doc); prodoc.enable_update_fields(doc)
    doc.save(path); print("  saved:", os.path.basename(path))

# ---------------------------------------------------------------- builders
def build_wa(answers):
    doc = base_doc()
    kind = "Written Assessment (SAQ) — Answer Key" if answers else "Written Assessment (SAQ)"
    prodoc.add_cover_page(doc, kind, TITLE, A_VER if answers else Q_VER,
                          org_logo=ORG_LOGO, course_logo=COURSE_LOGO)
    para(doc, TITLE, size=15, bold=True, color=DARK, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, "Answers to Written Assessment (SAQ)" if answers else "Written Assessment (SAQ)",
         size=13, bold=True, color=BRAND, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, f"Course Code: {COURSE_CODE}", size=11, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, after=12)
    if not answers:
        # Page 2 — candidate information, instructions and grading; questions begin on the next page.
        candidate_block(doc); instructions(doc, "1 hour")
        grading(doc, "Candidate has answered all written questions and demonstrated the underpinning "
                     "knowledge required for the course learning outcomes.")
        page_break(doc)
    para(doc, "Short-Answer Questions (Knowledge)", size=13, bold=True, color=BRAND, after=4)
    para(doc, "Answer all questions in your own words. Each question tests underpinning knowledge covered in the "
              "course slides.", size=10.5, italic=True, color=GREY, after=8)
    # Pagination is EXPLICIT — two questions to a page on the paper, one model answer to a
    # page in the key. Do not swap this for Word's keepNext/cantSplit: Word pushes an
    # oversized box to the next page, but Google Docs draws the border anyway and prints the
    # question text and the page footer straight THROUGH it. See SKILL.md → Pagination.
    per_page = 1 if answers else 2
    for i, (crit, ctx, q, pts) in enumerate(WRITTEN, 1):
        para(doc, f"Question {i}:", size=11.5, bold=True, after=2, before=6)
        para(doc, ctx, size=11, after=3)
        para(doc, f"{q}  ({crit})", size=11, bold=True, after=4)
        answer_box(doc, lines=pts if answers else None)
        if i % per_page == 0 and i < len(WRITTEN):
            page_break(doc)
    suffix = A_VER if answers else Q_VER
    name = (f"Answer to WA (SAQ) - {TITLE} - {suffix}.docx" if answers
            else f"WA (SAQ) - {TITLE} - {suffix}.docx")
    finish(doc, os.path.join(OUT, name))

def build_pp(answers):
    doc = base_doc()
    kind = "Practical Performance (PP) — Answer Key" if answers else "Practical Performance (PP)"
    prodoc.add_cover_page(doc, kind, TITLE, A_VER if answers else Q_VER,
                          org_logo=ORG_LOGO, course_logo=COURSE_LOGO)
    para(doc, TITLE, size=15, bold=True, color=DARK, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, "Answers to Practical Performance Assessment" if answers else "Practical Performance Assessment",
         size=13, bold=True, color=BRAND, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, f"Course Code: {COURSE_CODE}", size=11, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, after=12)
    if not answers:
        # Page 2 — candidate information, instructions and grading; the problem begins on the next page.
        candidate_block(doc); instructions(doc, "90 minutes")
        grading(doc, "Candidate has successfully completed all PP tasks and can explain the overall "
                     "functions and features used to achieve them.")
        page_break(doc)
    para(doc, "Practical Problem", size=13, bold=True, color=BRAND, after=4)
    para(doc, "Scenario", size=11.5, bold=True, after=2)
    para(doc, SCENARIO, size=11, after=8)
    # Practical tasks are long and their boxes are tall, so they get a page each — on the
    # paper AND in the key. Same rule as the WA: the page break is ours, not the renderer's.
    for i, (label, crit, prompt, cap, pts) in enumerate(PRACTICAL, 1):
        para(doc, f"{label} ({crit}):", size=11.5, bold=True, after=2, before=6)
        para(doc, prompt, size=11, after=3)
        para(doc, cap, size=10.5, italic=True, color=GREY, after=4)
        answer_box(doc, code=pts if answers else None, height_pt=150)
        if i < len(PRACTICAL):
            page_break(doc)
    suffix = A_VER if answers else Q_VER
    name = (f"Answer to PP Assessment - {TITLE} - {suffix}.docx" if answers
            else f"PP Assessment - {TITLE} - {suffix}.docx")
    finish(doc, os.path.join(OUT, name))

if __name__ == "__main__":
    print("Building WSQ assessment set…")
    build_wa(answers=False); build_wa(answers=True)
    build_pp(answers=False); build_pp(answers=True)
    print(f"Done. WA: {len(WRITTEN)} questions · PP: {len(PRACTICAL)} tasks.")
