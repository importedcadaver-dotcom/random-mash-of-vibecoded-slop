const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const root = __dirname;
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const gameSource = fs.readFileSync(path.join(root, 'game.js'), 'utf8');
assert.match(html, /style\.css/);
assert.match(html, /game\.js/);
new Function(gameSource);
assert.equal(/https?:\/\//i.test(html + gameSource + fs.readFileSync(path.join(root,'style.css'),'utf8')), false, 'game has no external network dependencies');

class Element {
  constructor(dataset = {}) { this.dataset = dataset; this.innerHTML = ''; this.onclick = null; this.textContent = ''; this.classList = { toggle() {} }; }
}
class Document {
  constructor() {
    this.nodes = Object.fromEntries(['#resources','#dayrail','#crumb','#view','#modalroot','#toastroot'].map(k=>[k,new Element()]));
    this.nav = ['den','build','train','raidMap','collection'].map(page=>new Element({page}));
    this.cache = new Map();
  }
  querySelector(selector) { if(this.nodes[selector])return this.nodes[selector];return this.querySelectorAll(selector)[0]||null; }
  querySelectorAll(selector) {
    if(selector==='.nav button'||selector==='[data-page]')return this.nav;
    const attr=selector.match(/^\[data-([\w-]+)\]$/)?.[1];if(!attr)return [];
    const markup=selector==='[data-dismiss]'?this.nodes['#modalroot'].innerHTML:this.nodes['#view'].innerHTML;
    const key=`${selector}|${markup}`;if(this.cache.has(key))return this.cache.get(key);
    const result=[];for(const tag of markup.match(/<[^>]+>/g)||[]){const dataset={};for(const m of tag.matchAll(/data-([\w-]+)(?:=(['"])(.*?)\2)?/g))dataset[m[1].replace(/-([a-z])/g,(_,c)=>c.toUpperCase())]=m[3]??'';if(Object.hasOwn(dataset,attr.replace(/-([a-z])/g,(_,c)=>c.toUpperCase())))result.push(new Element(dataset))}this.cache.set(key,result);return result;
  }
}
function newGame(existingStore=new Map()) {
  const document=new Document(),store=existingStore;
  const localStorage={getItem:k=>store.has(k)?store.get(k):null,setItem:(k,v)=>store.set(k,v),removeItem:k=>store.delete(k)};
  let beat=null;
  vm.runInNewContext(gameSource,{document,localStorage,window:{confirm:()=>true},setTimeout:()=>0,clearTimeout:()=>{},setInterval:fn=>{beat=fn;return 1},clearInterval:()=>{beat=null},console});
  return {document,store,advance:()=>{if(beat)beat()}};
}
function click(doc,selector,key,value) {
  const attr=key||selector.slice(6,-1).replace(/-([a-z])/g,(_,c)=>c.toUpperCase());
  const item=doc.querySelectorAll(selector).find(node=>node.dataset[attr]===value);
  assert.ok(item,`found ${selector} ${attr}=${value}`);assert.equal(typeof item.onclick,'function',`${selector} is wired`);item.onclick();
}
function clickUnitAction(doc,action,type) {
  const item=doc.querySelectorAll('[data-act]').find(node=>node.dataset.act===action&&node.dataset.unit===type);
  assert.ok(item,`found unit action ${action} for ${type}`);assert.equal(typeof item.onclick,'function',`${action}/${type} is wired`);item.onclick();
}
function deploy(doc,type,edge='south') {click(doc,'[data-troop]','troop',`${type}-1`);click(doc,'[data-edge]','edge',edge)}
function advanceUntil(game,condition,max=50) {for(let i=0;i<max&&!condition();i++)game.advance();assert.ok(condition(),'battle progressed to expected outcome')}
function saved(store){return JSON.parse(store.get('clash-cubs-save-v2'))}
function dismissWelcome(doc){click(doc,'[data-dismiss]','dismiss','')}

// Build placement, upgrades, all unit types, squad assignment, and save/load.
{
  const game=newGame(),{document,store}=game;dismissWelcome(document);
  click(document,'[data-page]','page','build');
  click(document,'[data-select-build]','selectBuild','berry');
  assert.match(document.nodes['#view'].innerHTML,/Tap an open meadow plot/);
  assert.match(document.nodes['#view'].innerHTML,/class="village-svg"/);
  assert.match(document.nodes['#view'].innerHTML,/ATTACK!/);
  click(document,'[data-cell]','cell','0,1');
  let data=saved(store),patches=data.buildings.filter(b=>b.type==='berry');
  assert.equal(patches.length,2,'new producer placed on an empty plot');
  const placed=patches.find(b=>b.x===0&&b.y===1);assert.ok(placed);
  click(document,'[data-act]','act','upgrade');
  data=saved(store);assert.equal(data.buildings.find(b=>b.id===placed.id).level,2,'selected building upgrades');
  click(document,'[data-page]','page','train');
  for(const type of ['roller','climber','screecher','tunnel','sleepy'])clickUnitAction(document,'train',type);
  clickUnitAction(document,'squad-up','screecher');clickUnitAction(document,'squad-up','tunnel');
  data=saved(store);
  assert.equal(data.collection.length,5,'training records each specialist in the Bear Book');
  assert.equal(Object.values(data.squad).reduce((a,b)=>a+b,0),5,'squad capacity accommodates five cub types');
  const reloaded=newGame(store);
  assert.match(reloaded.document.nodes['#view'].innerHTML,/MOSSWOOD FAMILY DEN/,'saved game loads back into the den');
  assert.equal(saved(store).buildings.filter(b=>b.type==='berry').length,2,'placed building survives reload');
}

// Successful raids, unlocks, five cub abilities, resource rewards, and night defense.
{
  const game=newGame(),{document,store}=game;dismissWelcome(document);
  click(document,'[data-page]','page','train');
  for(const type of ['screecher','tunnel'])clickUnitAction(document,'train',type);
  clickUnitAction(document,'squad-up','screecher');clickUnitAction(document,'squad-up','tunnel');
  let before=saved(store).resources.honey;
  click(document,'[data-page]','page','raidMap');click(document,'[data-rival]','rival','maple');
  assert.match(document.nodes['#view'].innerHTML,/Maple-Moon Outpost/);
  deploy(document,'climber','north');deploy(document,'screecher','west');
  for(let i=0;i<5;i++)game.advance();
  assert.ok(saved(store).activeRaid.guardStun>0,'screecher stuns the guard during a live raid');
  assert.match(document.nodes['#view'].innerHTML,/cubs move|Cub behavior/,'raid communicates autonomous combat');
  click(document,'[data-act]','act','wake-sleepy');deploy(document,'sleepy','south');
  advanceUntil(game,()=>/RAID COMPLETE/.test(document.nodes['#modalroot'].innerHTML));
  assert.match(document.nodes['#modalroot'].innerHTML,/RAID COMPLETE/,'two loot spots complete the raid');
  let data=saved(store);
  assert.equal(data.wins,1,'raid win unlocks the next rival');assert.ok(data.resources.honey>before,'raid honey reaches the den');assert.ok(data.resources.berries>92,'raid berries reach the den');
  click(document,'[data-dismiss]','dismiss','');click(document,'[data-page]','page','raidMap');click(document,'[data-rival]','rival','cedar');
  deploy(document,'screecher','west');deploy(document,'roller','north');deploy(document,'tunnel','east');deploy(document,'climber','south');click(document,'[data-act]','act','wake-sleepy');deploy(document,'sleepy','west');
  advanceUntil(game,()=>/RAID COMPLETE/.test(document.nodes['#modalroot'].innerHTML));
  const fight=saved(store);assert.ok(fight.wins>=2,'autonomous specialist squad wins the second rival');
  assert.ok(!fight.activeRaid,'raid results close the battle');
  assert.equal(saved(store).wins,2,'second rival advances progression');
  click(document,'[data-dismiss]','dismiss','');click(document,'[data-page]','page','den');
  data=saved(store);data.resources.honey=400;store.set('clash-cubs-save-v2',JSON.stringify(data));
  const night=newGame(store).document;
  click(night,'[data-act]','act','end-day');
  data=saved(store);
  assert.equal(data.day,2,'night advances the day');assert.equal(data.resources.honey,400,'hive production respects the storage cap');
  assert.match(data.history[0].text,/overflowed/,'excess production is logged');
  assert.match(night.nodes['#modalroot'].innerHTML,/stores are safe/,'home defenses stop the scripted night raid');
}

// Cub losses persist in the journal and are shown with grief, without graphic injury.
{
  const seed=new Map();seed.set('clash-cubs-save-v2',JSON.stringify({day:1,wins:2,casualties:0,nextBuildId:30,resources:{honey:150,berries:92,fish:72,toys:42,wood:205},buildings:[{id:1,type:'nursery',x:2,y:1,level:1},{id:2,type:'training',x:4,y:1,level:1},{id:3,type:'hive',x:1,y:0,level:1},{id:4,type:'berry',x:3,y:0,level:1},{id:5,type:'pond',x:5,y:0,level:1},{id:6,type:'toyshop',x:6,y:1,level:1},{id:7,type:'mill',x:1,y:4,level:1},{id:8,type:'storage',x:5,y:3,level:1},{id:9,type:'wall',x:2,y:2,level:1},{id:10,type:'wall',x:4,y:2,level:1},{id:11,type:'wall',x:2,y:3,level:1},{id:12,type:'guard',x:6,y:3,level:1},{id:13,type:'trap',x:4,y:4,level:1},{id:14,type:'home',x:3,y:2,level:1}],roster:{roller:1,climber:1,screecher:0,tunnel:0,sleepy:1},squad:{roller:1,climber:1,screecher:0,tunnel:0,sleepy:1},collection:['roller','climber','sleepy'],history:[],activeRaid:null}));
  const game=newGame(seed),{document,store}=game;dismissWelcome(document);click(document,'[data-page]','page','raidMap');click(document,'[data-rival]','rival','river');
  deploy(document,'sleepy','south');advanceUntil(game,()=>saved(store).casualties>=1,40);
  for(let i=0;i<75&&saved(store).activeRaid;i++)game.advance();
  const loss=saved(store);assert.ok(loss.casualties>=1,'dangerous advanced guards can cause a lasting cub loss');
  assert.match(document.nodes['#modalroot'].innerHTML,/frightened and grieving/);
}

console.log('PASS: build placement, upgrade, caps, training all five cubs, squad selection, save and reload');
console.log('PASS: two successful raids, rival unlocks, cub abilities, loot rewards, nightly production, home defense');
console.log('PASS: original offline source and non-graphic loss handling');

