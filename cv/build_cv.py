#!/usr/bin/env python3
"""Build the CV PDF from ~/kb/*.json.

  python3 cv/build_cv.py          -> cv/cv.html, public/cv.pdf

Rendering is done by headless Chromium so the PDF uses the same wording and
data as the site. Amounts of grants are deliberately not printed.
"""
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB = Path.home() / "kb"
CHROME = Path.home() / ".cache/ms-playwright/chromium-1234/chrome-linux64/chrome"

NAME = "Keita Ishizuka"
NAME_JA = "石塚 慶太"
EMAIL = "keitaishizuka1994@gmail.com"
SITE = "keitaishizuka.com"
ORCID = "0000-0001-5943-6245"
SCHOLAR = "scholar.google.com/citations?user=JCmQRmUAAAAJ"

OUT = ["published", "accepted", "camera_ready_submitted", "in_press", "presented"]
UNDER_REVIEW = ["preprint", "under_review", "submitted", "under review (revision 1)"]
ARXIV_RE = re.compile(r"^\d{4}\.\d{4,5}$")
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def e(s):
    return html.escape(str(s))


def load(name):
    with open(KB / name) as fh:
        return json.load(fh)


def by_year_desc(p):
    return (-(p.get("year") or 0), -(p.get("month") or 0))


def authors(p):
    a = p.get("authors") or []
    if isinstance(a, str):
        a = [a]
    return ", ".join(
        f"<strong>{e(x)}</strong>" if x == NAME else e(x) for x in a
    )


def venue_line(p, kind):
    bits = []
    v = p.get("journal") or p.get("venue")
    if kind != "preprint" and v:
        bits.append(f"<em>{e(v)}</em>")
    vol = p.get("volume")
    if vol:
        issue = p.get("issue")
        bits.append(f"{e(vol)}({e(issue)})" if issue else e(vol))
    pages = p.get("pages")
    if pages:
        pr = str(pages).replace("-", "\u2013")
        bits.append(f"pp. {e(pr)}" if "\u2013" in pr else f"Art. {e(pr)}")
    year = p.get("year")
    line_year = f" ({e(year)})" if year else ""
    tail = []
    if p.get("doi"):
        tail.append(f"doi:{e(p['doi'])}")
    if p.get("arxiv") and ARXIV_RE.match(str(p["arxiv"])):
        tail.append(f"arXiv:{e(p['arxiv'])}")
    if kind == "preprint":
        status = p.get("status")
        label = None if status == "preprint" else ("under review" if "review" in str(status) else "submitted")
        if label:
            tail.insert(0, label)
    line = ", ".join(bits) + line_year
    if tail:
        line += (" " if line.strip() else "") + f'<span class="meta">{" · ".join(tail)}</span>'
    return line.strip()


def entries(items, prefix, kind="pub"):
    rows = []
    n = len(items)
    for i, p in enumerate(items):
        tag = f"[{prefix}{n - i}]" if prefix else ""
        rows.append(
            f'<li><span class="tag">{e(tag)}</span><span class="body">'
            f'<span class="ptitle">{e(p.get("title", ""))}</span><br>'
            f'{authors(p)}<br>{venue_line(p, kind)}</span></li>'
        )
    return "\n".join(rows)


def fmt_period(period):
    def ym(t):
        m = re.match(r"^(\d{4})-(\d{2})$", t.strip())
        return f"{MONTHS[int(m.group(2)) - 1]} {m.group(1)}" if m else t.strip()
    parts = re.split(r"\s+to\s+", period)
    return f"{ym(parts[0])} – {ym(parts[1])}" if len(parts) == 2 else ym(period)


