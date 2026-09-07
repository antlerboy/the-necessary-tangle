#!/usr/bin/env python3
"""Render the unlisted Oshry adaptation. Sources are sufficient to rebuild it.

Normal publication requires Piper audio; --preview creates stills only.
No browser, paid API, source PDF, or access token is used by this renderer.
"""
from __future__ import annotations
import argparse, array, hashlib, html, json, math, os, re, shutil, subprocess, wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'sources/encounters-with-the-other'
OUT=ROOT/'docs/encounters-with-the-other'
TMP=ROOT/'validation/encounters'
W,H,FPS=1280,720,12
BG='#172e3d'; CREAM='#f6f1e8'; RED='#e59279'; TEAL='#72d2c3'; GOLD='#e8c778'; FAINT='#45606d'
FONTS=Path('/usr/share/fonts/truetype/dejavu')
FONT={s:ImageFont.truetype(str(FONTS/'DejaVuSans.ttf'),s) for s in [20,22,25,28,34,36,40,48,58]}
TITLE=ImageFont.truetype(str(FONTS/'DejaVuSerif.ttf'),58)
DATA=json.loads((SRC/'scenes.json').read_text())

def run(args,**kw):
    return subprocess.run(args,check=True,**kw)

def wrapped(text,font,width):
    lines=[]
    for para in text.split('\n'):
        line=''
        for word in para.split():
            attempt=(line+' '+word).strip()
            if font.getlength(attempt)>width and line:lines.append(line);line=word
            else:line=attempt
        lines.append(line)
    return lines

def centre(d,xy,text,font,color=CREAM):
    d.text(xy,text,font=font,fill=color,anchor='mm')

def base_frame(s,i):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    d.line((56,92,1224,92),fill=FAINT,width=1)
    d.text((56,44),s['chapter'],font=FONT[22],fill=GOLD)
    d.text((1224,44),f'{i+1:02d} / {len(DATA["scenes"]):02d}',font=FONT[20],fill=CREAM,anchor='ra')
    titles=wrapped(s['title'],TITLE,680)
    for j,line in enumerate(titles):d.text((56,151+j*72),line,font=TITLE,fill=CREAM)
    y=max(333,166+len(titles)*72+45)
    font=FONT[34];lines=wrapped(s['text'],font,654)
    if y+len(lines)*47>633:font=FONT[28];lines=wrapped(s['text'],font,654)
    assert y+len(lines)*(font.size+13)<=636,(s['title'],len(lines),y)
    for j,line in enumerate(lines):d.text((56,y+j*(font.size+13)),line,font=font,fill=CREAM)
    d.text((56,670),'BARRY OSHRY  /  ENCOUNTERS WITH THE OTHER',font=FONT[20],fill='#b9c5c6')
    d.text((1224,670),'AUTHOR REVIEW',font=FONT[20],fill='#b9c5c6',anchor='ra')
    return im

