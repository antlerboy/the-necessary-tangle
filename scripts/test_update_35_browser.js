/* Read-only checks of source reading, atlas entries, and question-led routes. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const root = path.resolve(__dirname, '../docs');
const output = path.resolve(__dirname, '../validation/update-35-browser');
let server, browser;

async function main() {
  let base = process.env.UPDATE_BASE_URL;
  if (!base) {
    server = http.createServer((req, res) => {
      try {
        let file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url, 'http://test').pathname));
        assert(file === root || file.startsWith(root + path.sep));
        if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
        res.setHeader('Content-Type', ({ '.js': 'application/javascript', '.json': 'application/json', '.css': 'text/css', '.html': 'text/html; charset=utf-8' })[path.extname(file)] || 'application/octet-stream');
        res.end(fs.readFileSync(file));
      } catch { res.writeHead(404); res.end(); }
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    base = 'http://127.0.0.1:' + server.address().port;
  }
  fs.mkdirSync(output, { recursive: true });
  browser = await chromium.launch();
  const request = await browser.newContext();
  const response = await request.request.get(base + '/assets/public-data.json');
  assert.equal(response.status(), 200);
  const data = await response.json();
  assert.equal(data.meta.release, '0.35');
  const journeys = data.journeys.filter(row => row.connection_pass === 'depth_20261029');
  const profiles = data.profiles.filter(row => row.connection_pass === 'depth_20261029');
  assert(profiles.length > 0);
  await request.close();
  const checked = [];
  for (const width of [1440, 390]) {
    const page = await browser.newPage({ viewport: { width, height: 900 }, reducedMotion: 'reduce' });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    for (const route of ['/reading/connections/', '/updates/2026-10-29/']) {
      const result = await page.goto(base + route);
      assert.equal(result.status(), 200, route);
      assert.equal(await page.locator('h1').count(), 1, route);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'Overflow ' + route + ' ' + width);
      assert(await page.getByRole('link', { name: 'Open updates', exact: true }).isVisible());
      await page.keyboard.press('Tab');
      assert(await page.evaluate(() => document.activeElement?.tagName === 'A'), 'First keyboard destination must be a link');
      if (route === '/reading/connections/') {
        for (const id of ['regulation', 'learning', 'transduction']) assert.equal(await page.locator('#' + id).count(), 1);
        assert(await page.locator('a[href^="http"]').count() > 0, 'Sources must be linked');
        assert(await page.locator('a[href^="/#view=item"]').count() > 0, 'Reading must connect to atlas entries');
      }
      await page.screenshot({ path: path.join(output, route.includes('/reading/') ? `reading-${width}.png` : `update-${width}.png`), fullPage: true });
      checked.push({ route, width });
    }
    await page.goto(base + '/');
    assert.equal(await page.locator('#releaseBadge').innerText(), 'Release 0.35');
    assert(await page.locator('a[href^="/reading/connections/"]').count() > 0, 'Home needs a route to the deeper reading');
    for (const journey of journeys) {
      await page.goto(base + '/#view=journeys&id=' + encodeURIComponent(journey.id) + '&step=0');
      await page.locator('#journeyRunner h2').filter({ hasText: journey.title }).waitFor();
      assert.equal(await page.locator('#journeyRunner .step-card a').first().getAttribute('data-id'), journey.steps[0].node_id);
      if (journey.steps.length > 1) {
        await page.locator('#journeyNext').click();
        assert.equal(await page.locator('#journeyRunner .step-card a').first().getAttribute('data-id'), journey.steps[1].node_id);
        assert(new URL(page.url()).hash.includes('step=1'));
      }
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'Journey overflow ' + journey.id + ' ' + width);
    }
    for (const profile of profiles) {
      await page.goto(base + '/#view=item&id=' + encodeURIComponent(profile.node_id));
      const node = data.nodes.find(row => row.id === profile.node_id);
      await page.getByRole('heading', { name: node.label, exact: true }).first().waitFor();
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'Entry overflow ' + profile.node_id + ' ' + width);
    }
    assert.deepEqual(errors, [], 'Browser errors at ' + width);
    await page.close();
  }
  fs.writeFileSync(path.join(output, 'report.json'), JSON.stringify({ release: '0.35', base, routes: checked, journeys: journeys.map(row => row.id), profiles: profiles.map(row => row.node_id), passed: true }, null, 2) + '\n');
  console.log('0.35 browser passed: source routes, linked reading, keyboard entry, atlas profiles, journey progression, desktop/mobile containment, and protected updates control.');
}
main().catch(error => { console.error(error); process.exitCode = 1; }).finally(async () => {
  if (server) await new Promise(resolve => {
    server.close(resolve);
    // Browser HTTP keep-alive sockets must not hold a completed test open.
    server.closeAllConnections();
  });
  if (browser) await browser.close();
});
