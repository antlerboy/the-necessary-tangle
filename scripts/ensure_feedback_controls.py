"""Apply page-wide feedback coverage after all public route generators."""
from pathlib import Path
import re
root = Path(__file__).resolve().parents[1] / 'docs'
css = '#openUpdates,.update-thread-dot{position:fixed!important;right:0!important;bottom:0!important;width:44px!important;height:44px!important;border:0!important;background:transparent!important;border-radius:0!important;z-index:99999;opacity:1!important;box-shadow:none!important}#openUpdates::after,.update-thread-dot::after{content:"";position:absolute;right:8px;bottom:8px;width:5px;height:5px;border-radius:50%;background:#862719;box-shadow:0 0 0 1px #fff}#openUpdates:focus-visible,.update-thread-dot:focus-visible{outline:3px solid #ffbf47!important;outline-offset:-3px}'
anchor = '<a id="openUpdates" href="/#view=contribute" aria-label="Open updates" title="Suggest a correction"></a>'
count = 0
for page in root.rglob('*.html'):
    text = page.read_text()
    text = re.sub(r'(<a\b[^>]*(?:id="openUpdates"|class="update-thread-dot")[^>]*href=")[^"]*', r'\1/#view=contribute', text)
    if not re.search(r'<a\b[^>]*aria-label=[\'"]Open updates[\'"]', text):
        text = text.replace('</body>', anchor + '</body>') if '</body>' in text else text + anchor
    if 'WEB_ESTATE_FEEDBACK_20260906' not in text:
        style = '<!-- WEB_ESTATE_FEEDBACK_20260906 --><style>' + css + '</style>'
        text = text.replace('</head>', style + '</head>') if '</head>' in text else style + text
    page.write_text(text)
    assert 'aria-label="Open updates"' in text, page
    count += 1
# Motion is the default requested presentation; reduced-motion readers keep posters.
script = root / 'assets/iteration-19.js'
text = script.read_text()
old = 'const candidates = usable.length > 1 ? usable.filter(mark => mark.id !== previous) : usable;'
new = 'const moving = reducedMotion ? [] : usable.filter(mark => mark.kind === "video");\n    const pool = moving.length ? moving : usable;\n    const candidates = pool.length > 1 ? pool.filter(mark => mark.id !== previous) : pool;'
if old in text:
    text = text.replace(old, new).replace('|| usable[0]', '|| pool[0]')
    script.write_text(text)
print(f'Checked feedback control on {count} public HTML pages; preserved reduced-motion mark fallback.')

# Give the changed selector a fresh asset URL so existing visitors receive it.
index = root / 'index.html'
text = index.read_text()
text = re.sub(r'assets/iteration-19\.js\?v=[^"\s]+', 'assets/iteration-19.js?v=20260906-motion', text)
index.write_text(text)

# Offer a route that does not require a GitHub account.
text=index.read_text()
text=text.replace('Your proposal opens as a GitHub issue for public discussion and editorial decision; it never changes the atlas silently.', 'Email a correction to the curator, or open a public GitHub issue.')
text=text.replace('The form prepares a public GitHub issue labelled <code>site-submission</code> and <code>awaiting-curator-review</code>. Research issues and pull requests are also valid routes. No proposal changes the atlas automatically.', 'Use the form to prepare an email to Benjamin P Taylor. You can also submit a public GitHub issue. Contributions are reviewed before they are incorporated.')
text=text.replace('GitHub will also record the submitting account','How you would like to be credited')
text=text.replace('This page sends nothing to the project. The button prepares a GitHub issue in a new tab; you review it before submitting. A GitHub account is required.', 'Email your correction opens a draft in your email app for you to review and send. You can also write directly to benjamin.taylor@redquadrant.com.')
text=text.replace('<button type="submit" class="primary">Prepare GitHub issue</button>', '<button type="button" id="emailCorrection" class="primary">Email your correction</button><button type="submit">Prepare a public GitHub issue</button>')
text=text.replace('<li>The proposal becomes a visible GitHub issue.</li>','<li>The curator reads your email or public issue.</li>')
if 'reader-feedback.js' not in text:text=text.replace('</body>','<script defer src="assets/reader-feedback.js?v=20260906"></script></body>')
index.write_text(text)
(root/'assets/reader-feedback.js').write_text("""(() => {
 const button=document.getElementById('emailCorrection'),form=document.getElementById('contributionForm');if(!button||!form)return;
 button.addEventListener('click',()=>{if(!form.reportValidity())return;const data=new FormData(form);const labels={submission_type:'Type',entry_label:'Entry',entry_id:'Entry identifier',statement:'Proposed change',reason:'Reason',source_url:'Public source',source_citation:'Citation',evidence:'Evidence',name:'Name'};const body=Array.from(data.entries()).filter(([,v])=>String(v).trim()).map(([k,v])=>(labels[k]||k)+': '+v).join('\\n\\n');const subject='The Necessary Tangle: '+data.get('submission_type');location.href='mailto:benjamin.taylor@redquadrant.com?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);document.getElementById('formStatus').textContent='Review and send the draft in your email app. If it does not open, email benjamin.taylor@redquadrant.com with your correction.';});
})();""")

