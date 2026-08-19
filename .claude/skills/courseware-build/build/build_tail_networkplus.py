# ============================================================ BUILD (Network+ N10-009)
# Teaching content is driven by CONTENT1..CONTENT5 spec lists (see CONTENT_SPEC.md).
# Labs render as overview + process map + verify — the step-by-step detail lives in
# the Learner Guide, not the deck.
from data_domain1 import CONTENT1
from data_domain2 import CONTENT2
from data_domain3 import CONTENT3
from data_domain4 import CONTENT4
from data_domain5 import CONTENT5
CONTENT = {1: CONTENT1, 2: CONTENT2, 3: CONTENT3, 4: CONTENT4, 5: CONTENT5}
ACT_BY_NUM = {a["num"]: a for a in ACTIVITIES}

CMAP = {"blue": BLUE, "teal": TEAL, "violet": VIOLET, "amber": AMBER, "grey": GREY}
def _c(name, default=BLUE):
    if isinstance(name, str):
        return CMAP.get(name.lower(), default)
    return name or default

SLIDE_INDEX = {"labs": {}, "domains": {}, "admin": {}}
def _now():
    return len(prs.slides._sldIdLst)

def _mark(kind, key):
    SLIDE_INDEX[kind][str(key)] = _now()

# ---------------- spec renderer ----------------
def _norm_items(items):
    out = []
    for it in items:
        if isinstance(it, (list, tuple)):
            out.append((str(it[0]), str(it[1])))
        else:
            out.append(str(it))
    return out

def render_spec(sp, t):
    ty = sp["type"]
    kk = sp.get("kicker")
    if ty == "tiles":
        tile_grid(sp["title"], _norm_items(sp["items"]), kicker=kk,
                  cols=sp.get("cols", 2), size=sp.get("size", 14),
                  icons=sp.get("icons"), accent=_c(sp.get("accent"), BLUE))
    elif ty == "cards":
        cards = [(_c(c[0]), c[1], list(c[2])) for c in sp["cards"][:3]]
        cards3(sp["title"], cards, kicker=kk)
    elif ty == "two_col":
        two_col(sp["title"], sp["left"], sp["right"], kicker=kk,
                lhead=sp.get("lhead", ""), rhead=sp.get("rhead", ""))
    elif ty == "flow":
        flow_h(sp["title"], sp["steps"][:6], kicker=kk, color=_c(sp.get("color"), BLUE))
    elif ty == "process":
        stages = [(st if isinstance(st, tuple) else (st, "")) for st in sp["stages"][:6]]
        process_map(sp["title"], stages, kicker=kk, color=_c(sp.get("color"), BLUE),
                    synthesis=tuple(sp["synthesis"]) if sp.get("synthesis") else None)
    elif ty == "decision":
        decision_map(sp["title"], sp["question"], tuple(sp["yes"]), tuple(sp["no"]),
                     kicker=kk, color=_c(sp.get("color"), VIOLET), note=sp.get("note"))
    elif ty == "table":
        compare_table(sp["title"], list(sp["headers"]), [list(r) for r in sp["rows"][:6]],
                      kicker=kk, accent=_c(sp.get("accent"), BLUE), note=sp.get("note"))
    elif ty == "worked":
        worked_example(sp["title"], sp["intro"], list(sp["code"])[:14],
                       [tuple(e) for e in sp["explain"]][:4], kicker=kk,
                       accent=_c(sp.get("accent"), TEAL))
    elif ty == "chart":
        chart_slide(sp["title"], list(sp["categories"]),
                    [(nm, list(vals)) for nm, vals in sp["series"]], kicker=kk,
                    accent=_c(sp.get("accent"), BLUE), kind=sp.get("kind", "column"),
                    insight=sp.get("insight"), number_format=sp.get("number_format", "0"))
    elif ty == "big":
        big_statement(sp["line1"], sp.get("line2", ""), sp.get("kicker", ""),
                      color=_c(sp.get("color"), BLUE))
    elif ty == "bullets":
        content(sp["title"], sp["items"], kicker=kk, size=sp.get("size", 18))
    elif ty == "lab":
        render_lab(ACT_BY_NUM[sp["num"]], t)
    else:
        raise ValueError("unknown spec type: %r" % ty)

