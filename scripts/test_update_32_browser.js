/* Check that the reader entrance and source directories work on desktop and mobile. */
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
  for(const route of ['/about/how-to-use/','/about/evidence/','/reading/design-horizon/','/prior-maps/sources/','/updates/2026-10-13/']){
   const response=await page.goto(base+route);assert.equal(response.status(),200,route);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Overflow '+route+' '+width);
   assert(await page.getByRole('link',{name:'Open updates',exact:true}).isVisible());
  }
  await page.goto(base+'/reading/design-horizon/');assert.equal(await page.locator('.grid article').count(),8);
  assert.equal(await page.locator('.grid article a[href^="/#view=item"]').count(),8);
  await page.goto(base+'/#view=about');
  await page.getByRole('heading',{name:'Choose a starting point',exact:true}).waitFor();
  const details=page.locator('#view-about > details');assert.equal(await details.evaluate(e=>e.open),false);
  assert(await page.getByRole('heading',{name:'What a connection means',exact:true}).isVisible());
  await details.locator('summary').first().click();assert.equal(await details.evaluate(e=>e.open),true);
  assert.equal(await page.locator('#view-about .layer-card').count(),6);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'About overflow '+width);
  await page.close();
 }
 console.log('Release 0.32 reader checks passed: five routes, eight resource links, About disclosure, six map layers, desktop and mobile.');
}
main().catch(e=>{console.error(e);process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();if(server)await new Promise(r=>server.close(r));});
