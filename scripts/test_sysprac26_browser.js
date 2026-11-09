/* SysPrac26 collection, workshop routes, source search, and narrow-screen access. */
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const root = path.resolve(__dirname, '../docs');
const output = path.resolve(__dirname, '../validation/sysprac26-browser');
const report = {status:'running', checks:[], errors:[]};
const collectionPath = '/library/sysprac26/';
const workshops = [
  {anchor:'systemic-consulting', date:'30 September 2026', query:'SysPrac26 systemic consulting', url:'https://antlerboy.com/flawfulconsulting/'},
  {anchor:'relational-public-services', date:'8 October 2026', query:'SysPrac26 relational public services', url:'https://antlerboy.com/relational/'}
];
let server, browser;
fs.mkdirSync(output, {recursive:true});

async function layout(page, label) {
  const size = await page.evaluate(() => ({viewport:innerWidth, document:document.documentElement.scrollWidth, body:document.body.scrollWidth}));
  assert(size.document <= size.viewport + 1 && size.body <= size.viewport + 1, label + ': horizontal overflow ' + JSON.stringify(size));
  const dot = page.getByRole('link', {name:'Open updates', exact:true});
  assert(await dot.isVisible(), label + ': Open updates is visible');
  assert(await dot.getAttribute('href'), label + ': Open updates remains a link');
  const position = await dot.evaluate(element => {
    const rect = element.getBoundingClientRect();
    return {position:getComputedStyle(element).position, right:rect.right, bottom:rect.bottom, width:innerWidth, height:innerHeight};
  });
  assert.equal(position.position, 'fixed', label + ': Open updates remains fixed');
  assert(Math.abs(position.right - position.width) < 3 && Math.abs(position.bottom - position.height) < 3, label + ': Open updates remains bottom-right');
}

async function keyboardFocus(page, link) {
  await page.keyboard.press('Tab');
  await link.focus();
  const focus = await link.evaluate(element => {
    const style = getComputedStyle(element);
    return {active:element === document.activeElement, visible:element.matches(':focus-visible'), outline:style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) > 0};
  });
  assert(focus.active && focus.visible && focus.outline, 'The focused navigation link has a visible keyboard outline');
}

async function libraryReady(page) {
  await page.waitForFunction(() => document.querySelector('#library-collection option[value="SysPrac26"]'));
}

async function sourceCount(page, count) {
  await page.waitForFunction(expected => document.querySelectorAll('.source-card').length === expected, count);
  assert.equal(await page.locator('.source-card').count(), count);
}

