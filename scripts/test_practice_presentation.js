/* Verify visible motion for every mark, with no playback controls or media permission. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const root=path.resolve(__dirname,'../docs'),out=path.resolve(__dirname,'../validation/practice-browser');
let server,browser,page;const report={status:'running',checks:[],marks:[],console:[]};fs.mkdirSync(out,{recursive:true});
async function movingPixels(p){
  const mark=p.locator('[data-living-mark]');
  const first=await mark.screenshot({animations:'allow'});
  for(let i=0;i<4;i++){
    await p.waitForTimeout(450);
    if(!first.equals(await mark.screenshot({animations:'allow'})))return true;
  }
  return false;
}
async function noControls(p){
  assert.equal(await p.locator('.living-mark-playback,.living-mark-toggle').count(),0);
  assert.equal(await p.locator('[data-living-mark] video').count(),0);
  assert.equal(await p.getByRole('button',{name:/^(play|pause|resume) (mark|animation)$/i}).count(),0);
}
async function main(){
 let base=process.env.PRACTICE_BASE_URL;
 if(!base){server=http.createServer((req,res)=>{let name=path.resolve(root,'.'+new URL(req.url,'http://test').pathname);try{if(!name.startsWith(root+path.sep)&&name!==root)throw Error('path');if(fs.statSync(name).isDirectory())name=path.join(name,'index.html');const types={'.html':'text/html','.js':'application/javascript','.css':'text/css','.json':'application/json','.webp':'image/webp','.svg':'image/svg+xml'};res.setHeader('Content-Type',types[path.extname(name)]||'application/octet-stream');res.end(fs.readFileSync(name));}catch(_){res.writeHead(404);res.end();}});await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));base='http://127.0.0.1:'+server.address().port;}
 browser=await chromium.launch({headless:true});
 const context=await browser.newContext({viewport:{width:1365,height:900}});page=await context.newPage();
 page.on('pageerror',e=>report.console.push(e.message));
 // Video rejection must not prevent the mark from moving. Old pause state is obsolete.
 await context.addInitScript(()=>{HTMLMediaElement.prototype.play=function(){return Promise.reject(new DOMException('Video unavailable in this test','NotAllowedError'));};try{sessionStorage.setItem('necessary-tangle:mark-motion','off');}catch(_){}});
 await page.goto(base+'/',{waitUntil:'domcontentloaded'});
 await page.waitForSelector('[data-living-mark][data-motion-state="playing"] img');
 assert(await movingPixels(page),'default automatic animation');await noControls(page);
 await page.reload({waitUntil:'domcontentloaded'});await page.waitForSelector('[data-motion-state="playing"] img');assert(await movingPixels(page),'automatic animation after reload');
 report.checks.push('automatic motion with video playback rejected','no playback controls','old pause state cannot disable animation','automatic motion after reload');
 const response=await context.request.get(base+'/assets/living-marks/playback-manifest.json');assert.equal(response.status(),200);
 const manifest=await response.json(),marks=manifest.marks.filter(m=>m.kind==='video');assert.equal(marks.length,44);
 for(const mark of marks){
   await page.goto(base+'/?mark='+encodeURIComponent(mark.id),{waitUntil:'domcontentloaded'});
   await page.waitForSelector('[data-living-mark][data-mark-id="'+mark.id+'"][data-motion-state="playing"] img');
   const changed=await movingPixels(page);report.marks.push({id:mark.id,visible_frames_changed:changed});assert(changed,'frozen mark: '+mark.id);await noControls(page);
 }
 report.checks.push('all 44 moving marks show visibly changing frames');
 await page.screenshot({path:path.join(out,'autoplay-header.png')});
 const reduced=await browser.newContext({reducedMotion:'reduce'});const rp=await reduced.newPage();await rp.goto(base+'/',{waitUntil:'domcontentloaded'});await rp.waitForSelector('[data-motion-state="paused"] img');assert.equal(await movingPixels(rp),false);await noControls(rp);
 await rp.goto(base+'/?motion=on',{waitUntil:'domcontentloaded'});await rp.waitForSelector('[data-motion-state="playing"] img');assert(await movingPixels(rp),'explicit URL choice can enable animation');await noControls(rp);
 await reduced.close();report.checks.push('reduced-motion still default','explicit motion URL works without a player');
 for(const width of [1365,390]){await page.setViewportSize({width,height:900});await page.goto(base+'/',{waitUntil:'domcontentloaded'});await page.waitForSelector('[data-motion-state="playing"] img');await noControls(page);assert(await movingPixels(page));assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));await page.goto(base+'/systems-thinking/practice/',{waitUntil:'load'});assert(await page.locator('.alpha-notice').isVisible());assert(await page.locator('#why-this-pack').isVisible());assert.match(await page.locator('h1').innerText(),/Systemic systems methods practice/);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));await page.screenshot({path:path.join(out,'alpha-home-'+width+'.png'),fullPage:true});}
 report.checks.push('automatic header on desktop and mobile','enduring author introduction','visible alpha status','desktop and mobile containment');
 const resource=await context.request.get(base+'/systems-thinking/practice/assets/pack.json');const pack=await resource.json();assert.equal(pack.publication_status,'alpha');assert.equal(pack.author,'Benjamin P Taylor');
 assert.equal(report.console.length,0,JSON.stringify(report.console));report.status='passed';
}
main().catch(async e=>{report.status='failed';report.error=e.stack;console.error(e);process.exitCode=1;if(page){report.host=await page.locator('[data-living-mark]').evaluate(el=>el.outerHTML).catch(()=>null);await page.screenshot({path:path.join(out,'presentation-failure.png')}).catch(()=>{});}}).finally(async()=>{fs.writeFileSync(path.join(out,'presentation-report.json'),JSON.stringify(report,null,2)+'\n');console.log('PRESENTATION_CHECK',JSON.stringify(report));if(browser)await browser.close();if(server)await new Promise(resolve=>server.close(resolve));});
