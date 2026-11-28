/* Check every new sourced entry in the final edition, with and without JS. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const root=path.resolve(__dirname,'../docs');
const packet=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../sources/first-pass-depth-44/packet.json'),'utf8'));
const out=path.resolve(__dirname,'../validation/first-pass-depth-44');
let server,browser;
(async()=>{
 let base=(process.env.TANGLE_BASE_URL||'').replace(/\/$/,'');
 if(!base){
  server=http.createServer((req,res)=>{
   try{
    let file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname));
    assert(file===root||file.startsWith(root+path.sep));
    if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');
    res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.json':'application/json','.css':'text/css','.js':'application/javascript','.webp':'image/webp'})[path.extname(file)]||'application/octet-stream');
    res.end(fs.readFileSync(file));
   }catch{res.writeHead(404);res.end();}
  });
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  base='http://127.0.0.1:'+server.address().port;
 }
 fs.mkdirSync(out,{recursive:true});
 browser=await chromium.launch({headless:true});
 const currentEdition=await(await fetch(base+'/reader-edition.json')).json();
 const release=currentEdition.graph_release;
 assert.equal(currentEdition.reader_release,release,'Reader and graph editions differ');
 const results=[];
 for(const width of [1440,390]){
  const context=await browser.newContext({viewport:{width,height:900},javaScriptEnabled:false});
  const page=await context.newPage();
  for(const [index,nid] of packet.cohort.entries()){
   const route='/entries/'+nid+'/';
   const response=await page.goto(base+route);
   assert.equal(response.status(),200,route);
   assert.equal(await page.locator('h1').count(),1,route);
   assert.equal(await page.getByRole('heading',{name:'Summary',exact:true}).count(),1);
   assert.equal(await page.getByRole('heading',{name:'Sources and passage locators',exact:true}).count(),1);
   assert.equal(await page.getByRole('heading',{name:'Review status',exact:true}).count(),1);
   assert(await page.getByRole('link',{name:'Open updates',exact:true}).isVisible());
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),route+' overflow '+width);
   const record=await(await context.request.get(base+route+'record.json')).json();
   assert.equal(record.entry.id,nid);
   assert.equal(record.release,release);
   assert.equal(record.profile.review_status,'research_pass_needs_editor');
   assert(record.connections.some(edge=>edge.connection_pass==='first_pass_depth_44'));
   assert(record.evidence_locators.length>0);
   if(index%28===0)await page.screenshot({path:path.join(out,nid+'-'+width+'.png'),fullPage:true});
   results.push({id:nid,width,status:response.status()});
  }
  await page.goto(base+packet.release_url);
  assert.equal(await page.locator('main ol li a').count(),84);
  await context.close();
 }
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 const page=await context.newPage();
 const errors=[];page.on('pageerror',error=>errors.push(error.message));
 for(const nid of packet.cohort.filter((_,index)=>index%28===0)){
  await page.goto(base+'/#view=item&id='+nid);
  const link=page.getByRole('link',{name:'Read or cite this entry',exact:true});
  await link.waitFor();
  assert.equal(await link.getAttribute('href'),'/entries/'+nid+'/');
 }
 assert.deepEqual(errors,[]);
 await page.goto(base+'/versions/');
 assert.equal(await page.locator('article').first().getAttribute('id'),'v'+release.replaceAll('.','-'));
 await context.close();
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify({release,cohort_release:'0.44',base,entries:84,route_checks:results.length,results,passed:true},null,2)+'\n');
 console.log('0.44 cohort browser passed in edition '+release+': all 84 sourced routes and downloads at 390/1440, release index, interactive links, and current history.');
})().catch(error=>{console.error(error);process.exitCode=1}).finally(async()=>{
 if(browser)await browser.close();
 if(server){server.closeAllConnections?.();await new Promise(resolve=>server.close(resolve));}
});
