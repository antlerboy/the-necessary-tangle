const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const root=path.resolve(__dirname,'../docs'),out=path.resolve(__dirname,'../validation/practice-browser');
let server,browser,page;const report={status:'running',checks:[],console:[]};fs.mkdirSync(out,{recursive:true});
async function main(){
 let base=process.env.PRACTICE_BASE_URL;
 if(!base){server=http.createServer((req,res)=>{let name=path.resolve(root,'.'+new URL(req.url,'http://test').pathname);try{if(!name.startsWith(root+path.sep)&&name!==root)throw Error('path');if(fs.statSync(name).isDirectory())name=path.join(name,'index.html');const types={'.html':'text/html','.js':'application/javascript','.css':'text/css','.json':'application/json','.mp4':'video/mp4','.webm':'video/webm','.webp':'image/webp','.svg':'image/svg+xml'};res.setHeader('Content-Type',types[path.extname(name)]||'application/octet-stream');res.end(fs.readFileSync(name));}catch(_){res.writeHead(404);res.end();}});await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));base='http://127.0.0.1:'+server.address().port;}
 // Use the runner's real Chrome for its supported production H.264 codecs.
 // Do not disable autoplay policy: the public page must qualify for muted autoplay.
 browser=await chromium.launch({headless:true,channel:'chrome'});const context=await browser.newContext({viewport:{width:1365,height:900}});page=await context.newPage();
 page.on('pageerror',e=>report.console.push(e.message));page.on('console',m=>{if(m.type()==='error')report.console.push(m.text());});
 await page.goto(base+'/',{waitUntil:'load'});
 report.codec=await page.evaluate(()=>document.createElement('video').canPlayType('video/mp4; codecs="avc1.42E01E"'));
 await page.waitForFunction(()=>{const v=document.querySelector('[data-living-mark] video');return v&&!v.paused&&v.currentTime>0.15;},null,{timeout:25000});
 assert.equal(await page.locator('.living-mark-playback').count(),0);
 const button=page.locator('.living-mark-toggle');assert.equal(await button.innerText(),'');assert((await button.boundingBox()).width<=36);
 await button.click();assert(await page.locator('[data-living-mark] video').evaluate(v=>v.paused));await button.click();await page.waitForFunction(()=>!document.querySelector('[data-living-mark] video').paused);
 await page.screenshot({path:path.join(out,'autoplay-header.png')});report.checks.push('actual muted autoplay in Chrome','compact pause and resume','no long playback button');
 const reduced=await browser.newContext({reducedMotion:'reduce'});const rp=await reduced.newPage();await rp.goto(base+'/',{waitUntil:'load'});await rp.waitForSelector('[data-living-mark] img');assert.equal(await rp.locator('[data-living-mark] video').count(),0);await reduced.close();report.checks.push('reduced-motion still image');
 for(const width of [1365,390]){await page.setViewportSize({width,height:900});await page.goto(base+'/systems-thinking/practice/',{waitUntil:'load'});assert(await page.locator('.alpha-notice').isVisible());assert(await page.locator('#why-this-pack').isVisible());assert.match(await page.locator('h1').innerText(),/Systemic systems methods practice/);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));await page.screenshot({path:path.join(out,'alpha-home-'+width+'.png'),fullPage:true});}
 report.checks.push('enduring author introduction','visible alpha status','desktop and mobile containment');
 const response=await context.request.get(base+'/systems-thinking/practice/assets/pack.json');const pack=await response.json();assert.equal(pack.publication_status,'alpha');assert.equal(pack.author,'Benjamin P Taylor');report.status='passed';
}
main().catch(async e=>{report.status='failed';report.error=e.stack;console.error(e);process.exitCode=1;if(page){report.diagnostics=await page.evaluate(()=>{const h=document.querySelector('[data-living-mark]'),v=h?.querySelector('video');return {host:h?.outerHTML,video:v?{paused:v.paused,readyState:v.readyState,currentTime:v.currentTime,error:v.error?.message,src:v.currentSrc}:null,scripts:Array.from(document.scripts,s=>s.src).filter(s=>s.includes('motion')||s.includes('iteration-19'))};}).catch(()=>null);await page.screenshot({path:path.join(out,'presentation-failure.png')}).catch(()=>{});}}).finally(async()=>{fs.writeFileSync(path.join(out,'presentation-report.json'),JSON.stringify(report,null,2)+'\n');console.log('PRESENTATION_CHECK',JSON.stringify(report));if(browser)await browser.close();if(server)await new Promise(resolve=>server.close(resolve));});