async function main() {
  let base = process.env.SYSPRAC_BASE_URL;
  if (!base) {
    server = http.createServer((req, res) => {
      try {
        let file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url, 'http://test').pathname));
        assert(file === root || file.startsWith(root + path.sep));
        if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
        res.setHeader('Content-Type', ({'.html':'text/html; charset=utf-8', '.css':'text/css', '.js':'application/javascript', '.json':'application/json', '.svg':'image/svg+xml', '.png':'image/png'})[path.extname(file)] || 'application/octet-stream');
        res.end(fs.readFileSync(file));
      } catch { res.writeHead(404); res.end(); }
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    base = 'http://127.0.0.1:' + server.address().port;
  }
  base = base.replace(/\/+$/, '');
  report.base = base;
  browser = await chromium.launch(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? {executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH} : {});
  for (const width of [1440, 390]) {
    const context = await browser.newContext({viewport:{width, height:900}, reducedMotion:'reduce'});
    const page = await context.newPage();
    page.setDefaultTimeout(15000);
    page.on('pageerror', error => report.errors.push({width, url:page.url(), message:error.message}));
    const visit = async route => {
      const response = await page.goto(base + route, {waitUntil:'domcontentloaded'});
      assert.equal(response.status(), 200, route);
    };
    try {
      await visit('/library/');
      await libraryReady(page);
      const entrance = page.getByRole('link', {name:'SysPrac26 collection', exact:true}).first();
      assert(await entrance.isVisible(), 'The source library exposes the collection');
      assert.equal(new URL(await entrance.getAttribute('href'), page.url()).pathname, collectionPath);
      assert(await entrance.evaluate(element => Boolean(element.compareDocumentPosition(document.querySelector('#search')) & Node.DOCUMENT_POSITION_FOLLOWING)), 'The collection link appears before the source search');
      await layout(page, 'Source library');
      await keyboardFocus(page, entrance);
      await Promise.all([page.waitForURL(url => url.pathname === collectionPath), page.keyboard.press('Enter')]);
      assert.equal((await page.locator('h1').innerText()).trim(), 'SysPrac26');
      await page.goBack({waitUntil:'domcontentloaded'});
      assert.equal(new URL(page.url()).pathname, '/library/');
      await page.goForward({waitUntil:'domcontentloaded'});
      assert.equal(new URL(page.url()).pathname, collectionPath);
      await layout(page, 'SysPrac26 collection');
      await page.screenshot({path:path.join(output, 'collection-' + width + '.png'), fullPage:true});

      for (const workshop of workshops) {
        assert.equal(await page.locator('#' + workshop.anchor).count(), 1, 'Stable workshop anchor');
        assert.equal((await page.locator('#' + workshop.anchor + ' time').textContent()).trim(), workshop.date, workshop.date);
        assert(await page.locator('a[href="' + workshop.url + '"]').first().isVisible(), workshop.url);
        const anchorLink = page.locator('a[href="#' + workshop.anchor + '"]').first();
        await keyboardFocus(page, anchorLink);
        await Promise.all([page.waitForURL(url => url.hash === '#' + workshop.anchor), page.keyboard.press('Enter')]);
        const target = await page.locator('#' + workshop.anchor).boundingBox();
        assert(target && target.y < 900 && target.y + target.height > 0, 'The workshop anchor brings its target into view');
        await layout(page, workshop.anchor);
        await page.screenshot({path:path.join(output, workshop.anchor + '-' + width + '.png')});
        await page.goBack({waitUntil:'domcontentloaded'});
        assert.equal(new URL(page.url()).hash, '', 'Back restores the collection route');
        await page.goForward({waitUntil:'domcontentloaded'});
        assert.equal(new URL(page.url()).hash, '#' + workshop.anchor, 'Forward restores the workshop fragment');
        await page.goBack({waitUntil:'domcontentloaded'});
      }
      assert(await page.locator('a[href="https://antlerboy.com/flawfulconsulting/september-session/"]').first().isVisible(), 'The actual September session account is linked');

      await page.locator('a[href="/reading/conditions-for-action/"]').first().click();
      await page.waitForURL(url => url.pathname === '/reading/conditions-for-action/');
      await layout(page, 'Existing conference guide');
      const returnLink = page.locator('a[href="' + collectionPath + '"]').first();
      assert(await returnLink.isVisible(), 'The existing conference guide links back to the collection');
      await returnLink.click();
      await page.waitForURL(url => url.pathname === collectionPath);
      assert.equal((await page.locator('h1').innerText()).trim(), 'SysPrac26');

      await visit('/library/');
      await libraryReady(page);
      await page.getByLabel('Collection', {exact:true}).selectOption({label:'SysPrac26'});
      assert.equal(await page.getByLabel('Collection', {exact:true}).inputValue(), 'SysPrac26');
      await sourceCount(page, 8);
      for (const workshop of workshops) assert.equal(await page.locator('.source-card h2 a[href="' + workshop.url + '"]').count(), 1);
      await layout(page, 'SysPrac26 source filter');
      await page.screenshot({path:path.join(output, 'source-filter-' + width + '.png'), fullPage:true});

      for (const workshop of workshops) {
        await visit('/library/?collection=SysPrac26&q=' + encodeURIComponent(workshop.query));
        await libraryReady(page);
        await sourceCount(page, 1);
        assert.equal(await page.getByRole('searchbox', {name:'Search sources'}).inputValue(), workshop.query);
        assert.equal(await page.locator('.source-card h2 a').getAttribute('href'), workshop.url);
        await layout(page, workshop.query);
        await page.screenshot({path:path.join(output, 'search-' + workshop.anchor + '-' + width + '.png'), fullPage:true});
      }
      assert.deepEqual(report.errors, [], 'No JavaScript runtime errors');
      report.checks.push({width, collection:true, workshopAnchors:true, workshopDates:true, publicResources:true, sourceRecords:8, sourceQueries:workshops.map(workshop => ({query:workshop.query, count:1})), libraryEntrance:true, guideReturnLink:true, keyboardFocus:true, clickNavigation:true, browserHistory:true, containment:true, fixedUpdatesControl:true});
    } catch (error) {
      await page.screenshot({path:path.join(output, 'failure-' + width + '.png'), fullPage:true}).catch(() => {});
      throw error;
    } finally {
      await context.close();
    }
  }
  report.status = 'passed';
}
main().catch(error => {report.status = 'failed'; report.error = error.stack; console.error(error); process.exitCode = 1;}).finally(async () => {
  fs.writeFileSync(path.join(output, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  console.log('SysPrac26 browser checks:', JSON.stringify(report));
  if (browser) await browser.close();
  if (server) await new Promise(resolve => server.close(resolve));
});
