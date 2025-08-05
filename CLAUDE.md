# Mills Shirley LLP Website Project

## Project Overview
Static website for Mills Shirley LLP, Texas's oldest continuously operating law firm (established 1846). Professional law firm website with custom typography, responsive design, and data-driven content generation.

## Key Technologies
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Typography**: Custom Equity Text and Equity Caps fonts
- **Content**: Generated from structured .txt data files
- **Responsive**: Mobile-first design with sticky navigation

## Project Structure

### Core Pages
- **Homepage** (`/index.html`): Hero section, about, two-tiered practice areas, attorney preview, contact
- **Attorney Profiles** (`/attorneys/`): Individual pages generated from data files
- **Practice Areas** (`/practice-areas/`): Two-tiered structure (Litigation/Transactional)
- **404 Page** (`/404.html`): Custom error page with helpful navigation

### Directory Structure
```
/
├── index.html                          # Homepage
├── 404.html                           # Error page
├── assets/
│   ├── css/styles.css                 # Custom CSS with @font-face declarations
│   ├── js/scripts.js                  # Navigation and interactions
│   ├── favicon/favicon.png            # Site favicon
│   └── fonts/equity/                  # Equity Text/Caps TTF files
├── attorneys/                         # Generated attorney profile pages
├── practice-areas/
│   ├── litigation/                    # Litigation practice area pages
│   ├── transactional/                 # Transactional practice area pages
│   └── trusts-and-estates/            # Trusts and estates practice area pages
└── data/                             # Source data files
    ├── attorneys/                     # Attorney .txt files
    └── practice-areas/               # Practice area .txt files
        ├── litigation/
        ├── transactional/
        └── trusts-and-estates/
```

## Data-Driven Content

### Attorney Profiles
**Source**: `/data/attorneys/*.txt`
**Generated Pages**: `/attorneys/*.html`

**Current Attorney Files**:
- `andy-soto.txt` → `andy-soto.html`
- `fred-raschke.txt` → `fred-raschke.html`
- `gus-knebel.txt` → `gus-knebel.html`
- `jack-brock.txt` → `jack-brock.html`
- `jessica-conley.txt` → `jessica-conley.html`
- `maureen-mccutchen.txt` → `maureen-mccutchen.html`
- `rachel-delgado.txt` → `rachel-delgado.html`
- `robert-booth.txt` → `robert-booth.html`

### Practice Areas (Three-Tiered Structure)
**Source**: `/data/practice-areas/`
**Generated Pages**: `/practice-areas/[category]/[practice].html`

**Current Structure**:
- **Litigation**:
  - `commercial-litigation-and-business-disputes.txt` → `/practice-areas/litigation/commercial-litigation-and-business-disputes.html`
  - `construction-litigation-and-defect-claims.txt` → `/practice-areas/litigation/construction-litigation-and-defect-claims.html`
  - `insurance-coverage-and-defense.txt` → `/practice-areas/litigation/insurance-coverage-and-defense.html`
- **Transactional**:
  - `business-formation-and-governance.txt` → `/practice-areas/transactional/business-formation-and-governance.html`
  - `commercial-real-estate-transactions.txt` → `/practice-areas/transactional/commercial-real-estate-transactions.html`
  - `contract-negotiation-and-drafting.txt` → `/practice-areas/transactional/contract-negotiation-and-drafting.html`
- **Trusts and Estates**:
  - `estate-planning-and-asset-protection.txt` → `/practice-areas/trusts-and-estates/estate-planning-and-asset-protection.html`
  - `probate-and-guardianship-administration.txt` → `/practice-areas/trusts-and-estates/probate-and-guardianship-administration.html`
  - `trust-and-fiduciary-litigation.txt` → `/practice-areas/trusts-and-estates/trust-and-fiduciary-litigation.html`

## Typography System (Equity Fonts)

### Font Implementation
- **Primary Font**: Equity Text (body text, navigation)
- **Heading Font**: Equity Caps (headings, titles)
- **Fallbacks**: Georgia, serif (accessibility)
- **Location**: `/assets/fonts/equity/` (TTF format)

### CSS Implementation
```css
/* Global font families set in styles.css */
html, body { font-family: 'Equity Text', Georgia, serif; }
h1, h2, h3, h4, h5, h6 { font-family: 'Equity Caps', 'Equity Text', Georgia, serif; }
```

### Tailwind Configuration
All HTML files include custom Tailwind configuration:
```javascript
fontFamily: {
    'serif': ['Equity Text', 'Georgia', 'serif'],
    'sans': ['Equity Text', 'Georgia', 'serif'],
    'caps': ['Equity Caps', 'Equity Text', 'Georgia', 'serif']
}
```

## Content Management

### Adding New Attorneys
1. Create `.txt` file in `/data/attorneys/` following existing format
2. Generate HTML page using established template pattern
3. Update homepage attorney preview section if needed

### Adding New Practice Areas
1. Create `.txt` file in appropriate `/data/practice-areas/[category]/` directory
2. Generate HTML page in corresponding `/practice-areas/[category]/` directory
3. Update homepage practice areas section to include new practice

