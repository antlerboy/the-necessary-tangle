/* Required publication check for the changed map-reading paths. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const http=require('node:http');
const root=path.resolve(__dirname,'../docs');
const output=path.resolve(__dirname,'../validation/maps-browser');
fs.mkdirSync(output,{recursive:true});
let server,browser;
const report={status:'running',checks:[],errors:[]};
async function main(){
  let base=process.env.MAPS_BASE_URL;
  if(!base){
    server=http.createServer((req,res)=>{
      let target=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://test').pathname));
      if(target!==root&&!target.startsWith(root+path.sep)){res.writeHead(403);return res.end();}
      try{
        if(fs.statSync(target).isDirectory())target=path.join(target,'index.html');
        const mime={'.html':'text/html; charset=utf-8','.json':'application/json','.js':'application/javascript','.css':'text/css','.svg':'image/svg+xml'};
        res.writeHead(200,{'Content-Type':mime[path.extname(target)]||'application/octet-stream'});res.end(fs.readFileSync(target));
      }catch{res.writeHead(404);res.end('Not found');}
    });
    await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
    base='http://127.0.0.1:'+server.address().port;
  }
  browser=await chromium.launch({headless:true});
  for(const width of [1440,390]){
    const context=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});
    const page=await context.newPage();
    page.on('pageerror',error=>report.errors.push(error.message));
    for(const route of ['/prior-maps/','/reading-list.html','/updates/']){
      const response=await page.goto(base+route,{waitUntil:'load'});assert.equal(response.status(),200);
      await page.locator('a[href="/prior-maps/coexplorer/"]').click();
      await page.getByRole('heading',{name:'Reading the CoExplorer maps',exact:true}).waitFor();
      assert.equal(await page.locator('article.source').count(),9);
      assert.equal(await page.locator('.status').filter({hasText:'Submitted; unread (HTTP 403)'}).count(),2);
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Overflow: '+width);
      assert(await page.getByRole('link',{name:'Open updates',exact:true}).isVisible());
      report.checks.push({route,width,navigation:true,sourceLabels:true,containment:true});
    }
    await page.getByRole('link',{name:'Reading a relationship',exact:true}).click();
    assert.equal(new URL(page.url()).hash,'#relations');
    const table=page.getByRole('region',{name:'Relationship comparison'});
    await table.focus();assert(await table.evaluate(el=>el===document.activeElement));
    const response=await context.request.get(base+'/prior-maps/coexplorer/source-review.json');
    assert.equal(response.status(),200);assert.equal((await response.json()).sources.length,9);
    await page.screenshot({path:path.join(output,'review-'+width+'.png'),fullPage:true});
    await context.close();
  }
  assert.deepEqual(report.errors,[]);report.status='passed';
}
main().catch(error=>{report.status='failed';report.failure=error.stack;process.exitCode=1;}).finally(async()=>{
  fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2)+'\n');
  if(browser)await browser.close();if(server)await new Promise(resolve=>server.close(resolve));console.log(JSON.stringify(report));
});
