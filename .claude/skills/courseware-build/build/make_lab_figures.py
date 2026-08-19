#!/usr/bin/env python3
"""Render each lab's 'How Lab N Runs' process-map slide from the deck PDF into
courseware/assets/figures/lab-NN-process.png, for embedding in the Learner Guide.

The process map is the slide immediately after each lab's overview slide, whose
page number is recorded in slide_index.json by build_slides.py.
"""
import os, sys, json, subprocess, glob
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
def _find_repo(start):
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE)

PDF=os.path.join(REPO,"courseware","%s-%s.pdf"%(C.SHORT_TITLE,C.VERSION))
OUT=os.path.join(REPO,"courseware","assets","figures")
IDX=json.load(open(os.path.join(HERE,"slide_index.json")))

if not os.path.exists(PDF):
    sys.exit("deck PDF not found: %s (render it first)"%PDF)
os.makedirs(OUT,exist_ok=True)

made=0
for num, overview_page in sorted(((int(k),v) for k,v in IDX["labs"].items())):
    page=overview_page+1          # the process map follows the overview slide
    stem=os.path.join(OUT,"lab-%02d-process"%num)
    subprocess.run(["pdftoppm","-f",str(page),"-l",str(page),"-r","110","-png",
                    "-singlefile",PDF,stem],check=True)
    if os.path.exists(stem+".png"): made+=1
print("wrote %d lab figures to %s"%(made,OUT))
