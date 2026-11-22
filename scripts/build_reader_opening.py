#!/usr/bin/env python3
"""Publish the atlas opening while retaining the historical rebuild baseline."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'sources/reader-opening'
HOME = ROOT / 'docs/index.html'
STYLESHEET = '<link rel="stylesheet" href="/assets/reader-opening.css">'
historical = (CONTENT / 'historical-home.html').read_text().rstrip()
opening = (CONTENT / 'home.html').read_text().rstrip()
controls = historical[historical.index('<div class="smart-search'):historical.index('          <p class="start-here-link">')].strip()
controls = controls.replace('Search for an idea, person, method or law', 'Search the atlas').replace('Try viability, feedback, VSM, emergence…', 'For example, viability or Stafford Beer')
controls, _, related = controls.partition('<div class="quick-links"')
related = '<div class="quick-links"' + related
actions = '<p class="hero-actions"><a href="#view=item&id=concept_viability&from=home" id="surpriseMeHero" class="surprise-me">Open a random entry</a> · <a href="/canon-and-lineage/">Who gets included in the atlas?</a></p>'
opening = opening.replace('{{search}}', controls.strip()).replace('{{related}}', related.strip()).replace('{{actions}}', actions)
coverage = '''      <!-- reader-coverage -->
      <a class="hero-panel release-panel" href="#view=about" aria-label="About the atlas and its coverage">
        <h2>Atlas coverage</h2>
        <div class="metrics" id="homeMetrics"></div>
        <span class="panel-link">How entries and connections are selected</span>
      </a>
      <!-- /reader-coverage -->
'''
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--reverse', action='store_true')
args = parser.parse_args()
text = HOME.read_text()
if args.reverse:
    text = re.sub(r'      <!-- reader-opening -->.*?<!-- /reader-opening -->', lambda m: historical, text, flags=re.S)
    text = re.sub(r'      <!-- reader-coverage -->.*?<!-- /reader-coverage -->\n', '', text, flags=re.S)
    text = text.replace(STYLESHEET + '\n', '')
elif '<!-- reader-opening -->' in text:
    text = re.sub(r'      <!-- reader-opening -->.*?<!-- /reader-opening -->', lambda m: opening, text, flags=re.S)
else:
    if historical not in text:
        raise ValueError('Historical atlas opening has changed: reconcile its controls with the reader opening.')
    text = text.replace(historical, opening, 1)
    before = '      <section class="author-strip">'
    if text.count(before) != 1:
        raise ValueError('Expected one curator section on the homepage')
    text = text.replace(before, coverage + before, 1)
    text = text.replace('</head>', STYLESHEET + '\n</head>', 1)
copy_edits = json.loads((CONTENT / 'interface-copy.json').read_text())
for original, revised in copy_edits.items():
    before, after = (revised, original) if args.reverse else (original, revised)
    text = text.replace(before, after)
HOME.write_text(text)

reading = ROOT / 'docs/reading/connections/index.html'
if reading.exists():
    text = reading.read_text()
    text = re.sub(r'<!-- reader-example -->.*?<!-- /reader-example -->\n', '', text, flags=re.S)
    example_link = '<a href="#museum-store">The museum alarm</a>'
    text = text.replace(example_link, '')
    if not args.reverse:
        anchor = '<section id="regulation">'
        if text.count(anchor) != 1:
            raise ValueError('Missing regulation section in reading guide')
        example = (CONTENT / 'museum.html').read_text().strip()
        text = text.replace(anchor, '<!-- reader-example -->' + example + '<!-- /reader-example -->\n' + anchor, 1)
        text = text.replace('<nav aria-label="Reading routes">', '<nav aria-label="Reading routes">' + example_link, 1)
    reading.write_text(text)

work = ROOT / 'documentation/NEXT_WORK.md'
work_text = re.sub(r'<!-- reader-opening-packet -->.*?<!-- /reader-opening-packet -->\n\n', '', work.read_text(), flags=re.S)
if not args.reverse:
    packet = '<!-- reader-opening-packet -->\n' + (CONTENT / 'packet.txt').read_text().strip() + '\n<!-- /reader-opening-packet -->\n\n'
    work_text = work_text.replace('# Next work\n', '# Next work\n' + packet, 1)
work.write_text(work_text)
