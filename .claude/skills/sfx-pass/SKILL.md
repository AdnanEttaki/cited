---
name: sfx-pass
description: Generate and place sound design (whoosh, message pop, sub boom, riser, chime) with ElevenLabs sound effects and mix it with VO + ducked music to -14 LUFS. Use whenever a video needs audio polish.
---
# SFX Pass

1. Generate library: `python3 video-studio/sfx.py video-studio/build/sfx` (needs ElevenLabs key on api.elevenlabs.io).
2. Music: the ElevenLabs Music API is paid-only; on free plans generate a loopable bed via sound-generation with `"loop": true, "duration_seconds": 22` (saved as `build/bed.mp3`).
3. Place hits in `timeline.json` → `sfx` (`at` can be a list). Rules: boom on the hook and the payoff, whoosh 0.3 s before each type transition/flash, pop on every message arrival (scene-change times), chime on proof moments, riser into the CTA.
4. `python3 video-studio/mix.py projects/<name>`: VO compressed + EQ, music side-chain ducked under VO, loudnorm -14 LUFS / -1 dBTP, muxed into the final MP4s.
