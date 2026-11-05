---
name: lux-edit
description: End-to-end luxury short-form edit of a raw screen recording or talking clip: voiceover, big type, chat zooms, captions, SFX, 9:16 + 1:1 export. Use when the user drops a raw video and wants a premium/viral edit.
---
# Lux Edit (pipeline)

Talk first: confirm palette, type style, voice, script, CTA keyword and formats with the user before rendering.

```bash
cd video-studio
# 1. frames of the source area
ffmpeg -i RAW -vf "crop=W:H:X:Y,scale=1.5x:flags=lanczos,unsharp=5:5:0.6" -q:v 2 build/frames/f%04d.jpg
# 2. voice + sfx            (skills: elevenlabs-voiceover, sfx-pass)
python3 vo.py projects/P/vo_cues.json VOICE build/vo && python3 sfx.py build/sfx
# 3. timeline               (skills: big-type-stack, chat-zoom)  -> projects/P/timeline.json
# 4. previews then render   (skills: vertical-reframe, kinetic-captions, lux-palette)
node render.mjs projects/P both --preview 0.6,16.8,44.8
node render.mjs projects/P both
# 5. mix + mux
python3 mix.py projects/P   # -> projects/P/out/final_9x16_reels.mp4, final_1x1_feed.mp4
```
Retention structure: hook in the first 1 s (boom + big type), a new visual change every 2–3 s, zoom on every proof moment, a checklist build for the close, and an end card with one button-style CTA.
