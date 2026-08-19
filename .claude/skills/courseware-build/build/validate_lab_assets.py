#!/usr/bin/env python3
"""Validate the asset files shipped inside each labs/lab-NN-*/ folder.

Checks, for every lab folder:
  - every .sh parses (bash -n) and is executable
  - every .sh starts with a shebang and a set -e/-u line
  - every CSV parses AND has a uniform column count (catches unquoted commas)
  - every shipped file is referenced by that lab's README
  - checklist.md exists and uses task-list syntax
  - no private key material is committed
"""
import csv, glob, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
def find_repo(d):
    for _ in range(8):
        d = os.path.dirname(d)
        if os.path.isdir(os.path.join(d, "courseware")) and os.path.isdir(os.path.join(d, "labs")):
            return d
    return os.getcwd()
REPO = find_repo(HERE)

KEY_RE = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
errs, warns, stats = [], [], {"labs": 0, "sh": 0, "csv": 0, "cfg": 0, "checklist": 0}

for folder in sorted(glob.glob(os.path.join(REPO, "labs", "lab-*"))):
    if not os.path.isdir(folder):
        continue
    name = os.path.basename(folder)
    stats["labs"] += 1
    readme_p = os.path.join(folder, "README.md")
    if not os.path.isfile(readme_p):
        errs.append(f"{name}: no README.md")
        continue
    readme = open(readme_p, encoding="utf-8").read()

    files = []
    for p in sorted(glob.glob(os.path.join(folder, "*"))):
        if os.path.isfile(p) and os.path.basename(p) != "README.md":
            files.append(p)
    for p in sorted(glob.glob(os.path.join(folder, "*", "*"))):
        if os.path.isfile(p):
            files.append(p)

    has_checklist = False
    for p in files:
        rel = os.path.relpath(p, folder)
        base = os.path.basename(p)

        # every shipped file must be referenced by the README
        if base not in readme and rel not in readme:
            errs.append(f"{name}: {rel} is not referenced by README.md")

        body = open(p, encoding="utf-8", errors="replace").read()
        if KEY_RE.search(body):
            errs.append(f"{name}: {rel} contains PRIVATE KEY material")

        if base.endswith(".sh"):
            stats["sh"] += 1
            r = subprocess.run(["bash", "-n", p], capture_output=True, text=True)
            if r.returncode != 0:
                errs.append(f"{name}: {rel} bash -n failed: {r.stderr.strip()[:120]}")
            if not os.access(p, os.X_OK):
                errs.append(f"{name}: {rel} is not executable (chmod +x)")
            if not body.startswith("#!"):
                errs.append(f"{name}: {rel} has no shebang")
            # the safety line follows the header comment, which can be long —
            # scan the whole preamble (everything before the first real command)
            preamble = "\n".join(body.split("\n")[:40])
            if not re.search(r"^set -[euxo]", preamble, re.M):
                warns.append(f"{name}: {rel} has no 'set -' safety line")

        elif base.endswith(".csv"):
            stats["csv"] += 1
            try:
                rows = list(csv.reader(open(p, encoding="utf-8")))
            except Exception as e:
                errs.append(f"{name}: {rel} does not parse as CSV: {e}")
                continue
            rows = [r for r in rows if r]
            if len(rows) < 9:
                warns.append(f"{name}: {rel} has {len(rows)-1} data rows (spec wants 8+)")
            widths = {len(r) for r in rows}
            if len(widths) > 1:
                errs.append(f"{name}: {rel} has ragged columns {sorted(widths)} "
                            f"— likely an unquoted comma")

        elif base == "checklist.md":
            has_checklist = True
            stats["checklist"] += 1
            if "- [ ]" not in body:
                errs.append(f"{name}: checklist.md has no '- [ ]' task items")
        else:
            stats["cfg"] += 1

    if not has_checklist:
        warns.append(f"{name}: no checklist.md")

print("labs=%(labs)d  scripts=%(sh)d  csv=%(csv)d  configs=%(cfg)d  checklists=%(checklist)d" % stats)
for w in warns:
    print("WARN:", w)
if errs:
    for e in errs:
        print("ERROR:", e)
    sys.exit(1)
print("OK")
