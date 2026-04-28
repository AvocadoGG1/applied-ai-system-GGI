from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


OUT_DIR = Path("presentation")
PPTX_PATH = OUT_DIR / "glitch_museum_mode_presentation.pptx"
NOTES_PATH = OUT_DIR / "glitch_museum_mode_speaker_notes.md"

NAVY = RGBColor(18, 31, 46)
INK = RGBColor(30, 41, 59)
MUTED = RGBColor(91, 105, 125)
TEAL = RGBColor(20, 184, 166)
AMBER = RGBColor(245, 158, 11)
RED = RGBColor(239, 68, 68)
WHITE = RGBColor(255, 255, 255)
SOFT = RGBColor(241, 245, 249)


def add_textbox(slide, left, top, width, height, text, size=28, color=INK, bold=False):
    box = slide.shapes.add_textbox(left, top, width, height)
    frame = box.text_frame
    frame.clear()
    paragraph = frame.paragraphs[0]
    paragraph.text = text
    paragraph.font.size = Pt(size)
    paragraph.font.color.rgb = color
    paragraph.font.bold = bold
    paragraph.font.name = "Aptos"
    return box


def add_title(slide, title, subtitle=None):
    add_textbox(
        slide,
        Inches(0.65),
        Inches(0.42),
        Inches(11.9),
        Inches(0.7),
        title,
        size=34,
        color=INK,
        bold=True,
    )
    if subtitle:
        add_textbox(
            slide,
            Inches(0.7),
            Inches(1.08),
            Inches(10.8),
            Inches(0.36),
            subtitle,
            size=15,
            color=MUTED,
        )


def add_footer(slide, text):
    add_textbox(
        slide,
        Inches(0.7),
        Inches(6.95),
        Inches(12.0),
        Inches(0.22),
        text,
        size=9,
        color=MUTED,
    )


def add_bullet_list(slide, items, left, top, width, height, size=22):
    box = slide.shapes.add_textbox(left, top, width, height)
    frame = box.text_frame
    frame.clear()
    for index, item in enumerate(items):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = item
        paragraph.level = 0
        paragraph.font.size = Pt(size)
        paragraph.font.name = "Aptos"
        paragraph.font.color.rgb = INK
        paragraph.space_after = Pt(9)
    return box


def add_tag(slide, left, top, width, text, fill_color=TEAL):
    shape = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
        left,
        top,
        width,
        Inches(0.42),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = fill_color
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = text
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.font.name = "Aptos"
    return shape


def add_step(slide, x, y, w, h, title, body, color):
    shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = SOFT
    shape.line.color.rgb = color
    shape.line.width = Pt(2)
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = color
    p.font.name = "Aptos"
    p2 = tf.add_paragraph()
    p2.text = body
    p2.font.size = Pt(12)
    p2.font.color.rgb = INK
    p2.font.name = "Aptos"
    return shape


def add_arrow(slide, x1, y1, x2, y2):
    line = slide.shapes.add_connector(1, x1, y1, x2, y2)
    line.line.color.rgb = MUTED
    line.line.width = Pt(1.7)
    line.line.end_arrowhead = True
    return line


