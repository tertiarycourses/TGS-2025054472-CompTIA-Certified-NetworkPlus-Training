---
name: courseware-build
description: Single-source build pipeline for a WSQ course — one content module (course_data.py + data_domainN.py) drives ALL artifacts (the all-white slide deck PPT, the Lesson Plan LP, the Learner Guide LG + its Markdown mirror, and the labs/ index) so they stay 100% aligned. Generic and course-agnostic: it locates the course repo and derives every filename from course_data, so the same engine works for any WSQ course. Use to regenerate courseware after editing course content.
---

# courseware-build — single-source WSQ courseware pipeline

**Model policy:** WSQ courseware generation must run on **Claude Opus 5** (`claude-opus-5`), never a Fable/other tier. If you are not on Opus 5, switch before generating (`/model opus`) — courseware quality and house-standard compliance are calibrated on Opus 5.

**Key principle:** the course material must be **100% aligned to the exam/skills domains so
students who take the course can pass the exam.** One content module drives every artifact, so
titles, lab numbering, learning outcomes, the schedule and the assessment can never drift apart.

## Layout

```
.claude/skills/courseware-build/
  SKILL.md
  assets/            brand assets (tertiary-infotech-logo.png + any course badge)
  build/
    course_data.example.py   TEMPLATE → copy to course_data.py and fill in (metadata, outcomes, topics, schedule)
    data_domain.example.py   TEMPLATE → copy to data_domain1.py … data_domainN.py (per-domain activities/labs)
    build_slides.py       generic engine → courseware/<TITLE>-<VER>.pptx  (all-white house style)
    build_lesson_plan.py  generic engine → courseware/LP-<TITLE>.docx
    build_learner_guide.py generic engine → LG-<TITLE>.md (repo root) + courseware/LG-<TITLE>.docx
    prodoc.py             shared DOCX helpers (cover page, version-control record, TOC, page numbers)
    inject_toc.py         page-numbered TOC injector (LibreOffice can't update TOC fields headless)
    build_courseware.sh   orchestrator: generate → render PDF → inject TOC → re-render
```

## How the pipeline stays generic (won't break when moved / installed elsewhere)

- Each builder finds the **course repo** by walking up from its own location for a directory that
  contains both `courseware/` and `labs/`. Override with the `COURSE_REPO` env var.
- `assets/` is resolved **relative to the skill** (co-located), never a hard-coded path.
- Output filenames are derived from `course_data.SHORT_TITLE` / `VERSION` — nothing is hard-coded to
  a specific course, so the same engine builds any WSQ course.

## Build

```bash
# one command: PPT + LP + LG as DOCX + PDF, with page-numbered TOCs
bash .claude/skills/courseware-build/build/build_courseware.sh

# or individually
python3 .claude/skills/courseware-build/build/build_slides.py
python3 .claude/skills/courseware-build/build/build_lesson_plan.py
python3 .claude/skills/courseware-build/build/build_learner_guide.py
```

Assessments (WA SAQ + PP) are built by the sibling **wsq-assessment** skill from the same course
content, so the assessment stays aligned with the slides/LG/LP.

## After a build (mandatory)

Bump `VERSION` in `course_data.py`, add a Document Version Control Record entry in the LG/LP builders,
delete superseded versioned files, then run the **courseware-qa** agent to visually audit the deck
against the WSQ hard rules before reporting completion.

## Reusing for a new course

Copy this skill into the new course's `.claude/skills/courseware-build/`, replace `course_data.py` and
`data_domainN.py` with the new course's content, drop the course badge into `assets/`, and run the
orchestrator. The engine files (build_*.py, prodoc.py, inject_toc.py, build_courseware.sh) are reused
unchanged.


## Course ed-tool (NovaSPC pattern)

If the course has a companion ed-tool (e.g. NovaSPC, https://alfredang.github.io/novaspc/, for the
SPC course), it is part of the single source: each activity dict carries the tool in `services`, a
tool step inside `steps`/`flow`, and a `csv=dict(name=..., rows=[[header],[...]])` data set. The LG
builder writes every `csv` to **labs/data/<name>.csv** and the lab files link it; the slide builder
renders an ed-tool intro slide in the admin block. Expected tool outputs (centre lines, limits,
OOC counts, Cp/Cpk/Pp/Ppk) belong in each activity's `test` so learners can self-verify.

## Deck scale, substance and motion (MANDATORY — v2 engine)

The v2 slide engine is `build/build_slides_v2_reference.py` — the proven implementation of the
components below (Gemini ADK deck v1.3, 160 slides, mean 28.6 shapes/slide, 0 overflow). Port
its helpers rather than hand-rolling layouts.

### 1. Slide count must match course duration
| Duration | Slides |
|---|---|
| 1 day (8h)  | 80–120 |
| 2 days (16h)| 100–150 |
| 3 days (24h)| 150–180 |
| 4+ days     | 200–250 |

Reach the band with **substantive teaching content**, never decorative filler. If the source
content runs out, expand from the course's original/legacy deck or reputable public
documentation, kept aligned to the assessed learning outcomes.

### 2. Instructional slides must be substantive
Every teaching slide carries a **substantive explanation, comparison, framework, worked example
or analysis**. A body of one or two sentences is only acceptable on a *section divider* or a
*big statement*. Section dividers stay brief; teaching slides are information-rich.

**Each lab expands into a full teaching unit** (this alone roughly doubles a thin deck):
```
activity_overview  →  process_map  →  steps_slide × ceil(len(steps)/4)  →  test_slide
   briefing            how it runs      the real procedure + commands       verify + troubleshoot
```
Drive it from the data you already have — `data_domainN.py` `steps` (text, command) pairs are
the procedure, `objective` is the process-map synthesis, `test` is the verify criterion.

### 3. Components to use (see tertiary-ppt-design for the full spec)
`process_map` (real connectors + arrowheads), `decision_map` (real diamond), `compare_table`,
`worked_example` (code + line-by-line), `chart_slide` (**native** pptx charts via `ChartData` /
`XL_CHART_TYPE`, with a "what the data shows" band), `steps_slide`, plus the existing
`tile_grid` / `cards3` / `trainer_slide` / `big_statement`.

### 4. Restrained motion
Content slides `fade` (fast), section dividers `push` (med), applied in **one pass at the end**.
Appear-on-click fade builds on **process maps only**. No spins, flies, zooms or sound; morph is
unavailable via python-pptx.

### 5. Verify before reporting completion
```bash
python3 -c "
from pptx import Presentation; from pptx.util import Emu; from statistics import mean,median
p=Presentation('deck.pptx'); c=[len(s.shapes) for s in p.slides]
print('slides',len(c),'mean %.1f'%mean(c),'median',median(c))"
```
Targets: slide count in band, mean ≈28 shapes, **0 shapes past the slide bottom**, transitions
on every slide. Then render pages to images and run `courseware-qa`.
