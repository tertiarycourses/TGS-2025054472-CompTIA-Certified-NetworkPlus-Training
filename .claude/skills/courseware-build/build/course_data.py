"""
SINGLE SOURCE OF TRUTH — course metadata for the WSQ CompTIA Certified
Network+ Training (N10-009) course. Every artifact (PPT, LP, LG, LG.md, labs
index) is generated from this file + data_domain1..5.py so they stay 100%
aligned with the five official N10-009 exam domains.
"""

# ------------------------------------------------------------------ metadata
TITLE        = "CompTIA Certified Network+ Training (N10-009)"
SHORT_TITLE  = "CompTIA Network+ (N10-009)"     # used in output filenames
COURSE_CODE  = "TGS-2025054472"
VERSION      = "v2.1"
VERSION_DATE = "19 August 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr. Alfred Ang"
DAYS         = 5
EXAM_CODE    = "N10-009"

REGISTER_URL = "https://www.tertiarycourses.com.sg/wsq-comptia-certified-network-training.html"
PRACTICE_EXAM_URL = "https://exams.tertiaryinfotech.com/practice-exams/comptia/comptia-network-plus"
REPO_URL     = "https://github.com/tertiarycourses/TGS-2025054472-CompTIA-Certified-NetworkPlus-Training"

# free web ed-tools used across the labs
TOOLS = dict(
    ipcalc   = "https://alfredang.github.io/ipcalculator/",
    pcap     = "https://alfredang.github.io/pcapanalyzer/",
    cybersim = "https://alfredang.github.io/cybersecuritysimulator/",
    regex    = "https://alfredang.github.io/regexgenerator/",
    killercoda = "https://killercoda.com/playgrounds/scenario/ubuntu",
)

# ------------------------------------------------------------------ outcomes
LEARNING_OUTCOMES = [
    "LO1: Explain networking concepts — the OSI model, network appliances, cloud concepts, "
    "ports and protocols, traffic types, transmission media, transceivers and connectors, "
    "network topologies and IPv4/IPv6 addressing and subnetting. (K1, K2)",
    "LO2: Implement networks — static and dynamic routing (BGP, EIGRP, OSPF), NAT/PAT, "
    "802.1Q VLANs, trunking, spanning tree, link aggregation, wireless devices and "
    "physical installation considerations. (K3, A1, A2)",
    "LO3: Operate and maintain networks — documentation and IPAM, life-cycle and change "
    "management, configuration backup and baselines, SNMP/flow/log monitoring, disaster "
    "recovery, DHCP/DNS/NTP network services and secure access methods. (K4, A3, A4)",
    "LO4: Secure networks — encryption and PKI, IAM/MFA/SSO, RADIUS/TACACS+, physical "
    "security, deception technologies, segmentation, common attacks and defence features "
    "such as hardening, NAC, ACLs and screened subnets. (K5, A5)",
    "LO5: Troubleshoot networks — apply the CompTIA troubleshooting methodology with the "
    "right tools to cabling, interface, switching, routing, service and performance "
    "issues. (K6, A6)",
]

