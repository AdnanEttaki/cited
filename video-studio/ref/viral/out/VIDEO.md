---
videomd: 1
name: ref
description: 'Made with (inferred): code / template render 94%, 3D render 6%'
source:
  file: ref.mp4
  sha256: 02418aef126b262806a176a75cf87dc99cb8c4a7b2f21f79a6d7a22b6fcf417a
  duration: 71.633
  size: 716x1274
  fps: 30.0
  aspect: '9:16'
shots: 21
lang: en
made_mix:
  code_render: 0.9372
  cg_3d: 0.0628
confidence: 0.779
readers:
- tools
open_questions: 3
generator:
  name: rea-video
  version: 0.1.0
---

# ref.mp4

**Verdict** (inferred): Mixed production: code / template render 94% + 3D render 6%; overlays: styled text, text labels, layout template, subtitles, title (composited in code / an editor); real material used: screen recording (17.6s), UI screenshot (8.1s); audio: voice + 15 sound effects; packaging: 123 subtitle lines, styled text ×1, text labels ×3, 7 sound effects land on text / sticker pops
**Made with** (inferred, by duration): code / template render 94%, 3D render 6%
**Remake**: 1 3D render shot → 1 generation unit, 1 Seedance 2.0 call; code render / screen capture 20 shots → 1 code project
**Real material to collect**: 8 shots (36% of the duration), list in `video/remake.md`

## Next steps

- No VLM ran: if you can see images, review first: `rea-video review <this dir>` → fill `review_answers.json` → `rea-video apply-review <this dir>`
- Remake: `rea-video remake <this dir>` does what can be done automatically and keeps the original elsewhere; `remake/status.md` says per shot what is left. Add incoming clips to `remake/mine.json` and run it again
- Code-rendered shots are redrawn by `rea-video code-remake <this dir>` (the step above runs it): edit `code/spec.json` and rerun, do not write one from scratch
- AI shots: prompts are in the generation units of `video/remake.md`; for automatic generation run `rea-video remake-plan` + `remake-run --dry-run` (paid: ask the user first)

## Open questions

- The VLM did not run (No VLM; live action / AI / 3D are told apart from pixel statistics only, so confidence is limited. An agent that can see images: run rea-vi…
- No AI listened to the soundtrack: real voice versus TTS is inferred from the waveform; the effects were found on the separated effects track and their types are…
- voice source to confirm: most likely TTS voice-over (43%); how to check is under “Sound”

## Map

Read this page first; for detail, open only the file you need. Each line is `path | ~tokens | what is in it · when to read it`; paths are relative to this directory.

```videomd-map
video/timeline.md | 1314 | Timeline: one line per shot · what a stretch says, which shots need review, how a shot was made
video/content.md | 87 | Content and structure · what it says, the narrative line, structure, the script
video/cast.md | 32 | Cast, scenes and props · reference images for characters, first-frame prompts
video/sound.md | 525 | Sound · voice, music, sound effects, beats and sources
video/look.md | 464 | Camera, lighting and editing · for filmed shots: framing, camera, lighting, kit
video/packaging.md | 4327 | Packaging · subtitles, styled text, stickers, picture-in-picture: timing and style
video/remake.md | 12498 | Remake plan · generation units, shoots, code builds, real material to collect, acting and emotion
video/shots/*.md | 434 | Per-shot detail, tokens per file on average · checking one shot: what is seen, the inference and its basis, prompts, frames
breakdown.json | 240776 | Full raw data · for programs; a model rarely needs it
shots/ | - | contact sheet, first and last frame of each shot · checking by eye
storyboard.jpg | - | storyboard of the whole video · the whole video at a glance
stems/ | - | voice, music and effects stems · listening, remaking the sound
sfx/ | - | a clip of each sound effect · finding matching effects
packaging/ | - | subtitle files, packaging timeline, sticker frames · remaking subtitles and packaging
frames/ | - | picture scenes: full-size frames, the drawn layer cut out and sampled, measurements · remaking rendered pictures
audio.png | - | waveform and beat chart · seeing the rhythm
```

## How to read

- One shot per line: `#<n> start-end (s) | key value | …`. A key ending in `~` is the tools' inference; keys without it are visible on screen or measured directly.
- `story` job in the story and the point · `seen` what is on screen · `act` acting (emotion, strength, face) · `camera` camera move · `overlay` overlays · `made~` how it was made (inferred) · `material~` where the material came from (inferred) · `remake` remake route · `flag` needs a second look
- Full detail for a shot is in `video/shots/<n>.md` (e.g. `video/shots/07.md`).
- What is “seen” can be checked against the frames; what is “inferred” is the tools' and image readers' judgement, with the basis in each shot file. When they disagree, trust the frames.
