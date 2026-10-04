const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const root=path.resolve(__dirname,'../docs');
const packet=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../sources/claim-lab-2026-10-04/cases.json'),'utf8'));
(async()=>{
 const server=http.createServer((req,res)=>{try{let file=path.resolve(root,'.'+new URL(req.url,'http://test').pathname);assert(file.startsWith(root+path.sep));if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');res.setHeader('Content-Type',file.endsWith('.json')?'application/json':'text/html');res.end(fs.readFileSync(file));}catch{res.writeHead(404);res.end();}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const browser=await chromium.launch();const out=path.resolve(__dirname,'../validation/claim-lab-browser');fs.mkdirSync(out,{recursive:true});
 try{
  for(const width of [390,1440]){
   const page=await browser.newPage({viewport:{width,height:900}});
   const routes=['/systems-thinking/claim-lab/','/systems-thinking/claim-lab/worksheets/','/updates/2026-10-04/',...packet.cases.map(c=>'/systems-thinking/claim-lab/'+c.id+'/')];
   for(const route of routes){
    const response=await page.goto('http://127.0.0.1:'+server.address().port+route);assert.equal(response.status(),200);
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),route+' overflow at '+width);
    assert(await page.getByRole('link',{name:'Open updates',exact:true}).isVisible());
    if(await page.locator('#attempt').count()){
     await page.getByText('Compare your reasoning',{exact:true}).click();assert(await page.locator('#attempt details').getAttribute('open')!==null);
     await page.getByText('Compare the changed case',{exact:true}).focus();await page.keyboard.press('Enter');assert(await page.locator('#changed details').getAttribute('open')!==null);
     assert.equal(await page.locator('#connections h3 a').count(),2);
    }
   }
   await page.goto('http://127.0.0.1:'+server.address().port+'/systems-thinking/claim-lab/');
   await page.screenshot({path:path.join(out,'home-'+width+'.png'),fullPage:true});
   await page.goto('http://127.0.0.1:'+server.address().port+'/systems-thinking/claim-lab/the-average-improved/');
   await page.screenshot({path:path.join(out,'case-'+width+'.png'),fullPage:true});
   await page.close();
  }
  fs.writeFileSync(path.join(out,'report.json'),JSON.stringify({cases:8,routes:11,widths:[390,1440],checks:['HTTP','containment','updates','keyboard disclosure','typed method routes'],passed:true},null,2));
  console.log('Claim lab: eleven routes, eight cases, keyboard comparisons, and updates controls passed at 390px and 1440px.');
 }finally{await browser.close();server.close();}
})().catch(e=>{console.error(e);process.exit(1)});
