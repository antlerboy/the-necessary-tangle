const {chromium}=require('playwright');
const assert=require('node:assert/strict'),http=require('node:http'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../docs'),out=path.resolve(__dirname,'../validation/adventure-42-browser');
(async()=>{
  let browser,server;const report={reader_release:'0.42',widths:[],checks:[],passed:false};
  try {
    let base=(process.env.ADVENTURE_BASE_URL||'').replace(/\/$/,'');
    if(!base){server=http.createServer((req,res)=>{try{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname));assert(f.startsWith(root+path.sep)||f===root);if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.json':'application/json','.js':'application/javascript','.css':'text/css','.svg':'image/svg+xml'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});await new Promise(r=>server.listen(0,'127.0.0.1',r));base='http://127.0.0.1:'+server.address().port;}
    report.base=base;fs.mkdirSync(out,{recursive:true});
    browser=await chromium.launch(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH}:{});
    for(const width of [1440,390,320]){
      const ctx=await browser.newContext({viewport:{width,height:960},reducedMotion:'reduce'}),page=await ctx.newPage(),errors=[];
      page.on('pageerror',e=>errors.push(e.message));
      assert.equal((await page.goto(base+'/42/')).status(),200);await page.waitForFunction(()=>!document.getElementById('command').disabled);
      assert(await page.getByText('A>TANGLE',{exact:true}).count());
      assert(await page.getByRole('heading',{name:'An adventure in the Tangle',exact:true}).isVisible());
      const cmd=async c=>{await page.getByRole('textbox',{name:'Adventure command'}).fill(c);await page.getByRole('textbox',{name:'Adventure command'}).press('Enter');};
      const last=()=>page.locator('#transcript .entry').last().innerText();
      await cmd('LAUNCH');assert((await last()).includes('still needs'));
      for(const c of ['N','DISTURB','SET 1','WAIT','TAKE COMPASS','S','S','OPEN INLET','OPEN DRAIN','WAIT','WAIT','TAKE LAMP','N','E','FIND EMERGENCE','OPEN 1','PRINT CHART','SAVE'])await cmd(c);
      const saved=await page.evaluate(()=>JSON.parse(localStorage.getItem('tnt42.save.v1')));assert.equal(saved.room,'library');assert(saved.inventory.includes('chart'));
      await cmd('FOLLOW');await cmd('FOLLOW 1');assert(await page.locator('#passage').isVisible());assert((await page.locator('#passage').innerText()).includes('RECORDED CONNECTION'));
      await cmd('RESTORE');assert.equal(await page.locator('#location').innerText(),'The library of actual passages');
      for(const c of ['W','LAUNCH','READ CHART'])await cmd(c);
      assert.equal(await page.locator('#location').innerText(),'A passage entered in the log');
      assert(await page.locator('#transcript .entry a').count());
      await page.reload();await page.waitForFunction(()=>!document.getElementById('command').disabled);
      assert.equal(await page.locator('#location').innerText(),'A passage entered in the log');
      await cmd('RESTORE');assert.equal(await page.locator('#location').innerText(),'The library of actual passages');
      await cmd('IMPROBABILITY');const first=await page.locator('#record h2').innerText();await cmd('IMPROBABILITY');assert.notEqual(await page.locator('#record h2').innerText(),first);
      await cmd('READ ATLAS');const link=page.locator('#record a.atlas-link');assert((await link.getAttribute('href')).startsWith('/'));
      const target=new URL(await link.getAttribute('href'),base);assert.equal((await ctx.request.get(target.href.split('#')[0])).status(),200);
      await page.getByRole('textbox',{name:'Adventure command'}).press('ArrowUp');assert.equal(await page.getByRole('textbox',{name:'Adventure command'}).inputValue(),'READ ATLAS');
      await cmd('<img src=x onerror=alert(1)>');assert.equal(await page.locator('img[src=x]').count(),0);
      const exit=page.locator('#exits a').first();const href=await exit.getAttribute('href');assert(href.includes('?place='));
      const newPagePromise=ctx.waitForEvent('page');await exit.click({modifiers:['Control']});const other=await newPagePromise;await other.waitForURL(url=>new URL(url).searchParams.has('place'));await other.waitForFunction(()=>!document.getElementById('command').disabled);assert.equal(new URL(other.url()).searchParams.get('place'),new URL(href,base).searchParams.get('place'));await other.close();
      await exit.click();const moved=await page.locator('#location').innerText();assert.notEqual(moved,'The library of actual passages');await page.goBack();assert.equal(await page.locator('#location').innerText(),'The library of actual passages');
      const dot=page.getByRole('link',{name:'Open updates',exact:true});assert(await dot.isVisible());const pos=await dot.evaluate(e=>{const r=e.getBoundingClientRect();return {position:getComputedStyle(e).position,right:r.right,bottom:r.bottom};});assert.equal(pos.position,'fixed');assert(Math.abs(pos.right-width)<2&&Math.abs(pos.bottom-960)<2);
      for(const palette of ['amber','paper','green']){await page.getByLabel('Display',{exact:true}).selectOption(palette);assert.equal(await page.locator('html').getAttribute('data-palette'),palette);}
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'mobile overflow');
      await page.screenshot({path:path.join(out,'adventure-'+width+'.png'),fullPage:true});
      assert.deepEqual(errors,[]);report.widths.push(width);await ctx.close();
    }
    const broken=await browser.newContext();await broken.addInitScript(()=>localStorage.setItem('tnt42.save.v1','{broken'));
    let page=await broken.newPage();await page.goto(base+'/42/');await page.waitForFunction(()=>!document.getElementById('command').disabled);await page.getByRole('button',{name:'Restore',exact:true}).click();assert((await page.locator('#transcript').innerText()).includes('No valid manual checkpoint'));await broken.close();
    const blocked=await browser.newContext();await blocked.addInitScript(()=>{Storage.prototype.setItem=function(){throw new DOMException('Storage unavailable','QuotaExceededError');};});
    page=await blocked.newPage();await page.goto(base+'/42/');await page.waitForFunction(()=>!document.getElementById('command').disabled);await page.getByRole('button',{name:'Save',exact:true}).click();assert((await page.locator('#storageStatus').innerText()).includes('unavailable'));assert((await page.locator('#transcript').innerText()).includes('could not be saved'));await blocked.close();
    const home=await browser.newPage();await home.goto(base+'/');assert(await home.locator('#adventure-42 a[href="/42/"]').count());await home.waitForFunction(()=>document.getElementById('releaseBadge').textContent==='Release 0.42');await home.goto(base+'/updates/2026-11-15-42/');assert(await home.getByRole('heading',{name:'An adventure in the Tangle',exact:true}).count());
    const manifest=await(await home.request.get(base+'/42/manifest.json')).json();assert.equal(manifest.reader_release,'0.42');assert(manifest.public_entries>1000);
    report.checks=['complete expedition','blocked launch','source-linked atlas passage','manual checkpoint and reload','corrupt checkpoint','unavailable storage','whole-atlas serendipity','real links and modified-click','history','keyboard command recall','palette','mobile containment','fixed updates dot','home reader release'];report.passed=true;
    console.log('Adventure browser passed: 1440, 390, and 320px; puzzles, atlas passages, save/reload, corrupt and blocked storage, keyboard, links, history, and home release.');
  } finally {fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');if(browser)await browser.close();if(server)await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exitCode=1;});
