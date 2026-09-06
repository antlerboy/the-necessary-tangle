"""Apply page-wide feedback coverage after all public route generators."""
from pathlib import Path
import re
root = Path(__file__).resolve().parents[1] / 'docs'
css = '#openUpdates,.update-thread-dot{position:fixed!important;right:0!important;bottom:0!important;width:44px!important;height:44px!important;border:0!important;background:transparent!important;border-radius:0!important;z-index:99999;opacity:1!important;box-shadow:none!important}#openUpdates::after,.update-thread-dot::after{content:"";position:absolute;right:8px;bottom:8px;width:5px;height:5px;border-radius:50%;background:#862719;box-shadow:0 0 0 1px #fff}#openUpdates:focus-visible,.update-thread-dot:focus-visible{outline:3px solid #ffbf47!important;outline-offset:-3px}'
anchor = '<a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates" title="Website updates"></a>'
count = 0
for page in root.rglob('*.html'):
    text = page.read_text()
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
