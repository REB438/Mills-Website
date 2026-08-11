#!/usr/bin/env python3
"""Phase-1 inventory. Writes inventory.json + inventory.md under audit/raw/."""
import os, re, json, hashlib
from html.parser import HTMLParser
from collections import defaultdict
from urllib.parse import urlparse, unquote

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
OUT = os.path.dirname(__file__)

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta = {}
        self.canonical = None
        self.h1s = []
        self.headings = []  # (level, text)
        self.links = []  # href
        self.imgs = []  # (src, alt)
        self.scripts = []
        self.externals = []
        self.iframes = []
        self.lang = None
        self.has_main = False
        self.has_nav = False
        self.has_header = False
        self.has_footer = False
        self.has_skip = False
        self.schema_types = []
        self.word_chunks = []
        self._capture = None
        self._buf = ""
        self.in_script = False
        self.in_style = False
        self.script_type = None
        self.script_buf = ""

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "html":
            self.lang = d.get("lang")
        if tag == "title":
            self._capture = "title"; self._buf = ""
        if tag == "meta":
            name = (d.get("name") or d.get("property") or "").lower()
            if name and "content" in d:
                self.meta[name] = d["content"]
        if tag == "link" and d.get("rel") == "canonical":
            self.canonical = d.get("href")
        if tag in ("h1","h2","h3","h4","h5","h6"):
            self._capture = tag; self._buf = ""
        if tag == "a" and "href" in d:
            self.links.append(d["href"])
            if d["href"].startswith("#") and "skip" in (d.get("class") or "").lower() or "skip" in (d.get("href") or "").lower():
                self.has_skip = True
            txt_hint = (d.get("aria-label") or "")
            if "skip" in txt_hint.lower():
                self.has_skip = True
        if tag == "img":
            self.imgs.append((d.get("src",""), d.get("alt")))
        if tag == "script":
            self.in_script = True
            self.script_type = d.get("type","")
            self.script_buf = ""
            if d.get("src"):
                self.scripts.append(d["src"])
        if tag == "style":
            self.in_style = True
        if tag == "iframe":
            self.iframes.append({"src": d.get("src",""), "title": d.get("title"), "attrs": d})
        if tag == "main": self.has_main = True
        if tag == "nav": self.has_nav = True
        if tag == "header": self.has_header = True
        if tag == "footer": self.has_footer = True
        # skip link detection via class/id
        cls = " ".join([d.get("class",""), d.get("id","")]).lower()
        if "skip" in cls:
            self.has_skip = True

    def handle_endtag(self, tag):
        if tag == "title" and self._capture == "title":
            self.title = " ".join(self._buf.split()); self._capture = None
        if tag in ("h1","h2","h3","h4","h5","h6") and self._capture == tag:
            t = " ".join(self._buf.split())
            lv = int(tag[1])
            self.headings.append((lv, t))
            if lv == 1: self.h1s.append(t)
            self._capture = None
        if tag == "script":
            self.in_script = False
            if self.script_type == "application/ld+json" and self.script_buf.strip():
                try:
                    data = json.loads(self.script_buf)
                    types = []
                    def walk(o):
                        if isinstance(o, dict):
                            if "@type" in o:
                                t = o["@type"]
                                types.append(t if isinstance(t,str) else ",".join(t))
                            for v in o.values(): walk(v)
                        elif isinstance(o, list):
                            for i in o: walk(i)
                    walk(data)
                    self.schema_types.extend(types)
                except Exception:
                    self.schema_types.append("INVALID_JSON_LD")
            self.script_buf = ""
        if tag == "style":
            self.in_style = False

    def handle_data(self, data):
        if self.in_script:
            self.script_buf += data
            return
        if self.in_style:
            return
        if self._capture:
            self._buf += data
        else:
            self.word_chunks.append(data)

def resolve(page, href):
    if not href or href.startswith(("#","mailto:","tel:","javascript:","data:")):
        return None
    u = urlparse(href)
    if u.scheme or u.netloc:
        return ("ext", href)
    path = unquote(u.path)
    parts = [p for p in os.path.dirname(page).split("/") if p]
    for seg in path.split("/"):
        if seg in ("", "."): continue
        if seg == "..":
            if parts: parts.pop()
        else:
            parts.append(seg)
    target = "/".join(parts)
    if href.endswith("/") or target == "" or target.endswith("/"):
        cand = (target.rstrip("/") + "/index.html").lstrip("/")
        if os.path.exists(os.path.join(ROOT, cand)):
            return ("int", cand)
    if os.path.exists(os.path.join(ROOT, target)):
        return ("int", target)
    return ("broken", target)

pages = sorted(
    os.path.relpath(os.path.join(dp,f), ROOT)
    for dp,dn,fn in os.walk(ROOT)
    for f in fn if f.endswith(".html")
    if ".git" not in dp and "/audit/" not in ("/"+dp+"/")
)

inventory = []
inbound = defaultdict(set)
outbound_ext = defaultdict(set)
broken = []
phones = defaultdict(list)
fragment_nav = []

