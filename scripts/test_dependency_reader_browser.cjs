#!/usr/bin/env node
'use strict';

const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const ROOT = path.resolve(__dirname, '../docs');
const OUTPUT = path.resolve(__dirname, '../validation/dependency-reader');
const report = { status: 'running', checks: [] };
const sorted = (values) => [...values].sort();
let server, browser;

async function serve() {
  const supplied = (process.env.TANGLE_BASE_URL || '').replace(/\/$/, '');
  if (supplied) return supplied;
  server = http.createServer((request, response) => {
    const filePath = path.resolve(ROOT, '.' + decodeURIComponent(new URL(request.url, 'http://local').pathname));
    if (filePath !== ROOT && !filePath.startsWith(ROOT + path.sep)) { response.writeHead(403); return response.end(); }
    try {
      const file = fs.statSync(filePath).isDirectory() ? path.join(filePath, 'index.html') : filePath;
      const mime = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.json': 'application/json', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.webp': 'image/webp' };
      response.setHeader('Content-Type', mime[path.extname(file)] || 'application/octet-stream');
      response.end(fs.readFileSync(file));
    } catch { response.writeHead(404); response.end(); }
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  return 'http://127.0.0.1:' + server.address().port;
}

async function ready(page, id) {
  await page.waitForFunction((expected) => {
    const model = window.TANGLE_DEPENDENCIES;
    return model && document.querySelector('#dependency-focus h2')?.textContent === model.nodes.get(model.canonical(expected))?.label;
  }, id);
}

async function gotoEntry(page, base, id, extra = '') {
  const response = await page.goto(base + '/dependencies/?entry=' + encodeURIComponent(id) + extra, { waitUntil: 'load' });
  assert.equal(response.status(), 200);
  await ready(page, id);
}

async function noOverflow(page, label) {
  const dimensions = await page.evaluate(() => ({ width: innerWidth, page: document.documentElement.scrollWidth }));
  assert.ok(dimensions.page <= dimensions.width + 1, label + ': horizontal overflow ' + JSON.stringify(dimensions));
}

async function checkLanes(page, id, depth = 1) {
  const expected = await page.evaluate(({ entry, reach }) => {
    const model = window.TANGLE_DEPENDENCIES;
    return Object.fromEntries(['predecessors', 'dependents'].map((side) => [side, model.trace(entry, side, reach).entries.map((group) => group.node.id).sort()]));
  }, { entry: id, reach: depth });
  for (const [side, ids] of Object.entries(expected)) {
    const prefix = side === 'predecessors' ? 'predecessor' : 'dependent';
    const actual = await page.locator('#' + prefix + '-cards > .dependency-card').evaluateAll((cards) => cards.map((card) => card.dataset.nodeId).sort());
    assert.deepEqual(actual, ids, side + ' IDs do not match the recorded direction and reach');
    assert.equal(await page.locator('#' + prefix + '-title').textContent(), (side === 'predecessors' ? 'Necessary predecessors' : 'Dependent entries') + ' (' + ids.length + ')');
  }
  return expected;
}

async function copyView(page) {
  await page.evaluate(() => { window.__dependencyCopied = null; });
  await page.locator('#dependency-copy').click();
  await page.waitForFunction(() => typeof window.__dependencyCopied === 'string');
  return new URL(await page.evaluate(() => window.__dependencyCopied));
}

async function search(page, text) {
  await page.locator('#dependency-query').fill(text);
  await page.locator('#dependency-search button').click();
}

async function checkViewport(base, width) {
  const context = await browser.newContext({ viewport: { width, height: 1000 }, reducedMotion: 'reduce' });
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { async writeText(value) { window.__dependencyCopied = value; } } });
  });
  const page = await context.newPage();
  page.setDefaultTimeout(15000);
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await gotoEntry(page, base, 'concept_boundary');
  const counts = await checkLanes(page, 'concept_boundary');
  assert.equal(counts.predecessors.length, 1, 'Boundary fixture changed; review its documented predecessor');
  assert.equal(counts.dependents.length, 5, 'Boundary fixture changed; review its five documented dependents');
  assert.equal(await page.locator('#dependency-mode').inputValue(), 'necessary');
  assert.equal(await page.locator('#dependency-depth').inputValue(), '1');
  assert.equal(await page.locator('#dependency-related').isVisible(), false);
  const feedback = page.getByRole('link', { name: 'Open updates', exact: true });
  assert.equal(await feedback.getAttribute('href'), 'https://github.com/antlerboy/the-necessary-tangle/issues/2');
  const dot = await feedback.boundingBox();
  assert.ok(dot.width >= 24 && dot.height >= 24 && dot.x >= width - 80 && dot.y >= 920, 'Updates dot must remain a usable bottom-right control');
  await noOverflow(page, 'Default diagram at ' + width);
  const boxes = await Promise.all(['dependency-predecessors', 'dependency-focus', 'dependency-dependents'].map((id) => page.locator('#' + id).boundingBox()));
  if (width > 780) assert.ok(boxes[0].x < boxes[1].x && boxes[1].x < boxes[2].x, 'Desktop diagram is not predecessor → focus → dependent');
  else assert.ok(boxes[1].y < boxes[0].y && boxes[0].y < boxes[2].y, 'Mobile view must put the focused entry before its directional lists');
  await page.screenshot({ path: path.join(OUTPUT, 'diagram-' + width + '.png'), fullPage: true });

  const firstCard = page.locator('#predecessor-cards > .dependency-card').first();
  const claimId = await firstCard.locator('.dependency-claim').first().getAttribute('data-edge-id');
  const claim = await page.evaluate((id) => {
    const model = window.TANGLE_DEPENDENCIES;
    const edge = model.edges.find((row) => row.id === id);
    return { ...edge, urls: model.unpack(edge.source_ids).map((source) => model.sources.get(source)?.url).filter((url) => /^https?:\/\//.test(url || '')) };
  }, claimId);
  await firstCard.locator('summary').click();
  const disclosure = firstCard.locator('.dependency-claim').first();
  assert.ok(await disclosure.isVisible());
  assert.ok((await disclosure.textContent()).includes(claim.plain_phrase));
  assert.equal(await disclosure.locator('.dependency-review').getAttribute('data-state'), claim.claim_status);
  if (claim.scope_conditions) assert.ok((await disclosure.textContent()).includes(claim.scope_conditions));
  if (claim.source_locator) assert.ok((await disclosure.textContent()).includes(claim.source_locator));
  for (const url of claim.urls) assert.ok((await disclosure.locator('a').evaluateAll((links) => links.map((link) => link.getAttribute('href')))).includes(url));
  await noOverflow(page, 'Expanded evidence at ' + width);
  await page.screenshot({ path: path.join(OUTPUT, 'evidence-' + width + '.png'), fullPage: true });

  const nextId = await firstCard.getAttribute('data-node-id');
  await firstCard.locator('h3 a.focus-link').click();
  await ready(page, nextId);
  assert.equal(new URL(page.url()).searchParams.get('entry'), nextId);
  await page.goBack(); await ready(page, 'concept_boundary');
  await page.goForward(); await ready(page, nextId);
  await page.goBack(); await ready(page, 'concept_boundary');
  for (const reach of [2, 3, 1]) {
    await page.locator('#dependency-depth').selectOption(String(reach));
    assert.equal(new URL(page.url()).searchParams.get('depth'), String(reach));
    await checkLanes(page, 'concept_boundary', reach);
  }
  await page.locator('#dependency-mode').selectOption('connections');
  assert.ok(await page.locator('#dependency-related').isVisible());
  assert.equal(await page.locator('#dependency-predecessors').isVisible(), false);
  assert.equal(await page.locator('#dependency-dependents').isVisible(), false);
  assert.ok(await page.locator('#dependency-depth').isDisabled());
  const relatedExpected = await page.evaluate(() => window.TANGLE_DEPENDENCIES.related('concept_boundary').map((group) => group.node.id).sort());
  while (await page.locator('#dependency-more').isVisible()) await page.locator('#dependency-more').click();
  assert.deepEqual(sorted(await page.locator('#related-cards > .dependency-card').evaluateAll((cards) => cards.map((card) => card.dataset.nodeId))), relatedExpected);
  await page.locator('#dependency-filter').fill('no such connected entry 9a146');
  assert.ok((await page.locator('#related-cards').textContent()).includes('No matching recorded relationship.'));
  await page.locator('#dependency-filter').fill('');
  await noOverflow(page, 'All relationships at ' + width);

  await gotoEntry(page, base, 'concept_boundaries', '&mode=connections&depth=3&side=dependents');
  let url = new URL(page.url());
  assert.equal(url.searchParams.get('entry'), 'concept_boundary');
  assert.equal(url.searchParams.get('mode'), 'connections');
  assert.equal(url.searchParams.get('depth'), '1');
  assert.equal(url.searchParams.get('side'), 'dependents');
  assert.equal(await page.locator('#dependency-mode').inputValue(), 'connections');
  let copied = await copyView(page);
  assert.equal(copied.href, page.url(), 'Copy must preserve the canonical, visible view');
  await gotoEntry(page, base, 'concept_boundaries', '&mode=necessary&depth=3&side=predecessors');
  url = new URL(page.url());
  assert.equal(url.searchParams.get('entry'), 'concept_boundary');
  assert.equal(url.searchParams.get('depth'), '3');
  assert.equal(url.searchParams.get('side'), 'predecessors');
  await checkLanes(page, 'concept_boundary', 3);
  copied = await copyView(page);
  assert.equal(copied.href, page.url());

  await search(page, 'no such public entry 9a146');
  assert.ok((await page.locator('#dependency-search-results').textContent()).includes('No public entry matched that search.'));
  const ambiguous = await page.evaluate(() => {
    const model = window.TANGLE_DEPENDENCIES;
    const normal = (value) => String(value || '').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
    const names = [...model.nodes.values()].map((node) => [node.label, ...model.unpack(node.aliases)].map(normal));
    return ['sys', 'cyb', 'comp', 'con'].find((query) => {
      const scores = names.map((row) => Math.max(0, ...row.map((name) => name === query ? 100 : name.startsWith(query) ? 30 : name.includes(query) ? 10 : 0))).sort((a, b) => b - a);
      return scores[0] > 0 && scores[0] === scores[1];
    });
  });
  assert.ok(ambiguous, 'Need a genuinely ambiguous public search fixture');
  await search(page, ambiguous);
  assert.ok(await page.locator('#dependency-search-results a.focus-link').count() > 1, 'Ambiguous search needs actual focus links');
  await search(page, 'Boundary'); await ready(page, 'concept_boundary');
  const alias = await page.evaluate(() => window.TANGLE_DEPENDENCIES.unpack(window.TANGLE_DEPENDENCIES.nodes.get('concept_boundary').aliases).find((text) => text.toLowerCase() === 'boundaries'));
  if (alias) { await search(page, alias); await ready(page, 'concept_boundary'); }
  const gap = await page.evaluate(() => {
    const model = window.TANGLE_DEPENDENCIES;
    return [...model.nodes.values()].find((node) => { const neighbours = model.direct(node.id); return !neighbours.predecessors.length && !neighbours.dependents.length && model.related(node.id).length; })?.id;
  });
  assert.ok(gap, 'Need a public entry with a prerequisite gap and other recorded relationships');
  await gotoEntry(page, base, gap);
  assert.equal(await page.locator('.dependency-empty').filter({ hasText: 'No prerequisite claim is recorded' }).count(), 2);
  await page.locator('#predecessor-cards a.focus-link').click();
  assert.equal(await page.locator('#dependency-mode').inputValue(), 'connections');
  assert.ok(await page.locator('#related-cards .dependency-card').count() > 0);

  await gotoEntry(page, base, 'concept_boundary');
  const newTabLink = page.locator('#predecessor-cards h3 a.focus-link').first();
  const expectedHref = new URL(await newTabLink.getAttribute('href'), base).href;
  const originalHref = page.url();
  const popupPromise = context.waitForEvent('page');
  await newTabLink.click({ modifiers: [process.platform === 'darwin' ? 'Meta' : 'Control'] });
  const popup = await popupPromise;
  await popup.waitForLoadState('load');
  assert.equal(popup.url(), expectedHref, 'Modified click must open the actual focus destination');
  assert.equal(page.url(), originalHref, 'Modified click must preserve the original view');
  await popup.close();

  await page.goto(base + '/?motion=off#view=item&id=concept_boundary&from=home', { waitUntil: 'load' });
  await page.waitForSelector('#entryDrawer.open');
  assert.equal(await page.locator('#drawerBody .entry-head h1').textContent(), 'Boundary');
  const entryLinks = page.locator('#drawerBody .dependency-entry-links a');
  assert.equal(await entryLinks.count(), 2);
  assert.equal(await entryLinks.nth(0).textContent(), 'Necessary predecessors (1)');
  assert.equal(await entryLinks.nth(1).textContent(), 'Dependent entries (5)');
  assert.equal(new URL(await entryLinks.nth(0).getAttribute('href'), base).searchParams.get('side'), 'predecessors');
  await entryLinks.nth(0).click(); await ready(page, 'concept_boundary');
  assert.equal(new URL(page.url()).searchParams.get('side'), 'predecessors');
  await noOverflow(page, 'Entry link destination at ' + width);
  await page.goto(base + '/?motion=off#view=browse', { waitUntil: 'load' });
  await page.locator('#browseSearch').fill('Boundary');
  await page.locator('#browseSearch').press('Escape');
  await page.locator('#browseSearch').blur();
  const card = page.locator('#browseCards .card').filter({ has: page.locator('a.open-card[data-id="concept_boundary"]') });
  await card.waitFor({ state: 'visible' });
  const browseLinks = card.locator('.dependency-card-links a');
  assert.equal(await browseLinks.count(), 2);
  assert.equal(await browseLinks.nth(0).textContent(), 'Predecessors (1)');
  assert.equal(await browseLinks.nth(1).textContent(), 'Dependents (5)');
  for (const link of await browseLinks.all()) {
    const target = await link.boundingBox();
    assert.ok(target && target.width >= 44 && target.height >= 44, 'New browse dependency links need 44px pointer targets');
  }
  // The existing browse filters are sticky. Put the footer below them, as a
  // reader can by scrolling, before exercising the real pointer action.
  await browseLinks.nth(1).evaluate((link) => link.scrollIntoView({ block: 'end' }));
  try {
    await browseLinks.nth(1).click();
  } catch (error) {
    await page.screenshot({ path: path.join(OUTPUT, 'browse-failure-' + width + '.png'), fullPage: true });
    report.browse_failure = await page.evaluate(() => {
      const target = [...document.querySelectorAll('#browseCards .card')].find((article) => article.querySelector('a.open-card[data-id="concept_boundary"]'))?.querySelector('.dependency-card-links a:last-child');
      const box = target?.getBoundingClientRect();
      const hit = box && document.elementFromPoint(box.x + box.width / 2, box.y + box.height / 2);
      return { width: innerWidth, scrollY, target: box?.toJSON(), intercept: hit && { tag: hit.tagName, id: hit.id, class: hit.className, text: hit.textContent.slice(0, 160) }, panel: document.querySelector('.filter-panel')?.getBoundingClientRect().toJSON() };
    });
    throw error;
  }
  await ready(page, 'concept_boundary');
  assert.equal(new URL(page.url()).searchParams.get('side'), 'dependents');

  const finalEdition = await page.evaluate(() => !!window.TANGLE_DATA.biographies_107_45);
  if (finalEdition) {
    await page.goto(base + '/entries/concept_boundary/', { waitUntil: 'load' });
    assert.equal(await page.locator('.dependency-summary').count(), 1);
    assert.equal(await page.locator('#predecessors h2').textContent(), 'Necessary predecessors (1)');
    assert.equal(await page.locator('#dependents h2').textContent(), 'Dependent entries (5)');
    await noOverflow(page, 'Static prerequisite lists at ' + width);
    const redirects = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../sources/biographies-107-45/packet.json'), 'utf8')).identity_redirects;
    assert.equal(Object.keys(redirects).length, 5, 'Review the verified identity-redirect cohort');
    const aliasChecks = [];
    for (const [original, target] of Object.entries(redirects)) {
      await page.goto(base + '/?motion=off#view=item&id=' + encodeURIComponent(original) + '&from=home', { waitUntil: 'load' });
      await page.waitForSelector('#entryDrawer.open');
      const canonicalLabel = await page.evaluate((id) => window.TANGLE_DATA.nodes.find((node) => node.id === id)?.label, target);
      assert.equal(await page.locator('#drawerBody .entry-head h1').textContent(), canonicalLabel, 'Old biography hash must show the verified identity');
      assert.equal(new URLSearchParams(new URL(page.url()).hash.slice(1)).get('id'), target, 'Old biography hash must canonicalise the address');
      const readerLink = page.locator('#drawerBody .dependency-entry-links a').first();
      assert.equal(new URL(await readerLink.getAttribute('href'), base).searchParams.get('entry'), target);
      await page.evaluate(() => { window.__dependencyCopied = null; });
      await page.locator('#copyEntryLink').click();
      await page.waitForFunction(() => typeof window.__dependencyCopied === 'string');
      assert.equal(new URLSearchParams(new URL(await page.evaluate(() => window.__dependencyCopied)).hash.slice(1)).get('id'), target);
      await page.goto(base + '/entries/' + encodeURIComponent(original) + '/', { waitUntil: 'load' });
      await page.waitForURL((location) => location.pathname === '/entries/' + target + '/');
      assert.equal(await page.locator('h1').textContent(), canonicalLabel, 'Readable alias route must reach the canonical biography');
      aliasChecks.push({ original, target, hash_drawer: 'canonical title, address, copied link, and dependency route', static_alias: 'automatic redirect' });
    }
    report.checks.push({ width, biography_aliases: aliasChecks });
  }
  assert.deepEqual(errors, [], 'Page errors at width ' + width);
  report.checks.push({ width, directional_ids: counts, evidence: claimId, history: 'back/forward', reach: '1/2/3', modes: 'necessary/connections', alias: 'canonical with mode/depth/side preserved', search: 'exact/ambiguous/missing', gap_entry: gap, modified_click: 'native new tab', entry_and_browse_links: 'passed', copied_url: copied.href, static_summary: finalEdition ? 'passed' : 'not expected before biographies_107_45', overflow: 'none', page_errors: errors });
  await context.close();
}

async function checkReviewFixture(base) {
  const context = await browser.newContext({ viewport: { width: 390, height: 1000 }, reducedMotion: 'reduce' });
  const fixture = {
    meta: { release: 'browser-fixture' }, canonical_redirects: {},
    nodes: ['fixture_need', 'fixture_focus', 'fixture_dependent', 'fixture_influence'].map((id) => ({ id, label: id.replace(/_/g, ' '), entity_type: 'concept', public_visibility: 'public', description: 'Fictional regression fixture.' })),
    relation_types: [{ relation_type: 'definitional_prerequisite', strict_dependency: 'yes' }, { relation_type: 'influenced', strict_dependency: 'no' }],
    sources: [{ id: 'fixture_source', title: 'Fictional review fixture', url: 'https://example.org/fixture' }], evidence: [{ id: 'fixture_evidence', locator: 'Fictional fixture, paragraph 2.' }], profiles: [],
    edges: [
      { id: 'fixture_proposed', source: 'fixture_need', target: 'fixture_focus', relation_type: 'definitional_prerequisite', claim_status: 'candidate' },
      { id: 'fixture_disputed', source: 'fixture_focus', target: 'fixture_dependent', relation_type: 'definitional_prerequisite', claim_status: 'disputed' },
      { id: 'fixture_influence_edge', source: 'fixture_influence', target: 'fixture_focus', relation_type: 'influenced', claim_status: 'candidate' },
      { id: 'fixture_loop', source: 'fixture_dependent', target: 'fixture_need', relation_type: 'definitional_prerequisite', claim_status: 'accepted' },
    ].map((edge) => ({ ...edge, plain_phrase: 'fixture relationship', scope_conditions: 'This fixture asserts only the explicitly recorded scope.', source_locator: 'Fictional fixture, section 1.', source_ids: '["fixture_source"]', evidence_ids: '["fixture_evidence"]' })),
  };
  await context.route('**/assets/public-data.js*', (route) => route.fulfill({ contentType: 'application/javascript', body: 'window.TANGLE_DATA=' + JSON.stringify(fixture) + ';' }));
  const page = await context.newPage();
  const errors = []; page.on('pageerror', (error) => errors.push(error.message));
  await gotoEntry(page, base, 'fixture_focus');
  const lanes = await checkLanes(page, 'fixture_focus');
  assert.deepEqual(lanes, { predecessors: ['fixture_need'], dependents: ['fixture_dependent'] });
  for (const [state, label] of [['candidate', 'Proposed'], ['disputed', 'Disputed']]) {
    const claim = page.locator('.dependency-columns .dependency-claim').filter({ has: page.locator('.dependency-review[data-state="' + state + '"]') });
    await claim.locator('..').locator('summary').click();
    assert.ok(await claim.isVisible());
    assert.ok((await claim.locator('.dependency-review').textContent()).startsWith(label + ' ·'));
    assert.ok((await claim.textContent()).includes('Fictional fixture, paragraph 2.'));
    assert.ok((await claim.textContent()).includes('explicitly recorded scope'));
  }
  assert.equal(await page.locator('#predecessor-cards [data-node-id="fixture_influence"]').count(), 0);
  assert.equal(await page.locator('#dependency-cycle').isVisible(), false);
  await page.locator('#dependency-depth').selectOption('3');
  assert.ok(await page.locator('#dependency-cycle').isVisible());
  assert.ok((await page.locator('#dependency-cycle').textContent()).includes('circular or mutual relationship'));
  await page.locator('#dependency-mode').selectOption('connections');
  assert.ok(await page.locator('#related-cards [data-node-id="fixture_influence"]').isVisible());
  assert.equal(await page.locator('#dependency-predecessors').isVisible(), false);
  await noOverflow(page, 'Proposed/disputed fixture');
  assert.deepEqual(errors, []);
  report.review_fixture = { candidate: 'Proposed', disputed: 'Disputed', influence: 'separate all-relationships mode', source_and_evidence_locators: 'visible', cycle_warning: 'visible at three steps', page_errors: errors };
  await context.close();
}

async function main() {
  fs.mkdirSync(OUTPUT, { recursive: true });
  const base = await serve(); report.base = base;
  browser = await chromium.launch({ headless: true });
  for (const width of [1440, 390]) { await checkViewport(base, width); console.log('Dependency reader real-page checks passed at ' + width + 'px.'); }
  await checkReviewFixture(base);
  report.status = 'passed';
  console.log('Dependency reader browser checks passed: real directional diagram at 1440/390, evidence, navigation, aliases, entry/card links, source labels, and no overflow or page errors.');
}

main().catch((error) => { report.status = 'failed'; report.error = error.stack; console.error(error); process.exitCode = 1; }).finally(async () => {
  fs.mkdirSync(OUTPUT, { recursive: true });
  fs.writeFileSync(path.join(OUTPUT, process.env.TANGLE_BASE_URL ? 'browser-live.json' : 'browser-local.json'), JSON.stringify(report, null, 2) + '\n');
  if (browser) await browser.close();
  if (server) { server.closeAllConnections?.(); await new Promise((resolve) => server.close(resolve)); }
});
