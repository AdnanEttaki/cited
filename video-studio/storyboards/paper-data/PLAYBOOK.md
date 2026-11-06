# PAPER MOTION VIDEO — Complete Playbook (portable)
Give this whole file to any AI or developer. It contains the full style system, every animation with exact timings, the voice/SFX/mix chain, the render pipeline, the QA checklist and the complete source code.
## Run it anywhere (outside the original environment)
Requirements: Python 3.10+, Node 20+, `npm i playwright` (+ `npx playwright install chromium`), ffmpeg, the Inter font installed (weights 500-900), an ElevenLabs API key.
Folder layout expected by the code:
```
video-studio/
  sfx.py                      # ElevenLabs sound effects -> build/sfx/*.mp3
  build/sfx/  build/vo/  build/bed.mp3
  storyboards/paper-data/     # build.py, video.py, render_video.mjs, shoot.mjs
```
1. The code sends `xi-api-key: proxy-injected` because the original environment injected the real key. Outside it, replace that string with your key (or read it from an env var, e.g. `os.environ["ELEVENLABS_API_KEY"]`) in `video.py` and `sfx.py`.
2. `python3 sfx.py build/sfx` then create the music bed:
   `curl -X POST https://api.elevenlabs.io/v1/sound-generation -H "xi-api-key: $KEY" -H "Content-Type: application/json" -d '{"text":"luxury minimal deep house instrumental loop, warm sub bass, soft piano chords, crisp hi-hats, elegant confident, 100 bpm, no vocals","duration_seconds":22,"prompt_influence":0.5,"loop":true}' -o build/bed.mp3`
3. `cd storyboards/paper-data && python3 build.py && node shoot.mjs` (storyboard), then `python3 video.py vo && python3 video.py html && node render_video.mjs A && python3 video.py mix A`.
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