def diagram(im,s,u,t):
    d=ImageDraw.Draw(im);kind=s['motif'];cx,cy=979,360
    p=min(1,u*3);p=p*p*(3-2*p)
    a=RED;b=TEAL
    def dot(x,y,r,col,outline=None):d.ellipse((x-r,y-r,x+r,y+r),fill=col,outline=outline,width=2)
    def cluster(x,y,color,phase=0,shape='circle',r=65):
        for k in range(8):
            ang=k*math.tau/8+phase
            xx=x+math.cos(ang)*r;yy=y+math.sin(ang)*r
            if shape=='square':d.rounded_rectangle((xx-8,yy-8,xx+8,yy+8),radius=2,fill=color)
            else:dot(xx,yy,8,color)
        dot(x,y,10,color)
    def pair(distance=113,connect=False,same=False):
        if connect:
            for j in [-42,0,42]:d.line((cx-distance,cy+j,cx+distance,cy+j),fill=FAINT,width=2)
            dot(cx-distance+2*distance*((t*.10)%1),cy,6,GOLD)
        cluster(cx-distance,cy,a,t*.045)
        cluster(cx+distance,cy,b,-t*.045,'circle' if same else 'square')
    def label(y,text,color=CREAM):centre(d,(cx,y),text,FONT[22],color)
    if kind in ['power-cycle','love-cycle']:
        color=a if kind=='power-cycle' else b
        words=('Separateness','Difference') if kind=='power-cycle' else ('Connectedness','Commonality')
        d.arc((cx-135,cy-135,cx+135,cy+135),15,165,fill=color,width=4)
        d.arc((cx-135,cy-135,cx+135,cy+135),195,345,fill=color,width=4)
        for offset in [0,math.pi]:
            angle=t*.7+offset;dot(cx+135*math.cos(angle),cy+135*math.sin(angle),7,GOLD)
        d.polygon([(cx-127,cy+38),(cx-143,cy+29),(cx-133,cy+15)],fill=color)
        d.polygon([(cx+127,cy-38),(cx+143,cy-29),(cx+133,cy-15)],fill=color)
        label(cy-166,words[0],color);label(cy+166,words[1],color)
        centre(d,(cx,cy),'reinforce',FONT[28]);centre(d,(cx,cy+37),'one another',FONT[22])
    elif kind=='whole':
        pair(108,True)
        label(177,'POWER + LOVE',GOLD)
        label(205,'Different and alike')
        label(510,'Separate and connected')
        d.arc((cx-192,cy-133,cx+192,cy+133),0,180,fill=b,width=2)
        d.arc((cx-192,cy-133,cx+192,cy+133),180,360,fill=a,width=2)
    elif kind=='memorial':
        for k in range(54):
            x=800+(k%9)*43;y=220+(k//9)*48
            strength=max(.18,1-max(0,p-k/60)*.9)
            col=tuple(int(v*strength) for v in (246,241,232));dot(x,y,5,col)
        label(561,'Lives, not abstractions',GOLD)
    elif kind in ['loose-tight','values','conflict']:
        pair(114)
        left,right=('Allow','Reject') if kind=='loose-tight' else ('Include','Preserve')
        centre(d,(cx-114,218),left,FONT[25],a);centre(d,(cx+114,218),right,FONT[25],b)
        if kind=='loose-tight':label(528,'Reflex responses')
        elif kind=='values':label(528,'Values-based responses')
        else:
            dot(cx+math.sin(t*.6)*100,cy+145,9,GOLD);label(560,'Conflict can be within us')
    elif kind in ['purity','collapse','threat','tolerance','power','blindness']:
        distance=110+26*p if kind!='tolerance' else 100
        pair(distance)
        barrier=cy-120
        d.line((cx,barrier,cx,cy+120),fill=GOLD,width=2 if kind=='tolerance' else 5)
        if kind in ['collapse','purity']:
            for j in range(5):d.line((cx+22+j*30,cy-110,cx+22+j*30,cy+110),fill=FAINT,width=2)
        labels={'purity':'Exclusion','collapse':'Commonality recedes','threat':'Unfamiliar becomes wrong','tolerance':'Conditional coexistence','power':'Difference + separateness','blindness':'The pattern is unseen'}
        label(541,labels[kind],a)
    elif kind in ['bridge','enterprise','love','sight','choice']:
        pair(135-25*p,True,kind=='love')
        labels={'bridge':'Ongoing, meaningful contact','enterprise':'A common enterprise','love':'Commonality + connection','sight':'See and change the pattern','choice':'Awareness makes choice possible'}
        label(535,labels[kind],b)
        if kind=='enterprise':
            d.rectangle((cx-35,cy-140,cx+35,cy-70),outline=GOLD,width=2)
            d.line((cx-110,cy-50,cx,cy-100,cx+110,cy-50),fill=GOLD,width=2)
    elif kind=='substitute':
        pair(123)
        for j,text in enumerate(['Fear','Projection','Rumour']):
            y=219+j*45;centre(d,(cx,y),text,FONT[22],GOLD)
        d.rectangle((cx-60,190,cx+64,330),outline=FAINT,width=1)
        label(535,'Stories fill the gap')
    elif kind=='law':
        pair(110)
        d.line((773,483,1185,483),fill=GOLD,width=5)
        label(536,'Protection and justice',GOLD)
        label(579,'How does seeing change?')
    elif kind=='assimilation':
        cluster(cx-110,cy,a,t*.035)
        for k in range(8):
            ang=k*math.tau/8-t*.035; x=cx+110+math.cos(ang)*65; y=cy+math.sin(ang)*65
            if k<int(8*p):dot(x,y,8,a)
            else:d.rectangle((x-8,y-8,x+8,y+8),fill=b)
        label(535,'Acceptance on whose terms?')
    elif kind=='lens':
        pair(110)
        for x,col in [(cx-110,a),(cx+110,b)]:
            radius=100-15*p;d.ellipse((x-radius,cy-radius,x+radius,cy+radius),outline=col,width=3)
        label(535,'We do not see our lens')
    elif kind=='learn':
        for j in range(3):
            cluster(cx,220+j*120,TEAL if j%2 else RED,t*.025,r=28+j*8)
        d.line((cx-90,200,cx-90,500),fill=GOLD,width=2)
        label(560,'Learned, then taken for granted')
    elif kind=='question':
        for r in [55,105,155]:d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=FAINT,width=1)
        centre(d,(cx,cy),'?',FONT[58],GOLD)
        dot(cx+155*math.cos(t*.25),cy+155*math.sin(t*.25),7,TEAL)
        label(561,'Anger becomes inquiry')
    else:
        pair(159-47*p)
        label(535,'Two cultures. One encounter.',GOLD)
    return im

