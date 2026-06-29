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

Then read `references/coursebook-map.md` and look the topic up there. This is what keeps the deck **aligned with the textbook and the syllabus structure** the class is using:

- It gives the **coursebook unit + chapter** for the topic (the endorsed Bamford & Grant book lays out one chapter per syllabus topic, in order). Put that in the deck's `kicker` field and the title-slide subtitle, e.g. `9708 · 2.1 · Coursebook Unit 2, Ch 7`, so students can read along.
- **Sequence your slides in the textbook's order** — the chapter's internal `X.1, X.2 …` sections mirror the syllabus sub-points, which is the order both the book and the class follow.
- It also lists the **`diagram_id`s that fit each topic**, so Step 4 is mostly a lookup.

(A-Level only. IGCSE 0455 is a different qualification — use `igcse-syllabus.md` and your own knowledge there.)

### Step 3 — Pull case studies

Read `references/case-study-bank.md` and pick the cases that match the topic — one *classic*, one *recent* per major concept (you can use the same case twice if it genuinely illustrates two concepts). If the bank doesn't cover the concept, generate fresh cases using your own knowledge but keep to the same shape: a real, famous, fact-checkable event with a short "theory link" line.

Do not invent specific statistics. If you're not sure of a number, describe direction ("roughly doubled", "fell sharply") rather than fabricating a precise figure.

### Step 4 — Pick diagrams

The topic's row in `references/coursebook-map.md` already lists the `diagram_id`s that fit it — start there. For full detail (what each renders, typical use) read `references/diagram-catalog.md`. For each concept in your scope that benefits from a diagram, choose the matching `diagram_id`. **Only use IDs that exist in the catalog** — they map to functions in `scripts/diagrams.py`. If a concept needs a diagram that isn't in the catalog, use a `content` slide instead and add `TODO_DIAGRAM: <description>` to the speaker notes; the user will extend the library later.

### Step 5 — Build the JSON spec

**First read `references/design-system.md`** — it explains the palette, the locked type scale, the slide types, and page rhythm. The styling is all handled by the engine; your job is to pick the right slide type per idea and sequence them well.

Set two top-level fields the design system uses:

- `"palette"` — one of `academy` (default), `cool-corporate`, `editorial-classic`, `warm-earth`, `nature-organic`, `mono-ink`, `dark-cinematic`. Pick by topic feel (see design-system.md §1); when unsure, use `academy`.
- `"kicker"` — the syllabus + coursebook tag from Step 2, e.g. `9708 · 2.1 · Coursebook Unit 2, Ch 7`. Shown on every content slide.

Construct a Python `dict` matching the schema in `scripts/build_deck.py` (the docstring at the top shows the full contract). Each slide is one of these `type`s:

- `title` — opening slide. Use once, at the top.
- `section` — a divider that opens a new concept block (big number + title on a near-empty field). This is a **breathing** slide — use it to break up the deck.
- `definition` — *the* canonical statement of one key term, in a quoted card. One per genuinely new term; bundle minor terms onto a `content` slide.
- `content` — explanatory body: mechanism, determinants, lists, derivations. Optional `intro` lead line.
- `diagram` — diagram in a card on the left, caption + walkthrough bullets on the right. Use one wherever a concept is visual.
- `diagram_pair` — **two diagrams side by side** (`left`/`right`, each `{diagram_id, caption}`). Use for visual contrasts: movement-vs-shift (`demand_movement` vs `demand_supply_demand_right`), monopoly-vs-perfect-competition, demand-pull-vs-cost-push.
- `case_study` — `era` is "Classic" or "Recent" (coloured chip); fill `summary`, `bullets`, and always `link_to_theory`.
- `compare` — two things side by side (`left`/`right`, each `{head, bullets}`). Use for movement-vs-shift, AS-vs-A2, monopoly-vs-perfect-competition, fiscal-vs-monetary.
- `stat` — one striking number (`value`) + `label` + `caption`. A **breathing** slide; use where a figure lands hard.
- `quote` — a pull-quote / framing line (`text`, `attribution`). A **breathing** slide.
- `summary` — closing "you should now be able to…" recap; use once, at the end.

