#!/usr/bin/env sh
set -eu
if command -v node >/dev/null 2>&1; then
  node --check docs/assets/app.js
  node --check docs/assets/site-config.js
  node --check docs/assets/public-data.js
else
  echo "Node is not installed; JavaScript syntax check skipped."
fi
