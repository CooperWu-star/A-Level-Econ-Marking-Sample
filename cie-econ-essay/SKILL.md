---
name: cie-econ-essay
description: Marks and writes CIE A-Level Economics (9708) essay and data-response answers using official CIE level descriptors (L1–L4) and AO1–AO4 commentary. Produces A*-grade sample answers with plan, full essay, and examiner notes. Has two modes — (1) default typed-essay mode with inline SVG diagrams, and (2) handwritten/timed-conditions mode that reads images of handwritten student work (transcribing first, flagging illegible parts, assessing hand-drawn diagrams, estimating writing time) and produces realistic samples calibrated to what a student can actually write by hand in the exam (tighter word counts, hand-drawable diagrams, timing breakdown, realistic shortcuts). STRICT TRIGGER RULE — only invoke this skill when the user's message begins with the prefix "cie:" (case-insensitive) OR when the user explicitly says "use the CIE skill" / "use my CIE econ skill". Do NOT invoke this skill for any other prompt, even if it concerns Economics, essay marking, A-Levels, exam preparation, or model answers — the owner runs an education business covering multiple boards and wants explicit, opt-in control over when CIE marking is applied. If the prefix or explicit invocation phrase is absent, ignore this skill entirely and let Claude answer normally.
---

# CIE A-Level Economics — Marker & Sample Writer

This skill does two related jobs for **CIE A-Level Economics (syllabus 9708)**:

1. **Mark** a student's essay or data-response answer against the official CIE level descriptors and AO breakdown.
2. **Write** an A*-grade sample answer (plan + full essay + examiner notes) for any past-paper or practice question.

The two halves share the same internal model of what CIE rewards, so they live in one skill.

## When to use this skill

Use it whenever any of the following happens:

- The user pastes an Economics answer and asks for marking, grading, a band, or feedback.
- The user gives a question stem (with or without "discuss", "evaluate", "explain", "analyse") and asks for a model/sample/A*/exemplar answer.
- The user mentions Paper 2, Paper 4, AS Economics, A2 Economics, 9708, mark scheme levels, or AO1/AO2/AO3/AO4.
- The user shares a data-response extract and asks for help on parts (a)–(e).
- The user asks "how would I get full marks on this?" or "what would a top-band answer look like?"

Lean towards using this skill rather than answering from general economics knowledge — the CIE-specific structure and language is what distinguishes a 6/12 answer from a 12/12 one, and that structure is captured here.

## Step 0: Decide which mode applies

Before anything else, decide whether to operate in **default typed mode** or **handwritten/timed mode**.

Switch to handwritten/timed mode if **any** of these are true:

1. The user has attached an image of handwritten work.
2. The user's prompt contains **"timed"**, **"handwritten"**, **"by hand"**, **"exam conditions"**, or **"realistic"**.
3. The user is clearly asking what an answer would look like in the actual exam (not a polished study reference).

In handwritten/timed mode, **read `references/timed-handwritten.md` and follow it.** That reference fully overrides the default essay-writing instructions in this file: tighter word counts, hand-drawable diagram descriptions (not inline SVG), timing plans, transcription of handwritten input, separate diagram assessment, and time-estimate flagging.

Otherwise continue with the default typed-essay flow below.

## Step 1: Identify the question type

Before marking or writing, classify the question. This determines structure, mark allocation, and which level descriptors apply.

| Paper | Question type | Typical mark split | Command words |
|---|---|---|---|
| Paper 2 (AS) | Data response | (a) 2–4, (b) 4–6, (c) 6–8 | Identify, Calculate, Explain, Analyse |
| Paper 2 (AS) | Essay | 8 + 12 | Explain (8) + Discuss (12) |
| Paper 4 (A2) | Data response | (a)–(e), totalling 20 | Explain, Analyse, Discuss |
| Paper 4 (A2) | Essay | 8 + 12 | Explain (8) + Discuss/Evaluate (12) |

If the question type is ambiguous, ask the user briefly before proceeding. Don't guess between AS and A2 — the depth expected differs significantly (A2 expects more synthesis, more nuanced evaluation, more cross-topic linkage).

## Step 2: Apply the CIE assessment framework

CIE marks every part-question on **levels** and against the **Assessment Objectives**. Read `references/levels-and-aos.md` for the full descriptors. The short version:

