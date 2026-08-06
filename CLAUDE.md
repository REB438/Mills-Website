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
- **Homepage** (`/index.html`): Hero section, about, four practice categories, attorney preview, contact
- **About** (`/about.html`): Firm history narrative and timeline
- **Attorney Profiles** (`/attorneys/`): Individual pages generated from data files, plus
  `/attorneys/index.html` as the team landing page
- **Practice Areas** (`/practice-areas/`): Four categories (Litigation, Transactional,
  Employment, Trusts & Estates), each with a landing page and detail pages
- **404 Page** (`/404.html`): Custom error page with helpful navigation

34 HTML files in total: 27 real pages plus 7 redirect stubs under `/attorney/` and
`/estate-trusts-and-guardianship/` that preserve legacy URLs.

### Directory Structure
```
/
├── index.html                          # Homepage
├── about.html                          # Firm history
├── 404.html                            # Error page
├── assets/
│   ├── css/styles.css                  # Custom CSS
│   ├── js/scripts.js                   # Navigation and interactions
│   ├── js/tailwind-config.js           # Shared Tailwind config for every page
│   ├── js/performance.js               # Perf helpers (loaded on 4 pages only)
│   ├── favicon/favicon.png             # Site favicon
│   ├── img/attorneys/                  # Attorney portraits (.webp + .jpg)
│   ├── pdf/, vcf/                      # Resumes and contact cards
│   └── fonts/equity/                   # UNUSED: Equity TTFs, retired in favour of Inter
├── attorneys/                          # Attorney profile pages + index.html
├── practice-areas/                     # index.html + one folder per category
│   ├── litigation/                     # index.html + 3 detail pages
│   ├── transactional/                  # index.html + 3 detail pages
│   ├── employment/                     # index.html + 3 detail pages
│   └── trusts-and-estates/             # index.html + 3 detail pages
├── attorney/                           # Legacy redirect stubs (JS redirect)
├── estate-trusts-and-guardianship/     # Legacy redirect stub (meta refresh)
└── data/                               # Source data files
    ├── attorneys/                      # Attorney .txt files
    └── practice-areas/                 # Practice area .txt files
        ├── litigation/
        ├── transactional/
        ├── employment/
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
- `maureen-mccutchen.txt` → `maureen-mccutchen.html`
- `rachel-delgado.txt` → `rachel-delgado.html`
- `robert-booth.txt` → `robert-booth.html`

### Practice Areas (Four Categories)
**Source**: `/data/practice-areas/`
**Generated Pages**: `/practice-areas/[category]/[practice].html`

Each category also has a landing page at `/practice-areas/[category]/index.html`, and
`/practice-areas/index.html` lists all four.

**Current Structure** (4 categories, 12 practices):
- **Litigation**:
  - `commercial-litigation-and-business-disputes.txt` → `/practice-areas/litigation/commercial-litigation-and-business-disputes.html`
  - `construction-litigation-and-defect-claims.txt` → `/practice-areas/litigation/construction-litigation-and-defect-claims.html`
  - `insurance-coverage-and-defense.txt` → `/practice-areas/litigation/insurance-coverage-and-defense.html`
- **Transactional**:
  - `business-formation-and-governance.txt` → `/practice-areas/transactional/business-formation-and-governance.html`
  - `commercial-real-estate-transactions.txt` → `/practice-areas/transactional/commercial-real-estate-transactions.html`
  - `contract-negotiation-and-drafting.txt` → `/practice-areas/transactional/contract-negotiation-and-drafting.html`
- **Employment**:
  - `employer-representation-and-compliance.txt` → `/practice-areas/employment/employer-representation-and-compliance.html`
  - `employment-litigation-and-disputes.txt` → `/practice-areas/employment/employment-litigation-and-disputes.html`
  - `workplace-safety-and-eeoc-matters.txt` → `/practice-areas/employment/workplace-safety-and-eeoc-matters.html`
- **Trusts and Estates**:
  - `estate-planning-and-asset-protection.txt` → `/practice-areas/trusts-and-estates/estate-planning-and-asset-protection.html`
  - `probate-and-guardianship-administration.txt` → `/practice-areas/trusts-and-estates/probate-and-guardianship-administration.html`
  - `trust-and-fiduciary-litigation.txt` → `/practice-areas/trusts-and-estates/trust-and-fiduciary-litigation.html`

## Typography System (Inter)

### Font Implementation
- **All text**: Inter, loaded from Google Fonts via `@import` at the top of `styles.css`
- **Fallbacks**: `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, Roboto, Helvetica Neue, Arial, sans-serif
- **Equity is retired.** The site was migrated from Equity Text/Caps to Inter. The
 `@font-face` blocks, `<link rel="preload">` tags, and service worker precache entries
 have been removed. The TTF files still sit in `/assets/fonts/equity/` but are unreferenced.

### CSS Implementation
```css
/* Global font families set in styles.css */
html, body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, ...; }
h1, h2, h3, h4, h5, h6 { font-family: 'Inter', -apple-system, BlinkMacSystemFont, ...; }
```

### Tailwind Configuration
Centralized in `/assets/js/tailwind-config.js` and loaded by every page via
`<script src=".../tailwind-config.js?v=N">`. It is **not** duplicated per page.

`font-serif`, `font-sans`, and `font-caps` all resolve to the same Inter stack. The
`caps`/`serif` keys are kept only because ~34 pages still carry those classes; they are
no longer meaningful distinctions and new markup should not rely on them.

### Spacing scale caution
The config **overrides Tailwind's default spacing scale with roughly half the usual
values** (`'8': '1rem'` rather than `2rem`, `'12': '1.5rem'` rather than `3rem`). So
`gap-8` is 16px and `w-12` is 24px, not the 32px/48px a stock Tailwind mental model
predicts. Check `tailwind-config.js` before reasoning about any spacing utility.

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
- **Current Structure**: 12 practices across 4 categories
- **Added Categories**: Trusts & Estates, then Employment, each with 3 practices
- **Landing Pages**: `/practice-areas/index.html` plus one `index.html` per category
- **Homepage Update**: Lists all four categories with their practices
- **URL Changes**: All practice area URLs follow the nested `[category]/[practice]` pattern

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
- **Typography**: Everything is Inter. `font-caps`/`font-serif` are legacy no-ops kept for
 existing markup; don't add them to new markup
- **Colors**: Use `navy-900` for primary navy, avoid bare `navy` references
- **Headings on dark sections need an explicit `text-white`**: `styles.css` sets
 `h1..h6 { color: #0f172a }`. An element-targeted rule beats an inherited value, so a
 heading inside a `text-white` dark section stays navy and can end up invisible against
 the navy background. Put the color class on the heading itself, not just the section
- **No `sage` accent**: the palette is monochrome navy. The old `bg-sage`/`text-sage-*`
 classes were never defined in the Tailwind config (they rendered transparent) and have
 been replaced with navy equivalents. Don't reintroduce them
- **Consistency**: All 34 pages share the centralized config at `/assets/js/tailwind-config.js`
- **Cache busting**: `styles.css` and `tailwind-config.js` are versioned with `?v=N`. Bump
 the query in all HTML files *and* `CACHE_NAME` in `sw.js` whenever either changes, since
 the service worker is cache-first
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
- Delete the unused `/assets/fonts/equity/` TTFs now that the site runs on Inter
- Trim the remaining legacy `font-caps`/`font-serif` classes from markup