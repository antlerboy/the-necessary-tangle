const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const root=path.resolve(__dirname,'../docs');
(async()=>{
 const server=http.createServer((req,res)=>{try{let file=path.resolve(root,'.'+new URL(req.url,'http://test').pathname);assert(file.startsWith(root+path.sep));if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');res.setHeader('Content-Type',file.endsWith('.json')?'application/json':'text/html');res.end(fs.readFileSync(file));}catch{res.writeHead(404);res.end();}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const browser=await chromium.launch();
 try{
  for(const width of [390,1440]){
   const page=await browser.newPage({viewport:{width,height:900}});
   for(const route of ['/systems-sciences/','/updates/2026-09-25/','/reading-list.html','/updates/','/updates/2026-09-09/']){
    const response=await page.goto('http://127.0.0.1:'+server.address().port+route);assert.equal(response.status(),200);
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),route+' overflows at '+width);
    assert(await page.locator('a[href^="/systems-sciences/"]').count()>0 || route==='/systems-sciences/');
    if(route==='/systems-sciences/'){
     assert(await page.getByRole('heading',{name:'Systems Sciences steward: David Ing',exact:true}).count()===1);
     assert(await page.getByRole('link',{name:'Open updates',exact:true}).isVisible());
     assert.equal(await page.locator('#jackson').count(),1);
    }
   }
   await page.close();
  }
  console.log('Submission guide: desktop/mobile containment, navigation, steward and updates control passed.');
 }finally{await browser.close();server.close();}
})().catch(e=>{console.error(e);process.exit(1)});
