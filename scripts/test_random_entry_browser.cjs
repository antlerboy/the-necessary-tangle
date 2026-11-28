#!/usr/bin/env node
'use strict';

const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const ROOT = path.resolve(__dirname, '../docs');
const OUTPUT = path.resolve(__dirname, '../validation/random-entry-all');
const report = { status: 'running', checks: [] };
let server, browser;

async function main() {
  let base = (process.env.TANGLE_BASE_URL || '').replace(/\/$/, '');
  if (!base) {
    server = http.createServer((request, response) => {
      const filePath = path.resolve(ROOT, '.' + decodeURIComponent(new URL(request.url, 'http://local').pathname));
      if (filePath !== ROOT && !filePath.startsWith(ROOT + path.sep)) {
        response.writeHead(403); return response.end();
      }
      try {
        const file = fs.statSync(filePath).isDirectory() ? path.join(filePath, 'index.html') : filePath;
        const mime = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.json': 'application/json', '.css': 'text/css', '.svg': 'image/svg+xml', '.webp': 'image/webp' };
        response.setHeader('Content-Type', mime[path.extname(file)] || 'application/octet-stream');
        response.end(fs.readFileSync(file));
      } catch { response.writeHead(404); response.end(); }
    });
    await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
    base = 'http://127.0.0.1:' + server.address().port;
  }
  report.base = base;
  browser = await chromium.launch({ headless: true });
  for (const width of [1440, 390]) {
    const context = await browser.newContext({ viewport: { width, height: 1000 }, reducedMotion: 'reduce' });
    await context.addInitScript(() => {
      window.__randomEntryIndex = null;
      const original = crypto.getRandomValues.bind(crypto);
      Object.defineProperty(crypto, 'getRandomValues', {
        configurable: true,
        value(values) {
          if (window.__randomEntryIndex !== null && values instanceof Uint32Array && values.length === 1) {
            values[0] = window.__randomEntryIndex;
            return values;
          }
          return original(values);
        },
      });
      Object.defineProperty(navigator, 'clipboard', {
        configurable: true,
        value: { async writeText(value) { window.__randomEntryCopied = value; } },
      });
    });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', (error) => errors.push(error.message));
    const response = await page.goto(base + '/?motion=off#view=home', { waitUntil: 'load' });
    assert.equal(response.status(), 200);
    await page.waitForFunction(() => document.getElementById('surpriseMeHero')?.dataset.surprise18 === 'true');
    const examples = await page.evaluate(() => {
      const data = window.TANGLE_DATA;
      const redirects = data.canonical_redirects || {};
      const pool = data.nodes.filter((node) => node.public_visibility === 'public' && (redirects[node.id] || node.id) === node.id);
      const profiles = new Set((data.profiles || []).map((profile) => profile.node_id));
      const previouslyExcluded = (node) => node.status !== 'accepted'
        || !['profile', 'described'].includes(node.publication_level)
        || ['corpus', 'source', 'evidence', 'claim'].includes(node.entity_type)
        || String(node.description || node.canonical_definition || '').trim().length < 80;
      const used = new Set();
      const select = (kind, predicate) => {
        const node = pool.find((entry) => !used.has(entry.id) && predicate(entry));
        if (!node) throw new Error('No representative entry found for ' + kind);
        used.add(node.id);
        return { kind, id: node.id, label: node.label, index: pool.findIndex((entry) => entry.id === node.id) };
      };
      return [
        select('source', (node) => node.entity_type === 'source'),
        select('corpus', (node) => node.entity_type === 'corpus'),
        select('candidate person', (node) => node.entity_type === 'person' && node.status === 'candidate'),
        select('person without a profile', (node) => node.entity_type === 'person' && !profiles.has(node.id) && previouslyExcluded(node)),
        select('short description', (node) => String(node.description || node.canonical_definition || '').trim().length < 80),
      ];
    });
    for (const example of examples) {
      await page.evaluate((index) => {
        window.__randomEntryIndex = index;
        window.__randomEntryCopied = null;
        location.hash = 'view=home';
      }, example.index);
      const hero = page.locator('#surpriseMeHero');
      await hero.waitFor({ state: 'visible' });
      await hero.hover();
      await hero.focus();
      const href = await hero.getAttribute('href');
      assert.equal(new URLSearchParams(href.replace(/^#/, '')).get('id'), example.id, 'Random destination is not a copyable link');
      await hero.click();
      await page.waitForFunction((id) => new URLSearchParams(location.hash.slice(1)).get('id') === id
        && document.getElementById('entryDrawer')?.classList.contains('open'), example.id);
      const title = page.locator('#drawerBody .entry-head h1');
      assert.equal(await title.textContent(), example.label);
      assert.ok(await title.isVisible());
      await page.locator('#copyEntryLink').click();
      await page.waitForFunction(() => typeof window.__randomEntryCopied === 'string');
      const copied = new URL(await page.evaluate(() => window.__randomEntryCopied));
      const params = new URLSearchParams(copied.hash.slice(1));
      assert.equal(params.get('view'), 'item');
      assert.equal(params.get('id'), example.id);
      assert.equal(params.get('from'), 'home');
      report.checks.push({ width, ...example, href, copied_url: copied.href });
    }
    assert.deepEqual(errors, [], 'Random entries caused browser errors at width ' + width);
    fs.mkdirSync(OUTPUT, { recursive: true });
    await page.screenshot({ path: path.join(OUTPUT, 'entry-' + width + '.png') });
    await context.close();
  }
  report.status = 'passed';
  console.log('Random entry browser checks passed: five previously excluded entries at 1440/390, actual drawer titles, destination links, copied links, and no page errors.');
}

main().catch((error) => {
  report.status = 'failed'; report.error = error.stack;
  console.error(error); process.exitCode = 1;
}).finally(async () => {
  fs.mkdirSync(OUTPUT, { recursive: true });
  fs.writeFileSync(path.join(OUTPUT, process.env.TANGLE_BASE_URL ? 'browser-live.json' : 'browser-local.json'), JSON.stringify(report, null, 2) + '\n');
  if (browser) await browser.close();
  if (server) { server.closeAllConnections?.(); await new Promise((resolve) => server.close(resolve)); }
});