def stamp(seconds):
    ms=round(seconds*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02d}:{m:02d}:{s:02d}.{ms:03d}'

def clock(seconds):return f'{int(seconds)//60}:{int(seconds)%60:02d}'

def prepare_audio(scenes,model):
    from piper import PiperVoice, SynthesisConfig
    voice=PiperVoice.load(str(model));config=SynthesisConfig(length_scale=1.10)
    pieces=[];sr=voice.config.sample_rate
    for i,s in enumerate(scenes):
        narration=s['title'].replace('\n',' ')+'. '+s['text'].replace('\n',' ')
        # Pronunciation aid affects the sound only; display and transcript retain the name.
        spoken=narration.replace('Oshry','Oshree')
        wavpath=TMP/f'scene-{i:02d}.wav'
        with wave.open(str(wavpath),'wb') as wav:voice.synthesize_wav(spoken,wav,syn_config=config)
        with wave.open(str(wavpath),'rb') as wav:
            assert wav.getnchannels()==1 and wav.getsampwidth()==2
            raw=wav.readframes(wav.getnframes());seconds=len(raw)/(sr*2)
        samples=array.array('h',raw)
        assert samples and sum(abs(v) for v in samples)/len(samples)>40,f'Silent narration: {i}'
        s['duration']=math.ceil((max(7,seconds+1.8))*FPS)/FPS
        s['narration']=narration;s['speech_duration']=seconds
        start=b'\0'*(round(.55*sr)*2)
        end=b'\0'*(round((s['duration']-.55-seconds)*sr)*2)
        pieces.append(start+raw+end)
        print(f'Narration {i+1}/{len(scenes)}: {seconds:.1f}s',flush=True)
    with wave.open(str(TMP/'narration.wav'),'wb') as wav:
        wav.setparams((1,2,sr,0,'NONE','not compressed'))
        for piece in pieces:wav.writeframes(piece)

