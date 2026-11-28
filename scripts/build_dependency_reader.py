#!/usr/bin/env python3
"""Project the maintained graph into a focused, source-labelled dependency view."""
import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
SOURCE = ROOT / 'sources/dependency-reader'
MARK = 'dependency-reader-45'


def strip(text, key):
    return re.sub(r'<!-- ' + key + r' -->.*?<!-- /' + key + r' -->\s*', '', text, flags=re.S)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reverse', action='store_true')
    args = parser.parse_args()
    home_path, app_path = DOCS / 'index.html', DOCS / 'assets/app.js'
    home, app = home_path.read_text(encoding='utf-8'), app_path.read_text(encoding='utf-8')
    for key in [MARK + '-styles', MARK + '-model', MARK + '-nav']:
        home = strip(home, key)
    for key in [MARK + '-entry', MARK + '-card']:
        app = strip(app, key)
    if args.reverse:
        home = re.sub(r'assets/app.js\?v=[^"\s]+', 'assets/app.js?v=0.31', home)
        home_path.write_text(home, encoding='utf-8'); app_path.write_text(app, encoding='utf-8')
        return
    data = json.loads((ROOT / 'data/public-data.json').read_text(encoding='utf-8'))
    release = data['meta']['release']
    for name in ['dependency-model.js', 'dependency-reader.js', 'dependency-reader.css']:
        shutil.copyfile(SOURCE / name, DOCS / 'assets' / name)
    target = DOCS / 'dependencies'; target.mkdir(parents=True, exist_ok=True)
    (target / 'index.html').write_text((SOURCE / 'index.html').read_text(encoding='utf-8').replace('{{release}}', release), encoding='utf-8')
    styles = '<!-- ' + MARK + '-styles --><link rel="stylesheet" href="/assets/dependency-reader.css?v=' + release + '"><!-- /' + MARK + '-styles -->\n'
    home = home.replace('</head>', styles + '</head>', 1)
    model = '\n<!-- ' + MARK + '-model --><script src="/assets/dependency-model.js?v=' + release + '"></script><!-- /' + MARK + '-model -->\n'
    home, count = re.subn(r'(<script\b[^>]*\bsrc="assets/public-data.js[^\"]*"[^>]*></script>)', lambda match: match[1] + model, home, count=1)
    assert count == 1, 'The reader dataset must load before the dependency model'
    nav = '<!-- ' + MARK + '-nav --><a href="/dependencies/">Predecessors and dependents</a><!-- /' + MARK + '-nav -->'
    home, count = re.subn(r'(<nav class="main-nav"[^>]*>)', lambda match: match[1] + nav, home, count=1)
    assert count == 1, 'Missing atlas navigation'
    home = re.sub(r'assets/app.js\?v=[^"\s]+', 'assets/app.js?v=' + release + '-dependencies-20261128', home)
    entry = '''<!-- dependency-reader-45-entry -->
      <nav class="dependency-entry-links" aria-label="Predecessor and dependent views">
        <a href="/dependencies/?entry=${encodeURIComponent(node.id)}&amp;side=predecessors">Necessary predecessors (${window.TANGLE_DEPENDENCIES?.direct(node.id).predecessors.length ?? 0})</a>
        <a href="/dependencies/?entry=${encodeURIComponent(node.id)}&amp;side=dependents">Dependent entries (${window.TANGLE_DEPENDENCIES?.direct(node.id).dependents.length ?? 0})</a>
      </nav>
      <!-- /dependency-reader-45-entry -->
      '''
    anchor = '<div class="entry-actions">'
    assert app.count(anchor) >= 1, 'Missing entry actions'
    app = app.replace(anchor, entry + anchor, 1)
    start, end = app.index('  function card(node)'), app.index('  function bindCards(', app.index('  function card(node)'))
    card = app[start:end]
    links = '''<!-- dependency-reader-45-card --><nav class="dependency-card-links" aria-label="Dependency views">
        <a href="/dependencies/?entry=${encodeURIComponent(node.id)}&amp;side=predecessors">Predecessors (${window.TANGLE_DEPENDENCIES?.direct(node.id).predecessors.length ?? 0})</a>
        <a href="/dependencies/?entry=${encodeURIComponent(node.id)}&amp;side=dependents">Dependents (${window.TANGLE_DEPENDENCIES?.direct(node.id).dependents.length ?? 0})</a>
      </nav><!-- /dependency-reader-45-card -->
    '''
    assert card.count('</article>') == 1, 'Missing browse-card closure'
    card = card.replace('</article>', links + '</article>', 1)
    app = app[:start] + card + app[end:]
    home_path.write_text(home, encoding='utf-8'); app_path.write_text(app, encoding='utf-8')
    sitemap = DOCS / 'sitemap.xml'
    text = sitemap.read_text(encoding='utf-8')
    if 'https://transduction.systems/dependencies/' not in text:
        text = text.replace('</urlset>', '<url><loc>https://transduction.systems/dependencies/</loc><lastmod>2026-11-28</lastmod></url></urlset>')
        sitemap.write_text(text, encoding='utf-8')
    print('Dependency reader built: source-labelled prerequisite chains, full relation mode, and entry-card access.')


if __name__ == '__main__':
    main()
