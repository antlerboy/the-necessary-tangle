"""Publish the current reader edition independently of graph and feature versions."""
import json
import re
from datetime import date
from html import escape
from pathlib import Path

from build_readable_atlas import page
from version_history import build as build_history

BASE = 'https://transduction.systems'


def marked(path, anchor, content, reverse):
    start, end = '<!-- museum-release -->', '<!-- /museum-release -->'
    text = re.sub(re.escape(start) + '.*?' + re.escape(end) + r'\n', '', path.read_text(), flags=re.S)
    if not reverse:
        if anchor not in text:
            raise ValueError(f'Missing insertion point in {path}')
        text = text.replace(anchor, anchor + start + '\n' + content + '\n' + end + '\n', 1)
    path.write_text(text)


def build(root: Path, reverse=False):
    docs = root / 'docs'
    edition = json.loads((docs / 'reader-edition.json').read_text())
    number, graph = edition['reader_release'], edition['graph_release']
    stamp = date.fromisoformat(edition['date'])
    display_date = f'{stamp.day} {stamp:%B %Y}'
    title, reading, route = edition['title'], edition['reading_url'], edition['release_url']
    summary = edition['summary']
    badge = f'<a id="releaseBadge" data-reader-release="{number}" href="/versions/" aria-label="Version history, current release {number}">Release {number}</a>'
    home = docs / 'index.html'
    if not reverse:
        content, count = re.subn(r'<(?:span|a) id="releaseBadge"[^>]*>Release [^<]+</(?:span|a)>', badge, home.read_text(), count=1)
        if count != 1:
            raise ValueError('Expected a release badge on the atlas home page')
        home.write_text(content)

    account = docs / route.strip('/') / 'index.html'
    if not reverse:
        account.parent.mkdir(parents=True, exist_ok=True)
        body = (f'<p><time datetime="{stamp.isoformat()}">{display_date}</time></p>'
                f'<p>{escape(summary)}</p><p><a href="{reading}">Read the museum alarm and its sources</a>.</p>'
                f'<p>The research graph stays at {graph}. The records and citations in <a href="/entries/">atlas entries</a> '
                'give the edition of that graph. The <a href="/42/">text adventure</a> appeared in reader release 0.42.</p>'
                '<p><a href="/versions/">Version history</a></p>')
        account.write_text(page(title, summary, route, body, number, edition_label='Reader release'))

    marked(docs / 'updates/index.html', '<main>\n',
           f'<section><h2><a href="{route}">Release {number} · {escape(title)}</a></h2><p>{display_date}. {escape(summary)}</p></section>', reverse)
    marked(root / 'README.md', '# The Necessary Tangle\n',
           f'Current reader release **{number}, {display_date}**. [{title}]({BASE}{reading}). [Release account]({BASE}{route}). Graph research edition **{graph}**.', reverse)
    marked(root / 'documentation/TANGLE_STATE.md', '# Current Tangle state\n',
           f'## Current reader release {number}\n\n{display_date}. [{title}]({BASE}{reading}) is a worked comparison of three primary sources. Entry and reading-route copy was revised. The research graph remains at {graph}. [Release account]({BASE}{route}).', reverse)

    if reverse:
        return
    changelog = root / 'CHANGELOG.md'
    record = f'## {number} — {display_date}\n\n{summary}\n\n'
    text = changelog.read_text()
    if f'## {number} — ' not in text:
        text = text.replace('# Changelog\n\n', '# Changelog\n\n' + record, 1)
        changelog.write_text(text)
    sitemap = docs / 'sitemap.xml'
    text = sitemap.read_text()
    if '<loc>' + BASE + route + '</loc>' not in text:
        text = text.replace('</urlset>', f'<url><loc>{BASE}{route}</loc><lastmod>{stamp.isoformat()}</lastmod></url></urlset>')
        sitemap.write_text(text)
    build_history(root, number)
