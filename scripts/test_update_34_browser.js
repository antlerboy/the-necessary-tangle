/* Read-only and intercepted-request checks; never submit a real contribution. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const root=path.resolve(__dirname,'../docs');let server,browser;
async function main(){
 let base=process.env.UPDATE_BASE_URL;
 if(!base){server=http.createServer((req,res)=>{try{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://test').pathname));assert(f===root||f.startsWith(root+path.sep));if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',({'.js':'application/javascript','.json':'application/json','.css':'text/css','.html':'text/html; charset=utf-8'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});await new Promise(r=>server.listen(0,'127.0.0.1',r));base='http://127.0.0.1:'+server.address().port;}
 browser=await chromium.launch();
 for(const width of [1440,390]){
  const page=await browser.newPage({viewport:{width,height:900},reducedMotion:'reduce'});
  for(const route of ['/reading/orglens/','/reading/42-systemic-review/','/reading/systems-leadership-and-action/','/updates/2026-10-24/','/contribute/']){
   const response=await page.goto(base+route);assert.equal(response.status(),200,route);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Overflow '+route+' '+width);
   assert(await page.getByRole('link',{name:'Open updates',exact:true}).isVisible());
  }
  assert.equal(await page.locator('#quickContributionEmail').getAttribute('required'),null);
  assert.equal(await page.locator('#quickContributionText').getAttribute('maxlength'),'6000');
  let succeed=false,submitted;
  await page.route('https://events.transduction.systems/api/contributions',async route=>{
   submitted=route.request().postDataJSON();
   await route.fulfill({status:succeed?201:503,contentType:'application/json',headers:{'Access-Control-Allow-Origin':'*'},body:JSON.stringify(succeed?{received:true,id:'intercepted-test-receipt'}:{error:'Temporarily unavailable; your text is still here.'})});
  });
  await page.locator('#quickContributionText').fill('A read-only browser test using intercepted network responses.');
  await page.getByRole('button',{name:'Send contribution',exact:true}).click();
  await page.getByRole('status').filter({hasText:'Temporarily unavailable'}).waitFor();
  assert((await page.locator('#quickContributionText').inputValue()).length>0);
  assert.equal(submitted.email,'');
  succeed=true;await page.getByRole('button',{name:'Send contribution',exact:true}).click();
  await page.getByRole('status').filter({hasText:'intercepted-test-receipt'}).waitFor();
  assert.equal(await page.locator('#quickContributionText').inputValue(),'');
  await page.goto(base+'/#view=contribute');assert.equal(await page.locator('#quickContributionForm').count(),1);assert(await page.locator('#quickContributionText').isVisible());
  await page.close();
 }
 console.log('0.34 browser passed: five routes, desktop/mobile containment, optional email, intercepted receipt, retained input on failure, and main contribution entrance.');
}
main().catch(e=>{console.error(e);process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();if(server)await new Promise(r=>server.close(r));});
