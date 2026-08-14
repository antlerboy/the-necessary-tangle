#!/usr/bin/env python3
"""Patch public site for release 0.15."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import quote
from apply_iteration_15 import make_observations, write_ai_document

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'docs'/'index.html'
CSS=ROOT/'docs'/'assets'/'styles.css'
DATA=ROOT/'data'/'public-data.json'
INVENTORY=ROOT/'data'/'reading-list-inventory.json'
READING_PAGE=ROOT/'docs'/'reading-list.html'
RELEASE='0.15-ing-reading-practice-alpha'


def clean(s:str)->str:
    return '\n'.join(x.rstrip() for x in s.rstrip().splitlines())+'\n'



def refresh_ai_observations()->None:
    data=json.loads(DATA.read_text(encoding='utf-8'))
    inv=json.loads(INVENTORY.read_text(encoding='utf-8'))
    report=make_observations(data,inv)
    data['ai_observations']=report
    rendered=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    DATA.write_text(rendered,encoding='utf-8')
    (ROOT/'docs'/'assets'/'public-data.json').write_text(rendered,encoding='utf-8')
    (ROOT/'docs'/'assets'/'public-data.js').write_text('window.TANGLE_DATA = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    write_ai_document(report)

def patch_index()->None:
    text=INDEX.read_text(encoding='utf-8')
    # Remove release-0.14 prominence card; material remains searchable and in its guided route.
    text=re.sub(r'\n\s*<a class="start-small-card" href="#view=journeys&id=journey_snowden_cynefin_sources_and_practice&step=0">.*?</a>','',text,count=1,flags=re.S)
    # Remove any previous 0.15 cards, making repeat builds stable.
    for marker in ['person_david_ing','journey_david_ing_systems_in_plural','journey_core_systems_practice_reading','reading-list.html']:
        text=re.sub(r'\n\s*<a class="start-small-card"[^>]+(?:'+re.escape(marker)+r')[^>]*>.*?</a>','',text,flags=re.S)
    old_anchor='<a class="start-small-card" href="#view=map&layer=substantive&depth=profiles"><span class="eyebrow">A quieter map</span><strong>Developed entries and substantive lines</strong><span>Begin with the evidence-deepened core before opening the complete provenance graph.</span></a>'
    anchor='<a class="start-small-card" href="#view=map&layer=substantive&depth=1&focus=concept_viability"><span class="eyebrow">A readable neighbourhood</span><strong>Viability and its immediate connections</strong><span>Start with one question-sized piece of the graph; expand only when it helps.</span></a>'
    text=text.replace(old_anchor,anchor,1)
    cards='''<a class="start-small-card" href="#view=journeys&id=journey_david_ing_systems_in_plural&step=0"><span class="eyebrow">Service systems and lineages</span><strong>David Ing journey</strong><span>Follow service systems thinking, Systems Changes Learning, pattern language and unusually rich documentation of systems lineages.</span></a>
          <a class="start-small-card" href="#view=journeys&id=journey_core_systems_practice_reading&step=0"><span class="eyebrow">Professional systems practice</span><strong>Core systems practice</strong><span>Concepts and laws, CSH, SSM, System Dynamics, VSM, multi-methodology, intervention and reflexive learning.</span></a>
          <a class="start-small-card" href="reading-list.html"><span class="eyebrow">Reading and coverage</span><strong>Reading-list depth map</strong><span>Every captured reading-list item with its current status: developed profile, represented, or inventory-only.</span></a>'''
    if anchor not in text: raise RuntimeError('map start card not found')
    text=text.replace(anchor,anchor+'\n          '+cards,1)
    # Add reading/core documentation routes.
    docs_marker='<a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/canonical-source-register.md" target="_blank" rel="noopener">Canonical source roles</a>'
    addition=docs_marker+'<a class="button" href="reading-list.html">Reading-list depth</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/core-systems-practice.md" target="_blank" rel="noopener">Core systems practice</a>'
    text=text.replace(addition,docs_marker)
    if docs_marker in text: text=text.replace(docs_marker,addition,1)
    # Update stylesheet cache key and release metadata without changing theme behaviour.
    text=re.sub(r'assets/styles\.css(?:\?v=[^"\']+)?', 'assets/styles.css?v=0.15-mapfix', text, count=1)
    INDEX.write_text(clean(text),encoding='utf-8')


def render_reading_page()->None:
    inv=json.loads(INVENTORY.read_text(encoding='utf-8'))
    rows=[]
    for item in inv['items']:
        status=item['coverage_status']; label={'developed_profile':'Developed profile','represented':'Represented','inventory_only':'Inventory only'}[status]
        display=html.escape(item['display'])
        if item['node_id']:
            href='index.html#view=item&id='+quote(item['node_id'])+'&from=reading-list'
            display=f'<a href="{href}">{display}</a>'
        rows.append(f'<tr data-section="{html.escape(item["section"])}" data-status="{status}"><td>{html.escape(item["section"])}</td><td>{display}</td><td><span class="coverage-status {status}">{label}</span></td></tr>')
    c=inv['counts']
    page=f'''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="theme-color" content="#9f161b"><title>Reading-list depth — The Necessary Tangle</title><link rel="stylesheet" href="assets/styles.css?v=0.15"><style>.reading-shell{{max-width:1200px;margin:0 auto;padding:1.4rem 1.3rem 5rem}}.reading-head{{max-width:850px;padding:2rem 0 1rem}}.coverage-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.7rem;margin:1rem 0 1.5rem}}.coverage-grid div{{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:.8rem}}.coverage-grid strong{{display:block;font-size:1.45rem;color:var(--accent)}}.reading-controls{{display:flex;gap:.6rem;flex-wrap:wrap;margin:1rem 0}}.reading-controls button{{background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:.45rem .7rem;cursor:pointer}}.reading-controls button.active{{border-color:var(--accent);color:var(--accent)}}table{{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line)}}th,td{{text-align:left;vertical-align:top;padding:.68rem;border-bottom:1px solid var(--line)}}th{{font-family:Arial,sans-serif;font-size:.8rem;color:var(--muted)}}.coverage-status{{font:700 .72rem Arial,sans-serif;white-space:nowrap}}.developed_profile{{color:var(--green)}}.represented{{color:var(--blue)}}.inventory_only{{color:var(--muted)}}@media(max-width:760px){{.coverage-grid{{grid-template-columns:1fr 1fr}}th:first-child,td:first-child{{display:none}}}}</style></head><body>
<div class="reading-shell"><p><a href="index.html#view=home">← The Necessary Tangle</a></p><header class="reading-head"><p class="eyebrow">Reading and coverage</p><h1>A systems | complexity | cybernetics reading list</h1><p>This is an item-level depth map of the public reading list. Inclusion means ‘on the list’. It does not mean every work has been read, endorsed or critically developed in the atlas.</p></header>
<div class="coverage-grid"><div><strong>{inv['item_count']}</strong>captured items</div><div><strong>{c['developed_profile']}</strong>developed profiles</div><div><strong>{c['represented']}</strong>represented more thinly</div><div><strong>{c['inventory_only']}</strong>inventory-only</div></div>
<p>{html.escape(inv['coverage_note'])}</p><p><a href="index.html#view=journeys&id=journey_core_systems_practice_reading&step=0">Follow the core systems-practice reading route</a> · <a href="{html.escape(inv['source_url'])}" target="_blank" rel="noopener">Open the public source list</a></p>
<div class="reading-controls" aria-label="Coverage filters"><button class="active" data-filter="all">All</button><button data-filter="developed_profile">Developed</button><button data-filter="represented">Represented</button><button data-filter="inventory_only">Inventory-only</button></div>
<table><thead><tr><th>Section</th><th>Reading-list item</th><th>Atlas depth</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<script>document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('[data-filter]').forEach(x=>x.classList.remove('active'));b.classList.add('active');const f=b.dataset.filter;document.querySelectorAll('tbody tr').forEach(r=>r.hidden=f!=='all'&&r.dataset.status!==f);}}));</script></body></html>'''
    READING_PAGE.write_text(page,encoding='utf-8')


def patch_repository_prose()->None:
    data=json.loads(DATA.read_text(encoding='utf-8')); meta=data['meta']; inv=data['reading_list_inventory'];
    readme=ROOT/'README.md'; t=readme.read_text(encoding='utf-8')
    t=re.sub(r'This is a public alpha\. Release 0\.14 contains \d+ canonical public entries, including \d+ developed profiles, \d+ sources and \d+ guided journeys\.',f"This is a public alpha. Release 0.15 contains {meta['public_entry_count']} canonical public entries, including {meta['profile_count']} developed profiles, {meta['source_count']} sources and {meta['journey_count']} guided journeys.",t,count=1)
    line=f"The [reading-list depth map](https://transduction.systems/reading-list.html) exposes all {inv['item_count']} captured items and distinguishes developed profiles, thinner representation and inventory-only coverage."
    if line not in t: t=t.replace('\n## Start here\n','\n'+line+'\n\n## Start here\n',1)
    readme.write_text(clean(t),encoding='utf-8')
    cit=ROOT/'CITATION.cff'; t=cit.read_text(encoding='utf-8'); t=re.sub(r'^version:.*$',f'version: {RELEASE}',t,flags=re.M); t=re.sub(r'^date-released:.*$','date-released: 2026-08-14',t,flags=re.M); cit.write_text(clean(t),encoding='utf-8')
    ch=ROOT/'CHANGELOG.md'; t=ch.read_text(encoding='utf-8')
    if '## 0.15-ing-reading-practice-alpha' not in t:
        entry='''## 0.15-ing-reading-practice-alpha — 14 August 2026\n\n- Added a developed David Ing constellation covering service systems thinking, Systems Changes Learning, pattern language, public corpora and lineage documentation.\n- Turned the public systems | complexity | cybernetics reading list into an item-level coverage map with explicit maturity states.\n- Added developed reading-list routes through *Systems Thinkers*, *Steps to an Ecology of Mind*, *Understanding Understanding* and *Flawless Consulting*.\n- Added a core systems-practice spine connecting systems laws and concepts, CSH, SSM, System Dynamics, VSM, multi-methodology, intervention and reflexive learning.\n- Regenerated graph observations from the current graph and reading-list coverage.\n- Kept the reader-controlled light/dark switch and the discreet public updates route.\n\n'''
        t=t.replace('# Changelog\n\n','# Changelog\n\n'+entry,1)
    ch.write_text(clean(t),encoding='utf-8')


def main()->None:
    refresh_ai_observations(); patch_index(); render_reading_page(); patch_repository_prose(); print('Patched 0.15 site, reading-list page, AI observations and repository prose')
if __name__=='__main__': main()
