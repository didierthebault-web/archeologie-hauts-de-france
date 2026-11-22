const {chromium}=require('../../soupotheque/node_modules/@playwright/test');
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert');
const root=path.resolve(__dirname,'..');
const server=http.createServer((req,res)=>{const p=path.join(root,decodeURIComponent(req.url.split('?')[0]==='/'?'/index.html':req.url.split('?')[0]));if(!p.startsWith(root+path.sep)){res.writeHead(403);res.end();return}fs.readFile(p,(e,b)=>{res.writeHead(e?404:200,{'Content-Type':p.endsWith('.webp')?'image/webp':p.endsWith('.json')?'application/json':'text/html; charset=utf-8'});res.end(e?'missing':b)})});
(async()=>{
 await new Promise(r=>server.listen(5194,'127.0.0.1',r));
 const browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH||'C:/Users/didie/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe'});const results={date:'2026-11-22',checks:[],viewports:[],errors:[],externalRequests:[]};
 try{
  const page=await browser.newPage({viewport:{width:1920,height:1080}});page.on('pageerror',e=>results.errors.push(String(e)));
  await page.route('**/*',route=>{const u=route.request().url();if(/^https?:/.test(u)&&!u.startsWith('http://127.0.0.1:5194/')){results.externalRequests.push(u);return route.abort()}return route.continue()});
  await page.clock.install({time:new Date('2026-11-22T12:00:00Z')});await page.clock.pauseAt(new Date('2026-11-22T12:00:01Z'));await page.goto('http://127.0.0.1:5194/');
  assert.equal(await page.locator('#speed').count(),0);assert.equal(await page.locator('.feature-card').count(),5);
  assert.equal(await page.locator('.feature-card.appear').count(),0);
  await page.clock.runFor(2299);assert.equal(await page.locator('.feature-card.appear').count(),0);
  await page.clock.runFor(1);assert.equal(await page.locator('.feature-card.appear').count(),1);results.checks.push('Intervalle initial réel : 2300 ms, premier groupe de cinq cartes');
  await page.click('#play');const count=await page.locator('#count').innerText();await page.clock.runFor(10000);assert.equal(await page.locator('#count').innerText(),count);results.checks.push('Pause sans progression');
  await page.click('#play');await page.clock.runFor(2300);assert.equal(await page.locator('.feature-card.appear').count(),2);results.checks.push('Reprise');
  await page.clock.runFor(5*2300);assert.equal(await page.locator('.mini').count(),5);assert.equal(await page.locator('#speed').count(),0);assert.equal(await page.locator('.feature-card').count(),5);results.checks.push('Transfert du premier groupe et conservation dans la galerie');
  await page.click('#play'); await page.click('#prev');assert.equal(await page.locator('.mini').count(),0);await page.click('#next');assert.equal(await page.locator('.mini').count(),5);results.checks.push('Navigation précédent / suivant conforme à V2');
  await page.click('#restart');assert.equal(await page.locator('.mini').count(),0);assert.equal(await page.locator('.feature-card.appear').count(),1);results.checks.push('Redémarrage');
  await page.click('#play');await page.clock.runFor(75*2300);
  assert.equal(await page.locator('.mini').count(),41);assert.equal(await page.locator('#count').innerText(),'41 / 41 publications');assert((await page.locator('#groupLabel').innerText()).includes('entièrement'));results.checks.push('Neuf groupes jusqu’à 41/41 et arrêt final');
  await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0));
  const pubs=JSON.parse(fs.readFileSync(path.join(root,'publications.json'),'utf8'));
  const anchors=await page.locator('.mini').evaluateAll(a=>a.map(x=>({href:x.href,target:x.target})));
  assert.equal(anchors.length,41);for(let i=0;i<41;i++){assert.equal(anchors[i].href,pubs[i].url_notice_bibdoc||pubs[i].url_publication);assert.equal(anchors[i].target,'_blank')}
  assert.equal(anchors.filter(a=>a.href.startsWith('https://bibdoc.culture.gouv.fr/recherche/viewnotice/')).length,39);
  results.checks.push('41 liens de galerie contrôlés : 39 notices Bibdoc fournies et 2 notices ministère conservées');
  const pics=await page.locator('.mini img').evaluateAll(a=>a.map(i=>({src:i.getAttribute('src'),width:i.naturalWidth,height:i.naturalHeight,fit:getComputedStyle(i).objectFit})));
  assert.equal(new Set(pics.map(p=>p.src)).size,41);assert(pics.every(p=>p.fit==='contain'));results.images=pics;results.checks.push('41 images locales distinctes décodées, proportions conservées, culture.gouv.fr bloqué');
  for(const size of [{width:1920,height:1080},{width:1366,height:768},{width:600,height:900}]){
   await page.setViewportSize(size);await page.clock.runFor(2000);await page.evaluate(()=>window.scrollTo(0,document.body.scrollHeight));await new Promise(r=>setTimeout(r,200));await page.evaluate(()=>window.scrollTo(0,0));await new Promise(r=>setTimeout(r,800));const name=`rendu-${size.width}x${size.height}.png`;await page.screenshot({path:path.join(root,'documentation',name),fullPage:true});results.viewports.push({...size,screenshot:name,horizontalOverflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)});
  }
  await page.setViewportSize({width:1920,height:1080});await page.click('#restart');await page.click('#play');await page.clock.runFor(4*2300);await page.click('#play');await page.clock.runFor(2000);await new Promise(r=>setTimeout(r,1500));await page.screenshot({path:path.join(root,'documentation','rendu-cinq-cartes.png'),fullPage:true});
  const filePage=await browser.newPage();await filePage.goto('file:///'+path.join(root,'index.html').replaceAll('\\','/'));await filePage.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth));results.checks.push('Ouverture file:// index.html sans chargement JSON externe');
  const auto=await browser.newPage();await auto.setOfflineMode?.(true);
  await auto.goto('file:///'+path.join(root,'autonome.html').replaceAll('\\','/'));await auto.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth));assert((await auto.locator('img').first().getAttribute('src')).startsWith('data:'));results.checks.push('Version autonome ouverte en file://, images embarquées');
  await page.click('#restart');await page.locator('.feature-card img').first().evaluate(i=>i.src='images/inexistante-test.webp');await page.waitForFunction(()=>document.querySelector('.missing')?.textContent==='Couverture non disponible');results.checks.push('Image locale manquante : remplacement explicite');
  assert.equal(results.errors.length,0);assert.equal(results.externalRequests.length,0);results.status='OK';
 }finally{fs.writeFileSync(path.join(root,'documentation/tests-navigateur.json'),JSON.stringify(results,null,2));await browser.close();server.close()}
 console.log(JSON.stringify(results.checks,null,2));
})().catch(e=>{console.error(e);server.close();process.exitCode=1});

