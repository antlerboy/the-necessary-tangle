"""Add a source-scoped reading guide without altering the evidence graph."""
from pathlib import Path
from html import escape
import json
import re
import xml.etree.ElementTree as ET
from build_readable_atlas import page

R = Path(__file__).resolve().parents[1]
D = R / 'docs'
r = json.loads((R / 'sources/complexity-in-eight-days/source.json').read_text())
data = json.loads((R / 'data/public-data.json').read_text())
nodes = {n['id'] for n in data['nodes']}
assert all(c['target'] in nodes for c in r['connections'])
e = lambda s: escape(s, quote=True)
body = '''<p class="lead">Fred Amonya’s lecture notes introduce complexity science through the question of when a description works, and when it needs to change.</p>
<p><a href="''' + e(r['url']) + '''">Source record on ResearchGate</a> · <a href="''' + e(r['pdf_url']) + '''">Read the author’s PDF</a> · Fred Amonya · <em>Master Lecture Notes: Introduction to Complexity Science</em></p>
<p>The inspected copy presents an eight-day intensive for advanced postgraduate and MRes readers. It describes an open course without institutional affiliation. ResearchGate reports publication and an author upload on 3 November 2026; its public record was checked on 9 November 2026. The inspected 33-page copy has matching date metadata. Its byte identity with the linked original PDF has not been verified. The author’s rights and terms apply.</p>
<section><h2>What the notes do</h2><p>The notes distinguish a change in a system’s state, a change in its dynamics, and a change in the effective description used to study it (pp. 1–2). They move from spaces, observables and dynamics through coarse-graining, hierarchy and renormalisation, emergence and non-equilibrium, information and prediction, adaptive systems, inadequate descriptions, and revising spaces. Applications include biological, financial and institutional systems.</p>
<p>Choosing a state space, observables, admissible interventions and evolution rules involves modelling judgement (pp. 3–4, §1.1). A coarse-grained description is closed under the stated condition π ∘ F = G ∘ π. Failure of that condition concerns the chosen projection; it does not establish that every microscopic description fails (p. 8, §§2.2–2.3). Whether a model is sufficient depends on its target, horizon and conditions (p. 15, §§4.2–4.3).</p>
<p>The notes distinguish predictive information loss, memory, computational limits and causal inadequacy, rather than treating ‘reductionism fails’ as a general theorem (p. 19, §6.1). Adaptive simulations can explore models, but are not empirical proof (pp. 17–19). Infrastructure interacts with other systems, and whose opportunities count is a question for analysis (p. 28, §8.4). The account of complexity depends partly on the question asked; interaction, feedback, collective organisation and adaptation can make component-wise reasoning insufficient (p. 29, §8.5).</p></section>
<section><h2>Questions for reading</h2><p>These are editorial prompts for comparison. They are not claims that the author draws the same conclusions as the linked traditions.</p><ul>
<li>For a particular prediction or intervention, which observables and time horizon make the model sufficient? What would show that the chosen projection has lost something needed?</li>
<li>Who chooses the description, and what changes when the purpose or the people whose opportunities count are different?</li>
<li>How does the account of emergence through coarse-graining compare with other uses of emergence? Which claim is mathematical, and which depends on empirical evidence?</li></ul>
<p>The notes acknowledge modelling choices, purposes and whose opportunities count; they do not offer a sustained critique of boundary judgements. They do not define ‘system’ generally or survey systems thinking and cybernetics as traditions of inquiry.</p></section>
<section><h2>A comparison with Ashby</h2><p>In <a href="https://ashby.info/Ashby-Introduction-to-Cybernetics.pdf">An Introduction to Cybernetics</a>, Ashby examines when grouping states retains determinate transitions (§6/13, pp. 103–105), and distinguishes a system considered as a thing from the observer’s selected variables (§6/14, pp. 106–107). Comparing these passages with Amonya’s closure condition (p. 8, §§2.2–2.3) can clarify what each description preserves and who selects it. This is an editorial comparison, not a claim of influence or priority.</p></section>
<section><h2>Explore the atlas</h2><p>These are editorial reading routes, not evidence of influence or agreement.</p><ul>'''
for c in r['connections']:
    body += '<li><a href="/#view=item&amp;id=' + e(c['target']) + '">' + e(c['label']) + '</a> — ' + e(c['phrase']) + ' (' + e(c['locator']) + '). ' + e(c['scope']) + '</li>'
