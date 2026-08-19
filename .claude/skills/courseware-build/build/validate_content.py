#!/usr/bin/env python3
"""Validate a data_domainN.py content module against CONTENT_SPEC.md limits.
Usage: python3 validate_content.py <N> <first_lab> <last_lab> [min_specs]"""
import sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

N = int(sys.argv[1]); LO = int(sys.argv[2]); HI = int(sys.argv[3])
MIN = int(sys.argv[4]) if len(sys.argv) > 4 else 50
m = importlib.import_module("data_domain%d" % N)
DOM = getattr(m, "DOMAIN%d" % N); CON = getattr(m, "CONTENT%d" % N)
errs, warns = [], []

def err(s): errs.append(s)
def warn(s): warns.append(s)

# ---- labs
nums = [a["num"] for a in DOM]
if nums != list(range(LO, HI + 1)):
    err("DOMAIN%d lab nums %r != %r" % (N, nums, list(range(LO, HI + 1))))
for a in DOM:
    ctx = "lab %s" % a.get("num")
    for k in ("num", "topic", "title", "objective", "desc", "build", "services", "steps", "test"):
        if k not in a: err("%s missing key %s" % (ctx, k))
    if a.get("topic") != N: err("%s topic %r != %d" % (ctx, a.get("topic"), N))
    if len(a.get("objective", "")) > 110: err("%s objective >110 chars" % ctx)
    if len(a.get("desc", "")) > 220: err("%s desc >220 chars" % ctx)
    if len(a.get("build", "")) > 130: err("%s build >130 chars" % ctx)
    if len(a.get("services", "")) > 90: err("%s services >90 chars" % ctx)
    if len(a.get("test", "")) > 200: err("%s test >200 chars" % ctx)
    st = a.get("steps", [])
    if not (4 <= len(st) <= 10): err("%s has %d steps (want 5-10)" % (ctx, len(st)))
    for i, s in enumerate(st):
        if not (isinstance(s, tuple) and len(s) == 2): err("%s step %d not a 2-tuple" % (ctx, i+1)); continue
        if len(s[0]) > 90: err("%s step %d instruction >90 chars" % (ctx, i+1))
        if s[1] and len(s[1].split("\n")[0]) > 96: err("%s step %d command line >96 chars" % (ctx, i+1))
    tb = a.get("troubleshoot")
    if tb is not None:
        if len(tb) != 3: err("%s troubleshoot needs exactly 3 pairs" % ctx)
        for sym, fix in tb:
            if len(sym) > 40: err("%s troubleshoot symptom >40: %r" % (ctx, sym))
            if len(fix) > 110: err("%s troubleshoot fix >110" % ctx)
    else:
        warn("%s has no troubleshoot list (generic fallback will be used)" % ctx)

# ---- content specs
lab_marks = [sp["num"] for sp in CON if sp.get("type") == "lab"]
if lab_marks != nums:
    err("lab markers %r != lab nums %r (each lab exactly once, ascending)" % (lab_marks, nums))
teach = [sp for sp in CON if sp.get("type") != "lab"]
if len(teach) < MIN: err("only %d teaching specs (want >= %d)" % (len(teach), MIN))
nbul = sum(1 for sp in teach if sp["type"] == "bullets")
if nbul > max(1, len(teach) // 10): warn("%d bullet slides — keep them sparse" % nbul)

def _len(s, lim, ctx):
    if len(str(s)) > lim: err("%s: %r… >%d chars" % (ctx, str(s)[:40], lim))

for i, sp in enumerate(CON):
    ty = sp.get("type"); ctx = "spec %d (%s / %r)" % (i, ty, str(sp.get("title", ""))[:30])
    if ty == "lab":
        continue
    if ty not in ("tiles","cards","two_col","flow","process","decision","table","worked","chart","big","bullets"):
        err("%s unknown type" % ctx); continue
    if ty not in ("big",) and not sp.get("title"): err("%s missing title" % ctx)
    if ty == "tiles":
        its = sp["items"]; cols = sp.get("cols", 2)
        if cols == 2 and not (4 <= len(its) <= 8): err("%s: %d items for cols=2 (want 4-8)" % (ctx, len(its)))
        if cols == 1 and not (3 <= len(its) <= 5): err("%s: %d items for cols=1 (want 3-5)" % (ctx, len(its)))
        for it in its:
            if isinstance(it, (tuple, list)):
                _len(it[0], 42, ctx + " head"); _len(it[1], 150, ctx + " caption")
            else: _len(it, 150, ctx)
    elif ty == "cards":
        if len(sp["cards"]) != 3: err("%s needs exactly 3 cards" % ctx)
        for c in sp["cards"]:
            if not (3 <= len(c[2]) <= 6): err("%s card %r wants 3-6 bullets" % (ctx, c[1]))
            for b in c[2]: _len(b, 60, ctx + " bullet")
    elif ty == "two_col":
        for side in ("left", "right"):
            xs = sp[side]
            if not (3 <= len(xs) <= 6): err("%s %s wants 3-6 items" % (ctx, side))
            for x in xs: _len(x[0] if isinstance(x, (tuple, list)) else x, 70, ctx)
    elif ty == "flow":
        if not (4 <= len(sp["steps"]) <= 6): err("%s wants 4-6 steps" % ctx)
        for st in sp["steps"]: _len(st, 55, ctx)
    elif ty == "process":
        if not (3 <= len(sp["stages"]) <= 6): err("%s wants 3-6 stages" % ctx)
        for st in sp["stages"]:
            lbl, cap = (st if isinstance(st, (tuple, list)) else (st, ""))
            _len(lbl, 40, ctx + " label"); _len(cap, 26, ctx + " caption")
        if sp.get("synthesis"): _len(sp["synthesis"][1], 160, ctx + " synthesis")
    elif ty == "decision":
        if sp["question"].count("\n") > 2: err("%s question >3 lines" % ctx)
        for br in ("yes", "no"): _len(sp[br][1], 140, ctx + " " + br)
    elif ty == "table":
        if not (3 <= len(sp["headers"]) <= 5): err("%s wants 3-5 columns" % ctx)
        if not (3 <= len(sp["rows"]) <= 6): err("%s wants 3-6 rows" % ctx)
        for r in sp["rows"]:
            if len(r) != len(sp["headers"]): err("%s row width mismatch" % ctx)
            for cell in r: _len(cell, 55, ctx + " cell")
    elif ty == "worked":
        if len(sp["code"]) > 14: err("%s >14 code lines" % ctx)
        for ln in sp["code"]: _len(ln, 62, ctx + " code")
        if not (2 <= len(sp["explain"]) <= 4): err("%s wants 2-4 explain tiles" % ctx)
        for lbl, body in sp["explain"]: _len(body, 95, ctx + " explain")
    elif ty == "chart":
        if len(sp["categories"]) < 2: err("%s wants >=2 categories" % ctx)
        for nm, vals in sp["series"]:
            if len(vals) != len(sp["categories"]): err("%s series length mismatch" % ctx)
    elif ty == "big":
        _len(sp["line1"], 70, ctx); _len(sp.get("line2", ""), 180, ctx)
    elif ty == "bullets":
        if not (3 <= len(sp["items"]) <= 7): err("%s wants 3-7 bullets" % ctx)
        for b in sp["items"]: _len(b, 130, ctx)

print("DOMAIN%d: %d labs, %d teaching specs, %d lab markers" % (N, len(DOM), len(teach), len(lab_marks)))
for w in warns: print("WARN:", w)
if errs:
    for e in errs: print("ERROR:", e)
    sys.exit(1)
print("OK")
