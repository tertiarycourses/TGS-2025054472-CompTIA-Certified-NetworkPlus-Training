# CONTENT spec — data_domainN.py schema (Network+ N10-009 deck)

Each `data_domainN.py` defines TWO module-level lists:

```python
DOMAINn  = [ <lab dict>, ... ]      # the hands-on labs of this domain
CONTENTn = [ <slide spec dict>, ... ]  # the teaching slides, in teaching order
```

Plain Python only — literals, no imports, no functions, no f-strings referencing
variables. ASCII quotes. The build engine renders CONTENTn in order; a
`dict(type="lab", num=N)` marker renders that lab's 3-slide block (overview +
process map + verify) at that position. Every lab of the domain MUST have
exactly one marker in CONTENTn, in ascending order, placed right after the
teaching slides that introduce its concepts.

## Lab dict (DOMAINn)

```python
dict(
  num=1,            # GLOBAL contiguous lab number (1..36)
  topic=1,          # domain number
  title="OSI Model Packet Inspection",
  objective="Inspect packets and map headers to OSI layers.",   # <= 110 chars
  desc="One-paragraph description of what the learner does.",   # <= 220 chars
  build="What the learner ends up with.",                       # <= 130 chars
  services="tcpdump, curl, TIS PCAP Analyzer",                  # tool list, <= 90 chars
  steps=[ ("Step instruction", "single-line shell command or ''"), ... ],  # 5-10 steps
  test="How the learner verifies success.",                     # <= 200 chars
  troubleshoot=[ ("Symptom","Fix"), ("Symptom","Fix"), ("Symptom","Fix") ],  # exactly 3, symptom <= 40, fix <= 110
)
```

Steps must be faithful to the existing `labs/lab-NN-*.md` file (same tools,
same commands). Instruction <= 90 chars; command single line <= 96 chars
(use the most representative command when the lab step has several).

## Slide spec dicts (CONTENTn)

Colors are strings: "blue" | "teal" | "violet" | "amber" | "grey".

1. **tiles** — grid of icon panels (the workhorse; use for concept groups)
   `dict(type="tiles", title=..., kicker=..., items=[("Head","Caption"), ...], cols=2, size=14, accent="blue")`
   - 4–8 items with cols=2 (6 is ideal); 3–5 items with cols=1.
   - Head <= 42 chars; caption one sentence <= 150 chars. Items may also be plain strings.

2. **cards** — 3 side-by-side comparison cards
   `dict(type="cards", title=..., kicker=..., cards=[("blue","Heading",["b1","b2",...]), ...])`
   - exactly 3 cards, 3–6 bullets each, bullet <= 60 chars.

3. **two_col** — two shaded columns with headers
   `dict(type="two_col", title=..., kicker=..., lhead="Left", rhead="Right", left=[...], right=[...])`
   - items are strings or ("text", 1) for sub-bullets; 3–6 per column, <= 70 chars.

4. **flow** — horizontal numbered chips
   `dict(type="flow", title=..., kicker=..., steps=[...], color="blue")`
   - 4–6 steps, each <= 55 chars.

5. **process** — staged process map with real connectors (animated)
   `dict(type="process", title=..., kicker=..., stages=[("Label","caption"),...], synthesis=("WHY IT MATTERS","one sentence"), color="blue")`
   - 3–6 stages; label <= 40 chars; caption <= 26 chars; synthesis sentence <= 160 chars.

6. **decision** — decision diamond with YES/NO branches
   `dict(type="decision", title=..., question="Line1\nLine2?", yes=("YES — head","body"), no=("NO — head","body"), kicker=..., note="one line")`
   - question <= 3 short lines; body <= 140 chars.

7. **table** — comparison matrix
   `dict(type="table", title=..., kicker=..., headers=[...], rows=[[...],...], note="when it matters", accent="blue")`
   - 3–5 columns, 3–6 rows; first column is the row label; cell <= 55 chars.

8. **worked** — dark code panel + line-by-line reading
   `dict(type="worked", title=..., intro="one line", code=["line1",...], explain=[("label","body"),...], kicker=...)`
   - <= 14 code lines, each <= 62 chars; exactly 2–4 explain tiles, body <= 95 chars.

9. **chart** — native editable chart + insight band
   `dict(type="chart", title=..., kicker=..., categories=[...], series=[("Name",[nums])], kind="column|bar|line|pie|doughnut", insight="what the data shows", number_format='0')`

10. **big** — big statement divider
    `dict(type="big", line1="Headline.", line2="Supporting sentence.", kicker="WHY IT MATTERS", color="blue")`

11. **bullets** — plain bullet slide. USE SPARINGLY (max 1 in 12 slides).
    `dict(type="bullets", title=..., kicker=..., items=[...], size=18)`

12. **lab** — placement marker: `dict(type="lab", num=7)`

## Substance rules (hard)

- Every teaching slide carries a substantive explanation, comparison, framework,
  worked example or analysis tied to the N10-009 objectives. No filler, no
  decorative one-liners outside `big`.
- Kickers name the exam objective where natural, e.g. `kicker="OBJ 1.4 · PORTS & PROTOCOLS"`.
- Mix the components: aim over a domain for roughly 40% tiles, 15% table,
  10% process/flow, 10% two_col/cards, 10% worked/chart/decision, 10% big/bullets.
- Port the old deck's real teaching content (reference/old-ppt-v8-content.txt) —
  definitions, key terms, worked subnetting examples, scenario walk-throughs —
  updated to N10-009 terminology.
- Character limits above are HARD limits (the renderer truncates with an
  ellipsis; a truncated caption is a QA failure).
