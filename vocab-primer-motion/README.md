# Vocab primer (motion version)

`index.html` is the finished page. Open it from GitHub Pages at `/vocab-primer-motion/`.

- **Self-hosted.** Fonts are in `fonts/`; audio and phoneme sounds are read from the folders already in this repo (`../vocab-describe-objects/`, `../shell-v2/assets/phonemes/`). Nothing is requested from another site, and a Content-Security-Policy in the page blocks it if something tries.
- **Deck text is cleaned on load** (`sanitizeDeck`): no tags, backslashes or odd quotes, and file fields can't use `javascript:` or other schemes.
- **Stays on the device:** progress, Known/Learning words, sound on/off and recordings live in the browser's own storage. Nothing is sent anywhere.

## Rebuilding

```
cd src
npm install
npm run build     # primer-motion-real.html -> notebook -> motion -> ../index.html and ../fonts/
npm test          # behaviour checks, a hostile-deck check and a deck-cleaning check
```

`src/primer-motion-real.html` is the editable source. Edit it (or `build_v2.py` for the motion layer), rebuild, test.
