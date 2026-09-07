const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const root=path.resolve(__dirname,'../docs'),out=path.resolve(__dirname,'../validation/practice-browser');
let server,browser;const report={status:'running',checks:[]};fs.mkdirSync(out,{recursive:true});
async function main(){
 let base=process.env.PRACTICE_BASE_URL;
 if(!base){server=http.createServer((req,res)=>{let name=path.resolve(root,'.'+new URL(req.url,'http://test').pathname);try{if(!name.startsWith(root+path.sep)&&name!==root)throw Error('path');if(fs.statSync(name).isDirectory())name=path.join(name,'index.html');const types={'.html':'text/html','.js':'application/javascript','.css':'text/css','.json':'application/json','.mp4':'video/mp4','.webm':'video/webm','.webp':'image/webp','.svg':'image/svg+xml'};res.setHeader('Content-Type',types[path.extname(name)]||'application/octet-stream');res.end(fs.readFileSync(name));}catch(_){res.writeHead(404);res.end();}});await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));base='http://127.0.0.1:'+server.address().port;}
 browser=await chromium.launch({headless:true});const context=await browser.newContext({viewport:{width:1365,height:900}});const page=await context.newPage();
 await page.goto(base+'/',{waitUntil:'load'});
 await page.waitForFunction(()=>{const v=document.querySelector('[data-living-mark] video');return v&&!v.paused&&v.currentTime>0.15;},null,{timeout:20000});
 assert.equal(await page.locator('.living-mark-playback').count(),0);
 const button=page.locator('.living-mark-toggle');assert.equal(await button.innerText(),'');assert((await button.boundingBox()).width<=36);
 await button.click();assert(await page.locator('[data-living-mark] video').evaluate(v=>v.paused));await button.click();await page.waitForFunction(()=>!document.querySelector('[data-living-mark] video').paused);
 await page.screenshot({path:path.join(out,'autoplay-header.png')});report.checks.push('actual muted autoplay','compact pause and resume','no long playback button');
 const reduced=await browser.newContext({reducedMotion:'reduce'});const rp=await reduced.newPage();await rp.goto(base+'/',{waitUntil:'load'});await rp.waitForSelector('[data-living-mark] img');assert.equal(await rp.locator('[data-living-mark] video').count(),0);await reduced.close();report.checks.push('reduced-motion still image');
 for(const width of [1365,390]){await page.setViewportSize({width,height:900});await page.goto(base+'/systems-thinking/practice/',{waitUntil:'load'});assert(await page.locator('.alpha-notice').isVisible());assert(await page.locator('#why-this-pack').isVisible());assert.match(await page.locator('h1').innerText(),/Systemic systems methods practice/);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));await page.screenshot({path:path.join(out,'alpha-home-'+width+'.png'),fullPage:true});}
 report.checks.push('enduring author introduction','visible alpha status','desktop and mobile containment');
 const response=await context.request.get(base+'/systems-thinking/practice/assets/pack.json');const pack=await response.json();assert.equal(pack.publication_status,'alpha');assert.equal(pack.author,'Benjamin P Taylor');report.status='passed';
}
main().catch(e=>{report.status='failed';report.error=e.stack;console.error(e);process.exitCode=1;}).finally(async()=>{fs.writeFileSync(path.join(out,'presentation-report.json'),JSON.stringify(report,null,2)+'\n');console.log('PRESENTATION_CHECK',JSON.stringify(report));if(browser)await browser.close();if(server)await new Promise(resolve=>server.close(resolve));});