def render_lab(a, t):
    _mark("labs", a["num"])
    activity_overview("LAB %d" % a["num"], a["title"], a["desc"], a["build"], a["services"],
                      kicker="DOMAIN %s · HANDS-ON" % t["code"],
                      objective=a.get("objective"), test=a.get("test"))
    stg = []
    for (stext, scmd) in a["steps"][:6]:
        lbl = stext.split(",")[0].split(" and ")[0].split(" (")[0].strip()
        cap = scmd.split("\n")[0].strip() if scmd else ""
        stg.append((_ellipsis(lbl, 40), _short_cmd(cap, 26) if cap else ""))
    if len(stg) >= 3:
        process_map("How Lab %d Runs" % a["num"], stg,
                    kicker="LAB %d · PROCESS MAP" % a["num"], color=TEAL,
                    synthesis=("THE POINT", a["objective"]))
    test_slide(a["title"], a["test"], kicker="LAB %d · VERIFY" % a["num"],
               troubleshoot=a.get("troubleshoot"))

# ---------------- COVER + ADMIN ----------------
cover()
_mark("admin", "cover")
section("COURSE ADMINISTRATION", "Welcome & Housekeeping", "")
tile_grid("Digital Attendance (Mandatory)", [
 ("Three times a day", "Take the AM, PM and Assessment digital attendance — mandatory for every WSQ-funded course."),
 ("Trainer shows the QR", "The trainer or administrator displays the digital attendance QR code from the SSG portal."),
 ("Scan and submit", "Scan the QR code with your mobile phone camera and submit your attendance."),
 ("75% minimum", "A minimum of 75% attendance is required to be eligible for assessment and funding.")],
 kicker="TRAQOM · SSG DIGITAL ATTENDANCE", cols=2, size=15)
trainer_slide("YOUR TRAINER · GENERAL", "Your Trainer",
 "General Trainer template —\nto be completed by the trainer",
 [("Name", ""), ("Title / Designation", ""), ("Qualifications", ""),
  ("Areas of expertise", ""), ("Training & industry experience", ""), ("Contact", "")],
 initials="?", accent=GREY)
trainer_slide("YOUR TRAINER", C.TRAINER, "Principal Trainer\nTertiary Infotech Academy Pte Ltd",
 [("Role", "Principal Trainer, Tertiary Infotech Academy Pte Ltd"),
  ("Expertise", "Networking, cybersecurity, cloud infrastructure, data science and AI — 20+ years of training and consulting."),
  ("Delivers", "WSQ courses on CompTIA Network+, Security+, Linux+, cloud computing and applied AI."),
  ("Founder", "Founder and lead instructor at Tertiary Infotech / Tertiary Courses.")],
 initials="AA", accent=BLUE)
content("Let's Know Each Other", [
 "Your name, organisation and role.",
 "Your experience with networking, Linux or IT support (if any).",
 "What network you manage or plan to build after this course."], kicker="ICE-BREAKER")
tile_grid("Ground Rules", [
 "Set your mobile phone to silent mode.", "Participate actively — no question is too small.",
 "Mutual respect: agree to disagree.", "One conversation at a time.",
 "Be punctual; return from breaks on time.", "75% attendance is required."],
 kicker="HOUSEKEEPING", cols=2, size=15)
_mark("admin", "download")
tile_grid("Download Your Course Material", [
 ("1 · Go to the LMS portal", "Open https://lms-tms.tertiaryinfotech.com in your browser."),
 ("2 · Log in", "Sign in with the account e-mail you used to register for this course."),
 ("3 · Open this course", "Select 'CompTIA Certified Network+ Training' in My Courses."),
 ("4 · Download", "Download the Learner Slides, Learner Guide and Lesson Plan (PDF)."),
 ("5 · Get the labs", "Open the lab repository on GitHub — the link is on the course page."),
 ("6 · Keep them open", "You may use these materials during the open-book assessment.")],
 kicker="LMS / TMS  ·  lms-tms.tertiaryinfotech.com", cols=2, size=14)
tile_grid("Lesson Plan — 5 Days · 8 Hours a Day", [
 ("Day 1 · " + C.DAY_THEMES[1], "OSI model, appliances, cloud, ports & protocols, media, topologies, IPv4/IPv6 · Labs 1–7."),
 ("Day 2 · " + C.DAY_THEMES[2], "Routing, NAT/PAT, VLANs & trunking, STP, link aggregation, wireless, installations · Labs 8–14."),
 ("Day 3 · " + C.DAY_THEMES[3], "Documentation, change & configuration management, monitoring, DR, network services · Labs 15–20."),
 ("Day 4 · " + C.DAY_THEMES[4], "Encryption & PKI, IAM/AAA, segmentation, attacks and defence features · Labs 21–27."),
 ("Day 5 · " + C.DAY_THEMES[5], "Seven-step methodology, layer-by-layer diagnosis, performance · Labs 28–36 · Final Assessment (WA + PP).")],
 kicker="SCHEDULE  ·  9:00 AM – 6:00 PM DAILY", cols=1, size=13)