---
## Source: `storyboards/paper-data/build.py`
```python
"""Paper-data style storyboard for the DM setter video (12 frames, 9:16). Chats shown on an Instagram-style DM screen.
Style: cream paper + grid, editorial header, tactile 3D bars/cards/stickers, big black captions, 24h scrubber.
Usage: python3 build.py  -> storyboard.html (render with shoot.mjs)"""
import os

here = os.path.dirname(os.path.abspath(__file__))
O, T, M, A, K = "#D8541E", "#1E9E95", "#D9257E", "#F2A33A", "#1B1B1B"  # orange teal magenta amber ink


def bar(w, color, h=46, label="", inner="", z=""):
    return (f'<div class="bar" style="width:{w}px;height:{h}px;--c:{color};{z}">'
            f'{f"<b>{label}</b>" if label else ""}{inner}</div>')


def card(html, x, y, w, rot=0, extra=""):
    return f'<div class="card" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);{extra}">{html}</div>'


def tag(txt, color, x, y, rot=0):
    return f'<div class="tag" style="left:{x}px;top:{y}px;background:{color};transform:rotate({rot}deg)">{txt}</div>'


def bubble(who, txt, lead=True):
    av = "L" if lead else "S"
    return (f'<div class="bub"><div class="who"><i class="{"" if lead else "ai"}">{av}</i>{who}<span>now</span></div>'
            f'<div class="txt">{txt}</div></div>')


ICON = {
 "back": '<svg viewBox="0 0 24 24"><path d="M15 4l-8 8 8 8" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "phone": '<svg viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2" fill="none" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"/></svg>',
 "video": '<svg viewBox="0 0 24 24"><rect x="2.5" y="6" width="13" height="12" rx="3" fill="none" stroke="#fff" stroke-width="1.8"/><path d="M15.5 10.5l6-3.5v10l-6-3.5" fill="none" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"/></svg>',
 "mic": '<svg viewBox="0 0 24 24"><rect x="9" y="3" width="6" height="11" rx="3" fill="none" stroke="#fff" stroke-width="1.8"/><path d="M5.5 11a6.5 6.5 0 0013 0M12 17.5V21" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/></svg>',
 "img": '<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="4" fill="none" stroke="#fff" stroke-width="1.8"/><circle cx="9" cy="9" r="1.8" fill="#fff"/><path d="M4 18l5-5 4 4 3-3 4 4" fill="none" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"/></svg>',
 "heart": '<svg viewBox="0 0 24 24"><path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0112 7.4 4.3 4.3 0 0119.5 10c0 5.4-7.5 10-7.5 10z" fill="none" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"/></svg>',
 "cam": '<svg viewBox="0 0 24 24"><path d="M4 8h3l2-2.5h6L17 8h3v11H4z" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"/><circle cx="12" cy="13" r="3.2" fill="none" stroke="#fff" stroke-width="2"/></svg>',
}


def phone(msgs, x=118, y=-18, rot=-3, w=304, h=478, typing=False, seen=True, hl=None, name="Jake | Coach"):
    """Instagram-style dark DM screen (lead's view). msgs: list of (side, text); side 'in' = coach account, 'out' = lead."""
    rows = []
    for i, (side, txt) in enumerate(msgs):
        last_in = side == "in" and (i + 1 == len(msgs) or msgs[i + 1][0] != "in")
        av = '<i class="av"></i>' if last_in else '<i class="av sp"></i>' if side == "in" else ""
        cls = "b " + side + (" hlb" if hl == i else "")
        rows.append(f'<div class="m {side}" style="--i:{i}">{av}<div class="{cls}">{txt}</div></div>')
    if seen and msgs and msgs[-1][0] == "out":
        rows.append(f'<div class="seen" style="--i:{len(msgs)}">Seen</div>')
    if typing:
        rows.append(f'<div class="m in" style="--i:{len(msgs)}"><i class="av"></i><div class="b in typing"><u></u><u></u><u></u></div></div>')
    return f'''<div class="ph" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)"><div class="scr">
<div class="sb"><b>9:41</b><span class="isl"></span><em><s></s><s></s><s></s><s></s></em></div>
<div class="hd">{ICON["back"]}<i class="pav"></i><div><b>{name}</b><small>Active now</small></div><span>{ICON["phone"]}{ICON["video"]}</span></div>
<div class="th">{"".join(rows)}</div>
<div class="in-bar"><i class="cam">{ICON["cam"]}</i><span>Message...</span>{ICON["mic"]}{ICON["img"]}{ICON["heart"]}</div>
</div></div>'''


DMS = ["still taking clients?", "how does it work?", "saw your post 🔥", "is this for beginners?", "can we hop on a call",
       "how do I start?", "u there?", "interested!!"]
COLS = [K, O, T, M, A, K, O, T]

frames = []

# 1 — DM avalanche
stack = "".join(
    f'<div class="row" style="top:{30 + i * 54}px;left:{-30 + (i % 3) * 14}px">'
    + bar(470 - (i % 4) * 30, COLS[i], 50, inner=f'<span class="dm"><em></em>{DMS[i]}</span>') + '</div>'
    for i in range(8))
frames.append(dict(label="Unread DMs", right="02:14 AM", num="48",
                   vis=stack + '<div class="badge" style="left:430px;top:6px">48</div>',
                   cap='<span class="hl">48 DMs</span> at 2&nbsp;AM.'))

# 2 — reply time race
race = (f'<div class="lbl" style="top:70px">YOU, ALONE</div><div class="row" style="top:96px;left:-20px">{bar(490, K, 70, inner="<span class=\'big pl\'>6h 12m</span>")}</div>'
        f'<div class="lbl" style="top:220px">WITH YOUR SETTER</div><div class="row" style="top:246px;left:-20px">{bar(170, O, 70, inner="<span class=\'big pl\'>2 min</span>")}</div>'
        + tag("&#9889; every lead, fast", T, 230, 268, -4))
frames.append(dict(label="Reply time", right="02:15 AM", num="2m",
                   vis=race, cap='You reply in <span class="g">6 hours.</span> We reply in <span class="hlo">minutes.</span>'))

# 3 — real conversation (IG DM)
frames.append(dict(label="A real conversation", right="02:16 AM", num="DM",
                   vis=phone([("out", "Heyy omg I just found your page and I'm obsessed with your content, been binging your posts all morning"),
                              ("in", "Appreciate that, glad it's been useful. What's the main thing you want to change in the next 90 days?"),
                              ("out", "Honestly I just want to drop like 8-10kg and actually stick with it this time")], hl=1)
                       + tag("right question", O, 372, 232, 7),
                   cap='Every lead gets a <span class="hl">real conversation.</span>'))

# 4 — the cost question, no prices
frames.append(dict(label="The cost question", right="02:18 AM", num="?",
                   vis=phone([("out", "Okay real talk - how much does coaching with Jake actually cost, and is there any guarantee?"),
                              ("in", "It depends on the goal, and Jake covers that on the call so you know exactly what fits you."),
                              ("in", "If this is something you're serious about starting now, I can help you find a time to talk")], rot=3, hl=2)
                       + tag("no dodge", K, 14, 150, -6) + tag("straight to the call", O, 300, 440, 4),
                   cap='The cost question? <span class="hl">Handled.</span>'))

# 5 — qualification checklist
chk = "".join(
    f'<div class="row" style="top:{50 + i * 92}px;left:{30 + i * 18}px">{bar(380, c, 68, inner=f"<span class=chk>&#10003;</span><span class=big2>{t}</span>")}</div>'
    for i, (t, c) in enumerate([("Goal", T), ("Timeline", O), ("Commitment", M), ("Decision maker", K)]))
frames.append(dict(label="Qualified in the DMs", right="02:21 AM", num="4/4", vis=chk,
                   cap='We <span class="hlo">qualify</span> them first.'))

# 6 — slots in the DM
frames.append(dict(label="Slots offered", right="02:23 AM", num="3",
                   vis=phone([("out", "Okay fair enough, yeah let's find a time, I'm in"),
                              ("in", "Quick one, what time zone are you in?"),
                              ("out", "I'm in Switzerland, so Central European time (CET)"),
                              ("in", "Got it. I've got Monday, October 26 at 1:00 PM, 3:00 PM, or 6:00 PM Swiss time, which works best?"),
                              ("out", "3:00 PM works for me")], rot=-2, hl=3)
                       + '<div class="flag" style="left:420px;top:330px"></div>',
                   cap='Three slots. <span class="hl">They pick one.</span>'))

# 7 — booked
frames.append(dict(label="Calendar", right="02:24 AM", num="✓",
                   vis=card('<div class="cal"><div class="calh">MONDAY · OCT 26</div><div class="calb"><b>3:00 PM</b><span>Strategy call · 30 min</span></div></div>', 60, 60, 400, -2)
                   + '<div class="stamp">BOOKED</div>',
                   cap='<span class="hlo">Booked.</span> Hands-free.'))

# 8 — calls booked per week (illustrative)
vals = [3, 4, 3, 9, 13, 16, 19]
chart = "".join(
    f'<div class="col" style="left:{20 + i * 66}px;height:{v * 17}px;--c:{K if i < 3 else O}"><span>{v}</span></div>'
    for i, v in enumerate(vals))
frames.append(dict(label="Calls booked per week", right="Week 7", num="19",
                   vis=f'<div class="chart">{chart}<div class="base"></div>'
                       f'<div class="cut" style="left:213px"><i>Setter on</i></div></div>',
                   cap='No missed <span class="hl">leads.</span>'))

# 9 — leads left on read
frames.append(dict(label="Leads left on read", right="Week 8", num="0",
                   vis=f'<div class="lbl" style="top:40px">BEFORE</div><div class="row" style="top:66px;left:-20px">{bar(460, M, 74, inner="<span class=\'big pl\'>27 leads ghosted</span>")}</div>'
                       f'<div class="lbl" style="top:200px">AFTER</div><div class="row" style="top:226px;left:-20px">{bar(110, T, 74, inner="<span class=\'big pl\'>0</span>")}</div>'
                       + tag("follow-ups done", A, 250, 250, -5) + tag("24/7", K, 330, 310, 4),
                   cap='No lead left <span class="hlo">on read.</span>'))

# 10 — CTA key
frames.append(dict(label="Your turn", right="Now", num="→",
                   vis='<div class="key">SETTER</div><div class="cbox"><i></i>Add a comment…<b>&#10148;</b></div>'
                       + tag("we'll DM you", O, 350, 40, 10),
                   cap='Comment <span class="hl">"SETTER"</span>'))

# 11 — DM arrives (IG DM)
frames.append(dict(label="Your DMs", right="Now", num="1",
                   vis=phone([("in", "Hey! Saw your comment 🙌"),
                              ("in", "What's your business, and roughly how many DMs do you get a week?"),
                              ("out", "Fitness coaching, around 40-50 a week"),
                              ("in", "Got it. Want me to show you how we'd turn those into booked calls?")], seen=False, typing=True, rot=2, name="Your Agency", hl=3)
                       + '<div class="badge" style="left:396px;top:-22px">1</div>',
                   cap="and we'll <span class=\"hlo\">DM you.</span>"))

# 12 — end card
frames.append(dict(label="DM setting", right="24/7", num="24",
                   vis='<div class="key big">24/7</div>' + tag("replies fast", T, 60, 300, -4) + tag("books calls", O, 270, 330, 5),
                   cap='Your DMs, <span class="hl">handled.</span>'))

PHONE_CSS = """
.ph{position:absolute;border-radius:40px;background:#0b0b0b;padding:9px;box-shadow:inset 0 0 0 2px #2b2b2b,0 0 0 1px #000,0 30px 50px rgba(50,30,10,.35),0 6px 0 #1a1a1a}
.scr{position:relative;width:100%;height:100%;border-radius:32px;overflow:hidden;background:#000;color:#fff;font-family:Inter,-apple-system,sans-serif;display:flex;flex-direction:column}
.sb{height:30px;display:flex;align-items:center;justify-content:space-between;padding:0 20px 0 24px;font:700 11px Inter;position:relative}
.sb .isl{position:absolute;left:50%;top:6px;width:72px;height:20px;margin-left:-36px;border-radius:12px;background:#111}
.sb em{display:flex;gap:2px;align-items:flex-end}.sb s{width:3px;background:#fff;border-radius:1px}.sb s:nth-child(1){height:4px}.sb s:nth-child(2){height:6px}.sb s:nth-child(3){height:8px}.sb s:nth-child(4){height:10px}
.hd{height:46px;display:flex;align-items:center;gap:9px;padding:0 12px;border-bottom:1px solid #1f1f1f}
.hd svg{width:20px;height:20px;flex:none}.hd .pav{width:30px;height:30px;border-radius:50%;flex:none;background:radial-gradient(circle at 50% 38%,#d9b59a 0 28%,transparent 29%),radial-gradient(circle at 50% 100%,#3b4a5c 0 45%,transparent 46%),#8a9bb0}
.hd b{display:block;font:700 14px Inter}.hd small{display:block;font:400 10px Inter;color:#a8a8a8}
.hd span{margin-left:auto;display:flex;gap:14px}
.th{flex:1;display:flex;flex-direction:column;justify-content:flex-end;gap:5px;overflow:hidden;padding:10px 10px 8px}
.m{display:flex;align-items:flex-end;gap:6px}.m.out{justify-content:flex-end}
.av{width:20px;height:20px;border-radius:50%;flex:none;background:radial-gradient(circle at 50% 38%,#d9b59a 0 28%,transparent 29%),radial-gradient(circle at 50% 100%,#3b4a5c 0 45%,transparent 46%),#8a9bb0}.av.sp{visibility:hidden}
.b{max-width:78%;padding:8px 12px;border-radius:18px;font:500 13.5px/1.3 Inter;letter-spacing:-.005em}
.b.in{background:#262626}
.b.out{background:linear-gradient(135deg,#3797F0 0%,#5B51F0 55%,#A033FF 100%)}
.b.hlb{box-shadow:0 0 0 2.5px #F2A33A,0 0 22px rgba(242,163,58,.55)}
.seen{align-self:flex-end;font:400 9.5px Inter;color:#a8a8a8;margin:1px 4px 0}
.typing{display:flex;gap:3px;padding:10px 12px}.typing u{width:6px;height:6px;border-radius:50%;background:#8e8e8e}
.in-bar{margin:6px 10px 14px;height:38px;border-radius:19px;background:#262626;display:flex;align-items:center;gap:10px;padding:0 12px 0 4px;font:400 11.5px Inter;color:#a8a8a8}
.in-bar .cam{width:30px;height:30px;border-radius:50%;background:#3797F0;display:grid;place-items:center}.in-bar .cam svg{width:17px;height:17px}
.in-bar span{flex:1}.in-bar>svg{width:18px;height:18px}
"""

TICKS = ["F1", "F3", "F5", "F7", "F9", "F11"]


def frame(i, f):
    knob = 40 + i * (460 / 11)
    ticks = "".join(f'<span style="left:{40 + j * 2 * (460 / 11)}px">{h}</span>' for j, h in enumerate(TICKS))
    return f'''<section class="fr">
<div class="num">{f["num"]}</div>
<header><div class="rule"></div><span>{f["label"]}</span><em>{f["right"]}</em></header>
<div class="vis">{f["vis"]}</div>
<div class="cap">{f["cap"]}</div>
<div class="scrub"><div class="line"></div><div class="prog" style="width:{knob - 40}px"></div><div class="fl" style="left:{40 + 6 * (460 / 11)}px"></div>
<div class="knob" style="left:{knob - 9}px"></div>{ticks}<small class="l">Values illustrative</small><small class="r">Frame {i + 1} of 12</small></div>
</section>'''


html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Paper Data Storyboard</title><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#1a1a1a;font-family:Inter,sans-serif;width:3284px;padding:12px;display:grid;grid-template-columns:repeat(6,540px);gap:4px}}
.fr{{position:relative;width:540px;height:960px;overflow:hidden;color:{K};
 background:radial-gradient(120% 90% at 50% 40%,#F4F0E8 0%,#ECE6DA 70%,#E2DBCD 100%)}}
.fr::before{{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.035) 0 1px,transparent 1px 36px),repeating-linear-gradient(90deg,rgba(0,0,0,.035) 0 1px,transparent 1px 36px)}}
.num{{position:absolute;left:-20px;bottom:-120px;font:800 430px/1 Inter;letter-spacing:-.06em;color:rgba(60,45,25,.06);white-space:nowrap}}
header{{position:absolute;left:40px;right:40px;top:78px;border-top:1px solid {K};padding-top:10px;display:flex;justify-content:space-between;font:800 13px Inter;letter-spacing:.08em;text-transform:uppercase}}
header .rule{{position:absolute;left:0;top:-3px;width:46px;height:5px;background:{K}}}
header em{{font-style:normal}}
.vis{{position:absolute;left:0;right:0;top:125px;height:470px}}
.cap{{position:absolute;left:40px;right:40px;top:620px;font:800 44px/1.08 Inter;letter-spacing:-.035em}}
.hl,.hlo{{color:#fff;background:{K};padding:0 .12em;border-radius:.08em;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
.hlo{{background:{O}}}
.g{{color:#9A9286}}
.scrub{{position:absolute;left:0;right:0;top:820px;height:70px;font:700 11px Inter;color:#6D665B}}
.scrub .line{{position:absolute;left:40px;right:40px;top:0;height:2px;background:#bdb5a7}}
.scrub .prog{{position:absolute;left:40px;top:-1px;height:4px;background:{K}}}.scrub .prog::after{{content:"";position:absolute;left:{40+6*460/11-40}px;right:0;top:0;bottom:0;background:{O}}}
.scrub .knob{{position:absolute;top:-8px;width:18px;height:18px;border-radius:50%;background:{K};box-shadow:0 3px 6px rgba(0,0,0,.3)}}
.scrub .fl{{position:absolute;top:-26px;width:2px;height:26px;background:{O}}}.scrub .fl::after{{content:"";position:absolute;left:2px;top:0;border-left:14px solid {O};border-top:6px solid transparent;border-bottom:6px solid transparent}}
.scrub span{{position:absolute;top:14px;transform:translateX(-50%)}}
.scrub small{{position:absolute;top:34px;font:500 10px Inter}}.scrub .l{{left:40px}}.scrub .r{{right:40px}}
.row{{position:absolute}}
.bar{{position:relative;border-radius:7px;display:flex;align-items:center;padding:0 18px;color:#fff;
 background:linear-gradient(180deg,color-mix(in srgb,var(--c),#fff 22%) 0%,var(--c) 45%,color-mix(in srgb,var(--c),#000 18%) 100%);
 box-shadow:inset 0 2px 0 rgba(255,255,255,.35),0 8px 0 color-mix(in srgb,var(--c),#000 40%),0 22px 30px rgba(50,30,10,.28)}}
.bar b{{font:800 18px Inter}}
.dm{{display:flex;align-items:center;gap:10px;font:700 19px Inter;white-space:nowrap}}
.dm em{{width:24px;height:24px;border-radius:6px;background:rgba(255,255,255,.9);box-shadow:inset 0 0 0 5px rgba(0,0,0,.15)}}
.pl{{padding-left:24px}}
.big{{font:800 30px Inter;letter-spacing:-.02em;white-space:nowrap}}.big2{{font:800 28px Inter;letter-spacing:-.02em}}
.chk{{width:34px;height:34px;border-radius:50%;background:#fff;color:{K};display:grid;place-items:center;font:900 20px Inter;margin-right:14px}}
.lbl{{position:absolute;left:40px;font:800 13px Inter;letter-spacing:.12em}}
.badge{{position:absolute;min-width:62px;height:62px;padding:0 12px;border-radius:31px;background:{O};color:#fff;font:800 30px Inter;display:grid;place-items:center;box-shadow:0 5px 0 #8f3510,0 14px 24px rgba(0,0,0,.3);border:3px solid #fff}}
.tag{{position:absolute;padding:8px 14px 8px 22px;border-radius:6px;color:#fff;font:800 17px Inter;white-space:nowrap;box-shadow:0 4px 0 rgba(0,0,0,.25),0 12px 20px rgba(0,0,0,.2)}}
.tag::before{{content:"";position:absolute;left:8px;top:50%;width:7px;height:7px;margin-top:-3.5px;border-radius:50%;background:#F4F0E8}}
.card{{position:absolute;background:#FBFAF6;border-radius:16px;padding:18px;box-shadow:0 2px 0 #d8d1c3,0 24px 40px rgba(70,50,20,.22)}}
.bub .who{{display:flex;align-items:center;gap:10px;font:800 14px Inter;letter-spacing:.04em;text-transform:uppercase;margin-bottom:10px}}
.bub .who i{{width:30px;height:30px;border-radius:50%;background:{K};color:#fff;font:800 12px Inter;font-style:normal;display:grid;place-items:center}}
.bub .who i.ai{{background:{O}}}
.bub .who span{{margin-left:auto;font-weight:500;color:#9A9286;text-transform:none}}
.bub .txt{{font:700 26px/1.25 Inter;letter-spacing:-.02em}}
mark{{background:{K};color:#fff;padding:0 .1em;border-radius:.1em}}mark.o{{background:{O}}}
.ptag{{position:absolute;width:190px;padding:22px 16px 18px;border-radius:10px 10px 10px 10px;background:#F7F3EA;border:2px solid {K};font:800 34px Inter;text-align:center;box-shadow:0 6px 0 #c9c0b0,0 20px 30px rgba(0,0,0,.2)}}
.ptag::before{{content:"";position:absolute;left:50%;top:9px;width:12px;height:12px;margin-left:-6px;border-radius:50%;border:2px solid {K};background:#ECE6DA}}
.ptag small{{display:block;font:600 14px Inter;color:#7d766a;margin-top:4px}}.ptag s{{text-decoration-thickness:4px;text-decoration-color:{O}}}
.ptag.dark{{background:{K};color:#fff;font-size:30px}}.ptag.dark small{{color:#bdb5a7}}
.slot{{position:absolute;top:140px;width:140px;height:170px;border-radius:14px;background:#FBFAF6;box-shadow:0 6px 0 #d0c8b8,0 20px 30px rgba(0,0,0,.18);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px}}
.slot small{{font:800 12px Inter;letter-spacing:.12em;color:#8a8275}}.slot b{{font:800 42px Inter;letter-spacing:-.03em}}
.slot.up{{top:96px;background:{O};color:#fff;box-shadow:0 8px 0 #8f3510,0 28px 40px rgba(0,0,0,.28);transform:rotate(-3deg)}}.slot.up small{{color:#ffe1d3}}
.slot em{{font:800 12px Inter;font-style:normal;background:#fff;color:{O};padding:3px 8px;border-radius:4px;text-transform:uppercase;letter-spacing:.1em}}
.flag{{position:absolute;width:3px;height:60px;background:{K}}}.flag::after{{content:"";position:absolute;left:3px;top:0;border-left:30px solid {O};border-top:12px solid transparent;border-bottom:12px solid transparent}}
.cal .calh{{background:{O};color:#fff;font:800 15px Inter;letter-spacing:.12em;padding:12px 16px;border-radius:10px 10px 0 0;margin:-18px -18px 0}}
.cal .calb{{padding:26px 4px 10px}}.cal b{{display:block;font:800 72px Inter;letter-spacing:-.05em}}.cal span{{font:600 18px Inter;color:#7d766a}}
.stamp{{position:absolute;left:230px;top:250px;padding:10px 22px;border:6px solid {O};color:{O};font:900 50px Inter;letter-spacing:.06em;border-radius:12px;transform:rotate(-12deg);background:rgba(244,240,232,.6)}}
.chart{{position:absolute;left:40px;top:40px;width:460px;height:380px}}
.col{{position:absolute;bottom:40px;width:50px;border-radius:6px 6px 2px 2px;background:linear-gradient(90deg,color-mix(in srgb,var(--c),#fff 15%),var(--c));box-shadow:6px 0 0 color-mix(in srgb,var(--c),#000 40%),0 16px 22px rgba(0,0,0,.2)}}
.col span{{position:absolute;top:-30px;left:0;right:0;text-align:center;font:800 20px Inter;color:{K}}}
.base{{position:absolute;left:-10px;right:-10px;bottom:30px;height:10px;border-radius:4px;background:{K}}}
.cut{{position:absolute;top:0;bottom:30px;border-left:2px dashed {O}}}.cut i{{position:absolute;top:-6px;left:6px;background:{O};color:#fff;font:800 13px Inter;font-style:normal;padding:4px 8px;border-radius:4px;white-space:nowrap}}
.key{{position:absolute;left:60px;top:90px;width:420px;height:170px;border-radius:26px;display:grid;place-items:center;color:#fff;font:900 76px Inter;letter-spacing:-.02em;
 background:linear-gradient(180deg,#E8703C,{O} 50%,#B9441A);box-shadow:inset 0 3px 0 rgba(255,255,255,.4),0 16px 0 #7f2e0d,0 40px 50px rgba(0,0,0,.3)}}
.key.big{{font-size:110px;top:70px;height:200px}}
.cbox{{position:absolute;left:60px;top:320px;width:420px;height:58px;border-radius:29px;background:#FBFAF6;border:1px solid #d6cfc1;display:flex;align-items:center;gap:12px;padding:0 10px;font:500 19px Inter;color:#8a8275;box-shadow:0 10px 20px rgba(0,0,0,.12)}}
.cbox i{{width:38px;height:38px;border-radius:50%;background:{K}}}.cbox b{{margin-left:auto;color:{K}}}
{PHONE_CSS}</style></head><body>{"".join(frame(i, f) for i, f in enumerate(frames))}</body></html>'''
open(os.path.join(here, "storyboard.html"), "w").write(html)
print("ok", len(frames))
```

