#!/usr/bin/env python3
"""Merge researched public post rows locally; never fetch, publish, or schedule.

Usage: python3 scripts/merge_syscoi_intake.py /tmp/incoming-public-posts.json
Input is an array of complete rows, or an object with a `posts` array.
The caller owns the SHA-guarded GitHub write and live deployment verification.
"""
import copy
import json
import sys
from pathlib import Path
from build_syscoi_intake import MANIFEST, validate_manifest


def merge(original, incoming):
    result = copy.deepcopy(original)
    by_id = {p['post_id']: p for p in result['posts']}
    seen = set()
    for candidate in incoming:
        ident = candidate['post_id']
        assert ident not in seen, f'Duplicate incoming post ID {ident}'
        seen.add(ident)
        previous = by_id.get(ident)
        current = dict(previous or {}, **copy.deepcopy(candidate))
        versions = list((previous or {}).get('versions', []))
        for version in candidate.get('versions', []):
            if not any((v['modified_local'], v['content_sha256']) == (version['modified_local'], version['content_sha256']) for v in versions):
                versions.append(version)
        current['versions'] = versions
        if previous is None:
            result['posts'].append(current)
        else:
            result['posts'][result['posts'].index(previous)] = current
        by_id[ident] = current
    result['posts'].sort(key=lambda p: (p['published_gmt'], p['post_id']))
    validate_manifest(result)
    return result


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    original = json.loads(MANIFEST.read_text(encoding='utf-8'))
    incoming = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    result = merge(original, incoming['posts'] if isinstance(incoming, dict) else incoming)
    if result == original:
        print('No change: the manifest already contains these versions and descriptions.')
        return
    MANIFEST.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Merged public SysCoI records; {len(result["posts"])} total. Validate, SHA-guard the commit, and verify live publication.')


if __name__ == '__main__':
    main()