def render_video(scenes):
    target=OUT/'encounters-with-the-other.mp4'
    ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-i',str(TMP/'narration.wav'),'-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-shortest',str(target)],stdin=subprocess.PIPE)
    for i,s in enumerate(scenes):
        base=base_frame(s,i);frames=round(s['duration']*FPS)
        for f in range(frames):
            im=diagram(base.copy(),s,f/max(1,frames-1),f/FPS)
            d=ImageDraw.Draw(im);d.line((56,644,56+1168*(f+1)/frames,644),fill=GOLD,width=2)
            # A short fade preserves the legibility of a steady text field.
            fade=min(1,(f+1)/(FPS*.4),(frames-f)/(FPS*.4))
            if fade<1:im=Image.blend(Image.new('RGB',(W,H),BG),im,fade)
            ff.stdin.write(im.tobytes())
        print(f'Animation {i+1}/{len(scenes)}',flush=True)
    ff.stdin.close()
    if ff.wait()!=0:raise RuntimeError('Film encoding failed')
    run(['ffmpeg','-y','-loglevel','error','-i',str(TMP/'narration.wav'),'-codec:a','libmp3lame','-b:a','128k',str(OUT/'narration.mp3')])

def write_pages(scenes):
    chapters=[];cues=[];transcript=[];t=0
    for i,s in enumerate(scenes):
        s['start']=t
        if not chapters or chapters[-1]['title']!=s['chapter']:chapters.append({'title':s['chapter'],'start':t})
        narration=s.get('narration',s['title'].replace('\n',' ')+'. '+s['text'].replace('\n',' '))
        cues.append(f'{i+1}\n{stamp(t)} --> {stamp(t+s["duration"])}\n{narration}\n')
        transcript.append(f'<section id="scene-{i+1}"><p class="locator">{html.escape(s["chapter"])} · <a href="index.html#t={t:.3f}">{clock(t)}</a> · Source pp. {html.escape(s["pages"])}</p><h2>{html.escape(s["title"].replace(chr(10)," "))}</h2><p>{html.escape(s["text"])}</p></section>')
        t+=s['duration']
    OUT.mkdir(parents=True,exist_ok=True)
    for filename in ['style.css','player.js']:shutil.copyfile(SRC/filename,OUT/filename)
    page=(SRC/'index.html').read_text().replace('@@RUNTIME@@',clock(t)).replace('@@CHAPTERS@@',''.join(f'<a href="#t={c["start"]:.3f}" data-start="{c["start"]:.3f}"><time>{clock(c["start"])}</time>{html.escape(c["title"])}</a>' for c in chapters))
    (OUT/'index.html').write_text(page)
    head='<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive,nosnippet"><link rel="stylesheet" href="style.css"><title>Encounters with the Other: transcript</title></head><body><main class="transcript"><a href="index.html">Back to the film</a>'
    foot='<a id="openUpdates" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" aria-label="Open updates"></a></body></html>'
    (OUT/'transcript.html').write_text(head+'<h1>Encounters with the Other</h1><p>Abridged adaptation of Barry Oshry\'s book, for the author\'s review. Synthetic narration reads the scene titles and text below. Page numbers refer to the printed pagination of the supplied 2026 free edition.</p>'+''.join(transcript)+'</main>'+foot)
    credits='<h1>Production notes</h1><p>Book: Barry Oshry, Encounters with the Other. Triarchy Press, 2026 free edition. ISBN 978-1-911193-70-8. Copyright Barry Oshry, 2024 and 2026.</p><p>Adaptation prepared by Benjamin P Taylor with AI assistance for the author\'s review. Wording is condensed except for short attributed quotations. The complete sequence of the argument is retained; front matter, endorsements, and the full historical catalogue are not reproduced. This page does not imply the author has approved the adaptation.</p><p>Voice: Piper en_US-ljspeech-high, a synthetic US English voice. It is not Barry Oshry\'s voice. Engine: Piper 1.3.0, GPL-3.0. Voice source and dataset terms are recorded in the <a href="https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/ljspeech/high/MODEL_CARD">voice model card</a>. The narrator speaks the on-screen text, with an approximate pronunciation aid for Oshry.</p><p>The figures are conceptual animations of the book\'s relationships. Colours and shapes have no racial, national, or party meanings. The film contains no graphic historical imagery and no music.</p><p>Video: H.264, 1280 by 720, 12 frames per second; embedded AAC narration. Captions, transcript, chapter navigation, and a separate MP3 accompany the film. The page is unlisted, with noindex metadata, and is accessible to anyone with its URL.</p>'
    (OUT/'production-notes.html').write_text(head.replace('transcript</title>','production notes</title>')+credits+'</main>'+foot)
    (OUT/'captions.vtt').write_text('WEBVTT\n\n'+'\n'.join(cues))
    (OUT/'chapters.vtt').write_text('WEBVTT\n\n'+'\n'.join(f'{stamp(c["start"])} --> {stamp(chapters[j+1]["start"] if j+1<len(chapters) else t)}\n{c["title"]}\n' for j,c in enumerate(chapters)))
    (OUT/'timeline.json').write_text(json.dumps({'duration':t,'chapters':chapters,'scenes':scenes},ensure_ascii=False,indent=2)+'\n')
    return t