---
## Source: `storyboards/paper-data/video.py`
```python
"""Animated paper-style videos: one shared body (storyboard frames 2-12) + one hook per video.
Steps:  python3 video.py vo        -> ElevenLabs VO per scene (build/vo/paper_*.mp3/json)
        python3 video.py html      -> video_<hook>.html + timeline_<hook>.json for hooks A, B, C
then    node render_video.mjs <hook> ; python3 video.py mix <hook>
"""
import json, os, re, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
studio = os.path.abspath(os.path.join(here, "..", ".."))
build = os.path.join(studio, "build")
ns = {"__file__": os.path.join(here, "build.py")}
exec(open(os.path.join(here, "build.py")).read(), ns)  # storyboard components + frames
K, O, T_, M, A = ns["K"], ns["O"], ns["T"], ns["M"], ns["A"]
bar, tag, frames = ns["bar"], ns["tag"], ns["frames"]
BASE_CSS = re.search(r"<style>(.*?)</style>", ns["html"], re.S).group(1)
VOICE = "EXAVITQu4vr4xnSDxMaL"  # Sarah

DMS = ["still taking clients?", "how does it work?", "saw your post 🔥", "is this for beginners?", "can we hop on a call",
       "how do I start?", "u there?", "interested!!"]
COLS = [K, O, T_, M, A, K, O, T_]


def stack(fall=False):
    return "".join(
        f'<div class="row" style="top:{30 + i * 54}px;left:{-30 + (i % 3) * 14}px">'
        + bar(470 - (i % 4) * 30, COLS[i], 50, inner=f'<span class="dm"><em></em>{DMS[i]}</span>',
              z=f"--f:{7 - i};" if fall else "").replace('class="bar"', 'class="bar fall"' if fall else 'class="bar"') + '</div>'
        for i in range(8))


HOOKS = {
    "A": dict(label="Unread DMs", right="02:14 AM", num="12",
              vis=stack() + '<div class="badge" style="left:430px;top:6px">12</div>'
                  + '<div class="tag xl" style="left:22px;top:-14px;background:#D8541E;transform:rotate(-4deg)">FOR COACHES</div>',
              cap='<span class="hl">12 DMs</span> at 2&nbsp;AM. You\'re <span class="hlo">asleep.</span>',
              vo="Twelve DMs at 2 AM. You're asleep."),
    "B": dict(label="Your DMs", right="Right now", num="↓",
              vis=stack(fall=True) + '<div class="badge" style="left:430px;top:6px">48</div>',
              cap='Stop posting more content. Your DMs are <span class="hlo">leaking clients.</span>',
              vo="Stop posting more content. Your DMs are leaking clients."),
    "C": dict(label="Speed to lead", right="HBR · 2011", num="7×",
              vis=f'<div class="lbl" style="top:40px">ANSWERED WITHIN 1 HOUR</div><div class="row" style="top:66px;left:-20px">{bar(490, O, 96, inner="<span class=\'huge pl\'>7×</span>")}</div>'
                  f'<div class="lbl" style="top:230px">AN HOUR LATER</div><div class="row" style="top:256px;left:-20px">{bar(130, K, 96, inner="<span class=\'huge pl\'>1×</span>")}</div>'
                  + tag("Harvard Business Review, 2011", T_, 190, 390, -3),
              cap='Reply within an hour. <span class="hl">7×</span> more real conversations.',
              vo="Reply within an hour. Seven-times more real conversations."),
}
BODY_VO = ["You reply in six hours. We reply in minutes.", "Every lead gets a real conversation.",
           "The cost question? Handled.", "We qualify them first.", "Three slots. They pick one.",
           "Booked. Hands-free.", "No missed leads.", "No lead left on read.", 'Comment "SETTER",',
           "and we'll DM you.", "Your DMs, handled."]
# per-scene sound design: (offset seconds, sfx, gain dB)
BODY_SFX = [[(0.12, "whoosh", -16), (0.55, "pop", -12)], [(0.35, "pop", -13), (0.73, "pop", -13), (1.11, "pop", -13)],
            [(0.35, "pop", -13), (0.73, "pop", -13), (1.11, "pop", -13)], [(0.2, "ding", -12), (0.5, "ding", -13), (0.8, "ding", -14), (1.1, "ding", -15)],
            [(0.35, "pop", -13), (0.73, "pop", -13), (1.11, "pop", -13), (1.49, "pop", -13), (1.9, "ding", -9)],
            [(0.55, "boom", -8)], [(0.2, "whoosh", -16), (0.8, "ding", -12)], [(0.6, "pop", -12)],
            [(0.15, "whoosh", -14), (1.1, "click", -6)], [(0.35, "pop", -12), (0.73, "pop", -12), (1.1, "pop", -12)],
            [(0.2, "boom", -9), (0.7, "ding", -10)]]
HOOK_SFX = {"A": [(0.0, "boom", -7), (0.3, "pop", -12)], "B": [(0.0, "boom", -7), (1.4, "whoosh", -12)],
            "C": [(0.0, "boom", -7), (0.4, "riser", -16)]}

ANIM_CSS = """
#stage{width:540px;height:960px;zoom:2;position:relative;overflow:hidden;background:#ECE6DA}
body{width:1080px;height:1920px;padding:0;display:block;background:#ECE6DA}
.fr{position:absolute;inset:0;opacity:0}
.fr.on{opacity:1}
.fr *{animation-fill-mode:both;animation-play-state:paused}
.fr{animation:push var(--dur) linear both paused}
@keyframes push{from{scale:1}to{scale:1.06}}
.num{animation:numIn .9s cubic-bezier(.2,.8,.2,1) calc(0ms - var(--pre)) both}
@keyframes numIn{from{translate:0 80px;opacity:0}}
header{animation:fadeIn .5s ease calc(0ms - var(--pre)) both}
@keyframes fadeIn{from{opacity:0;translate:0 -8px}}
.row{animation:barIn .7s cubic-bezier(.2,.9,.3,1.12) calc(var(--k,0)*70ms + 80ms - var(--pre)) both}
@keyframes barIn{from{translate:-115% 0}}
.bar.fall{animation:fall .65s cubic-bezier(.5,0,.9,.4) calc(1300ms + var(--f,0)*110ms - var(--pre)) both}
@keyframes fall{to{translate:60px 900px;rotate:24deg;opacity:.0}}
.lbl{animation:fadeIn .4s ease calc(var(--k,0)*150ms - var(--pre)) both}
.ph{animation:phIn .75s cubic-bezier(.2,.9,.3,1.1) calc(40ms - var(--pre)) both}
@keyframes phIn{from{translate:0 140px;opacity:0;scale:.9}}
.card{animation:phIn .7s cubic-bezier(.2,.9,.3,1.1) calc(var(--k,0)*150ms + 40ms - var(--pre)) both}
.m{animation:msgIn .32s cubic-bezier(.2,.9,.3,1.3) calc(350ms + var(--i,0)*380ms - var(--pre)) both}
.seen{animation:fadeIn .3s ease calc(350ms + var(--i,0)*380ms - var(--pre)) both}
@keyframes msgIn{from{opacity:0;translate:0 14px;scale:.85}}
.badge{animation:pop .45s cubic-bezier(.2,.9,.3,1.6) calc(320ms - var(--pre)) both}
.tag{animation:pop .45s cubic-bezier(.2,.9,.3,1.6) calc(var(--k,0)*160ms + 650ms - var(--pre)) both}
.tag.xl{font-size:22px;padding:10px 16px 10px 28px;animation-delay:calc(150ms - var(--pre))}
@keyframes pop{from{scale:0;opacity:0}}
.slot{animation:phIn .6s cubic-bezier(.2,.9,.3,1.2) calc(var(--k,0)*120ms + 80ms - var(--pre)) both}
.flag{animation:pop .4s cubic-bezier(.2,.9,.3,1.6) calc(1950ms - var(--pre)) both}
.stamp{animation:stamp .32s cubic-bezier(.5,0,.8,.5) calc(520ms - var(--pre)) both}
@keyframes stamp{from{scale:2.8;opacity:0}}
.vis.shake{animation:shake .45s linear calc(840ms - var(--pre)) both}
@keyframes shake{0%,100%{translate:0 0}15%{translate:-7px 4px}30%{translate:6px -5px}45%{translate:-5px 3px}60%{translate:4px -2px}80%{translate:-2px 1px}}
.col{transform-origin:bottom;animation:grow .6s cubic-bezier(.2,.9,.3,1.1) calc(var(--k,0)*90ms + 100ms - var(--pre)) both}
@keyframes grow{from{scale:1 0}}
.cut{animation:fadeIn .4s ease calc(800ms - var(--pre)) both}
.key{animation:keyIn .6s cubic-bezier(.2,.9,.3,1.2) calc(60ms - var(--pre)) both}
@keyframes keyIn{from{translate:0 -60px;opacity:0}}
.key.press{animation:keyIn .6s cubic-bezier(.2,.9,.3,1.2) calc(60ms - var(--pre)) both,press .28s ease calc(1050ms - var(--pre)) both}
@keyframes press{50%{scale:.94 .9}}
.cbox{animation:fadeUp .5s ease calc(450ms - var(--pre)) both}
@keyframes fadeUp{from{opacity:0;translate:0 20px}}
.huge{font:900 64px Inter;letter-spacing:-.04em}
.cap{z-index:5}
.ph,.card,.slot.up,.key{animation-composition:replace}
.ph{animation:phIn .75s cubic-bezier(.2,.9,.3,1.1) calc(40ms - var(--pre)) both,bob 2.6s ease-in-out calc(800ms - var(--pre)) infinite alternate none}
.card{animation:phIn .7s cubic-bezier(.2,.9,.3,1.1) calc(var(--k,0)*150ms + 40ms - var(--pre)) both,bob 2.2s ease-in-out calc(800ms - var(--pre)) infinite alternate none}
.tag{animation:pop .45s cubic-bezier(.2,.9,.3,1.6) calc(var(--k,0)*160ms + 650ms - var(--pre)) both,wig 1.4s ease-in-out calc(1100ms - var(--pre)) infinite alternate none}
.tag.xl{animation:pop .45s cubic-bezier(.2,.9,.3,1.6) calc(150ms - var(--pre)) both,wig 1.2s ease-in-out calc(600ms - var(--pre)) infinite alternate none}
.badge{animation:pop .45s cubic-bezier(.2,.9,.3,1.6) calc(320ms - var(--pre)) both,beat .9s ease-in-out calc(800ms - var(--pre)) infinite none}
@keyframes bob{from{rotate:-.9deg}to{rotate:.9deg}}
@keyframes wig{from{rotate:-3deg}to{rotate:3deg}}
@keyframes beat{0%,100%{scale:1}15%{scale:1.14}30%{scale:1}}
.b.hlb{animation:glow 1s ease-in-out calc(700ms + var(--i,0)*380ms - var(--pre)) infinite alternate none}
@keyframes glow{to{box-shadow:0 0 0 3.5px #F2A33A,0 0 34px rgba(242,163,58,.9)}}
.num{animation:numIn .9s cubic-bezier(.2,.8,.2,1) calc(0ms - var(--pre)) both,drift 4s linear calc(900ms - var(--pre)) infinite alternate none}
@keyframes drift{to{translate:-26px 0}}
.row{animation:barIn .7s cubic-bezier(.2,.9,.3,1.12) calc(var(--k,0)*70ms + 80ms - var(--pre)) both,sway 2.4s ease-in-out calc(900ms + var(--k,0)*90ms - var(--pre)) infinite alternate none}
@keyframes sway{to{translate:10px 0}}
.wipe{position:absolute;inset:-10%;z-index:20;pointer-events:none;opacity:0}
.cf{position:absolute;left:50%;top:45%;width:9px;height:14px;border-radius:2px;background:var(--c);z-index:6;
 animation:conf 1.3s cubic-bezier(.15,.7,.4,1) calc(var(--cd) - var(--pre)) both}
@keyframes conf{from{translate:0 0;rotate:0deg;opacity:1}75%{opacity:1}to{translate:var(--x) var(--y);rotate:var(--r);opacity:0}}
.key.press::after{content:"";position:absolute;left:50%;top:50%;width:40px;height:40px;margin:-20px;border-radius:50%;border:4px solid #fff;animation:ripple .6s ease-out calc(1080ms - var(--pre)) both}
@keyframes ripple{from{scale:.2;opacity:.9}to{scale:9;opacity:0}}

.w{display:inline-block;animation:wordIn .26s cubic-bezier(.2,.9,.3,1.3) var(--wd) both}
@keyframes wordIn{from{opacity:0;translate:0 18px;scale:.6}}
.cap .hl,.cap .hlo{background:linear-gradient(var(--hb),var(--hb)) no-repeat 0 0/0% 100%;color:#1B1B1B;animation:wipe .3s ease var(--wd) both}
.cap .hl{--hb:#1B1B1B}.cap .hlo{--hb:#D8541E}
@keyframes wipe{to{background-size:100% 100%;color:#fff}}
.scrub .knob{animation:slideK .5s cubic-bezier(.3,.9,.3,1) both}
@keyframes slideK{from{left:var(--from)}}
.scrub .prog{animation:slideP .5s cubic-bezier(.3,.9,.3,1) both}
@keyframes slideP{from{width:var(--pfrom)}}
"""


def words_of(alignment):
    ch, st = alignment["characters"], alignment["character_start_times_seconds"]
    out, cur, s = [], "", 0
    for i, c in enumerate(ch):
        if c == " ":
            if cur: out.append(s)
            cur = ""
        else:
            if not cur: s = st[i]
            cur += c
    if cur: out.append(s)
    return out, alignment["character_end_times_seconds"][-1]


def caption_html(cap, wtimes, vo_at):
    # tokenise into (text, cls) chunks
    parts, pos = [], 0
    for m in re.finditer(r'<span class="(hl|hlo|g)">(.*?)</span>', cap):
        if m.start() > pos: parts.append((cap[pos:m.start()], None))
        parts.append((m.group(2), m.group(1))); pos = m.end()
    if pos < len(cap): parts.append((cap[pos:], None))
    toks = [(w, cls) for txt, cls in parts for w in txt.split()]
    n, nv = len(toks), len(wtimes)
    delay = [vo_at + wtimes[min(nv - 1, round(k * nv / n))] for k in range(n)]
    html, k = [], 0
    for txt, cls in parts:
        ws = txt.split()
        if not ws: continue
        inner = " ".join(f'<span class="w" style="--wd:{int(delay[k + j] * 1000)}ms">{w}</span>' for j, w in enumerate(ws))
        if cls in ("hl", "hlo"):
            inner = f'<span class="{cls}" style="--wd:{int(delay[k] * 1000)}ms">{inner}</span>'
        elif cls == "g":
            inner = f'<span class="g">{inner}</span>'
        html.append(inner); k += len(ws)
    return " ".join(html)


def confetti(n=30, seed=3, delay=600):
    import random
    r = random.Random(seed); cols = ["#D8541E", "#1E9E95", "#D9257E", "#F2A33A", "#1B1B1B"]
    return "".join(f'<i class="cf" style="--c:{r.choice(cols)};--x:{r.uniform(-260, 260):.0f}px;--y:{r.uniform(-330, 120):.0f}px;'
                   f'--r:{r.uniform(-540, 540):.0f}deg;--cd:{delay + r.randint(0, 120)}ms"></i>' for _ in range(n))


def index_classes(vis):
    for cls in ("row", "slot", "col", "tag", "card", "lbl"):
        n = [0]
        def sub(m):
            n[0] += 1
            return m.group(0).replace('style="', f'style="--k:{n[0] - 1};', 1)
        vis = re.sub(rf'<div class="{cls}[^"]*" style="', sub, vis)
    return vis


def scenes_for(hook):
    return [dict(HOOKS[hook], id=f"paper_hook{hook}", sfx=HOOK_SFX[hook])] + [
        dict(frames[i + 1], id=f"paper_body{i + 2:02d}", vo=BODY_VO[i], sfx=BODY_SFX[i]) for i in range(11)]


def cmd_vo():
    os.makedirs(os.path.join(build, "vo"), exist_ok=True)
    allsc = [s for h in "ABC" for s in scenes_for(h)[:1]] + scenes_for("A")[1:]
    for i, s in enumerate(allsc):
        p = os.path.join(build, "vo", s["id"])
        if os.path.exists(p + ".json"): continue
        body = {"text": s["vo"], "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True}}
        json.dump(body, open(p + ".req", "w"))
        subprocess.run(["curl", "-sS", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
                        "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json", "-d", "@" + p + ".req", "-o", p + ".json"], check=True)
        d = json.load(open(p + ".json")); assert "audio_base64" in d, d
        import base64
        open(p + ".mp3", "wb").write(base64.b64decode(d.pop("audio_base64"))); json.dump(d, open(p + ".json", "w"))
        print(s["id"], round(d["alignment"]["character_end_times_seconds"][-1], 2))


def cmd_html(hook):
    sc = scenes_for(hook)
    t, secs, cues, sfx = 0.0, [], [], []
    n = len(sc)
    for i, s in enumerate(sc):
        al = json.load(open(os.path.join(build, "vo", s["id"] + ".json")))["alignment"]
        wt, vdur = words_of(al)
        pre = 450 if i == 0 else 0
        vo_at = 0.12 if i else 0.05
        dur = max(1.9, vo_at + vdur + 0.5) + (1.4 if i == n - 1 else 0)
        knob = 40 + i * (460 / 11)
        prev = 40 + max(0, i - 1) * (460 / 11)
        ticks = "".join(f'<span style="left:{40 + j * 2 * (460 / 11)}px">{h}</span>' for j, h in enumerate(ns["TICKS"]))
        vis = index_classes(s["vis"])
        vis_cls = "vis shake" if "stamp" in vis else "vis"
        if "stamp" in vis: vis += confetti(34, 5, 600)
        if "24/7" in s["vis"] and "key big" in s["vis"]: vis += confetti(30, 9, 250)
        if 'class="key' in vis and "SETTER" in vis: vis += confetti(22, 7, 1100)
        vis = re.sub(r'(<div class="col" style="--k:(\d+);[^"]*"><span>)(\d+)(</span>)',
                     lambda m: f'{m.group(1)}<b data-count="{m.group(3)}" data-cd="{int(m.group(2)) * 90 + 100}">{m.group(3)}</b>{m.group(4)}', vis)
        if "class=\"key\"" in vis and "SETTER" in vis: vis = vis.replace('class="key"', 'class="key press"')
        secs.append(f'''<section class="fr" data-t0="{t:.3f}" data-pre="{pre}" style="--dur:{dur:.2f}s;--pre:{pre}ms">
<div class="num">{s["num"]}</div>
<header><div class="rule"></div><span>{s["label"]}</span><em>{s["right"]}</em></header>
<div class="{vis_cls}">{vis}</div>
<div class="cap">{caption_html(s["cap"], wt, vo_at - (0.6 if i == 0 else 0))}</div>
<div class="scrub"><div class="line"></div><div class="prog" style="width:{knob - 40}px;--pfrom:{prev - 40}px"></div><div class="fl" style="left:{40 + 6 * (460 / 11)}px"></div>
<div class="knob" style="left:{knob - 9}px;--from:{prev - 9}px"></div>{ticks}<small class="l">Values illustrative</small><small class="r">Frame {i + 1} of 12</small></div>
</section>''')
        cues.append({"id": s["id"], "at": round(t + vo_at, 3)})
        for off, f, g in s["sfx"]: sfx.append({"file": f, "at": round(t + off, 3), "gain": g})
        if i: sfx.append({"file": "whoosh", "at": round(t - 0.12, 3), "gain": -15})
        t += dur
    html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Paper Video {hook}</title><style>{BASE_CSS}{ANIM_CSS}</style></head>
<body><div id="stage">{"".join(secs)}</div>
<script>
const S=[...document.querySelectorAll('.fr')].map(el=>({{el,t0:+el.dataset.t0}}));
window.ready=(async()=>{{await document.fonts.ready;S.forEach(s=>s.anims=s.el.getAnimations({{subtree:true}}));S.forEach(s=>s.anims.forEach(a=>a.pause()));}})();
const ease=x=>x>=1?1:1-Math.pow(2,-10*x),TR=.34,TYPES=['left','up','zoom'];
window.render=t=>{{let cur=0;S.forEach((s,i)=>{{if(t>=s.t0)cur=i}});
 const lt=t-S[cur].t0,inT=cur>0&&lt<TR,p=ease(lt/TR),ty=TYPES[cur%3];
 S.forEach((s,i)=>{{const on=i===cur||(inT&&i===cur-1);s.el.classList.toggle('on',on);s.el.style.transform='';s.el.style.filter='';s.el.style.zIndex=i===cur?2:1;
  if(!on)return;const loc=(t-s.t0)*1000;s.anims.forEach(a=>a.currentTime=Math.max(0,loc));
  s.el.querySelectorAll('[data-count]').forEach(e=>{{const q=Math.min(1,Math.max(0,(loc-(+e.dataset.cd))/800));e.textContent=Math.round(+e.dataset.count*(1-Math.pow(1-q,3)))}});}});
 if(inT){{const a=S[cur].el,b=S[cur-1].el;
  if(ty==='left'){{a.style.transform=`translateX(${{(1-p)*100}}%) rotate(${{(1-p)*4}}deg)`;b.style.transform=`translateX(${{-p*60}}%) rotate(${{-p*3}}deg)`;b.style.filter=`blur(${{p*6}}px)`}}
  else if(ty==='up'){{a.style.transform=`translateY(${{(1-p)*100}}%)`;b.style.transform=`translateY(${{-p*40}}%) scale(${{1-p*.1}})`;b.style.filter=`blur(${{p*6}}px)`}}
  else{{a.style.transform=`scale(${{.7+.3*p}})`;a.style.opacity=p;b.style.transform=`scale(${{1+p*.6}})`;b.style.filter=`blur(${{p*10}}px)`}}
 }} else S.forEach(s=>s.el.style.opacity='');}};
</script></body></html>'''
    open(os.path.join(here, f"video_{hook}.html"), "w").write(html)
    json.dump({"duration": round(t, 3), "fps": 30, "cues": cues, "sfx": sfx}, open(os.path.join(here, f"timeline_{hook}.json"), "w"), indent=1)
    print(hook, "duration", round(t, 2))


def cmd_mix(hook):
    T = json.load(open(os.path.join(here, f"timeline_{hook}.json"))); dur = T["duration"]
    inputs, filt, vo, fx = [], [], [], []
    def inp(p, loop=False):
        if loop: inputs.extend(["-stream_loop", "-1"])
        inputs.extend(["-i", p]); return len([x for x in inputs if x == "-i"]) - 1
    for c in T["cues"]:
        i = inp(os.path.join(build, "vo", c["id"] + ".mp3")); ms = int(c["at"] * 1000)
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]"); vo.append(f"[v{i}]")
    for s in T["sfx"]:
        i = inp(os.path.join(build, "sfx", s["file"] + ".mp3")); ms = int(s["at"] * 1000)
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={s['gain']}dB,adelay={ms}|{ms}[x{i}]"); fx.append(f"[x{i}]")
    mi = inp(os.path.join(build, "bed.mp3"), loop=True)
    filt.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},volume=-20dB,afade=t=in:d=0.4,afade=t=out:st={dur - 2}:d=2[mus]")
    filt.append(f"{''.join(vo)}amix=inputs={len(vo)}:normalize=0,asplit=2[vo][vk]")
    filt.append("[mus][vk]sidechaincompress=threshold=0.02:ratio=12:attack=20:release=350[musd]")
    filt.append(f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0[fx]")
    filt.append("[vo]highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,equalizer=f=3500:t=q:w=1:g=2[vop]")
    filt.append(f"[vop][musd][fx]amix=inputs=3:normalize=0,atrim=0:{dur},loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000[out]")
    mix = os.path.join(build, f"paper_mix_{hook}.m4a")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-c:a", "aac", "-b:a", "256k", mix], check=True)
    out = os.path.join(here, "out"); os.makedirs(out, exist_ok=True)
    final = os.path.join(out, f"paper_hook{hook}_9x16.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(build, f"paper_video_{hook}.mp4"), "-i", mix, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "copy", "-shortest", "-movflags", "+faststart", final], check=True)
    print("final ->", final)


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "vo": cmd_vo()
    elif c == "html": [cmd_html(h) for h in (sys.argv[2:] or "ABC")]
    elif c == "mix": cmd_mix(sys.argv[2])
```

