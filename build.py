#!/usr/bin/env python3
"""Build every theme of the site from one content tree.

    site.yml          site-wide settings and the nav
    content/*.yml     one file per page: theme-neutral blocks (text, figure, links, ...)
    _data/*.yml       news, group members, carousel, ADS config, publications.json
    static/           shared images / videos / assets
    themes/<name>/    theme.yml + templates/ (Jinja2) + static/ (theme-only css, js, images)
    _site/            output: the first theme at the root, the others in subfolders

Usage:  python3 build.py            build everything into _site/
        python3 build.py --serve    build, then serve _site/ on http://localhost:8765
"""
import argparse, datetime, html, json, pathlib, posixpath, re, shutil, sys
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = pathlib.Path(__file__).resolve().parent
CONTENT, DATA, STATIC, THEMES, OUT = ROOT / "content", ROOT / "_data", ROOT / "static", ROOT / "themes", ROOT / "_site"
TODAY = datetime.date.today()


def read_yaml(p):
    with open(p) as f:
        return yaml.safe_load(f) or {}


def load_data():
    d = {k: read_yaml(DATA / f"{k}.yml") for k in ("news", "group_members", "carousel", "ads_config")}
    pj = DATA / "publications.json"
    d["publications"] = json.load(open(pj)) if pj.exists() else None
    # news sorted newest first, with category objects attached
    cats = {c["name"]: c for c in d["news"].get("categories", [])}
    items = []
    for it in d["news"].get("items", []):
        it = dict(it)
        it["date"] = datetime.date.fromisoformat(str(it["date"]))
        it["cat"] = cats.get(it.get("category"), {"display_name": "Update", "color": "#ffc107", "icon": "fa-info-circle", "name": "update"})
        it["description"] = " ".join(str(it.get("description", "")).split())
        items.append(it)
    d["news_items"] = sorted(items, key=lambda i: i["date"], reverse=True)
    return d


def load_pages():
    pages = {}
    for p in sorted(CONTENT.glob("*.yml")):
        page = read_yaml(p)
        page["slug"] = p.stem
        page["filename"] = "index.html" if p.stem == "home" else f"{p.stem}.html"
        page.setdefault("template", "index.html" if p.stem == "home" else "page.html")
        page.setdefault("blocks", [])
        pages[p.stem] = page
    return pages


def member_lastnames(members):
    names = ["Millar-Blanchaer"]
    for m in members.get("current", []):
        names.append(re.sub(r"\([^)]*\)", "", m["name"]).strip().split()[-1])
    return names


def publications_by_year(pubs):
    years = {}
    for p in pubs["items"]:
        years.setdefault(p.get("year") or "n.d.", []).append(p)
    return sorted(years.items(), key=lambda kv: str(kv[0]), reverse=True)


