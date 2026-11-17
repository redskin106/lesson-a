#!/usr/bin/env bash
# Recreates the /home/claude/work/... folders the deck library reads (paths are hard-coded at the top of
# deck-library/sxl/core.py), so a fresh session can build L1-L4 in one step.
#   bash tools/setup_env.sh          (from the repo root; safe to re-run)
# Then:  cd deck-library && python3 lessons/lessons34.py
# Needs network access to the npm registry and raw.githubusercontent.com.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
W=/home/claude/work

mkdir -p "$W/lesson/art" "$W/lesson/audio" "$W/lesson/media" "$W/audio" "$W/emoji/e3d" "$W/dir"

# art, audio and media that ARE in the repo (never overwrite files already in work/)
cp --update=none "$REPO"/deck-library/art/*          "$W/lesson/art/"   2>/dev/null || true
cp --update=none "$REPO"/lessons-3-4/source-art/*.jpg "$W/lesson/art/"   2>/dev/null || true
cp --update=none "$REPO"/lessons-3-4/source-audio/*.mp3 "$W/lesson/audio/" 2>/dev/null || true
cp --update=none "$REPO"/deck-library/media/*       "$W/lesson/media/" 2>/dev/null || true

# fonts (@fontsource Outfit + Poppins)
if [ ! -f "$W/dir/node_modules/@fontsource/outfit/files/outfit-latin-700-normal.woff2" ]; then
  (cd "$W/dir" && { [ -f package.json ] || npm init -y >/dev/null; } && npm i @fontsource/outfit @fontsource/poppins >/dev/null 2>&1)
fi

# Fluent Emoji 3D PNGs: build L3/L4, fetch whichever emoji is reported missing, repeat until the build passes
python3 -I - "$REPO" <<'PY'
import re, subprocess, sys, urllib.parse, urllib.request
repo = sys.argv[1]
D = '/home/claude/work/emoji/e3d/'
BASE = 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/'
for _ in range(150):
    r = subprocess.run(['python3', 'lessons/lessons34.py'], cwd=repo + '/deck-library', capture_output=True, text=True)
    m = re.search(r"No such file or directory: '" + re.escape(D) + r"([^']+)\.png'", r.stderr)
    if not m:
        if r.returncode:
            print(r.stderr[-1500:]); sys.exit('build failed for a reason other than a missing emoji')
        print('environment OK: build passes'); break
    n = m.group(1)
    q = urllib.parse.quote(n.replace('_', ' ').capitalize())
    for u in (f'{BASE}{q}/3D/{n}_3d.png', f'{BASE}{q}/Default/3D/{n}_3d_default.png'):
        try:
            open(D + n + '.png', 'wb').write(urllib.request.urlopen(u, timeout=30).read()); print('emoji', n); break
        except Exception:
            pass
    else:
        sys.exit(f'could not fetch emoji {n}')
else:
    sys.exit('too many missing emoji')
PY
