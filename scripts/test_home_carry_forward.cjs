/* Verify the two repeatedly reported homepage regressions in the final build. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const root = path.resolve(__dirname, '../docs');
const output = path.resolve(__dirname, '../validation/home-carry-forward');
fs.mkdirSync(output, { recursive: true });
let server, browser;
const report = { status: 'running', checks: [] };

async function main() {
  let base = process.env.TANGLE_BASE_URL;
  if (!base) {
    server = http.createServer((req, res) => {
      let file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url, 'http://test').pathname));
      if (file !== root && !file.startsWith(root + path.sep)) { res.writeHead(403); return res.end(); }
      try {
        if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
        const mime = { '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json', '.webp': 'image/webp' };
        res.setHeader('Content-Type', mime[path.extname(file)] || 'application/octet-stream');
        res.end(fs.readFileSync(file));
      } catch { res.writeHead(404); res.end(); }
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    base = 'http://127.0.0.1:' + server.address().port;
  }
  browser = await chromium.launch({ headless: true });
  for (const width of [1440, 390]) {
    const context = await browser.newContext({ viewport: { width, height: 1000 }, reducedMotion: 'no-preference' });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(base + '/?mark=circular-impossibility', { waitUntil: 'load' });
    const mark = page.locator('[data-living-mark]');
    await page.waitForFunction(() => document.querySelector('[data-living-mark]')?.dataset.motionState === 'playing');
    assert.equal(await mark.locator('img[data-mark-format="animated-webp"]').count(), 1);
    const first = await mark.screenshot();
    let changed = false;
    for (let frame = 0; frame < 5 && !changed; frame++) {
      await page.waitForTimeout(250);
      changed = !first.equals(await mark.screenshot());
    }
    assert(changed, 'The rendered mark must visibly change frames, not merely carry an animated label');
    const original = await mark.getAttribute('data-mark-id');
    await mark.click();
    await page.waitForFunction(previous => {
      const mark = document.querySelector('[data-living-mark]');
      return mark.dataset.markId !== previous && mark.dataset.motionState === 'playing';
    }, original);
    assert.equal(await mark.locator('img[data-mark-format="animated-webp"]').count(), 1);
    await mark.focus();
    const beforeKey = await mark.getAttribute('data-mark-id');
    await page.keyboard.press('Enter');
    await page.waitForFunction(previous => document.querySelector('[data-living-mark]').dataset.markId !== previous, beforeKey);
    await mark.dblclick();
    await page.waitForFunction(() => document.fullscreenElement === document.querySelector('[data-living-mark]'));
    await page.keyboard.press('Escape');
    await page.waitForFunction(() => !document.fullscreenElement);
    let previous = await mark.getAttribute('data-mark-id');
    for (let visit = 0; visit < 3; visit++) {
      await page.goto(base + '/', { waitUntil: 'load' });
      await page.waitForFunction(() => document.querySelector('[data-living-mark]')?.dataset.motionState === 'playing');
      const selected = await mark.getAttribute('data-mark-id');
      assert.notEqual(selected, previous, 'A reload must choose another animated mark');
      assert.equal(await mark.locator('img[data-mark-format="animated-webp"]').count(), 1);
      previous = selected;
    }
    const counts = page.locator('#homeMetrics');
    assert.equal(await page.locator('#homeMetrics').count(), 1);
    assert.equal(await counts.locator('.metric').count(), 4);
    assert(await counts.evaluate(element => element.parentElement.classList.contains('atlas-finder') && element.previousElementSibling?.textContent === 'Inside the atlas'));
    if (width > 800) {
      const finder = await page.locator('.atlas-finder').boundingBox();
      const example = await page.locator('.alarm-feature').boundingBox();
      assert(finder.x >= example.x + example.width, 'Counts belong in the right-hand column');
    }
    assert(await page.getByRole('link', { name: 'Open updates', exact: true }).isVisible());
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 2));
    await page.screenshot({ path: path.join(output, 'home-' + width + '.png') });
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.waitForFunction(() => document.querySelector('[data-living-mark]')?.dataset.motionState === 'paused');
    assert.equal(await mark.locator('img[data-mark-format="still"]').count(), 1);
    await page.emulateMedia({ reducedMotion: 'no-preference' });
    await page.waitForFunction(() => document.querySelector('[data-living-mark]')?.dataset.motionState === 'playing');
    assert.deepEqual(errors, []);
    report.checks.push({ width, actualAnimatedFrames: true, animatedReloads: 3, click: true, keyboard: true, fullScreenAndEscape: true, countsImmediatelyBelowHeading: true, reducedMotion: true, overflow: false });
    await context.close();
  }
  const plain = await browser.newContext({ javaScriptEnabled: false });
  const page = await plain.newPage();
  await page.goto(base + '/');
  assert.equal(await page.locator('.atlas-finder #homeMetrics .metric').count(), 4);
  await plain.close();
  report.status = 'passed';
}
main().catch(error => { report.status = 'failed'; report.error = error.stack; process.exitCode = 1; }).finally(async () => {
  fs.writeFileSync(path.join(output, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  if (browser) await browser.close();
  if (server) await new Promise(resolve => server.close(resolve));
  console.log(JSON.stringify(report));
});
