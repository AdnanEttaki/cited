---
name: paper-motion-video
description: Full production system for animated "Paper Data" short-form videos (Reels/TikTok 9:16) - cream paper style, tactile 3D bars/cards/stickers, Instagram-style DM phone screens, word-synced kinetic captions, scene push/zoom transitions, idle motion, confetti, count-ups, ElevenLabs voiceover, SFX and -14 LUFS mix, frame-accurate Chromium rendering, multi-hook A/B variants. Use when the user wants a video "same style / same animation / same quality" as the DM-setter paper videos, a new hook variant, or a new story in this style.
---
# Paper Motion Video — the complete system

Proven output: `video-studio/storyboards/paper-data/out/paper_hook{A,B,C}_9x16.mp4` (same body, 3 hooks).
Engine (all in `video-studio/storyboards/paper-data/`):
| File | Role |
|---|---|
| `build.py` | Design system: tokens, CSS, components (`bar`, `card`, `tag`, `phone`…), the 12 storyboard frames, storyboard grid |
| `shoot.mjs` | Renders `storyboard.html` -> `storyboard.jpg` + `frames/frame_XX.png` (static review board) |
| `video.py` | Animation layer: hooks, VO per scene, word-synced captions, keyframes, transitions JS, SFX plan, audio mix |
| `render_video.mjs` | Frame-accurate renderer (Playwright Chromium -> JPEG pipe -> ffmpeg x264), 4 parallel workers |
| `../../build/sfx/*.mp3`, `../../build/bed.mp3` | ElevenLabs SFX library + loopable music bed |

Portable copy of everything (spec + full source) for other AIs: `PLAYBOOK.md` in this folder.

## Workflow (always in this order)
1. **Talk first.** Confirm: story beats, hook(s), voice, CTA keyword, format. Never render before the hook is decided.
2. **Storyboard.** Edit `frames` in `build.py` -> `python3 build.py && node shoot.mjs` -> review `storyboard.jpg` (one grid image, 540x960 per frame). Fix layout here, it is 100x cheaper than fixing video.
3. **Hooks.** Add/modify entries in `HOOKS` in `video.py` (label, right, num, vis, cap, vo). Body = frames[1:].
4. **Voice.** `python3 video.py vo` (ElevenLabs, one request per scene, cached by id; delete `build/vo/<id>.json` to regenerate).
5. **Compose.** `python3 video.py html` -> `video_<hook>.html` + `timeline_<hook>.json`.
6. **Preview stills at key times** (scene start + 0.15 for transitions, + 1.0 for settled): `node render_video.mjs A --preview 0,3.6,8.5` -> `out/pv_A_*.jpg`. Look at them. Always check frame 0 (= thumbnail).
7. **Render + mix:** `node render_video.mjs A && python3 video.py mix A` -> `out/paper_hookA_9x16.mp4`.
8. **QA** (checklist below), then deliver.

## Design tokens
- Paper bg: `radial-gradient(120% 90% at 50% 40%, #F4F0E8 0%, #ECE6DA 70%, #E2DBCD 100%)` + 36px grid lines `rgba(0,0,0,.035)`.
- Ink `#1B1B1B` · Orange `#D8541E` (primary accent) · Teal `#1E9E95` · Magenta `#D9257E` · Amber `#F2A33A` · grey text `#9A9286`.
- Type: Inter 800, letter-spacing -.035em. Captions 44px on a 540px frame (render at zoom 2 -> 1080x1920).
- Giant faded numeral bottom-left: 430px, `rgba(60,45,25,.06)`.

## Frame anatomy (540x960 design units, rendered at zoom:2)
| Zone | y | Content |
|---|---|---|
| Header | 78 | 1px ink rule + 46x5 ink tab, UPPERCASE label left, time/step right (13px 800, .08em) |
| Visual | 125-595 | ONE tactile idea |
| Caption | 620 | max ~8 words, 1-2 boxed words (`.hl` ink / `.hlo` orange), de-emphasis `.g` grey |
| Scrubber | 820 | progress line, knob = scene index, orange flag at payoff scene (F7), "Values illustrative", "Frame n of N" |

