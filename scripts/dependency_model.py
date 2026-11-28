"""The static-reader projection of recorded prerequisite claims."""
import json
from html import escape
from urllib.parse import quote


def unpack(value):
    if isinstance(value, list):
        return value
    try:
        parsed = json.loads(value or '[]')
        return parsed if isinstance(parsed, list) else []
    except (ValueError, TypeError):
        return []


class DependencyIndex:
    def __init__(self, data):
        self.redirects = data.get('canonical_redirects', {})
        self.nodes = {n['id']: n for n in data['nodes'] if n.get('public_visibility') == 'public' and self.canonical(n['id']) == n['id']}
        self.sources = {row['id']: row for row in data['sources']}
        self.strict = {row['relation_type'] for row in data['relation_types'] if row.get('strict_dependency') in [True, 'true', 'yes']}
        self.incoming, self.outgoing = {}, {}
        for original in data['edges']:
            edge = dict(original, source=self.canonical(original['source']), target=self.canonical(original['target']))
            if edge['source'] not in self.nodes or edge['target'] not in self.nodes or edge['source'] == edge['target']:
                continue
            if edge['relation_type'] not in self.strict or edge.get('claim_status') in ['rejected', 'superseded', 'legacy_unresolved']:
                continue
            self.incoming.setdefault(edge['target'], []).append(edge)
            self.outgoing.setdefault(edge['source'], []).append(edge)

    def canonical(self, ident):
        seen = set()
        while ident in self.redirects and ident not in seen:
            seen.add(ident)
            ident = self.redirects[ident]
        return ident

    def direct(self, ident):
        ident = self.canonical(ident)
        return dict(predecessors=sorted({e['source'] for e in self.incoming.get(ident, [])}),
                    dependents=sorted({e['target'] for e in self.outgoing.get(ident, [])}))

    def html(self, ident, node_link):
        ident = self.canonical(ident)
        parts = ['<section class="dependency-summary" aria-label="Recorded prerequisites and dependent entries"><p><a href="/dependencies/?entry=' + quote(ident, safe='_-') + '">Explore the focused dependency view</a>.</p><div class="dependency-summary-columns">']
        for key, heading, edges, endpoint in [
            ('predecessors', 'Necessary predecessors', self.incoming.get(ident, []), 'source'),
            ('dependents', 'Dependent entries', self.outgoing.get(ident, []), 'target'),
        ]:
            groups = {}
            for edge in edges:
                groups.setdefault(edge[endpoint], []).append(edge)
            parts.append('<div id="' + key + '"><h2>' + heading + ' (' + str(len(groups)) + ')</h2>')
            if not groups:
                parts.append('<p>No prerequisite claim is recorded in this direction.</p>')
            else:
                parts.append('<ul>')
                for other, claims in sorted(groups.items(), key=lambda pair: self.nodes[pair[0]]['label'].casefold()):
                    parts.append('<li><a href="' + escape(node_link(other), quote=True) + '">' + escape(self.nodes[other]['label']) + '</a><details><summary>Inspect ' + str(len(claims)) + ' recorded claim' + ('' if len(claims) == 1 else 's') + '</summary>')
                    for edge in claims:
                        status = edge.get('claim_status', 'not stated').replace('_', ' ')
                        status = 'proposed' if status == 'candidate' else status
                        parts.append('<p><strong>' + escape(edge.get('plain_phrase') or edge['relation_type'].replace('_', ' ')) + '</strong> · ' + escape(status) + '</p><p>' + escape(edge.get('scope_conditions', '')) + '</p>')
                        if edge.get('source_locator'):
                            parts.append('<p>Source passage: ' + escape(edge['source_locator']) + '</p>')
                        for sid in unpack(edge.get('source_ids')):
                            source = self.sources.get(sid, {})
                            title, url = source.get('title', sid), source.get('url', '')
                            parts.append('<p>' + ('<a href="' + escape(url, quote=True) + '">' + escape(title) + '</a>' if url.startswith(('https://', 'http://')) else escape(title)) + '</p>')
                    parts.append('</details></li>')
                parts.append('</ul>')
            parts.append('</div>')
        parts.append('</div><p>These are recorded prerequisite claims, with their own scope and review status. <a href="/dependencies/?entry=' + quote(ident, safe='_-') + '&amp;mode=connections">Explore all other recorded relationships</a>.</p></section>')
        return ''.join(parts)
