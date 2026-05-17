---
name: cie-econ-ppt
description: Builds teaching PowerPoint decks (.pptx) for CIE A-Level Economics (9708) and Cambridge IGCSE Economics (0455), chapter by chapter. Every deck combines (1) clear definitions of key terms, (2) one classic + one recent real-world case study per concept, and (3) properly-drawn economic model diagrams (D/S, PPC, AD-AS, cost curves, market structures, externalities, tariffs, exchange rates, etc.) rendered as matplotlib PNGs and embedded in slides via python-pptx. Output is a real, openable .pptx file styled in a consistent academy theme — not just slide notes. STRICT TRIGGER RULE — only invoke this skill when the user's message begins with the prefix "cie ppt:" (case-insensitive) OR when the user explicitly says "use the CIE PPT skill" / "use my CIE econ PPT skill" / "use the econ slides skill". Do NOT invoke this skill for any other prompt, even if it concerns Economics, slide decks, lesson planning, or A-Level/IGCSE material — the owner runs an education business and wants explicit, opt-in control over when slide generation runs. If the prefix or explicit invocation phrase is absent, ignore this skill entirely and let Claude answer normally.
---

# CIE A-Level / IGCSE Economics — Slide Deck Builder

This skill generates teaching slide decks (.pptx) for chapters of:

- **Cambridge International AS & A-Level Economics 9708** (2026–2028 syllabus)
- **Cambridge IGCSE Economics 0455** (provisional structure; replace `references/igcse-syllabus.md` when the owner uploads the full syllabus)

Every deck has the same DNA: **definitions → case studies → model diagrams → recap**. The skill is designed to produce a deck that a teacher can walk into a classroom with and use as-is.

## Trigger

Only run this skill when:

1. The user's message starts with `cie ppt:` (case-insensitive), e.g. *"cie ppt: A-Level Topic 2.1 Demand and supply"*, **or**
2. The user explicitly says "use the CIE PPT skill" / "use my CIE econ PPT skill" / "use the econ slides skill".

If neither condition holds, do nothing — let Claude answer normally. This is deliberate: the owner runs courses across multiple boards and doesn't want every "make me slides about supply and demand" prompt to fire this generator.

## What the user gives you

A chapter or topic identifier. Examples of valid inputs:

- `cie ppt: A-Level Topic 2.1 Demand and supply`
- `cie ppt: A-Level Chapter 7 Market structures`
- `cie ppt: AS macro — AD and AS`
- `cie ppt: IGCSE Chapter 4 government and macroeconomy`
- `cie ppt: 9708 topic 6.2 protectionism, 18 slides`
- `cie ppt: monopoly`  (you'll need to confirm A-Level Topic 7.6 vs IGCSE)

The user may add hints: a slide count, depth (AS vs A2), an audience (Year 12 vs Year 13), or a focus ("more cases, fewer derivations"). Honour these.

If the topic is ambiguous between A-Level and IGCSE, ask **one** clarifying question, then proceed. Don't ask multiple rounds of questions.

## What you produce

A real `.pptx` file written to disk. Default output path is the user's Desktop, named `<course>-<topic-slug>.pptx`. Important: on Windows machines where OneDrive sync is enabled, the Desktop lives at `C:\Users\<user>\OneDrive\Desktop\`, not the plain `C:\Users\<user>\Desktop\` (which won't exist). Detect this by checking both paths; use whichever exists. Fall back to the current working directory if neither exists, and always tell the user the exact path you wrote to.

The deck must contain, in order:

1. **Title slide** — course, chapter, subtitle (e.g. "AS Level | Microeconomics").
2. **Topic-overview slide** — what this chapter covers and where it fits in the syllabus.
3. **A run of concept blocks**, each typically: a *definition* slide, then any number of *content* slides explaining mechanism, then a *diagram* slide, then a *case study* slide. Use as many or as few slides per concept as the concept needs — short concepts get one slide, big ones (e.g. monopoly long-run equilibrium) get four or five.
4. **A recap / "you should now be able to…" slide** at the end.

There is no hard slide count. A typical Topic 2.x deck lands at 18–28 content slides; a fat chapter like Topic 7 may be 35+.

## Workflow

### Step 1 — Identify course and chapter

Parse the user's input. Decide:

- **Course**: A-Level (9708) or IGCSE (0455)?
- **Chapter / topic number**: map free-text like "demand and supply" to a numbered topic. If you can't pin it down with confidence, ask.

### Step 2 — Load the scope

