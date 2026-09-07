#!/usr/bin/env python3
"""Fail closed on missing cases, broken local routes, false coverage or bad model arithmetic."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from zipfile import ZipFile
import json
import hashlib
from collections import Counter
from build_practice_pack import load_content,DEST,ROOT,URL
from refresh_graph_snapshot import calculate
from apply_relational_depth_16 import calculate_relational_depth
from apply_iteration_09 import graph_metrics

class Page(HTMLParser):
    def __init__(self,path=None,text=None):
        super().__init__(convert_charrefs=True);self.ids=[];self.links=[];self.headings=[];self.tags=[]
        self.feed(text if text is not None else path.read_text())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);self.tags.append((tag,a))
        if 'id' in a:self.ids.append(a['id'])
        if tag in ['a','link','script']:self.links.append(a.get('href') or a.get('src') or '')
        if tag in ['h1','h2','h3','h4','h5','h6']:self.headings.append(int(tag[1]))

labs,resources,standard=load_content()
assert len(labs)==26 and len({x['id'] for x in labs})==26
assert len(standard['core_order'])==13 and len(standard['theory_order'])==3
assert set(standard['core_order']+standard['theory_order']) <= {x['id'] for x in labs}
assert len(standard['ksb'])==25 and set(standard['duties'])==set(map(str,range(1,13)))
counts=Counter(x['section'] for x in labs)
assert counts=={'Foundations':3,'Core methods':13,'Systemic intervention':10}
allcodes=set()
for lab in labs:
    assert len(lab['scenario'].split())>=45,lab['id']
    assert len(lab['rounds'])>=3 and len(lab['checks'])>=2
    assert lab['repair']['broken'] and lab['repair']['fix'] and lab['retry']['answer']
    assert len(lab['criteria'])>=3 and lab['scope']
    assert set(lab['resources']+lab['paid']) <= set(resources),lab['id']
    assert lab['paid'],lab['id']
    assert set(lab['ksb'])<=set(standard['ksb']);allcodes.update(lab['ksb'])
    for q in lab['checks']:
        assert 0<=q['correct']<len(q['options']) and len(set(q['options']))==len(q['options'])
        # A concise explanation can be complete. Detect empty/placeholder feedback,
        # not an arbitrary minimum number of words that encourages padded prose.
        assert len(q['explanation'].strip())>=40,(lab['id'],q['q'],'missing explanation')
    for step in lab['rounds']:
        assert step['output'] and len(step['answer'].strip())>=100,(lab['id'],step['task'])
assert allcodes==set(standard['ksb']),set(standard['ksb'])-allcodes
for resource in resources.values():
    assert resource['url'].startswith('https://') and resource['check'] and resource['use'] and resource['cost']
assert '404' in resources['ackoff-guide']['check']
assert 'Flash' in resources['ou-diagramming']['check']
assert 'not' in resources['vsm-guide']['check']

pages=sorted(DEST.rglob('*.html'));assert len(pages)==32,len(pages)
for p in pages:
    page=Page(p)
    assert len(page.ids)==len(set(page.ids)),p
    assert page.headings.count(1)==1,p
    assert all(b<=a+1 for a,b in zip(page.headings,page.headings[1:])),(p,page.headings)
    assert 'main' in page.ids and 'openUpdates' in page.ids,p
    assert any(tag=='a' and a.get('href')=='#main' for tag,a in page.tags)
    for url in page.links:
        u=urlsplit(url)
        if u.scheme or u.netloc:continue
        target=(ROOT/'docs'/u.path.lstrip('/')) if u.path.startswith('/') else p.parent/unquote(u.path)
        if not u.path:target=p
        if target.is_dir():target/= 'index.html'
        assert target.is_file(),(p,url)
        if u.fragment and target.suffix=='.html':assert u.fragment in Page(target).ids,(p,url)
    if p.parent.name in {x['id'] for x in labs}:
        assert any('data-check' in a for _,a in page.tags),p
        assert all(i in page.ids for i in ['case','work','checks','repair','retry','review','sources'])
works=(DEST/'worksheets/index.html').read_text();answers=(DEST/'answers/index.html').read_text()
import html
for lab in labs:
    assert html.escape(lab['rounds'][0]['answer'],quote=True) not in works
    assert html.escape(lab['rounds'][0]['answer'],quote=True) in answers

archive=DEST/'downloads/systems-methods-practice.zip'
with ZipFile(archive) as z:
    assert z.testzip() is None
    names=set(z.namelist());assert 'index.html' in names and 'START-HERE.txt' in names
    assert not any(n.endswith('.zip') for n in names)
    for name in names:
        if not name.endswith('.html'):continue
        pg=Page(text=z.read(name).decode())
        import posixpath
        for url in pg.links:
            u=urlsplit(url)
            if u.scheme or u.netloc or not u.path:continue
            target=posixpath.normpath(posixpath.join(posixpath.dirname(name),u.path))
            assert target in names,(name,url,target)

data=json.loads((ROOT/'data/public-data.json').read_text())
assert data==json.loads((ROOT/'docs/assets/public-data.json').read_text())
assert data['meta']['release']=='0.23-systems-methods-practice-alpha'
assert data['practice_pack']['lab_count']==26
assert data['graph_snapshot']==calculate(data)
assert data['relational_depth']['aggregate']==calculate_relational_depth(data)['aggregate']
assert data['ai_observations']['metrics']==graph_metrics(data)
assert data['meta']['public_entry_count']==746
assert sum(n['id'].startswith('practice_lab_') for n in data['nodes'])==26
assert any(n['id']=='practice_systems_methods_pack' for n in data['nodes'])
for edge in data['edges']:
    if edge['id'].startswith('practice_edge_'):
        assert edge['relation_type'] in ['provides_practice_for','includes_practice_resource']
        assert not edge['reviewed_by'] and not edge['reviewed_at']
        assert edge['scope_conditions'] and edge['source_ids']
for p in ['index.html','systems-thinking/index.html']:
    assert '/systems-thinking/practice/' in (ROOT/'docs'/p).read_text(),p
assert 'practice-context.js' in (ROOT/'docs/index.html').read_text()
for published,reviewed in {'assets/systemic-evolution-map.js':'site/assets/systemic-evolution-map.js','assets/prior-maps.css':'site/assets/prior-maps.css','assets/systemic-evolution-review-manifest.json':'review-manifest.json','assets/systemic-evolution-publication-approval.json':'PUBLICATION_APPROVAL.json'}.items():
    assert (ROOT/'docs'/published).read_bytes()==(ROOT/'sources/systemic-evolution/review-1'/reviewed).read_bytes()
report={'status':'passed','lab_pages':26,'html_pages':len(pages),'core_approaches':13,'theory_rows':3,'supporting_areas':10,'resource_routes':len(resources),'questions':sum(len(x['checks']) for x in labs),'worked_steps':sum(len(x['rounds']) for x in labs),'local_links':'all checked','offline_archive_bytes':archive.stat().st_size,'offline_archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'specialist_pedagogical_review':'not recorded'}
(ROOT/'validation').mkdir(exist_ok=True)
(ROOT/'validation/practice-structure.json').write_text(json.dumps(report,indent=2)+'\n')
print('PRACTICE_STRUCTURE',json.dumps(report))
