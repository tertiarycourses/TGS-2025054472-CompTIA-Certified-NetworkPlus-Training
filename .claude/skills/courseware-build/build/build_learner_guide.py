#!/usr/bin/env python3
"""Generate the CompTIA Network+ (N10-009) Learner Guide as BOTH a Markdown mirror (LG-*.md at repo
root) and a DOCX (courseware/LG-*.docx) from one source, so they never diverge.

House format: cover page, Document Version Control Record, auto TOC, Arial 11pt
body, one section per lab (Objective · Goal · What you'll build · Step-by-step
with commands · Test it · If it doesn't work), plus setup, exam-prep and
glossary. All content is driven by course_data + the domain data files, keeping
the LG 100% aligned with the slide deck, Lesson Plan and labs.
"""
import os, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3; from data_domain4 import DOMAIN4
from data_domain5 import DOMAIN5
ACT=DOMAIN1+DOMAIN2+DOMAIN3+DOMAIN4+DOMAIN5
import prodoc, glob
def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE); ASSETS=os.path.join(os.path.dirname(HERE),"assets")

def lab_folder(num):
    """Repo-relative path of the lab's folder (labs/lab-NN-slug)."""
    hits=sorted(glob.glob(os.path.join(REPO,"labs","lab-%02d-*"%num)))
    for h in hits:
        if os.path.isdir(h): return "labs/"+os.path.basename(h)
    for h in hits:
        return "labs/"+os.path.basename(h)
    return "labs/lab-%02d"%num

# ---------------- block DSL (single content stream → MD + DOCX) ----------------
B=[]
def h1(t): B.append(("h1",t))
def h2(t): B.append(("h2",t))
def h3(t): B.append(("h3",t))
def p(t):  B.append(("p",t))
def bullets(xs): B.append(("bullets",xs))
def steps(xs): B.append(("steps",xs))
def code(t): B.append(("code",t))
def note(t): B.append(("note",t))
def rule(): B.append(("rule",))
def figure(path, caption): B.append(("figure", path, caption))

FIGDIR=os.path.join(REPO,"courseware","assets","figures")
def lab_figure(num):
    """Repo-relative path of the lab's process-map figure, or None."""
    p=os.path.join(FIGDIR,"lab-%02d-process.png"%num)
    return p if os.path.exists(p) else None

# ---------------- content ----------------
h1("Introduction")
p(f"This Learner Guide accompanies the WSQ course {C.TITLE} ({C.COURSE_CODE}), conducted by {C.ORG}. "
  "It provides step-by-step instructions for all 36 hands-on labs, organised by the five official "
  "CompTIA Network+ N10-009 exam domains. Every lab maps to a published exam objective and runs on "
  "the free Killercoda Ubuntu Playground in your browser, supported by free TIS web tools — no "
  "installation on your own machine is required.")
p("Use this guide alongside the course slides and the per-lab folders in the labs/ directory of the "
  "course repository — each lab has its own folder with a README containing the full commands. The "
  "slides teach the concepts; this guide carries the complete step-by-step procedure for every lab.")

h1("Course Learning Outcomes")
bullets(C.LEARNING_OUTCOMES)

h1("Before You Start — Environment Setup")
h3("What you need")
bullets([
 "A modern browser — every lab runs in the free Killercoda Ubuntu Playground: "+C.TOOLS["killercoda"],
 "TIS IP Calculator (subnetting): "+C.TOOLS["ipcalc"],
 "TIS PCAP Analyzer (packet captures): "+C.TOOLS["pcap"],
 "TIS Cybersecurity Simulator (attack recognition): "+C.TOOLS["cybersim"],
 "TIS Regex Generator (log filtering): "+C.TOOLS["regex"],
 "Lab 11 (Wireless) optionally uses your own laptop's Wi-Fi radio with a free Wi-Fi analyzer app.",
])
h3("Launch and verify the playground")
p("Open the Killercoda Ubuntu Playground and wait for the terminal prompt. The VM is disposable — "
  "if a lab leaves the network in a broken state, simply close the session and start a fresh one. "
  "Confirm the basics before you begin:")
