#!/usr/bin/env python3
"""Derive automatic animated images from existing marks without changing originals."""
import hashlib
import json
import re
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def animation_frames(data):
    assert data[:4] == b'RIFF' and data[8:12] == b'WEBP'
    frames, offset = [], 12
    while offset + 8 <= len(data):
        name = data[offset:offset + 4]
        size = struct.unpack_from('<I', data, offset + 4)[0]
        payload = data[offset + 8:offset + 8 + size]
        if name == b'ANMF':
            frames.append(hashlib.sha256(payload[16:]).hexdigest())
        offset += 8 + size + (size % 2)
    return frames


def main():
    docs = ROOT / 'docs'
    assets = docs / 'assets/living-marks'
    manifest = json.loads((assets / 'manifest.json').read_text())
    report = []
    for mark in manifest['marks']:
        if mark['kind'] != 'video':
            continue
        source = docs / mark['src']
        output = assets / (mark['id'] + '-motion-v1.webp')
        if not output.exists():
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source), '-vf', 'fps=12,scale=192:192:flags=lanczos', '-an', '-c:v', 'libwebp_anim', '-quality', '65', '-compression_level', '4', '-loop', '0', str(output)], check=True)
        frames = animation_frames(output.read_bytes())
        assert len(frames) > 1 and len(set(frames)) > 1, mark['id']
        mark['animated_src'] = output.relative_to(docs).as_posix()
        report.append({'id': mark['id'], 'frames': len(frames), 'distinct_frame_payloads': len(set(frames)), 'bytes': output.stat().st_size})
    assert len(report) == 44
    (assets / 'playback-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    (docs / 'assets/iteration-19.js').write_text((ROOT / 'sources/living-mark-images.js').read_text())
    (docs / 'assets/reader-motion.js').write_text('/* Automatic image animation is owned by iteration-19.js. No playback controls. */\n')
    page = docs / 'index.html'
    text = page.read_text()
    text = re.sub(r'(assets/(?:reader-motion|iteration-19)\.js)(?:\?v=[^"\s]+)?', r'\1?v=20260907-automatic-2', text)
    text = re.sub(r'<style id="compact-mark-control">.*?</style>', '', text, flags=re.S)
    text = re.sub(r'<style>\.living-mark-playback\{.*?</style>', '', text, flags=re.S)
    page.write_text(text)
    target = ROOT / 'validation/living-mark-images.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps({'status': 'passed', 'moving_marks': len(report), 'source_videos_unchanged': True, 'playback_controls': False, 'marks': report}, indent=2) + '\n')
    print('Automatic animated-image playback:', len(report), 'marks;', sum(r['bytes'] for r in report), 'bytes. No playback controls. Original media unchanged.')


if __name__ == '__main__':
    main()
