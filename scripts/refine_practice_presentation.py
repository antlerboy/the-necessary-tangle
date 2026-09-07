#!/usr/bin/env python3
"""Apply the author's enduring introduction and alpha status after route generation."""
from pathlib import Path
import html
import json
import re
from refresh_graph_snapshot import write
from apply_iteration_09 import graph_metrics
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
PACK = DOCS / 'systems-thinking/practice'
TITLE = 'Systemic systems methods practice for systems practice'
CITATION = 'Taylor, B. P. (2026). Systemic systems methods practice for systems practice. Alpha version. The Necessary Tangle.'
NOTICE = 'Alpha version. The original teaching material has not had independent specialist pedagogical review. These exercises support technical learning; they do not establish professional competence or accreditation.'
INTRO = '''<section id="why-this-pack"><h2>Dry runs for learning a craft</h2>
<p>This pack grew from repeated requests by apprentices during Benjamin P Taylor's teaching with <a href="https://www.systemspractice.org/">SCiO</a> on the level 7 Systems Thinking Practitioner apprenticeship. They wanted simple exercises, worked examples and answers so they could try out methods and check their understanding.</p>
<p>Systems practice is learned through application in the real world. Teaching, workshop exercises, worked examples and support with live situations all contribute to apprenticing in a craft. A dry run can help develop technical skills and reveal a misunderstanding before using a method with people. It cannot reproduce the purposes, relationships, uncertainty and consequences of that work.</p>
<p>Use the exercises as preparation for practice and as a way to revisit a technical point. Getting a model or answer right is useful, but it is not the purpose of systems practice or the practice itself.</p>
</section>'''


