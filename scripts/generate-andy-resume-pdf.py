#!/usr/bin/env python3
"""
Generate Andy Soto's professional resume PDF.
Run from project root: python3 scripts/generate-andy-resume-pdf.py
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

# Brand colors (Mills Shirley)
NAVY = HexColor('#1A2A40')
NAVY_LIGHT = HexColor('#334155')
GRAY = HexColor('#6b7280')

def create_resume():
    output_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'pdf', 'andy-soto-resume.pdf')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        title="Professional Resume"
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='ResumeTitle',
        fontSize=24,
        textColor=NAVY,
        spaceAfter=2,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        name='ResumeTitleLeft',
        fontSize=24,
        textColor=NAVY,
        spaceAfter=2,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        name='ResumeSubtitle',
        fontSize=12,
        textColor=NAVY_LIGHT,
        spaceAfter=18,
        alignment=TA_CENTER,
        fontName='Helvetica'
    ))
    styles.add(ParagraphStyle(
        name='ResumeSubtitleLeft',
        fontSize=12,
        textColor=NAVY_LIGHT,
        spaceAfter=6,
        alignment=TA_LEFT,
        fontName='Helvetica'
    ))
    styles.add(ParagraphStyle(
        name='SectionHeader',
        fontSize=12,
        textColor=NAVY,
        spaceBefore=14,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        name='ResumeBody',
        fontSize=10,
        textColor=HexColor('#374151'),
        spaceAfter=6,
        fontName='Helvetica'
    ))
    styles.add(ParagraphStyle(
        name='ResumeBullet',
        fontSize=10,
        textColor=HexColor('#374151'),
        leftIndent=20,
        spaceAfter=2,
        fontName='Helvetica'
    ))

    story = []

    # Header with photo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    photo_path = os.path.join(project_root, 'assets', 'img', 'attorneys', 'andres-soto.jpg')

    if os.path.exists(photo_path):
        img = Image(photo_path, width=1.25*inch, height=1.6*inch)
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(Spacer(1, 8))
    # Single combined header to avoid duplication
    header_text = "<b><font size='24' color='#1A2A40'>ANDRES O. SOTO</font></b><br/><font size='12' color='#334155'>Partner | Mills Shirley LLP</font><br/><font size='9' color='#6b7280'>2200 Market St, Suite 300 | Galveston, TX 77550 | (409) 761-4035 | asoto@millsshirley.com</font>"
    story.append(Paragraph(header_text, ParagraphStyle('Header', alignment=TA_CENTER, spaceAfter=20)))

    # Biography
    story.append(Paragraph("PROFESSIONAL PROFILE", styles['SectionHeader']))
    story.append(Paragraph(
        "Partner in the litigation section of Mills Shirley LLP. Represents clients in commercial, construction, maritime, insurance defense, and civil disputes. Practice includes both trial and appellate work, with a particular focus on construction, design, and commercial litigation. Based in Houston and Galveston, advising a range of businesses, owners, and insurers.",
        styles['ResumeBody']
    ))

    # Practice Areas
    story.append(Paragraph("PRACTICE AREAS", styles['SectionHeader']))
    practices = [
        "Commercial Litigation", "Construction Litigation", "Maritime / Admiralty Litigation",
        "Insurance Defense", "Civil Disputes", "Transportation Law"
    ]
    for p in practices:
        story.append(Paragraph(f"• {p}", styles['ResumeBullet']))

    # Education
    story.append(Paragraph("EDUCATION", styles['SectionHeader']))
    story.append(Paragraph("J.D., The University of Texas School of Law, 2009", styles['ResumeBody']))
    story.append(Paragraph("Gardere & Wynne Endowed Outstanding Student Award", styles['ResumeBullet']))
    story.append(Paragraph("B.A., Rice University, 2006 — Major: English & Philosophy", styles['ResumeBody']))
    story.append(Paragraph("Presidential Achievement Award", styles['ResumeBullet']))

    # Bar Admissions
    story.append(Paragraph("BAR ADMISSIONS", styles['SectionHeader']))
    story.append(Paragraph("Texas | U.S. District Court, Southern District of Texas | U.S. Court of Appeals, Fifth Circuit", styles['ResumeBody']))

    # Professional Memberships
    story.append(Paragraph("PROFESSIONAL MEMBERSHIPS", styles['SectionHeader']))
    memberships = [
        "Galveston County Bar Association, Past President",
        "Galveston County Bar Association – Young Lawyers Section, Past President",
        "Texas Association of Defense Counsel, District #9 Director",
        "State Bar of Texas",
        "U.S. Federal Bar"
    ]
    for m in memberships:
        story.append(Paragraph(f"• {m}", styles['ResumeBullet']))

    # Representative Matters
    story.append(Paragraph("REPRESENTATIVE MATTERS", styles['SectionHeader']))
    matters = [
        "Representing companies in commercial supply contract disputes",
        "Counseling businesses on interstate and international transportation regulations",
        "Representing owners and contractors in construction defect litigation",
        "Defending insurers in bad faith insurance settlement cases",
        "Litigating debt collection and breach of contract matters for businesses",
        "Representing marine suppliers and ship owners in admiralty claims"
    ]
    for m in matters:
        story.append(Paragraph(f"• {m}", styles['ResumeBullet']))

    # Recognition & Awards
    story.append(Paragraph("RECOGNITION & AWARDS", styles['SectionHeader']))
    story.append(Paragraph("• Texas Super Lawyers – Rising Star, 2020–2022", styles['ResumeBullet']))
    story.append(Paragraph("• Galveston County Outstanding Young Lawyer, 2015", styles['ResumeBullet']))

    # Community Involvement
    story.append(Paragraph("COMMUNITY INVOLVEMENT", styles['SectionHeader']))
    community = [
        "Wills for Heroes, 2011",
        "Court Appointed Special Advocate, 2009",
        "Veterans' Clinic volunteer",
        "Galveston County Share Your Holiday Food Drive",
        "Resides in League City with his wife and sons, Samuel and Simon"
    ]
    for c in community:
        story.append(Paragraph(f"• {c}", styles['ResumeBullet']))

    # Footer
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "Mills Shirley LLP | Texas's Oldest Continuously Operating Law Firm | Established 1846",
        ParagraphStyle('Footer', fontSize=8, textColor=GRAY, alignment=TA_CENTER)
    ))

    doc.build(story)
    print(f"Generated: {output_path}")

if __name__ == '__main__':
    create_resume()
