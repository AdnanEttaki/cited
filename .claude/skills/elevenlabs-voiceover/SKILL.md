---
name: elevenlabs-voiceover
description: Write and generate a cue-timed ElevenLabs voiceover (one request per line, with character timestamps) so narration lands on the exact on-screen moments. Use when a video needs an AI voice.
---
# ElevenLabs Voiceover

1. Script = hook (≤3 s) → "not me / it's AI" reveal → proof moments → CTA with comment keyword. Avoid guessing anyone's gender in the script; use "they".
2. Write `projects/<name>/vo_cues.json`: `[{"id","at","text"}]`, `at` = second the line should start on screen.
3. `python3 video-studio/vo.py projects/<name>/vo_cues.json <voice_id> video-studio/build/vo` → `<id>.mp3` + `<id>.json` alignment. Uses `previous_text/next_text` for consistent delivery. Model `eleven_multilingual_v2`, stability .45, style .35.
4. Check no overlaps: `at + duration < next at`.
Auth: the key is injected by the environment proxy for api.elevenlabs.io; send `xi-api-key: proxy-injected` with curl (Python urllib's default user agent gets 403).
Voices used: Sarah `EXAVITQu4vr4xnSDxMaL` (DM setter brand).
