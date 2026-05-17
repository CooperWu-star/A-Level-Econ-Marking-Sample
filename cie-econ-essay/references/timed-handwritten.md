# Handwritten & Timed-Conditions Mode

This reference governs how the skill behaves when (a) the student submits a *handwritten* answer as an image, or (b) the user asks for a sample answer that is *realistic for timed exam conditions*.

It exists because the default "polished typed essay" the skill produces is too long, too neatly structured, and uses diagrams (inline SVG) that a real student cannot reproduce by hand in 15 minutes. A student who is shown a 600-word SVG-illustrated essay as the "A* target" comes away with the wrong calibration — they think their handwritten 350-word effort with a rough D-S diagram is L2, when in fact it could be L4. We want the sample answers to match what an A* student *actually writes* in the exam, not what a typed reproduction looks like.

## When this mode applies

Activate handwritten/timed mode when **any** of the following is true:

1. The user attaches an image of handwritten work — automatically infer this from the image content.
2. The user's prompt includes the word **"timed"**, **"handwritten"**, **"exam conditions"**, **"under timed conditions"**, or **"by hand"**.
3. The user's prompt asks for a "realistic" answer rather than a "model" or "polished" answer.

Otherwise use the default typed-essay mode described in the main SKILL.md.

## Part A — Marking a handwritten answer (image input)

When the input is a photo or scan of handwriting, follow this exact workflow.

### Step 1: Transcribe verbatim

Before doing anything else, produce a clean typed transcription of what the student wrote. This serves two purposes: it gives the student a record of what was legible, and it gives the marker (you) a clean text to work with.

Output format:

```
## Transcription
[Full transcription, line breaks roughly preserved. Use [illegible] for words/phrases that can't be made out. Use [unclear: best guess?] when partly readable. Preserve the student's wording, spelling, and any obvious errors — do NOT silently correct them, because spelling/terminology errors lose AO1 marks.]
```

### Step 2: Assess hand-drawn diagrams separately

Diagrams are a common mark-loss area in handwritten exams because labels go missing under time pressure. Add a dedicated diagram assessment block:

```
## Diagram assessment
- **Diagram present:** Yes / No / Partial
- **Type:** [e.g. AD-AS, Demand-Supply, Externality]
- **Axes labelled:** Yes / No — [list missing labels]
- **Curves labelled:** Yes / No — [list missing labels]
- **Shifts shown:** Yes / No — [is direction clear?]
- **Equilibrium points marked:** Yes / No
- **Integration with prose:** Does the essay reference the diagram (e.g. "as shown in Figure 1")? Yes / No
- **Mark impact:** [How many marks lost from the diagram, and which AO]
```

If key labels are missing (e.g. axes unlabelled), say so explicitly — examiners frequently cap diagram marks at half when axes are unlabelled. Be specific.

### Step 3: Estimate writing time

Roughly estimate how long the answer would have taken to write at typical handwriting speed (~20–25 words per minute under exam pressure for most students). Flag any of these red flags:

- **Answer appears rushed** (deteriorating handwriting, missing conclusion, partial diagram) → student likely ran out of time. Recommend better time management on the plan stage.
- **Answer is too long for the time available** (>500 words for a 12-marker = ~25 min, leaving too little for other questions) → recommend tighter planning.
- **Answer appears complete and well-paced** → no flag.

Output:

```
## Time estimate
Approximate writing time: [N] minutes. [Assessment: rushed / well-paced / over-long.] [Brief recommendation.]
```

### Step 4: Apply the standard marking framework

After Steps 1–3, apply the same marking output structure described in the main SKILL.md (Level / Why / AO breakdown / Strengths / Weaknesses / Targeted rewrite). Two adjustments for handwritten work:

