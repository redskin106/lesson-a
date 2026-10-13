# Stage 4: split the finished motion primer into shared files + a tiny per-lesson shell.
#   primer-motion-v2.html -> shared/vp-motion.css, vp-motion.js, fonts/  and  shared/shell-example.html
# The page markup is injected by vp-motion.js, so a lesson's shell never has to be regenerated when the player improves.
import os,re,shutil
S=os.path.dirname(os.path.abspath(__file__))+'/'
OUT=S+'shared/'; shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT+'fonts')
h=open(S+'primer-motion-v2.html').read()
# fonts (self-hosted)
FS=S+'fnt/node_modules/@fontsource/'
css_f='/* self-hosted fonts (SIL Open Font License) */\n'
RNG={'latin':'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD','latin-ext':'U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1EFF,U+2020,U+20A0-20AB,U+20AD-20CF,U+2113,U+2C60-2C7F,U+A720-A7FF'}
for pkg,fam,ws in (('noto-sans','Noto Sans',(400,500,700)),('fraunces','Fraunces',(700,)),('caveat','Caveat',(700,))):
    for w in ws:
        for sub in ('latin','latin-ext'):
            fn=f'{pkg}-{sub}-{w}-normal.woff2'; src=FS+pkg+'/files/'+fn
            if os.path.exists(src):
                shutil.copy(src,OUT+'fonts/'+fn)
                css_f+=f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;src:url(fonts/{fn}) format('woff2');unicode-range:{RNG[sub]}}}\n"
styles=re.findall(r'<style>(.*?)</style>',h,re.S)
open(OUT+'vp-motion.css','w').write(css_f+'\n'.join(styles))
# markup = body up to the first script
b0=h.index('<body>')+6; b1=h.index('<script',b0)
markup=h[b0:b1].strip()
scripts=[m for m in re.finditer(r'<script(?P<a>[^>]*)>(?P<b>.*?)</script>',h[b1:],re.S)]
js=[]
js.append("(function(){var m="+__import__('json').dumps(markup)+";document.body.insertAdjacentHTML('afterbegin',m)})();")
for m in scripts:
    a,body=m.group('a'),m.group('b')
    if 'application/json' in a: continue            # the inline sample deck: lessons load their own deck
    js.append(body)
j='\n;\n'.join(js)
old="JSON.parse(document.getElementById('deck-data').textContent)"
assert j.count(old)==1
j=j.replace(old,"await (await fetch(window.DECK_URL, {cache:'no-cache'})).json()")
j=j.replace("setLoad(20, 'Fetching deck…');\n    setLoad(60, 'Parsing…');","setLoad(20, 'Fetching deck…');")
open(OUT+'vp-motion.js','w').write(j)
shell='''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>{{TITLE}}</title>
<link rel="stylesheet" href="motion/vp-motion.css?v={{V}}">
</head>
<body>
<script>window.DECK_URL = '{{DECK}}';</script>
<script src="motion/vp-motion.js?v={{V}}"></script>
</body>
</html>
'''
open(OUT+'shell-template.html','w').write(shell)
print('css',len(open(OUT+'vp-motion.css').read())//1024,'KB  js',len(j)//1024,'KB  markup',len(markup)//1024,'KB scripts',len(scripts))
