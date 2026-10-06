#!/usr/bin/env python3
"""Fetch the group's publications from NASA ADS and write _data/publications.json.

Query = (PI OR current member 1 OR current member 2 ...) AND collection:astronomy AND year >= since_year

Needs an ADS API token in the ADS_DEV_KEY environment variable or in ~/.ads/dev_key
(get one at https://ui.adsabs.harvard.edu/user/settings/token).

Run with --print-query to see the query (and a clickable ADS search URL) without fetching.
"""
import json, os, pathlib, re, sys, urllib.parse, urllib.request
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "_data"
OUT = DATA / "publications.json"
API = "https://api.adsabs.harvard.edu/v1/search/query"
FIELDS = "bibcode,title,author,year,pubdate,pub,doctype,property,doi,identifier,citation_count"


def clean_name(name):
    """'Jaren N. Ashcraft (He/They)' -> ('Ashcraft', 'Jaren')"""
    name = re.sub(r"\([^)]*\)", "", name).strip()
    parts = name.split()
    return parts[-1], parts[0]


def orcid_id(value):
    m = re.search(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]", value or "")
    return m.group(0) if m else None


def member_term(m):
    if m.get("ads_query"):
        return m["ads_query"]
    last, first = clean_name(m["name"])
    by_name = f'(author:"{last}, {first}" AND aff:"Santa Barbara")'
    oid = orcid_id(m.get("orcid"))
    return f'({by_name} OR orcid:"{oid}")' if oid else by_name


def build_query(cfg, members):
    pi = cfg["pi"]
    terms = [f'(author:"{pi["name"].split(",")[0]}, {pi["name"].split(",")[1].strip()[0]}" OR orcid:"{pi["orcid"]}")']
    terms += [member_term(m) for m in members["current"]]
    people = " OR ".join(terms)
    q = f"({people}) AND collection:astronomy AND year:[{cfg['since_year']} TO 9999]"
    for dt in cfg.get("exclude_doctypes") or []:     # e.g. "abstract" drops AAS/DPS meeting abstracts
        q += f" AND NOT doctype:{dt}"
    return q


def keep_publication(pub, cfg):
    """Apply the `keep:` rules from ads_config.yml (shared with build.py)."""
    keep = cfg.get("keep") or {}
    if pub["kind"] == "refereed":
        return keep.get("refereed", True)
    if pub["kind"] == "preprint":
        return keep.get("preprints", True)
    series = keep.get("proceedings_from") or []
    return any(pub["bibcode"][4:4 + len(sx)] == sx for sx in series)


def token():
    t = os.environ.get("ADS_DEV_KEY")
    if not t:
        p = pathlib.Path.home() / ".ads" / "dev_key"
        if p.exists():
            t = p.read_text().strip()
    return t


def fetch(query, rows, tok):
    params = {"q": query, "fl": FIELDS, "rows": rows, "sort": "pubdate desc, bibcode desc"}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["response"]["docs"]


def kind_of(doc):
    props = set(doc.get("property") or [])
    dt = doc.get("doctype")
    if "REFEREED" in props:
        return "refereed"
    if dt == "eprint":
        return "preprint"
    if dt in ("inproceedings", "proceedings"):
        return "proceedings"
    return "other"


def arxiv_of(doc):
    for ident in doc.get("identifier") or []:
        if ident.lower().startswith("arxiv:"):
            return ident.split(":", 1)[1]
    return None


def main():
    cfg = yaml.safe_load(open(DATA / "ads_config.yml"))
    members = yaml.safe_load(open(DATA / "group_members.yml"))
    query = build_query(cfg, members)
    url = "https://ui.adsabs.harvard.edu/search/" + urllib.parse.urlencode({"q": query, "sort": "date desc, bibcode desc"})
    if "--print-query" in sys.argv:
        print(query)
        print()
        print(url)
        return
    tok = token()
    if not tok:
        sys.exit("No ADS token: set ADS_DEV_KEY or create ~/.ads/dev_key")
    docs = fetch(query, cfg.get("max_rows", 500), tok)
    skip = set(cfg.get("exclude_bibcodes") or [])
    pubs = []
    for d in docs:
        if d["bibcode"] in skip:
            continue
        pub = {
            "bibcode": d["bibcode"],
            "title": (d.get("title") or ["Untitled"])[0],
            "authors": d.get("author") or [],
            "year": d.get("year"),
            "pubdate": d.get("pubdate"),
            "journal": d.get("pub"),
            "kind": kind_of(d),
            "doi": (d.get("doi") or [None])[0],
            "arxiv": arxiv_of(d),
            "citations": d.get("citation_count", 0),
        }
        if keep_publication(pub, cfg):
            pubs.append(pub)
    OUT.write_text(json.dumps({"query": query, "search_url": url, "count": len(pubs), "items": pubs}, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {OUT} with {len(pubs)} publications")


if __name__ == "__main__":
    main()
