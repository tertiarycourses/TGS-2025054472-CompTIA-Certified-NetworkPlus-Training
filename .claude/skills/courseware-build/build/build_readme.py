#!/usr/bin/env python3
"""Generate the course landing-page README.md from the single source."""
import os, sys, glob
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3; from data_domain4 import DOMAIN4
from data_domain5 import DOMAIN5
ACT=DOMAIN1+DOMAIN2+DOMAIN3+DOMAIN4+DOMAIN5
def _find_repo(start):
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE)

def folder(num):
    for h in sorted(glob.glob(os.path.join(REPO,"labs","lab-%02d-*"%num))):
        if os.path.isdir(h): return os.path.basename(h)
    return "lab-%02d"%num

REG=C.REGISTER_URL
B="https://img.shields.io/badge"
o=[]
o.append('<div align="center">')
o.append("")
o.append("# 🌐 CompTIA Certified Network+ Training (N10-009)")
o.append("")
o.append("**Design, implement, operate, secure and troubleshoot modern networks — and get exam-ready for CompTIA Network+ N10-009.**")
o.append("")
o.append(f"[![Register]({B}/Register-Enrol%20Now-1F6FEB?style=for-the-badge)]({REG}) "
         f"[![WSQ Funded]({B}/WSQ-SkillsFuture%20Funded-10B981?style=for-the-badge)]({REG})")
o.append("")
o.append(f"![Course Code]({B}/Course%20Code-{C.COURSE_CODE.replace(chr(45), chr(45)*2)}-555) "
         f"![Duration]({B}/Duration-5%20Days%20·%2040%20Hours-1F6FEB) "
         f"![Level]({B}/Level-Beginner%20to%20Intermediate-7C3AED) "
         f"![Labs]({B}/Hands--On%20Labs-36-10B981) "
         f"![Exam]({B}/Exam-N10--009-F59E0B) "
         f"![Assessment]({B}/Assessment-WA%20%2B%20PP-555)")
o.append("")
o.append(f"### 📝 [Register for this course →]({REG})")
o.append("")
o.append("</div>")
o.append("")
o.append("---")
o.append("")
o.append("## About This Course")
o.append("")
o.append("This WSQ course takes you from networking fundamentals to confident hands-on practice across all "
         "**five official CompTIA Network+ (N10-009) exam domains**. You will build, break and fix real networks "
         "in a browser-based Linux environment — subnetting, routing, VLANs, wireless, monitoring, security "
         "and structured troubleshooting.")
o.append("")
o.append("It suits IT support staff, system administrators, helpdesk engineers and career switchers who want a "
         "recognised networking foundation. No prior certification is required. Every one of the **36 labs** runs "
         "free in the browser — nothing to install on your own machine.")
o.append("")
o.append(f"> **Conducted by [{C.ORG}](https://www.tertiarycourses.com.sg/)** · {C.UEN}")
o.append("")
o.append("## Learning Outcomes")
o.append("")
o.append("| # | On completion, learners will be able to |")
o.append("|---|---|")
for lo in C.LEARNING_OUTCOMES:
    code, rest = lo.split(":", 1)
    o.append(f"| **{code.strip()}** | {rest.strip()} |")
o.append("")
o.append("## Course Topics & Labs")
o.append("")
o.append("The course follows the five N10-009 exam domains and their official weightings. "
         "**Each lab lives in its own folder** with a README carrying the full step-by-step commands.")
o.append("")
o.append("| Domain | Exam weighting | Labs |")
o.append("|---|---|---|")
for t in C.TOPICS:
    acts=[a for a in ACT if a["topic"]==t["num"]]
    o.append(f"| **{t['code']} — {t['title']}** | {t['weighting']} | Labs {acts[0]['num']}–{acts[-1]['num']} |")
o.append("")
for t in C.TOPICS:
    acts=[a for a in ACT if a["topic"]==t["num"]]
    o.append(f"<details>\n<summary><b>Domain {t['code']} — {t['title']} ({t['weighting']})</b> · {len(acts)} labs</summary>\n")
    o.append("| # | Lab | Tools |")
    o.append("|---|-----|-------|")
    for a in acts:
        o.append(f"| {a['num']} | [{a['title']}](labs/{folder(a['num'])}/README.md) | {a['services']} |")
    o.append("\n</details>\n")
o.append("## Tools")
o.append("")
o.append("Everything is **free and browser-based** — no installation on your own machine.")
o.append("")
o.append("| Tool | Purpose |")
o.append("|---|---|")
o.append(f"| [Killercoda Ubuntu Playground]({C.TOOLS['killercoda']}) | Disposable Ubuntu VM in your browser — every Linux lab runs here |")
o.append(f"| [TIS IP Calculator]({C.TOOLS['ipcalc']}) | CIDR / VLSM subnet planning and verification |")
o.append(f"| [TIS PCAP Analyzer]({C.TOOLS['pcap']}) | Dissect packet captures layer by layer |")
o.append(f"| [TIS Cybersecurity Simulator]({C.TOOLS['cybersim']}) | Practise recognising network attacks safely |")
o.append(f"| [TIS Regex Generator]({C.TOOLS['regex']}) | Build regular expressions for log filtering |")
o.append("")
o.append("Command-line tools used inside the playground (installed with `apt`): `tcpdump`, `tshark`, `nmap`, "
         "`dig`, `ip`, `iptables`, `iperf3`, `snmpd`, `nfdump`, `rsyslog`, `chrony`, `bind9`, `isc-dhcp-server`, "
         "`suricata`, `wireguard`, `openssl`, `nginx`, `ethtool`, `mtr`, `traceroute`.")
