#!/usr/bin/env node
'use strict';

const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const ROOT = path.resolve(__dirname, '..');

function canonicalPublic(data) {
  const redirects = data.canonical_redirects || {};
  return (data.nodes || []).filter((node) =>
    node.public_visibility === 'public' && (redirects[node.id] || node.id) === node.id
  );
}

// Execute the published reader script and its actual link handlers. Supplying
// each entropy index makes the whole selection space testable without sampling.
function reader(data, script) {
  let entropy = 0;
  const ready = [];
  class Anchor {
    constructor(id) {
      this.id = id;
      this.classes = new Set(['surprise-me']);
      this.dataset = {};
      this.href = '#view=item&id=fallback&from=home';
      this.handlers = new Map();
    }
    addEventListener(name, callback) { this.handlers.set(name, callback); }
    getAttribute(name) { return this[name]; }
  }
  const anchors = [new Anchor('surpriseMeNav'), new Anchor('surpriseMeHero'), new Anchor('')];
  const location = { hash: '#view=home' };
  const context = {
    TANGLE_DATA: data,
    URLSearchParams,
    Uint32Array,
    HTMLAnchorElement: Anchor,
    location,
    history: { replaceState(_state, _title, url) { location.hash = url; } },
    crypto: { getRandomValues(values) { values[0] = entropy; return values; } },
    document: {
      addEventListener(name, callback) { if (name === 'DOMContentLoaded') ready.push(callback); },
      querySelectorAll(selector) {
        const selectors = selector.split(',').map((item) => item.trim());
        return anchors.filter((anchor) => selectors.some((item) =>
          item.startsWith('#') ? anchor.id === item.slice(1)
            : item.startsWith('.') && anchor.classes.has(item.slice(1))
        ));
      },
      querySelector() { return null; },
      getElementById() { return null; },
      body: { classList: { add() {}, remove() {} } },
    },
    MutationObserver: class { observe() {} },
    requestAnimationFrame() {},
    addEventListener() {},
  };
  context.window = context;
  vm.runInNewContext(script, context, { filename: 'iteration-18.js', timeout: 5000 });
  ready.forEach((callback) => callback());
  return {
    draw(index, hash = '#view=home', anchorIndex = 0, modifiers = {}) {
      // A previous draw becomes the current entry and would shift the next
      // pool. Reset the route before every independent indexed draw.
      location.hash = hash;
      entropy = index;
      const anchor = anchors[anchorIndex];
      assert.equal(typeof anchor.handlers.get('click'), 'function', 'Random link has no click handler');
      anchor.handlers.get('click')({
        button: 0, metaKey: false, ctrlKey: false, shiftKey: false, altKey: false,
        preventDefault() {}, stopImmediatePropagation() {}, ...modifiers,
      });
      return {
        id: new URLSearchParams(location.hash.replace(/^#/, '')).get('id'),
        hash: location.hash,
        href: anchor.href,
      };
    },
  };
}

function assertReachable(data, script) {
  const expected = canonicalPublic(data).map((node) => node.id);
  assert.equal(new Set(expected).size, expected.length, 'Canonical public IDs are duplicated');
  const runtime = reader(data, script);
  const selected = expected.map((id, index) => {
    const actual = runtime.draw(index);
    assert.equal(actual.id, id, `Random draw ${index} cannot reach canonical public entry ${id}`);
    assert.equal(new URLSearchParams(actual.hash).get('from'), 'home');
    return actual.id;
  });
  assert.deepEqual([...new Set(selected)].sort(), [...expected].sort(), 'Random pool differs from all canonical public entries');
  if (expected.length) {
    assert.equal(runtime.draw(expected.length).id, expected[0], 'Random pool contains entries outside the canonical public set');
  }
  // The header, hero, and footer controls all use the same complete pool.
  if (expected.length) {
    for (const anchorIndex of [1, 2]) {
      assert.equal(runtime.draw(expected.length - 1, '#view=home', anchorIndex).id, expected.at(-1));
    }
  }
  if (expected.length > 1) {
    const current = expected[0];
    const actual = runtime.draw(0, `#view=item&id=${encodeURIComponent(current)}&from=map`);
    assert.equal(actual.id, expected[1], 'Current entry was not omitted from the next draw');
    assert.equal(new URLSearchParams(actual.hash).get('from'), 'map', 'Return view was lost');
    const redirects = data.canonical_redirects || {};
    const alias = Object.keys(redirects).find((id) => redirects[id] !== id && expected.includes(redirects[id]));
    if (alias) {
      const alternatives = expected.filter((id) => id !== redirects[alias]);
      for (const index of [0, alternatives.length - 1]) {
        assert.equal(runtime.draw(index, `#view=item&id=${encodeURIComponent(alias)}&from=browse`).id, alternatives[index], 'Alias did not identify the current canonical entry');
      }
    }
    const modified = runtime.draw(expected.length - 1, '#view=browse', 0, { ctrlKey: true });
    assert.equal(modified.hash, '#view=browse', 'Modified click replaced the current route');
    assert.equal(new URLSearchParams(modified.href).get('id'), expected.at(-1), 'Modified click has no genuine destination');
  }
  return selected;
}

function checkFixtures(script) {
  const fixture = {
    nodes: [
      { id: 'source_candidate', entity_type: 'source', status: 'candidate', publication_level: 'research_stub', public_visibility: 'public' },
      { id: 'corpus_provisional', entity_type: 'corpus', status: 'provisional', publication_level: 'described', description: '', public_visibility: 'public' },
      { id: 'person_unprofiled', entity_type: 'person', public_visibility: 'public' },
      { id: 'evidence_entry', entity_type: 'evidence', public_visibility: 'public' },
      { id: 'claim_entry', entity_type: 'claim', public_visibility: 'public' },
      { id: 'unknown_type', entity_type: 'a_future_entry_type', public_visibility: 'public' },
      { id: 'private_entry', entity_type: 'person', public_visibility: 'private' },
      { id: 'source_alias', entity_type: 'source', public_visibility: 'public' },
    ],
    canonical_redirects: { source_alias: 'source_candidate' },
    profiles: [], edges: [],
  };
  assert.deepEqual(assertReachable(fixture, script), ['source_candidate', 'corpus_provisional', 'person_unprofiled', 'evidence_entry', 'claim_entry', 'unknown_type']);
  assertReachable({ nodes: [], edges: [] }, script);
  const empty = reader({ nodes: [], edges: [] }, script).draw(0);
  assert.equal(empty.hash, '#view=home', 'Empty pool changed the route');
  const singleton = { nodes: [{ id: 'only_entry', public_visibility: 'public' }], edges: [] };
  assertReachable(singleton, script);
  assert.equal(reader(singleton, script).draw(0, '#view=item&id=only_entry&from=home').id, 'only_entry', 'Singleton pool failed when its entry was already open');
}

function runChecks(data, script) {
  const selected = assertReachable(data, script);
  const publicNodes = canonicalPublic(data);
  const selectedIds = new Set(selected);
  const profiles = new Set((data.profiles || []).map((profile) => profile.node_id));
  const checks = {
    sources: publicNodes.filter((node) => node.entity_type === 'source'),
    corpora: publicNodes.filter((node) => node.entity_type === 'corpus'),
    people_without_profiles: publicNodes.filter((node) => node.entity_type === 'person' && !profiles.has(node.id)),
  };
  for (const [name, nodes] of Object.entries(checks)) {
    assert.ok(nodes.length, `Dataset has no ${name} examples for the coverage check`);
    assert.ok(nodes.every((node) => selectedIds.has(node.id)), `Random selection omits ${name}`);
  }
  assert.equal(data.meta?.surprise_me_eligible_count, publicNodes.length, 'Published random-entry count differs from the complete pool');
  checkFixtures(script);
  return {
    canonical_public_entries: publicNodes.length,
    reachable_random_entries: selectedIds.size,
    canonical_id_sha256: crypto.createHash('sha256').update([...selectedIds].sort().join('\n')).digest('hex'),
    explicit_coverage: Object.fromEntries(Object.entries(checks).map(([name, nodes]) => [name, nodes.length])),
    private_and_redirected_excluded: true,
    missing_metadata_and_future_entry_types_included: true,
    current_entry_avoidance: true,
    empty_and_singleton_pools: true,
  };
}

async function fetchText(url) {
  const response = await fetch(url, { cache: 'no-store', signal: AbortSignal.timeout(30000) });
  assert.ok(response.ok, `${url}: HTTP ${response.status}`);
  return response.text();
}

async function main() {
  const base = process.env.TANGLE_BASE_URL;
  let data, script, source;
  if (base) {
    const root = base.replace(/\/$/, '') + '/';
    const html = await fetchText(root);
    const matches = [...html.matchAll(/<script\b[^>]*\bsrc=["']([^"']*\biteration-18\.js[^"']*)["'][^>]*>/g)];
    assert.equal(matches.length, 1, 'Live page must load the active random-entry script exactly once');
    const dataMatches = [...html.matchAll(/<script\b[^>]*\bsrc=["']([^"']*\bpublic-data\.js[^"']*)["'][^>]*>/g)];
    assert.equal(dataMatches.length, 1, 'Live page must load the reader dataset exactly once');
    source = new URL(matches[0][1], root).href;
    const [readerScript, dataScript, payload] = await Promise.all([
      fetchText(source), fetchText(new URL(dataMatches[0][1], root)),
      fetchText(new URL('assets/public-data.json', root)),
    ]);
    script = readerScript;
    const dataContext = { window: {} };
    vm.runInNewContext(dataScript, dataContext, { filename: 'public-data.js', timeout: 10000 });
    data = dataContext.window.TANGLE_DATA;
    assert.ok(data?.nodes, 'The served reader dataset did not initialise TANGLE_DATA');
    const jsonData = JSON.parse(payload);
    assert.deepEqual(Array.from(canonicalPublic(data), (node) => node.id).sort(), canonicalPublic(jsonData).map((node) => node.id).sort(), 'Served JS and JSON disagree on canonical public entries');
  } else {
    source = 'docs/assets/iteration-18.js';
    data = JSON.parse(fs.readFileSync(path.join(ROOT, 'docs/assets/public-data.json'), 'utf8'));
    script = fs.readFileSync(path.join(ROOT, source), 'utf8');
  }
  const report = { source, release: data.meta?.release, ...runChecks(data, script) };
  const output = path.join(ROOT, 'validation/random-entry-all');
  fs.mkdirSync(output, { recursive: true });
  fs.writeFileSync(path.join(output, base ? 'live.json' : 'local.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
  return report;
}

module.exports = { main, runChecks, assertReachable, checkFixtures };
if (require.main === module) main().catch((error) => { console.error(error); process.exitCode = 1; });