**Page rhythm (important):** open each concept block with a `section`, carry the teaching in `definition`/`content`/`diagram`, and punctuate with a `stat`, `quote` or `compare`. Don't produce a run of identical bullet slides — that is the #1 "AI deck" tell. Aim for ~3–4 breathing slides spread through a 20-slide deck.

**Teach, don't just list (important).** A bullet may be a plain string (a short cue) OR a `{"point": "...", "detail": "..."}` object that *explains* it. On teaching slides use the object form — the `point` is the term (kept short, bolded) and the `detail` is the one-line explanation of the mechanism. A slide that is only keywords (`Income`, `Substitutes`, `Tastes`) is a revision aid, not a lesson; write `{"point":"Income","detail":"normal good → D shifts right as income rises; inferior good → D shifts left."}` instead. Keep the detail to one clause (~one line).

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
- the palette used and the coursebook chapter the deck follows (e.g. "academy palette · aligned to Coursebook Unit 2, Ch 7")
- any `TODO_DIAGRAM` placeholders you left, so they know what's missing
- any syllabus sub-points you intentionally trimmed (e.g. AS-only material in an A2 chapter)

## Slide design rules — read this carefully

These rules are baked into `build_deck.py`'s layouts, but you control the *content*, which is what decides whether the deck is teachable. Apply them as you draft the spec.

**Cover the whole topic — including both halves.** Before you finalise, list the topic's syllabus sub-points (from `syllabus-a-level.md`) and tick each one off against a slide. A topic titled "X **and** Y" (Demand **and** supply, Costs **and** revenue, Monopoly **and** perfect competition) must give **both** roughly equal treatment — it is a common failure to teach X thoroughly and leave Y as an afterthought. For Topic 2.1 that means: effective *demand* AND *supply* defined; determinants of *demand* AND of *supply*; shift in *D* AND in *S*; plus equilibrium and the movement/shift distinction. If you drop a sub-point on purpose, say so in Step 7.

**Frame policy topics as Definition → Mechanism → Evaluation.** For any *policy* topic (5.1–5.4 fiscal/monetary/supply-side, 8.1 micro intervention, 10.3 policy effectiveness, 11.1 BoP policies — anything where the answer is "use policy X"), teach each policy in the three beats a strong exam answer uses:
1. **① Definition** — what the policy is and its tools (AO1). The lead `definition` slide; supporting `content` slides (budget, taxation, spending, etc.) elaborate the tools under this beat.
2. **② Mechanism** — the chain of reasoning drawn on a diagram (AD/AS, money market, PPC) through to the macro objectives (AO2/AO3). The `diagram`/`diagram_pair` slides. The *reasons to tax and to spend are themselves mechanisms* (each is a channel — "manage AD" is macro, "redistribute"/"correct market failure" are micro) — give them their own detailed slides, not one throwaway bullet. For fiscal, also cover **automatic stabilisers vs discretionary policy**.
3. **③ Evaluation** — a dedicated slide (split into two if it runs past ~5 bullets) that weighs **strengths → limitations → judgement** (AO3/AO4): time lags, crowding out, the zero lower bound, magnitude/multiplier, cost, **expectations/confidence** (agents may *save* a tax cut rather than spend it, shrinking the multiplier), **disincentive & cost-push effects** of high tax rates (wage claims → higher firm costs), and *the state of the economy* ("it depends on the output gap"), ending on a reasoned judgement. This is the beat that separates grades and is the one most often missing — **never ship a policy block without it.**
Signpost the beats: put `① Define → ② Mechanism → ③ Evaluate` in the `section` subtitle, and prefix the lead slide of each beat (`① Definition — …`, `② Mechanism — …`, `③ Evaluation — …`). Add an early `content` slide teaching this skeleton so students internalise the exam structure.

**One concept per slide.** Resist the urge to cram. If a slide has a definition *and* a diagram *and* three bullets *and* a case study, it's three slides.