phone_re = re.compile(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
superlatives = re.compile(
    r"aggressive representation|Proven history|Strategic wins|Expert |trial-tested|Leading Galveston|best |#1 |guarantee",
    re.I
)

for rel in pages:
    raw = open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace").read()
    p = PageParser(); p.feed(raw)
    words = re.findall(r"[A-Za-z0-9']+", " ".join(p.word_chunks))
    # skip links detection improved
    if re.search(r'skip[- ]?(to|link)|class="[^"]*skip', raw, re.I):
        p.has_skip = True
    for href in p.links:
        kind = resolve(rel, href)
        if kind is None:
            if href.startswith("#"):
                # fragment from this page
                pass
            continue
        typ, target = kind
        if typ == "int":
            inbound[target].add(rel)
        elif typ == "ext":
            outbound_ext[rel].add(target)
        elif typ == "broken":
            broken.append({"from": rel, "href": href, "resolved": target})
    # fragment nav that points to homepage-only ids from interior
    for m in re.finditer(r'href="(#[a-zA-Z0-9_-]+)"', raw):
        frag = m.group(1)
        if frag in ("#about","#attorneys","#contact","#practice-areas") and rel != "index.html":
            fragment_nav.append({"page": rel, "href": frag})
    # also relative links like index.html#contact from interior - those are OK
    for m in re.finditer(r'href="([^"]*#[a-zA-Z0-9_-]+)"', raw):
        h = m.group(1)
        if h.startswith("#") and rel not in ("index.html",) and any(x in h for x in ("about","attorneys","contact","practice")):
            # already captured
            pass
    for ph in phone_re.findall(raw):
        phones[re.sub(r"\D","",ph)].append(rel)
    supers = sorted(set(superlatives.findall(raw)))
    inventory.append({
        "path": rel,
        "title": p.title,
        "title_len": len(p.title),
        "description": p.meta.get("description",""),
        "desc_len": len(p.meta.get("description","")),
        "canonical": p.canonical,
        "h1": p.h1s,
        "h1_count": len(p.h1s),
        "headings": p.headings[:40],
        "word_count": len(words),
        "lang": p.lang,
        "landmarks": {"main": p.has_main, "nav": p.has_nav, "header": p.has_header, "footer": p.has_footer, "skip": p.has_skip},
        "schema": p.schema_types,
        "imgs": [{"src": s, "alt": a} for s,a in p.imgs],
        "iframes": p.iframes,
        "meta_keywords": p.meta.get("keywords"),
        "og_image": p.meta.get("og:image"),
        "scripts": p.scripts,
        "external_link_count": len(outbound_ext[rel]),
        "superlatives_flagged": supers,
        "is_redirect_stub": bool(re.search(r'http-equiv=["\']refresh|location\.(replace|href)', raw[:5000], re.I)),
    })

# assets
assets = []
for dp,dn,fn in os.walk(os.path.join(ROOT,"assets")):
    for f in fn:
        path = os.path.join(dp,f)
        rel = os.path.relpath(path, ROOT)
        st = os.stat(path)
        assets.append({"path": rel, "bytes": st.st_size, "ext": os.path.splitext(f)[1].lower()})

# orphans: real pages with no inbound (excluding index, 404, redirect stubs)
real = [i for i in inventory if not i["is_redirect_stub"] and i["path"] != "404.html"]
orphans = [i["path"] for i in real if i["path"] != "index.html" and not inbound.get(i["path"])]

# also check directory index forms
for i in real:
    p = i["path"]
    # inbound via /attorneys/ for attorneys/index.html etc
    alts = set()
    if p.endswith("/index.html"):
        alts.add(p[:-10])  # trailing slash form without index
        alts.add(p[:-11] if p.endswith("/index.html") else p)
    # recount with flexible matching
    hits = set(inbound.get(p, set()))
    if p.endswith("index.html"):
        folder = p[: -len("index.html")]
        for k,v in inbound.items():
            if k.rstrip("/") == folder.rstrip("/") or k == p:
                hits |= v
    if p != "index.html" and not hits and p not in orphans:
        orphans.append(p)

out = {
    "page_count": len(pages),
    "pages": inventory,
    "inbound_counts": {k: len(v) for k,v in sorted(inbound.items())},
    "broken_links": broken,
    "phones": {k: sorted(set(v)) for k,v in phones.items()},
    "fragment_nav_suspects": fragment_nav,
    "orphans_approx": sorted(set(orphans)),
    "assets_summary": {
        "count": len(assets),
        "by_ext": {},
        "largest": sorted(assets, key=lambda a: -a["bytes"])[:25],
        "jpg_total_mb": round(sum(a["bytes"] for a in assets if a["ext"]==".jpg")/1e6, 2),
        "webp_total_mb": round(sum(a["bytes"] for a in assets if a["ext"]==".webp")/1e6, 2),
        "ttf_total_mb": round(sum(a["bytes"] for a in assets if a["ext"]==".ttf")/1e6, 2),
    },
    "external_destinations": sorted({u for s in outbound_ext.values() for u in s}),
}
# by_ext
from collections import Counter
c = Counter(a["ext"] for a in assets)
out["assets_summary"]["by_ext"] = dict(c.most_common())

with open(os.path.join(OUT, "inventory.json"), "w") as f:
    json.dump(out, f, indent=2)

# markdown table
lines = ["# Page Inventory\n", "| Path | Title len | Desc len | H1 | Words | Canonical | Schema | Stub |\n|---|---|---|---|---|---|---|---|\n"]
for i in inventory:
    lines.append(f"| `{i['path']}` | {i['title_len']} | {i['desc_len']} | {i['h1_count']}: {(i['h1'][0][:40] if i['h1'] else '—')} | {i['word_count']} | {(i['canonical'] or '—')[:50]} | {','.join(i['schema'][:4]) or '—'} | {i['is_redirect_stub']} |\n")
with open(os.path.join(OUT, "inventory.md"), "w") as f:
    f.writelines(lines)

print(f"Wrote inventory for {len(pages)} pages")
print(f"Broken links: {len(broken)}")
print(f"Fragment nav suspects: {len(fragment_nav)}")
print(f"Phones found: {list(phones.keys())}")
print(f"JPG MB: {out['assets_summary']['jpg_total_mb']}  WebP MB: {out['assets_summary']['webp_total_mb']}  TTF MB: {out['assets_summary']['ttf_total_mb']}")
print(f"External destinations: {len(out['external_destinations'])}")