code("id                     # you are root (or use sudo)\nip addr show           # the primary interface and its IP\napt update             # refresh package lists\nping -c 2 8.8.8.8      # outbound connectivity")
h3("Conventions used in every lab")
bullets([
 "Commands are run in the Killercoda terminal; a leading sudo is shown where root is required.",
 "Placeholders such as <ip>, <interface> and <subnet> are replaced with your own lab values.",
 "Each lab ends with a Test-it check — do not move on until it passes.",
 "Reset the playground between labs that change routing, firewall or DHCP state.",
 "Web-tool steps (IP Calculator, PCAP Analyzer, Simulator, Regex Generator) open in a second browser tab.",
])

# ---------------- per-domain, per-lab ----------------
for t in C.TOPICS:
    h1(f"Domain {t['code']} — {t['title']}  ({t['weighting']})")
    p(t["subtitle"])
    h3("Key concepts")
    bullets([f"{k} — {v}" for k,v in t["concepts"]])
    for a in [x for x in ACT if x["topic"]==t["num"]]:
        h2(f"Lab {a['num']} — {a['title']}")
        p(f"Exam objective: {a['objective']}")
        p(f"Goal: {a['desc']}")
        h3("What you'll build")
        p(a["build"]+f"   (Tools: {a['services']}.)")
        fig=lab_figure(a["num"])
        if fig:
            figure(fig, f"Figure {a['num']} — how Lab {a['num']} runs: the workflow you will follow.")
        h3("Step-by-step")
        steps([(instr,cmd) for instr,cmd in a["steps"]])
        h3("Test it")
        p(a["test"])
        if a.get("troubleshoot"):
            h3("If it doesn't work")
            bullets([f"{sym} — {fix}" for sym,fix in a["troubleshoot"]])
        note(f"The full lab file with all commands is in {lab_folder(a['num'])}/ in the course repository.")
        rule()

h1("Exam Focus — Quick References")
p("These cross-cutting references are examined throughout N10-009. Revise them alongside the labs.")
h3("Well-known ports to memorise")
bullets([
 "FTP 20/21 (TCP) · SFTP/SSH 22 (TCP) · Telnet 23 (TCP) · SMTP 25/587 (TCP) · DNS 53 (TCP+UDP)",
 "DHCP 67/68 (UDP) · TFTP 69 (UDP) · HTTP 80 (TCP) · NTP 123 (UDP) · SNMP 161/162 (UDP)",
 "LDAP 389 / LDAPS 636 (TCP) · HTTPS 443 (TCP) · SMB 445 (TCP) · syslog 514 (UDP) · RDP 3389 (TCP) · SIP 5060/5061 (TCP/UDP)",
])
h3("Subnetting quick method")
bullets([
 "Magic number = 256 − mask octet value. Networks step by the magic number in the interesting octet.",
 "/24=256 addresses; /25=128; /26=64; /27=32; /28=16; /29=8; /30=4. Usable hosts = block − 2.",
 "RFC1918 private ranges: 10.0.0.0/8 · 172.16.0.0/12 · 192.168.0.0/16. APIPA: 169.254.0.0/16. Loopback: 127.0.0.0/8.",
 "Verify every calculation in the TIS IP Calculator: "+C.TOOLS["ipcalc"],
])
h3("The CompTIA seven-step troubleshooting methodology")
bullets([
 "1 · Identify the problem — gather information, question users, determine what changed.",
 "2 · Establish a theory of probable cause — top-down, bottom-up or divide-and-conquer through the OSI layers.",
 "3 · Test the theory to determine the cause.",
 "4 · Establish a plan of action and identify potential effects.",
 "5 · Implement the solution or escalate.",
 "6 · Verify full system functionality and implement preventive measures.",
 "7 · Document findings, actions, outcomes and lessons learned.",
])
rule()

h1("Exam Preparation")
bullets([
 "First pass: complete every lab in the Killercoda playground, reading each lab folder's README.",
 "Second pass: redo the labs from memory until the command workflow is automatic.",
 "Drill subnetting daily until a /26 or /27 split takes under a minute.",
 "Memorise the well-known ports and the 802.11 standards tables from the slides.",
 "Sharpen exam readiness with the Tertiary Infotech Network+ practice exam: "+C.PRACTICE_EXAM_URL,
 "Book the N10-009 exam via a Pearson VUE test centre or online proctoring when practice scores exceed 80%.",
])

