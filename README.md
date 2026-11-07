# keitaishizuka.com

The personal research page of Keita Ishizuka, built with Astro and deployed to
GitHub Pages on every push to `main`.

## Layout

```
src/pages/{en,ja}/     the three pages of each locale (home, research, data)
src/components/        shared pieces, including the figures on the research page
src/data/              the published subset of the private knowledge base
src/i18n.ts            every string that appears in both languages
cv/build_cv.py         renders public/cv.pdf from the same data
scripts/export_kb.py   regenerates src/data/*.json from ~/kb (author only)
```

## Build

```sh
npm ci
npm run build      # -> dist/
```

`build.sh` does the same on the author's machine and refreshes `src/data/`
from `~/kb` first; that step needs files that are not part of this repository.
