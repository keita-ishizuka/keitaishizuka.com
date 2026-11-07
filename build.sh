#!/bin/bash
# Rebuild keita.homeishizuka.org from ~/kb/publications.json and ~/kb/grants.json.
# The system node is v20, which Astro 6 refuses; use the nvm-installed v24.
set -e
export PATH="$HOME/.nvm/versions/node/v24.14.0/bin:$PATH"
cd "$(dirname "$(readlink -f "$0")")"
node -v
# refresh the public subset of ~/kb that the site is built from
python3 scripts/export_kb.py
npm run build
echo "built. served from dist/ by the researcher-page user service (port 8400)."