# Let readers start playback when browser autoplay is paused, and pause motion explicitly.
motion = root / 'assets/reader-motion.js'
motion.write_text("""(() => {
 const host=document.querySelector('[data-living-mark]'); if(!host)return;
 const button=document.createElement('button');button.type='button';button.className='living-mark-playback';button.textContent='Play mark';
 const home=host.closest('a');(home||host).insertAdjacentElement('afterend',button);
 function sync(){const video=host.querySelector('video');button.textContent=video&&!video.paused?'Pause mark':'Play mark';button.setAttribute('aria-label',video&&!video.paused?'Pause living mark animation':'Play living mark animation');}
 function observe(){const v=host.querySelector('video');if(v){v.addEventListener('play',sync);v.addEventListener('pause',sync);}sync();}
 new MutationObserver(observe).observe(host,{childList:true});observe();
 button.addEventListener('click',async()=>{let video=host.querySelector('video');if(video&&!video.paused){video.pause();sync();return;}if(!video){try{const r=await fetch('assets/living-marks/manifest.json');const manifest=await r.json();const mark=manifest.marks.find(m=>m.id===host.dataset.markId&&m.kind==='video')||manifest.marks.find(m=>m.kind==='video');if(!mark)return;video=document.createElement('video');video.src=mark.src;video.poster=mark.poster||'';video.loop=true;video.muted=true;video.defaultMuted=true;video.playsInline=true;video.setAttribute('aria-hidden','true');host.replaceChildren(video);}catch{button.textContent='Animation unavailable';return;}}try{await video.play();}catch{button.textContent='Animation unavailable';}sync();});
})();""")
text=index.read_text()
if 'reader-motion.js' not in text:
 text=text.replace('</body>','<script defer src="assets/reader-motion.js?v=20260906-reader"></script></body>')
 text=text.replace('</head>','<style>.living-mark-playback{font:inherit;font-size:13px;color:inherit;background:transparent;border:1px solid currentColor;border-radius:4px;padding:5px 8px;cursor:pointer}.living-mark-playback:focus-visible{outline:3px solid #ffbf47;outline-offset:3px}</style></head>')
index.write_text(text)
# Normalise displayed punctuation at the final rendering layer; original sources stay intact.
for page in root.rglob('*.html'):
 text=page.read_text().replace(' — ','; ').replace(' – ','; ').replace('—',', ').replace('–','-').replace('&mdash;',', ').replace('&ndash;','-')
 page.write_text(text)

copy_script=root/'assets/reader-punctuation.js'
copy_script.write_text("""(() => {const normal=s=>s.replaceAll(' \u2014 ','; ').replaceAll(' \u2013 ','; ').replaceAll('\u2014',', ').replaceAll('\u2013','-');function clean(root){if(root.nodeType===3){if(!root.parentElement?.closest('script,style,textarea,input,code,pre')){const text=normal(root.nodeValue);if(text!==root.nodeValue)root.nodeValue=text;}return;}if(root.nodeType!==1)return;for(const child of root.childNodes)clean(child);}clean(document.body);new MutationObserver(records=>{for(const record of records){if(record.type==='characterData')clean(record.target);else for(const node of record.addedNodes)clean(node);}}).observe(document.body,{subtree:true,childList:true,characterData:true});})();""")
for page in root.rglob('*.html'):
 text=page.read_text()
 if 'reader-punctuation.js' not in text:text=text.replace('</body>','<script defer src="/assets/reader-punctuation.js?v=20260906"></script></body>')
 page.write_text(text)
