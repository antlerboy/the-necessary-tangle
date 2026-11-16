"""A readable release history from existing project records; no new releases."""
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re


class ReleasePage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.main = False
        self.tag = None
        self.parts = []
        self.paragraphs = []
        self.heading = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'main':
            self.main = True
        if self.main and tag in ('h1', 'p'):
            self.tag, self.parts = tag, []

    def handle_data(self, data):
        if self.tag:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == self.tag:
            text = ' '.join(''.join(self.parts).split())
            if tag == 'h1':
                self.heading = text
            elif text:
                self.paragraphs.append(text)
            self.tag = None
        if tag == 'main':
            self.main = False


def plain(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'[`*_]', '', text)
    return ' '.join(re.sub(r'^\s*[-*]\s+', '', text, flags=re.M).split())


def build(root: Path, reader_release: str):
    docs = root / 'docs'
    changelog = (root / 'CHANGELOG.md').read_text(encoding='utf-8')
    headings = list(re.finditer(r'^## (.+)$', changelog, flags=re.M))
    records = {}
    for index, match in enumerate(headings):
        header = match.group(1)
        version = re.match(r'^(0\.\d+(?:\.\d+)?)(?:-[\w-]+)?\s+[—–-]\s+(.+)$', header)
        if not version:
            continue
        number, date = version.groups()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(changelog)
        body = changelog[match.end():end].strip()
        first = re.split(r'\n\s*\n', body, maxsplit=1)[0]
        records[number] = dict(version=number, date=date, summary=plain(first), details='', title='')

    # Public release pages supply dates/details where the changelog is sparse.
    for path in sorted((docs / 'updates').glob('*/index.html')):
        page = ReleasePage()
        page.feed(path.read_text(encoding='utf-8'))
        lead = next((p for p in page.paragraphs[:3] if re.search(r'(?i)\brelease\s+0\.', p)), '')
        version = re.search(r'(?i)\brelease\s+(0\.\d+(?:\.\d+)?)', lead)
        if not version:
            continue
        number = version.group(1)
        route = '/' + path.parent.relative_to(docs).as_posix() + '/'
        if number not in records:
            summary = next((p for p in page.paragraphs if p != lead), page.heading)
            date = re.search(r'\d{1,2}\s+[A-Za-z]+\s+2026', lead)
            records[number] = dict(version=number, date=date.group(0) if date else '', summary=summary, details='', title='')
        # A later follow-up using the same graph version is not the original release.
        row = records[number]
        if not row['details']:
            row['details'], row['title'] = route, page.heading

    assert reader_release in records, 'Current reader release needs a history record'
    cards = []
    for number, row in sorted(records.items(), key=lambda pair: tuple(map(int, pair[0].split('.'))), reverse=True):
        ident = 'v' + number.replace('.', '-')
        href = '/42/' if number == '0.42' else row['details'] or '#' + ident
        current = ' <span class="current">Current reader release</span>' if number == reader_release else ''
        title = '<span class="release-title">' + escape(row['title']) + '</span>' if row['title'] else ''
        details = '<p class="release-actions"><a href="' + escape(row['details']) + '">Release account</a></p>' if row['details'] else ''
        if number == '0.42':
            details = '<p class="release-actions"><a href="/42/">Enter the adventure</a> · <a href="/updates/2026-11-15-42/">Release account</a></p>'
        cards.append('<article id="' + ident + '"><p class="release-date">' + escape(row['date']) + current + '</p><h2><a href="' + escape(href) + '">v' + escape(number) + '</a>' + title + '</h2><p>' + escape(row['summary']) + '</p>' + details + '</article>')
    target = docs / 'versions/index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Version history | The Necessary Tangle</title><meta name="description" content="Recorded releases of The Necessary Tangle, with what changed and links to their release accounts. Version 0.42 opens the text adventure."><link rel="canonical" href="https://transduction.systems/versions/"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/assets/readable-atlas.css"><style>.version-history article{border-top:1px solid #d8d0c0;padding:1.3rem 0;scroll-margin-top:1rem}.version-history h2{display:flex;flex-wrap:wrap;gap:.4rem 1rem;align-items:baseline;margin:.25rem 0 .8rem}.release-title{font-size:1.12rem;font-weight:normal}.release-date,.release-actions{font: .86rem/1.6 system-ui,sans-serif}.current{display:inline-block;margin-left:.7rem;padding:.1rem .5rem;background:#f1eadf;color:#682028;border-radius:3px}.version-history article>p{margin-block:.55rem}#openUpdates{position:fixed;right:0;bottom:0;width:44px;height:44px;z-index:99999}#openUpdates:after{content:"";position:absolute;right:8px;bottom:8px;width:5px;height:5px;background:#862719;border-radius:50%;box-shadow:0 0 0 1px white}#openUpdates:focus-visible{outline:3px solid #ffbf47;outline-offset:-3px}</style></head><body class="readable-atlas"><a class="skip-link" href="#main">Skip to content</a><header><a class="brand" href="/">The Necessary Tangle</a><nav aria-label="Main navigation"><a href="/">Atlas</a><a href="/42/">Adventure</a><a href="/updates/">Updates</a><a href="/entries/">Entries</a></nav></header><main id="main"><h1>Version history</h1><p>Recorded releases, most recent first. Open a version’s release account to see what changed. <a href="/42/">v0.42 opens the adventure.</a></p><div class="version-history">''' + ''.join(cards) + '''</div></main><footer><p>Curated by Benjamin P Taylor. <a href="/updates/">Dated updates and release accounts</a> · <a href="https://github.com/antlerboy/the-necessary-tangle/blob/main/CHANGELOG.md">Full changelog</a>.</p></footer><a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a></body></html>''', encoding='utf-8')
    sitemap = docs / 'sitemap.xml'
    content = sitemap.read_text(encoding='utf-8')
    if 'https://transduction.systems/versions/' not in content:
        content = content.replace('</urlset>', '<url><loc>https://transduction.systems/versions/</loc></url></urlset>')
        sitemap.write_text(content, encoding='utf-8')
    print(f'Version history built from {len(records)} recorded releases; v0.42 opens /42/.')