tile_grid("Learning Outcomes", [
 ("LO1 · Explain networking concepts", "OSI model, appliances, cloud, ports & protocols, traffic types, media, topologies and IP addressing."),
 ("LO2 · Implement networks", "Routing (BGP/EIGRP/OSPF), NAT/PAT, VLANs, STP, link aggregation, wireless and installations."),
 ("LO3 · Operate networks", "Documentation, IPAM, change management, SNMP/flow/log monitoring, DR and network services."),
 ("LO4 · Secure networks", "Encryption, PKI, IAM, AAA, segmentation, attack recognition and defence features."),
 ("LO5 · Troubleshoot networks", "The CompTIA methodology applied with the right tool at every layer.")],
 kicker="WHAT YOU'LL ACHIEVE", cols=1, size=13)
tile_grid("Course Outline — the Five N10-009 Domains", [
 ("Domain 1.0 · Networking Concepts · 23%", "OSI, appliances, cloud, ports & protocols, traffic, media, topologies, IPv4 · Labs 1–7."),
 ("Domain 2.0 · Network Implementation · 20%", "Routing, switching, wireless and physical installations · Labs 8–14."),
 ("Domain 3.0 · Network Operations · 19%", "Documentation, life-cycle, change, monitoring, DR, services, access · Labs 15–20."),
 ("Domain 4.0 · Network Security · 14%", "Logical/physical security, attacks, segmentation and defence · Labs 21–27."),
 ("Domain 5.0 · Network Troubleshooting · 24%", "Methodology, cabling, services, performance, tools · Labs 28–36.")],
 kicker="FIVE DOMAINS · 36 HANDS-ON LABS", cols=1, size=13)
chart_slide("N10-009 Exam Weighting by Domain",
 [t["title"] for t in C.TOPICS],
 [("Exam weighting (%)", [int(t["weighting"].replace("%", "")) for t in C.TOPICS])],
 kicker="KNOW THE BLUEPRINT", accent=BLUE, kind="bar",
 insight="Troubleshooting (24%) and Networking Concepts (23%) carry almost half the exam — "
         "the course spends Day 1 and Day 5 on them and every lab ends with a verify step.",
 number_format='0"%"')
tile_grid("About the CompTIA Network+ Exam (N10-009)", [
 ("Format", "Maximum of 90 questions — multiple-choice and performance-based — in 90 minutes."),
 ("Passing score", "720 on a 100–900 scale. Book at Pearson VUE test centres or online proctoring."),
 ("No prerequisites", "CompTIA recommends A+ and 9–12 months of networking experience, but neither is required."),
 ("Renewal", "The certification is valid for 3 years and renews through CompTIA CE credits.")],
 kicker="THE CERTIFICATION TARGET", cols=2, size=14)
tile_grid("Your Lab Environment", [
 ("Killercoda Ubuntu Playground", "A free, throwaway Ubuntu VM in your browser — every Linux lab runs here. " + C.TOOLS["killercoda"]),
 ("TIS IP Calculator", "Web subnetting tool for CIDR/VLSM planning and verification. " + C.TOOLS["ipcalc"]),
 ("TIS PCAP Analyzer", "Upload and dissect packet captures layer by layer in the browser. " + C.TOOLS["pcap"]),
 ("TIS Cybersecurity Simulator", "Practise recognising network attacks in a safe simulated environment. " + C.TOOLS["cybersim"]),
 ("TIS Regex Generator", "Build the regular expressions used to search and filter log files. " + C.TOOLS["regex"]),
 ("No installs needed", "Everything is browser-based; packages are pulled with apt inside the playground VM.")],
 kicker="FREE TOOLS USED THROUGHOUT", cols=2, size=13, accent=TEAL)
_mark("admin", "briefing")
tile_grid("Briefing for Assessment", [
 ("Do · Clear your desk", "Place phones and other materials under the table or on the floor."),
 ("Don't · No recording", "No photos or recording of assessment scripts."),
 ("Don't · No discussion", "Work individually — no discussion during the assessment."),
 ("Do · Black or blue pen", "Use a black or blue pen for hard-copy assessments."),
 ("Don't · No correction fluid", "No liquid paper or correction tape may be used."),
 ("Do · Stop on time", "Scripts are collected when time is up.")],
 kicker="BEFORE YOU START", cols=2, size=14, accent=AMBER)