body += '</ul></section>'
folder = D / 'reading/complexity-in-eight-days'
folder.mkdir(parents=True, exist_ok=True)
(folder / 'index.html').write_text(page('Complexity in Eight Days', r['summary'], '/reading/complexity-in-eight-days/', body, data['meta']['release']), encoding='utf-8')
p = D / 'library/catalogue.json'
cat = json.loads(p.read_text())
cat['records'] = [x for x in cat['records'] if x['id'] != r['id']]
cat['records'].append({**{k: r[k] for k in ('id','title','url','pdf_url','publication_date','metadata_verified_on','authors','summary','locator','connections')}, 'collection':'Complexity readings', 'format':'Lecture notes', 'year':'2026', 'review':'Source-scoped reading; ResearchGate metadata verified 9 November 2026; hosted PDF version not compared', 'atlas_id':''})
cat['counts']['source_register_records'] = len(cat['records'])
p.write_text(json.dumps(cat, ensure_ascii=False, separators=(',', ':')) + '\n')
p = D / 'library/index.html'
t = p.read_text()
start, end = '<!-- complexity-eight-days -->', '<!-- /complexity-eight-days -->'
block = start + '<section class="resource-pathways"><h2><a href="/reading/complexity-in-eight-days/">Complexity in Eight Days</a></h2><p>Read Fred Amonya’s lecture notes on complexity and the adequacy of descriptions.</p></section>' + end
if start in t:
    t = re.sub(re.escape(start) + '.*?' + re.escape(end), lambda _: block, t, flags=re.S)
else:
    t = t.replace('</main>', block + '</main>', 1)
p.write_text(t)
p = D / 'sitemap.xml'
url = 'https://transduction.systems/reading/complexity-in-eight-days/'
namespace = 'http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('', namespace)
tree = ET.parse(p)
root = tree.getroot()
if not any(item.findtext('{' + namespace + '}loc') == url for item in root):
    item = ET.Element('{' + namespace + '}url')
    ET.SubElement(item, '{' + namespace + '}loc').text = url
    generated_prefixes = tuple('https://transduction.systems/' + part for part in ('entries/', 'journeys/', 'stewardship/'))
    insertion = next((i for i, row in enumerate(root) if (row.findtext('{' + namespace + '}loc') or '').startswith(generated_prefixes)), len(root))
    root.insert(insertion, item)
ET.indent(tree, space='  ')
tree.write(p, encoding='utf-8', xml_declaration=True)
p = R / 'documentation/NEXT_WORK.md'
t = p.read_text(encoding='utf-8')
start, end = '<!-- complexity-eight-days-source -->', '<!-- /complexity-eight-days-source -->'
note = start + '''
## Source addition: Complexity in Eight Days, 9 November 2026

Benjamin P Taylor authorised the ResearchGate source and supplied PDF to be added to the site. The bounded source packet is `sources/complexity-in-eight-days/PACKET.md`. The maintained reading guide is `/reading/complexity-in-eight-days/`, with one searchable source record, page locators, and clearly labelled editorial comparisons. The public ResearchGate record was checked on 9 November 2026 and reports publication and an author upload on 3 November 2026. The original PDF is linked at the author's host; its byte identity with the inspected supplied copy remains unverified. The PDF is not redistributed. No atlas nodes, edges, profiles, or graph release number change. Validation and publication results are identified by the current Publish workflow and deployment.json; source inclusion does not assert independent scholarly endorsement.
''' + end
if start in t:
    t = re.sub(re.escape(start) + '.*?' + re.escape(end), lambda _: note, t, flags=re.S)
else:
    t = t.rstrip() + '\n\n' + note + '\n'
p.write_text(t, encoding='utf-8')
print('Complexity in Eight Days: source register and reading guide built; graph unchanged.')
