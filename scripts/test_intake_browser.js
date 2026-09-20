/* Publication gate: profile provenance and containment at desktop/mobile widths. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const root = path.resolve(__dirname, '../docs');
const packet = require('../sources/intake-2026-09-18/entries.json');
const sourceById = new Map(packet.sources.map(source => [source.id, source]));
const output = path.resolve(__dirname, '../validation/intake-browser');
fs.mkdirSync(output, { recursive: true });
let server, browser;
const report = { status: 'running', checks: [], errors: [] };
async function main() {
  server = http.createServer((req, res) => {
    let target = path.resolve(root, '.' + decodeURIComponent(new URL(req.url, 'http://test').pathname));
    if (target !== root && !target.startsWith(root + path.sep)) { res.writeHead(403); return res.end(); }
    try {
      if (fs.statSync(target).isDirectory()) target = path.join(target, 'index.html');
      const mime = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.webp': 'image/webp' };
      res.writeHead(200, { 'Content-Type': mime[path.extname(target)] || 'application/octet-stream' });
      res.end(fs.readFileSync(target));
    } catch { res.writeHead(404); res.end('Not found'); }
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = 'http://127.0.0.1:' + server.address().port;
  browser = await chromium.launch({ headless: true });
  for (const width of [1440, 390]) {
    const context = await browser.newContext({ viewport: { width, height: 900 }, reducedMotion: 'reduce' });
    const page = await context.newPage();
    page.on('pageerror', error => report.errors.push(error.message));
    for (const entry of packet.entries) {
      await page.goto(base + '/#view=item&id=' + entry.id, { waitUntil: 'domcontentloaded' });
      const drawer = page.locator('#entryDrawer');
      await drawer.getByRole('heading', { name: entry.label, exact: true }).waitFor();
      await drawer.getByRole('heading', { name: 'Editorial status', exact: true }).waitFor();
      assert.match(await drawer.innerText(), /Independent specialist review is not recorded/);
      const sourceSection = drawer.locator('.entry-section').filter({ has: page.getByRole('heading', { name: 'Sources', exact: true }) });
      assert(await sourceSection.getByRole('link').count() >= entry.sources.length, entry.id + ': original intake sources were lost');
      for (const sourceId of entry.sources) {
        const source = sourceById.get(sourceId);
        assert(source, entry.id + ': unknown source ' + sourceId);
        assert.equal(await sourceSection.getByRole('link', { name: source.title, exact: true }).count(), 1, entry.id + ': missing original source ' + sourceId);
      }
      await page.waitForFunction(() => {
        const el = document.querySelector('#entryDrawer');
        const rect = el.getBoundingClientRect();
        return rect.left >= -1 && rect.right <= innerWidth + 1;
      });
      assert(await drawer.evaluate(el => el.scrollWidth <= el.clientWidth + 1), entry.id + ': drawer overflow at ' + width);
      assert(await page.getByRole('link', { name: 'Open updates', exact: true }).isVisible());
      report.checks.push({ entry: entry.id, width, provenance: true, containment: true });
    }
    await page.goto(base + '/updates/2026-09-18/', { waitUntil: 'load' });
    assert.equal(await page.getByRole('link', { name: 'Submission and remaining claims', exact: true }).count(), 7);
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
    await page.screenshot({ path: path.join(output, 'update-' + width + '.png'), fullPage: true });
    await context.close();
  }
  assert.deepEqual(report.errors, []);
  report.status = 'passed';
}
main().catch(error => { report.status = 'failed'; report.failure = error.stack; process.exitCode = 1; }).finally(async () => {
  fs.writeFileSync(path.join(output, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  if (browser) await browser.close();
  if (server) await new Promise(resolve => server.close(resolve));
  console.log(JSON.stringify(report));
});
