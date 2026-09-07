/* Browser regression tests for the built or deployed practice pages. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const http=require('node:http');
const {spawnSync}=require('node:child_process');
const root=path.resolve(__dirname,'../docs');
const pack=JSON.parse(fs.readFileSync(path.join(root,'systems-thinking/practice/assets/pack.json'),'utf8'));
const output=path.resolve(__dirname,'../validation/practice-browser');fs.mkdirSync(output,{recursive:true});
let server,browser;
const errors=[];
const report={status:'running',pages:0,questions:0,checks:[],base:process.env.PRACTICE_BASE_URL||'local build'};
async function main(){
 let base=process.env.PRACTICE_BASE_URL;
 if(!base){
  server=http.createServer((req,res)=>{let pathname=decodeURIComponent(new URL(req.url,'http://test').pathname);let target=path.resolve(root,'.'+pathname);if(!target.startsWith(root+path.sep)&&target!==root){res.writeHead(403);return res.end();}try{if(fs.statSync(target).isDirectory())target=path.join(target,'index.html');const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.png':'image/png','.zip':'application/zip'};res.writeHead(200,{'Content-Type':mime[path.extname(target)]||'application/octet-stream','Cache-Control':'no-store'});res.end(fs.readFileSync(target));}catch(_){res.writeHead(404);res.end('Not found');}});
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));base='http://127.0.0.1:'+server.address().port;
 }
 base=base.replace(/\/$/,'');const start=base+'/systems-thinking/practice/';
 browser=await chromium.launch({headless:true});
 const context=await browser.newContext({viewport:{width:1365,height:900},acceptDownloads:true});
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto(start,{waitUntil:'networkidle'});
 assert.equal(await page.locator('[data-lab-card]').count(),26);
 await page.locator('[data-filter]').fill('SSM');assert.equal(await page.locator('[data-lab-card]:visible').count(),1);
 await page.locator('[data-filter]').fill('unlikely-no-match');assert.equal(await page.locator('[data-lab-card]:visible').count(),0);
 await page.locator('[data-filter]').fill('');assert.equal(await page.locator('[data-lab-card]:visible').count(),26);
 await page.screenshot({path:path.join(output,'home-desktop.png'),fullPage:true});report.checks.push('method search');
 for(const lab of pack.labs){
  const response=await page.goto(start+lab.id+'/',{waitUntil:'load'});assert.equal(response.status(),200,lab.id);
  assert.equal(await page.locator('h1').count(),1);assert(await page.locator('h1').innerText());
  assert.equal(await page.locator('[data-check]').count(),lab.checks.length);
  const unlabelled=await page.locator('input,textarea,select').evaluateAll(els=>els.filter(el=>!el.closest('label')&&!el.getAttribute('aria-label')&&!document.querySelector('label[for="'+el.id+'"]')).length);
  assert.equal(unlabelled,0,lab.id+' input names');
  for(let i=0;i<lab.checks.length;i++){
   const check=page.locator('[data-check]').nth(i),q=lab.checks[i];
   if(i===0){await check.locator('button').click();assert.match(await check.locator('[data-result]').innerText(),/Choose an answer/);}
   await check.locator('input[type=radio]').nth((q.correct+1)%q.options.length).check();await check.locator('button').click();assert.equal(await check.locator('[data-result]').getAttribute('data-outcome'),'revise');
   await check.locator('input[type=radio]').nth(q.correct).check();await check.locator('button').click();assert.equal(await check.locator('[data-result]').getAttribute('data-outcome'),'correct');report.questions++;
  }
  const answer=page.locator('.steps .answer').first();assert.equal(await answer.getAttribute('open'),null);await answer.locator('summary').click();assert(await answer.locator('p').first().isVisible());
  report.pages++;
 }
 report.checks.push('all question wrong/right/missing states','all worked-answer disclosure controls','labelled inputs');
 for(const lab of ['system-dynamics','interactive-management','viable-system-model']){
  await page.goto(start+lab+'/',{waitUntil:'load'});const form=page.locator('[data-model-check]');
  if(lab==='interactive-management'){await form.locator('button').click();assert.equal(await form.locator('[data-model-result]').getAttribute('data-outcome'),'revise');}
  const fields=form.locator('[data-expected]');
  for(let i=0;i<await fields.count();i++){const field=fields.nth(i);const value=await field.getAttribute('data-expected');const tag=await field.evaluate(el=>el.tagName);const type=await field.getAttribute('type');if(type==='checkbox'){if(value==='1')await field.check();else await field.uncheck();}else if(tag==='SELECT')await field.selectOption(value);else await field.fill(value);}
  await form.locator('button').click();assert.equal(await form.locator('[data-model-result]').getAttribute('data-outcome'),'correct');
 }
 report.checks.push('queue input checker','25-cell reachability checker','VSM function checker');
 await page.goto(start+'soft-systems/',{waitUntil:'load'});
 await page.locator('textarea[name="step-1"]').fill('My first model: residents and repair completion. <script>not executed</script>');
 await page.locator('[data-save]').click();await page.reload({waitUntil:'load'});assert.match(await page.locator('textarea[name="step-1"]').inputValue(),/My first model/);
 const downloadPromise=page.waitForEvent('download');await page.locator('[data-export]').click();const download=await downloadPromise;await download.saveAs(path.join(output,'attempt.md'));assert.match(fs.readFileSync(path.join(output,'attempt.md'),'utf8'),/My first model/);
 page.once('dialog',dialog=>dialog.accept());await page.locator('[data-reset]').click();assert.equal(await page.locator('textarea[name="step-1"]').inputValue(),'');
 report.checks.push('save and restore','attempt export','confirmed reset');
 for(const route of ['coverage/','resources/','worksheets/','answers/','tutor-notes/']){const response=await page.goto(start+route);assert.equal(response.status(),200);report.pages++;}
 const zipResponse=await context.request.get(start+'downloads/systems-methods-practice.zip');assert.equal(zipResponse.status(),200);assert((await zipResponse.body()).length>30000);
 report.checks.push('download archive');
 await page.setViewportSize({width:390,height:844});
 for(const route of ['',...pack.labs.map(l=>l.id+'/'),'coverage/','resources/','tutor-notes/']){
  await page.goto(start+route,{waitUntil:'load'});
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+2),'horizontal overflow: '+route);
 }
 await page.goto(start);await page.screenshot({path:path.join(output,'home-mobile.png'),fullPage:true});
 await page.goto(start+'system-dynamics/');await page.screenshot({path:path.join(output,'system-dynamics-mobile.png'),fullPage:true});
 report.checks.push('390px layout across practice pages');
 const nojs=await browser.newContext({javaScriptEnabled:false});const plain=await nojs.newPage();await plain.goto(start+'soft-systems/');assert(await plain.locator('#case').isVisible());const details=plain.locator('.steps details').first();await details.locator('summary').click();assert(await details.locator('p').first().isVisible());await nojs.close();report.checks.push('no-script case and answer access');
 await page.setViewportSize({width:1365,height:900});await page.goto(base+'/systems-thinking/');assert(await page.locator('a[href="/systems-thinking/practice/"]').count()>0);
 await page.goto(base+'/');assert(await page.locator('[data-practice-nav]').count()>0);assert(await page.locator('#systemsPracticeCallout').count()>0);
 // Data-level and live DOM integration for an existing method.
 const data=JSON.parse(fs.readFileSync(path.join(root,'assets/public-data.json'),'utf8'));const mapping=data.practice_pack.mappings.find(m=>m.lab_id==='soft-systems');
 assert(mapping.method_node_ids.length,'SSM must be linked to an existing method');
 await page.goto(base+'/#view=item&id='+mapping.method_node_ids[0]);
 await page.waitForSelector('[data-practice-for]',{state:'attached',timeout:20000});
 assert(await page.locator('[data-practice-for] a[href*="soft-systems"]').count()>0);
 report.checks.push('gateway/home/navigation routes','existing SSM item practice link');
 if(!process.env.PRACTICE_BASE_URL){
  const offline=path.join(output,'offline');fs.mkdirSync(offline,{recursive:true});
  const extract=spawnSync('python3',['-m','zipfile','-e',path.join(root,'systems-thinking/practice/downloads/systems-methods-practice.zip'),offline]);assert.equal(extract.status,0);
  await page.goto('file://'+path.join(offline,'index.html'));assert.equal(await page.locator('[data-lab-card]').count(),26);
  await page.goto('file://'+path.join(offline,'system-dynamics/index.html'));await page.locator('[data-check]').first().locator('input[type=radio]').nth(1).check();await page.locator('[data-check]').first().locator('button').click();assert.equal(await page.locator('[data-check]').first().locator('[data-result]').getAttribute('data-outcome'),'correct');
  report.checks.push('offline HTML and interactive answer check');
 }
 assert.equal(errors.length,0,JSON.stringify(errors));report.status='passed';
}
main().catch(error=>{report.status='failed';report.error=error.stack;console.error(error);process.exitCode=1;}).finally(async()=>{fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2)+'\n');console.log('PRACTICE_BROWSER',JSON.stringify(report));if(browser)await browser.close();if(server)await new Promise(resolve=>server.close(resolve));});
