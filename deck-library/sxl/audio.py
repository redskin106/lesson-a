"""Recorded clips by exact text. register(dir, texts): match each mp3 to a deck text (file name = the text with punctuation dropped, optional tag words in front),
build_interactive injects window.SXLA and SXLsay(text,cb). Anything without a clip falls back to the browser voice."""
import re, base64, pathlib
CLIPS = {}
def norm(t): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]',' ',t.lower())).strip()
def register(folder, texts):
    keys = {norm(t): t for t in texts}
    for p in sorted(pathlib.Path(folder).glob('*.mp3')):
        stem = re.sub(r'^[0-9a-f]{8}-','',p.stem); fk = norm(stem.replace('_',' '))
        hit = [k for k in keys if fk == k] or [k for k in keys if fk.endswith(' '+k)]
        if hit: CLIPS[max(hit,key=len)] = p
        else: print('audio: no deck text for', p.name)
def script():
    if not CLIPS: return ''
    m = ','.join(f'"{k}":"data:audio/mpeg;base64,{base64.b64encode(p.read_bytes()).decode()}"' for k,p in CLIPS.items())
    return ('<script>window.SXLA={'+m+'};window.SXLsay=function(t,cb){var k=String(t).toLowerCase().replace(/[^a-z0-9 ]/g," ").replace(/\\s+/g," ").trim(),u=window.SXLA[k];if(!u)return false;'
            'try{if(window.__sxla){window.__sxla.pause()}var a=new Audio(u);window.__sxla=a;a.onended=function(){if(cb)cb()};a.onerror=function(){if(cb)cb()};a.play()["catch"](function(){if(cb)cb()});return true}catch(e){return false}};</script>')
