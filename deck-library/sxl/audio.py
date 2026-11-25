"""Recorded clips by exact text. register(dir, texts): match each mp3 to a deck text (file name = the text with punctuation dropped, optional tag words in front),
build_interactive injects window.SXLA and SXLsay(text,cb). Anything without a clip falls back to the browser voice."""
import re, base64, pathlib
CLIPS = {}
SFX = {}   # name -> [files]; name_1.mp3, name_2.mp3 are alternate takes of 'name'
def register_sfx(folder):
    for p in sorted(pathlib.Path(folder).glob('*.mp3')):
        SFX.setdefault(re.sub(r'_\d+$','',p.stem),[]).append(p)
def norm(t): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]',' ',t.lower())).strip()
def register(folder, texts):
    keys = {norm(t): t for t in texts}
    mf = pathlib.Path(folder) / 'manifest.json'
    if mf.exists():  # clips made by tts-tool.html: file = ID.mp3 (or slug--ID.mp3), text = the manifest row's text
        import json
        for a in json.loads(mf.read_text(encoding='utf-8')).get('assets', []):
            k = norm(a['text'])
            hit = [p for p in pathlib.Path(folder).glob('*.mp3') if p.stem == a['id'] or p.stem.endswith('--' + a['id'])]
            if hit and k in keys: CLIPS[k] = hit[0]
            elif hit: print('audio: manifest text not on any slide:', a['id'])
    for p in sorted(pathlib.Path(folder).glob('*.mp3')):
        if p in CLIPS.values(): continue
        stem = re.sub(r'^[0-9a-f]{8}-','',p.stem); fk = norm(stem.replace('_',' '))
        hit = [k for k in keys if fk == k] or [k for k in keys if fk.endswith(' '+k)]
        if hit: CLIPS[max(hit,key=len)] = p
        else: print('audio: no deck text for', p.name)
def script():
    sf=''
    if SFX: sf='<script>window.SXLS={'+','.join('"%s":[%s]'%(k,','.join('"data:audio/mpeg;base64,'+base64.b64encode(p.read_bytes()).decode()+'"' for p in v)) for k,v in SFX.items())+'};</script>'
    if not CLIPS: return sf
    m = ','.join(f'"{k}":"data:audio/mpeg;base64,{base64.b64encode(p.read_bytes()).decode()}"' for k,p in CLIPS.items())
    return sf+('<script>window.SXLA={'+m+'};window.SXLsay=function(t,cb){var k=String(t).toLowerCase().replace(/[^a-z0-9 ]/g," ").replace(/\\s+/g," ").trim(),u=window.SXLA[k];if(!u)return false;'
            'try{if(window.__sxla){window.__sxla.pause()}var a=new Audio(u);window.__sxla=a;a.onended=function(){if(cb)cb()};a.onerror=function(){if(cb)cb()};a.play()["catch"](function(){if(cb)cb()});return true}catch(e){return false}};</script>')
