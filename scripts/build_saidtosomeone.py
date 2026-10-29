"""Build the source-led HvF register without changing the atlas dataset."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources/saidtosomeone'
DOCS = ROOT / 'docs'
DEST = DOCS / 'saidtosomeone'
DEST.mkdir(parents=True, exist_ok=True)

register = json.loads((SOURCE / 'maxims.json').read_text(encoding='utf-8'))
ledger = json.loads((SOURCE / 'source-ledger.json').read_text(encoding='utf-8'))
entries = register['entries']
source_ids = {source['id'] for source in ledger['sources']}
assert len({entry['id'] for entry in entries}) == len(entries), 'Duplicate register IDs'
assert all(set(entry['source_ids']) <= source_ids for entry in entries), 'Unknown source in register'
labels = {'primary': 'In his writing or an interview', 'reported': 'Reported or remembered', 'paraphrase': 'Paraphrase — follow the original', 'attribution': 'Attribution needs care'}

cards = []
contents = []
for number, entry in enumerate(entries, 1):
    key, title = escape(entry['id'], quote=True), escape(entry['title'])
    kind = entry['kind']
    contents.append(f'<li><a href="#{key}">{title}</a></li>')
    cards.append(f'<article id="{key}" class="maxim" data-evidence="{kind}">'
                 f'<div class="maxim-header"><a class="number" href="#{key}" aria-label="Link to {title}">{number:02d}</a><h3>{title}</h3></div>'
                 f'<p class="evidence-label">{labels[kind]}</p>{entry["body_html"]}</article>')
register_html = ('<details class="register-contents"><summary>Browse every entry by title</summary><ol>'
                 + ''.join(contents) + '</ol></details>'
                 '<div class="register-controls" hidden><label for="maxim-search">Find a saying or source<input id="maxim-search" type="search" placeholder="Try choices, information, Brün…"></label>'
                 '<label for="evidence-filter">Show<select id="evidence-filter"><option value="all">All entries</option>'
                 + ''.join(f'<option value="{kind}">{label}</option>' for kind, label in labels.items())
                 + '</select></label><button id="clear-filters" type="button">Clear</button></div>'
                 f'<p id="register-count" class="meta" role="status" aria-live="polite">{len(entries)} entries, with variants kept together.</p>'
                 '<div class="maxims">' + '\n'.join(cards) + '</div>')

anthology = register['anthology']
assert [str(i) for i in range(1, 30)] == [row[0] for row in anthology['index'][:29]], 'Anthology coverage must include all 29 items in order'
anthology_rows = []
for number, topic in anthology['index']:
    key = 'anthology-' + re.sub(r'[^a-z0-9]+', '-', number.lower())
    link = f'<a href="{escape(anthology["url"], quote=True)}" aria-label="Original anthology entry {escape(number, quote=True)}: {escape(topic, quote=True)}">{escape(topic)}</a>'
    companion = anthology.get('crosslinks', {}).get(number)
    if companion:
        link += f' <a class="crosslink" href="#{companion}" aria-label="Read the register entry for anthology item {number}">↳</a>'
    anthology_rows.append(f'<li id="{key}"><span class="anthology-number">{escape(number)}</span>{link}</li>')
anthology_html = '<ol class="anthology-index">' + ''.join(anthology_rows) + '</ol>'

series_html = []
for series in register.get('other_series', []):
    series_html.append(f'<details class="source-series" id="{escape(series["id"], quote=True)}"><summary>{escape(series["title"])}</summary>'
                       f'<p>{series["intro_html"]}</p><ol class="series-index">'
                       + ''.join(f'<li><strong>{escape(row[0])}</strong> {escape(row[1])}</li>' for row in series['index'])
                       + f'</ol><p class="source">{series["source_html"]}</p></details>')

page = (SOURCE / 'page.html').read_text(encoding='utf-8')
for marker, value in [('MAXIM_REGISTER', register_html), ('ANTHOLOGY_INDEX', anthology_html), ('OTHER_SERIES', '\n'.join(series_html)), ('REGISTER_TOTAL', str(len(entries)))]:
    assert f'<!-- {marker} -->' in page, f'Missing page marker: {marker}'
    page = page.replace(f'<!-- {marker} -->', value)
(DEST / 'index.html').write_text(page, encoding='utf-8')

for source, output in [('style.css', 'style.css'), ('source-ledger.json', 'source-ledger.json'), ('maxims.json', 'maxims.json')]:
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
    'Companion page, edition **1.1, 29 October 2026**: [Heinz von Foerster’s maxims, talks, and writing](https://transduction.systems/saidtosomeone/). '
    f'All 29 anthology items indexed; {len(entries)} register entries distinguish primary formulations, reported sayings, paraphrases, and variants. '
    'Further numbered collections, four firsthand recollections, recordings, papers, and Benjamin’s imagined conversation with Don Van Vliet. '
    'The large TNT mark animates, pauses, and changes using the main site’s asset family. '
    'One deliberately invented marginal saying is identified by a dagger and a visible contains hallucinations warning. Atlas dataset release and counts are unchanged.',
    '## Release 0.23')

path = ROOT / 'CHANGELOG.md'
text = path.read_text(encoding='utf-8')
heading = '## Said to someone 1.1 — 29 October 2026'
if heading not in text:
    text = text.replace('# Changelog', '# Changelog\n\n' + heading + '\n\n'
        f'Expanded /saidtosomeone/ from ten selections to {len(entries)} source-led entries, without a numerical cap. '
        'Indexed all 29 items of the 1995 anthology, its subitems and source anomalies, all 12 main Notes propositions, every visible numbered Luhmann entry, '
        'and the complete three-theorem and three-education sequences. Kept exact formulations, variants, paraphrases, witnesses, borrowed attributions, and unlocated primary wording distinct. '
        'Added a searchable register and same-site living-mark animation, pause, motif changes, keyboard control, and reduced-motion support. '
        'Existing stories, media, imaginative dialogue, disclosed invention, and Open updates route remain. This companion update does not change the atlas dataset or graph counts.\n', 1)
path.write_text(text, encoding='utf-8')

state = ROOT / 'documentation/TANGLE_STATE.md'
text = state.read_text(encoding='utf-8')
start, end = '<!-- saidtosomeone-state-1 -->', '<!-- /saidtosomeone-state-1 -->'
note = (start + '\n\n## Companion page: Said to someone\n\n'
    f'Edition 1.1, 29 October 2026. /saidtosomeone/ has {len(entries)} entries with exact and reported wording, paraphrases, and variants. '
    'It indexes all 29 anthology items and supplementary material, the 12 main Notes propositions, all 11 visible Luhmann labels, and two three-item sequences. It also has '
    'four firsthand recollections, video, audio, primary writing, and Benjamin’s imagined conversation with Don Van Vliet. '
    'One deliberate marginal invention is identified by a dagger, explicit source note, and contains hallucinations warning. '
    'The page reuses the main site’s mark family with animation, pause, motif changes, keyboard control, and reduced-motion support. It is linked from the home page and source library. '
    'The source ledger distinguishes text verification from full playback; it makes no exhaustive-collection or first-use claim. '
    'This companion update does not change the atlas graph or counts. Source packet: sources/saidtosomeone/PACKET.md. '
    'The current Publish workflow and deployment.json identify validation and the deployed revision.\n\n' + end + '\n')
if start in text:
    text = re.sub(re.escape(start) + r'.*?' + re.escape(end) + r'\n?', lambda _: note, text, flags=re.S)
else:
    text = text.rstrip() + '\n\n' + note
state.write_text(text, encoding='utf-8')
# The companion packet stays in SOURCE; the current atlas release owns NEXT_WORK.md.

ledger = json.loads((DEST / 'source-ledger.json').read_text(encoding='utf-8'))
print(f'Built Said to someone {ledger["edition"]}: {len(entries)} register entries, full anthology index, {len(ledger["sources"])} source records, and two atlas entry points. Dataset unchanged.')
