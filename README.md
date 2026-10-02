# Millar-Blanchaer Research Group website

One content tree, many themes. `build.py` renders every theme in `themes/` from the same
`content/` and `_data/` files. Today that is the GeoCities edition (`retro`) at the site root, the
default, and the previous look (`modern`, HTML5 UP "Massively") at `/modern/`. Visitors flip
between them with the MODERN MODE / 1998 mode button in each nav; the choice is remembered in
their browser. The first theme listed under `themes:` in `site.yml` is the one at the root.

```
site.yml            title, contact, nav order, which themes to build, the web ring
content/*.yml       one file per page, written as theme-neutral blocks (see below)
_data/              news.yml, group_members.yml, carousel.yml  (same format as before; the scripts still work)
                    ads_config.yml, publications.json (written by scripts/fetch_ads.py)
static/             shared images/, videos/, assets/ (cv.pdf)
themes/<name>/      theme.yml + templates/ (Jinja2) + static/ (theme-only css/js/images/audio)
scripts/            manage_news.py, update_group_member.py, fetch_ads.py
_site/              build output (git-ignored; GitHub Actions builds and deploys it)
```

## Everyday edits

| I want to...                      | Edit                                   | Then |
|-----------------------------------|----------------------------------------|------|
| post news                         | `_data/news.yml` (or `scripts/manage_news.py`) | `python3 build.py` |
| add / change a group member       | `_data/group_members.yml` (or `scripts/update_group_member.py`) | build |
| change the home-page photos       | `_data/carousel.yml` + drop the image in `static/images/` | build |
| change text on a page             | `content/<page>.yml`                   | build |
| add a page                        | new `content/<slug>.yml` + a line in `site.yml` nav | build |
| change the look of one theme      | `themes/<name>/templates/*` or `static/style.css` | build |
| add a whole new theme             | copy `themes/retro/` to `themes/<new>/`, edit `theme.yml`, add it to `themes:` in `site.yml` | build |

Build needs Python 3 with `pyyaml` and `jinja2`:

```bash
python3 build.py            # writes _site/
python3 build.py --serve    # ...and serves it at http://localhost:8765
```

"Last updated" everywhere is the date the build ran.

## Content blocks

A page file looks like:

```yaml
title: Polarization Gratings
nav: instrumentation            # which nav item lights up
show_title: true                # subpages print their title; section pages don't
back: {href: instrumentation.html, label: Instrumentation}
description: "for the <meta description>"
blocks:
  - {type: text, html: "A paragraph. <a href=...>Links</a> and <em>emphasis</em> are fine."}
  - {type: heading, text: "A sub-heading", tag: hot}         # tag: hot | new (retro shows a badge)
  - {type: figure, src: images/PG_Photo.png, width: 50%, caption: "..."}
  - {type: video,  src: videos/betapic.mp4, poster: images/betapic.png, caption: "..."}
  - {type: list,   items: [{href: ..., name: ..., desc: "optional"}]}
  - {type: links,  items: [{href: gpi.html, title: ..., blurb: ..., image: images/gpi_logo.jpg}]}  # sub-page cards
  - {type: construction, text: "...", themes: [retro]}         # `themes:` limits a block to some themes
```

Images are referenced by their shared name (`images/foo.png`). A theme can ship its own copy
under `themes/<name>/static/<image_dir>/` (any extension; `image_dir` is set in `theme.yml`) and it is
picked up automatically. The retro theme keeps resized versions and its wallpaper in `retro-img/`;
the modern theme keeps the Massively background in `images/`.

## Themes

`themes/<name>/theme.yml`:

```yaml
label: Retro
out: ""                          # output subfolder ("" = site root; the first theme in site.yml should be the root)
image_dir: retro-img             # theme-only images (must not be "images" for the root theme, or it would shadow the shared folder)
switch_labels: {modern: "MODERN MODE"}   # what this theme calls its link to each other theme
extra_outputs: [frames.html, frame_top.html, frame_nav.html]   # extra templates to render as-is
```

Templates get: `site`, `data` (news_items sorted newest first, group_members, carousel,
publications, ads_config), `page` (the content file + `switch_links`), `nav`, `root` (prefix to
reach shared static files), `updated`, and helpers `img()`, `href()`, `is_member()`, `pubs_by_year()`.
Every theme must provide `page.html`, `index.html`, `group.html`, `publications.html`.

## Publications from ADS

`scripts/fetch_ads.py` queries ADS for (PI OR every current group member) since `since_year`,
minus meeting abstracts, and writes `_data/publications.json`. Members with an ORCID in
`group_members.yml` are matched by ORCID; others by `author:"Last, First" AND aff:"Santa Barbara"`.
Add `ads_query:` to a member to override, or a bibcode to `exclude_bibcodes` to drop a paper.
`--print-query` shows the query and an ADS search link. Needs a token in `$ADS_DEV_KEY` or
`~/.ads/dev_key`. The weekly GitHub Action runs it and opens a PR when the list changes.

## Deploying

Push this folder to a GitHub repo (the `UCSB-Exoplanet-Polarimetry-Lab.github.io` repo, replacing
the Jekyll setup). Settings -> Pages -> Source: **GitHub Actions**. Every push to `main` builds
and deploys. See the comments at the top of the two workflow files for the ADS secret and PR
permission settings.

## Retro theme notes

- Music: "Stereotypical 90's space shooter music" by Jan125, OGA-BY 3.0 (`themes/retro/static/audio/CREDITS.txt`).
  If the files can't load, `script.js` falls back to an original FM-style loop generated with the Web Audio API.
- The counter, guestbook and theme preference live only in the visitor's browser (localStorage). Nothing is sent anywhere.
- `frames.html` is the frameset edition. Pages detect when they're inside it and hide their own banner and nav.
- Every animation is CSS; there are no GIFs. CALM DOWN turns them all off (then says PARTY TIME).