## Components
- `bar(w, color, h, inner)` extruded 3D bar: gradient (color+22% white -> color -> color+18% black) + `0 8px 0` darker bottom edge + soft drop shadow + inset highlight.
- `card()` paper card, `tag()` sticker (dot + white bold text, rotated), `badge` red/orange count bubble with white ring.
- `phone(msgs, hl=index, name=..., typing=...)` Instagram-style dark DM screen: status bar + island, header (back, avatar, name, "Active now", call/video icons), incoming `#262626`, outgoing gradient `135deg #3797F0 -> #5B51F0 -> #A033FF`, "Seen", typing dots, message bar (blue camera circle, Message..., mic/image/heart). Key message gets class `hlb` (amber outline + glow). Never draw the Instagram logo.
- `slot` time tiles (`.up` = picked, orange, lifted, flag), `cal` + `stamp` (BOOKED), `chart`/`col` 3D columns + dashed "on" marker, `key` 3D key-cap CTA + `cbox` comment field.

## Animation spec (CSS keyframes, all driven by time — never by wall clock)
Every scene is a `<section class="fr">`; all its CSS animations are paused and set via `anim.currentTime = (t - sceneStart)*1000` each frame. `--pre` (ms) pre-rolls a scene (hook uses 450ms so frame 0 is already alive).

| Element | Entrance | Then (idle, infinite) |
|---|---|---|
| Scene `.fr` | — | camera push `scale 1 -> 1.06` over scene duration |
| Giant numeral `.num` | `translate 0 80px -> 0`, .9s `cubic-bezier(.2,.8,.2,1)` | drift `translate -26px`, 4s alternate |
| Header | fade + 8px drop, .5s | — |
| Bar rows `.row` | `translate -115% -> 0`, .7s `cubic-bezier(.2,.9,.3,1.12)` (overshoot), stagger 70ms, +80ms | sway `translate 10px`, 2.4s alternate, staggered |
| Labels `.lbl` | fade, stagger 150ms | — |
| Phone `.ph` / cards | `translate 0 140px, scale .9, opacity 0 -> rest`, .75s overshoot | bob `rotate -0.9deg <-> 0.9deg`, 2.2-2.6s |
| Chat messages `.m` | `opacity 0, translate 0 14px, scale .85`, .32s `cubic-bezier(.2,.9,.3,1.3)`, delay 350ms + i*380ms | highlighted bubble `.b.hlb`: amber glow pulse 1s alternate |
| Badge | pop `scale 0 -> 1`, .45s `cubic-bezier(.2,.9,.3,1.6)`, +320ms | heartbeat `scale 1.14` every .9s |
| Stickers `.tag` | pop, +650ms + i*160ms | wiggle `rotate ±3deg`, 1.4s |
| Hook sticker `.tag.xl` | pop at +150ms | wiggle 1.2s |
| Slots | drop-in stagger 120ms; flag pops at 1.95s (when "3:00 PM works for me" lands) | — |
| Stamp | `scale 2.8 -> 1, opacity 0 -> 1`, .32s ease-in at +520ms | `.vis.shake` screen shake .45s at +840ms + 34 confetti pieces |
| Chart `.col` | `scale 1 0 -> 1` from bottom, stagger 90ms; numbers count up (ease-out cubic, 800ms) via `data-count` | — |
| Key-cap CTA | drop from -60px, then press `scale .94 .9` at +1050ms + white ripple ring + 22 confetti | — |
| Comment box | fade up 20px at +450ms | — |
| Hook B bars `.bar.fall` | fall `translate 60px 900px, rotate 24deg, opacity 0`, ease-in, from 1.3s, bottom first, 110ms stagger | — |
| Caption words `.w` | `opacity 0, translate 0 18px, scale .6 -> rest`, .26s overshoot, delay = that word's ElevenLabs start time | — |
| Caption boxes `.cap .hl/.hlo` | background wipe `0% -> 100%` + text ink -> white, .3s at first word's time | — |
| Scrubber knob/progress | slide from previous scene position, .5s | — |
| Confetti `.cf` | 5 brand colors, 9x14px, random end `x ±260, y -330..120, rotate ±540deg`, 1.3s `cubic-bezier(.15,.7,.4,1)` | — |

Rules that make it feel premium: overshoot on entrances, nothing linear except camera push, every scene has at least one idle loop, one hero moment per scene (stamp, press, count, fall), stagger everything (never all at once).

## Scene transitions (JS, 0.34s, expo-out, cycle left / up / zoom)
- left: new `translateX(100% -> 0) rotate(4deg -> 0)`; old `translateX(0 -> -60%) rotate(-3deg)`, blur 0 -> 6px.
- up: new `translateY(100% -> 0)`; old `translateY(-40%) scale(.9)`, blur 6px.
- zoom: new `scale(.7 -> 1)` + opacity; old `scale(1 -> 1.6)`, blur 10px.
Both scenes visible only during the 0.34s window; whoosh SFX at every cut (-15 dB, 0.12s before).

