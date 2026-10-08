/* Reader behaviour is the acceptance criterion, including reload and native link state. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const root=path.resolve(__dirname,'../docs'),out=path.resolve(__dirname,'../validation/update-31-browser');
fs.mkdirSync(out,{recursive:true});
let server,browser;const report={status:'running',checks:[],errors:[]};
async function main(){
 let base=process.env.UPDATE_BASE_URL;
 if(!base){server=http.createServer((req,res)=>{try{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://test').pathname));assert(f===root||f.startsWith(root+path.sep));if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',({'.js':'application/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.html':'text/html; charset=utf-8'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});await new Promise(r=>server.listen(0,'127.0.0.1',r));base='http://127.0.0.1:'+server.address().port;}
 browser=await chromium.launch();
 for(const width of [1440,390]){
  const context=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});const page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));
  for(const route of ['/learning/','/learning/isss/','/corpora/ing-ocad/','/reading/researcher-modules/','/reading/orglens/','/prior-maps/principles/','/prior-maps/review-2026-10/','/updates/2026-10-08/']){
   const response=await page.goto(base+route);assert.equal(response.status(),200,route);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Overflow '+route+' '+width);
   assert(await page.getByRole('link',{name:'Open updates',exact:true}).isVisible());report.checks.push({route,width,readable:true});
  }
  assert.equal(await page.locator('#comments ol>li').count(),85);assert.equal(await page.locator('#issues article').count(),14);
  await page.goto(base+'/learning/');await page.locator('#learningSearch').fill('PSTA');assert.equal(await page.locator('#learningRoutes article:visible').count(),5);
  await page.reload();assert.equal(await page.locator('#learningSearch').inputValue(),'PSTA');
  await page.locator('#learningSearch').fill('');await page.locator('#learningAccess').selectOption('open');assert(await page.locator('#learningRoutes article:visible').count()>4);
  await page.screenshot({path:path.join(out,'learning-'+width+'.png'),fullPage:true});
  await page.goto(base+'/corpora/ing-ocad/');const first=page.locator('#module-1 summary');await first.focus();await page.keyboard.press('Enter');assert(await page.locator('#module-1 details').evaluate(e=>e.open));assert(await page.locator('#module-1 details a').count()>0);
  await page.goto(base+'/#view=map&focus=concept_viability&layer=all&family=all&depth=all&display=graph');
  await page.waitForFunction(()=>document.querySelectorAll('#graphNodes [data-id]').length>20);
  const group=page.locator('#graphNodes [data-id]').filter({hasNot:page.locator('.no-such-child')}).nth(1);
  const newFocus=await group.getAttribute('data-id');const href=await group.evaluate(g=>g.closest('a').getAttribute('href'));
  assert(new URLSearchParams(href.slice(1)).get('depth')==='all');
  const prevented=await group.evaluate(g=>{const e=new MouseEvent('click',{bubbles:true,cancelable:true,ctrlKey:true,button:0});g.dispatchEvent(e);return e.defaultPrevented;});assert.equal(prevented,false,'Ctrl-click swallowed');
  await group.focus();await page.keyboard.press('Enter');assert.equal(await page.locator('#mapDepth').inputValue(),'all');assert.equal(new URLSearchParams(new URL(page.url()).hash.slice(1)).get('focus'),newFocus);
  assert.equal(new URLSearchParams(new URL(page.url()).hash.slice(1)).get('family'),'all');
  await page.reload();await page.waitForFunction(()=>document.querySelector('#mapDepth')?.value==='all');
  await page.goto(base+'/#view=map&focus=concept_viability&layer=substantive&family=conceptual&depth=2&display=graph');
  await page.waitForFunction(()=>document.querySelector('#mapFamily')?.value==='conceptual');
  const node=page.locator('#graphNodes [data-id]').first();await node.focus();await page.keyboard.press('Enter');
  assert.equal(await page.locator('#mapFamily').inputValue(),'conceptual');assert.equal(await page.locator('#mapDepth').inputValue(),'2');
  assert.equal(new URLSearchParams(new URL(page.url()).hash.slice(1)).get('family'),'conceptual');
  const edge=page.locator('#graphEdges [data-edge]').first();assert(await edge.count()>0);const eid=await edge.getAttribute('data-edge');const edgeHref=await edge.evaluate(g=>g.closest('a').getAttribute('href'));
  assert.equal(new URLSearchParams(edgeHref.slice(1)).get('family'),'conceptual');await edge.focus();await page.keyboard.press('Enter');assert.equal(new URLSearchParams(new URL(page.url()).hash.slice(1)).get('edge'),eid);
  await page.reload();await page.waitForFunction(()=>document.querySelector('#graphEdges .graph-edge.selected'));
  assert((await page.locator('#mapInspector').textContent()).length>80);
  await page.locator('#mapCardToggle').click();await page.waitForFunction(()=>document.querySelector('#graphWrap').classList.contains('map-card-mode'));
  assert.equal(new URLSearchParams(new URL(page.url()).hash.slice(1)).get('display'),'cards');
  const neighbour=page.locator('#mapCardView .map-card-relation a').first();const nextHref=await neighbour.getAttribute('href');const state=new URLSearchParams(nextHref.slice(1));assert.equal(state.get('family'),'conceptual');assert.equal(state.get('depth'),'2');assert.equal(state.get('display'),'cards');
  await neighbour.click();await page.waitForFunction(()=>document.querySelector('#mapCardView h2')?.textContent.length>0);assert.equal(await page.locator('#mapFamily').inputValue(),'conceptual');
  await page.reload();await page.waitForFunction(()=>document.querySelector('#graphWrap').classList.contains('map-card-mode'));
  const disclosure=page.locator('#mapCardView details summary').first();await disclosure.focus();await page.keyboard.press('Enter');assert(await page.locator('#mapCardView details').first().evaluate(e=>e.open));
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Map overflow '+width);
  await page.screenshot({path:path.join(out,'cards-'+width+'.png'),fullPage:true});
  await page.getByRole('link',{name:'Switch to graph view'}).click();await page.waitForFunction(()=>!document.querySelector('#graphWrap').classList.contains('map-card-mode'));
  await page.goBack();await page.waitForFunction(()=>document.querySelector('#graphWrap').classList.contains('map-card-mode'));
  report.checks.push({width,refocus:true,filterPersistence:true,scalePersistence:true,modifiedClick:true,edgeReload:true,cardReload:true,keyboardEvidence:true,browserBack:true});await context.close();
 }
 assert.equal(report.errors.length,0,report.errors.join('\n'));report.status='passed';report.base=process.env.UPDATE_BASE_URL||'Local publication candidate';
}
main().catch(e=>{report.status='failed';report.failure=e.stack;process.exitCode=1}).finally(async()=>{fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');if(browser)await browser.close();if(server)server.close();console.log(JSON.stringify(report));});