o.append("")
o.append("## Repository Structure")
o.append("")
o.append("```")
o.append("├── courseware/                 # Slide deck, Lesson Plan, Learner Guide (+ PDFs)")
o.append(f"│   ├── {C.SHORT_TITLE}-{C.VERSION}.pptx / .pdf")
o.append(f"│   ├── LP-{C.SHORT_TITLE}.docx / .pdf")
o.append(f"│   ├── LG-{C.SHORT_TITLE}.docx / .pdf")
o.append("│   └── archive/                # Superseded versions")
o.append("├── labs/                       # 36 hands-on labs, one folder each")
o.append("│   ├── README.md               # Lab index by exam domain")
o.append("│   ├── lab-01-osi-packet-inspection/README.md")
o.append("│   └── ...")
o.append(f"├── LG-{C.SHORT_TITLE}.md       # Learner Guide (Markdown mirror)")
o.append("└── README.md")
o.append("```")
o.append("")
o.append("> **Note:** the confidential WSQ **assessment** materials (Written Assessment, Practical Performance "
         "and their answer keys) are intentionally **not** published to this repository.")
o.append("")
o.append("## Course Details")
o.append("")
o.append("| | |")
o.append("|---|---|")
o.append(f"| **Course Title** | {C.TITLE} |")
o.append(f"| **WSQ Course Reference** | {C.COURSE_CODE} |")
o.append(f"| **Duration** | {C.DAYS} days · 8 training hours per day (40 hours) |")
o.append("| **Daily Timing** | 9:30 am – 6:30 pm (1-hour lunch; tea breaks within training time) |")
o.append("| **Mode** | Instructor-led, hands-on labs |")
o.append("| **Assessment** | Written Assessment (SAQ, 1 hr) + Practical Performance (PP, 90 min) — both open book |")
o.append(f"| **Certification target** | CompTIA Network+ {C.EXAM_CODE} (Pearson VUE) |")
o.append(f"| **Trainer** | {C.TRAINER} |")
o.append(f"| **Training Provider** | {C.ORG} ({C.UEN}) |")
o.append("")
o.append("### Funding")
o.append("")
o.append(f"This course is **WSQ / SkillsFuture funded**. A minimum **75% attendance** and a **Competent** "
         f"assessment outcome are required for funding eligibility. "
         f"See the [course page]({REG}) for current fees, subsidy levels and upcoming dates.")
o.append("")
o.append("## Exam Preparation")
o.append("")
o.append(f"Sharpen your readiness with the Tertiary Infotech practice exam: "
         f"**[CompTIA Network+ practice exam →]({C.PRACTICE_EXAM_URL})**")
o.append("")
o.append("## Building the Courseware")
o.append("")
o.append("All artifacts are generated from a single source (`course_data.py` + `data_domain1..5.py`), so the deck, "
         "Lesson Plan, Learner Guide and lab index can never drift apart.")
o.append("")
o.append("```bash")
o.append("# everything: PPT + LP + LG (DOCX + PDF, with page-numbered TOCs)")
o.append("bash .claude/skills/courseware-build/build/build_courseware.sh")
o.append("")
o.append("# or individually")
o.append("python3 .claude/skills/courseware-build/build/build_slides.py")
o.append("python3 .claude/skills/courseware-build/build/build_lesson_plan.py")
o.append("python3 .claude/skills/courseware-build/build/build_learner_guide.py")
o.append("python3 .claude/skills/courseware-build/build/build_labs_index.py")
o.append("```")
o.append("")
o.append("## Contact")
o.append("")
o.append(f"- 🌐 **Course page:** {REG}")
o.append("- ✉️ **Email:** enquiry@tertiaryinfotech.com")
o.append("- ☎️ **Tel:** +65 6100 0613")
o.append("- 🎓 **LMS / TMS:** https://lms-tms.tertiaryinfotech.com")
o.append("")
o.append("---")
o.append("")
o.append('<div align="center">')
o.append("")
o.append("### Ready to build your networking career?")
o.append("")
o.append(f"[![Register Now]({B}/Register%20Now-Enrol%20for%20this%20course-1F6FEB?style=for-the-badge)]({REG})")
o.append("")
o.append(f"© 2026 {C.ORG} · {C.UEN.replace('UEN: ','UEN ')}")
o.append("")
o.append("</div>")
o.append("")
open(os.path.join(REPO,"README.md"),"w").write("\n".join(o))
print("Saved README.md")