class Theme:
    def __init__(self, name, site, data, pages, all_themes):
        self.name = name
        self.dir = THEMES / name
        self.cfg = read_yaml(self.dir / "theme.yml")
        self.out_sub = self.cfg.get("out", name)          # "" for the root theme
        self.out = OUT / self.out_sub if self.out_sub else OUT
        self.root = "" if not self.out_sub else "../" * len(pathlib.PurePosixPath(self.out_sub).parts)
        self.site, self.data, self.pages, self.all_themes = site, data, pages, all_themes
        self.env = Environment(loader=FileSystemLoader(str(self.dir / "templates")), autoescape=False,
                               trim_blocks=True, lstrip_blocks=True)
        self.env.filters["e"] = html.escape
        self.env.filters["date"] = lambda d, fmt="%b %-d, %Y": d.strftime(fmt)
        self.env.filters["dateiso"] = lambda d: d.isoformat()
        self.env.tests["member"] = self.is_member            # usable as: authors | select("member")
        self.env.globals.update(site=site, data=data, theme=self.cfg, theme_name=name, root=self.root,
                                updated=TODAY.strftime("%b %-d, %Y"), year=TODAY.year, today=TODAY,
                                img=self.img, href=self.href, nav=self.nav(), switch=self.switch,
                                member_lastnames=member_lastnames(data["group_members"]),
                                pubs_by_year=publications_by_year, is_member=self.is_member)

    # --- helpers available inside templates ---
    def img(self, src):
        """Theme-local override (e.g. a resized copy) if the theme ships one, else the shared image."""
        src = src.lstrip("/")
        p = pathlib.PurePosixPath(src)
        if len(p.parts) == 2 and p.parts[0] == "images":        # top-level shared image: a theme may ship its own copy
            image_dir = self.cfg.get("image_dir", "images")
            local_dir = self.dir / "static" / image_dir
            if local_dir.exists():
                for cand in local_dir.iterdir():
                    if cand.stem == p.stem and cand.suffix.lower() in (".jpg", ".jpeg", ".png", ".svg", ".gif", ".webp"):
                        return f"{image_dir}/{cand.name}"
        return self.root + src

    def href(self, h, shared=False):
        if re.match(r"^(https?:|mailto:|#)", h):
            return h
        return (self.root + h) if (shared or h.startswith(("assets/", "videos/"))) else h

    def nav(self):
        return [dict(n, url=self.href(n["href"], n.get("shared", False))) for n in self.site["nav"]]

    def switch(self, page_filename):
        """Links to this same page in every other theme, for the theme-switch button."""
        out = []
        for t in self.all_themes:
            if t.name == self.name:
                continue
            rel = posixpath.relpath(t.out_sub or ".", self.out_sub or ".")
            # ?theme=<name> carries the choice in the URL, so the link works even when a theme's mobile menu
            # clones the nav and drops data attributes; the landing page stores it and strips the parameter.
            url = posixpath.normpath(posixpath.join(rel, page_filename)) + f"?theme={t.name}"
            label = self.cfg.get("switch_labels", {}).get(t.name, t.cfg.get("label", t.name))
            out.append({"name": t.name, "label": label, "url": url})
        return out

    def is_member(self, author):
        last = author.split(",")[0].strip().lower()
        return any(last == h.lower() for h in self.env.globals["member_lastnames"])

    # --- build ---
    def build(self):
        self.out.mkdir(parents=True, exist_ok=True)
        static = self.dir / "static"
        if static.exists():
            shutil.copytree(static, self.out, dirs_exist_ok=True)
        for page in self.pages.values():
            tpl = self.env.get_template(page["template"])
            page_ctx = dict(page, switch_links=self.switch(page["filename"]))
            (self.out / page["filename"]).write_text(tpl.render(page=page_ctx))
        # pages that come straight from data, not from content/
        for filename, template, extra in (("group.html", "group.html", {}), ("publications.html", "publications.html", {})):
            page = {"title": template.split(".")[0].title(), "nav": template.split(".")[0], "filename": filename,
                    "slug": filename[:-5], "description": "", "switch_links": self.switch(filename)}
            (self.out / filename).write_text(self.env.get_template(template).render(page=page, **extra))
        for extra in self.cfg.get("extra_outputs", []):      # e.g. the retro frameset files
            page = {"title": extra, "nav": "", "filename": extra, "slug": extra[:-5], "switch_links": self.switch("index.html")}
            (self.out / extra).write_text(self.env.get_template(extra).render(page=page))
        print(f"  theme {self.name:7s} -> {self.out.relative_to(ROOT)}/")


def build():
    site = read_yaml(ROOT / "site.yml")
    data, pages = load_data(), load_pages()
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(STATIC, OUT, dirs_exist_ok=True)       # shared images/, videos/, assets/
    (OUT / ".nojekyll").write_text("")
    themes = [Theme(n, site, data, pages, None) for n in site["themes"]]
    for t in themes:
        t.all_themes = themes
    for t in themes:
        t.build()
    print(f"built {len(pages) + 2} pages x {len(themes)} themes into {OUT.relative_to(ROOT)}/  (updated {TODAY})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--serve", action="store_true")
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    build()
    if a.serve:
        import functools, http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        print(f"serving {OUT} at http://localhost:{a.port}")
        http.server.ThreadingHTTPServer(("", a.port), handler).serve_forever()