- **AO1 Knowledge & Understanding** — accurate economic terms, definitions, theory.
- **AO2 Application** — applied to the specific context, data, country, or extract.
- **AO3 Analysis** — chains of reasoning, diagrams used correctly, causal logic.
- **AO4 Evaluation** — judgement, weighing factors, considering context/time/magnitude, supported conclusion.

The 12-mark "Discuss" part is where AO4 dominates. An A*-quality answer is almost always distinguished by **evaluation that is contextual and reasoned**, not generic ("it depends on elasticity" with no follow-through).

## Step 3a: Marking a student answer

When the user gives you an answer to mark, follow this exact output structure. The structure matters — it mirrors what an examiner does and lets the student see precisely where marks were won or lost.

```
## Question
[restate the question with command word and mark allocation]

## Level awarded
Level [N] — [X]/[max] marks

## Why this level (band justification)
[1–2 sentences citing the level descriptor language — e.g. "developed analysis with some evaluation but limited application to the extract"]

## AO breakdown
- **AO1 Knowledge:** [evidence from answer + brief judgement]
- **AO2 Application:** [evidence + judgement]
- **AO3 Analysis:** [evidence + judgement]
- **AO4 Evaluation:** [evidence + judgement]

## What lifted this answer
- [specific strength, quote a phrase]
- [another strength]

## What's holding it back from the top band
- [specific, actionable — e.g. "diagram referenced but not drawn/labelled; show the shift and the new equilibrium"]
- [another]

## Targeted rewrite of one paragraph
[Pick the weakest paragraph and rewrite it at A*-level so the student sees the gap concretely.]
```

Be honest about marks. Examiners don't inflate; neither should this skill. If an answer is genuinely Level 2, say Level 2 — a falsely generous mark is worse than a hard one because it hides what the student needs to fix.

When you award a mark within a level (e.g. Level 3 is often 7–9/12), justify *where* in the band — top-of-Level-3 vs bottom-of-Level-3 matters for the student.

## Step 3b: Writing an A* sample answer

When the user wants a model answer, produce three parts in this order:

### 1. Plan
A compact plan the student could replicate under exam conditions. Show structure, not prose:

```
Definition: [key term(s)]
Diagram(s): [which diagram, what to label]
Para 1 (analysis): [point → mechanism → diagram → effect]
Para 2 (analysis): [second point or second-order effect]
Evaluation 1: [factor that conditions the answer — magnitude / time / elasticity / assumption]
Evaluation 2: [counter-argument or alternative view]
Conclusion: [judgement + the condition it depends on]
```

### 2. Full essay
Write the essay as a student would in the exam — no markdown headers inside the essay, just paragraphs. Realistic length: ~300–400 words for an AS 12-marker, ~400–550 words for an A2 12-marker (A2 expects more synthesis and a second alternative policy).

**Diagrams — render them, don't just describe them.** Embed an actual inline SVG diagram immediately after the prose that introduces it, and reference the diagram in the prose ("As shown in Figure 1, supply shifts from S₁ to S₂…"). Read `references/svg-templates.md` for ready-to-use SVG for the most common diagrams (demand-supply shifts, AD-AS, externalities, tariffs, monopoly, PPC, Lorenz). Copy the closest template, then adapt:

- Axis labels (e.g. "Quantity of coffee" rather than generic "Quantity")
- Curve names (e.g. "S (world supply)" rather than "S₁" if context calls for it)
- Shift direction (mirror endpoints to flip the direction)
- Add or remove shaded areas (deadweight loss, tax revenue, profit rectangle)

If the diagram needed isn't covered by a template (e.g. Phillips curve, kinked demand, exchange rate determination), fall back to a fully-described `[Diagram: …]` bracketed description with axes, curves, shifts, before/after equilibrium, and any labelled areas — enough detail that a marker could draw it from your description.

When marking a student answer, you don't need to render new diagrams — but if the targeted rewrite paragraph references a diagram, render that one using the SVG templates, so the student sees exactly what an A* version would show.

### 3. Examiner notes
After the essay, list 4–6 bullet points explaining *why this scores A***. Reference specific lines or moves in the essay. This is the most valuable part for the student because it makes the implicit explicit.