**Explain, don't list.** Keep the *point* short, but add the *detail* that teaches the mechanism (use the `{point, detail}` bullet form — see "Teach, don't just list" above). A wall of bare nouns is a revision flashcard, not a lesson. Aim for 3–5 bullets per slide; never more than 6. Where the explanation is for the teacher to say aloud rather than show, put it in `notes`.

**Diagrams must be load-bearing — and use them generously.** Wherever a concept is inherently visual (a curve, a shift, a movement, an equilibrium, surplus, a tax wedge), show the diagram — don't describe it in words. A diagram slide needs a caption that names the mechanism and bullets that walk through what happens at the labelled points. For a *contrast* between two diagrams (movement vs shift, monopoly vs perfect competition), use a `diagram_pair` slide so the student sees them together. If the only thing you'd say is "here is supply and demand", use a `content` slide instead.

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

Top-level: `palette` "academy", `kicker` "9708 · 2.1 · Coursebook Unit 2, Ch 7" (from the coursebook map). Your spec, in outline (not literal Python, just the shape):

1. `title` — "Demand & Supply Curves", subtitle "AS Micro · Theme 2 · Coursebook Ch 7"
2. `section` №1 "How markets set a price" — *breathing*
3. `definition` "Effective demand" — CIE definition + 3 key-point bullets
4. `content` "Determinants of demand" — 5 bullets
5. `diagram` "The demand curve" — `demand_supply`, caption on why it slopes down
6. `definition` "Supply"
7. `content` "Determinants of supply"
8. `section` №2 "Equilibrium and change" — *breathing*
9. `diagram` "Market equilibrium" — `demand_supply`, caption "P* and Q* clear the market"
10. `compare` "Movement along vs shift" — the distinction, side by side
11. `diagram` "Rightward shift in demand" — `demand_supply_demand_right`
12. `diagram` "Leftward shift in supply" — `demand_supply_supply_left`
13. `case_study` Classic — OPEC 1973 oil shock, era "Classic"
14. `case_study` Recent — 2022 egg price spike, era "Recent"
15. `stat` "+60%" — US egg prices YoY — *breathing*, lands the low-PED point
16. `content` "Functions of price" — rationing, signalling, incentivising
17. `summary` — "you should now be able to…" mapping back to the 7 sub-points of 2.1

That's 17; to reach 22 add granularity (split determinants into two, a worked PED-numerical `content`, a "common exam pitfalls" `content`, a `quote` on the functions of price). Note the rhythm: `section`/`stat`/`quote`/`compare` break up the bullet runs so it never reads as an "AI deck".

## Files in this skill

```
cie-econ-ppt/
├── SKILL.md                          (you are here)
├── references/
│   ├── syllabus-a-level.md           (authoritative topic list for 9708, 2026–28)
│   ├── coursebook-map.md             (syllabus topic ↔ Bamford & Grant chapter + diagrams)
│   ├── design-system.md              (palettes, type scale, slide types, page rhythm)
│   ├── igcse-syllabus.md             (provisional IGCSE 0455 structure)
│   ├── diagram-catalog.md            (which diagram_id renders what)
│   └── case-study-bank.md            (classic + recent cases, ready to drop in)
└── scripts/
    ├── diagrams.py                   (matplotlib econ diagram library, palette-aware)
    └── build_deck.py                 (JSON spec → .pptx, full design-system layout engine)
```

## Common failures to avoid

- **Generating slide text without building the .pptx.** The user asked for slides — produce the file. Don't leave it as markdown.
- **Inventing case-study statistics.** If a number isn't widely known, describe the direction.
- **Skipping syllabus sub-points.** The user will check the deck against the syllabus. Cover every sub-point or explicitly flag what you trimmed and why.
- **Using diagram IDs that don't exist.** The build will crash. Stick to `references/diagram-catalog.md`.
- **Putting everything on one dense slide.** This is a teaching deck, not a textbook page. Let it breathe.
- **Skipping speaker notes on diagrams.** A diagram slide without notes is a slide the teacher has to think on their feet for. Don't do that to them.