def build_deck():
    OUT_DIR.mkdir(exist_ok=True)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    notes = []

    # Slide 1
    slide = prs.slides.add_slide(blank)
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = NAVY
    add_tag(slide, Inches(0.75), Inches(0.65), Inches(2.6), "RAG + Reliability", TEAL)
    add_textbox(
        slide,
        Inches(0.75),
        Inches(1.55),
        Inches(11.5),
        Inches(1.25),
        "Game Glitch Investigator",
        size=48,
        color=WHITE,
        bold=True,
    )
    add_textbox(
        slide,
        Inches(0.78),
        Inches(2.63),
        Inches(10.7),
        Inches(0.75),
        "Glitch Museum Mode",
        size=36,
        color=TEAL,
        bold=True,
    )
    add_textbox(
        slide,
        Inches(0.8),
        Inches(3.65),
        Inches(9.8),
        Inches(0.82),
        "A RAG-powered museum guide that explains fixed AI-generated bugs using real project evidence.",
        size=23,
        color=SOFT,
    )
    add_textbox(
        slide,
        Inches(0.8),
        Inches(6.62),
        Inches(8.5),
        Inches(0.26),
        "Live demo first. Slides as backup structure.",
        size=12,
        color=SOFT,
    )
    notes.append(
        "Start by saying the project name and the one-sentence summary. Explain that the deck is only a frame, and the real proof is the live Streamlit demo."
    )

    # Slide 2
    slide = prs.slides.add_slide(blank)
    add_title(
        slide,
        "Original Project: The Impossible Guesser",
        "An AI-generated Streamlit game that ran, but behaved incorrectly.",
    )
    add_bullet_list(
        slide,
        [
            "Secret number changed during play because Streamlit reran the script.",
            "Higher/lower hints pointed the player in the wrong direction.",
            "New Game did not fully reset status, score, attempts, and history.",
            "Invalid and out-of-range guesses were accepted.",
            "Scoring gave inconsistent rewards for wrong guesses.",
        ],
        Inches(0.9),
        Inches(1.85),
        Inches(7.1),
        Inches(4.5),
        size=21,
    )
    add_tag(slide, Inches(8.85), Inches(2.0), Inches(2.2), "Fixed", TEAL)
    add_textbox(
        slide,
        Inches(8.35),
        Inches(2.75),
        Inches(3.4),
        Inches(1.8),
        "Refactored logic + pytest turned hidden bugs into repeatable checks.",
        size=25,
        color=INK,
        bold=True,
    )
    add_footer(slide, "Original project goal: debug, refactor, and test AI-generated game logic.")
    notes.append(
        "Explain that the original Modules 1-3 project was a broken guessing game. The key point is that AI-generated code can run without being logically correct."
    )

    # Slide 3
    slide = prs.slides.add_slide(blank)
    add_title(
        slide,
        "How Glitch Museum Mode Works",
        "A local RAG pipeline searches project files before the guide answers.",
    )
    steps = [
        ("User Input", "artifact or custom question", TEAL),
        ("Streamlit", "app.py sends query", AMBER),
        ("Retriever", "rag_utils.py scores chunks", TEAL),
        ("Evidence", "README, reflection, code, tests", AMBER),
        ("Guide", "answer + confidence", TEAL),
    ]
    x = Inches(0.65)
    y = Inches(2.35)
    w = Inches(2.15)
    h = Inches(1.35)
    gap = Inches(0.42)
    for idx, (title, body, color) in enumerate(steps):
        add_step(slide, x + idx * (w + gap), y, w, h, title, body, color)
        if idx < len(steps) - 1:
            add_arrow(
                slide,
                x + idx * (w + gap) + w,
                y + Inches(0.68),
                x + (idx + 1) * (w + gap),
                y + Inches(0.68),
            )
    add_textbox(
        slide,
        Inches(1.35),
        Inches(4.8),
        Inches(10.4),
        Inches(0.7),
        "The guide does not just print raw files. It uses retrieved snippets to explain what broke, why, how it was fixed, and what test proves it.",
        size=22,
        color=INK,
        bold=True,
    )
    add_footer(slide, "Knowledge base: README.md, reflection.md, app.py, logic_utils.py, tests/test_game_logic.py")
    notes.append(
        "Use this slide to explain the architecture quickly, then move back to the app. Name app.py as the interface and rag_utils.py as retrieval, response generation, and confidence scoring."
    )

    # Slide 4
    slide = prs.slides.add_slide(blank)
    add_title(
        slide,
        "Reliability: The System Has to Prove It",
        "Tests and confidence scoring make the guide safer than a generic answer box.",
    )
    add_textbox(
        slide,
        Inches(0.9),
        Inches(1.85),
        Inches(4.0),
        Inches(1.0),
        "26 / 26",
        size=60,
        color=TEAL,
        bold=True,
    )
    add_textbox(
        slide,
        Inches(1.0),
        Inches(2.78),
        Inches(4.2),
        Inches(0.35),
        "automated tests passed",
        size=18,
        color=INK,
        bold=True,
    )
    add_bullet_list(
        slide,
        [
            "Game logic tests check hints, resets, validation, difficulty, and scoring.",
            "RAG tests check retrieval, evidence-backed answers, and fallback behavior.",
            "Confidence scores use retrieval strength and source diversity.",
            "Unrelated questions return 0.00 confidence instead of a fake answer.",
        ],
        Inches(5.1),
        Inches(1.85),
        Inches(7.15),
        Inches(4.3),
        size=20,
    )
    add_footer(slide, "Demo guardrail input: 'Explain database migrations and cloud billing'")
    notes.append(
        "Point out the test count and then demo the unrelated question in Streamlit. This is the required reliability or guardrail behavior."
    )

    # Slide 5
    slide = prs.slides.add_slide(blank)
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = SOFT
    add_title(slide, "What I Learned", "Responsible AI is evidence, tests, and honest limits.")
    add_bullet_list(
        slide,
        [
            "AI-generated code can run and still be wrong.",
            "RAG is strongest when retrieved evidence actually shapes the answer.",
            "Confidence scoring helps users know when the system has support.",
            "A good AI engineer verifies suggestions instead of trusting the demo.",
        ],
        Inches(0.9),
        Inches(1.85),
        Inches(7.0),
        Inches(4.4),
        size=23,
    )
    add_textbox(
        slide,
        Inches(8.55),
        Inches(2.05),
        Inches(3.7),
        Inches(2.4),
        "What this says about me:\nI build AI systems that are useful, testable, and honest about their limits.",
        size=24,
        color=NAVY,
        bold=True,
    )
    add_footer(slide, "End the Loom here after the live demo.")
    notes.append(
        "End by saying that this project shows you care about building AI that is not just impressive, but inspectable and reliable."
    )

    prs.save(PPTX_PATH)
    write_notes(notes)


def write_notes(notes):
    lines = ["# Speaker Notes\n"]
    for idx, note in enumerate(notes, start=1):
        lines.append(f"## Slide {idx}\n")
        lines.append(note)
        lines.append("")
    NOTES_PATH.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    build_deck()
    print(PPTX_PATH)
    print(NOTES_PATH)
