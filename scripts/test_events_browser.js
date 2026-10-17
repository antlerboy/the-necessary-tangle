/* Read-only events regression checks for the built candidate and live page. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const root=path.resolve(__dirname,'../docs');
const title='systems | cybernetics | complexity events';
let server,browser;
async function main(){
 let base=process.env.EVENTS_BASE_URL;
 if(!base){
  server=http.createServer((req,res)=>{try{
   let file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://test').pathname));
   assert(file===root||file.startsWith(root+path.sep));
   if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');
   res.setHeader('Content-Type',({'.js':'application/javascript','.json':'application/json','.css':'text/css','.html':'text/html; charset=utf-8'})[path.extname(file)]||'application/octet-stream');
   res.end(fs.readFileSync(file));
  }catch{res.writeHead(404);res.end();}});
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  base='http://127.0.0.1:'+server.address().port;
 }
 const eventData=process.env.EVENTS_BASE_URL
  ? await fetch('https://raw.githubusercontent.com/antlerboy/systemsmap/main/dist/data/events.json').then(response=>{assert(response.ok);return response.json();})
  : JSON.parse(fs.readFileSync(path.join(root,'events/data/events.json'),'utf8'));
 // Use the reported CSH case while retained, then a current timed event. Do not
 // turn an expired event into a permanent publication blocker.
 const example=eventData.events.find(event=>event.id==='0c75ea1398ff9f9ccd5553f1')||eventData.events.find(event=>event.calendarEligible&&!event.allDay);
 assert(example,'A timed event is available for calendar export');
 const utc=value=>new Date(value).toISOString().replace(/[-:]/g,'').replace(/\.\d{3}/,'');
 browser=await chromium.launch();
 for(const width of [1440,390]){
  const page=await browser.newPage({viewport:{width,height:900},reducedMotion:'reduce'});
  if(!process.env.EVENTS_BASE_URL){
   const prefix='https://raw.githubusercontent.com/antlerboy/systemsmap/main/dist/';
   await page.route(prefix+'**',async route=>{
    const file=path.resolve(root,'events',decodeURIComponent(route.request().url().slice(prefix.length).split('?')[0]));
    assert(file.startsWith(path.join(root,'events')+path.sep));
    await route.fulfill({path:file});
   });
  }
  const response=await page.goto(base+'/events/');assert.equal(response.status(),200);
  await page.waitForFunction(()=>/^\d+ events?$/.test(document.querySelector('#count').textContent));
  assert.equal(await page.title(),title);
  assert.equal(await page.locator('h1').textContent(),title);
  assert((await page.locator('meta[name="description"]').getAttribute('content')).startsWith(title));
  assert(await page.locator('[aria-label="Open updates"]').isVisible());
  const overflow=await page.evaluate(()=>[...document.querySelectorAll('body *')].filter(element=>{const box=element.getBoundingClientRect();return box.width>0&&box.right>innerWidth+1&&getComputedStyle(element).position!=='absolute';}).map(element=>({tag:element.tagName,id:element.id,className:typeof element.className==='string'?element.className:'',right:Math.round(element.getBoundingClientRect().right)})).slice(0,12));
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Events overflow '+width+' '+JSON.stringify(overflow));
  await page.locator('#period').selectOption('all');
  for(const query of ['systems','cybernetics','complexity']){
   await page.locator('#q').fill(query);
   await page.waitForFunction(()=>parseInt(document.querySelector('#count').textContent)>0);
   assert(await page.locator('#results .event-card').count()>0,query+' results at '+width);
  }
  await page.locator('#q').fill(example.title);
  await page.locator('[data-event="'+example.id+'"]').click();
  const download=page.waitForEvent('download');
  await page.getByRole('button',{name:'Add to calendar',exact:true}).click();
  const file=await download;
  const ics=fs.readFileSync(await file.path(),'utf8').replace(/\r\n /g,'');
  assert(ics.includes('UID:'+example.id+'@systemsmap.antlerboy.com'));
  assert(ics.includes('DTSTART:'+utc(example.start)));
  if(example.end)assert(ics.includes('DTEND:'+utc(example.end)));
  if(example.id==='0c75ea1398ff9f9ccd5553f1'){
   assert(ics.includes('DTSTART:20261020T130000Z'));
   assert(ics.includes('DTEND:20261020T133000Z'));
  }
  await page.locator('#detail .close').click();
  await page.goto(base+'/events/submissions.html');
  assert((await page.title()).includes(title));
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Queue overflow '+width);
  await page.close();
 }
 console.log('Events checks passed: naming/metadata, three subject searches, stable calendar time/UID (CSH while retained), queue, feedback, desktop and mobile. No form submitted.');
}
main().catch(error=>{console.error(error);process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();if(server)await new Promise(resolve=>server.close(resolve));});
