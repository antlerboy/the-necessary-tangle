#!/usr/bin/env python3
"""Check that the current reading experience survives the historical rebuild."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = []
        self.links = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if 'id' in values:
            self.ids.append(values['id'])
        if tag == 'a':
            self.links.append(values.get('href'))


home = DOCS / 'index.html'
reading = DOCS / 'reading/connections/index.html'
work = ROOT / 'documentation/NEXT_WORK.md'
files = [home, reading, work]
before = [p.read_bytes() for p in files]
subprocess.run([sys.executable, str(ROOT / 'scripts/build_reader_opening.py')], check=True)
assert before == [p.read_bytes() for p in files], 'Reader openings must rebuild without drift'

opening = Page(home)
guide = Page(reading)
assert '/reading/connections/#museum-store' in opening.links
for anchor in ('museum-store', 'regulation', 'learning', 'transduction', 'sources'):
    assert guide.ids.count(anchor) == 1 and '#' + anchor in guide.links
for key in ('heroSearch', 'surpriseMeHero', 'homeMetrics', 'quickLinks', 'alarm-title'):
    assert opening.ids.count(key) == 1
example = (ROOT / 'sources/reader-opening/museum.html').read_text().strip()
assert example in reading.read_text() and '<caption>' in example
article = Page(ROOT / 'sources/reader-opening/museum.html')
assert len([u for u in article.links if u.startswith('https://')]) == 3
for href in article.links:
    if href.startswith('/'):
        assert (DOCS / href.lstrip('/') / 'index.html').is_file(), href
for path in (home, reading):
    assert 'aria-label="Open updates"' in path.read_text()
entry = (DOCS / 'entries/law_or_principle_conant_ashby_theorem/index.html').read_text()
assert 'href="#review"' in entry and entry.index('<h2>Review status</h2>') > entry.index('<h2>Summary</h2>')
assert 'research pass needs editor' not in (DOCS / 'entries/index.html').read_text()
print('Museum reading checked: homepage, three primary sources, four local readings, review labels, and repeat build.')
