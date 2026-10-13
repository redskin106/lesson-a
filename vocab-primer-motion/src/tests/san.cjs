function sanitizeDeck(deck) {
  var FREE = /sentence|transl|note|hint|text|caption|name|lesson|title/i, FILE = /image|audio|video|src|poster|url|thumb|animation/i;
  var BAD_SCHEME = /^\s*(?!https?:|data:(image|audio|video)\/|clip:|blob:)[a-z][a-z0-9+.\-]*:/i;
  function clean(s, key, free) {
    if (FILE.test(key)) return BAD_SCHEME.test(s) ? '' : s.replace(/[\u0000-\u001f\u007f<>"'`\\]/g, '');
    s = s.replace(/[\u0000-\u001f\u007f<>\\]/g, '').replace(/"/g, '\u201d').replace(/`/g, '\u2019');
    return free ? s : s.replace(/'/g, '\u2019');
  }
  function walk(o, key, free) {
    if (typeof o === 'string') return clean(o, key, free);
    if (Array.isArray(o)) return o.map(function (x) { return walk(x, key, free); });
    if (o && typeof o === 'object') { var out = {}; Object.keys(o).forEach(function (k) { out[k] = walk(o[k], k, free || FREE.test(k)); }); return out; }
    return o;
  }
  return walk(deck, '', false);
}

const fs=require('fs');const dir=require('path').join(__dirname,'../../../vocab-primer')+'/';
let tot=0;
for(const f of fs.readdirSync(dir).filter(x=>x.endsWith('.json'))){
 const d=JSON.parse(fs.readFileSync(dir+f));const s=sanitizeDeck(d);
 const a=[],b=[];(function w(x,y,p){if(typeof x==='string'){if(x!==y)a.push(p+': '+x.slice(0,70)+' => '+y.slice(0,70))}else if(x&&typeof x==='object')Object.keys(x).forEach(k=>w(x[k],y[k],p+'.'+k))})(d,s,'');
 console.log(f,'changed',a.length);a.slice(0,6).forEach(l=>console.log('  ',l));tot+=a.length}