Read the relevant syllabus reference file to get the **authoritative list of sub-points** the deck must cover:

- A-Level → `references/syllabus-a-level.md`
- IGCSE → `references/igcse-syllabus.md` (currently a provisional structure; if the topic isn't there, fall back to your own knowledge of IGCSE 0455 and flag this in speaker notes)

Find the topic and copy its sub-points into your working memory. **Every sub-point must be covered by at least one slide.** If the syllabus lists six sub-points under 2.1, you should be able to point to six slides (or six bullets across a handful of slides) that map onto them.

### Step 3 — Pull case studies

Read `references/case-study-bank.md` and pick the cases that match the topic — one *classic*, one *recent* per major concept (you can use the same case twice if it genuinely illustrates two concepts). If the bank doesn't cover the concept, generate fresh cases using your own knowledge but keep to the same shape: a real, famous, fact-checkable event with a short "theory link" line.

Do not invent specific statistics. If you're not sure of a number, describe direction ("roughly doubled", "fell sharply") rather than fabricating a precise figure.

### Step 4 — Pick diagrams

Read `references/diagram-catalog.md`. For each concept in your scope that benefits from a diagram, choose the matching `diagram_id`. **Only use IDs that exist in the catalog** — they map to functions in `scripts/diagrams.py`. If a concept needs a diagram that isn't in the catalog, use a `content` slide instead and add `TODO_DIAGRAM: <description>` to the speaker notes; the user will extend the library later.

### Step 5 — Build the JSON spec

Construct a Python `dict` matching the schema in `scripts/build_deck.py` (the docstring at the top shows the full contract). Concretely, each slide is one of these `type`s:

- `title` — opening slide. Use once, at the top.
- `definition` — for *the* canonical statement of a key term. Use sparingly: one definition slide per genuinely new term. Bundle related minor terms onto a `content` slide.
- `content` — explanatory body: mechanism, determinants, lists, derivations.
- `diagram` — left half is the diagram image, right half is caption + bullets.
- `case_study` — `era` is "Classic" or "Recent"; renders a coloured chip and a "Theory link" band.
- `summary` — closing recap; use once, at the end.

### Step 6 — Hand the spec to `build_deck.py`

Write the spec to a temp JSON file, then call:

```
python scripts/build_deck.py <spec.json> <out.pptx>
```

Use the user's Python interpreter. To find it, try in this order:

1. Check memory for a saved Python path note (e.g. `python_setup` memory entry).
2. Run `python --version` / `python3 --version` / `py -3 --version` in the user's shell. The first that returns a real version (NOT the Windows Store placeholder error) is the interpreter to use.
3. On Windows, also check `C:\Users\<user>\AppData\Local\Programs\Python\Python3*\python.exe`.
4. If none work, tell the user: "I need Python 3.10+ with `python-pptx` and `matplotlib`. Run `./install.ps1` (or `install.sh`) from the cloned A-Level-Econ-Marking-Sample repo to set it up, then retry."

Save the discovered path to memory the first time you find it on a new machine, so future runs are instant.

If the call fails, read the traceback and fix the spec. Common pitfalls:

- Using a `diagram_id` that doesn't exist (typos like `demand_supply_right` instead of `demand_supply_demand_right`).
- Putting `bullets` as a single string instead of a list.
- Forgetting that `slides` must be a list, not a dict.

### Step 7 — Report

Tell the user:

- the exact path of the .pptx
- the slide count and rough breakdown (e.g. "26 slides: 1 title, 5 definitions, 8 content, 7 diagrams, 4 case studies, 1 recap")
- any `TODO_DIAGRAM` placeholders you left, so they know what's missing
- any syllabus sub-points you intentionally trimmed (e.g. AS-only material in an A2 chapter)

## Slide design rules — read this carefully

These rules are baked into `build_deck.py`'s layouts, but you control the *content*, which is what decides whether the deck is teachable. Apply them as you draft the spec.

**One concept per slide.** Resist the urge to cram. If a slide has a definition *and* a diagram *and* three bullets *and* a case study, it's three slides.

**Bullets are sentences with the verb removed.** "Effective demand requires willingness and ability to pay" → "Willingness *and* ability to pay (not just want)". Keep each bullet under ~14 words. Aim for 3–5 bullets per slide; never more than 6.

**Diagrams must be load-bearing.** Don't add a diagram for decoration. A diagram slide should have a caption that names the mechanism and bullets that walk through what happens at the labelled points. If the only thing you'd say about the diagram is "here is supply and demand", use a `content` slide instead.

**Case studies must link to theory.** Always fill `link_to_theory` with the specific mechanism the case illustrates (e.g. *"Leftward shift in S with low PED → sharp price rise, small Q fall"*). This is what makes the case examinable — without the link it's just a news headline.

**Speaker notes.** Add `notes` to every diagram and case slide. Notes are where you put: the things the teacher should say out loud but that shouldn't crowd the slide, follow-up questions to ask students, or 1-line context the teacher might forget.

**Definitions in CIE language.** When a CIE definition exists in the syllabus or examiner reports, use it verbatim or near-verbatim. Do not paraphrase canonical definitions into something looser — "willingness *and* ability to pay" is examinable phrasing.

**Don't over-explain at A2 if AS is assumed.** A2 decks should not re-derive AS material. Reference it (`Prerequisite — Topic 4.3 AD-AS`) and move on. The syllabus says "AS Level content is assumed knowledge for A Level Paper 3 and Paper 4" — respect that.

## Course-specific calibration

| | A-Level (9708) | IGCSE (0455) |
|---|---|---|
| Vocab | Use full CIE terms (ceteris paribus, MES, PED) | Plain-language; gloss any jargon |
| Derivations | Welcome (MR=MC, X-MES) | Avoid; give intuition |
| Diagrams | Full library available | Stick to D/S, PPC, AD-AS (basic), circular flow (2-sector), tariff |
| A2 material | Yes (Topics 7–11) only if user asks for A2 | Never |
| Slides per chapter | 20–35 | 10–18 |

When the user says "AS" or "A2" explicitly, lock to that. Don't put A2 indifference-curve content in an AS deck.

## A worked example

User: `cie ppt: A-Level Topic 2.1 Demand and supply, 22 slides`

Your spec, in outline (not literal Python, just the shape):

1. `title` — "Topic 2.1 — Demand and supply curves", subtitle "CIE A-Level Economics 9708 · AS Microeconomics"
2. `content` "What this topic covers" — bullets are the sub-point list from the syllabus
3. `definition` "Effective demand" — term + CIE definition + 3 key-point bullets
4. `content` "Determinants of demand" — PASIFIC or similar, 5 bullets
5. `diagram` "Demand curve" — `demand_supply` with the supply curve hidden? — no, use a `content` slide with bullets ("downward sloping because…")
6. `definition` "Supply"
7. `content` "Determinants of supply"
8. `diagram` "Equilibrium" — `demand_supply` — caption "P\* and Q\* clear the market"
9. `content` "Shift vs movement along" — explain the distinction
10. `diagram` "Rightward shift in demand" — `demand_supply_demand_right`
11. `diagram` "Leftward shift in supply" — `demand_supply_supply_left`
12. `case_study` Classic — OPEC 1973 oil shock, era "Classic"
13. `case_study` Recent — 2022 egg price spike, era "Recent"
14. `content` "Functions of price" — rationing, signalling, incentivising
15. `summary` — 5 "you should now be able to…" bullets mapping back to the syllabus sub-points

That's 15 slides, not 22 — so add more granularity: split the "determinants of demand" slide into two, add a worked numerical example slide, add a "common exam pitfalls" slide. Land at 22.

## Files in this skill

```
cie-econ-ppt/
├── SKILL.md                          (you are here)
├── references/
│   ├── syllabus-a-level.md           (authoritative topic list for 9708, 2026–28)
│   ├── igcse-syllabus.md             (provisional IGCSE 0455 structure)
│   ├── diagram-catalog.md            (which diagram_id renders what)
│   └── case-study-bank.md            (classic + recent cases, ready to drop in)
└── scripts/
    ├── diagrams.py                   (matplotlib econ diagram library)
    └── build_deck.py                 (JSON spec → .pptx, full layout engine)
```

## Common failures to avoid

- **Generating slide text without building the .pptx.** The user asked for slides — produce the file. Don't leave it as markdown.
- **Inventing case-study statistics.** If a number isn't widely known, describe the direction.
- **Skipping syllabus sub-points.** The user will check the deck against the syllabus. Cover every sub-point or explicitly flag what you trimmed and why.
- **Using diagram IDs that don't exist.** The build will crash. Stick to `references/diagram-catalog.md`.
- **Putting everything on one dense slide.** This is a teaching deck, not a textbook page. Let it breathe.
- **Skipping speaker notes on diagrams.** A diagram slide without notes is a slide the teacher has to think on their feet for. Don't do that to them.
