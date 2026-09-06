#!/usr/bin/env python3
"""Check current integrity, truthful coverage, static access, and retained assets."""
import hashlib
import json
import re
import subprocess
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from apply_iteration_09 import graph_metrics
from apply_iteration_17 import parse
from apply_relational_depth_16 import calculate_relational_depth
from apply_release_21 import COMPARATOR_SHA256, RECONCILIATION_SHA256, PACKAGE_SHA256
from refresh_graph_snapshot import calculate

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'


def load(path):
    return json.loads((ROOT / path).read_text())


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.headings = []
        self.rules = {}
        self.rule = None
        self.tags = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ('a', 'link', 'script'):
            self.links.append(attrs.get('href') or attrs.get('src') or '')
        if re.fullmatch('h[1-6]', tag):
            self.headings.append(int(tag[1]))
        if tag == 'li' and 'data-rule-number' in attrs:
            self.rule = int(attrs['data-rule-number'])
            self.rules[self.rule] = ''

    def handle_endtag(self, tag):
        if tag == 'li':
            self.rule = None

    def handle_data(self, data):
        if self.rule is not None:
            self.rules[self.rule] += data


def main():
    d = load('data/public-data.json')
    assert d['meta']['release'] == '0.22'
    assert d['meta']['generated'] == '2026-09-05'
    assert d['meta']['public_entry_count'] == 719
    assert (len(d['nodes']), len(d['edges']), len(d['profiles']), len(d['sources']), len(d['journeys'])) == (846, 1987, 137, 224, 24)
    assert d == load('docs/assets/public-data.json')
    assert d['graph_snapshot'] == calculate(d)
    assert d['relational_depth']['aggregate'] == calculate_relational_depth(d)['aggregate']
    assert d['ai_observations']['metrics'] == graph_metrics(d)
    for key in ('relational_depth', 'ai_observations', 'reading_list_inventory', 'reading_list_coverage', 'core_systems_practice'):
        assert d[key]['release'] == '0.22', key
    quality = load('data/relationship-quality.json')
    assert quality == load('docs/assets/relationship-quality.json')
    assert quality['current']['public_entries'] == 719
    assert quality['current']['all_edges'] == 1987
    for key in ('adversarial_review', 'doncaster_lineage_review'):
        assert quality[key] == d[key]
    for rows, key in ((d['nodes'],'id'), (d['sources'],'id'), (d['edges'],'id'), (d['profiles'],'node_id'), (d['journeys'],'id')):
        assert len({r[key] for r in rows}) == len(rows), key
    triples = [(e['source'], e['target'], e['relation_type']) for e in d['edges']]
    assert len(set(triples)) == len(triples), 'Duplicate typed assertions'
    for e in d['edges']:
        if not e['id'].startswith('e22_'):
            continue
        assert e['relation_type'] != 'conceptually_related_to'
        assert not e['reviewed_by'] and not e['reviewed_at']
        assert parse(e['source_ids']) and e['source_locator'] and e['scope_conditions']
        if e['relation_type'] == 'listed_in_bibliography':
            assert e['relation_family'] == 'documentary'

    intake = load('docs/assets/early-cybernetics-bibliography.json')
    original = load('sources/cybernetics-bibliographies/intake.json')
    assert d['early_cybernetics_corpus'] == intake
    assert 'Sean Manion' in json.dumps(intake) and 'Menion' not in json.dumps(intake)
    assert len(intake['entries']) == 48
    assert Counter(r['section'] for r in intake['entries']) == Counter({'selected-1952': 8, 'short-1956': 20, 'popular-1951': 15, 'popular-wiener': 5})
    assert [r['transcribed_entry'] for r in intake['entries']] == [r['transcribed_entry'] for r in original['entries']]
    assert intake['summary']['resolved_work_count'] == 45
    assert intake['summary']['unresolved_references'] == 1
    assert intake['summary']['selected_passage_reviews'] == 4
    assert intake['summary']['metadata_checks'] == 1
    assert intake['summary']['barrett_shepard_bibliography_rows_available'] == 0
    assert not any(r['full_text_reviewed'] for r in intake['entries'])
    nodes = {n['id'] for n in d['nodes']}
    journeys = {j['id'] for j in d['journeys']}
    for row in intake['entries']:
        assert row['node_id'] in nodes or row['work_key'] == 'current-biography'
        if row['review_status'] == 'selected_passages_reviewed':
            assert row['primary_url'].startswith('https://') and row['review_locator']

    rules = load('sources/redquadrant-rules.json')
    assert rules == load('docs/assets/redquadrant-rules.json')
    assert [r['number'] for r in rules['rules']] == list(range(1, 257))
    pages = ['systems-thinking/index.html', 'corpora/early-cybernetics/index.html', 'little-redquadrant-rules/index.html', 'updates/0.22/index.html']
    for path in pages:
        page = Page(DOCS / path)
        assert len(page.ids) == len(set(page.ids)), path
        assert page.headings.count(1) == 1, path
        assert all(b <= a + 1 for a, b in zip(page.headings, page.headings[1:])), path
        assert 'main' in page.ids and 'openUpdates' in page.ids, path
        assert any(tag == 'a' and attrs.get('href') == '#main' for tag, attrs in page.tags)
        assert any(tag == 'a' and attrs.get('aria-label') == 'Open updates' for tag, attrs in page.tags)
        for url in page.links:
            u = urlsplit(url)
            if u.scheme or u.netloc:
                continue
            target = DOCS / u.path.lstrip('/') if u.path.startswith('/') else (DOCS / path).parent / u.path
            if target.is_dir():
                target /= 'index.html'
            assert target.is_file(), (path, url)
            if u.fragment.startswith('view='):
                query = parse_qs(u.fragment)
                identity = query.get('id', [None])[0]
                if identity:
                    assert identity in (journeys if query['view'] == ['journeys'] else nodes), (path, url)
            elif u.fragment:
                assert u.fragment in Page(target).ids, (path, url)
    # Public punctuation follows Benjamin's instruction; canonical wording is otherwise identical.
    assert Page(DOCS / pages[2]).rules == {r['number']: r['text'].replace('—', ', ').replace('–', '-') for r in rules['rules']}
    css = (DOCS / 'assets/learning-pages.css').read_text()
    assert all(s in css for s in (':focus-visible', 'prefers-reduced-motion', 'prefers-color-scheme:dark', '@media print', '760px'))
    index = (DOCS / 'index.html').read_text()
    assert '<span id="releaseBadge">Release 0.22</span>' in index
    assert 'class="start-here-link"' in index and 'id="earlyCyberneticsCallout"' in index
    enhancements = (DOCS / 'assets/site-enhancements.js').read_text()
    assert 'setupLittleRules();' not in enhancements
    assert 'function setupLittleRules()' in enhancements
    assert 'keepRuleBeneathBrand();' not in (DOCS / 'assets/iteration-20.js').read_text()
    assert 'version: 0.22' in (ROOT / 'CITATION.cff').read_text()
    assert '## Release 0.22' in (ROOT / 'README.md').read_text()
    assert '719 public entries' in (ROOT / 'documentation/ai-observations.md').read_text()
    assert d['meta']['systemic_evolution_review_archive_sha256'] == PACKAGE_SHA256
    for name, expected in [('comparator-systemic-evolution.json', COMPARATOR_SHA256), ('systemic-evolution-reconciliation.json', RECONCILIATION_SHA256)]:
        content = (ROOT / 'data' / name).read_bytes()
        assert hashlib.sha256(content).hexdigest() == expected, name
        assert content == (DOCS / 'assets' / name).read_bytes(), name
    for published, reviewed in {
        'assets/systemic-evolution-map.js': 'site/assets/systemic-evolution-map.js',
        'assets/prior-maps.css': 'site/assets/prior-maps.css',
        'assets/systemic-evolution-review-manifest.json': 'review-manifest.json',
        'assets/systemic-evolution-publication-approval.json': 'PUBLICATION_APPROVAL.json',
    }.items():
        assert (DOCS / published).read_bytes() == (ROOT / 'sources/systemic-evolution/review-1' / reviewed).read_bytes(), published
    for path in ['early-cybernetics.js', 'redquadrant-rules.js', 'site-enhancements.js', 'iteration-20.js']:
        subprocess.run(['node', '--check', str(DOCS / 'assets' / path)], check=True)
    print('Release 0.22 passed: current data, evidence coverage, 256 preserved rules, static routes, source-owner assets, and script syntax.')


if __name__ == '__main__':
    main()
