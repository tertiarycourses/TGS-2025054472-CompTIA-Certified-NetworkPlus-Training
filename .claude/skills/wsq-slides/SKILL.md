---
name: wsq-slides
description: >
  Generate or revamp WSQ courseware slide decks for Tertiary Infotech Academy Pte Ltd.
  Use whenever building, revamping, or standardising a WSQ training PowerPoint (.pptx).
  Enforces the house standards: copyright line, organisation name + UEN on the front
  page, two "About the Trainer" variants (a blank General Trainer template and the
  named trainer) as visual profile cards, the correct admin slide order (Briefing for
  Assessment before the Assessment slide), a Lesson Plan slide, a mandatory professional
  visual component system (tile grids, flow diagrams, cards, profile cards — never plain
  bullet walls), and the assessment admin pages (Assessment, Assessment Flow, Digital
  Attendance/TRAQOM) repeated at the END of the deck before Thank You.
---

> **Key principle:** The course material must be **100% aligned to the exam/skills domains** so that students who take the course can pass the exam.

# WSQ Slides Skill

**Model policy:** WSQ courseware generation must run on **Claude Opus 5** (`claude-opus-5`), never a Fable/other tier. If you are not on Opus 5, switch before generating (`/model opus`) — courseware quality and house-standard compliance are calibrated on Opus 5.

> **Scope:** This skill (with `wsq-learner-guide` and `wsq-lesson-plan`) applies to **all**
> Tertiary Infotech Academy WSQ courseware design — not just one course. Swap in the relevant
> course title, TGS code and content; keep the house standard below.

House standard for Tertiary Infotech Academy WSQ courseware decks. Apply ALL of the
rules below to every WSQ slide deck you create or revamp.

## HARD RULES (non-negotiable)

Every WSQ deck **must** satisfy all of the following. A deck that fails any of these does
not meet the WSQ house standard.

1. **Slides must ALWAYS be visual — never a wall of bullet text.** Build each slide from
   the [Visual design system](#visual-design-system-mandatory) components (tile grids,
   horizontal flow diagrams, colour-topped cards, profile cards, big statements,
   activity/step/verify slides, section dividers). Any slide that would be 4+ bullets of
   concept, outcome, process, comparison or trainer content **must** be converted to the
   matching component. Plain bullet lists are allowed **only** for genuinely list-like
   admin text (Learner Introduction, LMS instructions).

