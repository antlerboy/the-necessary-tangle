#!/usr/bin/env node
'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const ROOT = path.resolve(__dirname, '..');
const api = require(path.join(ROOT, 'docs/assets/dependency-model.js'));
const STRICT = ['definitional_prerequisite', 'explanatory_prerequisite', 'formal_logical_prerequisite', 'methodological_prerequisite'];
const sorted = (values) => [...values].sort();
const node = (id, visibility = 'public') => ({ id, label: id, public_visibility: visibility, entity_type: 'concept' });
const edge = (id, source, target, relation_type = STRICT[0], claim_status = 'accepted') =>
  ({ id, source, target, relation_type, claim_status, source_ids: '["fixture_source"]', evidence_ids: '[]', source_locator: 'Fictional fixture, ' + id, scope_conditions: 'Test fixture only.' });

function fixture(nodes, edges, redirects = {}) {
  return {
    nodes: nodes.map((id) => typeof id === 'string' ? node(id) : id), edges,
    canonical_redirects: redirects,
    relation_types: [...STRICT.map((relation_type, i) => ({ relation_type, strict_dependency: [true, 'yes', 'true', 'yes'][i] })),
      { relation_type: 'influenced', strict_dependency: 'no' }, { relation_type: 'cites', strict_dependency: false },
      { relation_type: 'legacy_association_unspecified', strict_dependency: 'no' }],
    sources: [{ id: 'fixture_source', title: 'Fictional model fixture', url: '' }], evidence: [], profiles: [],
  };
}

function checkFixtures() {
  const data = fixture(['need', 'focus', 'dependent', 'influence', 'citation', 'rejected', 'superseded', 'legacy', 'unknown', 'alias', 'alias_chain', 'private_alias', node('private', 'private'), 'gap'], [
    edge('need-focus', 'need', 'focus'),
    edge('focus-dependent', 'focus', 'dependent', STRICT[2], 'candidate'),
    edge('alias-dependent', 'alias_chain', 'dependent', STRICT[1], 'disputed'),
    edge('historical-influence', 'influence', 'focus', 'influenced'),
    edge('citation', 'focus', 'citation', 'cites'),
    edge('private', 'private', 'focus'), edge('private-alias', 'private_alias', 'focus'),
    edge('rejected', 'rejected', 'focus', STRICT[0], 'rejected'),
    edge('superseded', 'superseded', 'focus', STRICT[0], 'superseded'),
    edge('legacy-status', 'legacy', 'focus', STRICT[0], 'legacy_unresolved'),
    edge('legacy-type', 'legacy', 'focus', 'legacy_association_unspecified'),
    { ...edge('unknown-type', 'unknown', 'focus', 'unknown_relation'), strict_dependency: true },
    edge('missing', 'missing', 'focus'), edge('self', 'focus', 'focus'),
    edge('gap-citation', 'gap', 'citation', 'cites'),
  ], { alias_chain: 'alias', alias: 'focus', private_alias: 'private' });
  const model = api.create(data);
  assert.deepEqual(sorted(model.strict), STRICT);
  assert.equal(model.canonical('alias_chain'), 'focus');
  assert.equal(model.nodes.has('alias'), false);
  assert.equal(model.nodes.has('private'), false);
  assert.equal(model.nodes.has('private_alias'), false);
  assert.deepEqual(model.direct('focus'), { predecessors: ['need'], dependents: ['dependent'] });
  assert.deepEqual(model.direct('alias_chain'), model.direct('focus'));
  assert.deepEqual(model.direct('dependent'), { predecessors: ['focus'], dependents: [] });
  assert.deepEqual(model.direct('need'), { predecessors: [], dependents: ['focus'] });
  assert.deepEqual(model.direct('gap'), { predecessors: [], dependents: [] });
  assert.deepEqual(model.direct('missing'), { predecessors: [], dependents: [] });
  const related = model.related('focus').flatMap((group) => group.edges);
  assert.ok(related.some((claim) => claim.id === 'historical-influence'));
  assert.ok(related.some((claim) => claim.id === 'citation'));
  assert.ok(related.some((claim) => claim.claim_status === 'rejected'));
  assert.deepEqual(model.related('gap').map((group) => group.node.id), ['citation']);
  assert.ok(model.edges.every((claim) => !['private', 'private-alias', 'missing', 'self'].includes(claim.id)));
  const direct = model.trace('focus', 'dependents', 1);
  assert.deepEqual(direct.entries.map((group) => group.node.id), ['dependent']);
  assert.equal(direct.entries[0].paths.length, 2, 'Distinct proposed and disputed claims must remain inspectable');
  assert.deepEqual(sorted(direct.entries[0].paths.flat().map((claim) => claim.claim_status)), ['candidate', 'disputed']);
  assert.deepEqual(api.unpack('["a","b"]'), ['a', 'b']);
  assert.deepEqual(api.unpack(['a']), ['a']);
  assert.deepEqual(api.unpack('{broken'), []);

  const chain = api.create(fixture(['p3', 'p2', 'p1', 'focus', 'd1', 'd2', 'd3', 'd4'], [
    edge('p3-p2', 'p3', 'p2'), edge('p2-p1', 'p2', 'p1'), edge('p1-focus', 'p1', 'focus'),
    edge('focus-d1', 'focus', 'd1'), edge('d1-d2', 'd1', 'd2'), edge('d2-d3', 'd2', 'd3'), edge('d3-d4', 'd3', 'd4'),
  ]));
  assert.deepEqual(chain.trace('focus', 'predecessors', 1).entries.map((group) => group.node.id), ['p1']);
  assert.deepEqual(chain.trace('focus', 'predecessors', 2).entries.map((group) => group.node.id), ['p1', 'p2']);
  assert.deepEqual(chain.trace('focus', 'predecessors', 3).entries.map((group) => group.node.id), ['p1', 'p2', 'p3']);
  assert.deepEqual(chain.trace('focus', 'dependents', 99).entries.map((group) => group.node.id), ['d1', 'd2', 'd3']);
  assert.deepEqual(chain.trace('focus', 'dependents', 0).entries.map((group) => group.node.id), ['d1']);
  assert.deepEqual(chain.trace('focus', 'dependents', 2.9).entries.map((group) => group.node.id), ['d1', 'd2']);
  const cyclic = api.create(fixture(['focus', 'b', 'c'], [edge('f-b', 'focus', 'b'), edge('b-c', 'b', 'c'), edge('c-f', 'c', 'focus')]));
  assert.equal(cyclic.trace('focus', 'dependents', 2).cycles.length, 0);
  const traced = cyclic.trace('focus', 'dependents', 3);
  assert.deepEqual(traced.entries.map((group) => group.node.id), ['b', 'c']);
  assert.equal(traced.cycles.length, 1);
  assert.deepEqual(traced.cycles[0].map((claim) => claim.id), ['f-b', 'b-c', 'c-f']);
  assert.equal(traced.truncated, false);
  const diamond = api.create(fixture(['focus', 'left', 'right', 'end'], [edge('f-l', 'focus', 'left'), edge('f-r', 'focus', 'right'), edge('l-e', 'left', 'end'), edge('r-e', 'right', 'end')]));
  const end = diamond.trace('focus', 'dependents', 2).entries.find((group) => group.node.id === 'end');
  assert.equal(end.distance, 2); assert.equal(end.paths.length, 2);
  assert.deepEqual(sorted(end.paths.flat().map((claim) => claim.id)), ['f-l', 'f-r', 'l-e', 'r-e']);
  assert.deepEqual(api.create(fixture([], [])).trace('missing', 'predecessors', 3), { entries: [], cycles: [], truncated: false });
}

