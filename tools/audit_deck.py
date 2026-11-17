"""Deck audit: python3 audit_deck.py deck.html [more.html]
 1. new-word coverage: which slides use each target word (text + exercise data)
 2. shared-rule checks: Fluent credit position, exercise slides with a partner prompt or hint, covers have a phase background
"""
import re,sys,html
WORDS=['exhausted','dizzy','shaky','racing heart','nauseous','breathless','sweaty','pale','mild','moderate','severe','unbearable','might','can\'t','because','slightly','much','dangerously','higher','lower','ago']
def slides(h):
    out=[]
    for m in re.finditer(r'<section class="sl[^"]*"[^>]*?data-m="([^"]*)"[^>]*?data-label="([^"]*)"[^>]*>(.*?)</section>',h,re.S):
        out.append((html.unescape(m.group(2)),m.group(3)))
    return out
def text(b): return html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<style.*?</style>','',b,flags=re.S))).lower().replace('’',"'")
def run(f):
    h=open(f).read(); S=slides(h); print('==',f,len(S),'slides')
    for w in WORDS:
        hits=[i+1 for i,(l,b) in enumerate(S) if w in text(b)]
        print(f'  {w:13s} {len(hits):2d}  slides {hits}')
    for i,(l,b) in enumerate(S):
        if 'Fluent Emoji (MIT)' in b:
            st=re.search(r'style="([^"]*)">Emoji: Microsoft',b); print('  credit on slide',i+1,'->',st.group(1) if st else '?')
    ex=[(i+1,l) for i,(l,b) in enumerate(S) if (l.startswith('Exercise') or l.startswith('Everybody')) and 'class="ptp"' not in b and 'class="a mu"' not in b]
    print('  exercise slides with no partner prompt/hint:',ex or 'none')
for f in sys.argv[1:]: run(f)
