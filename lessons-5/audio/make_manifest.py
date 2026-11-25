"""pack.txt (ID | [tag] text, grouped by '# speaker X') -> manifest.json for tts-tool.html. Checks every line against the deck's own spoken texts."""
import re, json, sys, pathlib
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / 'deck-library'))
from sxl.audio import norm
spk = None; assets = []
for ln in (HERE / 'pack.txt').read_text(encoding='utf-8').splitlines():
    ln = ln.strip()
    if not ln: continue
    m = re.match(r'# speaker (\w+)', ln)
    if m: spk = m.group(1); continue
    i, rest = [s.strip() for s in ln.split('|', 1)]
    t = re.match(r'\[([^\]]*)\]\s*(.*)', rest)
    tag, text = (t.group(1), t.group(2)) if t else ('', rest)
    assets.append(dict(id=i, text=text, tag=tag, speaker=spk, voice='teach', emotion='neutral', status='pending', file=''))
try:
    from lessons.lesson5_v2 import _texts
    deck = {norm(x) for x in _texts()}
    ours = {norm(a['text']) for a in assets}
    for a in assets:
        if norm(a['text']) not in deck: print('NOT A DECK TEXT:', a['id'], a['text'])
    for x in sorted(deck - ours): print('deck text with no clip:', x)
except Exception as e: print('deck check skipped:', e)
(HERE / 'manifest.json').write_text(json.dumps(dict(lesson='lesson5', assets=assets), indent=1, ensure_ascii=False), encoding='utf-8')
print(len(assets), 'assets ->', HERE / 'manifest.json')
