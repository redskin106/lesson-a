# Stage 3: make the self-hosted copy for the lesson-a repo (no third-party requests).
#   primer-motion-v2.html -> <repo>/vocab-primer-motion/index.html  (+ fonts/)
# Audio and phoneme sounds already live in the repo, so absolute GitHub URLs become relative paths.
import os,re,shutil,sys
S=os.path.dirname(os.path.abspath(__file__))+'/'
REPO=sys.argv[1] if len(sys.argv)>1 else os.path.abspath(S+'../..')
OUT=REPO+'/vocab-primer-motion/'
os.makedirs(OUT+'fonts',exist_ok=True)
html=open(S+'primer-motion-v2.html').read()
# fonts
FS=S+'node_modules/@fontsource/'
faces=[('noto-sans','Noto Sans',w,'normal') for w in (400,500,700)]+[('fraunces','Fraunces',700,'normal'),('caveat','Caveat',700,'normal')]
css='/* self-hosted fonts (SIL Open Font License) */\n'
for pkg,fam,w,st in faces:
    for sub,rng in (('latin','U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'),('latin-ext','U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1EFF,U+2020,U+20A0-20AB,U+20AD-20CF,U+2113,U+2C60-2C7F,U+A720-A7FF')):
        fn=f'{pkg}-{sub}-{w}-normal.woff2'; src=FS+pkg+'/files/'+fn
        if not os.path.exists(src): continue
        shutil.copy(src,OUT+'fonts/'+fn)
        css+=f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};font-display:swap;src:url({fn}) format('woff2');unicode-range:{rng}}}\n"
open(OUT+'fonts/fonts.css','w').write(css)
n0=len(re.findall(r'<link[^>]*fonts\.googleapis[^>]*>',html))
assert n0>=2,n0
html=re.sub(r'<link[^>]*fonts\.googleapis[^>]*>\s*','',html)
html=re.sub(r'<link[^>]*(preconnect|dns-prefetch)[^>]*fonts\.g[^>]*>\s*','',html)
html=html.replace('</head>','<link rel="stylesheet" href="fonts/fonts.css">\n</head>',1)
# audio and sounds: same origin
RAW='https://raw.githubusercontent.com/redskin106/lesson-a/main/'
PG='https://redskin106.github.io/lesson-a/'
html=html.replace(RAW,'../').replace(PG,'../')
# every local file the page names must exist
missing=[u for u in set(re.findall(r'\.\./[A-Za-z0-9_./-]+\.(?:mp3|png|jpg|webp|svg)',html)) if not os.path.exists(os.path.normpath(OUT+u))]
print('relative files referenced:',len(set(re.findall(r'\.\./[A-Za-z0-9_./-]+\.(?:mp3|png|jpg|webp|svg)',html))),'missing:',missing[:5],len(missing))
# fallback: phoneme file names are built in code, so also report the pattern
# Content-Security-Policy: nothing may load from or send to another site
csp="default-src 'none'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data: blob:; media-src 'self' data: blob:; connect-src 'self' data: blob:; object-src 'none'; base-uri 'none'; form-action 'none'"
html=html.replace('<head>','<head>\n<meta http-equiv="Content-Security-Policy" content="'+csp+'">\n<meta name="referrer" content="no-referrer">',1)
assert 'googleapis' not in html.replace('www.w3.org','') or print('googleapis still present')
left=sorted(set(re.findall(r'https?://[a-zA-Z0-9.-]+',html))-{'http://www.w3.org'})
print('remaining external hosts:',left)
open(OUT+'index.html','w').write(html); print(len(html)//1024,'KB ->',OUT)
