/* Inspect current routes at desktop and mobile sizes with real navigation. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const root=path.resolve(__dirname,'../docs'),output=path.resolve(__dirname,'../validation/update-38-browser');
const ids=['organisation_principia_cybernetica_project','publication_principia_cybernetica_web','concept_semantic_network','comparator_corpus_principia_cybernetica_web_dictionary','tradition_evolutionary_cybernetics','concept_metasystem_transition','approach_family_metasystem_transition_theory'];
const guide='/reading/knowledge-and-worldviews/',update='/updates/2026-11-06-principia/';
(async()=>{
 let server,browser;
 try{
  let base=(process.env.UPDATE_BASE_URL||'').replace(/\/$/,'');
  if(!base){server=http.createServer((req,res)=>{try{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname));assert(f===root||f.startsWith(root+path.sep));if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.json':'application/json','.js':'application/javascript','.css':'text/css','.svg':'image/svg+xml'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f))}catch{res.writeHead(404);res.end()}});await new Promise(r=>server.listen(0,'127.0.0.1',r));base='http://127.0.0.1:'+server.address().port}
  fs.mkdirSync(output,{recursive:true});browser=await chromium.launch(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH}:{});
  const request=await browser.newContext();const data=await (await request.request.get(base+'/assets/public-data.json')).json();assert.equal(data.meta.release,'0.41');const journey=data.journeys.find(j=>j.connection_pass==='principia_20261106');assert(journey);await request.close();
  const routes=[guide,update,...ids.map(id=>'/entries/'+id+'/'),'/journeys/'+journey.id+'/', '/', '/library/','/learning/','/updates/'];const checked=[];
  for(const width of [1440,390]){const context=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text()+' ['+m.location().url+']')});
   for(const route of routes){const response=await page.goto(base+route);assert.equal(response.status(),200,route);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow '+route+' '+width);const dot=page.getByRole('link',{name:'Open updates',exact:true});assert(await dot.isVisible(),route);assert(await dot.getAttribute('href'));const pos=await dot.evaluate(e=>{let r=e.getBoundingClientRect(),s=getComputedStyle(e);return {right:r.right,bottom:r.bottom,position:s.position}});assert.equal(pos.position,'fixed');assert(Math.abs(pos.right-width)<3&&Math.abs(pos.bottom-900)<3,route+' dot');
    if(['/','/library/','/learning/','/updates/'].includes(route))assert(await page.locator('a[href="'+guide+'"]').count(),route+' guide link');
    if(route===guide){assert(await page.locator('a[href="'+update+'register.json"]').count());assert(await page.locator('a[href="'+update+'primary-traces.json"]').count());assert((await page.locator('body').innerText()).toLowerCase().includes('editorial acceptance'));for(const id of ids)assert(await page.locator('a[href*="'+id+'"]').count(),id)}
    if(route===update)assert(await page.locator('a[href="'+guide+'"]').count());
    if(route.startsWith('/entries/'))assert(await page.getByRole('heading',{name:'Sources and passage locators',exact:true}).count());
    checked.push({route,width});
   }
   assert.deepEqual(errors,[]);await page.goto(base+guide);await page.screenshot({path:path.join(output,'guide-'+width+'.png'),fullPage:true});await page.goto(base+update);await page.screenshot({path:path.join(output,'update-'+width+'.png'),fullPage:true});await context.close();
  }
  fs.writeFileSync(path.join(output,'report.json'),JSON.stringify({release:'0.41',routes:checked,passed:true},null,2));console.log('0.38 browser passed:',checked.length,'desktop/mobile routes, links, and fixed updates control.');
 }finally{if(browser)await browser.close();if(server)await new Promise(r=>server.close(r))}
})().catch(e=>{console.error(e);process.exitCode=1});