# ------------------------------------------------------------------ topics (= the five N10-009 exam domains)
TOPICS = [
    dict(num=1, code="1.0",
         title="Networking Concepts",
         subtitle="OSI model · appliances · cloud · ports & protocols · traffic types · media · "
                  "transceivers & connectors · topologies · IPv4 addressing",
         weighting="23%",
         concepts=[
            ("OSI model", "Seven layers — physical, data link, network, transport, session, presentation, application — and the PDU at each."),
            ("Appliances & functions", "Routers, switches, firewalls, IDS/IPS, load balancers, proxies, NAS/SAN and wireless devices — physical and virtual."),
            ("Cloud concepts", "NFV, VPC, network security groups/lists, cloud gateways, public/private/hybrid deployment, SaaS/IaaS/PaaS service models."),
            ("Ports & protocols", "FTP, SFTP, SSH, Telnet, SMTP, DNS, DHCP, HTTP/HTTPS, SNMP, LDAP, RDP, SIP — number, transport and purpose."),
            ("Traffic types", "Unicast, multicast, anycast and broadcast delivery."),
            ("Media, transceivers & connectors", "802.11/cellular/satellite wireless; fibre, coax and DAC wired media; SC/LC/ST/MPO, RJ11/RJ45, F-type and BNC."),
            ("Topologies", "Mesh, hybrid, star (hub-and-spoke), spine-and-leaf, point-to-point, three-tier and collapsed core."),
            ("IPv4 addressing", "Public vs private (RFC1918), APIPA, loopback, classes A–E, VLSM and CIDR subnetting."),
         ]),
    dict(num=2, code="2.0",
         title="Network Implementation",
         subtitle="Routing technologies · switching technologies · wireless devices · physical installations",
         weighting="20%",
         concepts=[
            ("Routing technologies", "Static vs dynamic routing — BGP, EIGRP, OSPF — route selection, NAT/PAT, FHRP, VIP and subinterfaces."),
            ("Switching technologies", "VLANs and SVIs, interface configuration, 802.1Q trunking, spanning tree, MTU and jumbo frames."),
            ("Wireless devices", "Channels and channel width, 2.4/5/6 GHz bands, SSIDs, encryption, guest networks, authentication, antennas and AP placement."),
            ("Physical installations", "Installation implications, power (UPS, PDU) considerations and environmental factors (HVAC, fire suppression)."),
         ]),
    dict(num=3, code="3.0",
         title="Network Operations",
         subtitle="Documentation · life-cycle · change & configuration management · monitoring · DR · "
                  "network services · access & management",
         weighting="19%",
         concepts=[
            ("Documentation", "Physical vs logical diagrams, rack diagrams, cable maps, asset inventory, IPAM, SLA and wireless surveys."),
            ("Life-cycle & change", "EOL/EOS, software management, decommissioning and the change-request process."),
            ("Configuration management", "Production, backup and baseline configurations."),
            ("Network monitoring", "SNMP, flow data, packet capture, baseline metrics, log aggregation, API integration and port mirroring."),
            ("Disaster recovery", "RPO, RTO, MTTR, MTBF; cold/warm/hot sites; active-active vs active-passive; DR testing."),
            ("Network services", "DHCP, SLAAC, DNS, NTP, PTP and NTS."),
            ("Access & management", "Site-to-site and client VPNs, SSH, GUI, API and console access."),
         ]),
    dict(num=4, code="4.0",
         title="Network Security",
         subtitle="Logical & physical security · deception · terminology · audits & compliance · "
                  "segmentation · attacks · defence features",
         weighting="14%",
         concepts=[
            ("Logical security", "Encryption in transit/at rest, PKI, IAM, MFA, SSO, RADIUS, LDAP, SAML, TACACS+, least privilege, RBAC and geofencing."),
            ("Physical & deception", "Cameras and locks; honeypots and honeynets."),
            ("Terminology & compliance", "Risk, vulnerability, exploit, threat, the CIA triad; data locality, PCI DSS and GDPR."),
            ("Segmentation", "IoT/IIoT, SCADA/ICS/OT, guest and BYOD network segmentation."),
            ("Attacks", "DoS/DDoS, VLAN hopping, MAC flooding, ARP/DNS poisoning and spoofing, rogue devices, evil twin, on-path and social engineering."),
            ("Defence features", "Device hardening, NAC, key management, ACLs, URL/content filtering, trusted vs untrusted zones and screened subnets."),
         ]),
    dict(num=5, code="5.0",
         title="Network Troubleshooting",
         subtitle="Methodology · cabling & physical interfaces · network services · performance · tools",
         weighting="24%",
         concepts=[
            ("Methodology", "Identify the problem → establish a theory → test → plan and implement → verify → document findings."),
            ("Cabling & interface issues", "Incorrect cable type, signal degradation, improper termination, TX/RX transposed, error counters, port status, PoE and transceiver mismatch."),
            ("Network service issues", "STP problems, VLAN assignment, ACLs, routing-table and default-route faults, address-pool exhaustion, wrong gateway/IP/mask."),
            ("Performance issues", "Congestion, latency, packet loss and wireless interference."),
            ("Tools & protocols", "Protocol analyzers, command-line tools, cable testers and Wi-Fi analyzers."),
         ]),
]

# ------------------------------------------------------------------ day themes (8 training hours/day)
DAY_THEMES = {
    1: "Networking Concepts",
    2: "Network Implementation",
    3: "Network Operations",
    4: "Network Security",
    5: "Network Troubleshooting & Assessment",
}

# ------------------------------------------------------------------ assessment
ASSESSMENT = dict(
    written="Written Assessment (WA) — Short-Answer Questions (SAQ), 1 hour, open book.",
    practical="Practical Performance (PP) — hands-on networking tasks, 90 minutes, open book.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding.",
)

RECOMMENDED_COURSES = [
    "WSQ CompTIA Certified Security+ Training",
    "WSQ CompTIA Certified PenTest+ Training",
    "WSQ CompTIA Certified CySA+ Cybersecurity Analyst Training",
    "WSQ CompTIA Certified Linux+ Training",
    "WSQ CompTIA Certified Cloud+ Training",
]