- **AO1 penalty for illegibility of key terms:** If a key economic term is illegible or clearly misspelled in a way that obscures meaning ("ellasticity" is fine, "elasticy" loses an AO1 mark when it's the central concept), state this in the AO1 line. Examiners cannot award marks for terms they cannot read.
- **Targeted rewrite is hand-realistic:** The rewrite paragraph you provide should be one a real student could write by hand in the time available — not a polished 150-word paragraph the student couldn't reproduce. Aim for ~60–100 words for the rewrite paragraph, in the same style and tempo as the student's own writing.

## Part B — Writing a sample answer for timed handwritten conditions

When asked for a sample answer "under timed conditions" / "by hand" / "realistic for the exam", switch to timed mode. The structure is the same (plan + essay + examiner notes) but the parameters change.

### Target word counts (handwritten, realistic)

| Question | Time available | Realistic word count |
|---|---|---|
| AS 8-mark "Explain" | ~10 min | 150–200 words |
| AS 12-mark "Discuss" | ~15 min | 220–280 words |
| A2 8-mark "Explain" | ~10–12 min | 180–230 words |
| A2 12-mark "Discuss" | ~18–20 min | 320–400 words |
| Data response 6-mark | ~7–8 min | 100–140 words |

These are word counts of *prose only* — diagrams don't count. Do not produce 500+ word essays for a 12-marker in timed mode; that would be unrealistic and miscalibrates the student.

### Plan with timing breakdown

The plan must include a time allocation, because under exam conditions the plan IS the time-management tool. Use this exact format:

```
## Plan (writing time: ~15 min for AS 12-marker)
- 1 min: jot key definitions and identify command word
- 2 min: rough diagram sketch in margin
- 1 min: outline 3 paragraphs (analysis, analysis/alt, evaluation+conclusion)
- 10 min: write prose, integrating diagram
- 1 min: scan for missing definitions and a conditional conclusion
```

Adjust the minute allocation by question length.

### Diagrams — describe how to draw them by hand

In timed mode, do NOT use inline SVG. The student cannot reproduce SVG by hand. Instead, give a clear *drawing instruction* — terse, action-oriented — that the student can follow:

```
[Diagram to draw by hand:
- Axes: vertical = Price (P), horizontal = Quantity (Q). Label both with arrows.
- Draw D as a downward-sloping line; label it D.
- Draw S₁ upward-sloping; label.
- Draw S₂ parallel and to the LEFT of S₁; label.
- Mark E₁ where S₁ meets D, drop dashed lines to P₁ and Q₁.
- Mark E₂ where S₂ meets D, drop dashed lines to P₂ and Q₂.
- Make sure P₂ > P₁ and Q₂ < Q₁ visually.
Time: ~2 min. Don't shade anything unless the question demands it.]
```

The drawing instruction must be doable in 2–3 minutes, with no shading or complex annotation unless the question explicitly requires welfare areas (DWL, tax revenue).

### Realistic shortcuts in prose

A real exam answer uses shortcuts. The sample should too — within reason. Acceptable handwriting-era shortcuts:

- **Arrows for direction:** "AD↑ → PL↑, Y↑" is fine in an analysis chain. Don't over-do it (a full paragraph of arrows reads as bullet-point thinking, which examiners penalise) — use them only in the causal chain itself, not in the conclusion.
- **Abbreviations after first use:** "marginal propensity to consume (MPC)" → then "MPC" thereafter. Same for "PED", "AD", "AS", "LRAS", "BoP", "ToT".
- **Numbered evaluation points:** "(1) Magnitude — ... (2) Time horizon — ..." is acceptable shorthand for "Firstly... Secondly..." and saves seconds.
- **Skip the textbook flourish:** No need for "throughout history, economists have debated..." opening lines. Definitions first sentence, then straight into the mechanism.

What is *not* acceptable, even under time pressure:
- Bullet-list essays (examiners want connected prose).
- Skipping definitions of the key term in the question.
- Skipping the diagram for a question that says "using a diagram".
- A conclusion that is a single sentence with no conditional judgement.

### Fewer evaluation dimensions

The polished sample answer evaluates by 3 dimensions (magnitude, time, assumption, context, counter-factor). In timed mode, **2 well-developed dimensions** is the realistic A* target. Trying for 3+ leads to shallow points. Pick the two strongest evaluation dimensions for this specific question and develop them.

### Examiner notes — same structure, shorter

The examiner notes at the end still explain why the answer scores A*, but should be 3–4 bullets rather than 6, and should explicitly mention the time-realism: "This answer is achievable in 15 minutes by hand because…"

## Worked tempo example

For an AS 12-marker (15 minutes total):

- 0:00–1:00 — Read question twice, jot key terms and command word at top of page.
- 1:00–3:00 — Sketch the diagram in the margin, labelling axes and shift.
- 3:00–4:00 — Outline three paragraphs in the margin.
- 4:00–13:00 — Write prose. Reference the diagram once. Hit two evaluation dimensions.
- 13:00–14:00 — Write conclusion with a conditional judgement.
- 14:00–15:00 — Scan for missing definitions, missing diagram labels, missing conclusion. Fix the most damaging gap.

If you reach 13:00 without a conclusion, **stop the current paragraph and write the conclusion** — a missing conclusion loses more than an incomplete paragraph.

## What to tell the student

When delivering a timed-mode sample, prefix the answer with one sentence that frames it correctly:

> "This is a realistic A*-level handwritten answer at ~270 words and one diagram, achievable in 15 minutes. The polished 480-word typed version with two SVG diagrams is a different target — useful for understanding the *content* of an A* answer, but not what you should aim to reproduce in the exam itself."

This prevents miscalibration. Students who see only the polished version often write twice as much as they need and run out of time.
