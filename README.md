# CIE A-Level Economics — Claude Code skills

Custom Claude Code skills for teaching and assessment of **Cambridge International AS & A-Level Economics (9708)** and **Cambridge IGCSE Economics (0455)**.

| Skill | What it does | Trigger |
|---|---|---|
| [`cie-econ-essay`](./cie-econ-essay) | Marks essays/data-response answers against CIE level descriptors; writes A*-grade sample answers with inline SVG diagrams; supports handwritten/timed mode | message starts with **`cie:`** |
| [`cie-econ-ppt`](./cie-econ-ppt) | Builds full `.pptx` chapter decks combining definitions, real-world case studies (classic + recent), and matplotlib-rendered econ diagrams (D/S, AD-AS, cost curves, externalities, tariffs, etc.) | message starts with **`cie ppt:`** |

Both skills are **opt-in by prefix** — they won't fire on generic economics prompts.

---

## Install on a new machine

### 1. Prerequisites

- **Claude Code** v2.1.51+ ([install guide](https://docs.claude.com/en/docs/claude-code/setup))
- **Python 3.10+** (only required for `cie-econ-ppt`)
- **git** (to clone this repo)

### 2. One-command install

**Windows (PowerShell):**

```powershell
git clone https://github.com/CooperWu-star/A-Level-Econ-Marking-Sample.git
cd A-Level-Econ-Marking-Sample
./install.ps1
```

**macOS / Linux (bash):**

```bash
git clone https://github.com/CooperWu-star/A-Level-Econ-Marking-Sample.git
cd A-Level-Econ-Marking-Sample
bash install.sh
```

The installer:

1. Copies both skill folders into `~/.claude/skills/` (the standard user-skill location Claude Code reads on startup).
2. Installs the Python packages `cie-econ-ppt` needs (`python-pptx`, `matplotlib`, `pypdf`, `scipy`) into your user site-packages.
3. Prints the next steps.

### 3. Verify

Restart Claude Code, then in any session type:

```
cie: write me a 12-mark sample answer on price elasticity
```

or:

```
cie ppt: A-Level Topic 2.1 Demand and supply
```

If the skill fires, you're done. If nothing happens, run `/skills` (or check `~/.claude/skills/` exists and contains both folders).

---

## Updating

To pull the latest version of both skills onto a machine where you've already installed:

```
cd A-Level-Econ-Marking-Sample
git pull
./install.ps1     # or: bash install.sh
```

The installer is idempotent — it overwrites the skill folders cleanly.

---

## Notes

- The `cie-econ-ppt` skill writes `.pptx` files to the user's Desktop by default. On OneDrive-synced Windows machines, this is `C:\Users\<you>\OneDrive\Desktop\`, not `C:\Users\<you>\Desktop\`.
- `cie-econ-ppt/references/igcse-syllabus.md` is currently a provisional structure. Replace it with the full IGCSE 0455 syllabus extract when you have it.
- To extend the diagram library, add a function + registry entry in `cie-econ-ppt/scripts/diagrams.py`, then update `cie-econ-ppt/references/diagram-catalog.md` so the skill knows the new `diagram_id` exists.
