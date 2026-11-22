const {chromium}=require('../../soupotheque/node_modules/@playwright/test');
const fs=require('fs'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'..');const notices=JSON.parse(fs.readFileSync(path.join(root,'notices.json'),'utf8'));
(async()=>{const b=await chromium.launch({headless:true,executablePath:'C:/Users/didie/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe'});const result={notices:Object.keys(notices).length,checks:[],errors:[]};try{
 assert.equal(Object.keys(notices).length,39);
 for(const file of ['index.html','autonome.html']){
  const p=await b.newPage({viewport:{width:1366,height:768},reducedMotion:'reduce'});p.on('pageerror',e=>result.errors.push(String(e)));await p.goto('file:///'+path.join(root,file).replaceAll('\\','/'));
  assert.equal(await p.locator('#speed').count(),0);
  assert.equal(await p.evaluate(()=>Object.keys(NOTICES_CAPTURE).length),39);
  for(const [number,n] of Object.entries(notices)){
   await p.evaluate(num=>{stop();completed=0;drawArchive();index=Math.floor(PUBS.findIndex(x=>x.number===num)/SIZE);drawFeatured();shown=groups().length;update()},Number(number));
   const card=p.locator('.feature-card').filter({has:p.locator('.meta b',{hasText:new RegExp('^N° '+number+'$')})});await card.click();
   const dialog=p.locator('dialog');await dialog.waitFor({state:'visible'});assert.equal(await dialog.locator('h2').innerText(),n.titre);
   const values=await dialog.locator('dd').allTextContents();for(const v of [n.auteurs,n.description,n.resume,n.sujets])assert(values.includes(v),number+' contenu manquant');
   if(n.collaborateurs)assert(values.includes(n.collaborateurs));if(n.anomalie)assert(values.includes(n.anomalie));
   assert.equal(await p.locator('.mini').count(),0);assert.equal(await p.evaluate(()=>playing),false);
   assert.equal(await dialog.evaluate(d=>d.scrollWidth>d.clientWidth),false);
   if(file==='index.html'&&['41','27','8'].includes(number))await p.screenshot({path:path.join(root,'documentation',`notice-${number}-integree.png`)});
   await p.keyboard.press('Escape');await dialog.waitFor({state:'hidden'});
  }
  await p.evaluate(()=>{completed=PUBS.length;drawArchive()});assert.equal(await p.locator('.mini.notice-available').count(),39);
  for(const [number,n] of Object.entries(notices)){
   const card=p.locator('.mini').filter({has:p.locator('.number',{hasText:new RegExp('^N° '+number+'$')})});await card.click();assert.equal(await p.locator('dialog h2').innerText(),n.titre);await p.getByRole('button',{name:'Fermer ×'}).click();await p.locator('dialog').waitFor({state:'hidden'});
  }
  await p.setViewportSize({width:600,height:900});await p.locator('.mini').filter({has:p.locator('.number',{hasText:/^N° 27$/})}).click();assert.equal(await p.locator('dialog').evaluate(d=>d.scrollWidth>d.clientWidth),false);if(file==='index.html')await p.screenshot({path:path.join(root,'documentation','notice-27-mobile.png')});
  result.checks.push(file+' : 39 fiches centrales, 39 fiches de galerie, contenus et affichage étroit vérifiés');await p.close();
 }
 assert.equal(result.errors.length,0);result.status='OK';fs.writeFileSync(path.join(root,'documentation/tests-notices-completes.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));
}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
