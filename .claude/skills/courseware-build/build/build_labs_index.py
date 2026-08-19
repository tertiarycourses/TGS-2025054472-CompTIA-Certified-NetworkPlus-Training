#!/usr/bin/env python3
"""Regenerate labs/README.md (the lab index) from the single source, with
per-lab folder links, so it stays aligned with the deck, LP and LG."""
import os, sys, glob
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3; from data_domain4 import DOMAIN4
from data_domain5 import DOMAIN5
ACT=DOMAIN1+DOMAIN2+DOMAIN3+DOMAIN4+DOMAIN5
def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE)

def folder(num):
    hits=sorted(glob.glob(os.path.join(REPO,"labs","lab-%02d-*"%num)))
    for h in hits:
        if os.path.isdir(h): return os.path.basename(h)
    return "lab-%02d"%num

out=[f"# {C.TITLE} — Lab Index","",
 f"All 36 hands-on labs for the WSQ course **{C.TITLE}** ({C.COURSE_CODE}), organised by the five official N10-009 exam domains. Each lab lives in its own folder with a README containing the full step-by-step commands.","",
 "## Lab environment (all free, browser-based)","",
 f"- **Killercoda Ubuntu Playground** (every Linux lab): {C.TOOLS['killercoda']}",
 f"- **TIS IP Calculator** (subnetting): {C.TOOLS['ipcalc']}",
 f"- **TIS PCAP Analyzer** (packet captures): {C.TOOLS['pcap']}",
 f"- **TIS Cybersecurity Simulator** (attack recognition): {C.TOOLS['cybersim']}",
 f"- **TIS Regex Generator** (log filtering): {C.TOOLS['regex']}","",
 "No installs are needed on your own machine — packages are pulled with `apt` inside the throw-away VM. Lab 11 (Wireless) optionally uses your own laptop's Wi-Fi radio.","",
 "See [tools.md](tools.md) for every free tool used, with install commands.",""]
for t in C.TOPICS:
    out.append(f"## Domain {t['code']} — {t['title']}  ({t['weighting']})")
    out.append("")
    out.append("| # | Lab | Tools |")
    out.append("|---|-----|-------|")
    for a in [x for x in ACT if x["topic"]==t["num"]]:
        f=folder(a["num"])
        out.append(f"| {a['num']} | [{a['title']}]({f}/README.md) | {a['services']} |")
    out.append("")
out+=["---","",
 f"© 2026 {C.ORG} ({C.UEN}). Course registration: {C.REGISTER_URL}",""]
open(os.path.join(REPO,"labs","README.md"),"w").write("\n".join(out))
print("Saved labs/README.md")
