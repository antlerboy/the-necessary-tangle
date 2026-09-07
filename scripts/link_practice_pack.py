#!/usr/bin/env python3
"""Link the pack from maintained entry points; leave source-owner packages intact."""
import html
import json
import re
import shutil
from pathlib import Path
from build_practice_pack import URL,DATE,DEST,load_content,page
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
callout='''<section id="systemsPracticeCallout" class="resource-pathways"><h2>Practise a systems method</h2><p>Choose a fictional case, build a model, compare it with worked reasoning and try a changed case. All 13 core SCiO approaches and three theory rows have a free practice route, with explicit limits.</p><p><a class="button" href="/systems-thinking/practice/">Open the systems methods practice pack</a> · <a href="/systems-thinking/practice/coverage/">Inspect standards coverage</a></p></section>'''
index=DOCS/'index.html';text=index.read_text()
if 'id="systemsPracticeCallout"' not in text:
    marker='<section class="resource-pathways"'
    if marker in text:text=text.replace(marker,callout+'\n'+marker,1)
    else:text=text.replace('</main>',callout+'</main>',1)
# Add a true page link, not a hash route, to the existing main navigation.
if 'data-practice-nav' not in text:
    text=re.sub(r'(<nav\b[^>]*>)',r'\1<a data-practice-nav href="/systems-thinking/practice/">Practice</a>',text,count=1)
text=re.sub(r'<span id="releaseBadge">.*?</span>','<span id="releaseBadge">Release 0.23</span>',text)
for asset in ['public-data.js','practice-links.js','practice-context.js']:
    if asset in text:text=re.sub(r'(assets/'+re.escape(asset)+r')(?:\?v=[^"\s]+)?',r'\1?v=20260907-practice',text)
    else:text=text.replace('</body>','<script defer src="assets/'+asset+'?v=20260907-practice"></script></body>')
index.write_text(text)
shutil.copyfile(ROOT/'sources/practice-pack/practice-context.js',DOCS/'assets/practice-context.js')
# These are maintained local reading surfaces, not locked third-party maps.
for relative in ['systems-thinking/index.html','reading-list.html','core-practice.html','resources/index.html']:
    p=DOCS/relative
    if not p.exists():continue
    t=p.read_text()
    if 'id="systemsPracticeCallout"' not in t:
        if '</main>' in t:t=t.replace('</main>',callout+'</main>',1)
        else:t=t.replace('</body>',callout+'</body>',1)
    p.write_text(t)
# Correct the footer route to the actual single-page contribution interface.
for p in DEST.rglob('*.html'):
    t=p.read_text().replace('https://transduction.systems/submissions/','https://transduction.systems/#view=contribute')
    p.write_text(t)
# Readable release note: generated state is built and tested by CI, not asserted reviewed.
body='''<h1>Systems methods practice: release 0.23</h1><p>26 free original practice pages now sit under the systems-thinking introduction. Each has a fictional scenario, explicit outputs, worked comparisons, checks, a defective claim or model to repair, and a second case.</p><p><a href="/systems-thinking/practice/">Open the practice pack</a> · <a href="/systems-thinking/practice/coverage/">Inspect the coverage and its limits</a> · <a href="/systems-thinking/practice/resources/">Read the source register</a></p><h2>What changed</h2><p>All thirteen approaches and three theory rows from the public SCiO portfolio have an introductory rehearsal. Ten further pages support systemic inquiry, intervention, learning, conversations and evaluation. Free and paid external routes are distinguished from original exercises. The Open University map exercises and MIT problem/solution pairs are linked directly.</p><p>Practice resources are searchable in the atlas and connected to existing method entries where their identities could be matched. The gateway, atlas home, main navigation and reading-list page link to the pack. Model-specific links appear in relevant atlas item views.</p><h2>What the checks establish</h2><p>The release gate checks the site, standards inventory, source references, worked arithmetic, graph integrity and interactive behaviour. It preserves the previous release's tests and protected source-owner assets. Browser test results are recorded in the GitHub workflow for the deployed commit.</p><p>Those tests do not constitute independent specialist review of every pedagogical judgement. The pages state where they rehearse only part of a fuller methodology and where real organisational application is still needed. They are not accreditation or provider endorsement.</p><p><a href="https://github.com/antlerboy/the-necessary-tangle/actions/workflows/pages.yml">Inspect publication and test runs</a> · <a href="/deployment.json">Inspect the deployed commit</a></p>'''
# Use the site's established accessible learning-page shell for a non-pack route.
from apply_release_22 import shell
p=DOCS/'updates/0.23/index.html';p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(shell('Systems methods practice, release 0.23','Original systems-method cases, explicit checks and standards coverage.',body,'updates/0.23/').replace('5 September 2026','7 September 2026'))
sitemap=DOCS/'sitemap.xml';text=sitemap.read_text()
for p in [*DEST.rglob('index.html'),DOCS/'updates/0.23/index.html']:
    route=p.relative_to(DOCS).as_posix().removesuffix('index.html')
    url='https://transduction.systems/'+route
    if '<loc>'+url+'</loc>' not in text:text=text.replace('</urlset>','  <url><loc>'+html.escape(url)+'</loc><lastmod>'+DATE+'</lastmod></url>\n</urlset>')
sitemap.write_text(text)
print('Linked practice pages from the gateway, atlas navigation/home, reading routes and matched method views.')
