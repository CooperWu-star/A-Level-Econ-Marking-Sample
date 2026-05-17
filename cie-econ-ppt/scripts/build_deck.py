"""Assemble a CIE Economics slide deck (.pptx) from a JSON spec.

Usage:
    python build_deck.py spec.json out.pptx
    python build_deck.py - out.pptx          # read spec from stdin

The spec is a JSON object with this shape (see spec_schema.md for the full
contract):

{
  "course": "CIE A-Level Economics 9708",          # or "IGCSE Economics 0455"
  "chapter": "Topic 2.1 — Demand and supply curves",
  "subtitle": "AS Level | Microeconomics",         # optional
  "footer": "Aixiom Academy",                       # optional, shown on every slide
  "slides": [
    { "type": "title", "title": "...", "subtitle": "..." },
    { "type": "definition",
      "title": "Effective demand",
      "term": "Effective demand",
      "definition": "...",
      "bullets": ["...", "..."],
      "notes": "speaker notes" },
    { "type": "diagram",
      "title": "Shift in demand",
      "diagram_id": "demand_supply_demand_right",
      "diagram_title": "Optional override for the diagram's own title",
      "caption": "When income rises, demand shifts right...",
      "bullets": ["...", "..."] },
    { "type": "case_study",
      "title": "Case: 2022–24 egg price spike (US)",
      "era": "Recent",            # 'Classic' or 'Recent'
      "summary": "Avian flu cut supply; prices rose 60% YoY...",
      "bullets": ["Supply curve shifted left...", "..."],
      "link_to_theory": "Illustrates a leftward shift in S → higher P, lower Q." },
    { "type": "content",
      "title": "Determinants of demand",
      "bullets": ["Price of substitutes", "Income", "Tastes"] },
    { "type": "summary",
      "title": "Topic recap",
      "bullets": ["...", "..."] }
  ]
}

Design rules baked in:
- One concept per slide; let it breathe. No more than ~6 bullets.
- Diagrams are rendered to PNG via diagrams.py then embedded.
- Definition slides emphasise the term (large) and use 'CIE definition style'.
- Case study slides flag era (Classic / Recent) as a coloured chip.
- Notes (speaker notes) are optional but encouraged.
"""
from __future__ import annotations
import json, os, sys, tempfile, shutil, uuid
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# diagrams.py lives next to this file
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import diagrams as dg  # noqa: E402

# ---------- Theme ----------
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

PRIMARY = RGBColor(0x0E, 0x3A, 0x66)   # deep navy
ACCENT = RGBColor(0xE0, 0x6B, 0x2A)    # warm orange
INK = RGBColor(0x1F, 0x2A, 0x37)
MUTED = RGBColor(0x6B, 0x72, 0x80)
BG = RGBColor(0xFF, 0xFF, 0xFF)
BAND = RGBColor(0xF4, 0xEF, 0xE6)
CHIP_CLASSIC = RGBColor(0x35, 0x4A, 0x21)
CHIP_RECENT = RGBColor(0xB2, 0x42, 0x1F)

FONT = "Calibri"


# ---------- Helpers ----------

def _add_textbox(slide, left, top, width, height, text, *,
                 size=18, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
                 italic=False, font=FONT):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return tb


def _add_bullets(slide, left, top, width, height, bullets, *, size=18, color=INK, font=FONT):
    if not bullets:
        return None
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.05)
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(6)
        run = p.add_run()
        run.text = f"•  {b}"
        run.font.name = font
        run.font.size = Pt(size)
        run.font.color.rgb = color
    return tb


def _header_band(slide, title_text, course_text, chapter_text):
    # Coloured top band
    band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, Inches(1.1))
    band.line.fill.background()
    band.fill.solid()
    band.fill.fore_color.rgb = PRIMARY
    band.shadow.inherit = False
    # Title
    _add_textbox(slide, Inches(0.5), Inches(0.15), Inches(12), Inches(0.6),
                 title_text, size=28, bold=True, color=BG)
    # Sub-line: course | chapter
    sub = f"{course_text}  ·  {chapter_text}"
    _add_textbox(slide, Inches(0.5), Inches(0.7), Inches(12), Inches(0.35),
                 sub, size=12, color=RGBColor(0xCC, 0xD6, 0xE0))


def _footer(slide, footer_text, page_idx=None, total=None):
    if footer_text:
        _add_textbox(slide, Inches(0.5), Inches(7.05), Inches(8), Inches(0.35),
                     footer_text, size=10, color=MUTED, italic=True)
    if page_idx is not None and total is not None:
        _add_textbox(slide, Inches(12.0), Inches(7.05), Inches(1.0), Inches(0.35),
                     f"{page_idx} / {total}", size=10, color=MUTED, align=PP_ALIGN.RIGHT)


