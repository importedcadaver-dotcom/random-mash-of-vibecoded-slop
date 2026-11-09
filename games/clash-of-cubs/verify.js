const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const start = html.indexOf('<script>') + '<script>'.length;
const end = html.indexOf('</script>', start);
assert.ok(start >= 8 && end > start, 'inline game script exists');
const source = html.slice(start, end);
try { new Function(source); }
catch (error) {
  try { new Function(source.replace(/\}\)\(\);\s*$/, '')); console.error('removing IIFE close makes syntax valid'); } catch (e) { console.error('IIFE close removal:', e.message); }
  source.split(/\r?\n/).forEach((line, i) => { if (line.includes('function ')) { try { new Function(line); } catch (e) { if (!e.message.includes('Unexpected end')) console.error(`function line ${i + 1}: ${e.message}`); } } });
  const cuts = [...source.matchAll(/\nfunction /g)].map(m => m.index);
  for (const [index, cut] of cuts.entries()) {
    try { new Function(`${source.slice(0, cut)}\n})();`); }
    catch (prefixError) { if (prefixError.message.includes('Unexpected token')) { console.error(`unexpected token before function ${index + 1}: ${prefixError.message}`); break; } }
  }
  throw error;
}
assert.equal(html.includes('https://'), false, 'game does not depend on external network resources');