h1("Glossary")
gl=[
 ("OSI model","The seven-layer reference model — Physical, Data Link, Network, Transport, Session, Presentation, Application."),
 ("CIDR / VLSM","Classless Inter-Domain Routing and Variable-Length Subnet Masking — sizing subnets by prefix length rather than class."),
 ("RFC1918","The private IPv4 address ranges (10/8, 172.16/12, 192.168/16) that are not routable on the Internet."),
 ("VLAN / 802.1Q","A logical LAN segment; 802.1Q tags frames on a trunk so many VLANs can share one physical link."),
 ("Spanning Tree Protocol (STP)","Blocks redundant switch paths to prevent Layer-2 loops; elects a root bridge via BPDUs."),
 ("NAT / PAT","Network/Port Address Translation — rewriting private source addresses (and ports) to a public address."),
 ("OSPF / EIGRP / BGP","Interior link-state, interior advanced distance-vector and exterior path-vector dynamic routing protocols."),
 ("FHRP / VIP","First-Hop Redundancy Protocol — two routers share a Virtual IP so the default gateway survives a failure."),
 ("SLAAC","IPv6 Stateless Address Autoconfiguration — a host builds its own address from the router-advertised prefix."),
 ("SNMP / MIB / OID","Simple Network Management Protocol; the Management Information Base tree of Object Identifiers a device exposes."),
 ("NetFlow","Flow-level traffic accounting exported by routers/switches — who talked to whom, when, and how much."),
 ("Syslog","The standard log-forwarding protocol (UDP 514) with severity levels 0 (Emergency) to 7 (Debug)."),
 ("RPO / RTO","Recovery Point Objective (how much data loss is tolerable) and Recovery Time Objective (how fast service must return)."),
 ("MTTR / MTBF","Mean Time To Repair and Mean Time Between Failures — the core availability metrics."),
 ("PKI / CA","Public Key Infrastructure; a Certificate Authority signs certificates to create a chain of trust."),
 ("AAA / RADIUS / TACACS+","Authentication, Authorization and Accounting; the two main AAA protocols for network access."),
 ("Screened subnet (DMZ)","A perimeter network between two firewalls that exposes public services without exposing the LAN."),
 ("Honeypot / honeynet","Deliberately vulnerable decoy hosts/networks deployed to detect and study attackers."),
 ("Evil twin","A rogue access point broadcasting a legitimate SSID to lure clients into connecting."),
 ("On-path attack","An attacker inserted between two parties (formerly man-in-the-middle), often via ARP spoofing."),
 ("MTU / PMTUD","Maximum Transmission Unit; Path MTU Discovery finds the smallest MTU along a route using ICMP."),
 ("Jitter","Variation in packet arrival time — the enemy of voice and video quality."),
]
B.append(("dl",gl))

# ---------------- render Markdown ----------------
def _anchor(txt):
    return "".join(ch.lower() if ch.isalnum() else ("-" if ch in " -" else "") for ch in txt)

def render_md():
    out=[f"# {C.TITLE} — Learner Guide",""]
    out.append(f"**WSQ Course Code:** {C.COURSE_CODE}  |  **Conducted by:** {C.ORG} ({C.UEN.replace('UEN: ','UEN ')})  |  **Version {C.VERSION} · {C.VERSION_DATE}**")
    out.append("")
    out.append("## Contents"); out.append("")
    for kind,*rest in B:
        if kind=="h1": out.append(f"- [{rest[0]}](#{_anchor(rest[0])})")
        elif kind=="h2": out.append(f"  - [{rest[0]}](#{_anchor(rest[0])})")
    out.append("")
    for kind,*rest in B:
        if kind=="h1": out+=["",f"## {rest[0]}",""]
        elif kind=="h2": out+=["",f"### {rest[0]}",""]
        elif kind=="h3": out+=[f"**{rest[0]}**",""]
        elif kind=="p": out+=[rest[0],""]
        elif kind=="bullets": out+=[f"- {x}" for x in rest[0]]+[""]
        elif kind=="steps":
            for i,(instr,cmd) in enumerate(rest[0],1):
                out.append(f"{i}. {instr}")
                if cmd: out+=["","   ```bash",f"   {cmd}","   ```",""]
            out.append("")
        elif kind=="code": out+=["```bash",rest[0],"```",""]
        elif kind=="note": out+=[f"> **Note:** {rest[0]}",""]
        elif kind=="rule": out+=["---",""]
        elif kind=="figure":
            rel=os.path.relpath(rest[0],REPO)
            out+=[f"![{rest[1]}]({rel})","",f"*{rest[1]}*",""]
        elif kind=="dl":
            for term,defn in rest[0]: out.append(f"- **{term}** — {defn}")
            out.append("")
    return "\n".join(out)