## Timing
- Scene duration = `max(1.9s, voStart + voDuration + 0.5s)`; last scene +1.4s hold. Total ~30s for 12 scenes.
- VO starts 0.12s into each scene (0.05s for the hook).
- Hook: visuals pre-rolled 450ms, caption shifted 0.6s earlier -> frame 0 already shows bars + first boxed words (thumbnail).
- Caption word k of N maps to VO word `round(k*nVO/N)` (handles "2 AM" vs "2&nbsp;AM", "7x" vs "Seven-times").

## Voice (ElevenLabs)
- Endpoint `POST /v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128`, model `eleven_multilingual_v2`, settings `stability .45, similarity_boost .8, style .35, use_speaker_boost true`.
- Voice used: Sarah `EXAVITQu4vr4xnSDxMaL`. One request per scene; VO text = caption text (spell numbers so they read naturally: "Seven-times").
- Auth: key injected by proxy for `api.elevenlabs.io`; call with curl and header `xi-api-key: proxy-injected` (Python urllib's user agent gets 403).
- Music API is paid-only; the bed is a 22s `sound-generation` loop with `"loop": true`.

## Sound design + mix
- Per scene SFX list `(offset, file, gain)`: pop for each chat message/sticker (-12/-13 dB, on the message delays .35 + i*.38), ding per checklist bar, boom on stamp/hook/end (-7..-9), click on key press (-6), riser under data hook (-16), whoosh every cut (-15).
- Mix chain (ffmpeg): VO -> highpass 80 Hz -> compressor (thr -20 dB, 3:1, 5/80 ms) -> EQ +2 dB @3.5 kHz; music bed -20 dB, sidechain-ducked by VO (thr .02, 12:1, 20/350 ms), fade in .4s / out 2s; amix VO+music+SFX -> `loudnorm I=-14:TP=-1:LRA=9`; AAC 256k; mux with `-shortest -movflags +faststart`.

## Render pipeline
- Page 1080x1920, `#stage{width:540px;height:960px;zoom:2}` (zoom keeps text vector-sharp).
- Scenes toggled with opacity, NEVER `display:none` (hidden elements lose their CSS animations).
- `window.ready` awaits fonts, collects `el.getAnimations({subtree:true})` per scene and pauses them.
- 4 Playwright pages render frame ranges in parallel -> JPEG q95 -> `ffmpeg image2pipe mjpeg -> libx264 crf 18 yuv420p` -> concat.

## Pitfalls already hit (do not repeat)
1. **Class collision**: caption highlight `.hl` also matched the chat bubble -> dark text on dark bubble. Scope caption styles as `.cap .hl`, use `hlb` for bubbles.
2. Two animations on one element fighting over `transform`: use the individual properties (`translate`, `scale`, `rotate`) and give each animation a different one; idle loops use fill-mode `none`.
3. `display:none` kills CSS animations -> use opacity.
4. Inline `transform: rotate()` on stickers/phones stays; animate `rotate`/`scale` properties on top.
5. Stickers must never cover message text; check every chat frame still.
6. Bars bleeding off the left edge need inner padding (`.pl`) or the label gets cut.
7. Frame 0 is the thumbnail: pre-roll the hook so it is never empty.
8. Audio is ~0.35s shorter than video after loudnorm; `-shortest` trims the end-card hold (fine), never the VO.

## Content rules for this brand
- No prices, no AI mentions; chats always on the Instagram-style phone; real conversations only (with permission).
- Any number that is not the user's real data stays labelled "Values illustrative" or gets replaced before ads.
- Statistics in hooks must be sourced (HBR 2011 "The Short Life of Online Sales Leads": within 1 hour ~7x more likely to have a meaningful conversation — verify against the original before ads).
- Original content only: copy the style language, never another creator's logos, names or layouts.

## QA checklist before delivering
- [ ] Frame 0 of each hook readable as a thumbnail
- [ ] Every chat frame: all message text readable, no sticker overlap, highlighted message glows
- [ ] Mid-transition stills look intentional (no blank frames)
- [ ] Captions sync to voice; boxes wipe on the right word
- [ ] Loudness -14 LUFS ±1, true peak <= -1 dB (`ffmpeg -af ebur128=peak=true`)
- [ ] Duration ~30s, 1080x1920, H.264 + AAC, faststart
- [ ] Contact sheet `fps=1/2,tile=8x2` reviewed end to end