def main():
    # Run after the legacy feedback helper so future builds cannot restore its
    # long playback control over the author's current instruction.
    motion = (ROOT / 'sources/living-mark-motion.js').read_text()
    (DOCS / 'assets/reader-motion.js').write_text(motion)
    selector = DOCS / 'assets/iteration-19.js'
    script = selector.read_text().replace("video.preload = 'metadata';", "video.preload = 'auto';")
    script = script.replace("playback.catch(() => showPoster(mark))", "playback.catch(() => { /* Keep the poster-backed video available for ordinary user activation. */ })")
    selector.write_text(script)
    css = '<style id="compact-mark-control">.living-mark-toggle{flex:0 0 32px;display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;min-width:32px;max-width:32px;min-height:32px;margin:0 4px;padding:6px;border:0;background:transparent;color:inherit;cursor:pointer;border-radius:4px}.living-mark-toggle svg{width:16px;height:16px;fill:currentColor}.living-mark-toggle[hidden]{display:none!important}.living-mark-toggle:focus-visible{outline:3px solid #ffbf47;outline-offset:2px}</style>'
    index = DOCS / 'index.html'
    text = index.read_text()
    text = re.sub(r'<style>\.living-mark-playback\{.*?</style>', '', text, flags=re.S)
    text = re.sub(r'<style id="compact-mark-control">.*?</style>', '', text, flags=re.S)
    text = text.replace('</head>', css + '</head>')
    text = re.sub(r'(assets/(?:reader-motion|iteration-19)\.js)\?v=[^"\s]+', r'\1?v=20260907-autoplay', text)
    index.write_text(text)

    for path in PACK.rglob('*.html'):
        text = path.read_text()
        banner = '<aside class="alpha-notice" aria-label="Alpha version"><p>' + NOTICE + '</p></aside>'
        text = re.sub(r'<aside class="alpha-notice".*?</aside>', '', text, flags=re.S)
        text = text.replace('<main id="main">', '<main id="main">' + banner, 1)
        if path == PACK / 'index.html':
            text = text.replace('<h1>Systems methods practice</h1>', '<h1>' + TITLE + '</h1>')
            text = text.replace('<p class="lead">Work through a fictional case, then compare your model and reasoning with a worked answer.</p>', '<p class="lead">Free exercises, worked examples and answers for technical dry runs of systems methods.</p><p class="meta">Benjamin P Taylor | 2026 | Alpha version</p>')
            text = re.sub(r'<section id="why-this-pack">.*?</section>', '', text, flags=re.S)
            text = text.replace('<section><h2>Use the external exercises', INTRO + '<section><h2>Use the external exercises', 1)
            text = text.replace('<title>Systems methods practice |', '<title>' + TITLE + ' (alpha) |')
            text = text.replace('content="Original systems-method cases, modelling checks, worked comparisons and source-labelled free and paid resources."', 'content="Alpha practice pack by Benjamin P Taylor (2026): 26 free systems-method dry runs with worked examples and answers, supporting rather than replacing real-world practice."')
            citation = '<section id="citation"><h2>Reference this resource</h2><p>' + CITATION + '</p><p><a href="https://transduction.systems/systems-thinking/practice/">Canonical online edition</a>. Original exercises were prepared with AI assistance. Technical and website tests do not amount to independent review of the teaching material.</p></section>'
            if 'id="citation"' not in text: text = text.replace('</main>', citation + '</main>', 1)
        elif path.parent.name == 'tutor-notes':
            if 'id="why-this-pack"' not in text: text = text.replace('<section>', INTRO + '<section>', 1)
        text = text.replace('This is low-stakes rehearsal, not an end-point assessment', 'These technical dry runs support learning a craft. They are not an end-point assessment')
        path.write_text(text)
    css_path = PACK / 'assets/practice.css'
    styling = '.alpha-notice{border:1px solid var(--accent);border-left:4px solid var(--accent);border-radius:4px;padding:10px 16px;margin:0 0 24px;background:var(--card)}.alpha-notice p{font-size:.94rem;margin:0;max-width:85ch}@media print{.alpha-notice{break-inside:avoid;border-color:#555}}'
    text = css_path.read_text()
    if '.alpha-notice{' not in text: css_path.write_text(text + '\n' + styling + '\n')
    for path in [PACK/'assets/pack.json', PACK/'assets/coverage.json']:
        data = json.loads(path.read_text())
        data.update(publication_status='alpha', author='Benjamin P Taylor', citation=CITATION, pedagogical_review='Independent specialist review not recorded')
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    # Keep atlas search wording and resource metadata in step with the actual page.
    data = json.loads((ROOT/'data/public-data.json').read_text())
    hub = 'practice_systems_methods_pack'
    desc = 'An alpha collection of 26 free technical dry runs by Benjamin P Taylor (2026), developed in response to apprentice requests during teaching with SCiO. Fictional cases, worked examples and answers support technical learning without replacing real-world systems practice. Independent specialist pedagogical review is not recorded.'
    for node in data['nodes']:
        if node['id'] == hub:
            node['label'] = TITLE + ' (alpha)'
            node['description'] = node['canonical_definition'] = desc
    for profile in data['profiles']:
        if profile['node_id'] == hub:
            profile.update(title=TITLE+' (alpha)', summary=desc, canonical_definition=desc)
    data['practice_pack'].update(publication_status='alpha', author='Benjamin P Taylor', citation=CITATION)
    for source in data['sources']:
        if source['id'] == 'src_systems_methods_practice_pack':
            source.update(title=TITLE+' (alpha)', creators=json.dumps(['Benjamin P Taylor']), notes=NOTICE)
    data['ai_observations']['metrics'] = graph_metrics(data)
    write(data)
    subprocess.run([sys.executable, str(ROOT/'scripts/build_public_knowledge.py')], check=True)
    for path in [DOCS/'index.html',DOCS/'systems-thinking/index.html',DOCS/'reading-list.html',DOCS/'core-practice.html',DOCS/'resources/index.html']:
        if not path.exists(): continue
        text=path.read_text()
        text=text.replace('<h2>Practise a systems method</h2>', '<h2>Systems methods practice: alpha version</h2>')
        text=text.replace('Choose a fictional case, build a model, compare it with worked reasoning and try a changed case.', 'Technical dry runs with fictional cases, worked examples and answers. Developed by Benjamin P Taylor to support learning a craft, not replace real-world systems practice.')
        path.write_text(text)
    assert 'Play mark' not in motion and 'Pause mark' not in motion
    assert len(list(PACK.rglob('index.html'))) == 32
    assert all('class="alpha-notice"' in p.read_text() for p in PACK.rglob('index.html'))
    print('Applied author framing, visible alpha status on 32 pages, and compact-control muted autoplay.')

if __name__ == '__main__':
    main()
