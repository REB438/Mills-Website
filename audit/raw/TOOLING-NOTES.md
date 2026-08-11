# Tooling notes (Phase 1)

## What ran successfully
- Custom Python inventory (`audit/raw/inventory.json`, `inventory.md`) across all 34 HTML pages.
- axe-core 4.10.3 injected in Cursor browser on homepage (saved `axe/index.json`).
- `@axe-core/cli` with system Chrome once succeeded on homepage earlier in session (0 violations in that run; browser-injected axe found target-size — difference likely viewport/CSS).
- Production HTTP header / redirect checks via curl against https://millsshirley.com (GitHub Pages + Fastly).
- Manual CDP contrast sampling and map iframe inspection.

## What could not be completed in this environment
- Full `@axe-core/cli` / Pa11y / Lighthouse sweeps across every page: sandbox blocked Chrome system-interface calls on subsequent runs (`uv_interface_addresses` / permission harness rejections).
- Google Rich Results Test (external Google UI) — not automated here; schema inventory is from static parse.
- Live GBP / Martindale / Avvo citation scrape — flagged as open firm questions, not verified live.
- Map tile visual confirmation inside cross-origin iframe (browser tools cannot inspect iframe contents). Embed URL returns from Google but `pb=` looks hand-authored (`!4v1`, synthetic place id hex); recommend regenerating.

## Recommendation for Phase 2 verification
Re-run Lighthouse mobile+desktop and axe CLI on all 27 real pages from an unrestricted local machine before closing findings.
