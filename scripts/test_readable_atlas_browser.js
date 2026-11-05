/* Reader behaviour, static access, keyboard entry, and mobile containment. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const root = path.resolve(__dirname, '../docs');
const output = path.resolve(__dirname, '../validation/readable-atlas-browser');
let server, browser;
async function main() {
  let base = process.env.READABLE_BASE_URL || process.env.PRACTICE_BASE_URL;
  if (!base) {
    server = http.createServer((req, res) => {
      try {
        let file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url, 'http://test').pathname));
        assert(file === root || file.startsWith(root + path.sep));
        if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
        res.setHeader('Content-Type', ({ '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'application/javascript', '.json': 'application/json' })[path.extname(file)] || 'application/octet-stream');
        res.end(fs.readFileSync(file));
      } catch { res.writeHead(404); res.end(); }
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    base = 'http://127.0.0.1:' + server.address().port;
  }
  fs.mkdirSync(output, { recursive: true });
  browser = await chromium.launch(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH } : {});
  const manifest = JSON.parse(fs.readFileSync(path.join(root, 'entries/manifest.json')));
  const entryRoute = '/entries/concept_structural_coupling/';
  const journeyRoute = manifest.routes.find(r => r.startsWith('/journeys/') && r !== '/journeys/');
  const checked = [];
  for (const width of [1440, 390]) {
    const context = await browser.newContext({ viewport: { width, height: 900 }, javaScriptEnabled: false });
    const page = await context.newPage();
    for (const route of ['/entries/', '/journeys/', '/stewardship/', entryRoute, journeyRoute]) {
      const response = await page.goto(base + route);
      assert.equal(response.status(), 200, route);
      assert.equal(await page.locator('h1').count(), 1, route);
      assert(await page.getByRole('link', { name: 'Open updates', exact: true }).isVisible());
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'Horizontal overflow: ' + route + ' at ' + width);
      await page.keyboard.press('Tab');
      assert.equal(await page.evaluate(() => document.activeElement.textContent), 'Skip to content');
      if (route === entryRoute) {
        assert(await page.getByRole('heading', { name: 'Sources and passage locators', exact: true }).isVisible());
        assert(await page.getByRole('link', { name: 'Open the interactive entry', exact: true }).isVisible());
        const downloadUrl = new URL(await page.getByRole('link', { name: 'Download the sourced record (JSON)', exact: true }).getAttribute('href'), page.url());
        const data = await (await context.request.get(downloadUrl.href)).json();
        assert.equal(data.entry.id, 'concept_structural_coupling');
        assert(data.citation.includes('/entries/concept_structural_coupling/'));
        await page.screenshot({ path: path.join(output, `entry-${width}.png`) });
      }
      checked.push({ route, width, javaScript: false });
    }
    await page.goto(base + '/');
    for (const name of ['Check a transformation claim', 'Practise a systems method', 'Read the entries and sources']) assert(await page.getByRole('link', { name, exact: true }).isVisible());
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'Home-route overflow at ' + width);
    await page.locator('#practical-routes').scrollIntoViewIfNeeded();
    await page.screenshot({ path: path.join(output, `home-routes-${width}.png`) });
    await context.close();
  }
  const page = await browser.newPage();
  await page.goto(base + '/#view=item&id=concept_structural_coupling');
  await page.getByRole('link', { name: 'Read or cite this entry', exact: true }).waitFor();
  assert.equal(await page.getByRole('link', { name: 'Read or cite this entry', exact: true }).getAttribute('href'), entryRoute);
  await page.goto(base + '/#view=journeys&id=' + encodeURIComponent(journeyRoute.split('/')[2]) + '&step=0');
  await page.getByRole('link', { name: 'Read the whole journey', exact: true }).waitFor();
  assert.equal(await page.getByRole('link', { name: 'Read the whole journey', exact: true }).getAttribute('href'), journeyRoute);
  fs.writeFileSync(path.join(output, 'report.json'), JSON.stringify({ release: manifest.release, entry_count: manifest.entry_count, journey_count: manifest.journey_count, checked }, null, 2));
  console.log('Readable atlas browser checks passed: static access, sourced download, keyboard entry, mobile containment, practical routes, and interactive link.');
}
main().catch(error => { console.error(error); process.exitCode = 1; }).finally(async () => {
  if (browser) await browser.close();
  if (server) {
    server.closeAllConnections?.();
    await new Promise(resolve => server.close(resolve));
  }
});
