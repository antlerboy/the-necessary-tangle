"""Add the first-party page-visit beacon to every generated Tangle page."""
from pathlib import Path
import sys

root = Path(sys.argv[1])
tag = '<script defer src="https://transduction.systems/events/analytics.js"></script>'
for page in root.rglob("*.html"):
    text = page.read_text(encoding="utf-8")
    if "analytics.js" in text:
        continue
    if "</head>" in text:
        text = text.replace("</head>", tag + "</head>", 1)
    elif "</body>" in text:
        text = text.replace("</body>", tag + "</body>", 1)
    else:
        continue
    page.write_text(text, encoding="utf-8")
