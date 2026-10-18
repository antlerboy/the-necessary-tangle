/* Verify the current intake links and reading pathways at desktop/mobile widths. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const root=path.resolve(__dirname,'../docs');
let server,browser;
async function main(){
 let base=process.env.UPDATE_BASE_URL;
 if(!base){server=http.createServer((req,res)=>{try{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://test').pathname));assert(f===root||f.startsWith(root+path.sep));if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',({'.js':'application/javascript','.json':'application/json','.css':'text/css','.html':'text/html; charset=utf-8'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});await new Promise(r=>server.listen(0,'127.0.0.1',r));base='http://127.0.0.1:'+server.address().port;}
 browser=await chromium.launch();
 for(const width of [1440,390]){
  const page=await browser.newPage({viewport:{width,height:900},reducedMotion:'reduce'});
  for(const route of ['/reading/ashby-laboratory/','/updates/2026-10-18/']){
   const response=await page.goto(base+route);assert.equal(response.status(),200,route);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Overflow '+route+' '+width);
   assert(await page.getByRole('link',{name:'Open updates',exact:true}).isVisible());
  }
  assert.equal(await page.locator('article[data-status="new_discovery"]').count(),20);
  assert.equal(await page.locator('article[data-status="already_represented"]').count(),7);
  await page.goto(base+'/reading/ashby-laboratory/');assert.equal(await page.locator('.grid article').count(),4);
  assert.equal(await page.locator('.grid article a[href^="https://ashby-laboratory."]').count(),4);
  await page.locator('#chapter-6 summary').click();assert(await page.getByText('Chapter 6; A blank is not a self-loop;', {exact:false}).isVisible());
  await page.goto(base+'/learning/');assert(await page.getByRole('link',{name:'Ashby Laboratory: four pathways through 56 exercises',exact:true}).isVisible());
  await page.close();
 }
 console.log('0.33 browser passed: two reader routes, 27 reconciled posts, four chapter pathways, glossary/source limits, Learning link, desktop and mobile.');
}
main().catch(e=>{console.error(e);process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();if(server)await new Promise(r=>server.close(r));});