def _chip(slide, left, top, label, color):
    chip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(1.1), Inches(0.32))
    chip.adjustments[0] = 0.5
    chip.line.fill.background()
    chip.fill.solid()
    chip.fill.fore_color.rgb = color
    tf = chip.text_frame
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.0)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = label
    r.font.name = FONT; r.font.size = Pt(10); r.font.bold = True; r.font.color.rgb = BG


# ---------- Slide builders ----------

def _slide_title(prs, slide_data, ctx):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    # Full-bleed background
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    bg.line.fill.background(); bg.fill.solid(); bg.fill.fore_color.rgb = PRIMARY
    # Accent bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(3.4), Inches(0.8), Inches(0.12))
    bar.line.fill.background(); bar.fill.solid(); bar.fill.fore_color.rgb = ACCENT
    _add_textbox(slide, Inches(0.6), Inches(2.2), Inches(12), Inches(0.6),
                 ctx["course"], size=18, color=RGBColor(0xCC, 0xD6, 0xE0))
    _add_textbox(slide, Inches(0.6), Inches(2.7), Inches(12), Inches(0.9),
                 slide_data.get("title", ctx["chapter"]), size=44, bold=True, color=BG)
    sub = slide_data.get("subtitle") or ctx.get("subtitle", "")
    if sub:
        _add_textbox(slide, Inches(0.6), Inches(4.1), Inches(12), Inches(0.5),
                     sub, size=20, color=RGBColor(0xCC, 0xD6, 0xE0))
    if ctx.get("footer"):
        _add_textbox(slide, Inches(0.6), Inches(7.0), Inches(8), Inches(0.4),
                     ctx["footer"], size=12, color=RGBColor(0xCC, 0xD6, 0xE0), italic=True)
    _notes(slide, slide_data.get("notes"))


def _slide_definition(prs, slide_data, ctx, idx, total):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    _header_band(slide, slide_data.get("title", "Definition"), ctx["course"], ctx["chapter"])
    # Term
    term = slide_data.get("term") or slide_data.get("title", "")
    _add_textbox(slide, Inches(0.6), Inches(1.4), Inches(12), Inches(0.7),
                 term, size=30, bold=True, color=PRIMARY)
    # Definition body
    defn = slide_data.get("definition", "")
    _add_textbox(slide, Inches(0.6), Inches(2.2), Inches(12), Inches(1.4),
                 defn, size=18, color=INK)
    # Side panel band for context bullets
    if slide_data.get("bullets"):
        panel = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(4.0), Inches(12), Inches(2.7))
        panel.line.fill.background(); panel.fill.solid(); panel.fill.fore_color.rgb = BAND
        _add_textbox(slide, Inches(0.8), Inches(4.1), Inches(11.5), Inches(0.4),
                     "Key points", size=14, bold=True, color=PRIMARY)
        _add_bullets(slide, Inches(0.8), Inches(4.55), Inches(11.5), Inches(2.1),
                     slide_data["bullets"], size=16)
    _footer(slide, ctx.get("footer"), idx, total)
    _notes(slide, slide_data.get("notes"))


def _slide_diagram(prs, slide_data, ctx, idx, total, tmpdir):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    _header_band(slide, slide_data.get("title", "Diagram"), ctx["course"], ctx["chapter"])
    # Render diagram
    diagram_id = slide_data["diagram_id"]
    png = os.path.join(tmpdir, f"{uuid.uuid4().hex}.png")
    dg.render(diagram_id, png, title=slide_data.get("diagram_title"))
    # Place diagram on left half
    slide.shapes.add_picture(png, Inches(0.5), Inches(1.4), height=Inches(5.4))
    # Right side: caption + bullets
    if slide_data.get("caption"):
        _add_textbox(slide, Inches(7.6), Inches(1.4), Inches(5.3), Inches(1.0),
                     slide_data["caption"], size=16, italic=True, color=PRIMARY)
    if slide_data.get("bullets"):
        _add_bullets(slide, Inches(7.6), Inches(2.5), Inches(5.3), Inches(4.0),
                     slide_data["bullets"], size=16)
    _footer(slide, ctx.get("footer"), idx, total)
    _notes(slide, slide_data.get("notes"))