MD_OUT=os.path.join(REPO,f"LG-{C.SHORT_TITLE}.md")
with open(MD_OUT,"w") as f: f.write(render_md())
print("Saved",MD_OUT)

# ---------------- render DOCX ----------------
BRAND=RGBColor(0x1F,0x6F,0xEB); INKCODE=RGBColor(0x0B,0x30,0x60)
doc=Document()
normal=doc.styles["Normal"]; normal.font.name="Arial"; normal.font.size=Pt(11)
prodoc.style_headings(doc)
prodoc.add_cover_page(doc,"LEARNER GUIDE",C.TITLE,C.VERSION.lstrip("v"),
                      org_logo=os.path.join(ASSETS,"tertiary-infotech-logo.png"),
                      course_logo=os.path.join(ASSETS,"comptia-network-badge.png"),
                      course_code=C.COURSE_CODE)
prodoc.add_version_control(doc,[
 ("1.0","2 July 2026","Initial release — CompTIA Network+ (N10-009) Learner Guide covering all 36 labs.",C.TRAINER),
 (C.VERSION.lstrip("v"),C.VERSION_DATE,
  "Regenerated from the single-source pipeline: per-lab folders, per-lab troubleshooting tables, TIS "
  "web ed-tools (IP Calculator, PCAP Analyzer, Cybersecurity Simulator, Regex Generator) woven into "
  "the labs, and new Exam Focus quick references (ports, subnetting, methodology).",C.TRAINER),
])
prodoc.add_toc(doc)

def code_para(text):
    for line in text.split("\n"):
        para=doc.add_paragraph()
        r=para.add_run(line); r.font.name="Consolas"; r.font.size=Pt(9.5); r.font.color.rgb=INKCODE

for kind,*rest in B:
    if kind=="h1": doc.add_heading(rest[0],level=1)
    elif kind=="h2": doc.add_heading(rest[0],level=2)
    elif kind=="h3":
        para=doc.add_paragraph(); r=para.add_run(rest[0]); r.bold=True; r.font.size=Pt(11); r.font.color.rgb=BRAND
    elif kind=="p": doc.add_paragraph(rest[0])
    elif kind=="bullets":
        for x in rest[0]: doc.add_paragraph(x,style="List Bullet")
    elif kind=="steps":
        # Numbered manually so each lab's procedure restarts at 1. Word's List Number
        # style shares one counter across the whole document, which would run 1..260.
        for i,(instr,cmd) in enumerate(rest[0],1):
            para=doc.add_paragraph()
            para.paragraph_format.left_indent=Pt(18)
            para.paragraph_format.first_line_indent=Pt(-18)
            para.paragraph_format.space_after=Pt(3)
            r=para.add_run("%d.  "%i); r.bold=True; r.font.color.rgb=BRAND
            para.add_run(instr)
            if cmd: code_para(cmd)
    elif kind=="code": code_para(rest[0])
    elif kind=="note":
        para=doc.add_paragraph(); r=para.add_run("Note: "); r.bold=True; r.font.color.rgb=BRAND
        para.add_run(rest[0]).font.size=Pt(10)
    elif kind=="rule": doc.add_paragraph("")
    elif kind=="figure":
        try:
            para=doc.add_paragraph(); para.alignment=WD_ALIGN_PARAGRAPH.CENTER
            para.add_run().add_picture(rest[0], width=Inches(6.0))
            cap=doc.add_paragraph(); cap.alignment=WD_ALIGN_PARAGRAPH.CENTER
            cr=cap.add_run(rest[1]); cr.italic=True; cr.font.size=Pt(9)
            cr.font.color.rgb=RGBColor(0x55,0x5B,0x66)
        except Exception as e:
            print("  ! figure skipped:", rest[0], e)
    elif kind=="dl":
        for term,defn in rest[0]:
            para=doc.add_paragraph(style="List Bullet")
            r=para.add_run(term+" — "); r.bold=True; para.add_run(defn)

prodoc.add_page_numbers(doc)
prodoc.enable_update_fields(doc)
DOCX_OUT=os.path.join(REPO,"courseware",f"LG-{C.SHORT_TITLE}.docx")
doc.save(DOCX_OUT)
print("Saved",DOCX_OUT)
