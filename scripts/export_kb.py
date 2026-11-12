#!/usr/bin/env python3
"""Export the public subset of ~/kb into src/data/ so the site can be built
from the repository alone (GitHub Actions has no access to ~/kb).

Allowlists only: any field not named here never reaches the public repo.
"""
import json, os, sys
from pathlib import Path

KB = Path(os.environ.get("KB_DIR", Path.home() / "kb"))
OUT = Path(__file__).resolve().parent.parent / "src" / "data"

PAPER = ["id", "title", "title_ja", "authors", "journal", "venue", "venue_ja", "volume",
         "issue", "pages", "article_number", "year", "month", "status", "type",
         "doi", "arxiv", "dataset", "url", "slides", "slides_label"]
GRANT = ["title", "title_en", "title_ja", "description", "description_ja", "type", "type_en",
         "role", "period", "number", "kaken_id", "record_label", "record_url",
         "selectivity", "selectivity_ja", "status", "show_amount", "amount_jpy"]
CV_ROW = ["when", "when_ja", "title", "title_ja", "org", "org_ja", "note", "note_ja"]
DS_COLL = ["key", "title", "title_ja", "short", "short_ja", "summary", "summary_ja",
           "format", "format_ja", "license", "published", "updated", "updated_note",
           "updated_note_ja", "paper", "table", "records"]
DS_PAPER = ["authors", "title", "arxiv", "doi"]
DS_REC = ["title", "doi", "concept_doi", "version", "bytes"]


def pick(d, keys):
    return {k: d[k] for k in keys if k in d and d[k] is not None}


def load(name):
    return json.loads((KB / f"{name}.json").read_text())


def main():
    pubs = load("publications")
    out_pubs = {"papers": [pick(p, PAPER) for p in pubs["papers"]]}

    grants = load("grants")
    kept = [g for g in grants["grants"] if g.get("show_on_site") is not False]
    out_grants = {"grants": []}
    for g in kept:
        row = pick(g, GRANT)
        # amounts are never rendered unless show_amount is true; do not publish them otherwise
        if not row.get("show_amount"):
            row.pop("amount_jpy", None)
        out_grants["grants"].append(row)

    cv = load("cv")
    out_cv = {k: [pick(r, CV_ROW) for r in cv[k]] for k in ("appointments", "visits", "education")}
    out_cv["service"] = {"referee_for": cv["service"]["referee_for"]}

    ds = load("datasets")
    colls = []
    for c in ds["collections"]:
        row = pick(c, DS_COLL)
        if "paper" in row:
            row["paper"] = pick(row["paper"], DS_PAPER)
        if "records" in row:
            row["records"] = [pick(r, DS_REC) for r in row["records"]]
        colls.append(row)
    out_ds = {"collections": colls}

    OUT.mkdir(parents=True, exist_ok=True)
    for name, data in (("publications", out_pubs), ("grants", out_grants),
                       ("cv", out_cv), ("datasets", out_ds)):
        p = OUT / f"{name}.json"
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        print(f"wrote {p.relative_to(OUT.parent.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
