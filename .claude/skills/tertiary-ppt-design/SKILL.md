---
name: tertiary-ppt-design
description: Best-practice design system and rules for building highly professional, visual training/course slide decks with python-pptx (Tertiary Infotech house style). Use whenever creating or polishing a .pptx deck so the result is clean, white-theme, visual, and consistent — large readable fonts, brand colours, icon/card layouts, screenshots and diagrams instead of walls of text. Pair with the tertiary-course-slides skill.
---

# PPT Design & Presentation — Best Practices

**Model policy:** WSQ courseware generation must run on **Claude Opus 5** (`claude-opus-5`), never a Fable/other tier. If you are not on Opus 5, switch before generating (`/model opus`) — courseware quality and house-standard compliance are calibrated on Opus 5.

Apply these when generating or refining a course/training deck (python-pptx).

## Theme & format
- **16:9** (13.333 × 7.5 in). **All-white slides — never dark/black backgrounds.**
- **Font: Arial** for every run. Brand colours: blue `#1F6FEB`, teal `#10B981`, ink `#161B26`, grey `#5B6372`, violet `#7C3AED`, light `#F5F8FC`.
- Cover with the **course title + n8n & Tertiary Infotech Academy logos + UEN**; footer on every content slide = course/code (left), `© 2026 Tertiary Infotech Academy Pte Ltd` (center), slide number (right).

## Typography (make it presentable — large fonts)
- Slide **title ≈ 28–30 pt**, kicker label ≈ 14 pt (brand colour, uppercase).
- **Body bullets ≈ 18–20 pt** (never below 16 pt). Two-column body ≈ 17 pt. Card body ≈ 14 pt.
- Section dividers: title ≈ 40 pt, big faint topic number ≈ 72 pt.
- Step slides: one step, big numbered circle + step text ≈ 24 pt.

## Be visual, not wordy
- **≤ 5 bullets per slide**, one idea per bullet. Split dense slides.
- Prefer **layouts over paragraphs**:
  - **3 colour cards** for "features / why / pillars" (heading + 3 short lines each).
  - **Two-column** for comparisons (GET vs POST, model vs memory, in-memory vs Pinecone).
  - **Big-statement** slides (one large sentence) to punctuate sections.
  - **Screenshot slides**: real product screenshots (websites, the n8n canvas) beside short steps.
  - **Diagrams**: redraw concepts in the brand theme (e.g. a RAG flow) — never paste watermarked images.
- Add a **workflow screenshot** for every hands-on activity; a **gallery** for sample student work.

## Structure of a course deck
1. Cover → admin (digital attendance/TRAQOM, trainer, ground rules, lesson plan, learning outcomes, assessment).
2. Per topic: a **section divider**, concept slides (what / why / how, with cards & comparisons), then per activity: **overview → workflow screenshot → one-step-per-slide → green "Test it"**.
3. **Lunch/tea-break** divider slides; recap slides at the end of each day; a Thank-You close.

## Consistency & alignment
- Activity titles and topic numbering must **match the Learner Guide and Lesson Plan exactly**.
- Reuse helper functions (`content`, `two_col`, `cards3`, `website_slide`, `gallery_slide`, `img_slide`, `big_statement`, `section`, `step_slide`) so spacing/fonts stay uniform.

Implementation lives in the **tertiary-course-slides** skill (`make_slides.py`).

## COMPACT v2 component specs (proven on the SPC deck, TGS-2026064862)

Full runnable reference: `wsq-slides/reference/compact/` (build_slides.py + make_charts.py +
worked-example content). Key measurements (16:9, 13.333×7.5 in, content area x 0.85–12.48 in,
y 1.95–6.65 in, footer at y 7.05):

- **img_points**: image aspect-fit to ~7.0 in wide × 4.75 in tall on the left; 3–4 takeaway
  tiles on the right, each `LIGHT` panel + 0.09 in colour bar, title 14 pt bold in the palette
  colour, caption 12 pt ink. THE default concept slide — beats any bullet wall.
