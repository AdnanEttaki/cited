---
name: kinetic-captions
description: Word-by-word captions generated from ElevenLabs character timestamps, with the active word highlighted in electric blue. Use for any voiced short-form video (most viewers watch muted).
---
# Kinetic Captions

Automatic: `render.mjs` reads `build/vo/<cue>.json` alignments + `vo_cues.json` offsets, groups words into chunks of ≤3 (break on punctuation), and the composition highlights the active word (#3D8BFF + glow), spoken words white, upcoming words 38% white.
- 9:16: glass pill (blurred navy, platinum hairline) centred under the phone, above the Reels UI safe zone.
- 1:1: left-aligned under the headline stack.
Edit layout in `LAYOUTS[fmt].cap` in `render.mjs`. Captions hide automatically on the end card.
