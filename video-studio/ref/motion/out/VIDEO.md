---
videomd: 1
name: ref
description: 'Made with (inferred): code / template render 91%, 3D render 9%'
source:
  file: ref.mp4
  sha256: 3e99ee7882930d5dc2d46e8f563f91f91aaf047129a3def03e61f3411d1efefb
  duration: 20.933
  size: 720x1280
  fps: 30.0
  aspect: '9:16'
shots: 8
lang: en
made_mix:
  code_render: 0.914
  cg_3d: 0.086
confidence: 0.646
readers:
- tools
open_questions: 9
generator:
  name: rea-video
  version: 0.1.0
---

# ref.mp4

**Verdict** (inferred): Mixed production: code / template render 91% + 3D render 9%; overlays: text labels, title (composited in code / an editor); audio: music 178.2BPM (to confirm, leaning stock library music) + 13 sound effects; packaging: 2 subtitle lines, styled text ×1, text labels ×3, 1 sound effects land on text / sticker pops
**Made with** (inferred, by duration): code / template render 91%, 3D render 9%
**Remake**: 4 3D render shots → 3 generation units, 3 Seedance 2.0 calls; code render / screen capture 4 shots → 1 code project (2 parts)

## Next steps

- No VLM ran: if you can see images, review first: `rea-video review <this dir>` → fill `review_answers.json` → `rea-video apply-review <this dir>`
- Remake: `rea-video remake <this dir>` does what can be done automatically and keeps the original elsewhere; `remake/status.md` says per shot what is left. Add incoming clips to `remake/mine.json` and run it again
- Code-rendered shots are redrawn by `rea-video code-remake <this dir>` (the step above runs it): edit `code/spec.json` and rerun, do not write one from scratch
- AI shots: prompts are in the generation units of `video/remake.md`; for automatic generation run `rea-video remake-plan` + `remake-run --dry-run` (paid: ask the user first)

## Open questions

- The VLM did not run (No VLM; live action / AI / 3D are told apart from pixel statistics only, so confidence is limited. An agent that can see images: run rea-vi…
- Shot #1 (0.0–5.5s): code / template render at only 51% confidence, runner-up cg_3d
- Shot #2 (5.5–7.5s): code / template render at only 59% confidence, runner-up cg_3d
- Shot #3 (7.5–8.1s): 3D render at only 50% confidence, runner-up code_render
- Shot #4 (8.1–8.5s): 3D render at only 52% confidence, runner-up code_render
- Shot #5 (8.5–8.8s): 3D render at only 53% confidence, runner-up code_render
- Shot #6 (8.8–9.3s): 3D render at only 54% confidence, runner-up code_render
- No AI listened to the soundtrack: real voice versus TTS is inferred from the waveform; the effects were found on the separated effects track and their types are…
- 1 more, see the `flag` lines in `video/timeline.md`

## Map

Read this page first; for detail, open only the file you need. Each line is `path | ~tokens | what is in it · when to read it`; paths are relative to this directory.

```videomd-map
video/timeline.md | 594 | Timeline: one line per shot · what a stretch says, which shots need review, how a shot was made
video/content.md | 87 | Content and structure · what it says, the narrative line, structure, the script
video/cast.md | 32 | Cast, scenes and props · reference images for characters, first-frame prompts
video/sound.md | 616 | Sound · voice, music, sound effects, beats and sources
video/look.md | 482 | Camera, lighting and editing · for filmed shots: framing, camera, lighting, kit
video/packaging.md | 479 | Packaging · subtitles, styled text, stickers, picture-in-picture: timing and style
video/remake.md | 4964 | Remake plan · generation units, shoots, code builds, real material to collect, acting and emotion
video/shots/*.md | 371 | Per-shot detail, tokens per file on average · checking one shot: what is seen, the inference and its basis, prompts, frames
breakdown.json | 48742 | Full raw data · for programs; a model rarely needs it
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
