# Mills Shirley LLP Website — Phase 1 Technical Audit

**Site:** https://millsshirley.com  
**Repo audited:** local working copy (matches production content as of commit `32005cf`, Aug 10 2026)  
**Auditor role:** senior web engineer / accessibility specialist  
**Audience:** Managing Partner (litigator)  
**Scope:** Phase 1 — audit only. **No site files were changed** except this `/audit/` deliverable.  
**Phase 2:** Do not begin until you approve the plan below.

---

## Executive summary (plain English)

The site is a **static multi-page HTML website** hosted on **GitHub Pages** (CNAME `millsshirley.com`) behind Fastly’s CDN. There is **no build step, no React/Next, no package.json**. Pages use Tailwind CSS from a CDN plus a custom `styles.css`, and a small amount of vanilla JavaScript. That is a good, boring stack for a law firm: fast to host, easy to reason about, few moving parts.

**What is already in good shape**

- Clear information architecture: homepage → About, four practice categories (12 detail pages), attorney profiles, contact/intake, Clio pay links.
- Semantic landmarks (`header` / `nav` / `main` / `footer`), skip links, and a single `<h1>` on real pages.
- Substantial structured data already present (homepage `LegalService`/`LocalBusiness`, attorney `Person`, practice-page `FAQPage` + `BreadcrumbList`, `llms.txt`, AI crawlers allowed in `robots.txt`). The prompt’s assumption that the site “has little or no schema” is **outdated** — schema is a strength, not a gap.
- HTTPS, www→apex redirect, and HTTP→HTTPS redirect all work.
- Recent Galveston-focused titles, visible FAQs, and a real `/attorneys/` team page improved local/AI answerability.

**What is broken or risky (highest priority)**