tile_grid("Assessment", [
 ("Written Assessment (WA)", "Short-Answer Questions (SAQ) · 1 hour · open book. Tests the underpinning networking knowledge."),
 ("Practical Performance (PP)", "Hands-on networking tasks · 1 hour · open book. Tests the ability you built in the 36 labs."),
 ("Open book", "You may use the course slides, the Learner Guide and approved materials only."),
 ("Eligibility", "A minimum of 75% attendance is required to be eligible for assessment and funding."),
 ("Result", "You are assessed as Competent (C) or Not Yet Competent (NYC) on each instrument."),
 ("Appeals", "An appeal process is available if you wish to contest an assessment outcome.")],
 kicker="FINAL ASSESSMENT · DAY 5", cols=2, size=14)
process_map("Assessment Flow", [
 ("TRAQOM survey", "Scan the QR on the LMS"),
 ("Digital attendance", "Scan the SSG QR"),
 ("Sit WA then PP", "Open book · 1 hr each"),
 ("Submit on the LMS", "Upload your answers"),
 ("Sign the record", "Assessment Summary")],
 kicker="ON ASSESSMENT DAY", color=BLUE,
 synthesis=("REMEMBER", "All five steps are mandatory for WSQ funding — missing the digital "
            "attendance or the TRAQOM survey can invalidate your claim."))
tile_grid("Criteria for Funding", [
 ("Attendance", "A minimum attendance rate of 75%, based on the SSG Digital Attendance record."),
 ("Assessment", "Complete both assessment components and be assessed as 'Competent'."),
 ("Digital attendance", "Scan the SSG QR code for AM, PM and Assessment on every training day."),
 ("TRAQOM survey", "Complete the mandatory TRAQOM course feedback survey on the LMS.")],
 kicker="WSQ FUNDING", cols=2, size=15, accent=AMBER)

# ---------------- DOMAINS ----------------
for t in C.TOPICS:
    _mark("domains", t["num"])
    section("DOMAIN %s  ·  %s OF THE EXAM" % (t["code"], t["weighting"]),
            t["title"], t["code"], t["subtitle"])
    acts0 = [a for a in ACTIVITIES if a["topic"] == t["num"]]
    third = (len(acts0) + 2) // 3
    groups = [acts0[i:i + third] for i in range(0, len(acts0), third)][:3]
    while len(groups) < 3:
        groups.append([])
    cards = []
    for gi, g in enumerate(groups):
        lbl = "—" if not g else ("Lab %d" % g[0]["num"] if g[0]["num"] == g[-1]["num"]
                                 else "Labs %d–%d" % (g[0]["num"], g[-1]["num"]))
        cards.append(([BLUE, TEAL, VIOLET][gi], lbl,
                      [a["title"] for a in g] if g else ["—"]))
    cards3("Hands-On Labs — %s" % t["title"], cards, kicker="WHAT YOU'LL DO")
    for sp in CONTENT[t["num"]]:
        render_spec(sp, t)
    acts = [a for a in ACTIVITIES if a["topic"] == t["num"]]
    content("Recap — %s" % t["title"],
            ["You can now: " + a["objective"] for a in {x["objective"]: x for x in acts}.values()][:7],
            kicker="DOMAIN %s RECAP" % t["code"], size=16)

# ---------------- CLOSE ----------------
section("WRAP-UP", "Course Summary & Next Steps", "")
tile_grid("What You Achieved", [
 ("LO1 · Explained networking concepts", "OSI layers, appliances, cloud models, ports & protocols, media, topologies and IPv4/IPv6 subnetting."),
 ("LO2 · Implemented networks", "Static & dynamic routing, NAT/PAT, 802.1Q VLANs, STP, bonding, wireless design and installations."),
 ("LO3 · Operated networks", "SNMP, NetFlow, syslog, NTP, DHCP/DNS services, configuration backup and disaster recovery."),
 ("LO4 · Secured networks", "Firewalls, ACLs, IDS, TLS/PKI, SSH hardening, VPNs, segmentation and attack recognition."),
 ("LO5 · Troubleshot networks", "The seven-step CompTIA methodology with the right diagnostic tool at every layer.")],
 kicker="LEARNING OUTCOMES", cols=1, size=13)
