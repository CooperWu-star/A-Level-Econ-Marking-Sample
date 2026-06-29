# Design system — how to make the deck look professional

`build_deck.py` bakes in a design system ported from the **ppt-master** skill.
You don't write any styling — you choose a **palette**, pick the right **slide
type** per idea, and sequence them with **page rhythm**. The engine handles
colour proportion, the locked type scale, spacing, flat-card discipline and
restraint. This file tells you how to drive it well.

---

## 1. Palette — set once, top-level `"palette"`

One palette per deck. Default is `academy`. Each is a coordinated role set
(background / surface / primary / accent / ink / muted) following the 60-30-10
rule, so you never pick colours by hand.

| `palette` | Feel | Good for |
|---|---|---|
| `academy` *(default)* | Navy + warm orange, clean | House style; any topic |
| `cool-corporate` | Navy + gold, restrained | Macro / policy / finance topics |
| `editorial-classic` | Cream + serif headings + burnt orange | "Magazine" feel; essay-skills decks |
| `warm-earth` | Cream + terracotta | Development, labour, inequality |
| `nature-organic` | Forest green + amber | Environment, sustainability (9.2), agriculture |
| `mono-ink` | Black + one orange accent | High-contrast, minimalist revision decks |
| `dark-cinematic` | Deep navy + teal + gold | Projected-in-a-dark-room showcase decks |

The deck accent automatically re-tints the **"new / shifted" curve** in diagrams
(e.g. the orange D₁ on a D/S shift) so diagrams match the deck — handled for you.

---

## 2. Locked type scale — do NOT fight it

Every structural role has ONE size, reused on every slide (same-role size drift
is the #1 "AI deck" tell). The engine owns these; your job is just to keep text
to the right length:

- **Bullets**: 3–5 per slide, never more than 6. A bullet is either a short cue (plain string) OR a teaching bullet `{"point": "...", "detail": "..."}` — point short, detail one clause that explains the mechanism. On teaching slides prefer the `{point, detail}` form; don't ship bare keyword lists.
- **Definition**: one or two sentences — it sits in a quoted card.
- **Lead/intro line**: one sentence framing the slide.
- **Stat value**: a few characters (`2.1m`, `£0`), not a sentence — and only a **sourced or direction-safe** figure (don't fabricate a precise number; see SKILL.md).

If a slide's text won't fit those limits, it's **two slides**.

---

## 3. Slide types — pick the one that fits the idea

| `type` | Use it for | Key fields |
|---|---|---|
| `title` | Opening slide (once) | `title`, `subtitle` |
| `section` | Divider before a new concept block | `number`, `title`, `subtitle` |
| `definition` | THE canonical statement of one key term | `term`, `definition`, `bullets` |
| `content` | Mechanism, determinants, lists, derivations | `title`, `intro`, `bullets` |
| `diagram` | A load-bearing diagram + walkthrough | `diagram_id`, `caption`, `bullets` |
| `diagram_pair` | TWO diagrams side by side (visual contrast) | `left{diagram_id,caption}`, `right{diagram_id,caption}` |
| `case_study` | One real, fact-checkable event + theory link | `era`, `summary`, `bullets`, `link_to_theory` |
| `compare` | Two things contrasted side by side (text) | `left{head,bullets}`, `right{head,bullets}` |
| `stat` | One striking number that carries a point | `value`, `label`, `caption` |
| `quote` | A pull-quote / framing line | `text`, `attribution` |
| `summary` | "You should now be able to…" recap (once, last) | `bullets` |

`section`, `stat` and `quote` are the **breathing** slides — they punctuate the
dense content runs so the deck doesn't read as bullets-on-every-page.

---

## 4. Page rhythm — the anti-"AI deck" rule

A run of identical bullet slides is what makes a deck look machine-made.
Interleave **breathing** slides between **dense** ones:

- Open each concept block with a `section` divider (breathing).
- Carry the teaching in `definition` / `content` / `diagram` slides (dense).
- Punctuate with a `stat` or `quote` (breathing) where a number or line lands hard.
- A `compare` slide is the natural home for "movement vs shift", "AS vs A2",
  "monopoly vs perfect competition", "fiscal vs monetary".

Rough target for a 20-slide topic deck: ~3–4 breathing slides spread through it,
not clustered. Don't put two `section` dividers back to back.

---

## 5. "AI deck tells" to avoid (carried over from ppt-master)

1. **Every slide is a title bar + bullets.** Vary the type; use the breathing slides.
2. **Walls of uniform text.** Keep bullets short; lift the load-bearing noun, not the connective.
3. **A diagram that only says "here is supply and demand".** A `diagram` slide must walk through what happens at the labelled points — otherwise make it `content`.
4. **A case study with no theory link.** Always fill `link_to_theory`.
5. **Cramming.** One concept per slide. Let it breathe.
6. **Decoration diagrams / clip-art.** Diagrams are load-bearing only.

---

## 6. Worked example (shape of a good spec)

```json
{
  "course": "CIE A-Level Economics 9708",
  "chapter": "Topic 2.1 — Demand and supply curves",
  "subtitle": "AS Level · Microeconomics",
  "footer": "Aixiom Academy",
  "palette": "academy",
  "kicker": "9708 · 2.1 · Coursebook Unit 2, Ch 7",
  "slides": [
    {"type":"title","title":"Demand & Supply Curves","subtitle":"AS Micro · Theme 2 · Coursebook Ch 7"},
    {"type":"section","number":"1","title":"How markets set a price"},
    {"type":"definition","term":"Effective demand","definition":"Willingness AND ability to pay…","bullets":["…","…"]},
    {"type":"content","title":"Determinants of demand","intro":"A non-price change shifts the whole curve.","bullets":["Income","Substitutes & complements","Tastes","…"]},
    {"type":"diagram","title":"Rightward shift in demand","diagram_id":"demand_supply_demand_right","caption":"Higher income raises demand at every price.","bullets":["D→D₁ at all prices","New P₁,Q₁","Excess demand pushes P up"]},
    {"type":"compare","title":"Movement vs shift","left":{"head":"Movement ALONG","bullets":["Own-price change","Contract/extend"]},"right":{"head":"SHIFT","bullets":["Non-price factor","Whole curve moves"]}},
    {"type":"case_study","title":"2022–24 egg price spike","era":"Recent","summary":"Avian flu cut supply…","bullets":["S shifts left","Eggs price-inelastic"],"link_to_theory":"Left shift in S + low PED → big ΔP, small ΔQ."},
    {"type":"stat","title":"Scale of the shock","value":"+60%","label":"US egg prices YoY","caption":"Low PED → price does the adjusting."},
    {"type":"summary","title":"Topic recap","bullets":["Define effective demand","Distinguish movement vs shift","Read the new equilibrium off a D/S diagram"]}
  ]
}
```