---
## Source: `storyboards/paper-data/render_video.mjs`
```javascript
// Renders video_<hook>.html frame-by-frame -> ../../build/paper_video_<hook>.mp4
// Usage: node render_video.mjs <hook> [--preview t1,t2] [--workers N]
import { createRequire } from 'node:module';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const { chromium } = createRequire(import.meta.url)('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const build = path.join(here, '..', '..', 'build');
const [hook, ...rest] = process.argv.slice(2);
const opt = (k, d) => { const i = rest.indexOf(k); return i >= 0 ? rest[i + 1] : d; };
const T = JSON.parse(fs.readFileSync(path.join(here, `timeline_${hook}.json`), 'utf8'));
const W = +opt('--workers', 4), fps = T.fps, total = Math.round(T.duration * fps);
const url = pathToFileURL(path.join(here, `video_${hook}.html`)).href;

const browser = await chromium.launch();
async function page() {
  const p = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto(url); await p.evaluate(() => window.ready); return p;
}
const preview = opt('--preview', null);
if (preview) {
  const p = await page(); fs.mkdirSync(path.join(here, 'out'), { recursive: true });
  for (const t of preview.split(',').map(Number)) {
    await p.evaluate(t => window.render(t), t);
    await p.screenshot({ path: path.join(here, 'out', `pv_${hook}_${t}.jpg`), type: 'jpeg', quality: 85 });
  }
} else {
  const per = Math.ceil(total / W);
  const segs = await Promise.all([...Array(W)].map(async (_, w) => {
    const a = w * per, b = Math.min(total, a + per), seg = path.join(build, `pseg_${hook}_${w}.mp4`);
    const p = await page();
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', seg], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = a; i < b; i++) {
      await p.evaluate(t => window.render(t), i / fps);
      const buf = await p.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); return seg;
  }));
  const list = path.join(build, `psegs_${hook}.txt`);
  fs.writeFileSync(list, segs.map(s => `file '${s}'`).join('\n'));
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', path.join(build, `paper_video_${hook}.mp4`)]);
  console.log('video ->', path.join(build, `paper_video_${hook}.mp4`));
}
await browser.close();
```

