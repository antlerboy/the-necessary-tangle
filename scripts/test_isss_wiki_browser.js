/* Inspect the source guide, complete inventory, filters and existing search. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const root = path.resolve(__dirname, '../docs');
const output = path.resolve(__dirname, '../validation/isss-wiki-browser');
let server, browser;
async function main() {
  let base = process.env.UPDATE_BASE_URL;
  if (!base) {
    server = http.createServer((req, res) => {
      try {
        let file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url, 'http://test').pathname));
        assert(file === root || file.startsWith(root + path.sep));
        if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
        res.setHeader('Content-Type', ({'.js':'application/javascript', '.json':'application/json', '.css':'text/css', '.html':'text/html; charset=utf-8'})[path.extname(file)] || 'application/octet-stream');
        res.end(fs.readFileSync(file));
      } catch { res.writeHead(404); res.end(); }
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    base = 'http://127.0.0.1:' + server.address().port;
  }
  fs.mkdirSync(output, {recursive:true});
  browser = await chromium.launch();
  const checked = [];
  for (const width of [1440, 390]) {
    const page = await browser.newPage({viewport:{width, height:900}, reducedMotion:'reduce'});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    const response = await page.goto(base + '/reading/isss-wiki/');
    assert.equal(response.status(), 200);
    await page.locator('#wiki-count').filter({hasText:'of 704 pages match'}).waitFor();
    assert.equal(await page.locator('h1').innerText(), 'Reading the ISSS wiki');
    assert.equal(await page.locator('.questions a').count(), 7);
    assert(await page.getByRole('link', {name:'Open updates', exact:true}).isVisible());
    await page.keyboard.press('Tab');
    assert(await page.evaluate(() => document.activeElement?.tagName === 'A'));
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
    const inventory = await (await page.request.get(base + '/reading/isss-wiki/inventory.json')).json();
    assert.equal(inventory.records.length, 704);
    assert.equal(new Set(inventory.records.map(row => row.page_id)).size, 704);
    assert.equal(inventory.counts.redirects, 202);
    assert.equal(inventory.counts.unfinished_profiles, 194);
    const read = inventory.records.filter(row => row.review.startsWith('Wiki page read in full'));
    assert.equal(read.length, 19);
    await page.locator('#wiki-state').selectOption('read');
    assert((await page.locator('#wiki-count').innerText()).startsWith('19 of 704'));
    await page.locator('#wiki-state').selectOption('unfinished');
    assert((await page.locator('#wiki-count').innerText()).startsWith('194 of 704'));
    await page.locator('#wiki-state').selectOption('redirect');
    assert((await page.locator('#wiki-count').innerText()).startsWith('202 of 704'));
    await page.locator('#wiki-next').click();
    assert.equal(await page.locator('#wiki-page-number').innerText(), 'Page 2 of 9');
    await page.locator('#wiki-state').selectOption('usable');
    await page.locator('#wiki-query').fill('Benjamin Taylor');
    assert.equal(await page.locator('#wiki-results #wiki-page-849').count(), 1);
    assert.equal(await page.locator('#wiki-results #wiki-page-250').count(), 0);
    const href = await page.locator('#wiki-page-849 a').first().getAttribute('href');
    assert(href.startsWith('https://wiki.isss.org/'));
    await page.screenshot({path:path.join(output, 'index-' + width + '.png'), fullPage:false});
    await page.goto(base + '/reading/isss-wiki/?page=250#wiki-index');
    await page.locator('#wiki-page-250').waitFor();
    assert(await page.getByText('Unfinished profile:', {exact:false}).last().isVisible());
    assert.equal(await page.locator('.wiki-card').count(), 1);
    await page.goto(base + '/library/?collection=ISSS%20Wiki&q=Pangaro');
    await page.locator('#results .source-card').first().waitFor();
    assert.equal(await page.locator('#library-collection').inputValue(), 'ISSS Wiki');
    assert((await page.locator('#results').innerText()).includes('ISSS Wiki contributors'));
    for (const route of ['/', '/learning/', '/learning/isss/', '/library/']) {
      await page.goto(base + route);
      assert.equal(await page.locator('#isssWikiGuide a[href="/reading/isss-wiki/"]').count(), 1, route);
    }
    assert.deepEqual(errors, []);
    checked.push({width, passed:true});
    await page.close();
  }
  fs.writeFileSync(path.join(output, 'report.json'), JSON.stringify({base, checked, pages:704, wiki_pages_read:19, passed:true}, null, 2) + '\n');
  console.log('ISSS wiki reader passed: complete inventory, reading states, search, pagination, shareable records, library and learning routes, keyboard access and mobile containment.');
}
main().catch(error => {console.error(error); process.exitCode = 1;}).finally(async () => {
  if (server) await new Promise(resolve => {server.close(resolve); server.closeAllConnections();});
  if (browser) await browser.close();
});