### Data File Format
**Attorney Files**:
```
Name: [Full Name]
Title: [Position]
Phone: [Direct Phone]
Office: [Office Location]
Bio: [Biography paragraph]
Education: [Degree info]
Bar Admissions: [Admission details]
Specialties: [Practice areas]
```

**Practice Area Files**:
```
Title: [Practice Area Name]
Slug: [url-slug]
Short Description: [Brief description]
Full Description: [Detailed content]
Representative Services: [Bullet points]
Related Attorneys: [Attorney names]
Related Keywords: [SEO keywords]
```

## Design System (Apple-Inspired)

### Color Palette
- **Navy-900**: #1A2A40 (primary brand color)
- **Navy Palette**: 50-950 range with sophisticated variations
- **Light Gray**: #f9fafb (background sections)
- **Sage Accents**: Complementary neutral palette
- **8px Base Spacing**: Mathematical spacing system

### Component Patterns
- **Hero Sections**: Navy background, white text, centered content
- **Practice Area Cards**: White background, shadow, hover effects
- **Attorney Profiles**: Circular images, contact cards, biographical layout
- **Navigation**: Sticky header, mobile hamburger menu

## Recent Major Changes

### Professional Design Refinement & Performance Optimization (Latest)
- **Navigation Enhancement**: Refined navbar with 72px height, improved spacing, and professional minimalistic design
- **Performance Optimization**: Replaced expensive CSS animations with hardware-accelerated transitions using `translate3d()` and `will-change` properties
- **Attorney Section Standardization**: Enhanced attorney cards with 40px padding, standardized typography, and consistent design across all profiles
- **Footer Standardization**: Unified footer design across all 20+ pages with consistent navy color scheme, removed taglines, and centered copyright text
- **Animation Performance**: Eliminated laggy animations by optimizing CSS transitions and using specific property animations instead of `transition: all`
- **Typography Hierarchy**: Standardized `font-caps` for headings, `font-serif` for body text
- **Color System**: Unified navy-900 usage, refined palette with 50-950 variations
- **Font Loading**: Fixed critical @font-face paths for proper Equity font display
- **Component Consistency**: Standardized buttons, cards, navigation across all 20+ pages
- **Tailwind Configuration**: Unified advanced config across all HTML files
- **8px Spacing System**: Mathematical spacing for Apple-style precision

### Practice Area Expansion
- **Previous Structure**: Two-tiered with 3 total practices (Litigation: 2, Transactional: 1)
- **New Structure**: Three-tiered with 9 total practices across 3 categories
- **Added Category**: Trusts & Estates with 3 specialized practices
- **Expanded Categories**: Litigation (3 practices) and Transactional (3 practices)
- **Homepage Update**: Updated to 3-column layout showcasing all categories
- **URL Changes**: All practice area URLs follow nested pattern with new category

### Font Implementation
- Added Equity Text and Equity Caps @font-face declarations
- Updated all HTML files with custom Tailwind font configurations
- Overrode default fonts with Equity fonts throughout site
- Maintained accessibility with proper fallback stacks

### Attorney Profile Generation
- Generated 8 individual attorney pages from data files
- Updated homepage to display attorney preview cards
- Implemented consistent attorney profile template

## Development Guidelines

### File Naming Conventions
- **Attorneys**: `firstname-lastname.html` (lowercase, hyphenated)
- **Practice Areas**: `practice-name.html` (lowercase, hyphenated)
- **Data Files**: Match HTML filename with `.txt` extension

### CSS and JavaScript
- **Custom CSS**: `/assets/css/styles.css` (global styles, font declarations, performance optimizations)
- **JavaScript**: `/assets/js/scripts.js` (navigation, mobile menu)
- **Tailwind**: CDN-based with inline configuration per page
- **Performance**: Hardware-accelerated animations, CSS containment, and optimized transitions

### Responsive Design
- **Breakpoints**: Mobile-first approach using Tailwind classes
- **Navigation**: Collapsible mobile menu with hamburger icon
- **Layout**: Grid systems adapt from 1-column (mobile) to multi-column (desktop)

## Contact Information
- **Galveston Office**: (409) 763-2341
- **Houston Office**: (713) 242-1880
- **Email**: info@millsshirley.com

## Important Notes
- **Typography**: Use `font-caps` for all headings, `font-serif` for body text
- **Colors**: Use `navy-900` for primary navy, avoid bare `navy` references
- **Fonts**: Equity fonts now load properly via corrected @font-face paths
- **Consistency**: All 20+ pages share unified Tailwind configuration
- **Practice Areas**: Content generated from .txt data files in nested structure
- **Attorney Profiles**: Auto-generated from data - don't manually edit
- **URL Structure**: Nested pattern `/practice-areas/[category]/[practice].html`
- **Navigation**: Optimized navbar with 72px height and professional spacing
- **Spacing**: Follow 8px base unit system for Apple-style precision
- **Components**: All buttons, cards, and interactive elements follow design system
- **Performance**: All animations use hardware acceleration for smooth performance
- **Footers**: Standardized across all pages with consistent navy color scheme and centered copyright

## Future Considerations
- Consider adding more practice areas to existing categories
- Potential for adding blog/news section
- Integration with contact form backend
- Performance optimization for font loading
- Addition of practice area category landing pages