- **img_full**: image aspect-fit to 11.6 in, centred; optional caption band (LIGHT, 14 pt) at
  y 6.3. For family portraits (all four attribute charts) and big comparisons.
- **table_slide**: header row in BLUE with white 13 pt bold; body rows alternate LIGHT/WHITE
  with LINE borders; first column bold; per-column width fractions; ≤ 8 rows.
- **formula_slide**: 2–3 panels; each LIGHT with 0.1 in top colour bar, heading 16 pt, formula
  in a NAVY box (15 pt bold, light-blue #9CDCFE), caption 12.5 pt grey.
- **activity_slide**: teal kicker `TOPIC 0X · HANDS-ON ACTIVITY`; top-right badge
  `ACTIVITY N · M MIN`; scenario ≤ 3 lines at 15 pt; 5 chips (0.56 in numbered circles, labels
  11.5 pt, ▶ connectors); green `YOU'LL PRODUCE` band; grey Tools line naming the ed-tool +
  data file + "Full step-by-step guide: Learner Guide, Activity N".
- **browser-mock slides** (LMS / ed-tool): white card with traffic-light dots, URL pill, nav or
  content mock inside; numbered how-to tiles on the right; one summary line under both.
- **Chart assets** (make_charts.py): matplotlib, Arial, white bg, palette #1F6FEB/#10B981/
  #7C3AED/#F59E0B (+#DC2626 for limits/defects), 150 dpi, bbox_inches="tight". Draw from the
  SAME numbers the labs use. Pitfalls that cost QA rounds: suptitle needs
  `tight_layout(rect=[0,0,1,0.86])`; stacked subplots need `h_pad ≥ 2`; labels on lines need a
  white bbox; avoid non-Arial glyphs (e.g. superscript minus U+207B).
- **Titles ≤ ~48 chars** at 28 pt or they wrap into the divider rule.
- **slide_map.json**: `mark(key)` before each section/activity; the LP builder reads it so
  schedule slide references never drift from the deck.

## Reference-deck concept grammar (proven on the n8n deck v47 + the Power Automate/Copilot deck v7.4)
For concept-heavy technical decks (n8n, Power Automate, agentic AI), use this grammar instead of bullet walls:
- **Mechanism chevron strips** (`chev_strip`): outlined white boxes (bold title + small grey sub-caption) joined by ▶ — one strip per mechanism (webhook round-trip, RAG ingestion vs retrieval as two stacked strips, expression resolution, approval suspension). Red "manual" vs green "automated" stacked strips make a strong before/after.
- **Outlined concept cards** (`ncards`): white fill, colored border, numbered badge, colored title, 1–2 line body — for enumerations (trigger nodes, data-processing nodes, model parameters, guardrail scopes).
- **Two-panel comparisons** (`two_panel`): solid colored header bars over outlined bullet panels — GET vs POST, Test URL vs Production URL, Generative vs Agentic AI, MCP server vs client.
- **Data tables** (`data_table`): colored header row + striped rows, first column bold — trigger→lab mapping, HTTP anatomy, vector DB comparison, human in/on/out of the loop.
- **Good/bad callout pairs**: green ✓ vs red ✗ outlined boxes (good vs bad agent instructions, picker vs typed expressions, prompt-stuffing vs retrieval).
- **Takeaway band** (`takeaway`): end most concept slides with ONE bold boxed sentence stating the rule to remember.
- **Agent anatomy hub**: central "THE AI AGENT" box with four outlined satellite cards — MODEL, MEMORY, TOOLS, INSTRUCTIONS.
- **Lab slides** (`lab_slide`): ONE per activity — intro line + workflow chevron strip of the ACTUAL nodes (title = node, sub = role) + the real n8n/product screenshot + a bottom LAB band (ACT chip · lab name · stack meta · "steps in the Learner Guide"); plus a `website_lab` screenshot slide when the lab has a web front-end. Step-by-step detail lives ONLY in the Learner Guide.
- **Concept coverage for agentic-AI courses**: trigger nodes (+ which lab uses which), data-processing nodes, webhook GET vs POST and **Test vs Production URL**, agent components, good-vs-bad instructions, model parameters (temperature bands), MCP, RAG four words (chunk · embedding · similarity · top_k) + the dimension rule, human in/on/out of the loop, input/output guardrails.
- Runnable implementation: the n8n course repo's `.claude/skills/tertiary-course-slides/make_slides.py` (v47).

## MEASURED GRID SPEC — extracted from the Power Automate/Copilot deck v7.4

Everything below was **measured out of the shipped deck**, not estimated. When a
generated deck looks flat next to that one, the cause is almost always that it
skipped a *layer*, not that it used the wrong colour. Reproduce the layers.

### Canvas and the one content column
```
slide            13.333 × 7.5 in
content column   x = 0.72  →  12.57      (width 11.85)   ← every full-width band uses this
kicker           x 0.72, y 0.34, 12 pt BOLD, accent colour, UPPERCASE, " · " separated
title            x 0.72, y 0.68, 29 pt BOLD ink          ← 29, not 28
hairline rule    x 0.72, y 1.50, 11.85 × 0.01, #D7E0EA   ← separates head from body
left edge tab    x 0.00, y 0.00, 0.22 × 1.48, accent     ← the vertical colour tab, easy to omit
body starts      y = 1.85
footer           y = 6.95, 8 pt: course name (left) + slide number (right)
```

### Card grid — pick the column count, then use these exact widths
| Columns | Card width | Left positions | Gap |
|---|---|---|---|
| 2 | 5.85 | 0.72, 6.72 | 0.15 |
| 3 | 3.71 | 0.72, 4.71, 8.70 | 0.28 |
| 4 | 2.72 | 0.72, 3.72, 6.72, 9.72 | 0.28 |

Card height 2.50 typical (1.85–3.15 range). **Four across is the reference's
signature move** — a 2×2 grid of fat cards reads as a poster; 4 across reads as a
system.

### The five layers of a concept card (omit one and it looks generic)
```
1  panel        card_w × 2.50           fill #F5F8FC
2  accent bar   0.09 × 2.50 at card x   fill = that card's accent   ← left edge, full height
3  number badge 0.46 × 0.46 at x+0.24, y+0.20, accent fill, 15 pt BOLD white, centred
4  title        14 pt BOLD ink, x+0.82 (right of the badge), y+0.14
5  body         11 pt ink, x+0.28, y+0.66, width card_w−0.54, 2–4 lines
6  chip (opt)   1.50 × 0.34 accent fill, 10 pt BOLD white — "Labs 1–3", "Every lab"
```
Note layers 3 and 4 sit **side by side on the same line**, not stacked. Body drops
below both.

### Full-width closers — a concept slide is not finished without one
```
synthesis band   0.72, 4.62, 11.85 × 1.50, #F5F8FC
   heading       12 pt BOLD accent, UPPERCASE, at +0.28, +0.13
   body          12 pt ink, at +0.28, +0.50, width 11.30
lab band         0.72, 6.08, 11.85 × 0.78, #FFFFFF (sits on the page, not in it)
   chip          1.15 × 0.50 accent at 0.92, 13 pt BOLD white  — "LAB 0", "ACT 2"
   title         14 pt BOLD at 2.25
   meta          11 pt grey at 2.25, +0.36 — environment · tools · " · " separated
```

### Section divider — 7 shapes, no more
```
panel  0.72, 1.90, 11.85 × 3.60, #F5F8FC
bar    0.72, 1.90,  0.14 × 3.60, accent      ← 0.14 here, wider than a card's 0.09
label  1.40, 2.35, 15 pt BOLD accent         "MODULE 1" / "TOPIC 1"
title  1.40, 2.85, 34 pt BOLD ink            ← 34, larger than a content title
sub    1.40, 3.95, 15 pt grey                the outcome, " · " separated
```

### Type scale, as actually used
`29 title · 34 divider title · 15 divider label · 14 card title · 13 lab chip ·
12 kicker/synthesis · 11 card body · 10 chip · 8 footer`

**This contradicts the "body ≈ 18–20 pt" guidance above.** Both are right in their
place: 18–20 pt is for a slide whose body is a short bullet list. In the card grid
the body is 11 pt because there are four columns of it and a synthesis band
underneath — the *composition* carries the slide, not the type size. Do not scale
card body text up; it breaks the grid and forces a 2-column fallback.

### Accent rotation
`#1F6FEB blue → #6D3FD2 purple → #108A73 teal → #16845B green → #C77600 amber →
#C2413A red`. Rotate **per card within a slide**, and per section across the deck.
Amber and red carry meaning (caution / failure) — do not use them decoratively.

### Density target
Mean **28 shapes per slide**, median 31, top slides 45–73. A 12-shape "concept"
slide is a bullet list wearing a card. If a slide is under ~20 shapes and is not a
divider (7), a lab-workflow (13–15) or a full-bleed image, it is under-built.

### The check that catches a flat deck
```python
from pptx import Presentation; from statistics import mean, median
p = Presentation("slides.pptx"); c = [len(s.shapes) for s in p.slides]
print(mean(c), median(c), max(c))       # want ≈28 / 31 / 45+
```
Then dump one concept slide's shapes sorted by (top, left) and confirm all five
card layers are present. Comparing *palettes* proves nothing — two decks can share
every hex value and look completely different if one skipped the badges, the chips
and the synthesis band.

### Process, flow and timeline visuals — the reference's most-used shapes

The v7.4 deck leans heavily on **process** rather than description. Three
measured patterns cover almost all of it. Reach for one of these before writing
any slide whose content is a sequence, a lifecycle or a set of ordered steps.

#### A. Numbered process strip (5 stages, with ▶ connectors)
The assessment-flow slide. Use for any 4–6 stage linear process.
```
card    2.05 × 3.15   at x 0.85, 3.24, 5.64, 8.03, 10.43   (gap 0.34)   #F5F8FC
top bar 2.05 × 0.10   same x, same y, accent                ← TOP bar here, not left
badge   0.82 × 0.82   centred in card, y +0.42, accent fill, 30 pt BOLD white
▶       0.42 × 0.60   in the gap, y 3.83, 15 pt BOLD accent  ← between cards only
body    1.73 × 1.45   centred, y 4.10, 14 pt ink, 2–4 lines
```
The badge is **30 pt** — deliberately oversized. That single choice is what makes
the strip read as a process at the back of a room.

#### B. Four-step diagnostic row (with a synthesis band underneath)
The run-history slide. Use for a *procedure* — the steps someone follows.
```
card   2.72 × 2.30 at the 4-across x positions, #F5F8FC
bar    0.09 × 2.30 left edge, accent (rotate per card)
badge  0.46 × 0.46 at x+0.24, y+0.20, 15 pt BOLD white
title  1.68 × 0.44 at x+0.82, y+0.14, 14 pt BOLD
body   2.18 × 1.50 at x+0.28, y+0.66, 11 pt
band   11.85 × 1.35 at y 4.95 — the caveat the four steps do not cover
```
The synthesis band is where the *judgement* goes ("the three states that look
alike"). The cards carry the procedure; the band carries what makes it hard.

#### C. Two-column roadmap / timeline (the "journey" slide)
13 items on one slide, still legible. Use for the lab or topic roadmap.
```
row    5.85 × 0.57, left column x 0.72, right column x 6.72
       y from 1.62, pitch 0.63  (rows: 1.62, 2.25, 2.88, 3.51, 4.14, 4.77, 5.40)
badge  0.44 × 0.44 at x+0.10, y+0.07, accent fill, 11.5 pt BOLD white
title  5.08 × 0.30 at x+0.66, y+0.00, 11.5 pt BOLD ink
sub    5.08 × 0.27 at x+0.66, y+0.28,  9 pt grey     ← the one-line "what it teaches"
closer 11.85 × 0.62 at y 6.14, #F5F8FC, 14 pt BOLD — the through-line
```
Reading order is **down the left column, then down the right** — number the
badges accordingly. Accent changes per *phase*, not per row, so the colour blocks
show the shape of the course.

#### Choosing between them
| Content | Pattern |
|---|---|
| A linear process, 4–6 stages | A — numbered strip with ▶ |
| A procedure someone performs | B — 4 cards + synthesis band |
| A roadmap / many ordered items | C — two-column rows |
| A comparison, 2–4 things | 4-across card grid (no ▶) |
| One mechanism with a twist | 4-across grid + synthesis band |

**Do not draw a process as bullets with arrows typed into the text.** The ▶ is its
own shape in the gap between cards; typing "→" inside a text box gives none of the
spacing and reads as prose.


## COMPACT v3 component specs — technical / API-teaching courses

Added for the Agentic AI course (TGS-2025059028, 201 slides). These are what let a
deck teach a real SDK without collapsing into a wall of monospace text. Reference
implementation: `wsq-slides/reference/compact/build_slides.py`.

- **code_slide(title, code, caption=)** — full-width syntax-highlighted code card on a
  near-black navy panel (`#0B1220`) with an accent bar. The card **shrink-wraps to its
  own line count and is vertically centred**: a fixed-height card under a 6-line snippet
  reads as a rendering bug. Font auto-sizes 15 → 10 pt by line count. Use the `caption`
  band (LIGHT, 12.5 pt) to state *what the code proves*, not to repeat it.
- **code_points(title, code, points)** — code card LEFT (~6.9 in), 3–4 colour-coded
  takeaway tiles RIGHT. **The workhorse for "here is the API, here is what matters
  about it."** Prefer this over a bare code_slide whenever the code has more than one
  teachable idea.
- **annotated_code(title, code, annotations)** — numbered badges in the left gutter,
  aligned to the exact code line they annotate (`(line_no, text)`, 1-based), with the
  matching numbered explanations in a 2-column grid underneath. For the 3–5 line
  moments that carry the whole concept (a tripwire, a handoff, a context= handoff).
- **api_table(title, rows, headers=)** — parameter reference: a **monospace, accent-coloured
  name column** (30%) beside a plain-language description column. Alternating row fill,
  accent header band. This replaced bullet-list API dumps entirely — it is dramatically
  more scannable and is the single highest-value addition in v3.
- **compare3(title, cols)** — three labelled comparison columns of short rows, each with a
  coloured header band. For "framework A vs B vs C" decisions. Keep rows ≤ 6 and ≤ 30 chars.
- **stack(title, items)** — vertical numbered stack, big badge + bold title + grey caption
  per row. Reads as a *sequence*: a process, a hierarchy, an ordered checklist. Use where
  a tile_grid would wrongly imply the items are unordered.
- **split_note(title, l_head, l_items, r_head, r_items)** — Do/Don't (or Wrong/Right) two
  panels with tinted backgrounds (red `#FEF2F2` / green `#E8F7EE`). Excellent for
  anti-patterns, and for the safety/utility trade-off shape.
- **verify_slide(activity)** — the green "Test it" acceptance criterion for a hands-on
  activity, plus its deliverable and its lab folder. One per activity, straight after the
  activity_slide.

### Syntax highlighting
`_code_runs()` / `_code_lines()` tokenise Python into coloured runs — keywords `#FF7B72`,
strings `#A5D6FF`, functions/classes `#D2A8FF`, comments `#8B949E`, numbers `#79C0FF`.
`_code_lines()` tracks **triple-quoted docstrings across lines** so a multi-line docstring
renders as one continuous string colour. Deliberately not a real parser — enough to make
slide code readable.

### Title auto-fit (hard-won)
`_fit_title_size()` **measures** the rendered width in Arial Bold with PIL and picks the
largest of 28/26/24/22/21 pt that fits on ONE line, against `TITLE_BOX_IN = 11.75 * 0.95`.
- A character-count heuristic is **not** safe: two 58-character titles can differ by 2 in
  of rendered width, and the one that wraps has its second line struck through by the
  divider rule.
- The 5% margin is required — PowerPoint and LibreOffice lay text out slightly
  differently, so a title measured at 99% of the box still wraps when rendered.

### Rules learned building the 201-slide deck
- **Never bake a title into a diagram PNG shown with `img_full`** — `head()` already draws
  the slide title and the two collide. Titles belong on the slide, captions in the figure.
- One idea per slide still holds at 200 slides: it is better to have 12 focused slides on a
  framework than 4 crowded ones.
- Diagrams should teach a *mechanism*, not decorate. The best assets in this deck
  (`chunking_overlap`, `prompt_injection`) each make one non-obvious idea visible.

## MOTION — transitions & animation (python-pptx, proven on the Gemini ADK deck v1.3)

Polished motion, never a distracting one. **One transition family per deck**; animation only
where it genuinely aids teaching.

House rule:
- **Content slides** → `fade`, speed `fast`.
- **Section dividers** → `push` (dir `l`), speed `med`.
- **Nothing else.** No random/checkerboard/vortex/wipe-per-slide, no sound, no auto-advance
  (`advClick="1"` keeps the trainer in control).
- **Animation is reserved for process maps**: an appear-on-click *fade* build so the trainer
  reveals one stage at a time. Never animate body text, bullets or whole slides.

python-pptx cannot write transitions natively — inject the OOXML. `p:transition` must be the
**last** child of `p:sld`, and the PowerPoint-2010 set is what LibreOffice/PowerPoint both honour:

```python
from pptx.oxml.ns import qn
from lxml import etree

def _transition(s, kind="fade", speed="med"):
    sld = s._element
    for old in sld.findall(qn("p:transition")): sld.remove(old)
    tr = etree.SubElement(sld, qn("p:transition"))
    tr.set("spd", speed); tr.set("advClick", "1")
    if kind == "fade":  etree.SubElement(tr, qn("p:fade"))
    elif kind == "push": etree.SubElement(tr, qn("p:push")).set("dir", "l")
    sld.append(tr)          # schema order: transition goes last
```

Apply it in **one pass at the very end of the build**, so every slide is covered exactly once
and no later helper can overwrite it.

Appear-on-click builds use a `p:timing` tree targeting shape ids (`p:spTgt spid=`). Use
`presetID="1" presetClass="entr"` (Appear) plus a 400 ms `animEffect filter="fade"`; the first
node is `clickEffect`, the rest `afterEffect` so one click reveals a stage and its connector.
Grab `shape.shape_id` as you draw each stage — that is what the timing tree references.

**Morph is not available** through this route: it is a `p159:morph` extension, not part of the
2010 transition set. Do not attempt it; the fade/push pair is the house look.

## Process maps, decisions and charts — real shapes, not typed glyphs

`from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR`

- **`process_map(title, stages, synthesis=)`** — staged `ROUNDED_RECTANGLE` cards, each with a
  colour top bar + oversized number badge, joined by **real connectors**
  (`add_connector(MSO_CONNECTOR.STRAIGHT, ...)`) with an arrowhead appended as
  `a:tailEnd type="triangle"` on the line's `<a:ln>`. Closes with a synthesis band ("THE POINT").
  Give the label its own fixed band and the caption the remainder — if they share a box the
  label wraps into the caption and collides.
- **`decision_map(title, question, yes, no)`** — a real `MSO_SHAPE.DIAMOND` with two branch
  connectors to outcome panels (teal = yes, amber = no). Use for "which pattern do I choose".
- **`compare_table(title, headers, rows, note=)`** — a real comparison matrix with a coloured
  header row, zebra body rows and a "WHEN IT MATTERS" band. Budget the row height against the
  footer explicitly (`BOTTOM = 6.88in − note band`), or 5+ rows overrun the footer.
- **`worked_example(title, intro, code, explain)`** — dark code card on the left, 4 colour-coded
  "what this line does" tiles on the right. This is what turns a decorative API slide into a
  teaching slide.

### Native charts (editable, not screenshots)
```python
from pptx.chart.data import ChartData, XyChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
```
`chart_slide(title, categories, series, kind=, insight=)` adds a **native** chart with
`add_chart(...)` — it stays editable in PowerPoint and never pixelates. House treatment:
- `chart.has_title = False` (the slide's `head()` already carries the title — two titles collide).
- Arial 12 pt, ink; legend BOTTOM with `include_in_layout = False`, and only when there are
  multiple series or it is a pie/doughnut.
- Recolour to the house palette **per point** for pie/doughnut (`plot.points[i].format.fill`)
  and **per series** otherwise; for `LINE_MARKERS` set `series.format.line.color` instead of fill.
- Turn on data labels (`plot.has_data_labels`) with an explicit `number_format` and
  `number_format_is_linked = False`, else the label ignores your format.
- Always pair the chart with a **"WHAT THE DATA SHOWS" insight band** — a chart without the
  reading is decoration. Label indicative teaching figures as indicative.
- Wrap the recolour/data-label blocks in `try/except`: chart types differ in what they expose.

### Overflow check that must pass before delivery
```python
from pptx import Presentation; from pptx.util import Emu
p = Presentation("deck.pptx"); SH = Emu(6858000)      # 7.5in
bad = [(i, sh.text_frame.text[:40])
       for i, s in enumerate(p.slides, 1) for sh in s.shapes
       if sh.has_text_frame and sh.text_frame.text.strip()
       and sh.top is not None and sh.height is not None
       and sh.height < Emu(int(7.0*914400))            # skip full-bleed backgrounds
       and sh.top + sh.height > SH]
print(len(bad), bad[:10])                              # must be 0
```
Long titles also need `_fit_title()` (step 29→25→22→20 pt by length) or they wrap through the
hairline rule — visible immediately on a "— Part 1/2" continuation title.

### Text-fit defects a geometry check will NOT catch (found by rendering, v1.3 QA)

A shape-bounds check (`top + height > slide height`) proves only that the *box* is on the
slide. It says nothing about whether the **text inside** fits. These six defects all passed the
geometry check and were caught only by rendering pages to images:

1. **Mid-word truncation.** `label[:42]` slices "…dependencies with uv (creates" — ugly and
   unreadable. Always truncate on a word boundary with an ellipsis:
   ```python
   def _ellipsis(text, limit):
       t = " ".join(str(text).split())
       if len(t) <= limit: return t
       cut = t[:limit]; sp = cut.rfind(" ")
       if sp > limit*0.55: cut = cut[:sp]
       return cut.rstrip(" ,.;:-—(") + "…"
   ```
2. **Two-line captions overflow their card.** A caption box sized for one line renders two and
   spills through the card's bottom border. Force **one line**, anchor it near the card bottom
   (`y + ch − 0.52in`), and shorten the source string (~26 chars) rather than trusting wrap.
3. **Diamond text spills past the facets.** A diamond's usable text area is only ~50% of its
   bounding box. 3 lines at 13 pt need roughly **4.6 × 2.7 in**, not 3.5 × 2.0.
4. **Chart category labels truncate.** Slicing a long topic title (`title[:34]`) shows
   "Build A Multi Agent App with Gemin". Author **short chart labels** — never slice.
5. **Footer page numbers off by one.** If the cover draws no footer but still occupies slide 1,
   a counter starting at 0 makes every later slide read one low. Start the counter at **1** so
   the first numbered slide prints 2.
6. **Degenerate ranges.** A grouped label prints "Labs 13–13". Emit `Lab N` when start == end.

**Rule: after any layout change, render the affected slides to PNG and look at them.** The
geometry check is a floor, not a substitute for looking.
