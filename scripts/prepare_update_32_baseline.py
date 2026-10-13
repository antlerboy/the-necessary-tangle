"""Restore the pre-0.32 reader entrance before historical release checks."""
from pathlib import Path
import re
R = Path(__file__).resolve().parents[1]
p = R / 'docs/index.html'
s = p.read_text()
before = (R / 'sources/update-2026-10-13/about-before.html').read_text()
s = re.sub(r'    <section id="view-about".*?(?=    <section id="view-ai-observations")', lambda _: before, s, flags=re.S)
s = s.replace('Release 0.32', 'Release 0.31')
p.write_text(s)
