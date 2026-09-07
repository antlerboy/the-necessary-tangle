#!/usr/bin/env python3
"""Verify the deployed, unlisted film and its downloadable narration."""
import hashlib,json,os,subprocess,time,urllib.request
from pathlib import Path

base='https://transduction.systems'
route='/encounters-with-the-other/'
commit=os.environ['DEPLOY_COMMIT']
out=Path('validation/encounters-live');out.mkdir(parents=True,exist_ok=True)
def get(path):
    request=urllib.request.Request(base+path+'?revision='+commit,headers={'User-Agent':'NecessaryTangle-publication-check/1.0','Cache-Control':'no-cache'})
    with urllib.request.urlopen(request,timeout=90) as response:
        assert response.status==200,(path,response.status)
        return response.read()

for attempt in range(8):
    deployed=json.loads(get('/deployment.json'))
    if deployed['commit']==commit:break
    if attempt==7:raise RuntimeError('Live deployment identity has not reached this revision')
    time.sleep(10)

report=json.loads(get(route+'verification.json'))
assert report['passed'] and report['audio']
for filename in ['index.html','transcript.html','production-notes.html']:
    data=get(route+filename);assert b'noindex' in data and b'@@' not in data
    (out/filename).write_bytes(data)
assert route.encode() not in get('/sitemap.xml')
assert route.encode() not in get('/index.html')
for filename in ['encounters-with-the-other.mp4','narration.mp3','captions.vtt','chapters.vtt','timeline.json']:
    data=get(route+filename);(out/filename).write_bytes(data)
film=out/'encounters-with-the-other.mp4'
assert hashlib.sha256(film.read_bytes()).hexdigest()==report['sha256']
media=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_streams','-show_format','-of','json',str(film)]))
assert {'video','audio'}<={s['codec_type'] for s in media['streams']}
assert abs(float(media['format']['duration'])-report['duration'])<.3
report.update(live_url=base+route,commit=commit,live_media_sha256_verified=True,unlisted=True)
(out/'live-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