class Element {
  constructor(dataset = {}) { this.dataset = dataset; this.innerHTML = ''; this.onclick = null; this.textContent = ''; this.classList = { toggle() {} }; }
}
class Document {
  constructor() {
    this.nodes = Object.fromEntries(['#resources', '#dayrail', '#crumb', '#view', '#modalroot', '#toastroot'].map(k => [k, new Element()]));
    this.nav = ['den', 'train', 'raid', 'collection'].map(page => new Element({ page }));
    this.cache = new Map();
    this.nav.forEach(node => node.onclick = null);
  }
  querySelector(selector) {
    if (this.nodes[selector]) return this.nodes[selector];
    return this.querySelectorAll(selector)[0] || null;
  }
  querySelectorAll(selector) {
    if (selector === '.nav button' || selector === '[data-page]') return this.nav;
    const attr = selector.match(/^\[data-([\w-]+)\]$/)?.[1];
    if (!attr) return [];
    const html = selector === '[data-dismiss]' ? this.nodes['#modalroot'].innerHTML : this.nodes['#view'].innerHTML;
    if (html === undefined) throw new Error(`No HTML source for ${selector}; document nodes: ${Object.keys(this.nodes).join(', ')}`);
    const cacheKey = `${selector}|${html}`;
    if (this.cache.has(cacheKey)) return this.cache.get(cacheKey);
    const tags = html.match(/<[^>]+>/g) || [];
    const result = [];
    for (const tag of tags) {
      const dataset = {};
      for (const m of tag.matchAll(/data-([\w-]+)(?:=(['"])(.*?)\2)?/g)) dataset[m[1].replace(/-([a-z])/g, (_, c) => c.toUpperCase())] = m[3] ?? '';
      if (Object.hasOwn(dataset, attr.replace(/-([a-z])/g, (_, c) => c.toUpperCase()))) result.push(new Element(dataset));
    }
    this.cache.set(cacheKey, result);
    return result;
  }
}
function newGame() {
  const document = new Document();
  const store = new Map();
  const localStorage = { getItem: k => store.has(k) ? store.get(k) : null, setItem: (k,v) => store.set(k,v), removeItem: k => store.delete(k) };
  vm.runInNewContext(source, { document, localStorage, window: { confirm: () => true }, setTimeout: () => 0, console });
  return { document, store };
}
function click(doc, selector, value) {
  const attr = selector.slice(6, -1).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
  const item = doc.querySelectorAll(selector).find(n => n.dataset[attr] === value);
  assert.ok(item, `found ${selector}=${value}`);
  assert.equal(typeof item.onclick, 'function', `${selector}=${value} is wired`);
  item.onclick();
}

// Full success loop: upgrade, recruit a specialist, raid, gain supplies, keep survivors, progress, defend.
{
  const { document, store } = newGame();
  click(document, '[data-dismiss]', '');
  click(document, '[data-build]', 'nursery');
  let save = JSON.parse(store.get('clash-cubs-save'));
  assert.equal(save.build.nursery, 2, 'den building upgrade is saved');
  click(document, '[data-page]', 'train');
  click(document, '[data-train]', 'screecher');
  save = JSON.parse(store.get('clash-cubs-save'));
  assert.equal(save.roster.screecher, 1, 'trained cub joins roster');
  click(document, '[data-page]', 'raid');
  assert.match(document.nodes['#view'].innerHTML, /MAPLE-MOON OUTPOST/);
  click(document, '[data-pick]', 'roller');
  click(document, '[data-target]', 'wall');
  click(document, '[data-act]', 'deploy');
  assert.match(document.nodes['#view'].innerHTML, /crashes into the wall/);
  click(document, '[data-pick]', 'climber');
  click(document, '[data-target]', 'honey');
  click(document, '[data-act]', 'deploy');
  click(document, '[data-pick]', 'sleepy');
  click(document, '[data-target]', 'honey');
  click(document, '[data-act]', 'deploy');
  click(document, '[data-pick]', 'screecher');
  click(document, '[data-target]', 'toy');
  click(document, '[data-act]', 'deploy');
  assert.match(document.nodes['#modalroot'].innerHTML, /RAID COMPLETE/);
  save = JSON.parse(store.get('clash-cubs-save'));
  assert.equal(save.wins, 1, 'clearing two targets wins raid');
  assert.equal(save.roster.roller, 1, 'surviving cub returns to roster');
  assert.ok(save.res.honey > 80, 'raid loot increases honey after training costs');
  assert.equal(save.day, 2, 'raid advances day');
  click(document, '[data-dismiss]', '');
  click(document, '[data-act]', 'end-day');
  save = JSON.parse(store.get('clash-cubs-save'));
  assert.equal(save.day, 3, 'end-day advances progression');
  assert.ok(save.res.berries > 84, 'daily patrol yields a berry basket');
}

// Emotional loss path: the scripted scene appears without visual gore and records a lasting casualty.
{
  const { document, store } = newGame();
  click(document, '[data-dismiss]', '');
  click(document, '[data-page]', 'raid');
  click(document, '[data-pick]', 'roller'); click(document, '[data-target]', 'berries'); click(document, '[data-act]', 'deploy');
  click(document, '[data-pick]', 'climber'); click(document, '[data-target]', 'honey'); click(document, '[data-act]', 'deploy');
  click(document, '[data-pick]', 'sleepy'); click(document, '[data-target]', 'store'); click(document, '[data-act]', 'deploy');
  assert.match(document.nodes['#modalroot'].innerHTML, /littermate fell/);
  assert.match(document.nodes['#modalroot'].innerHTML, /scared.*mad.*miss her/);
  const save = JSON.parse(store.get('clash-cubs-save'));
  assert.equal(save.casualties, 1, 'fallen cub is remembered as a permanent loss');
  assert.match(document.nodes['#modalroot'].innerHTML, /A quiet moment/);
}

// Signature unit abilities appear in gameplay feedback.
{
  const { document } = newGame();
  click(document, '[data-dismiss]', '');
  click(document, '[data-page]', 'train');
  click(document, '[data-train]', 'screecher');
  click(document, '[data-train]', 'tunnel');
  click(document, '[data-page]', 'raid');
  click(document, '[data-pick]', 'climber'); click(document, '[data-target]', 'honey'); click(document, '[data-act]', 'deploy');
  assert.match(document.nodes['#view'].innerHTML, /climbs over the wall/);
  assert.doesNotMatch(document.nodes['#view'].innerHTML, /swats at the team/);
  click(document, '[data-pick]', 'screecher'); click(document, '[data-target]', 'guard'); click(document, '[data-act]', 'deploy');
  assert.match(document.nodes['#view'].innerHTML, /mighty screech/);
  assert.match(document.nodes['#view'].innerHTML, /guard blinks/);
  click(document, '[data-pick]', 'roller'); click(document, '[data-target]', 'toy'); click(document, '[data-act]', 'deploy');
  click(document, '[data-pick]', 'tunnel'); click(document, '[data-target]', 'wall'); click(document, '[data-act]', 'deploy');
  assert.match(document.nodes['#view'].innerHTML, /burrows under the wall/);
  click(document, '[data-pick]', 'sleepy'); click(document, '[data-target]', 'store'); click(document, '[data-act]', 'deploy');
  assert.match(document.nodes['#modalroot'].innerHTML, /wakes the sleepy cub/);
}

console.log('PASS: offline source and JavaScript syntax');
console.log('PASS: building upgrade, training, specialist raid, loot, survivor return, day progression, daily defense');
console.log('PASS: scripted loss scene, fear/grief text, and saved casualty');
console.log('PASS: climber bypass, screecher stun, tunnel breach, and sleepy timing');

