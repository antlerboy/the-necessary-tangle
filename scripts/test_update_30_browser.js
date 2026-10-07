const {chromium}=require('playwright');const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const root=path.resolve(__dirname,'../docs');
(async()=>{
 const server=http.createServer((req,res)=>{try{let file=path.resolve(root,'.'+new URL(req.url,'http://test').pathname);assert(file===root||file.startsWith(root+path.sep));if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');res.setHeader('Content-Type',file.endsWith('.json')?'application/json':file.endsWith('.js')?'application/javascript':file.endsWith('.css')?'text/css':'text/html');res.end(fs.readFileSync(file));}catch{res.writeHead(404);res.end();}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=process.env.UPDATE_BASE_URL||'http://127.0.0.1:'+server.address().port;const browser=await chromium.launch();
 try{for(const width of [390,1440]){
  const page=await browser.newPage({viewport:{width,height:900}});await page.goto(base+'/updates/2026-10-07/');
  assert.equal(await page.locator('#recent article').count(),31);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.getByRole('link',{name:'Read Schot and test the conditions around a pilot',exact:true}).click();assert(page.url().includes('/reading/socio-technical-transitions/'));
  assert(await page.getByRole('link',{name:'Open updates',exact:true}).isVisible());assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.getByText('Compare a possible response',{exact:true}).focus();await page.keyboard.press('Enter');assert(await page.locator('#application details').getAttribute('open')!==null);
  const out=path.resolve(__dirname,'../validation/update-30-browser');fs.mkdirSync(out,{recursive:true});await page.screenshot({path:path.join(out,'reader-'+width+'.png'),fullPage:true});
  await page.getByRole('link',{name:'Inspect the source-located meta-rule distinction',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('#graphEdges .graph-edge.selected'));assert((await page.locator('#mapInspector').textContent()).includes('PDF page 9'));
  await page.goto(base+'/#view=item&id=person_johan_schot');await page.waitForFunction(()=>document.body.textContent.includes('Historian working on socio-technical change'));assert((await page.locator('body').textContent()).includes('Utrecht'));
  const packet=await(await page.request.get(base+'/updates/2026-10-07/review.json')).json();assert.equal(packet.posts.length,31);
  await page.close();
 }console.log('Release 0.30 browser checks passed: full intake, source reader, keyboard disclosure, profile and selected graph evidence at 390/1440px.');}finally{await browser.close();server.close();}
})().catch(e=>{console.error(e);process.exit(1)});
