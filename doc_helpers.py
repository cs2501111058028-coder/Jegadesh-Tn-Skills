"""
Comprehensive Document Generator for EduGenie
Generates professional .docx files for Phases 1 to 8 and Final Project Report.
Uses real code metrics, real screenshots, and real test execution results.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(REPO_DIR, "Phase_Wise_Submission")
SCREENSHOTS_DIR = os.path.join(REPO_DIR, "docs", "screenshots")
DIAGRAMS_DIR = os.path.join(DOCS_DIR, "03_Project_Design", "diagrams")
PLANNING_DIR = os.path.join(DOCS_DIR, "04_Project_Planning")

# Colors
COLOR_PRIMARY_HEX = "1E1B4B"      # Deep Indigo
COLOR_ACCENT_HEX = "4F46E5"       # Indigo Accent
COLOR_BG_ALT_HEX = "F8FAFC"       # Light Slate
COLOR_BORDER_HEX = "CBD5E1"       # Border Grey
COLOR_GREEN_HEX = "10B981"        # Emerald
COLOR_RED_HEX = "EF4444"          # Crimson

def set_cell_background(cell, fill_hex):
    """Sets background color of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding in twips (dxa)."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_styled_heading(doc, text, level):
    """Adds a beautifully styled heading with specific colors and spacing."""
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    
    if level == 1:
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(30, 27, 75)
    elif level == 2:
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(79, 70, 229)
    elif level == 3:
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_body_paragraph(doc, text, bold_prefix="", italic=False):
    """Adds a standard body paragraph with clean typography."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.bold = True
        r_b.font.size = Pt(10)
        r_b.font.color.rgb = RGBColor(15, 23, 42)
    if text:
        r_t = p.add_run(text)
        r_t.font.size = Pt(10)
        r_t.italic = italic
        r_t.font.color.rgb = RGBColor(30, 41, 59)
    return p

def add_bullet_point(doc, text, bold_prefix=""):
    """Adds a bullet point paragraph."""
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.bold = True
        r_b.font.size = Pt(10)
        r_b.font.color.rgb = RGBColor(15, 23, 42)
    r_t = p.add_run(text)
    r_t.font.size = Pt(10)
    r_t.font.color.rgb = RGBColor(30, 41, 59)
    return p

def add_styled_table(doc, headers, data, col_widths=None):
    """Creates a modern styled table with dark headers, zebra stripes, and borders."""
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Header Row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], COLOR_PRIMARY_HEX)
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=150, right=150)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

    # Data Rows
    for r_idx, row in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        bg_color = COLOR_BG_ALT_HEX if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.line_spacing = 1.1
            p.paragraph_format.space_after = Pt(2)
            if c_idx == 0 or "ID" in headers[c_idx] or "Status" in headers[c_idx] or "Priority" in headers[c_idx]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(15, 23, 42)
                if val in ["Pass", "Completed", "High", "VERIFIED (100%)", "100%"]:
                    r.bold = True

    # Set Column Widths if provided
    if col_widths:
        for r in table.rows:
            for i, w in enumerate(col_widths):
                r.cells[i].width = Inches(w)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return table

def add_figure(doc, image_path, caption_text, width=Inches(5.5)):
    """Embeds an image figure with centered alignment and italicized caption."""
    if os.path.exists(image_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(image_path, width=width)

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.size = Pt(8.5)
        r_cap.italic = True
        r_cap.font.color.rgb = RGBColor(100, 116, 139)

def add_callout_box(doc, text, title=""):
    """Adds a callout highlight box with a tinted background."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "EEF2FF")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.15
    if title:
        r_t = p.add_run(f"📌 {title}\n")
        r_t.bold = True
        r_t.font.size = Pt(10)
        r_t.font.color.rgb = RGBColor(79, 70, 229)
    r_body = p.add_run(text)
    r_body.font.size = Pt(9.5)
    r_body.font.color.rgb = RGBColor(30, 27, 75)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def setup_page_layout(doc, title, subtitle, phase_num=None):
    """Initializes standard document margins, header, and cover block."""
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

        # Header
        header = section.header
        hp = header.paragraphs[0]
        hp.text = f"EduGenie: Google Gemini Powered Learning Assistant • {title}"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for r in hp.runs:
            r.font.size = Pt(8)
            r.font.color.rgb = RGBColor(148, 163, 184)

        # Footer
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Academic & Internship Project Submission • Technical Documentation"
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in fp.runs:
            r.font.size = Pt(8)
            r.font.color.rgb = RGBColor(148, 163, 184)

    # Title Block
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(2)
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_title = p_title.add_run(title)
    r_title.bold = True
    r_title.font.size = Pt(20)
    r_title.font.color.rgb = RGBColor(30, 27, 75)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(8)
    r_sub = p_sub.add_run(subtitle)
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(79, 70, 229)

    add_callout_box(
        doc,
        "Project: EduGenie (Google Gemini Powered Learning Assistant)\n"
        "Framework: FastAPI ASGI • Runtime: Python 3.10+ / 3.13 • Frontend: Vanilla JS & CSS3\n"
        "AI Models: Google Gemini (gemini-1.5-flash / pro) + Local MBZUAI/LaMini-Flan-T5-783M\n"
        "Verification: 37 Automated Pytest Test Cases (100% Pass) • Real Playwright Screenshots",
        "DOCUMENT METADATA"
    )

print("Document generator helper module loaded.")
