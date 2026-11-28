#!/usr/bin/env python3
"""Check the generated dependency reader and Python/JavaScript graph parity."""
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import parse_qs, unquote, urlsplit

from dependency_model import DependencyIndex

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'


class SummaryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_summary = False
        self.count = 0
        self.side = None
        self.divs = []
        self.ids = {'predecessors': set(), 'dependents': set()}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'section' and 'dependency-summary' in attrs.get('class', '').split():
            self.in_summary = True
            self.count += 1
        if not self.in_summary:
            return
        if tag == 'div':
            self.divs.append(self.side)
            if attrs.get('id') in self.ids:
                self.side = attrs['id']
        if tag == 'a' and self.side:
            href = urlsplit(attrs.get('href', ''))
            match = re.fullmatch(r'/entries/([^/]+)/', href.path)
            ident = unquote(match[1]) if match else parse_qs(href.fragment).get('id', [None])[0]
            if ident:
                self.ids[self.side].add(ident)

    def handle_endtag(self, tag):
        if self.in_summary and tag == 'div' and self.divs:
            self.side = self.divs.pop()
        if self.in_summary and tag == 'section':
            self.in_summary = False


def main():
    data_path = DOCS / 'assets/public-data.json'
    data = json.loads(data_path.read_text(encoding='utf-8'))
    index = DependencyIndex(data)
    node = shutil.which('node')
    assert node, 'Node is required for independent Python/JavaScript graph parity'
    result = subprocess.run([node, str(ROOT / 'scripts/test_dependency_model.cjs'), '--dump-direct', str(data_path)],
                            check=True, capture_output=True, text=True, encoding='utf-8')
    js = json.loads(result.stdout)
    py = {ident: index.direct(ident) for ident in sorted(index.nodes)}
    assert js['direct'] == py, 'Python and JavaScript disagree on canonical direct prerequisite/dependent IDs'
    assert js['canonical_public_count'] == len(index.nodes)
    assert js['strict_types'] == sorted(index.strict)

    for asset in ['dependency-model.js', 'dependency-reader.js', 'dependency-reader.css']:
        assert (DOCS / 'assets' / asset).read_bytes() == (ROOT / 'sources/dependency-reader' / asset).read_bytes(), f'Stale generated asset: {asset}'
    page = (DOCS / 'dependencies/index.html').read_text(encoding='utf-8')
    for ident in ['dependency-search', 'dependency-query', 'dependency-mode', 'dependency-depth', 'dependency-copy',
                  'dependency-predecessors', 'dependency-focus', 'dependency-dependents', 'dependency-related', 'dependency-cycle']:
        assert page.count(f'id="{ident}"') == 1, f'Missing or duplicate reader control: {ident}'
    assert '{{release}}' not in page
    assert 'aria-label="Open updates"' in page
    assert 'https://www.systemspractice.org/sysbok-from-scio' in page
    assert 'recorded' in page.lower() and 'scope' in page.lower() and 'review' in page.lower()
    home = (DOCS / 'index.html').read_text(encoding='utf-8')
    dataset_at = home.index('src="assets/public-data.js')
    model_at = home.index('src="/assets/dependency-model.js')
    app_at = home.index('src="assets/app.js')
    assert dataset_at < model_at < app_at, 'Dependency model must initialise after data and before entry/card rendering'
    assert home.count('href="/dependencies/"') >= 1
    app = (DOCS / 'assets/app.js').read_text(encoding='utf-8')
    assert app.count('<!-- dependency-reader-45-entry -->') == 1
    assert app.count('<!-- dependency-reader-45-card -->') == 1
    assert 'dependency-entry-links' in app and 'dependency-card-links' in app
    assert 'https://transduction.systems/dependencies/' in (DOCS / 'sitemap.xml').read_text(encoding='utf-8')

    static_checked = 0
    if data.get('biographies_107_45'):
        profiles = {index.canonical(row['node_id']) for row in data['profiles']} & index.nodes.keys()
        for ident in sorted(profiles):
            html = (DOCS / 'entries' / ident / 'index.html').read_text(encoding='utf-8')
            summary = SummaryParser()
            summary.feed(html)
            assert summary.count == 1, f'Expected one static dependency summary: {ident}'
            expected = index.direct(ident)
            assert {key: sorted(values) for key, values in summary.ids.items()} == expected, f'Static summary IDs differ from the graph: {ident}'
            for direction in ['predecessors', 'dependents']:
                assert f'({len(expected[direction])})</h2>' in html, f'Static summary count missing: {ident}/{direction}'
            static_checked += 1
    report = {'release': data['meta']['release'], 'canonical_public_entries': len(index.nodes),
              'strict_edge_count': js['strict_edge_count'], 'python_js_direct_id_parity': 'all canonical public IDs',
              'static_summaries_checked': static_checked,
              'static_summary_gate': 'biographies_107_45 present' if data.get('biographies_107_45') else 'not expected before biographies_107_45',
              'generated_assets_current': True}
    output = ROOT / 'validation/dependency-reader'
    output.mkdir(parents=True, exist_ok=True)
    (output / 'validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
