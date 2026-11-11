const { chromium } = require('playwright');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const tangle = fs.existsSync('sources/making-things-change/guide.json');
const data = JSON.parse(fs.readFileSync(tangle ? 'sources/making-things-change/guide.json' : 'content/making-things-change.json','utf8'));
const root = path.resolve(tangle ? 'docs' : '_site');
(async()=>{
 let server;
 let base = process.env.GUIDE_BASE_URL;
 if(!base){
  server=http.createServer((req,res)=>{
   const file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
   if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return}
   const target=fs.existsSync(file)&&fs.statSync(file).isDirectory()?path.join(file,'index.html'):file;
   if(!fs.existsSync(target)){res.writeHead(404).end();return}
   res.setHeader('Content-Type',target.endsWith('.pdf')?'application/pdf':target.endsWith('.css')?'text/css':target.endsWith('.js')?'text/javascript':'text/html; charset=utf-8');
   fs.createReadStream(target).pipe(res);
  });
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  base='http://127.0.0.1:'+server.address().port;
 }
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage({acceptDownloads:true});
  for(const width of [1440,390]){
   await page.setViewportSize({width,height:1000});
   const response=await page.goto(base+data.route,{waitUntil:'networkidle'});
   assert.equal(response.status(),200);
   assert.equal(await page.locator('.guide-editions article').count(),2);
   assert.ok((await page.locator('.guide-editions article').first().innerText()).includes('Revised draft'));
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Horizontal overflow at '+width);
  }
  for(const version of data.versions){
   const anchor=page.locator('#'+version.id+' a[download]');
   assert.equal(await anchor.innerText(),version.filename);
   assert.equal(await anchor.getAttribute('download'),version.filename);
   const [download]=await Promise.all([page.waitForEvent('download'),anchor.click()]);
   assert.equal(download.suggestedFilename(),version.filename);
   assert.equal(await download.failure(),null);
   assert.equal(crypto.createHash('sha256').update(fs.readFileSync(await download.path())).digest('hex'),version.sha256);
  }
  if(tangle)assert.equal(await page.locator('[aria-label="Open updates"]').count(),1);
  console.log('Guide editions: desktop/mobile, exact download names, PDF hashes, and navigation checks passed');
 }finally{
  await browser.close();
  if(server)await new Promise(resolve=>server.close(resolve));
 }
})().catch(error=>{console.error(error);process.exit(1)});

