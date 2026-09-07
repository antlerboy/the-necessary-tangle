#!/usr/bin/env python3
"""Create a deterministic offline pack, with relative assets and no self-inclusion."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED,ZipInfo
import re
from build_practice_pack import DEST,ROOT,load_content
assets=DEST/'assets'
# Page-wide feedback/punctuation additions use a root asset online. Make a local copy
# for the downloadable package so its ordinary learning pages also work offline.
punctuation=ROOT/'docs/assets/reader-punctuation.js'
if punctuation.exists():
    (assets/'reader-punctuation.js').write_bytes(punctuation.read_bytes())
for p in DEST.rglob('*.html'):
    relative='assets/' if p.parent==DEST else '../assets/'
    t=p.read_text().replace('/assets/reader-punctuation.js?v=20260906',relative+'reader-punctuation.js?v=20260906')
    p.write_text(t)
downloads=DEST/'downloads';downloads.mkdir(exist_ok=True)
archive=downloads/'systems-methods-practice.zip'
files=[p for p in sorted(DEST.rglob('*')) if p.is_file() and downloads not in p.parents]
with ZipFile(archive,'w',compression=ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:
        name=p.relative_to(DEST).as_posix()
        content=p.read_bytes()
        if p.suffix=='.html':
            text=content.decode().replace('downloads/systems-methods-practice.zip','https://transduction.systems/systems-thinking/practice/downloads/systems-methods-practice.zip')
            text=text.replace('../https://','https://').replace('./https://','https://')
            content=text.encode()
        info=ZipInfo(name,date_time=(2026,9,7,0,0,0));info.compress_type=ZIP_DEFLATED
        z.writestr(info,content)
    info=ZipInfo('START-HERE.txt',date_time=(2026,9,7,0,0,0));info.compress_type=ZIP_DEFLATED
    z.writestr(info,'Open index.html in a browser. Cases and answers work offline. External sources and atlas links need internet access. The notes tool does not transmit answers; browser storage may be restricted for local files, so use Export to keep a copy. Original material CC BY-SA 4.0. This is practice, not accreditation.\n')
print('Packaged',len(files),'files;',archive.stat().st_size,'bytes.')
