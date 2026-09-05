# Next Session — Confidence Ladder v2 Build

## Start here

Read the full spec first:
`micro-lesson/MICRO-LESSON-SPEC.md`

PAT: rotate before use — see GitHub settings
Repo: redskin106/lesson-a
Target file: micro-lesson/confidence-ladder-v2.html

---

## Context

Students: A0-A2 refugees aged 16-18, Bangkok, mixed literacy
Teacher: Nick — CG background, methodology designer, not in the room during app use
Current player: micro-lesson/confidence-ladder-objects.html (v1 — working but needs full redesign)
Current builder: micro-lesson/micro-lesson-builder.html
Teaching moment prototype: micro-lesson/tm-adjective-order.html (reference for spring physics)
Full UX mockup: micro-lesson/confidence-ladder-mockup-v2.html (reference for visual design)

---

## Build priority order

### 1. Zone 0 — Mystery silhouette opening
- Object is HIDDEN on arrival — shown as dark silhouette only
- Word appears first (large, audio plays automatically)
- Student taps to reveal full image only after hearing the word
- Curiosity is the engine — mystery pulls the student forward
- No "Let's go" button until image has been revealed

### 2. Animated tile system
Every tile demonstrates what it means through its own appearance:

**Colour tiles** — background floods with the actual colour (grey → colour bleed like ink)
**Size tiles** — tile physically changes size (small tile for small, large for big)
**Texture tiles** — CSS surface treatment (grain for wooden, glossy for smooth, blur for soft)
**Shape tiles** — border-radius morphs (circle for round, sharp for square)

Reveal sequence (first encounter per tile type):
1. Icon only — no text
2. Animation triggers (colour/size/texture change)
3. Word fades in as animation settles
4. Optional multiple choice to confirm understanding
5. Snap sound — tile settles into learned form

### 3. Flying sentence assembly
Tiles fly in from scattered/off-screen positions and settle into correct order:
- Noun lands first (anchor)
- Each modifier flies in and finds its position
- Wrong order first: tiles arrive chaotically, wobble, then rearrange mid-air
- Spring physics: cubic-bezier(0.34, 1.56, 0.64, 1)
- Last tile snaps → full sentence glows → audio plays

### 4. Articles teaching moment (indigo world)
- Deep indigo background — completely different mode from lesson
- A closed box, question mark on lid
- Voice: "There's a bag in here"
- Box opens, same voice: "That's the bag"
- Zero English explanation — the experience IS the lesson
- Got it button → warm resolution sound

### 5. Because teaching moment (rose world)
- Deep rose background
- Two sentence halves floating separately, both faded
- "because" slides in as a bridge, both halves brighten
- Joined sentence plays as audio
- Gesture animation: two fists apart → interlaced together

### 6. Self-pacing
- No timer anywhere
- Next button pulses gently (warm gold, heartbeat rhythm)
- No urgency, no countdown, no pressure
- Lesson waits as long as student needs
- Every zone is a natural stopping point

### 7. Student tracking
Quiet JSON log per session:
- open timestamp
- zone depth reached
- dwell time per screen
- audio replay count
- record button attempts (not recordings)
- return visit flag

Teacher view: separate simple HTML reading the JSON

---

## Seven-step cycle (reference)

Every concept goes through:
```
Icon → Mime → Image → Audio → Word → Record & Compare → Sketch
```

The student experiences this as one smooth flow, not seven stages.
Steps are not all equal weight — icon/mime/image/audio take seconds,
record and sketch are longer and always optional.

---

## Key design principles (never violate)

1. No timer, no pressure, no Duolingo mechanics
2. Zero English required to understand teaching moments
3. Wrong version always before right version
4. One concept per teaching moment — never two
5. Tiles demonstrate their meaning through animation
6. Audio plays before text appears, always
7. Record and sketch are invitations, never demands
8. Natural stopping points at every zone boundary

---

## Audio files needed (source before wiring)

- `micro-lesson/audio/ui/teaching-moment-arrival.mp3`
- `micro-lesson/audio/ui/teaching-moment-snap.mp3`
- `micro-lesson/audio/ui/teaching-moment-celebrate.mp3`

Sources: Freesound.org (CC0), Mixkit.co, Pixabay/music
Search: "warm rise stinger", "snap resolved", "achievement warm melodic"
Avoid: anything that sounds like a phone notification or quiz app

---

## What NOT to rebuild

The builder (micro-lesson-builder.html) is fine — don't touch it.
The spec (MICRO-LESSON-SPEC.md) is the source of truth — check it for anything not covered here.
