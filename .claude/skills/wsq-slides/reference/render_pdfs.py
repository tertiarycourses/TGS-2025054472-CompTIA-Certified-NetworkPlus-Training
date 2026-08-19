#!/usr/bin/env python3
"""Render the built PPTX/DOCX courseware to PDF using local MS Office COM
automation (no LibreOffice available on this machine). Word updates the TOC
/ page-number fields on open, so the exported PDF's Table of Contents is
correct — no separate static-TOC injection step is needed here.

Usage: python3 render_pdfs.py <file1.pptx|.docx> [file2 ...]
"""
import os, sys, time
import win32com.client as win32

def pdf_path(src):
    return os.path.splitext(src)[0] + ".pdf"

def render_pptx(path, out):
    app = win32.gencache.EnsureDispatch("PowerPoint.Application")
    app.Visible = True
    try:
        pres = app.Presentations.Open(path, WithWindow=False)
        pres.SaveAs(out, 32)  # ppSaveAsPDF = 32
        pres.Close()
    finally:
        app.Quit()

def render_docx(path, out):
    app = win32.gencache.EnsureDispatch("Word.Application")
    app.Visible = False
    try:
        doc = app.Documents.Open(path)
        doc.Fields.Update()
        try:
            doc.TablesOfContents(1).Update()
        except Exception:
            pass
        doc.Repaginate()
        doc.Fields.Update()
        doc.SaveAs(out, FileFormat=17)  # wdFormatPDF = 17
        doc.Close(False)
    finally:
        app.Quit()

def main(files):
    for f in files:
        f = os.path.abspath(f)
        out = pdf_path(f)
        ext = os.path.splitext(f)[1].lower()
        print(f"Rendering {f} -> {out}")
        if ext == ".pptx":
            render_pptx(f, out)
        elif ext == ".docx":
            render_docx(f, out)
        else:
            print(f"  skip (unsupported extension): {f}")
            continue
        time.sleep(1)
        print(f"  OK: {out}" if os.path.exists(out) else "  FAILED: no output produced")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: render_pdfs.py <file1> [file2 ...]"); sys.exit(1)
    main(sys.argv[1:])
