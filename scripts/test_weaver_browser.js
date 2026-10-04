const {chromium}=require('playwright');const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const root=path.resolve(__dirname,'../docs');
(async()=>{
 const server=http.createServer((req,res)=>{try{let file=path.resolve(root,'.'+new URL(req.url,'http://test').pathname);assert(file===root||file.startsWith(root+path.sep));if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');res.setHeader('Content-Type',file.endsWith('.json')?'application/json':file.endsWith('.js')?'application/javascript':'text/html');res.end(fs.readFileSync(file));}catch{res.writeHead(404);res.end();}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=process.env.WEAVER_BASE_URL||'http://127.0.0.1:'+server.address().port;const browser=await chromium.launch();
 try{for(const width of [390,1440]){
  const page=await browser.newPage({viewport:{width,height:900}});await page.goto(base+'/reading/weaver-complexity/');
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));assert.equal(await page.locator('#claims article').count(),4);
  assert(await page.getByRole('link',{name:'Open updates',exact:true}).isVisible());
  await page.getByText('Compare a possible response',{exact:true}).focus();await page.keyboard.press('Enter');assert(await page.locator('#application details').getAttribute('open')!==null);
  assert.equal(await page.locator('#claims a[href*="publication_fpcs_010"]').count(),8);
  const record=await (await page.request.get(base+'/reading/weaver-complexity/review.json')).json();assert.equal(record.claims.length,4);
  const data=await (await page.request.get(base+'/assets/public-data.json')).json();assert.equal(data.edges.filter(e=>e.connection_pass==='weaver_20261004').length,4);
  const out=path.resolve(__dirname,'../validation/weaver-browser');fs.mkdirSync(out,{recursive:true});await page.screenshot({path:path.join(out,'reader-'+width+'.png'),fullPage:true});
  await page.goto(base+'/#view=item&id=publication_fpcs_010');await page.waitForTimeout(600);assert(await page.getByText('1948 essay distinguishes kinds of scientific problem and examines both the promise and limits of scientific inquiry.',{exact:false}).count()>0);
  await page.close();
 }console.log('Weaver reader, four public graph claims, existing atlas profile, keyboard disclosure, and mobile/desktop containment passed.');}finally{await browser.close();server.close();}
})().catch(e=>{console.error(e);process.exit(1)});
