#!/usr/bin/env python3
"""
Generate professional resume PDFs for Mills Shirley LLP attorneys.
Run from project root: python3 scripts/generate-attorney-resume.py [attorney-slug]
With no args, generates all attorney resumes.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os
import re
import sys

# Brand colors (Mills Shirley)
NAVY = HexColor('#1A2A40')
NAVY_LIGHT = HexColor('#334155')
GRAY = HexColor('#6b7280')
ADDRESS = "2200 Market St, Suite 300 | Galveston, TX 77550"

# Attorney config: slug -> (photo_file, phone, email, practice_areas_override)
ATTORNEY_CONFIG = {
    "andy-soto": ("andres-soto.jpg", "(409) 761-4035", "asoto@millsshirley.com", None),
    "gus-knebel": ("gus-knebel.jpg", "(409) 761-4056", "", None),
    "maureen-mccutchen": ("maureen-mccutchen.jpg", "(409) 761-4023", "", None),
    "fred-raschke": ("fred-raschke.jpg", "(409) 761-4028", "", None),
    "jack-brock": ("jack-brock.jpg", "(713) 242-1880", "", None),
    "rachel-delgado": ("rachel-delgado.jpg", "(409) 761-4038", "rdelgado@millsshirley.com",
        ["Appeals", "Real Estate", "Construction", "Contracts", "Business Torts", "Fraud Claims", "Employment Contracts"]),
}


def _clean_text(s):
    """Fix encoding and placeholder text. Replace curly/smart quotes and mojibake with ASCII."""
    if not s:
        return s
    # Curly quotes, en-dash mojibake (0xD0 in cp1252 = Ð), and common replacements
    replacements = [
        ("Ò", "'"), ("Ó", "'"), ("Õ", "'"), ("Ð", "-"), ("–", "-"), ("—", "-"),
        (""", "'"), (""", "'"), (""", '"'), (""", '"'),  # Unicode curly quotes
        ("\u00d2", "'"), ("\u00d3", "'"),  # Latin O variants used as quote mojibake
        ("\u00d0", "-"),  # Ð - often used as en-dash in cp1252 files (e.g. 2014Ð2015)
    ]
    for old, new in replacements:
        s = s.replace(old, new)
    return s


def parse_data_file(path):
    """Parse attorney data file into structured dict."""
    if not os.path.exists(path):
        return None
    # Try cp1252 first (common for Windows-saved files with curly quotes), fallback to utf-8
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
        # Section header: "Section Name:" at start (not a bullet)
        if ":" in first and not first.startswith("- ") and not first.startswith("  -"):
            key, _, val = first.partition(":")  # split on first colon
            key = key.strip().lower().replace(" ", "_")
            val = _clean_text(val.strip())
            # Single-line metadata - first block has multiple such lines
            if key in ("name", "title", "office", "phone", "email", "headshot", "vcard", "linkedin"):
                data[key] = val
                # Process remaining lines in block if they're also key:value (metadata block)
                for line in lines[1:]:
                    s = line.strip()
                    if ":" in s and not s.startswith("- "):
                        k, _, v = s.partition(":")
                        k = k.strip().lower().replace(" ", "_")
                        v = _clean_text(v.strip() if v else "")
                        if k in ("name", "title", "office", "phone", "email", "headshot"):
                            data[k] = v
                continue
            # Bio Summary: content is on following line(s)
            if key == "bio_summary":
                body = "\n".join(lines[1:]).strip() if len(lines) > 1 else val
                if body and "[Insert" not in body:
                    data["bio_summary"] = _clean_text(body)
                continue
            # List sections: collect "- item" lines
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


def _debug_parse(path):
    """Debug: print parse state for first 30 lines."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.read().split("\n")
    for i, line in enumerate(lines[:30]):
        has_colon = ": " in line
        starts_dash = line.startswith("- ") or line.startswith("  -")
        print(f"{i:2}: has_colon={has_colon} dash={starts_dash} | {repr(line[:60])}")


def clean_text(s):
    """Clean placeholder text."""
    if not s:
        return ""
    placeholders = ["[Insert if known]", "[Insert if available]", "[None listed]", "[Not specified]", "[Insert if known or applicable]"]
    for p in placeholders:
        if p in s:
            return ""
    return s


def create_resume(slug):
    """Generate resume PDF for attorney."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_path = os.path.join(project_root, "data", "attorneys", f"{slug}.txt")
    output_path = os.path.join(project_root, "assets", "pdf", f"{slug}-resume.pdf")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    data = parse_data_file(data_path)
    if not data:
        print(f"  No data file for {slug}, skipping")
        return False

    config = ATTORNEY_CONFIG.get(slug, (f"{slug}.jpg", "", "", None))
    photo_file = config[0]
    phone = config[1] if len(config) > 1 else ""
    email = config[2] if len(config) > 2 else ""
    practices_override = config[3] if len(config) > 3 else None
    if not phone and data.get("phone"):
        phone = data["phone"]
    photo_path = os.path.join(project_root, "assets", "img", "attorneys", photo_file)

    name = data.get("name", slug.replace("-", " ").title())
    title = data.get("title", "")
    contact_line = ADDRESS
    if phone:
        contact_line += f" | {phone}"
    if email:
        contact_line += f" | {email}"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title="Professional Resume",
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="SectionHeader", fontSize=12, textColor=NAVY, spaceBefore=14, spaceAfter=6, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="ResumeBody", fontSize=10, textColor=HexColor("#374151"), spaceAfter=6, fontName="Helvetica"))
    styles.add(ParagraphStyle(name="ResumeBullet", fontSize=10, textColor=HexColor("#374151"), leftIndent=20, spaceAfter=2, fontName="Helvetica"))

    story = []

    # Photo
    if os.path.exists(photo_path):
        img = Image(photo_path, width=1.25 * inch, height=1.6 * inch)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Spacer(1, 8))

    # Header
    # Use plain ASCII for header - avoid HTML entities that can cause rendering issues
    name_upper = name.upper()
    title_safe = title
    header_text = f"<b><font size='24' color='#1A2A40'>{name_upper}</font></b><br/><font size='12' color='#334155'>{title_safe} | Mills Shirley LLP</font><br/><font size='9' color='#6b7280'>{contact_line}</font>"
    story.append(Paragraph(header_text, ParagraphStyle("Header", alignment=TA_CENTER, spaceAfter=20)))

    # Bio
    bio = data.get("bio_summary", "")
    if bio:
        story.append(Paragraph("PROFESSIONAL PROFILE", styles["SectionHeader"]))
        story.append(Paragraph(bio, styles["ResumeBody"]))

    # Practice Areas
    practices = practices_override if practices_override else data.get("practice_areas", [])
    if practices:
        story.append(Paragraph("PRACTICE AREAS", styles["SectionHeader"]))
        for p in practices:
            story.append(Paragraph(f"• {p}", styles["ResumeBullet"]))

    # Education
    education = data.get("education", [])
    if education:
        story.append(Paragraph("EDUCATION", styles["SectionHeader"]))
        for e in education:
            story.append(Paragraph(f"• {e}", styles["ResumeBullet"]))

    # Bar Admissions
    bar = data.get("bar_admissions", [])
    if bar:
        story.append(Paragraph("BAR ADMISSIONS", styles["SectionHeader"]))
        story.append(Paragraph(" | ".join(bar), styles["ResumeBody"]))

    # Legal Certifications (Maureen)
    certs = data.get("legal_certifications", [])
    if certs:
        story.append(Paragraph("LEGAL CERTIFICATIONS", styles["SectionHeader"]))
        for c in certs:
            story.append(Paragraph(f"• {c}", styles["ResumeBullet"]))

    # Professional Memberships
    memberships = data.get("professional_memberships", [])
    if memberships:
        story.append(Paragraph("PROFESSIONAL MEMBERSHIPS", styles["SectionHeader"]))
        for m in memberships:
            story.append(Paragraph(f"• {m}", styles["ResumeBullet"]))

    # Representative Matters
    matters = data.get("representative_matters", [])
    if matters:
        story.append(Paragraph("REPRESENTATIVE MATTERS", styles["SectionHeader"]))
        for m in matters:
            story.append(Paragraph(f"• {m}", styles["ResumeBullet"]))

    # Awards & Recognition
    awards = data.get("awards_&_recognition", [])
    if awards:
        story.append(Paragraph("RECOGNITION & AWARDS", styles["SectionHeader"]))
        for a in awards:
            story.append(Paragraph(f"• {a}", styles["ResumeBullet"]))

    # Publications
    pubs = data.get("publications", [])
    if pubs:
        story.append(Paragraph("PUBLICATIONS", styles["SectionHeader"]))
        for p in pubs:
            story.append(Paragraph(f"• {p}", styles["ResumeBullet"]))

    # Presentations & Seminars
    pres = data.get("presentations_&_seminars", [])
    if pres:
        story.append(Paragraph("PRESENTATIONS & SEMINARS", styles["SectionHeader"]))
        for p in pres:
            story.append(Paragraph(f"• {p}", styles["ResumeBullet"]))

    # Community Involvement
    community = data.get("community_involvement", [])
    if community:
        story.append(Paragraph("COMMUNITY INVOLVEMENT", styles["SectionHeader"]))
        for c in community:
            story.append(Paragraph(f"• {c}", styles["ResumeBullet"]))

    # Past Positions (Jack)
    past = data.get("past_positions", [])
    if past:
        story.append(Paragraph("PAST POSITIONS", styles["SectionHeader"]))
        for p in past:
            story.append(Paragraph(f"• {p}", styles["ResumeBullet"]))

    # Languages (Rachel)
    langs = data.get("languages", [])
    if langs:
        story.append(Paragraph("LANGUAGES", styles["SectionHeader"]))
        story.append(Paragraph(" | ".join(langs), styles["ResumeBody"]))

    # Footer
    story.append(Spacer(1, 20))
    story.append(Paragraph("Mills Shirley LLP | Texas's Oldest Continuously Operating Law Firm | Established 1846", ParagraphStyle("Footer", fontSize=8, textColor=GRAY, alignment=TA_CENTER)))

    doc.build(story)
    print(f"  Generated: {output_path}")
    return True


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_dir = os.path.join(project_root, "data", "attorneys")

    if len(sys.argv) > 1:
        slugs = [sys.argv[1]]
    else:
        slugs = list(ATTORNEY_CONFIG.keys())

    for slug in slugs:
        print(f"Generating resume for {slug}...")
        create_resume(slug)


if __name__ == "__main__":
    main()