---
## Source: `storyboards/paper-data/shoot.mjs`
```javascript
// Renders storyboard.html -> storyboard.jpg (grid) + frames/frame_XX.png
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const { chromium } = createRequire(import.meta.url)('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 3284, height: 1960 }, deviceScaleFactor: 1 });
await p.goto(pathToFileURL(path.join(here, 'storyboard.html')).href);
await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: path.join(here, 'storyboard.jpg'), type: 'jpeg', quality: 92, fullPage: true });
fs.mkdirSync(path.join(here, 'frames'), { recursive: true });
const fr = await p.$$('.fr');
for (let i = 0; i < fr.length; i++) await fr[i].screenshot({ path: path.join(here, 'frames', `frame_${String(i + 1).padStart(2, '0')}.png`) });
await b.close();
console.log('frames', fr.length);
```

---
## Source: `sfx.py`
```python
"""ElevenLabs sound effects. Usage: python3 sfx.py outdir"""
import json,subprocess,sys
out=sys.argv[1]
fx={"whoosh":("fast clean cinematic whoosh transition, airy, premium",1.2),
    "pop":("soft subtle iphone message received pop, clean, short",0.6),
    "boom":("deep luxury cinematic sub bass boom impact with long tail, trailer hit",3.0),
    "riser":("smooth cinematic tension riser building up, airy shimmer",3.0),
    "ding":("elegant crystal bell chime, success notification, luxury",1.5),
    "click":("crisp mechanical keyboard click, single, clean",0.5)}
for k,(t,d) in fx.items():
    subprocess.run(["curl","-sS","-X","POST","https://api.elevenlabs.io/v1/sound-generation","-H","xi-api-key: proxy-injected",
      "-H","Content-Type: application/json","-d",json.dumps({"text":t,"duration_seconds":d,"prompt_influence":0.6}),"-o",f"{out}/{k}.mp3"],check=True)
    print(k, subprocess.run(["file","-b",f"{out}/{k}.mp3"],capture_output=True,text=True).stdout.strip()[:40])
```
