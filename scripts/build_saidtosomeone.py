"""Build the bounded HvF companion page without changing the atlas dataset."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources/saidtosomeone'
DOCS = ROOT / 'docs'
DEST = DOCS / 'saidtosomeone'
DEST.mkdir(parents=True, exist_ok=True)

for source, output in [('page.html', 'index.html'), ('style.css', 'style.css'), ('source-ledger.json', 'source-ledger.json')]:
    (DEST / output).write_bytes((SOURCE / source).read_bytes())


def insert_block(path, name, block, before):
    text = path.read_text(encoding='utf-8')
    start, end = f'<!-- {name} -->', f'<!-- /{name} -->'
    replacement = start + '\n' + block + '\n' + end + '\n'
    if start in text:
        text = re.sub(re.escape(start) + r'.*?' + re.escape(end) + r'\n?', lambda _: replacement, text, flags=re.S)
    else:
        if before not in text:
            raise ValueError(f'Missing insertion point in {path.relative_to(ROOT)}')
        text = text.replace(before, replacement + before, 1)
    path.write_text(text, encoding='utf-8')


insert_block(DOCS / 'index.html', 'saidtosomeone-1',
    '<section class="resource-pathways" id="saidToSomeoneCallout"><h2>Heinz von Foerster: said to someone</h2>'
    '<p>The collected aphorisms, checked sources, stories from friends, video, audio, and writing — with a flight of fancy involving Captain Beefheart.</p>'
    '<p><a class="button" href="/saidtosomeone/">Read the maxims and follow the sources</a></p></section>',
    '<section class="resource-pathways" id="earlyCyberneticsCallout">')

insert_block(DOCS / 'library/index.html', 'saidtosomeone-library-1',
    '<p><a href="/saidtosomeone/">Heinz von Foerster’s maxims, stories, talks, and writing</a> — a guide to the sources, recollections, and recordings, with a confessed invention.</p>',
    '<details class="coverage">')

path = DOCS / 'sitemap.xml'
text = path.read_text(encoding='utf-8')
if '<loc>https://transduction.systems/saidtosomeone/</loc>' not in text:
    text = text.replace('</urlset>', '<url><loc>https://transduction.systems/saidtosomeone/</loc><lastmod>2026-10-29</lastmod></url>\n</urlset>')
path.write_text(text, encoding='utf-8')

insert_block(ROOT / 'README.md', 'saidtosomeone-readme-1',
    'Companion page, edition **1.0, 29 October 2026**: [Heinz von Foerster’s maxims, talks, and writing](https://transduction.systems/saidtosomeone/). '
    'The existing 1995 anthology, ten source-checked entries, four firsthand recollections, recordings, papers, and Benjamin’s imagined conversation with Don Van Vliet. '
    'One deliberately invented marginal saying is identified by a dagger and a visible contains hallucinations warning. Atlas dataset release and counts are unchanged.',
    '## Release 0.23')

path = ROOT / 'CHANGELOG.md'
text = path.read_text(encoding='utf-8')
heading = '## Said to someone 1.0 — 29 October 2026'
if heading not in text:
    text = text.replace('# Changelog', '# Changelog\n\n' + heading + '\n\n'
        'Added /saidtosomeone/ with a large existing TNT mark, the credited 1995 HvF anthology, ten sourced entries, the documented Beer connection, '
        'four firsthand recollections with short excerpts, video and audio routes, primary writing, and the Chosen Path HvF/Don Van Vliet imagined dialogue. '
        'One deliberate marginal invention has a dagger, explicit source note, and contains hallucinations warning. Homepage and source-library links make the page discoverable. '
        'A deterministic build and source ledger preserve the page and attribution distinctions. Atlas dataset release 0.34 and graph counts are unchanged.\n', 1)
path.write_text(text, encoding='utf-8')

state = ROOT / 'documentation/TANGLE_STATE.md'
text = state.read_text(encoding='utf-8')
start, end = '<!-- saidtosomeone-state-1 -->', '<!-- /saidtosomeone-state-1 -->'
note = (start + '\n\n## Companion page: Said to someone\n\n'
    'Edition 1.0, 29 October 2026. /saidtosomeone/ brings the existing Heinz von Foerster anthology together with ten selected entries, checked attribution, '
    'four firsthand recollections, video, audio, primary writing, and Benjamin’s imagined conversation with Don Van Vliet. '
    'One deliberate marginal invention is identified by a dagger, explicit source note, and contains hallucinations warning. '
    'The page reuses a large existing TNT mark and is linked from the home page and source library. '
    'The source ledger distinguishes text verification from full playback; it makes no exhaustive-collection or first-use claim. '
    'The atlas graph and release 0.34 counts are unchanged. Source packet: sources/saidtosomeone/PACKET.md. '
    'The current Publish workflow and deployment.json identify validation and the deployed revision.\n\n' + end + '\n')
if start in text:
    text = re.sub(re.escape(start) + r'.*?' + re.escape(end) + r'\n?', lambda _: note, text, flags=re.S)
else:
    text = text.rstrip() + '\n\n' + note
state.write_text(text, encoding='utf-8')
(ROOT / 'documentation/NEXT_WORK.md').write_bytes((SOURCE / 'PACKET.md').read_bytes())

ledger = json.loads((DEST / 'source-ledger.json').read_text(encoding='utf-8'))
print(f'Built Said to someone {ledger["edition"]}: ten selected entries, {len(ledger["sources"])} source records, and two atlas entry points. Dataset unchanged.')
