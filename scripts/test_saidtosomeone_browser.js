/* Reader checks against the built candidate, or the deployed site via SAID_BASE_URL. */
const {chromium} = require('playwright');
const assert = require('node:assert/strict'), fs = require('node:fs'), path = require('node:path'), http = require('node:http');
const root = path.resolve(__dirname, '../docs');
let server, browser;
async function main() {
  let base = process.env.SAID_BASE_URL;
  if (!base) {
    server = http.createServer((req, res) => {
      try {
        let file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url, 'http://test').pathname));
        assert(file === root || file.startsWith(root + path.sep));
        if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
        res.setHeader('Content-Type', ({'.html':'text/html; charset=utf-8', '.css':'text/css', '.js':'application/javascript', '.json':'application/json', '.webp':'image/webp'})[path.extname(file)] || 'application/octet-stream');
        res.end(fs.readFileSync(file));
      } catch { res.writeHead(404); res.end(); }
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    base = 'http://127.0.0.1:' + server.address().port;
  }
  browser = await chromium.launch();
  for (const width of [375, 768, 1440]) {
    const page = await browser.newPage({viewport:{width, height:900}, reducedMotion:'no-preference'});
    const manifest = page.waitForResponse(response => response.url().includes('/assets/living-marks/playback-manifest.json') && response.status() === 200);
    assert.equal((await page.goto(base + '/saidtosomeone/?mark=impossible-tangle')).status(), 200);
    const marks = (await (await manifest).json()).marks;
    const host = page.locator('[data-living-mark]');
    await page.waitForFunction(() => document.querySelector('[data-living-mark]')?.dataset.motionState === 'playing');
    assert.equal(await host.getAttribute('data-mark-id'), 'impossible-tangle');
    assert.equal(await host.locator('img').getAttribute('data-mark-format'), 'animated-webp');
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `Overflow at ${width}`);
    await page.getByRole('button', {name:'Pause animation'}).click();
    await page.waitForFunction(() => document.querySelector('[data-living-mark]')?.dataset.motionState === 'paused');
    assert.equal(await host.locator('img').getAttribute('data-mark-format'), 'still');
    await page.getByRole('button', {name:'Animate', exact:true}).click();
    await page.waitForFunction(() => document.querySelector('[data-living-mark]')?.dataset.motionState === 'playing');
    async function verifySelectedImage() {
      const id = await host.getAttribute('data-mark-id');
      const mark = marks.find(item => item.id === id);
      assert(mark, 'Selected mark must be in manifest');
      const candidates = [mark.src, mark.poster, mark.animated_src].filter(Boolean).map(src => new URL('/' + src.replace(/^\/+/, ''), base).href);
      await page.waitForFunction(urls => {
        const image = document.querySelector('[data-living-mark] img');
        return image && image.complete && image.naturalWidth > 0 && urls.includes(image.src);
      }, candidates);
    }
    let previous = await host.getAttribute('data-mark-id');
    await page.getByRole('button', {name:'Change motif'}).click();
    assert.notEqual(await host.getAttribute('data-mark-id'), previous);
    await verifySelectedImage();
    previous = await host.getAttribute('data-mark-id');
    await host.focus(); await page.keyboard.press('Enter');
    assert.notEqual(await host.getAttribute('data-mark-id'), previous);
    await verifySelectedImage();
    previous = await host.getAttribute('data-mark-id');
    await host.focus(); await page.keyboard.press('Space');
    assert.notEqual(await host.getAttribute('data-mark-id'), previous);
    await verifySelectedImage();
    const entries = page.locator('.maxim[data-evidence]');
    const total = await entries.count(); assert(total > 1);
    await page.locator('#maxim-search').fill('observer');
    let visible = await entries.filter({visible:true}).count();
    assert(visible > 0 && visible < total, 'Search should narrow the register');
    await page.locator('#maxim-search').fill('');
    await page.locator('#evidence-filter').selectOption('reported');
    visible = await entries.filter({visible:true}).count();
    assert(visible > 0 && visible < total, 'Evidence filter should narrow the register');
    assert.equal(await page.locator('.maxim[data-evidence]:visible:not([data-evidence="reported"])').count(), 0);
    const hiddenId = await page.locator('.maxim[hidden][id]').first().getAttribute('id');
    assert(hiddenId);
    await page.evaluate(id => { location.hash = id; }, hiddenId);
    await page.waitForFunction(id => !document.getElementById(id).hidden, hiddenId);
    assert.equal(await page.locator('#evidence-filter').inputValue(), 'all');
    await page.close();
  }
  const page = await browser.newPage({reducedMotion:'reduce'});
  await page.goto(base + '/saidtosomeone/?mark=impossible-tangle');
  await page.waitForFunction(() => document.querySelector('[data-living-mark]')?.dataset.motionState === 'paused');
  assert.equal(await page.locator('[data-living-mark] img').getAttribute('data-mark-format'), 'still');
  await page.getByRole('button', {name:'Animate', exact:true}).click();
  await page.waitForFunction(() => document.querySelector('[data-living-mark]')?.dataset.motionState === 'playing');
  assert.equal(await page.locator('[data-living-mark] img').getAttribute('data-mark-format'), 'animated-webp');
  await page.close();
  console.log('Said to someone browser passed: living mark, reduced motion, register, hash reveal and three viewport widths.');
}
main().catch(error => { console.error(error); process.exitCode = 1; }).finally(async () => { if (browser) await browser.close(); if (server) await new Promise(resolve => server.close(resolve)); });