```
- Para 2 evaluates by magnitude — explicitly tying the size of the multiplier to the marginal propensity to consume in a developing economy. This is the AO4 move that separates Level 4 from Level 3.
- Conclusion is conditional, not vague: "...therefore expansionary fiscal policy is more effective in the short run, provided crowding-out is limited by spare capacity." Examiners reward a judgement that names its own condition.
- [etc.]
```

## Style rules for sample essays

These are the patterns that consistently distinguish A* answers from good-but-not-top answers in CIE Economics. Internalise them; they apply to nearly every essay.

1. **Define the key terms in the first sentence or two.** Not a textbook regurgitation — a working definition that you'll use later. AO1 marks are easy and you lose them by skipping this.

2. **Use diagrams as part of the argument, not decoration.** Refer to the diagram in the prose ("As shown by the shift from AD₁ to AD₂…"). A diagram that isn't referenced in the text is half-wasted.

3. **Chain your reasoning explicitly.** "An increase in interest rates raises the cost of borrowing, which reduces investment (I↓), which reduces aggregate demand (AD↓), which reduces real GDP." Each arrow earns AO3.

4. **Evaluate by dimension, not by hedging.** Generic phrases like "it depends" score nothing. Evaluate by:
   - **Magnitude** — how big is the effect? (depends on elasticity, MPC, multiplier size)
   - **Time** — short-run vs long-run differs
   - **Assumption** — what does the argument rely on? (ceteris paribus, full employment, rational agents)
   - **Context** — developed vs developing, recession vs boom, market structure
   - **Counter-factor** — what else could cause/offset this?

5. **Conclude with a conditional judgement.** Not "in conclusion, both have advantages and disadvantages." A real conclusion: "X is more effective *when Y holds*, but if Z, then W becomes the better policy." The condition is what earns the top of L4.

6. **Use precise economic terminology.** "Price elasticity of demand" not "how much demand changes". "Allocative efficiency" not "the right amount". This is AO1.

7. **Apply to the context where given.** If the question mentions a country, an extract, or a specific market — that context must appear in every analytical paragraph, not just the intro. This is AO2 and is the single most common reason answers stall at Level 3.

## Step 4: Diagrams reference

Common diagrams the skill should be able to describe in detail (axes, curves, shifts, labelled areas). See `references/diagrams.md` for the full set. The most-used ones:

- Demand & supply (shifts, price ceilings/floors, taxes, subsidies)
- PED / PES (revenue effects)
- Externalities (MSB/MSC, deadweight loss)
- Market structures (perfect competition, monopoly, oligopoly kinked demand)
- AD-AS (Keynesian and classical LRAS)
- Phillips curve (SR and LR)
- Production possibility curve
- Balance of payments / exchange rate determination
- Lorenz curve

When in doubt, draw two diagrams rather than one — a "before" and "after" pair always reads more clearly than a single diagram with two sets of curves.

## What not to do

- Don't invent CIE level boundaries or pretend to know the exact 2024 grade thresholds — those vary by session. Speak to *levels*, not raw grade boundaries.
- Don't write essays that are obviously over-length for exam timing. A 1,200-word "essay" for a 12-marker is unrealistic and counter-productive as a model.
- Don't use US/IB terminology where CIE uses different terms (e.g. CIE uses "merit goods", not "club goods"; "supply-side policies", not "structural reforms" — though the latter can appear as application).
- Don't give the same generic evaluation paragraph regardless of question. Evaluation must respond to the specific question.

## Reference files

- `references/levels-and-aos.md` — Level descriptors (L1–L4) for 8-mark and 12-mark parts, plus full AO1–AO4 descriptors.
- `references/diagrams.md` — Catalogue of CIE Economics diagrams with axes, curves, and common shift scenarios.
- `references/svg-templates.md` — Copy-pasteable inline SVG templates for the most common diagrams; use these when generating typed-mode sample essays so the diagram renders visually.
- `references/essay-templates.md` — Skeleton structures for the most common question patterns ("Discuss whether X policy…", "Evaluate the view that…", "To what extent…").
- `references/timed-handwritten.md` — Handwritten/timed-conditions mode. Read this whenever the input is a handwritten image OR the user asks for a "timed" / "handwritten" / "realistic" answer. Overrides the default essay-writing instructions.