tile_grid("Preparing for the N10-009 Exam", [
 ("Redo the labs", "Repeat every lab from memory until the commands and workflow are automatic."),
 ("Master subnetting", "Drill CIDR/VLSM until a /26 split takes under a minute — use the TIS IP Calculator to self-check."),
 ("Memorise the ports", "FTP 20/21, SSH 22, Telnet 23, SMTP 25, DNS 53, DHCP 67/68, HTTP 80, HTTPS 443, SNMP 161/162, LDAP 389, RDP 3389, SIP 5060/5061."),
 ("Know the blueprint", "Revise by the five domains and their weightings — troubleshooting scenarios are the largest share."),
 ("Practice exams", "Attempt timed practice exams and review every wrong answer against the objectives."),
 ("Book the exam", "Schedule N10-009 at a Pearson VUE centre or online when practice scores pass 80%.")],
 kicker="NEXT STEPS", cols=2, size=13)
_mark("admin", "practice_exam")
tile_grid("Practice Exam — exams.tertiaryinfotech.com", [
 ("1 · Open the portal", "Go to " + C.PRACTICE_EXAM_URL),
 ("2 · Choose Network+", "Select the CompTIA Network+ practice exam that matches this course."),
 ("3 · Sit it timed", "Attempt the full paper under exam timing — 90 minutes, no notes."),
 ("4 · Review and repeat", "Review every explanation, revisit the weak domain's labs, then re-take it.")],
 kicker="TEST YOURSELF BEFORE THE REAL EXAM", cols=2, size=14, accent=VIOLET)
tile_grid("Recommended Courses", [(rc, "") for rc in C.RECOMMENDED_COURSES],
 kicker="CONTINUE WITH TERTIARY INFOTECH", cols=1, size=15)
content("Support", [
 "If you have any enquiries during or after the class, you can contact us below.",
 "Email: enquiry@tertiaryinfotech.com", "Tel: +65 6100 0613",
 "Website: www.tertiarycourses.com.sg", "LMS / TMS: https://lms-tms.tertiaryinfotech.com"],
 kicker="WE'RE HERE TO HELP")
tile_grid("Assessment", [
 ("Written Assessment (SAQ)", "1 hour · open book · short-answer knowledge questions."),
 ("Practical Performance (PP)", "1 hour · open book · hands-on networking tasks on the lab environment."),
 ("Digital attendance", "Remember to take the Assessment digital attendance (TRAQOM) before you start."),
 ("Submit on the LMS", "Upload your completed answers at https://lms-tms.tertiaryinfotech.com/")],
 kicker="WRAP-UP", cols=2, size=15)
process_map("Assessment Flow", [
 ("TRAQOM survey", "Scan the QR on the LMS"),
 ("Digital attendance", "Scan the SSG QR"),
 ("Sit WA then PP", "Open book · 1 hr each"),
 ("Submit on the LMS", "Upload your answers"),
 ("Sign the record", "Assessment Summary")],
 kicker="ON ASSESSMENT DAY", color=BLUE,
 synthesis=("REMEMBER", "All five steps are mandatory for WSQ funding — missing the digital "
            "attendance or the TRAQOM survey can invalidate your claim."))
tile_grid("Digital Attendance (Mandatory)", [
 ("Three times a day", "Take the AM, PM and Assessment digital attendance — mandatory for every WSQ-funded course."),
 ("Trainer shows the QR", "The trainer or administrator displays the digital attendance QR code from the SSG portal."),
 ("Scan and submit", "Scan the QR code with your mobile phone camera and submit your attendance."),
 ("75% minimum", "A minimum of 75% attendance is required to be eligible for assessment and funding.")],
 kicker="TRAQOM · SSG DIGITAL ATTENDANCE", cols=2, size=15)
big_statement("Thank You!",
 "You can now design, implement, operate, secure and troubleshoot modern networks — "
 "and you are ready for the CompTIA Network+ (N10-009) exam.",
 "HAPPY NETWORKING", color=TEAL)

# ---------------- restrained motion pass ----------------
for s in prs.slides:
    txts = [sh.text_frame.text for sh in s.shapes if sh.has_text_frame]
    joined = " ".join(txts)
    is_div = ("COURSE ADMINISTRATION" in joined) or ("WRAP-UP" in joined and "Course Summary" in joined) or \
             any(("DOMAIN %s" % t["code"]) in joined and t["title"] in joined and t["subtitle"][:20] in joined
                 for t in C.TOPICS)
    _transition(s, "push" if is_div else "fade", speed="med" if is_div else "fast")

import json
OUT = os.path.join(REPO, "courseware", "%s-%s.pptx" % (C.SHORT_TITLE, C.VERSION))
prs.save(OUT)
with open(os.path.join(HERE, "slide_index.json"), "w") as f:
    json.dump(SLIDE_INDEX, f, indent=1)
print("Saved %s  (%d slides)" % (OUT, len(prs.slides._sldIdLst)))
