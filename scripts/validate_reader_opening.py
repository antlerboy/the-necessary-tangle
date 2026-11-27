#!/usr/bin/env python3
"""Check that the current reading experience survives the historical rebuild."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
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
edition = json.loads((DOCS / 'reader-edition.json').read_text())
release = DOCS / edition['release_url'].strip('/') / 'index.html'
history = DOCS / 'versions/index.html'
graph = ROOT / 'data/public-data.json'
adventure = DOCS / '42/manifest.json'
files = [home, reading, work, release, history, DOCS / 'updates/index.html',
         DOCS / 'sitemap.xml', DOCS / 'reader-edition.json', ROOT / 'README.md',
         ROOT / 'CHANGELOG.md', ROOT / 'documentation/TANGLE_STATE.md', graph, adventure]
before = [p.read_bytes() for p in files]
subprocess.run([sys.executable, str(ROOT / 'scripts/build_reader_opening.py')], check=True)
assert before == [p.read_bytes() for p in files], 'Reader openings must rebuild without drift'

assert edition['reader_release'] == '0.43' and edition['date'] == '2026-11-22'
assert edition['graph_release'] == json.loads(graph.read_text())['meta']['release'] == '0.41'
assert json.loads(adventure.read_text())['reader_release'] == '0.42'
assert f'data-reader-release="{edition["reader_release"]}" href="/versions/" aria-label="Version history, current release {edition["reader_release"]}">Release {edition["reader_release"]}</a>' in home.read_text()
history_text = history.read_text()
rows = re.findall(r'<article id="([^"]+)">(.*?)</article>', history_text, re.S)
assert rows[0][0] == 'v0-43' and rows[1][0] == 'v0-42'
assert rows[0][1].count('class="current"') == history_text.count('class="current"') == 1
assert edition['release_url'] in rows[0][1] and 'href="/42/"' in rows[1][1]
assert edition['reading_url'] in Page(release).links and edition['release_url'] in Page(reading).links
assert 'aria-label="Open updates"' in release.read_text()
assert 'Graph research edition 0.41' in (DOCS / 'entries/index.html').read_text()
opening = Page(home)
guide = Page(reading)
assert '/reading/connections/#museum-store' in opening.links
for anchor in ('museum-store', 'regulation', 'learning', 'transduction', 'sources'):
    assert guide.ids.count(anchor) == 1 and '#' + anchor in guide.links
for key in ('heroSearch', 'surpriseMeHero', 'homeMetrics', 'quickLinks', 'alarm-title'):
    assert opening.ids.count(key) == 1
assert re.search(r'<div class="atlas-finder">\s*<h2>Inside the atlas</h2>\s*<div class="metrics" id="homeMetrics"', home.read_text()), 'Counts must immediately follow Inside the atlas in its right-hand finder'
assert '<!-- reader-coverage -->' not in home.read_text(), 'Do not restore the displaced lower counts card'
assert home.read_text().split('id="homeMetrics"', 1)[1].split('</div>\n', 1)[0].count('class="metric"') == 4, 'Counts must also be readable without JavaScript'
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
print('Museum reader 0.43 checked: badge, history, dated release, graph 0.41, adventure 0.42, three primary sources, four local readings, review labels, and repeat build.')