def stills(scenes):
    thumbs=[]
    for i,s in enumerate(scenes):
        frame=diagram(base_frame(s,i),s,.5,4)
        if i==0:frame.save(OUT/'poster.jpg',quality=94)
        frame.save(TMP/f'frame-{i+1:02d}.jpg',quality=88)
        thumb=frame.resize((384,216));thumbs.append(thumb)
    contact=Image.new('RGB',(384*3,242*math.ceil(len(thumbs)/3)),CREAM)
    d=ImageDraw.Draw(contact)
    for i,thumb in enumerate(thumbs):
        x=(i%3)*384;y=(i//3)*242;contact.paste(thumb,(x,y));d.text((x+8,y+219),str(i+1),font=FONT[20],fill=BG)
    contact.save(TMP/'contact-sheet.jpg',quality=85)

def verify():
    timeline=json.loads((OUT/'timeline.json').read_text())
    media=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_format','-show_streams','-of','json',str(OUT/'encounters-with-the-other.mp4')]))
    types={s['codec_type'] for s in media['streams']};assert {'video','audio'}<=types
    assert abs(float(media['format']['duration'])-timeline['duration'])<.3
    assert '<meta name="robots" content="noindex' in (OUT/'index.html').read_text()
    assert 'encounters-with-the-other' not in (ROOT/'docs/sitemap.xml').read_text()
    for s in timeline['scenes']:assert s.get('speech_duration',0)>1
    for p in OUT.glob('*.html'):
        content=p.read_text();assert 'noindex' in content and '@@' not in content
        for ref in re.findall(r'(?:src|href)="([^"#]+)',content):
            target=ref.split('#')[0].split('?')[0]
            if not target or target.startswith(('http','/','mailto:')):continue
            assert (OUT/target).exists(),(p,target)
    report={'passed':True,'duration':timeline['duration'],'scenes':len(timeline['scenes']),'audio':True,'resolution':'1280x720','sha256':hashlib.sha256((OUT/'encounters-with-the-other.mp4').read_bytes()).hexdigest()}
    (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--verify-only',action='store_true');ap.add_argument('--model',type=Path,default=ROOT/'voice/en_US-ljspeech-high.onnx');args=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
    if args.verify_only:verify();return
    scenes=DATA['scenes'];stills(scenes)
    if args.preview:write_pages(scenes);print('Preview stills and page generated; no film claimed.');return
    assert args.model.exists(),'A downloaded Piper voice is required; no silent substitute will be published.'
    prepare_audio(scenes,args.model);write_pages(scenes);render_video(scenes);verify()

if __name__=='__main__':main()
