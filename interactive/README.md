# Interactive deck slice (offline, single file)
`lesson2.html` and `lesson1.html` — open in any browser, no network. Three library modules driven by the same data dicts as the PDF deck:
- timeline: tap the picture that happened next (wrong = boop, no penalty)
- sort: tap a word, tap its picture row
- chat: tap-to-fill gaps, thread auto-scrolls, scroll back freely
General layer: primer SXLSound engine (copied, not modified), Sound on/off, Motion On/Calm/Off (Calm mutes sound). No scores, no spoken audio.
`src/` holds the generator (`interactive.py`) and the spec picker; it depends on the SkillsXLab `sxl` library kept with the lesson decks.