def _slide_case_study(prs, slide_data, ctx, idx, total):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    _header_band(slide, slide_data.get("title", "Case study"), ctx["course"], ctx["chapter"])
    era = (slide_data.get("era") or "").strip().lower()
    if era.startswith("class"):
        _chip(slide, Inches(0.6), Inches(1.35), "CLASSIC", CHIP_CLASSIC)
    elif era.startswith("recent") or era.startswith("modern"):
        _chip(slide, Inches(0.6), Inches(1.35), "RECENT", CHIP_RECENT)
    # Summary
    if slide_data.get("summary"):
        _add_textbox(slide, Inches(0.6), Inches(1.85), Inches(12), Inches(1.1),
                     slide_data["summary"], size=17, color=INK)
    # Bullets
    if slide_data.get("bullets"):
        _add_textbox(slide, Inches(0.6), Inches(3.1), Inches(12), Inches(0.35),
                     "What it shows", size=14, bold=True, color=PRIMARY)
        _add_bullets(slide, Inches(0.6), Inches(3.5), Inches(12), Inches(2.6),
                     slide_data["bullets"], size=16)
    # Link to theory band
    if slide_data.get("link_to_theory"):
        band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(6.2), Inches(12), Inches(0.7))
        band.line.fill.background(); band.fill.solid(); band.fill.fore_color.rgb = BAND
        _add_textbox(slide, Inches(0.8), Inches(6.27), Inches(11.6), Inches(0.6),
                     f"Theory link: {slide_data['link_to_theory']}",
                     size=14, italic=True, color=PRIMARY, anchor=MSO_ANCHOR.MIDDLE)
    _footer(slide, ctx.get("footer"), idx, total)
    _notes(slide, slide_data.get("notes"))


def _slide_content(prs, slide_data, ctx, idx, total):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    _header_band(slide, slide_data.get("title", "Content"), ctx["course"], ctx["chapter"])
    if slide_data.get("intro"):
        _add_textbox(slide, Inches(0.6), Inches(1.4), Inches(12), Inches(0.8),
                     slide_data["intro"], size=17, color=INK)
        top = Inches(2.3)
    else:
        top = Inches(1.4)
    _add_bullets(slide, Inches(0.6), top, Inches(12), Inches(5.0),
                 slide_data.get("bullets", []), size=18)
    _footer(slide, ctx.get("footer"), idx, total)
    _notes(slide, slide_data.get("notes"))


def _slide_summary(prs, slide_data, ctx, idx, total):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    _header_band(slide, slide_data.get("title", "Topic recap"), ctx["course"], ctx["chapter"])
    panel = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.5), Inches(12), Inches(5.2))
    panel.line.fill.background(); panel.fill.solid(); panel.fill.fore_color.rgb = BAND
    _add_textbox(slide, Inches(0.85), Inches(1.65), Inches(11.5), Inches(0.5),
                 "You should now be able to…", size=18, bold=True, color=PRIMARY)
    _add_bullets(slide, Inches(0.85), Inches(2.25), Inches(11.5), Inches(4.3),
                 slide_data.get("bullets", []), size=17)
    _footer(slide, ctx.get("footer"), idx, total)
    _notes(slide, slide_data.get("notes"))


def _notes(slide, text):
    if not text:
        return
    notes_tf = slide.notes_slide.notes_text_frame
    notes_tf.text = text


# ---------- Top-level ----------

HANDLERS = {
    "title": None,  # handled outside (not counted in idx/total)
    "definition": _slide_definition,
    "diagram": _slide_diagram,
    "case_study": _slide_case_study,
    "content": _slide_content,
    "summary": _slide_summary,
}


def build(spec: dict, out_path: str) -> str:
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    ctx = {
        "course": spec.get("course", "CIE Economics"),
        "chapter": spec.get("chapter", ""),
        "subtitle": spec.get("subtitle", ""),
        "footer": spec.get("footer", ""),
    }

    slides = spec.get("slides", [])
    # Total page count excludes the title slide
    content_slides = [s for s in slides if s.get("type") != "title"]
    total = len(content_slides)

    tmpdir = tempfile.mkdtemp(prefix="ciepptx_")
    try:
        content_idx = 0
        for s in slides:
            stype = s.get("type", "content")
            if stype == "title":
                _slide_title(prs, s, ctx)
                continue
            content_idx += 1
            if stype == "diagram":
                _slide_diagram(prs, s, ctx, content_idx, total, tmpdir)
            else:
                handler = HANDLERS.get(stype, _slide_content)
                handler(prs, s, ctx, content_idx, total)
        prs.save(out_path)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    return out_path


def main(argv):
    if len(argv) < 3:
        print("Usage: build_deck.py <spec.json|-> <out.pptx>", file=sys.stderr)
        return 2
    spec_arg, out_path = argv[1], argv[2]
    if spec_arg == "-":
        spec = json.load(sys.stdin)
    else:
        with open(spec_arg, "r", encoding="utf-8") as f:
            spec = json.load(f)
    build(spec, out_path)
    print(out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
