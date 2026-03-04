#!/usr/bin/env python3
"""
Generate professional resume PDFs for Mills Shirley LLP attorneys.
Run from project root: python3 scripts/generate-attorney-resume.py [attorney-slug]
With no args, generates all attorney resumes.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, Color
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os
import re
import sys

NAVY = HexColor('#1A2A40')
NAVY_LIGHT = HexColor('#2a3a56')
ACCENT = HexColor('#4a5d77')
DARK_TEXT = HexColor('#1f2937')
BODY_TEXT = HexColor('#374151')
MUTED = HexColor('#6b7280')
LIGHT_LINE = HexColor('#d1d5db')
VERY_LIGHT = HexColor('#f3f4f6')
WHITE = HexColor('#ffffff')

ADDRESS = "2200 Market St, Suite 300 | Galveston, TX 77550"

ATTORNEY_CONFIG = {
    "andy-soto": ("andres-soto.jpg", "(409) 761-4035", "asoto@millsshirley.com", None, None),
    "gus-knebel": ("gus-knebel.jpg", "(409) 761-4056", "", None, None),
    "maureen-mccutchen": ("maureen-mccutchen.jpg", "(409) 761-4023", "mmccutchen@millsshirley.com", None, "board-certified-estate-planning.png"),
    "fred-raschke": ("fred-raschke.jpg", "(409) 761-4028", "", None, None),
    "jack-brock": ("jack-brock.jpg", "(713) 242-1880", "", None, None),
    "rachel-delgado": ("rachel-delgado26.jpg", "(409) 761-4038", "rdelgado@millsshirley.com",
        ["Appeals", "Real Estate", "Construction", "Contracts", "Business Torts", "Fraud Claims", "Employment Contracts"], None),
}
# Config tuple: (photo_file, phone, email, practice_areas_override, certification_logo)


def _clean_text(s):
    if not s:
        return s
    replacements = [
        ("\u00d2", "'"), ("\u00d3", "'"), ("\u00d5", "'"), ("\u00d0", "-"),
        ("\u2013", "-"), ("\u2014", "-"),
        ("\u201c", '"'), ("\u201d", '"'), ("\u2018", "'"), ("\u2019", "'"),
        ("Ò", "'"), ("Ó", "'"), ("Õ", "'"), ("Ð", "-"), ("\x9d", "-"),
    ]
    for old, new in replacements:
        s = s.replace(old, new)
    return s


def parse_data_file(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="cp1252") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

    data = {}
    blocks = re.split(r"\n\n+", content)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.split("\n")
        first = lines[0].strip()
        if ":" in first and not first.startswith("- ") and not first.startswith("  -"):
            key, _, val = first.partition(":")
            key = key.strip().lower().replace(" ", "_")
            val = _clean_text(val.strip())
            if key in ("name", "title", "office", "phone", "email", "headshot", "vcard", "linkedin"):
                data[key] = val
                for line in lines[1:]:
                    s = line.strip()
                    if ":" in s and not s.startswith("- "):
                        k, _, v = s.partition(":")
                        k = k.strip().lower().replace(" ", "_")
                        v = _clean_text(v.strip() if v else "")
                        if k in ("name", "title", "office", "phone", "email", "headshot"):
                            data[k] = v
                continue
            if key == "bio_summary":
                body = "\n".join(lines[1:]).strip() if len(lines) > 1 else val
                if body and "[Insert" not in body:
                    data["bio_summary"] = _clean_text(body)
                continue
            items = []
            for line in lines[1:]:
                s = line.strip()
                if s.startswith("- ") or s.startswith("  -"):
                    item = _clean_text(s.lstrip("- ").strip())
                    if item and "[Insert" not in item and "[None listed]" not in item and "[Not specified]" not in item:
                        items.append(item)
            if items:
                data[key] = items
    return data


def _section_header_flowables(title, styles):
    """Return the flowables that make up a section header (spacer, rule, title)."""
    return [
        Spacer(1, 14),
        HRFlowable(width="100%", thickness=0.75, color=NAVY, spaceAfter=4, spaceBefore=0),
        Paragraph(title, styles["SectionTitle"]),
        Spacer(1, 4),
    ]


def _build_bullet_flowables(items, styles, columns=1):
    """Return a list of flowables for bullet items."""
    flowables = []
    if columns == 2 and len(items) >= 4:
        mid = (len(items) + 1) // 2
        left_col = items[:mid]
        right_col = items[mid:]
        col_data = []
        for i in range(max(len(left_col), len(right_col))):
            left = Paragraph(f"<bullet>&bull;</bullet> {left_col[i]}", styles["ResumeBullet"]) if i < len(left_col) else ""
            right = Paragraph(f"<bullet>&bull;</bullet> {right_col[i]}", styles["ResumeBullet"]) if i < len(right_col) else ""
            col_data.append([left, right])
        col_width = 3.25 * inch
        tbl = Table(col_data, colWidths=[col_width, col_width])
        tbl.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))
        flowables.append(tbl)
    else:
        for item in items:
            flowables.append(Paragraph(f"<bullet>&bull;</bullet> {item}", styles["ResumeBullet"]))
    return flowables


def _add_section(story, title, content_flowables, styles):
    """Add a section with header kept together with the first content items.

    Uses KeepTogether to prevent the header from being orphaned at
    the bottom of a page while its content starts on the next page.
    """
    header = _section_header_flowables(title, styles)
    # Keep the header together with at least the first 3 content items
    peek = content_flowables[:3]
    rest = content_flowables[3:]
    story.append(KeepTogether(header + peek))
    story.extend(rest)


def create_resume(slug):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_path = os.path.join(project_root, "data", "attorneys", f"{slug}.txt")
    output_path = os.path.join(project_root, "assets", "pdf", f"{slug}-resume.pdf")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    data = parse_data_file(data_path)
    if not data:
        print(f"  No data file for {slug}, skipping")
        return False

    config = ATTORNEY_CONFIG.get(slug, (f"{slug}.jpg", "", "", None, None))
    photo_file, phone, email = config[0], config[1], config[2]
    practices_override = config[3] if len(config) > 3 else None
    cert_logo_file = config[4] if len(config) > 4 else None
    if not phone and data.get("phone"):
        phone = data["phone"]
    photo_path = os.path.join(project_root, "assets", "img", "attorneys", photo_file)

    name = data.get("name", slug.replace("-", " ").title())
    title_text = data.get("title", "")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        title=f"{name} - Resume",
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="NameStyle", fontSize=22, textColor=NAVY, fontName="Helvetica-Bold",
        spaceAfter=2, leading=26
    ))
    styles.add(ParagraphStyle(
        name="TitleStyle", fontSize=11, textColor=ACCENT, fontName="Helvetica",
        spaceAfter=6, leading=14
    ))
    styles.add(ParagraphStyle(
        name="ContactStyle", fontSize=8.5, textColor=MUTED, fontName="Helvetica",
        spaceAfter=0, leading=12
    ))
    styles.add(ParagraphStyle(
        name="SectionTitle", fontSize=11, textColor=NAVY, fontName="Helvetica-Bold",
        spaceBefore=0, spaceAfter=4, leading=14
    ))
    styles.add(ParagraphStyle(
        name="BodyText2", fontSize=9.5, textColor=BODY_TEXT, fontName="Helvetica",
        spaceAfter=4, leading=13.5
    ))
    styles.add(ParagraphStyle(
        name="ResumeBullet", fontSize=9.5, textColor=BODY_TEXT, fontName="Helvetica",
        leftIndent=14, bulletIndent=0, spaceAfter=2, leading=13
    ))
    styles.add(ParagraphStyle(
        name="SmallBody", fontSize=9, textColor=BODY_TEXT, fontName="Helvetica",
        spaceAfter=3, leading=12.5
    ))
    styles.add(ParagraphStyle(
        name="FooterStyle", fontSize=7.5, textColor=MUTED, fontName="Helvetica",
        alignment=TA_CENTER, spaceBefore=12
    ))

    story = []

    # ── Header: Photo + Name/Title/Contact side-by-side ──
    has_photo = os.path.exists(photo_path)

    contact_parts = [ADDRESS]
    if phone:
        contact_parts.append(phone)
    if email:
        contact_parts.append(email)
    contact_line = "  |  ".join(contact_parts)

    name_para = Paragraph(name.upper(), styles["NameStyle"])
    title_para = Paragraph(f"{title_text}  |  Mills Shirley LLP", styles["TitleStyle"])
    contact_para = Paragraph(contact_line, styles["ContactStyle"])

    # Build optional certification logo for header
    cert_img_obj = None
    if cert_logo_file:
        cert_path = os.path.join(project_root, "assets", "img", cert_logo_file)
        if os.path.exists(cert_path):
            cert_img_obj = Image(cert_path, width=1.4 * inch, height=0.79 * inch, kind='proportional')
            cert_img_obj.hAlign = "RIGHT"

    if has_photo:
        img = Image(photo_path, width=1.15 * inch, height=1.45 * inch)
        img.hAlign = "LEFT"

        # Text rows: name, title, contact — and cert logo aligned right if present
        text_rows = [[name_para], [title_para], [contact_para]]
        text_col_width = 3.85 * inch if cert_img_obj else 5.2 * inch

        text_block = Table(text_rows, colWidths=[text_col_width])
        text_block.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))

        if cert_img_obj:
            mid_block = Table(
                [[text_block, cert_img_obj]],
                colWidths=[3.95 * inch, 1.4 * inch]
            )
            mid_block.setStyle(TableStyle([
                ('VALIGN', (0, 0), (0, 0), 'TOP'),
                ('VALIGN', (1, 0), (1, 0), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            header_table = Table(
                [[img, mid_block]],
                colWidths=[1.35 * inch, 5.35 * inch]
            )
        else:
            header_table = Table(
                [[img, text_block]],
                colWidths=[1.35 * inch, 5.35 * inch]
            )
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(header_table)
    else:
        story.append(name_para)
        story.append(title_para)
        story.append(contact_para)

    # Thick accent bar under header
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=2.5, color=NAVY, spaceAfter=4))

    # ── Professional Profile ──
    bio = data.get("bio_summary", "")
    if bio:
        _add_section(story, "PROFESSIONAL PROFILE",
                     [Paragraph(bio, styles["BodyText2"])], styles)

    # ── Practice Areas (2-column) ──
    practices = practices_override if practices_override else data.get("practice_areas", [])
    if practices:
        _add_section(story, "PRACTICE AREAS",
                     _build_bullet_flowables(practices, styles, columns=2), styles)

    # ── Education ──
    education = data.get("education", [])
    if education:
        _add_section(story, "EDUCATION",
                     [Paragraph(f"<bullet>&bull;</bullet> {e}", styles["ResumeBullet"]) for e in education], styles)

    # ── Bar Admissions ──
    bar = data.get("bar_admissions", [])
    if bar:
        _add_section(story, "BAR ADMISSIONS",
                     [Paragraph("  |  ".join(bar), styles["SmallBody"])], styles)

    # ── Legal Certifications ──
    certs = data.get("legal_certifications", [])
    if certs:
        _add_section(story, "LEGAL CERTIFICATIONS",
                     [Paragraph(f"<bullet>&bull;</bullet> {c}", styles["ResumeBullet"]) for c in certs], styles)

    # ── Professional Memberships (2-column) ──
    memberships = data.get("professional_memberships", [])
    if memberships:
        _add_section(story, "PROFESSIONAL MEMBERSHIPS",
                     _build_bullet_flowables(memberships, styles, columns=2), styles)

    # ── Representative Matters ──
    matters = data.get("representative_matters", [])
    if matters:
        _add_section(story, "REPRESENTATIVE MATTERS",
                     _build_bullet_flowables(matters, styles, columns=1), styles)

    # ── Awards & Recognition ──
    awards = data.get("awards_&_recognition", [])
    if awards:
        _add_section(story, "RECOGNITION & AWARDS",
                     _build_bullet_flowables(awards, styles, columns=1), styles)

    # ── Publications ──
    pubs = data.get("publications", [])
    if pubs:
        _add_section(story, "PUBLICATIONS",
                     [Paragraph(f"<bullet>&bull;</bullet> {p}", styles["ResumeBullet"]) for p in pubs], styles)

    # ── Presentations & Seminars ──
    pres = data.get("presentations_&_seminars", [])
    if pres:
        _add_section(story, "PRESENTATIONS & SEMINARS",
                     [Paragraph(f"<bullet>&bull;</bullet> {p}", styles["ResumeBullet"]) for p in pres], styles)

    # ── Community Involvement ──
    community = data.get("community_involvement", [])
    if community:
        _add_section(story, "COMMUNITY INVOLVEMENT",
                     _build_bullet_flowables(community, styles, columns=2), styles)

    # ── Past Positions ──
    past = data.get("past_positions", [])
    if past:
        _add_section(story, "PAST POSITIONS",
                     [Paragraph(f"<bullet>&bull;</bullet> {p}", styles["ResumeBullet"]) for p in past], styles)

    # ── Languages ──
    langs = data.get("languages", [])
    if langs:
        _add_section(story, "LANGUAGES",
                     [Paragraph("  |  ".join(langs), styles["SmallBody"])], styles)

    # ── Footer ──
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_LINE, spaceAfter=6))
    story.append(Paragraph(
        "Mills Shirley LLP  |  Texas's Oldest Continuously Operating Law Firm  |  Established 1846",
        styles["FooterStyle"]
    ))
    story.append(Paragraph(
        "Galveston  |  Houston  |  millsshirley.com",
        styles["FooterStyle"]
    ))

    doc.build(story)
    print(f"  Generated: {output_path}")
    return True


def main():
    if len(sys.argv) > 1:
        slugs = [sys.argv[1]]
    else:
        slugs = list(ATTORNEY_CONFIG.keys())

    for slug in slugs:
        print(f"Generating resume for {slug}...")
        create_resume(slug)


if __name__ == "__main__":
    main()