def main():
    pubs = load("publications.json")["papers"]
    grants = [g for g in load("grants.json")["grants"] if g.get("show_on_site") is not False]
    datasets = load("datasets.json")["collections"]
    cv = load("cv.json")

    def of_type(t):
        return sorted([p for p in pubs if p.get("type") == t and p.get("status") in OUT],
                      key=by_year_desc)

    journals = of_type("journal")
    proceedings = of_type("proceedings")
    posters = of_type("poster")
    talks = of_type("talk")
    seminars = of_type("seminar")
    other = of_type("translation")
    preprints = sorted(
        [p for p in pubs
         if p.get("status") in UNDER_REVIEW and ARXIV_RE.match(str(p.get("arxiv") or ""))],
        key=by_year_desc)

    sections = []

    def add(title, body):
        if body.strip():
            sections.append(f'<section><h2>{e(title)}</h2>{body}</section>')

    add("Research Interests",
        '<p class="plain">Algebraic coding theory · classification and construction of LCD, '
        'self-dual and self-orthogonal codes · post-quantum cryptography · combinatorial design '
        'theory and Hadamard matrices · insertion–deletion codes for DNA data storage.</p>')

    def timeline(rows):
        out = []
        for r in rows:
            note = f'<br><span class="meta">{e(r["note"])}</span>' if r.get("note") else ""
            out.append(
                f'<li><span class="when">{e(r["when_cv"])}</span><span class="body">'
                f'<strong>{e(r["title"])}</strong>, {e(r["org"])}{note}</span></li>')
        return f'<ul class="timeline">{"".join(out)}</ul>'

    add("Appointments", timeline(cv["appointments"]))
    add("Research Visits", timeline(cv["visits"]))
    add("Education", timeline(cv["education"]))

    if journals:
        add("Journal Articles", f'<ul class="pubs">{entries(journals, "J")}</ul>')
    if proceedings:
        add("Refereed Conference Proceedings", f'<ul class="pubs">{entries(proceedings, "C")}</ul>')
    if posters:
        add("Posters", f'<ul class="pubs">{entries(posters, "P")}</ul>')
    if preprints:
        add("Preprints",
            f'<ul class="pubs">{entries(preprints, "", kind="preprint")}</ul>')

    grant_rows = []
    for g in grants:
        role = {"PI": "Principal Investigator", "fellow": "Fellow"}.get(g.get("role"), g.get("role") or "")
        num = f' <span class="meta">({e(g["number"])})</span>' if g.get("number") else ""
        grant_rows.append(
            f'<li><span class="when">{e(fmt_period(g.get("period", "")))}</span>'
            f'<span class="body"><strong>{e(g.get("title_en") or g.get("title"))}</strong><br>'
            f'{e(g.get("type_en") or g.get("type"))}{num}'
            f'<span class="meta"> — {e(role)}</span></span></li>')
    add("Research Funding", f'<ul class="timeline">{"".join(grant_rows)}</ul>')

    ds_rows = []
    for c in datasets:
        ds_rows.append(
            f'<li><span class="tag"></span><span class="body">'
            f'<span class="ptitle">{e(c["title"])}</span><br>'
            f'{len(c["records"])} record{"s" if len(c["records"]) != 1 else ""}, Zenodo, {e(c["license"])} '
            f'<span class="meta">doi:{e(c["records"][0]["doi"])}</span></span></li>')
    add("Published Datasets", f'<ul class="pubs">{"".join(ds_rows)}</ul>')

    if talks:
        add("Contributed Talks", f'<ul class="pubs">{entries(talks, "T")}</ul>')
    if seminars:
        add("Seminars", f'<ul class="pubs">{entries(seminars, "S")}</ul>')
    if other:
        add("Other Publications", f'<ul class="pubs">{entries(other, "")}</ul>')

    journals = cv.get("service", {}).get("referee_for", [])
    if journals:
        listed = ", ".join(journals[:-1]) + " and " + journals[-1] if len(journals) > 1 else journals[0]
        add("Service", f'<p class="plain">Referee for {listed}.</p>')
    add("Languages", '<p class="plain">Japanese (native) · English (professional working proficiency).</p>')

    doc = TEMPLATE.format(
        name=e(NAME), name_ja=e(NAME_JA), email=e(EMAIL), site=e(SITE),
        orcid=e(ORCID), scholar=e(SCHOLAR), sections="\n".join(sections))

    out_html = ROOT / "cv" / "cv.html"
    out_html.write_text(doc, encoding="utf-8")

    out_pdf = ROOT / "public" / "cv.pdf"
    cmd = [str(CHROME), "--headless", "--disable-gpu", "--no-sandbox",
           "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}", out_html.as_uri()]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not out_pdf.exists():
        sys.stderr.write(r.stderr)
        sys.exit("chromium failed to produce the PDF")
    print(f"{out_html}\n{out_pdf}  ({out_pdf.stat().st_size // 1024} kB)")


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{name} — CV</title>
<style>
  @page {{ size: A4; margin: 16mm 18mm 18mm 18mm; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: "Liberation Sans", Arial, "Noto Sans CJK JP", sans-serif;
         font-size: 9.6pt; line-height: 1.42; color: #16181d; }}
  a {{ color: #0f4c75; text-decoration: none; }}
  header {{ border-bottom: 1.6pt solid #16181d; padding-bottom: 6pt; margin-bottom: 12pt; }}
  h1 {{ font-size: 20pt; margin: 0; letter-spacing: -0.3pt; }}
  h1 .ja {{ font-size: 12pt; font-weight: 500; color: #4a5056; margin-left: 8pt; }}
  .role {{ margin: 3pt 0 0; color: #3b4147; }}
  .contact {{ margin-top: 5pt; font-size: 8.8pt; color: #4a5056; }}
  .contact span + span::before {{ content: " · "; color: #9aa1a8; }}
  h2 {{ font-size: 9.6pt; text-transform: uppercase; letter-spacing: 0.7pt;
       color: #0f4c75; margin: 13pt 0 5pt; padding-bottom: 2pt;
       border-bottom: 0.5pt solid #ccd3d9; }}
  section {{ break-inside: auto; }}
  h2 {{ break-after: avoid; }}
  p.plain {{ margin: 0; }}
  ul {{ list-style: none; margin: 0; padding: 0; }}
  ul.pubs > li, ul.timeline > li {{ display: flex; gap: 7pt; margin-bottom: 6pt;
                                   break-inside: avoid; }}
  ul.pubs > li:last-child, ul.timeline > li:last-child {{ margin-bottom: 0; }}
  .tag {{ flex: 0 0 22pt; font-variant-numeric: tabular-nums; color: #6b7177;
         font-size: 8.6pt; padding-top: 0.6pt; }}
  .when {{ flex: 0 0 88pt; color: #6b7177; font-size: 8.8pt; padding-top: 0.6pt; }}
  .body {{ flex: 1 1 auto; }}
  .ptitle {{ font-weight: 600; }}
  .meta {{ color: #6b7177; font-size: 8.6pt; }}
  em {{ color: #0f4c75; font-style: italic; }}
</style></head>
<body>
  <header>
    <h1>{name}<span class="ja">{name_ja}</span></h1>
    <p class="role">Research Associate, Mitsubishi Electric Corporation —
       Information Technology R&amp;D Center. Ph.D. in Information Science,
       Tohoku University (2024). Nationality: Japanese.</p>
    <p class="contact">
      <span><a href="mailto:{email}">{email}</a></span>
      <span><a href="https://{site}/en/">{site}</a></span>
      <span><a href="https://orcid.org/{orcid}">ORCID {orcid}</a></span>
      <span><a href="https://{scholar}">Google Scholar</a></span>
    </p>
  </header>
  {sections}
</body></html>
"""

if __name__ == "__main__":
    main()
