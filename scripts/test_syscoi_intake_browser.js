/* Public resource route, search, and narrow-screen containment. */
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const root = path.resolve(__dirname, '../docs');
const output = path.resolve(__dirname, '../validation/syscoi-intake-browser');
let server, browser;
async function main() {
  let base = process.env.SYSCOI_BASE_URL;
  if (!base) {
    server = http.createServer((req, res) => {
      try {
        let file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url, 'http://test').pathname));
        assert(file === root || file.startsWith(root + path.sep));
        if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
        res.setHeader('Content-Type', ({'.html':'text/html; charset=utf-8', '.css':'text/css', '.js':'application/javascript', '.json':'application/json'})[path.extname(file)] || 'application/octet-stream');
        res.end(fs.readFileSync(file));
      } catch { res.writeHead(404); res.end(); }
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    base = 'http://127.0.0.1:' + server.address().port;
  }
  fs.mkdirSync(output, {recursive:true});
  browser = await chromium.launch(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? {executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH} : {});
  const checks = [];
  for (const width of [1440, 390]) {
    const context = await browser.newContext({viewport:{width,height:900}});
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    const response = await page.goto(base + '/library/syscoi/');
    assert.equal(response.status(), 200);
    assert.equal(await page.locator('h1').textContent(), 'SysCoI reading');
    const data = await (await context.request.get(base + '/library/syscoi/intake.json')).json();
    assert.equal(await page.locator('.syscoi-resource').count(), data.resource_count);
    for (const post of data.posts) assert.equal(await page.locator('#post-' + post.post_id).count(), 1);
    assert(await page.getByRole('link', {name:'Open updates',exact:true}).isVisible());
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
    await page.screenshot({path:path.join(output, 'collection-' + width + '.png')});
    await page.goto(base + '/library/?q=Ladder%20of%20Abstraction', {waitUntil:'networkidle'});
    assert.equal(await page.locator('.source-card').count(), 1);
    assert((await page.locator('.source-card').textContent()).includes('Bret Victor'));
    assert(await page.getByRole('link', {name:'New reading from SysCoI',exact:true}).isVisible());
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
    assert.deepEqual(errors, []);
    checks.push({width, resource_count:data.resource_count, anchors:true, sourceSearch:true, containment:true, feedbackControl:true});
    await context.close();
  }
  fs.writeFileSync(path.join(output, 'report.json'), JSON.stringify({status:'passed', base, checks}, null, 2) + '\n');
  console.log('SysCoI resource browser checks passed:', JSON.stringify(checks));
}
main().catch(error => {console.error(error); process.exitCode = 1;}).finally(async () => {if(browser) await browser.close(); if(server) server.close();});