2. **Admin pages must be present** (see [Required elements](#required-elements) for detail):
   Title (org + UEN), Digital Attendance (TRAQOM · SSG), About the Trainer ×2, Learner
   Introduction, Ground Rules, Course Outline / Lesson Plan, Learning Outcomes, Briefing
   for Assessment, Assessment & Funding, and the LMS courseware/assessment slide.

3. **About the Trainer — two slides, as visual profile cards** (avatar badge + name/role
   panel + labelled info tiles): a blank **General Trainer** template and the **named
   trainer**. Never a plain bullet list.

4. **Assessment Flow must be a horizontal numbered flow diagram** (numbered chips joined
   by chevrons): TRAQOM → Assessment Digital Attendance → Assessment (WA then PP) →
   Submit on the LMS → Sign the Assessment Summary Record.

5. **TRAQOM · SSG Digital Attendance page must be present** (front of deck, and again at
   the end — see rule 6). TRAQOM = the SSG **digital attendance** system, not a survey.

6. **Assessment admin pages repeated at the END**, immediately before *Thank You*, in
   this order: **Assessment** (reminder) → **Assessment Flow** (the flow diagram) →
   **Digital Attendance (Mandatory)** (TRAQOM · SSG).

7. **Visual QA before delivery** — render the new/changed slides to images and inspect for
   overlap, clipping and balance.

7a. **DECK SCALE — slide count must match the course duration.** A WSQ deck that is far
   short of these bands is under-built and must be beefed up (expand each lab into a full
   teaching unit, add comparison/decision/worked-example slides, add concept depth from the
   original deck or authoritative public sources) before delivery:

   | Course duration | Required slide count |
   |---|---|
   | 1 day  (8h)  | **80–120 slides** |
   | 2 days (16h) | **100–150 slides** |
   | 3 days (24h) | **150–180 slides** |
   | 4+ days      | **200–250 slides** |

   Check it: `python3 -c "from pptx import Presentation; print(len(Presentation('deck.pptx').slides))"`.
   Never pad with decorative filler to reach the band — reach it with *substantive* teaching
   content (rule 7b). If content genuinely runs out, source additional material from the
   original/legacy deck for the course or reputable public documentation, and keep it aligned
   to the assessed learning outcomes.

7b. **INSTRUCTIONAL SLIDES MUST BE SUBSTANTIVE — no decorative one-liner slides.** Every
   teaching slide must carry real instructional load: a **substantive explanation, a
   comparison, a framework, a worked example, or an analysis**. A slide whose entire body is
   one or two sentences is a failure unless it is a *section divider* or a *big statement*
   (which stay deliberately brief). In practice:
   - A lab/activity is never just "briefing + verify". Expand it to a full unit:
     **briefing → process map → procedure slides (with the real commands) → verify slide
     with a troubleshooting band.**
   - A verify/test slide states the expected result **and** how to diagnose failure.
   - A concept slide that is a sequence becomes a `process_map`; a choice becomes a
     `decision_map`; two or more things being weighed becomes a `compare_table`; an API or
     code idea becomes a `worked_example`.
   - Density check (from the measured reference): mean **≈28 shapes/slide**, median ≈28.
     Under ~20 shapes on a non-divider slide means it is under-built.

7c. **RESTRAINED MOTION — transitions and animation are required, distraction is not.**
   Ship polished motion, never a slideshow that fidgets:
   - **One transition family for the whole deck.** Content slides `fade` (fast); section
     dividers `push` (medium). Nothing else. No random/checkerboard/vortex/sound.
   - **Animation only where it aids teaching** — an appear-on-click *fade* build on
     **process maps only**, so the trainer reveals one stage at a time. No spins, flies,
     bounces or zooms; never animate body text or whole slides.
   - Transitions are applied in one pass at the end of the build so every slide is covered
     exactly once.

7d. **Process maps must be REAL shapes and REAL connectors** — staged rounded-rectangles
   joined by actual PowerPoint connectors with arrowheads (`MSO_CONNECTOR.STRAIGHT` +
   `a:tailEnd`), plus a synthesis band. **Never** type "→" or "▶" into a text box and call it
   a process; typed glyphs give none of the spacing and read as prose.

8. **Import and reuse ALL the reference diagram components — never hand-roll slide layouts.**
   The deck MUST be built from the visual component helpers shipped in
   `reference/build_slides.py` — import/port **every** one of them into the course's
   `build_slides.py` and use the right component for each slide:
   `cover`, `section`, `content`, `two_col`, `cards3`, `tile_grid`, `flow_h`,
   `trainer_slide`, `big_statement`, `activity_overview`, `step_slide`, `test_slide` and
   `brk` (break/lunch dividers). Do **not** lay out shapes ad hoc, and do **not** fall back
   to a plain bullet slide where a diagram component fits. If the reference gains a new
   diagram type, adopt it too. Verify before delivery that the deck actually *uses* each
   component (e.g. `grep` the builder for every helper name).

9. **Build to the instructional depth of the scheduled course.** Use these normal ranges
   for **substantive slides**: **1 day: 80–120 slides; 2 days: 100–150 slides; 3 days:
   150–180 slides; 4 days: 200–250 slides.** For longer or fractional durations, scale
   proportionally and apply instructional judgement. Use the approved legacy deck as the
   coverage floor, then deepen or update it with reliable current sources. Do not reach the
   count by padding. Every instructional slide must teach through a structured explanation,
   framework, comparison, worked example, process map, diagram, table or evidence-based
   analysis. **Do not use low-density teaching slides with only one or two comment lines.**
   Brief title, break and section-divider slides are the only exceptions. Keep detailed
   click-by-click procedures in the Learner Guide.

10. **Make practical work progressive and cross-artifact aligned.** Sequence labs from
    simple foundations to intermediate integration and finally advanced/interactive work.
    Each lab must use a meaningfully different design or scenario, and its level, output,
    concepts, K/A mapping and acceptance test must match the PPT, Learner Guide, Lesson Plan,
    workbook and assessment. Rebuild the deck first, then generate the slide map and every
    dependent artifact from the same source.

11. **Use motion purposefully.** Draw sequences as real process maps with separate stage and
    connector shapes. Apply one restrained transition style across the deck and use simple
    entrance builds only where progressive disclosure improves explanation. Never use motion
    as decoration or as the only way to understand content; the static slide must remain
    complete and accessible. Preview the slide show in PowerPoint and verify transitions and
    animations after package generation.

## Reference implementation (use this to build PPT + LP + LG)

A complete, working **single-source build pipeline** ships with this skill at
**`reference/`** (installed at both the user level `~/.claude/skills/wsq-slides/reference/`
and the project level `.claude/skills/wsq-slides/reference/`). One content module
(`course_data.py` + `data_domainN.py`) drives **all three** artifacts so they never
drift: the slide deck (`build_slides.py` — contains every visual component helper), the
Lesson Plan (`build_lesson_plan.py`) and the Learner Guide (`build_learner_guide.py`),
plus the shared `prodoc.py` (WSQ cover page + version control + TOC + footer). For any new
WSQ course, **copy `reference/` into the course repo, edit the data modules, and re-run**
— see `reference/README.md`. The `wsq-lesson-plan` and `wsq-learner-guide` skills point
to this same reference.

## Organisation constants

- Organisation name: **Tertiary Infotech Academy Pte Ltd**
- UEN: **201200696W**
- Copyright line (footer of every slide): **© Tertiary Infotech Academy Pte Ltd**
- Contact: enquiry@tertiaryinfotech.com · +65 6100 0613 · www.tertiarycourses.com.sg
- LMS (courseware download + assessment): **https://lms-tms.tertiaryinfotech.com/**

## Required elements

1. **Copyright on every slide.** Put `© Tertiary Infotech Academy Pte Ltd` in the
   footer of every slide (title, dividers, content, activity and closing slides).

2. **Front / title page.** Show the course title, course code, trainer name, version,
   and the **organisation name + UEN** clearly on the title slide.

3. **About the Trainer — two slides, as visual profile cards** (not bullet lists).
   Use the **profile-card layout**: a left panel with a round **avatar badge**
   (initials for the named trainer, a neutral "?" for the template) plus the name and
   role, and a right column of **labelled info tiles** (one coloured tile per field).
   - A **General Trainer** template — neutral/grey theme, avatar "?", info tiles left
     blank with fill-in lines (fields: Name, Title/Designation, Qualifications, Areas
     of expertise, Training & industry experience, Contact) so any trainer can fill it in.
   - The **named trainer** (e.g. Dr. Alfred Ang) — accent theme, initials avatar, tiles
     filled with Role, Certification, Delivers, Founder (or equivalent).

4. **Admin slide order.** The **Briefing for Assessment** slide must come **before**
   the **Assessment / Final Assessment** slide.

5. **Lesson Plan slide.** Include a Lesson Plan slide showing the day's schedule
   (e.g. a time/session table, typically 9:00 AM – 6:00 PM with breaks). Follow the
   [Lesson plan & assessment scheduling](#lesson-plan--assessment-scheduling) rules below.

6. **Standard admin slides** to include where relevant: Digital Attendance,
   About the Trainer (×2), Learner Introduction, Ground Rules, Course Outline,
   Lesson Plan, Briefing for Assessment, Assessment & Funding, and a closing
   Certification & TRAQOM survey slide (ai-lms-tms.tertiaryinfo.tech).

7. **LMS slide.** Include a slide telling learners to **download the courseware**
   and **complete the assessment on the LMS** at **https://lms-tms.tertiaryinfotech.com/**.
   Place it near the end (e.g. before the Certification & TRAQOM survey slide).

8. **Assessment flow.** Render the procedure as a **horizontal numbered flow diagram**
   (numbered chips joined by chevrons — not a bullet list), in this order:
   (1) TRAQOM (scan the QR code on the LMS) → (2) Assessment Digital Attendance →
   (3) Assessment (WA then PP, open book) → (4) Submit the assessment answers on the LMS →
   (5) Sign the Assessment Summary Record. The TRAQOM QR code and the assessment
   submission are both on the LMS (https://lms-tms.tertiaryinfotech.com/).

9. **Assessment admin pages at the END of the deck.** Just before the closing
   *Thank You* slide, repeat the assessment admin block so it is fresh right before
   learners sit the assessment, in this order:
   1. **Assessment** — concise reminder (WA 1 hr · PP 1 hr, open book; take the
      Assessment digital attendance; submit on the LMS).
   2. **Assessment Flow** — the same horizontal numbered flow diagram as rule 8.
   3. **Digital Attendance (Mandatory)** — the TRAQOM · SSG digital-attendance page
      (same content as the front-of-deck attendance slide).
   Then the **Thank You** closing slide. (TRAQOM here = the SSG **digital attendance**
   system, not a survey.)

10. **Access the Labs slide.** If the course's hands-on labs live in a Git/GitHub
    repository, include an **"Access the Hands-On Labs"** slide that shows the course
    **GitHub repo URL as a REAL clickable hyperlink** (python-pptx: `run.hyperlink.address`),
    plus how to get the labs — **Option A** clone (`git clone <repo>.git`) and **Option B**
    download the ZIP (GitHub *Code → Download ZIP*) — as two colour-topped cards, and a note
    that the labs run free in the browser (e.g. Killercoda). Place it in the admin / hands-on
    intro (e.g. right after the workbench slide). The repo URL **must be clickable**, not
    plain text.

11. **Practice Exam slide.** Search for the course's associated practice exam at
    **https://exams.tertiaryinfotech.com/** and, if one exists, include a **Practice Exam**
    slide with the exam's URL as a **REAL clickable hyperlink** (python-pptx:
    `run.hyperlink.address`), telling learners to attempt it before the assessment.
    Place it right after the *Courseware & Assessment on the LMS* slide
    (canonical order #16). If no matching exam exists, skip the slide and note it
    in the delivery report.

## Visual design system (mandatory)

Decks must look **professional and visual — never a wall of bullet text**. Build slides
from a small **component library** and reach for a component before a plain bullet list.
Reference implementation: the AZ-104 course `courseware/build/build_slides.py` helpers
(`tile_grid`, `flow_h`, `cards3`, `two_col`, `trainer_slide`, `big_statement`,
`activity_overview`, `step_slide`, `test_slide`, `section`).

**Required components** (use the right one for the content):
- **Section dividers** — a full-height accent bar, kicker, big title, oversized ghost number.
- **Tile grid** — a 2-column grid of light panels, each with a coloured numbered/icon
  badge, a left accent stripe, and a bold lead title + caption. Use for **Key Concepts,
  Learning Outcomes / What You Achieved, overviews, Ground Rules** — anything that would
  otherwise be a 4–6 item bullet list.
- **Horizontal flow diagram** — numbered chips joined by chevrons. Use for the
  **Assessment Flow** and any step-by-step process.
- **3-card layout** — three colour-topped cards (blue/teal/violet). Use for grouped
  comparisons (e.g. lab groupings, options).
- **Profile cards** — the About-the-Trainer layout (rule 3).
- **Big statement** — one bold sentence + supporting line, for "why it matters" beats.
- **Activity / Step / Verify** — coloured tag + description for each hands-on lab, a
  numbered-circle step slide (with an optional dark code block), and a green "✅ Test it"
  verify panel.

**Rules of thumb**
- Colours cycle through the house palette **blue → teal → violet → amber**; keep the
  all-white background and the footer/kicker system.
- A concept, outcomes, process or trainer slide must **not** be a plain `bullets`/`content`
  slide — convert it to the matching component above.
- Plain bullet slides are acceptable only for genuinely list-like admin content
  (e.g. Learner Introduction, LMS instructions).
- Always run visual QA: render the new/changed slides to images and inspect for overlap,
  clipping and balance before delivering.

## Recommended canonical order

1. Title (with org name + UEN)
2. Digital Attendance (TRAQOM · SSG)
3. About the Trainer — General (blank template, profile card)
4. About the Trainer — Named trainer (profile card)
5. Learner Introduction ("Let's know each other")
6. Ground Rules (tile grid)
7. Course Outline / Lesson Plan
8. Learning Outcomes (tile grid)
9. Briefing for Assessment
10. Assessment & Funding
11. Assessment Flow (horizontal flow diagram)
12. Access the Hands-On Labs (clickable GitHub repo link — if labs are in a repo)
13. … topic content + activities (each topic: section divider → Key Concepts tile grid → labs cards → activity/step/verify slides → recap) …
14. Summary / What You Achieved (tile grid)
15. Courseware & Assessment on the LMS (download courseware, take assessment)
16. Practice Exam (if available)
17. **Assessment** (end reminder — rule 9)
18. **Assessment Flow** (end flow diagram — rule 9)
19. **Digital Attendance (Mandatory)** — TRAQOM · SSG (end — rule 9)
20. Thank You

## Lesson plan & assessment scheduling

Every class ends at **6:00 PM**. Schedule the teaching content and activities to finish
before the assessment start time, then place the assessment at the end.

- **One-day class:** a **1-hour** assessment starts at **5:00 PM** (5:00 – 6:00 PM),
  made up of **30 min Written Assessment (WA) + 30 min Practical Performance (PP)**.
  Content and wrap-up must finish by 5:00 PM.
- **Two-day class:** a **2-hour** assessment starts at **4:00 PM** on the final day
  (4:00 – 6:00 PM), made up of **1 hr Written Assessment (WA) + 1 hr Practical
  Performance (PP)**. Content and wrap-up must finish by 4:00 PM.

To free up the time needed for the assessment block, you may compress the breaks:

- **Morning / afternoon breaks:** reduce to **10 minutes** each.
- **Lunch break:** reduce to **45 minutes**.

Always show the assessment block explicitly on the Lesson Plan slide (and in any
Lesson Plan document) with its start and end time.

## Design notes

- Build 16:9 (13.333 × 7.5 in). Either `python-pptx` (as the AZ-104 reference
  `build_slides.py` does) or `pptxgenjs` is fine — reuse the **Visual design system**
  component helpers above rather than laying out shapes ad hoc. See the `pptx` and
  `tertiary-ppt-design` skills for mechanics.
- Keep a clean, modern, all-white look with the house palette
  (blue `1F6FEB` · teal `10B981` · violet `7C3AED` · amber `F59E0B`); one kicker/accent
  per slide; consistent footer (course · code · © · page number).
- Prefer components (tile grid, flow diagram, cards, profile cards) over bullet walls —
  see the mandatory Visual design system section.
- Safe fonts: Arial throughout (Cambria/Calibri also acceptable); a monospace
  (Consolas / Courier New) for code blocks.
- Always run visual QA (render the new/changed slides to images, inspect for overlap and
  clipping) before delivering.

## Versioning rule (MANDATORY — every update)

Every content update to a courseware artifact MUST, in the same change:

1. **Bump the version number** (and the version date) in the generator/template — e.g. `VERSION="vNN"` for slide decks (the version is also part of the output filename), `VERSION = "N.N"` plus a new `VERSIONS` entry for DOCX documents.
2. **Document the change in the Document Version Control Record** — add a row (Version Number | Effective Date of Release | Summary of Included Changes | Author) wherever the document carries one (Learner Guide / Lesson Plan). For slide decks the bumped version must appear on the cover page and in the filename.
3. **Regenerate the outputs**, remove (`git rm`) the superseded versioned files, and update any references to the versioned filename (README, slides that cite the document, etc.).

Never regenerate an artifact with content changes while keeping the old version number.

## HARD RULES — WSQ deck admin slides (non-negotiable)

Every WSQ slide deck built with this skill MUST satisfy all of the following:

1. **About the Trainer — always TWO slides, as visual profile cards** (avatar badge + name/role panel + labelled info tiles — never plain bullets): first a blank **General Trainer** template (grey theme, "?" avatar, fill-in lines: Name, Title/Designation, Qualifications, Areas of expertise, Training & industry experience, Contact) for the trainer to complete, then the **named trainer** (accent theme, initials avatar, filled tiles).
2. **Assessment Flow — a horizontal numbered flow diagram** (numbered chips joined by chevrons): TRAQOM → Assessment digital attendance → Sit WA then PP → Submit on the LMS → Sign the Assessment Summary Record.
3. **TRAQOM · SSG Digital Attendance slide** at the FRONT of the deck and repeated at the END.
4. **Assessment admin pages repeated at the END**, immediately before Thank You, in this order: Assessment (reminder) → Assessment Flow (flow diagram) → Digital Attendance (Mandatory).
5. **Briefing for Assessment comes BEFORE the Assessment slide** in the front admin section.
6. **Use the wsq-slides visual components everywhere** (tile_grid, flow_h, trainer_slide, cards, flows — port them from the wsq-slides skill's reference/build_slides.py); never hand-roll plain bullet walls for admin slides (Ground Rules, Learning Outcomes, etc.).

## GitHub Pages — NOT used for WSQ courseware repos

WSQ courseware repositories (TGS-coded course repos with `courseware/` + `labs/`) do
**not** deploy to GitHub Pages. Do not create a `deploy-pages.yml` workflow, do not
enable the Pages site, and skip any "deploy static site" phase for these repos. The
repo homepage should point to the course page on www.tertiarycourses.com.sg instead.
Lab web apps are run locally by learners (or demoed via localhost) — they don't need
a hosted deployment.


## Course ed-tool integration (NovaSPC pattern)

When the course has a companion **ed-tool** (e.g. the SPC course uses **NovaSPC**,
https://alfredang.github.io/novaspc/ — CSV upload, c/u/np/p and X-mR/X̄-R/X̄-s chart panels,
Distribution and Process Capability analysis, PNG/CSV export), the deck must:

1. Carry ONE **ed-tool introduction slide** in the admin block (after Download Course Material):
   a browser-mockup card of the tool (URL bar + left navigation + statistics tiles) beside a
   numbered "how every activity uses it" tile column — same visual grammar as the LMS slide.
   Never a bare text link.
2. Name the ed-tool (with URL) and the activity's data file (labs/data/*.csv) in every
   **activity workflow slide's Tools line**, and put the tool step inside the workflow strip
   (e.g. "Upload thickness.csv to NovaSPC" → "X̄-R Chart → Generate → compare").
3. Keep the pedagogy **hand-compute first, tool confirms second** — the workflow strip shows the
   hand computation before the tool verification, so the tool never replaces the taught method.

## COMPACT v2 format — preferred for new decks

For new or revamped decks, prefer the **compact information-dense format** in
`reference/compact/` (worked example: the SPC course, TGS-2026064862 v14; visual grammar of the
Business Process Automation reference deck). It extends the classic component set with:

- `img_points` (chart image + colour-coded takeaway tiles — the workhorse concept slide) and
  `img_full` (full-width visual + caption band), fed by matplotlib assets from
  `reference/compact/make_charts.py` drawn from the SAME numbers the activities use
- `table_slide` (styled decision/comparison tables) and `formula_slide` (dark formula panels)
- `activity_slide` — ONE workflow slide per hands-on activity (badge + scenario + 5-chip
  numbered strip + "YOU'LL PRODUCE" band + Tools line); never step-per-slide runs
- browser-mockup slides for the LMS portal and any course ed-tool (never a bare text link)
- `slide_map.json` export so the Lesson Plan cites exact slide ranges

Layout rules that keep QA green: titles ≤ ~48 chars (or they wrap into the divider);
`tight_layout(rect=[0,0,1,0.86])` under matplotlib suptitles; `h_pad ≥ 2` for stacked subplots;
white bbox behind any label sitting ON a chart line; Arial-only glyphs; every generated asset
must be placed on a slide; aspect-fit images with PIL — never stretch.

## Visual quality bar — follow the measured reference grammar

Before building or revamping any deck, read **`tertiary-ppt-design`**, sections
"MEASURED GRID SPEC" and "Process, flow and timeline visuals". Those carry exact
geometry extracted from the shipped Power Automate/Copilot Studio deck v7.4 —
column widths, the five layers of a concept card, badge and chip sizes, and the
three process patterns (numbered strip, four-step diagnostic row, two-column
roadmap).

Two failure modes that pass every colour check and still look flat:

1. **Skipping a layer.** A concept card is panel + accent bar + number badge +
   title + body (+ optional chip). Drop the badge and the chip and you have a
   coloured box. Palette equality proves nothing.
2. **Describing a process instead of drawing one.** If the content is a sequence,
   a lifecycle or an ordered procedure, it gets a process strip with real ▶ shapes
   in the gaps — not bullets with arrows typed into the text.

Verify before shipping:
```python
from pptx import Presentation; from statistics import mean, median
c=[len(s.shapes) for s in Presentation("slides.pptx").slides]
print(mean(c), median(c), max(c))    # target ≈28 / 31 / 45+
```
Under ~20 shapes on a non-divider, non-image slide means it is under-built.
