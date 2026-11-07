#!/usr/bin/env python3
"""Project the hourly worker's public SysCoI manifest into source resources.

This deterministic, offline overlay runs after the historical release gates.
It adds no atlas nodes, profiles, claims, evidence, or conceptual relationships.
"""
from __future__ import annotations

import copy
import hashlib
import html
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'sources/syscoi/intake.json'
OWNER = 'syscoi_continuous_intake'
MARKER = 'syscoi-continuous-intake'
PROTECTED = ('nodes', 'edges', 'profiles', 'claims', 'evidence', 'journeys', 'canonical_redirects')
TRACKING = {'fbclid', 'gclid', 'dclid', 'mc_cid', 'mc_eid', 'igshid', 'ref_src', 'srsltid'}


def encoded(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def unpack(value):
    if isinstance(value, list):
        return value
    try:
        result = json.loads(value or '[]')
        return result if isinstance(result, list) else []
    except (TypeError, ValueError):
        return []


def canonical_url(value):
    """A comparison key; keep the observed URL separately for attribution."""
    parsed = urlsplit(html.unescape(str(value)).strip())
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Expected a public HTTP(S) URL')
    host = parsed.hostname.lower().removeprefix('www.')
    if host in ('localhost', '127.0.0.1', '0.0.0.0', '::1') or host.endswith(('.local', '.internal', '.sharepoint.com')) or host in ('mail.google.com', 'graph.microsoft.com'):
        raise ValueError('Private URL is not publishable')
    port = parsed.port
    netloc = host + (f':{port}' if port and port not in (80, 443) else '')
    query = sorted((k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True) if not k.lower().startswith('utm_') and k.lower() not in TRACKING)
    return urlunsplit(('https', netloc, parsed.path.rstrip('/') or '/', urlencode(query), ''))


def urls(record):
    return [record.get('url', ''), *unpack(record.get('original_urls')), *unpack(record.get('canonical_aliases'))]


def keys(values):
    result = set()
    for value in values:
        if value:
            try:
                result.add(canonical_url(value))
            except ValueError:
                pass
    return result


def validate_manifest(manifest):
    assert manifest['schema_version'] == 1
    assert manifest['site_id'] == 130780538
    assert canonical_url(manifest['site_url']) == 'https://stream.syscoi.com/'
    seen = set()
    for post in manifest['posts']:
        ident = post['post_id']
        assert isinstance(ident, int) and ident > 0 and ident not in seen, f'Duplicate/invalid post ID {ident}'
        seen.add(ident)
        assert post['status'] == 'publish' and post['password_protected'] is False, ident
        assert urlsplit(post['post_url']).hostname == 'stream.syscoi.com', ident
        assert post['published_gmt'].endswith('Z') and post['modified_local'], ident
        assert re.fullmatch(r'[0-9a-f]{64}', post['content_sha256']), ident
        assert post['title'].strip() and post['author_name'].strip(), ident
        assert len(post['description'].split()) >= 20, f'Missing useful description: {ident}'
        assert post['description_status'] in ('source_scoped_summary', 'link_only_access_limited'), ident
        assert post['description_sources'], ident
        for source in post['description_sources']:
            canonical_url(source['url'])
            assert source['locator'].strip() and source['checked_at'], ident
        for url in [post['post_url'], post['primary_url'], *post['original_urls'], *post.get('canonical_aliases', [])]:
            canonical_url(url)
        versions = post.get('versions', [])
        assert any(v['content_sha256'] == post['content_sha256'] and v['modified_local'] == post['modified_local'] for v in versions), f'Current version absent: {ident}'
        assert len({(v['modified_local'], v['content_sha256']) for v in versions}) == len(versions), f'Duplicate versions: {ident}'


def reconcile(manifest, data, catalogue):
    """Match the whole earlier public source register before making a resource."""
    old_sources = [s for s in data['sources'] if s.get('intake_owner') != OWNER]
    old_catalogue = [r for r in catalogue['records'] if r.get('intake_owner') != OWNER]
    source_index, catalogue_index, node_index = defaultdict(set), defaultdict(set), defaultdict(set)
    cited_source_index = defaultdict(set)
    redirects = data.get('canonical_redirects', {})
    for source in old_sources:
        identity_urls = [source.get('url', ''), *unpack(source.get('canonical_aliases'))]
        original_keys = keys(unpack(source.get('original_urls')))
        # A one-destination discovery record identifies that resource. A link
        # among several outbound citations is only a reconciliation candidate.
        if source.get('source_role') == 'discovery provenance' and len(original_keys) == 1:
            identity_urls.extend(original_keys)
        for key in keys(identity_urls):
            source_index[key].add(source['id'])
        for key in original_keys:
            cited_source_index[key].add(source['id'])
    for record in old_catalogue:
        for key in keys([record.get('url', ''), *unpack(record.get('canonical_aliases'))]):
            catalogue_index[key].add(record['id'])
    for node in data['nodes']:
        # A concept citing a source is not itself the source's work identity.
        if node.get('public_visibility') == 'public' and node.get('entity_type') in ('publication', 'resource', 'tool', 'corpus', 'collection'):
            for sid in unpack(node.get('source_ids')):
                node_index[sid].add(redirects.get(node['id'], node['id']))
    grouped, url_resources, resolutions = {}, {}, []
    for post in sorted(manifest['posts'], key=lambda p: (p['published_gmt'], p['post_id'])):
        # Primary URL/explicit verified aliases identify a work. An incidental
        # outbound citation must never merge two otherwise distinct resources.
        match_keys = keys([post['primary_url'], *post.get('canonical_aliases', [])])
        sids = sorted(set().union(*(source_index[k] for k in match_keys)))
        cited_sids = sorted(set().union(*(cited_source_index[k] for k in match_keys)))
        cids = sorted(set().union(*(catalogue_index[k] for k in match_keys)))
        nids = sorted(set().union(*(node_index[sid] for sid in sids)))
        cited_nids = sorted(set().union(*(node_index[sid] for sid in cited_sids)))
        existing = cids or nids or sids
        same_batch = sorted({url_resources[k] for k in match_keys if k in url_resources})
        override = post.get('canonical_resource_id')
        if override:
            assert override in set(cids + nids + sids + cited_sids + cited_nids + same_batch), f'Unverified canonical resource {override}'
        candidates = {'source_ids': sorted(set(sids + cited_sids)), 'node_ids': sorted(set(nids + cited_nids)), 'catalogue_ids': cids}
        ambiguous = len(existing) > 1 or len(same_batch) > 1
        citation_only = not existing and bool(cited_sids)
        selected = existing[0] if len(existing) == 1 else same_batch[0] if not ambiguous and len(same_batch) == 1 else None
        if (ambiguous or citation_only) and not override:
            selected = same_batch[0] if len(same_batch) == 1 else None
        resource_id = override or selected or f'resource_syscoi_post_{post["post_id"]}'
        identity_status = 'explicitly_reconciled' if override else 'ambiguous_existing_matches' if ambiguous or citation_only else 'existing_resource' if existing else 'new_resource'
        if (ambiguous or citation_only) and not override:
            sids, nids, cids = [], [], []
        elif override:
            # Preserve the specifically chosen identity, not every conflicting
            # candidate merely found at the same URL.
            if len(cids) > 1: cids = [override] if override in cids else []
            if len(nids) > 1: nids = [override] if override in nids else []
            if override in cited_sids and override not in sids: sids.append(override)
            if override in cited_nids and override not in nids: nids.append(override)
        if resource_id not in grouped:
            grouped[resource_id] = {'id': resource_id, 'posts': [], 'existing_source_ids': set(), 'existing_catalogue_ids': set(), 'existing_node_ids': set(), 'canonical_aliases': set()}
        group = grouped[resource_id]
        group['posts'].append(post)
        group['existing_source_ids'].update(sids)
        group['existing_catalogue_ids'].update(cids)
        group['existing_node_ids'].update(nids)
        group['canonical_aliases'].update(match_keys)
        for key in match_keys:
            url_resources[key] = resource_id
        resolutions.append({'post_id': post['post_id'], 'resource_id': resource_id, 'source_id': f'src_syscoi_post_{post["post_id"]}', 'content_sha256': post['content_sha256'], 'modified_local': post['modified_local'], 'identity_status': identity_status, 'match_candidates': candidates, 'existing_source_ids': sids, 'existing_node_ids': nids, 'existing_catalogue_ids': cids})
    resources = []
    for group in grouped.values():
        latest = group['posts'][-1]
        resource = {key: sorted(value) if isinstance(value, set) else value for key, value in group.items() if key != 'posts'}
        resource.update(title=latest['title'], url=latest['primary_url'], description=latest['description'], description_status=latest['description_status'], description_sources=latest['description_sources'], source_authors=latest.get('source_authors', []), post_ids=[p['post_id'] for p in group['posts']], source_ids=[f'src_syscoi_post_{p["post_id"]}' for p in group['posts']], latest_published_gmt=latest['published_gmt'])
        resources.append(resource)
    return resources, resolutions


def projection(manifest, original, catalogue):
    validate_manifest(manifest)
    data, catalogue = copy.deepcopy(original), copy.deepcopy(catalogue)
    resources, resolutions = reconcile(manifest, data, catalogue)
    by_id = {s['id']: s for s in data['sources']}
    for post in sorted(manifest['posts'], key=lambda p: p['post_id']):
        sid = f'src_syscoi_post_{post["post_id"]}'
        row = {'id': sid, 'title': post['title'], 'source_type': 'public_source', 'quality_tier': 'B', 'access': 'public', 'url': post['post_url'], 'date': post['published_gmt'][:10], 'notes': post['description'], 'creators': encoded([post['author_name']]), 'doi': '', 'isbn': '', 'publisher': 'Systems Community of Inquiry', 'licence': 'Linked works retain their authorship and terms', 'archived_url': '', 'content_hash': post['content_sha256'], 'review_status': post['description_status'], 'last_checked': max(s['checked_at'] for s in post['description_sources']), 'public_link_status': 'public_link', 'original_urls': encoded(post['original_urls']), 'canonical_aliases': encoded(sorted(keys([post['primary_url'], *post.get('canonical_aliases', [])]))), 'source_role': 'discovery provenance', 'source_locator': f'Public post {post["post_id"]}; original outbound links; description locators in /library/syscoi/intake.json', 'intake_owner': OWNER, 'wp_site_id': manifest['site_id'], 'wp_post_id': post['post_id'], 'wp_modified_local': post['modified_local'], 'description_sources': post['description_sources'], 'versions': post['versions']}
        if sid not in by_id:
            data['sources'].append(row)
            by_id[sid] = row
        elif by_id[sid].get('intake_owner') == OWNER:
            by_id[sid].update(row)
        # Earlier curated source rows retain all their fields unchanged.
    catalogue_rows = {r['id']: r for r in catalogue['records']}
    for resource in resources:
        ident = resource['id']
        catalogue_ident = resource['existing_catalogue_ids'][0] if len(resource['existing_catalogue_ids']) == 1 else ident
        if catalogue_ident in catalogue_rows:
            record = catalogue_rows[catalogue_ident]
            record['syscoi_post_ids'] = sorted(set(record.get('syscoi_post_ids', [])) | set(resource['post_ids']))
            record['syscoi_resource_url'] = '/library/syscoi/#post-' + str(resource['post_ids'][0])
        else:
            record = {'id': ident, 'title': resource['title'], 'url': resource['url'], 'summary': resource['description'], 'authors': resource['source_authors'], 'collection': 'SysCoI reading', 'format': 'Source resource', 'year': resource['latest_published_gmt'][:4], 'review': 'Source-scoped reading' if resource['description_status'] == 'source_scoped_summary' else 'Public discovery link; destination content unavailable at check', 'locator': '; '.join(s['locator'] for s in resource['description_sources']), 'connections': [], 'atlas_id': resource['existing_node_ids'][0] if resource['existing_node_ids'] else '', 'intake_owner': OWNER, 'syscoi_post_ids': resource['post_ids'], 'syscoi_resource_url': '/library/syscoi/#post-' + str(resource['post_ids'][0])}
            catalogue['records'].append(record)
            catalogue_rows[ident] = record
        if record.get('intake_owner') == OWNER:
            record.update(title=resource['title'], url=resource['url'], summary=resource['description'], authors=resource['source_authors'], syscoi_post_ids=resource['post_ids'])
    manifest_hash = hashlib.sha256(encoded(manifest).encode()).hexdigest()
    intake = {'schema_version': 1, 'site_id': manifest['site_id'], 'collection_url': 'https://transduction.systems/library/syscoi/', 'manifest_sha256': manifest_hash, 'post_count': len(resolutions), 'resource_count': len(resources), 'reused_resource_count': sum(bool(r['existing_source_ids'] or r['existing_node_ids'] or r['existing_catalogue_ids']) for r in resources), 'atlas_nodes_added': 0, 'graph_edges_added': 0, 'resources': resources, 'posts': resolutions}
    data['syscoi_intake'] = intake
    data['meta']['source_count'] = len(data['sources'])
    data['meta']['public_link_source_count'] = sum(s.get('public_link_status') == 'public_link' for s in data['sources'])
    data['meta']['latest_syscoi_intake_url'] = intake['collection_url']
    catalogue['counts']['source_register_records'] = len(catalogue['records'])
    catalogue['counts']['continuous_syscoi_posts'] = len(resolutions)
    catalogue['counts']['continuous_syscoi_resources'] = len(resources)
    for key in PROTECTED:
        assert data[key] == original[key], f'Intake changed protected graph field {key}'
    return data, catalogue, intake


def render(manifest, intake, data):
    from build_readable_atlas import page, esc
    posts = {p['post_id']: p for p in manifest['posts']}
    body = '<p>Reading discovered through the Systems Community of Inquiry. Each resource keeps its original author, source links, and the public post that brought it here. Existing atlas records are linked where the same work is already represented.</p>'
    body += f'<p>{intake["post_count"]} public posts, {intake["resource_count"]} resources, and {intake["reused_resource_count"]} existing resource routes reconciled since 24 October 2026.</p>'
    body += '<p><a href="/library/?collection=SysCoI%20reading">Search these additions</a> · <a href="/library/">Search all sources</a> · <a href="intake.json">Download records and provenance</a></p>'
    for resource in sorted(intake['resources'], key=lambda r: r['latest_published_gmt'], reverse=True):
        body += '<article class="syscoi-resource">' + ''.join(f'<span id="post-{ident}"></span>' for ident in resource['post_ids'])
        body += '<h2><a href="' + esc(resource['url']) + '">' + esc(resource['title']) + '</a></h2>'
        if resource['source_authors']:
            body += '<p><small>' + esc(', '.join(resource['source_authors'])) + '</small></p>'
        body += '<p>' + esc(resource['description']) + '</p>'
        additional = []
        seen_urls = {canonical_url(resource['url'])}
        for ident in resource['post_ids']:
            for url in posts[ident]['original_urls']:
                key = canonical_url(url)
                if key not in seen_urls:
                    label = urlsplit(url).hostname + (urlsplit(url).path.rstrip('/') or '')
                    additional.append('<a href="' + esc(url) + '">' + esc(label) + '</a>')
                    seen_urls.add(key)
        if additional:
            body += '<p>Other links in the post: ' + ' · '.join(additional) + '</p>'
        body += '<p><small>Description based on ' + '; '.join('<a href="' + esc(s['url']) + '">' + esc(s['locator']) + '</a> (checked ' + esc(s['checked_at']) + ')' for s in resource['description_sources']) + '.</small></p>'
        body += '<p>' + ' · '.join('<a href="' + esc(posts[i]['post_url']) + '">SysCoI post, ' + esc(posts[i]['published_gmt'][:10]) + '</a> by ' + esc(posts[i]['author_name']) for i in resource['post_ids']) + '</p>'
        if resource['existing_node_ids']:
            body += '<p>' + ' · '.join('<a href="/#view=item&amp;id=' + esc(n) + '">Existing atlas record</a>' for n in resource['existing_node_ids']) + '</p>'
        if resource['existing_catalogue_ids']:
            body += '<p><a href="/library/?item=' + esc(resource['existing_catalogue_ids'][0]) + '">Existing source reading</a></p>'
        body += '</article>'
    return page('SysCoI reading', 'Attributed sources discovered through the Systems Community of Inquiry, with duplicate resources reconciled and original links preserved.', '/library/syscoi/', body, data['meta']['release'])


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    from refresh_graph_snapshot import write
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    original = json.loads((ROOT / 'data/public-data.json').read_text(encoding='utf-8'))
    catalogue_path = ROOT / 'docs/library/catalogue.json'
    data, catalogue, intake = projection(manifest, original, json.loads(catalogue_path.read_text(encoding='utf-8')))
    write(data)
    # Preserve the compact format used by the existing source-register builder.
    catalogue_path.write_text(encoded(catalogue) + '\n', encoding='utf-8')
    # Include the public descriptions and observed versions in the download.
    output = dict(intake, observed_posts=manifest['posts'])
    write_json(ROOT / 'docs/library/syscoi/intake.json', output)
    (ROOT / 'docs/library/syscoi/index.html').write_text(render(manifest, intake, data), encoding='utf-8')
    for relative in ('data/relationship-quality.json', 'docs/assets/relationship-quality.json'):
        path = ROOT / relative
        quality = json.loads(path.read_text(encoding='utf-8'))
        quality['current']['sources'] = len(data['sources'])
        quality['changes_from_baseline']['sources']['after'] = len(data['sources'])
        write_json(path, quality)
    library_path = ROOT / 'docs/library/index.html'
    text = library_path.read_text(encoding='utf-8')
    text = re.sub(r'<!-- ' + MARKER + r' -->.*?<!-- /' + MARKER + r' -->\s*', '', text, flags=re.S)
    block = '<!-- ' + MARKER + ' --><section class="resource-pathways" id="syscoi-reading"><h2><a href="/library/syscoi/">New reading from SysCoI</a></h2><p>Public posts, original sources, and attributed descriptions, with existing resource records brought together.</p></section><!-- /' + MARKER + ' -->'
    library_path.write_text(text.replace('</header>', '</header>' + block, 1), encoding='utf-8')
    next_path = ROOT / 'documentation/NEXT_WORK.md'
    text = next_path.read_text(encoding='utf-8')
    text = re.sub(r'<!-- ' + MARKER + r' -->.*?<!-- /' + MARKER + r' -->\s*', '', text, flags=re.S).rstrip()
    text += '\n\n<!-- ' + MARKER + ' -->\n## Standing intake: public SysCoI resources\n\nThe existing hourly publication worker maintains `sources/syscoi/intake.json`. This final build overlay publishes attributed source resources at `/library/syscoi/` and in the source register; graph nodes, profiles, relationships, and random-entry eligibility remain unchanged. See `documentation/SYSCOI_INTAKE.md` for merge and verification rules. The public data records each post ID, content hash, and canonical resource identity. Deployment identity and live checks belong to deployment.json and the Publish workflow.\n<!-- /' + MARKER + ' -->\n'
    next_path.write_text(text, encoding='utf-8')
    print(f'SysCoI intake: {intake["post_count"]} posts, {intake["resource_count"]} resources, {intake["reused_resource_count"]} existing resource routes; no graph additions.')


if __name__ == '__main__':
    main()
