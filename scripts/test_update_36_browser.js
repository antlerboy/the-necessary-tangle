/* Read-only release36 checks of situated inquiry, readable entries, and practice. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const http=require('node:http');
const root=path.resolve(__dirname,'../docs');
const output=path.resolve(__dirname,'../validation/update-36-browser');
const release='0.40';
const cohort='depth_20261106';
const guide='/reading/from-observation-to-action/';
const update='/updates/2026-11-06/';
const journeyId='journey_observation_judgement_action';
const entryIds=['concept_observer','concept_multiple_perspectives','concept_boundary_critique','concept_structure_agency','concept_autopoiesis','concept_autonomy'];
const labs=['critical-systems-heuristics','multi-methodology','ethics-and-power'];
const routesChecked=[];
const errors=[];
let server,browser;

function captureErrors(page,route,width){
  page.on('pageerror',error=>errors.push({route,width,message:error.message}));
}

async function common(page,base,route,width){
  const response=await page.goto(base+route);
  assert.equal(response.status(),200,route);
  assert.equal(await page.locator('h1').count(),1,route);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Horizontal overflow '+route+' at '+width);
  const updates=page.getByRole('link',{name:'Open updates',exact:true});
  assert(await updates.isVisible(),route+' updates control');
  assert(await updates.getAttribute('href'),route+' updates href');
  await page.keyboard.press('Tab');
  assert(await page.evaluate(()=>document.activeElement?.tagName==='A'&&Boolean(document.activeElement.getAttribute('href'))),'Keyboard destination needs a real link '+route);
}

async function main(){
  let base=(process.env.UPDATE_BASE_URL||'').replace(/\/$/,'');
  if(!base){
    server=http.createServer((req,res)=>{
      try{
        let file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://test').pathname));
        assert(file===root||file.startsWith(root+path.sep));
        if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');
        res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.js':'application/javascript','.json':'application/json','.css':'text/css'})[path.extname(file)]||'application/octet-stream');
        res.end(fs.readFileSync(file));
      }catch{res.writeHead(404);res.end();}
    });
    await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
    base='http://127.0.0.1:'+server.address().port;
  }
  fs.mkdirSync(output,{recursive:true});
  browser=await chromium.launch(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH}:{});
  const request=await browser.newContext();
  const dataResponse=await request.request.get(base+'/assets/public-data.json');
  assert.equal(dataResponse.status(),200);
  const data=await dataResponse.json();
  assert.equal(data.meta.release,release,'Test needs generated release 0.40');
  assert(data[cohort],'The new research cohort must be recorded');
  assert(data.depth_20261029,'The historical cohort remains recorded');
  const journey=data.journeys.find(row=>row.id===journeyId);
  assert(journey&&journey.steps.length>=2,'The new journey must have an actual sequence');
  for(const id of entryIds)assert(data.profiles.some(row=>row.node_id===id),'Developed profile '+id);
  const evidenceResponse=await request.request.get(base+update+'evidence.json');
  assert.equal(evidenceResponse.status(),200);
  const evidence=await evidenceResponse.json();
  assert.equal(evidence.date,'2026-11-06');
  assert.equal(evidence.practice.content_changes.length,3);
  assert.equal(evidence.practice.content_changes.reduce((n,row)=>n+row.added_rounds,0),6);
  assert.equal(evidence.practice.content_changes.reduce((n,row)=>n+row.added_checks,0),4);
  const packResponse=await request.request.get(base+'/systems-thinking/practice/assets/pack.json');
  assert.equal(packResponse.status(),200);
  const pack=await packResponse.json();
  for(const id of labs){
    const lab=pack.labs.find(row=>row.id===id);
    assert(lab&&lab.rounds.length===6,'Six current rounds for '+id);
    assert(lab.scope.includes('fictional'),'Original application labelled '+id);
  }
  await request.close();

  for(const width of[1440,390]){
    const context=await browser.newContext({viewport:{width,height:900},javaScriptEnabled:false,reducedMotion:'reduce'});
    const page=await context.newPage();
    captureErrors(page,'static reader',width);
    for(const route of[guide,update,...entryIds.map(id=>'/entries/'+id+'/'),'/journeys/'+journeyId+'/']){
      await common(page,base,route,width);
      if(route===guide){
        for(const id of['observation','judgement','action','limits','sources'])assert.equal(await page.locator('#'+id).count(),1,'Guide section '+id);
        for(const id of entryIds)assert(await page.locator('a[href="/#view=item&id='+id+'"]').count(),'Real atlas link '+id);
        for(const id of labs)assert(await page.locator('a[href^="/systems-thinking/practice/'+id+'/"]').count(),'Real practice link '+id);
        assert(await page.locator('a[href="/journeys/'+journeyId+'/"]').count(),'Real journey link');
        assert(await page.locator('#sources a[href^="http"]').count(),'Public primary-source links');
        assert(await page.locator('a[href="'+update+'evidence.json"]').count(),'Evidence download link');
      }
      if(route===update){
        assert((await page.locator('main').innerText()).includes('0.36'));
        assert(await page.locator('a[href="'+guide+'"]').count(),'Update links to reading');
      }
      if(route.startsWith('/entries/')){
        const id=route.split('/')[2];
        assert(await page.getByRole('heading',{name:'Sources and passage locators',exact:true}).count());
        assert.equal(await page.getByRole('link',{name:'Open the interactive entry',exact:true}).getAttribute('href'),'/#view=item&id='+id);
        const download=page.getByRole('link',{name:'Download the sourced record (JSON)',exact:true});
        const recordResponse=await context.request.get(new URL(await download.getAttribute('href'),page.url()).href);
        assert.equal(recordResponse.status(),200);
        const record=await recordResponse.json();
        assert.equal(record.entry.id,id);assert.equal(record.release,release);
        assert(record.sources.length>0&&record.evidence_locators.length>0,'Source and locator records '+id);
      }
      if(route.startsWith('/journeys/')){
        assert.equal(await page.locator('ol.journey > li').count(),journey.steps.length);
        assert(await page.locator('a[href="/#view=journeys&id='+journeyId+'&step=0"]').count(),'Journey has actual interactive href');
        assert(await page.locator('ol.journey a[href]').count()>=journey.steps.length);
      }
      const slug=route.replace(/^\//,'').replace(/\/$/,'').replaceAll('/','-');
      await page.screenshot({path:path.join(output,slug+'-'+width+'.png'),fullPage:true});
      routesChecked.push({route,width,javaScript:false});
    }
    await context.close();

    const active=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});
    const live=await active.newPage();
    captureErrors(live,'interactive reader',width);
    for(const id of labs){
      const route='/systems-thinking/practice/'+id+'/';
      await common(live,base,route,width);
      assert.equal(await live.locator('.steps > li').count(),6);
      for(const step of[5,6]){
        const row=live.locator('.steps > li').nth(step-1);
        assert.equal(await row.locator('details').getAttribute('open'),null);
        await row.locator('summary').click();
        assert(await row.locator('details[open]').count());
        assert((await row.locator('details[open]').innerText()).length>100);
        await row.screenshot({path:path.join(output,'practice-'+id+'-step'+step+'-'+width+'.png')});
      }
      const last=live.locator('form[data-check]').last();
      const correct=await last.getAttribute('data-correct');
      await last.locator('input[value="'+correct+'"]').check();
      await last.getByRole('button').click();
      assert((await last.locator('[data-result]').innerText()).length>15,'Current check feedback '+id);
      await live.getByRole('link',{name:'Task-only version',exact:true}).click();
      assert(live.url().endsWith('/worksheets/index.html#'+id));
      routesChecked.push({route,width,javaScript:true,added_rounds_checked:[5,6],check_feedback:true});
    }
    await live.goto(base+'/');
    assert.equal(await live.locator('#releaseBadge').innerText(),'Release '+release);
    assert(await live.locator('a[href^="'+guide+'"]').count(),'Home has real reading-guide link');
    assert(await live.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Home overflow '+width);
    await live.goto(base+'/#view=journeys&id='+journeyId+'&step=0');
    await live.locator('#journeyRunner h2').filter({hasText:journey.title}).waitFor();
    assert.equal(await live.getByRole('link',{name:'Read the whole journey',exact:true}).getAttribute('href'),'/journeys/'+journeyId+'/');
    assert.equal(await live.locator('#journeyRunner .step-card a').first().getAttribute('data-id'),journey.steps[0].node_id);
    await live.locator('#journeyNext').click();
    assert.equal(await live.locator('#journeyRunner .step-card a').first().getAttribute('data-id'),journey.steps[1].node_id);
    assert(new URL(live.url()).hash.includes('step=1'));
    assert(await live.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Interactive journey overflow '+width);
    await live.screenshot({path:path.join(output,'interactive-journey-'+width+'.png')});
    routesChecked.push({route:'/#view=journeys&id='+journeyId+'&step=0',width,javaScript:true,progressed_to_step:1});
    await active.close();
  }
  assert.deepEqual(errors,[],'Browser JavaScript errors');
  const report={release,cohort,historical_cohort_preserved:'depth_20261029',base,entry_ids:entryIds,journey:journeyId,practice_labs:labs,practice_added_rounds:6,practice_added_checks:4,routes:routesChecked,browser_errors:errors,passed:true};
  fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2)+'\n');
  console.log('0.36 browser passed: static source routes, six readable entries, journey progression, three deepened labs, keyboard links, desktop/mobile containment, and updates control.');
}
main().catch(error=>{console.error(error);process.exitCode=1;}).finally(async()=>{
  if(browser)await browser.close();
  if(server){server.closeAllConnections?.();await new Promise(resolve=>server.close(resolve));}
});