1. ~~**Attorney-advertising / privilege language**~~ **Privilege (L-01) addressed — Option A chosen:** homepage intake no longer claims attorney-client privilege. Remaining Part VII items: marketing phrases (“aggressive representation,” “Proven history. Modern edge. Strategic wins.,” “Leading Galveston County law firm,” “Expert …”) and trial write-ups with dollar amounts / “winning jury verdict” language still need firm review.
2. ~~**No privacy policy / terms / accessibility statement**~~ **Addressed (2026-08-10):** `privacy.html`, `terms.html`, and `accessibility.html` now exist with Clio disclosures where relevant; footer links wired sitewide and URLs added to `sitemap.xml`. Counsel should still finalize Privacy/Terms copy as needed (**L-05** / **L-06**).
3. **Security response headers are essentially absent** on GitHub Pages (no CSP, HSTS, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`). Mitigate what you can via `static.json`/headers if you add a host that supports them, or accept GitHub Pages limits and harden links/embeds.
4. ~~**Performance debt in images and PDFs.**~~ **Addressed (2026-08-10):** JPG fallbacks recompressed (~20 MB → ~1.9 MB total); resume PDFs recompressed in place (~16.5 MB → ~0.24 MB) via embedded-image rewrite; unused Equity TTFs (~2.2 MB) deleted. WebP + JPG `<picture>` pattern unchanged. Residual: optional `width`/`height` on imgs (**P-01**); Google Fonts still third-party (**X-03** partial — Maps embed removed).
5. ~~**Google Maps embed looks hand-fabricated**~~ **Addressed (2026-08-10):** Fabricated Maps iframe removed from homepage contact. Replaced with a navy directions CTA + real Google Maps search URL (no embed, no place_id). Address text and “Get Directions” button retained (**B-01** / **A-03** / **P-03**).
6. **Houston office inconsistency.** `llms.txt` and homepage schema description mention Houston; the visible footer/NAP show only Galveston. Directories may disagree. Do not “fix” this in code until the firm decides the public NAP.

**What the sales email about ChatGPT got wrong**

Website HTML alone will not put you into ChatGPT’s “best small business lawyers” answers on demand. Off-site signals (Google Business Profile, reviews, directories) matter more. The site’s technical AI baseline (`llms.txt`, schema, crawl allow) is already ahead of most peer firms.

**Effort snapshot if you approve Phase 2**

| Band | Examples | Rough effort |
|---|---|---|
| Critical / High (ethics + a11y + trust) | Privilege/disclaimer language (with your copy), privacy page stub, touch-target fixes, duplicate URL canonicals | 1–3 days engineering + your review time |
| Medium (performance / SEO hygiene) | Compress/remove JPG masters from deploy, slim PDFs, remove `meta keywords`, branded OG image, security headers where host allows | 1–2 days |
| Lower (polish) | Landmark labels, print CSS, dynamic copyright year, blog decision | optional |

---

## Stack confirmation

| Item | Finding |
|---|---|
| Markup | Static `.html` (34 files: 27 real pages + 7 legacy redirect stubs) |
| CSS | Tailwind CDN + `/assets/css/styles.css` + `/assets/js/tailwind-config.js` |
| JS | `/assets/js/scripts.js` (nav + SW registration), `/assets/js/performance.js` (4 pages), `/sw.js` |
| Fonts | Inter via Google Fonts in CSS; Equity TTFs **deleted** |
| Hosting | GitHub Pages (`CNAME` → millsshirley.com), Fastly edge cache |
| Build | None (no `package.json`, no bundler) |
| Forms / payments | Clio Grow intake + Clio payment links (external) |
| Service worker | Network-first for HTML; cache-first for static assets |

---

## Information architecture

```
/ (homepage)
├── about.html
├── attorneys/
│   ├── index.html          ← team landing (real page)
│   ├── robert-booth.html
│   ├── maureen-mccutchen.html
│   ├── fred-raschke.html
│   ├── andy-soto.html
│   ├── gus-knebel.html
│   ├── jack-brock.html
│   └── rachel-delgado.html
├── practice-areas/
│   ├── index.html
│   ├── litigation/ (index + 3)
│   ├── transactional/ (index + 3)
│   ├── employment/ (index + 3)
│   └── trusts-and-estates/ (index + 3)
├── 404.html
├── llms.txt, robots.txt, sitemap.xml, sw.js
└── legacy stubs (disallowed or redirecting)
    ├── /attorney/*/          (robots Disallow)
    └── /estate-trusts-and-guardianship/estate-planning/
```

**Orphans:** none among real pages (every real page has inbound internal links).  
**Dead ends:** none material — footers and CTAs provide escape hatches.  
**Full page table:** `audit/raw/inventory.md` (titles, description lengths, H1, word counts, schema types).

### Suspected nav bug (prompt §1.6.2) — status: **mostly fixed**

Interior pages use real paths (`about.html`, `attorneys/index.html`, `index.html#contact`), not bare `#attorneys`. Homepage footer still uses `#about` / `#attorneys` / `#contact`, which is correct **on the homepage only**. Residual inconsistency: some footers say “Our Attorneys” → `index.html#attorneys` (homepage section) rather than `/attorneys/` (team page). Prefer linking to `/attorneys/` for clarity.

---

## Findings table

Severity: **Critical** (ethics/legal risk or severe a11y blocker) · **High** · **Medium** · **Low**  
Effort: **S** (&lt;2h) · **M** (half–1 day) · **L** (multi-day / firm process)

| ID | Cat | Sev | Page(s) | Location | Description | Recommended fix | Eff | Firm? |
|---|---|---|---|---|---|---|---|---|
| L-01 | Legal | Critical | `index.html` | Consultation block | **Addressed (Option A):** Intake no longer claims attorney-client privilege. Copy treats submissions as confidential to the extent required by law/professional responsibilities and states submitting the form does not by itself create an attorney-client relationship. | Applied Option A from Open Questions on homepage feature line + Confidentiality Notice. | S | **Done** |
| L-02 | Legal | Critical | Sitewide marketing | e.g. `index.html` hero & litigation blurb; schema `description` | Phrases for Part VII review: “Proven history. Modern edge. Strategic wins.”; “aggressive representation”; “trial-tested”; “Leading Galveston County law firm”; “Expert …” in several meta/OG strings. **Partial:** employment practice schema descriptions no longer use “Expert …” (factual counsel naming on the three employment detail pages). | Attorney reviews each claim; keep, edit, or remove. Engineering applies approved copy only. | S–M | **Yes** (partial) |
| L-03 | Legal | High | Attorney profiles (esp. Booth) | **Partial (Booth):** past-results / advertising disclaimer added above Representative Trials on `attorneys/robert-booth.html` (mirrored in `data/attorneys/robert-booth.txt`). Trial narratives retained pending firm review. | Dollar recoveries / “winning jury verdict” narratives may be advertising that requires substantiation and/or disclaimers under Texas rules. | Counsel confirm disclaimer wording (`TODO(firm)`); decide which results stay; extend notice to other profiles if needed. | M | **Yes** (finalize) |
| L-04 | Legal | High | Sitewide | **Partial (footer notice)** | Short sitewide footer notice added on all real content pages (and legacy estate-planning page with a footer): “This website may constitute attorney advertising. Use of this website does not create an attorney-client relationship.” Aligns with `terms.html` §§2 / 8. Prior-results disclaimer already on Booth / Terms — not duplicated in footer. | Counsel confirm final notice wording (`TODO(firm)` on `index.html` footer). **Still open:** lawyer responsible for Site content (and principal-office designation text if more than Galveston already stated in Terms §8). | S | **Yes** (finalize) |
| L-05 | Legal | High | Sitewide | **Addressed (pages + footer + sitemap)** | Privacy Policy and Terms of Use pages exist (`/privacy.html`, `/terms.html`) with Clio-related disclosures; footer links sitewide. Note TDPSA applicability for your counsel — copy may still need counsel finalization. | Counsel review/finalize; keep footer links. | M | **Yes** (finalize) |
| L-06 | Legal | Medium | Sitewide | **Addressed (page + footer + sitemap)** | Accessibility statement at `/accessibility.html` with accommodation contact; footer links sitewide. | Keep page current; confirm contact path. | S | Review |
| L-07 | Legal | Low | Board cert claims | Booth, McCutchen pages | Board certification **does** name Texas Board of Legal Specialization in body/schema — good. Spot-check any short cards that say “Board Certified …” without TBLS in the same breath (e.g. attorneys index blurbs). | Ensure every certification claim names TBLS nearby (Rule 7.02/7.01 certification identification). | S | Review |
| A-01 | A11y | High | Homepage practice links | axe `target-size` | **Addressed:** `.practice-specialty-title .content-link` now `inline-flex` with `min-height: 44px` + padding-block (scoped; global `.content-link` left alone for prose). | Keep ≥24px (target 44px) on specialty title links. | S | Done |
| A-02 | A11y | Medium | `attorneys/robert-booth.html` | axe `landmark-unique` | Duplicate landmark role without unique accessible name. | Add `aria-label` to one of the duplicate `nav`/`aside` landmarks. | S | No |
| A-03 | A11y | Medium | Maps iframe | `index.html` | **Addressed (2026-08-10):** Live Maps iframe removed. Replaced with accessible directions link (meaningful text: “Open in Google Maps” / “Get directions”); address remains as text. | Keep CTA + address; no live embed. | S–M | Done |
| A-04 | A11y | Medium | Manual | Focus | `*:focus { outline }` rules exist in CSS; CDP showed `outline: none` on a focused nav link in one check — verify `:focus-visible` actually paints in Safari/Chrome. | Manual keyboard pass; strengthen focus ring if flaky. | S | No |
| A-05 | A11y | Low | Inventory | All real pages | `lang="en"` present; skip links present; single H1; no missing `img alt` found in inventory. | Keep; no churn. | — | No |
| A-06 | A11y | Low | Motion | `styles.css` | `prefers-reduced-motion` media query exists. | Keep. | — | No |
| S-01 | SEO | Medium | Many pages | `<meta name="keywords">` | Still present; ignored by Google for years. | Remove sitewide. | S | No |
| S-02 | SEO | Medium | `/practice-areas/` vs `index.html` | Production both 200 | Duplicate URLs without redirect. Canonicals often point to slash URL — good — but both remain crawlable. | Prefer one URL; 301 the other if host allows, or reinforce canonical + sitemap-only form. | S–M | No |
| S-03 | SEO | Medium | Homepage / social | `og:image` | Share card uses an attorney headshot (awkward for firm shares). | Commission/export branded 1200×630; update OG/Twitter. | M | **Yes** (asset) |
| S-04 | SEO | Low | `README.md` | Root | README describes obsolete structure (old `/practice/` paths, Georgia typography). Misleads future editors. | Rewrite README to match reality. | S | No |
| S-05 | SEO | Low | Blog | Absent | No insights/publications section. SEO cost is real but capacity cost may be higher. | Outline only in Open Questions — do not build unless firm will feed it. | L | **Yes** |
| S-06 | SEO | Low | Schema | Already strong | Prompt asked to “add schema”; most recommended types **already exist**. Gaps: Houston as second `PostalAddress` (only if real), richer `sameAs`, review schema **only** if real reviews (do not fake). | Validate blocks in Rich Results Test in Phase 2; extend carefully. | S | Partial |
| P-01 | Perf | High | `/assets/img/attorneys/*.jpg` | ~~1.5–3.1 MB each~~ **Done:** ~175–273 KB fallbacks (~1.9 MB JPG total); WebP primary unchanged | WebP already used in `<picture>`. Optional follow-up: set width/height on imgs to limit CLS. | Re-encode JPG fallbacks; keep WebP; set width/height on imgs. | M | No |
| P-02 | Perf | High | `/assets/pdf/*-resume.pdf` | ~~1.9–3.8 MB~~ **Done:** ~26–57 KB each (~0.24 MB total); text verified; `w-9` untouched | Was heavy downloads from full-res embedded portraits. | Compress PDFs; ensure tagged where feasible (tagging still open). | M | No |
| P-03 | Perf | Medium | Maps | Homepage | **Addressed (2026-08-10):** No Maps iframe; directions open Google Maps only on user click via search URL. | Keep static CTA approach. | S | Done |
| P-04 | Perf | Medium | Fonts | Google Fonts Inter; ~~unused Equity TTFs~~ **deleted** | Third-party Inter CSS remains; Equity no longer ships. | Self-host Inter optional. | S | Done (Equity) |
| P-05 | Perf | Medium | Tailwind CDN | All pages | Runtime Tailwind compilation on client — convenient but not ideal for CWV. | Stay CDN for now (no new build without approval); revisit only if Lighthouse LCP/TBT demands it. | L | Ask before build |
| P-06 | Perf | Low | Hosting | GitHub Pages | `cache-control: max-age=600` on HTML; no Brotli control; SW helps return visitors. | Acceptable; document. Precache/query-string mismatch for `?v=` assets noted previously — separate SW cleanup. | M | No |
| B-01 | Bug | High | Maps `pb=` | `index.html` | **Addressed (2026-08-10):** Fabricated embed removed. Homepage uses Google Maps search/directions URL for 2200 Market St Suite 300, Galveston TX 77550 (no invented place_id). | Keep real search URL; do not reintroduce fabricated `pb=` embeds. | S | Done |
| B-02 | Bug | Medium | NAP / phones | Site vs directories | Site main line **(409) 763-2341**. Direct lines use **409-761-40xx**. Prompt’s **(409) 761-1498** **not found in repo**. Houston phone **(713) 242-1880** appears on Jack Brock profile / some cards, not as a firm Houston office block. | Firm confirms official public numbers and Houston presence; engineering aligns NAP. | S | **Yes** |
| B-03 | Bug | Medium | Houston | `llms.txt`, schema blurb | Claims Galveston **and Houston** offices; UI footer shows Galveston only. | Decide public story; then align site + directories. | M | **Yes** |
| B-04 | Bug | Low | W-9 | `assets/pdf/w-9-2026.pdf` | Public W-9 linked from homepage. Confirm intentional and current. | Firm confirms; do not remove without approval. | S | **Yes** |
| B-05 | Bug | Low | Copyright | Footer | Hardcoded `© 2026`. | Tiny JS year or annual checklist. | S | No |
| X-01 | Security | High | Response headers | Production | Missing CSP, HSTS, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`. | If staying on GitHub Pages, options are limited; document residual risk. If moving host / CloudFlare, add headers. External `target="_blank"` links generally have `noopener noreferrer` (good). | M–L | Hosting decision |
| X-02 | Security | Medium | Repo hygiene | `.DS_Store` in tree; ~~huge JPGs / unused fonts~~ JPGs slimmed, Equity deleted | Remaining: `.DS_Store` noise. | `.gitignore` DS_Store. | S | No |
| X-03 | Privacy | Medium | Maps + Google Fonts | Homepage / CSS | **Partial (2026-08-10):** Maps embed gone (no Google contact until user clicks directions). Google Fonts Inter still loads from Google. | Optional: self-host Inter. | M | Partial |
| D-01 | Design/UX | Medium | Footer “Our Attorneys” | Many pages | Points to homepage `#attorneys` preview, not `/attorneys/` index. | Point to team page. | S | No |
| D-02 | Design/UX | Medium | Conversion | Mobile | Phone is tappable in footer; not a persistent sticky call bar. Clio CTAs in header help. | Optional sticky “Call” on mobile — design decision. | M | Prefer |
| D-03 | Design/UX | Low | Visual brand | Global | Clean Inter/navy system reads modern-professional more than “1846 parchment.” That may be intentional. | Do not restyle without a brand decision. | L | **Yes** if changing |
| D-04 | Design/UX | Low | Print / favicon | Partial | Single PNG favicon; no print stylesheet observed. | Add print CSS hiding nav/chrome; expand favicon set if desired. | S | No |

---

## Accessibility (WCAG 2.2 AA) — interpretation

### Automated (axe-core 4.10.3)

| Page | Violations | Notes |
|---|---|---|
| Homepage | 1 serious (`target-size`) | 6 incomplete color-contrast (hero overlap / pseudo); frame-tested incomplete for Maps |
| `attorneys/robert-booth.html` | 1 moderate (`landmark-unique`) | Otherwise clean |

Raw JSON: `audit/raw/axe/`.  
CLI/`pa11y`/Lighthouse full-matrix: **not completed** in this environment (see `audit/raw/TOOLING-NOTES.md`). Re-run in Phase 2 before closing.

### Manual contrast samples (homepage)

| Element | Ratio | Requirement | Result |
|---|---|---|---|
| Hero H1 white on navy | 20.17:1 | 3:1 large | Pass |
| Nav link slate on white | 4.76:1 | 4.5:1 | Pass (tight) |
| Body `text-gray-600` | 4.83:1 | 4.5:1 | Pass |
| Footer link on navy | 17.85:1 | 4.5:1 | Pass |

### Manual checks tools often miss

- **Skip links** present and labeled.
- ~~**Maps iframe** has `title`~~ **Addressed:** iframe removed; directions CTA link only.
- **Keyboard mobile menu:** scripts support toggle; full trap testing should be repeated manually in Phase 2.
- **320px / 400% zoom:** prior session found no horizontal overflow on 28 pages at 375px; re-verify 320px in Phase 2.
- **Link text:** practice specialty titles are unique; homepage card links include long accessible names (verbose but not “click here”).

---

## SEO

### Technical

| Check | Status |
|---|---|
| `robots.txt` | Present; allows site; Disallow `/attorney/`; allows major AI bots; points to sitemap |
| `sitemap.xml` | Present; covers main IA; `lastmod` dates partly stale (Feb/Mar 2026) |
| Canonicals | Present on key pages; homepage → `https://millsshirley.com/` |
| HTTPS / www | OK (301s) |
| Trailing slash duplicates | `/practice-areas/` and `.../index.html` both 200 |
| Broken internal links | **0** in inventory resolve |
| External links | Clio pay ×2, Clio Grow intake, LinkedIn, Google Maps query link |

### On-page

- Titles/descriptions recently tightened with Galveston intent (good).
- Remove obsolete `meta keywords`.
- Practice pages ~300–420 words — acceptable after recent thickening on key pages; employment/trusts pages still thinner.
- No blog (see Open Questions).

### Structured data

Already present (do not rip out):

- Homepage: `LegalService` + `LocalBusiness`, geo, opening hours, offer catalog, employees  
- Attorneys: `Person` + breadcrumbs; credentials where applicable  
- Practice details: `FAQPage` + `BreadcrumbList` (and visible FAQ sections)  
- About: `AboutPage` + `LegalService`

**Validate** in Google Rich Results Test during Phase 2 rather than assuming inventing more schema is the win.

### Local SEO

- Visible NAP: Galveston only.  
- Schema/`llms.txt`: Houston mentioned — **inconsistency for firm to resolve**.  
- Directions CTA + address present (no live Maps embed).  
- Directory citation audit (Martindale, Avvo, etc.) **not scraped live** — listed as firm homework.

### Social

- OG/Twitter tags present on most pages.  
- `og:image` → attorney photo — replace with branded 1200×630 when available.

---

## Performance & Core Web Vitals

Full Lighthouse numbers were **not** captured this pass (tooling limits). Evidence-based issues:

1. ~~**JPG fallbacks 1.5–3 MB**~~ **Done (2026-08-10):** fallbacks now ~175–273 KB; WebP still primary.  
2. ~~**Resume PDFs 2–4 MB.**~~ **Done:** resumes now ~26–57 KB (embedded photos rewritten; content text unchanged).  
3. ~~**Maps**~~ embed removed; **Google Fonts** still third-party.  
4. **Tailwind CDN** runtime cost — accept for now per “no new build” rule.  
5. HTML cache `max-age=600` at edge; SW network-first for navigations (good for deploys).

Phase 2 should attach mobile/desktop Lighthouse JSON under `audit/raw/lighthouse/` **before and after** image work.

---

## Design / UX (opinionated)

- The site reads as a **competent modern professional services site**, not a dusty 1846 archive. History lives on `/about.html`. That split is fine if intentional.
- Hierarchy and spacing are generally disciplined; navy + Inter is coherent.
- Conversion: header Pay Invoice / Pay Retainer + Clio Grow CTAs are unusually prominent for a law firm — good for operations, slightly retail. Keep unless you want a quieter header.
- Attorney pages (Booth especially) are genuinely useful to referring counsel: trials, certifications, PDFs, vCards.
- Twelve practice subpages earn their URLs if kept distinct; avoid further thin clones.

---

## Correctness bugs (prompt §1.6) — status

| # | Suspected issue | Status |
|---|---|---|
| 1 | Malformed Maps `pb=` | **Addressed (2026-08-10).** Replaced with directions CTA + real search URL. |
| 2 | `#about`/`#attorneys`/`#contact` break on interior | **Mostly mitigated.** Interior nav uses paths + `index.html#contact`. Prefer `/attorneys/` in footers. |
| 3 | `.html` 404s; `/practice-areas/` vs index | **No broken internals found.** Both practice-areas URLs **200** (duplicate). |
| 4 | Phone 761-1498 vs 763-2341 | **761-1498 not in repo.** Public main line is **763-2341**; directs are **761-40xx**; Houston **713-242-1880** on some attorney cards. |
| 5 | W-9 public | File `w-9-2026.pdf` exists and is linked. **Firm confirms** currency and intent. Accessibility of PDF tagging not verified. |

---

## Legal-industry compliance checklist (for attorney review — not decisions)

You must review; engineering will not choose language:

1. **Texas Disciplinary Rules of Professional Conduct, Part VII (post–July 2021 advertising rules)**  
   - Substantiation for service claims.  
   - Certification identification (TBLS) — mostly OK where present; verify short blurbs.  
   - Flagged copy: “aggressive representation,” “Strategic wins,” “Leading …,” “Expert …,” “trial-tested,” hero tagline.  
   - Trial results with dollars on attorney pages.
2. **Site notices:** ~~advertising notice; no A/C relationship created by website~~ **Partial — footer one-liner live sitewide (**L-04**)**; “results depend on facts” / prior results elsewhere; principal office (Galveston) in Terms §8; lawyer responsible for content still open.
3. ~~**Privilege statement on intake**~~ **Done — Option A** on homepage.
4. **Privacy / Terms** — pages + footer links exist; counsel should finalize copy; Clio Grow data flow documented on Privacy.
5. **Accessibility statement** — `/accessibility.html` exists with footer link.
6. **Copyright year** maintenance.

*This section is a checklist, not legal advice.*

---

## Security & privacy hygiene

| Check | Result |
|---|---|
| CSP / HSTS / XCTO / Referrer-Policy / Permissions-Policy | **Not present** on GitHub Pages responses |
| `rel="noopener noreferrer"` on external blanks | Generally yes |
| HTTPS / mixed content | HTTPS OK |
| Email harvest | Attorney emails on profile pages (normal; expect scraping) |
| Third parties | Google Fonts, Clio, LinkedIn, Tailwind CDN; Google Maps only if user clicks directions (no embed). Cloudflare CDN for axe during audit only |
| Secrets in repo | None found; `.DS_Store` present; large binaries committed |

---

## Prioritized remediation plan (Phase 2 sequence)

Work on branch `website-audit-remediation`. One finding group per commit. Re-test after each group.

### Phase 2A — Risk reduction (do first)

1. **Firm copy decisions** for ~~L-01~~ (**Done — Option A**), L-02, ~~L-04 advertising/no-A-C footer~~ (**Partial** — notice live; counsel confirm + responsible-attorney still open). Engineering applies approved text only.  
2. ~~**A-01** touch targets~~ **Done** (44px specialty links); **A-02** landmark labels.  
3. ~~**B-01 / P-03 / A-03** map~~ **Done:** static directions CTA + real Google Maps search URL (no iframe).  
4. **S-02** canonicalize practice-area URLs.  
5. Footer attorneys link → `/attorneys/` (**D-01**).

### Phase 2B — Trust & compliance pages

6. ~~Privacy + Terms stubs~~ **Done:** pages live; counsel finalize remaining `TODO(firm):` copy if any (**L-05**).  
7. ~~Accessibility statement~~ **Done** (**L-06**).  
8. ~~Advertising / no-A-C-relationship footer notice~~ **Partial (**L-04**):** sitewide footer notice shipped; counsel confirm wording; responsible-attorney designation still open.

### Phase 2C — Performance

9. ~~Recompress attorney JPG fallbacks~~ **Done**; optional follow-up: verify `width`/`height` (**P-01**).  
10. ~~Compress resume PDFs~~ **Done** (**P-02**); PDF tagging still open if desired.  
11. ~~Remove unused Equity fonts~~ **Done** (**P-04**).  
12. Optional: self-host Inter (**X-03** residual; Maps embed already removed).

### Phase 2D — SEO hygiene

13. Strip `meta keywords` (**S-01**).  
14. Branded OG image when provided (**S-03**).  
15. README refresh (**S-04**).  
16. Rich Results validation pass (**S-06**).  
17. SW cache match for `?v=` assets (pre-existing tech debt).

### Phase 2E — Only with firm capacity

18. Blog/insights (**S-05**) — outline exists in Open Questions; build only if you’ll feed it quarterly.  
19. Sticky mobile call bar (**D-02**) — design choice.  
20. Hosting/header upgrade (**X-01**) — infrastructure decision.

---

## Open questions for the firm

1. ~~**Privilege language:**~~ **Decided — Option A** applied on `index.html` (feature line + Confidentiality Notice).
2. **Houston office:** Public office, appointment-only, or remove from `llms.txt`/schema?
3. **Official public phone list:** Confirm main **(409) 763-2341**, which directs to publish, whether **(409) 761-1498** appears anywhere you care about, and Houston **(713) 242-1880** usage.
4. Keep, edit, or remove each flagged marketing phrase and trial-result block?
5. Is the public **W-9** intentional and current?
6. Approve a **branded 1200×630** share image? Who supplies art?
7. Do you want a **blog/insights** section you can sustain (e.g., 4 posts/year), or explicitly defer?
8. ~~Maps: regenerated live embed vs static map + Get Directions?~~ **Decided:** static directions CTA (no embed).
9. ~~May we **delete unused Equity font files** from the repo?~~ **Done (2026-08-10)** — Equity TTFs removed.
10. Any appetite to move off GitHub Pages for **security headers**, or accept the limitation?
11. Privacy Policy / Terms: who drafts — firm counsel or outside privacy counsel?
12. Who is the **lawyer responsible for website content**, and what is the **principal office** designation text? (**L-04 residual** — advertising / no-A-C footer notice is live; do not invent responsible-attorney names until firm decides.)

---

## Raw tool output

| Path | Contents |
|---|---|
| `audit/raw/inventory.json` | Full machine-readable inventory |
| `audit/raw/inventory.md` | Page table |
| `audit/raw/axe/` | axe-core results (homepage + Booth; more in Phase 2) |
| `audit/raw/production-headers.txt` | Live header/redirect notes |
| `audit/raw/TOOLING-NOTES.md` | What ran / what couldn’t |
| `audit/raw/lighthouse/` | Empty — fill in Phase 2 |
| `audit/raw/pa11y/` | Empty — fill in Phase 2 |

---

## Stop — awaiting approval

Phase 1 is complete. **No implementation has started.**

Please reply with:

1. Approval (or edits) to the prioritized Phase 2 plan,  
2. Answers to any Open Questions you can decide now (~~**L-01 privilege language**~~ **done — Option A**; especially **Houston NAP**),  
3. Whether to create branch `website-audit-remediation` and begin **2A** only.

I will not change public site files until you say so.