function actualGraph(data) {
  const model = api.create(data);
  assert.deepEqual(sorted(model.strict), STRICT, 'The public strict registry changed; review its semantics');
  const direct = Object.fromEntries([...model.nodes.keys()].sort().map((id) => [id, {
    predecessors: sorted(model.direct(id).predecessors), dependents: sorted(model.direct(id).dependents),
  }]));
  const strictEdges = model.edges.filter(model.necessary);
  for (const [id, neighbours] of Object.entries(direct)) {
    assert.deepEqual(sorted(model.trace(id, 'predecessors', 1).entries.map((group) => group.node.id)), neighbours.predecessors);
    assert.deepEqual(sorted(model.trace(id, 'dependents', 1).entries.map((group) => group.node.id)), neighbours.dependents);
  }
  return { canonical_public_count: model.nodes.size, strict_edge_count: strictEdges.length, strict_types: sorted(model.strict), direct };
}

function main() {
  const dump = process.argv[2] === '--dump-direct';
  const input = dump && process.argv[3] ? path.resolve(process.argv[3]) : path.join(ROOT, 'docs/assets/public-data.json');
  const data = JSON.parse(fs.readFileSync(input, 'utf8'));
  if (dump) { process.stdout.write(JSON.stringify(actualGraph(data))); return; }
  checkFixtures();
  const actual = actualGraph(data);
  const output = path.join(ROOT, 'validation/dependency-reader'); fs.mkdirSync(output, { recursive: true });
  const report = { release: data.meta.release, canonical_public_count: actual.canonical_public_count, strict_edge_count: actual.strict_edge_count, strict_types: actual.strict_types, fixture_checks: 'passed', direct_trace_parity: 'all canonical public IDs' };
  fs.writeFileSync(path.join(output, 'model.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
}
module.exports = { checkFixtures, actualGraph, STRICT };
if (require.main === module) main();
