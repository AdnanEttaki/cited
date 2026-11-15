---
videomd: 1
part: remake
tokens: 12486
---

## Remake plan

### Step by step

This is a motion-graphics explainer. Every number in the steps below was measured on the original; follow them and check yours against it.

1. **Write the content**: one picture of your own for each of the 21 shots in the shot list
2. **Collect material**: the real material in the picture (screen recording, UI screenshot) needs the original files, listed under “What to prepare”
3. **Voice**: the original is to confirm
4. **Motion graphics**: `rea-video code-remake <report dir>` writes an editable project and a first cut from the measured layout and motion; change the text and data and rerun; elements and timing per scene under “Code build” below
5. **Subtitles and styled text**: the subtitle timing is saved as `packaging/subtitles.srt` (standard SRT), which any editor that imports SRT can use; replace the words; the other styled text and stickers, with timing and style, under “Packaging layer”
6. **Sound effects**: 15, with the time and the picture event each one hits under “Sound”; each can be played first
7. **Put it together and compare**: hand the shots you made to the agent; `rea-video remake` places them on the original timeline, keeps the original where yours are missing, and renders a side-by-side comparison with the original

**1 3D render shot → 1 generation unit, 1 Seedance 2.0 call; code render / screen capture 20 shots → 1 code project**

- Grouping: AI shots in the same scene joined by hard cuts are generated in one call; ≤15s per call; consecutive hard cuts inside a unit preferably ≤8s, at most 10s; split at dissolves / fades and scene changes
- Audio: the model can generate action sound effects and ambience along with the picture; the voice was recorded by a person: record it separately and mix it in rather than having the video model speak, so copy and timing stay editable
- Packaging: the subtitle, styled text, text label on the generated shots is post-production packaging: keep it out of the prompts, erase it from reference frames, and lay it back on from the packaging timeline after generation
- The prompts below are written generically; before generating with Seedance 2.0, rewrite them the way it expects (timing and shots, how references are addressed, dialogue, exclusions): `rea-video models seedance-2.0`

A video model can take these inputs; each generation unit below lists which ones to feed and where they come from:
- **Text prompt**: always; describes the picture, action and camera
- **First frame**: locks the composition and subject of frame one. Without it this is plain text-to-video and framing changes every time
- **Last frame**: also locks the final frame so the model only fills in between. Suits a single shot with a camera move or action
- **Reference images**: how the product and people look, so they stay the same across shots (`@图片1` in the prompt)
- **Reference video**: copy the action, camera move and rhythm, not the picture (`@视频1`); not every model takes one

### Generation units

One generation per unit. The table lists what to feed the model; open a unit for where each input comes from and the prompt.

| Unit | Shots | Time | Duration | Mode | Feed | Continuity |
|---|---|---|---|---|---|---|
| G1 | #1 | 0.0–4.5s | 4.5s | single shot | first frame + last frame | — |

**G1 · shots #1 · 4.5s · first + last frame to video**

| Input | Needed | From | Why |
|---|---|---|---|
| text prompt | yes | see the prompt below | describes picture, action and camera; every other input only constrains it |
| first frame | yes | source frame `shots/shot_001_first.jpg` (to change product, person or style, redraw it with an image model from the first-frame prompt below) | locks composition, shot size and subject position; with text alone every generation frames it differently |
| last frame | worth it | source frame `shots/shot_001_last.jpg`, treated like the first frame | the shot moves; pinning the end frame leaves the model only the in-between, so motion and the final framing stay close to the source |
| reference video | no | — | this unit locks framing with first / last frames; the model takes no reference video alongside them, so put action and camera move in the prompt |

- Alternative: a 3D project. Have an LLM write a Blender script or a Three.js scene; model the characters / props once and render each shot from its own camera. Best for multiple angles and character consistency, and changing copy or shots is just a code change
- Shots #1 have no prompt

```text
Vertical 9:16; high key (bright overall, almost no shadows), soft light (almost no lit / shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode).
(prompt missing: run --vlm or have the agent write one from the frames)
```

### Code composition

One Remotion / HTML project rebuilt from the text tracks and layout (text and UI are 100% controllable; changing copy is a data change). An LLM can write this project directly.

Start with `rea-video code-remake <breakdown folder>`: it writes `code/spec.json` + `code/render.py` from each scene's sampled points / cut-out, motion and background glow below, matches each scene's amount and brightness to the original, renders `code/remake.mp4` and scores it. Work from that version (edit spec.json, swap the points, or port it to Remotion) instead of writing one from scratch.

- Part 1: shots #2–#21 (4.5–71.6s)

Remake assets (all in the report folder; hand them over together with the data below to whoever writes the code, or to an LLM):
- `shots/shot_XXX_first.jpg` / `_last.jpg`: first / last frame of each shot at full size, for layout, type size and margins
- `shots/shot_XXX_strip.jpg`: key frames about every 0.5 s, to follow the animation
- `shots/shot_XXX_elements.jpg` and `_el_NN.jpg` / `_st_NN.jpg` / `_ly_NN.jpg`: full-size crop of every element once settled, numbered as in the motion timeline; redraw shapes from them, cut out icons, logos and illustrations that cannot be redrawn
- `packaging/overlays.ass`, `packaging/timeline.json`: timing, position and colour of the text

How to build the pictures (by the measured picture type):
- kinetic type: Word-by-word spring() entrances (offset + scale + opacity), highlight boxes on key words; match font, size and leading from the frame
- data chart: SVG / D3 scales for axes and marks, numbers counted up with interpolate(), bars / lines grown with spring()
- line art / dots: SVG paths drawn on with stroke-dashoffset, or Canvas flow lines from a noise field / dots placed on a target shape; match stroke width, colour and density from the frame

| Shot | Time | Build | Picture | Camera | Colours | On-screen text |
|---|---|---|---|---|---|---|
| #2 | 4.5–6.2s | kinetic type | (to fill from the images: what the elements form and how they move) | static | ground #f9f8f6 · #131210 #e7e2df #cac6c3 #a6a4a4 · drawn #161512 #b7a9a7 #6b6764 #da7f62 | your_account / 米 |
| #3 | 6.2–8.0s | kinetic type | (to fill from the images: what the elements form and how they move) | static | ground #faf9f7 · #dfdedd #171715 #c3bfbc #a6a6a6 · drawn #151412 #c2a89e #817e7d #474341 | $0 / FREE / 米 |
| #4 | 8.0–11.6s | data chart | (to fill from the images: what the elements form and how they move) | static | ground #f8f7f5 · #fcfdff #c9c6c4 #e1e1e1 #a6a3a1 · drawn #c0bbbb #262424 #a29794 #6c6968 | github.com/.../instagram-agent-skill |
| #5 | 11.6–18.9s | line art / dots | (to fill from the images: what the elements form and how they move) | static | ground #f8f7f5 · #fcfdff #dbdad8 #a5a2a0 #797777 · drawn #161413 #b5adaa #7d7978 #484646 | /ig-audit / 米 / ONE SKILL? / 13 / SKILLS |
| #6 | 18.9–22.4s | line art / dots | (to fill from the images: what the elements form and how they move) | static | ground #f9f8f6 · #c3c0c1 #e0e0de #a7a4a2 #d77a55 · drawn #241f1e #75706e #b1adaa #df7d56 | 米 / REEL DRAFT |
| #7 | 22.4–25.0s | line art / dots | (to fill from the images: what the elements form and how they move) | static | ground #f8f7f5 · #fcfdff #e0dddb #9f9f9f #c6beba · drawn #211e1e #6c6865 #aca6a3 #df7f58 | EXAMPLE FROM THE REPO / 米 / HOOK |
| #8 | 25.0–28.3s | kinetic type | (to fill from the images: what the elements form and how they move) | static | ground #f9f8f6 · #e5e0db #de7b52 #bfbbb8 #a19b98 · drawn #e07f59 #29201d #71655f #b2aca8 | /ig-comment / 米 / 9 COMMENT TYPES |
| #9 | 28.3–30.9s | kinetic type | (to fill from the images: what the elements form and how they move) | static | ground #faf9f7 · #dd7c54 #e8e3e0 #d4cfcc #bfb4af · drawn #e07d55 #2a2321 #716764 #b5ada9 | /ig-reply / DRAFT REPLY / 米 / YOUR POST |
| #10 | 30.9–33.6s | line art / dots | (to fill from the images: what the elements form and how they move) | static | ground #f9f9f9 · #e1ddda #b6b2b1 #d67b56 #807d7c · drawn #24201f #6d6663 #b0aaa7 #dd7d57 | 米 / 22 / 38 |
| #11 | 33.6–35.7s | data chart | (to fill from the images: what the elements form and how they move) | static | ground #f9f8f6 · #e17d54 #e3dfdc #a8a19d #c8c1be · drawn #e07e56 #27211e #6f5b53 #ada7a4 | + 20 MIN ENGAGING, DAILY / WHO / 米 / THURSDAY |
| #12 | 35.7–38.9s | line art / dots | (to fill from the images: what the elements form and how they move) | static | ground #f8f7f5 · #fcfdff #e1ddda #b2afb0 #827c7c · drawn #222020 #726f6e #aeaaa9 #d67d5a | WHO / 5 REACH 3 PEERS 2 BUYERS / 米 / THURSDAY |
| #13 | 38.9–41.0s | kinetic type | (to fill from the images: what the elements form and how they move) | static | ground #f8f7f5 · #12110f #dfddda #bcb5b1 #5e5d5c · drawn #141310 #b6a8a1 #807c78 #403e3b | 米 |
| #14 | 41.0–45.7s | kinetic type | (to fill from the images: what the elements form and how they move) | static | ground #f8f7f5 · #9b9a98 #dfdedd #bfbcbb #df7c55 · drawn #fbf8f7 #171512 #a8968f #5b5856 | Q / 米 |
| #15 | 45.7–47.6s | line art / dots | (to fill from the images: what the elements form and how they move) | static | ground #f9f8f6 · #e4e0dd #c9c5c2 #aba7a4 #c67758 · drawn #251f1d #6c615e #aaa39f #d77e5c | YOU PICK 6–12 ACCOUNTS / ILLUSTRATIVE / VIEWS ÷ THAT ACCOUNT'S MEDIAN / 米 |
| #16 | 47.6–51.0s | data chart | (to fill from the images: what the elements form and how they move) | static | ground #f8f7f5 · #fcfdff #dfdcda #dd7c54 #c8c1be · drawn #e07d55 #24201e #695e5a #a6a09d | 7.4× / ILLUSTRATIVE VALUES / 米 / VIEWS ÷ THAT ACCOUNT'S MEDIAN |
| #17 | 51.0–53.0s | data chart | (to fill from the images: what the elements form and how they move) | static | ground #f9f8f6 · #dcdbd9 #bab7b5 #979493 #1d1b1c · drawn #201d1c #716d6c #aea6a2 #da7c57 | ABOUT HALF OF REAL HOOKS MATCH A FORMULA / TOP REELS· NAMED HOOK / TOP REELS·NAMED HOOK |
| #18 | 53.0–57.7s | line art / dots | (to fill from the images: what the elements form and how they move) | static | ground #f9f9f9 · #b8b4b3 #dcdbd9 #706462 #969696 · drawn #1b1818 #967b71 #494442 #bab2ae | 1,000 followers are." / 米 / @niche_02 / 7.4× |
| #19 | 57.7–62.3s | data chart | (to fill from the images: what the elements form and how they move) | static | ground #f9f8f6 · #e6e1de #a8a8a8 #c3bfbe #191917 · drawn #1b1816 #a29e9b #de805a #5e5754 | YOUR VERSION READY / 米 / SWIPE FILE / O HOURS / OHOURS |
| #20 | 62.3–67.4s | line art / dots | (to fill from the images: what the elements form and how they move) | static | ground #f9f8f6 · #c6c1be #dedddb #1c1b1a #a4a3a1 · drawn #231f1f #6f6b6a #aaa5a3 #dd7e59 | OPEN CLAUDE / instagram-agent-skill / /ig-reel works. / 米 |
| #21 | 67.4–71.6s | kinetic type | (to fill from the images: what the elements form and how they move) | static | ground #f8f7f5 · #fcfdff #d57b58 #c9bfbb #e8e0dc · drawn #d97a56 #1c1a19 #79706d #b9b1ad | INSTAGRAM AGENT SKILL |

**Picture scenes** (a new scene whenever what is drawn moves or changes shape as a whole inside a shot. `frames/` holds first / middle / last full-size frames per scene, `scene_XX_layer.png` the drawn layer of the middle frame (background and text removed, alpha by how strongly it stands out), `frames/points/scene_XX.json` samples of that layer, one `x y r g b a` per row with x, y in 0–1. Place particles, trace lines or redraw shapes from these instead of guessing from a description. `track` in `frames/scenes.json` follows the layer's centre and spread over time)

| Scene | Shot | Time | Ground | Background glow | Drawn colours | Pieces | Area (x0 y0 x1 y1) | Motion |
|---|---|---|---|---|---|---|---|---|
| scene_01 | #2 | 4.5–6.2s | #f9f8f4 | #3a3a36, centre (0.67, 0.41), radius 0.30 | #141511 #ac8882 #555452 | 71 | 0.11 0.12 0.95 0.78 | near still |
| scene_02 | #3 | 6.2–8.0s | #f9f8f4 | #838381, centre (0.51, 0.33), radius 0.17 | #949390 #171615 #555351 | 33 | 0.06 0.00 0.95 1.00 | near still |
| scene_03 | #4 | 8.0–9.5s | #f9f8f4 | #dbdad8, centre (0.55, 0.46), radius 0.43 | #171716 #969592 #5a5957 | 32 | 0.05 0.00 0.95 1.00 | near still |
| scene_04 | #4 | 9.5–11.6s | #f9f8f4 | #d8d8d5, centre (0.54, 0.45), radius 0.39 | #857a76 #1f1e1c #b1b0af | 420 | 0.06 0.12 0.95 0.80 | morphs in from the last scene |
| scene_05 | #5 | 11.6–14.1s | #f9f8f4 | #50514d, centre (0.56, 0.46), radius 0.26 | #151612 #92918d #575653 | 84 | 0.05 0.00 0.92 1.00 | near still |
| scene_06 | #5 | 14.1–18.9s | #f9f8f4 | #bfbeba, centre (0.48, 0.45), radius 0.39 | #1c1b1a #a5a4a0 #656461 | 354 | 0.05 0.00 0.95 1.00 | morphs in from the last scene |
| scene_07 | #6 | 18.9–22.4s | #f9f8f4 | #d1a495, centre (0.25, 0.28), radius 0.20 | #181716 #a68f86 #585351 | 180 | 0.06 0.00 0.95 1.00 | near still |
| scene_08 | #7 | 22.4–25.0s | #f9f8f4 | #aba9a9, centre (0.47, 0.50), radius 0.21 | #21201f #d8785a #8d8c89 | 39 | 0.06 0.12 0.95 0.80 | near still |
| scene_09 | #8 | 25.0–28.3s | #f9f8f4 | #cd9a89, centre (0.47, 0.55), radius 0.32 | #211e1b #d77556 #8a8683 | 37 | 0.07 0.00 0.95 1.00 | near still |
| scene_10 | #9 | 28.3–30.9s | #f9f8f4 | #d0a392, centre (0.57, 0.46), radius 0.43 | #d87757 #27211e #898582 | 40 | 0.06 0.12 0.95 0.80 | near still |
| scene_11 | #10 | 30.9–33.6s | #f9f8f4 | #cea292, centre (0.42, 0.51), radius 0.23 | #8a8986 #201f1d #d67657 | 51 | 0.05 0.00 0.96 1.00 | near still |
| scene_12 | #11 | 33.6–35.7s | #f9f8f4 | #d08b74, centre (0.44, 0.43), radius 0.41 | #d67556 #221e1b #8c8986 | 110 | 0.06 0.12 0.95 0.80 | near still |
| scene_13 | #12 | 35.7–38.9s | #f9f8f4 | #d8d4d1, centre (0.43, 0.34), radius 0.42 | #171715 #a49690 #5d5754 | 331 | 0.05 0.00 0.95 1.00 | near still |
| scene_14 | #13 | 38.9–41.0s | #f9f8f4 | #63635e, centre (0.43, 0.55), radius 0.32 | #141410 #91908c #5a5956 | 70 | 0.06 0.00 0.94 1.00 | near still |
| scene_15 | #14 | 41.0–43.0s | #f9f8f4 | #4f4f4a, centre (0.63, 0.40), radius 0.28 | #151511 #908f8c #5b5a58 | 65 | 0.14 0.00 0.95 1.00 | near still |
| scene_16 | #14 | 43.0–45.7s | #9e9c9a | #f9f8f4, centre (0.51, 0.52), radius 0.70 | #f9f9f6 #141411 | 182 | 0.01 0.12 0.94 0.80 | morphs in from the last scene, pans (-0.7%, +0.2%)/s |
| scene_17 | #15 | 45.7–47.6s | #f9f8f4 | #c7b3ab, centre (0.47, 0.36), radius 0.46 | #191614 #a99086 #5d5451 | 82 | 0.05 0.12 0.95 0.80 | near still |
| scene_18 | #16 | 47.6–51.0s | #f9f8f4 | #ce8770, centre (0.32, 0.51), radius 0.22 | #1f1c1a #d67658 #93908d | 41 | 0.05 0.12 0.95 0.80 | near still |
| scene_19 | #17 | 51.0–53.0s | #f9f8f4 | #a18c85, centre (0.25, 0.39), radius 0.32 | #1d1c19 #858381 #d47557 | 56 | 0.06 0.00 0.95 1.00 | near still |
| scene_20 | #18 | 53.0–57.7s | #f9f8f4 | #c4c3c2, centre (0.28, 0.36), radius 0.31 | #161514 #9a9390 #595755 | 45 | 0.05 0.00 0.95 1.00 | near still |
| scene_21 | #19 | 57.7–62.3s | #f9f8f4 | #9b9893, centre (0.36, 0.34), radius 0.25 | #1a1916 #949390 #d37556 | 223 | 0.04 0.12 0.95 0.80 | near still |
| scene_22 | #20 | 62.3–67.4s | #f9f8f4 | #d8bfb6, centre (0.31, 0.41), radius 0.44 | #21201e #898784 #d7795b | 62 | 0.06 0.12 0.94 0.80 | near still |
| scene_23 | #21 | 67.4–71.6s | #f9f8f4 | #e0a38f, centre (0.52, 0.24), radius 0.24 | #d17557 #1d1b19 #96928f | 223 | 0.09 0.12 0.93 0.80 | near still |

When built, score it with `rea-video compare original remake --scenes frames/scenes.json -o dir` (each side's drawn layer is taken against its own ground, so a new ground colour still compares) and fix the lowest-scoring scenes first, from `compare_worst.jpg`.

Per-shot motion timeline (measured: positions in % of frame width / height, colours sampled once the element settles; read together with the key-frame strip)

**Motion #2 4.5–6.2s (wipe in) · 5 events**

- Ground #f9f8f6; other main colours #131210 #e7e2df #cac6c3 #a6a4a4; drawn layer #161512 #b7a9a7 #6b6764 #da7f62
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_002_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #9f9e9d · [crop](shots/shot_002_st_02.jpg)
- S3. never moves: shape / text block · x 5%–30%, y 18%–42% · #1d1a19 · [crop](shots/shot_002_st_03.jpg)
- S4. never moves: shape / text block · x 36%–96%, y 18%–71% · #666465 · text “your_account / DRAFTED, NOT POSTED / ILLUSTRATIVE” · [crop](shots/shot_002_st_04.jpg)
- S5. never moves: shape / text block · x 39%–72%, y 19%–24% · #cd5a6a · text “your_account” · [crop](shots/shot_002_st_05.jpg)
- S6. never moves: shape / text block · x 39%–92%, y 26%–45% · #12110e · [crop](shots/shot_002_st_06.jpg)
- S7. never moves: shape / text block · x 5%–35%, y 62%–69% · #4a4136 · text “IT DRAFTS. / YOU POST.” · [crop](shots/shot_002_st_07.jpg)
- S8. never moves: horizontal line · x 0%–100%, y 99%–100% · #d2d0cc · [crop](shots/shot_002_st_08.jpg)
- [crop L1](shots/shot_002_ly_01.jpg) [crop L2](shots/shot_002_ly_02.jpg) · Continuous layer: 6% of the frame moves through the whole shot (x 9%–91%, y 46%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 4.57–5.03s · middle (x 40%–93%, y 36%–56%) · changes, unfolds downward (draw-on / grow / wipe), linear · #12110e · [crop](shots/shot_002_el_01.jpg)
2. 4.57–4.63s · middle left (x 13%–22%, y 42%–48%) · disappears, instant · #be7a56 · [crop](shots/shot_002_el_02.jpg)
3. 4.57–4.83s · middle left (x 13%–22%, y 50%–62%) · changes, moves downward, ease-in-out · #faf7f4 · text “IT DRAFTS.” · [crop](shots/shot_002_el_03.jpg)
4. 5.57–5.83s · top left (x 7%–27%, y 19%–30%) · changes, ease-in-out · #fffdfe · [crop](shots/shot_002_el_04.jpg)
5. 6.17–6.23s · bottom (x 16%–84%, y 78%–80%) · changes, instant · #393636 · text “YOUR ENTIRE INSTAGRAM / CONTENT WITH CLAUDE, / AND IT'S COMPLETELY” · [crop](shots/shot_002_el_05.jpg)

**Motion #3 6.2–8.0s (blur in) · 4 events**

- Ground #faf9f7; other main colours #dfdedd #171715 #c3bfbc #a6a6a6; drawn layer #151412 #c2a89e #817e7d #474341
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_003_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #9f9e9d · [crop](shots/shot_003_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d2d0cc · [crop](shots/shot_003_st_03.jpg)
- [crop L1](shots/shot_003_ly_01.jpg) [crop L2](shots/shot_003_ly_02.jpg) · Continuous layer: 10% of the frame moves through the whole shot (x 7%–93%, y 40%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 6.30–6.70s · middle (x 13%–98%, y 16%–50%) · appears, linear · #9d9b99 · text “$0 / FREE” · [crop](shots/shot_003_el_01.jpg)
2. 6.30–6.37s · bottom (x 20%–82%, y 80%–81%) · disappears, instant · #b8b5b4 · [crop](shots/shot_003_el_02.jpg)
3. 6.50–6.77s · middle (x 4%–96%, y 52%–71%) · appears, slides leftward, linear · #868383 · text “The 13 skills / FREE·MIT / Claude Code” · [crop](shots/shot_003_el_03.jpg)
4. 7.57–7.70s · middle right (x 60%–98%, y 39%–50%) · changes, moves rightward, instant · #c17b56 · text “FREE” · [crop](shots/shot_003_el_04.jpg)

**Motion #4 8.0–11.6s · 3 events**

- Ground #f8f7f5; other main colours #fcfdff #c9c6c4 #e1e1e1 #a6a3a1; drawn layer #c0bbbb #262424 #a29794 #6c6968
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_004_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #a09e9d · [crop](shots/shot_004_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d1cfcb · [crop](shots/shot_004_st_03.jpg)
- [crop L1](shots/shot_004_ly_01.jpg) [crop L2](shots/shot_004_ly_02.jpg) · Continuous layer: 13% of the frame moves through the whole shot (x 11%–89%, y 25%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 8.07–8.47s · middle (x 4%–96%, y 18%–71%) · appears, slides downward, ease-out · #c7c4c4 · text “github.com/.../instagram-agent-skill / Jakeschincariol and claude Restore sentence capitals ...d03c56b· last month / 2 Commits” · [crop](shots/shot_004_el_01.jpg)
2. 8.87–10.00s · middle (x 9%–91%, y 21%–67%) · changes, moves rightward, linear · #eceaec · text “github.com/.../instagram-agent-skill / Jakeschincariol and claude Restore sentence capitals ...d03c56b· last month / 2 Commits” · [crop](shots/shot_004_el_02.jpg)
3. 8.87–9.60s · middle (x 22%–87%, y 61%–62%) · disappears, moves leftward, linear · #c7c4c3 · text “waste a take on it. One goes and finds the reels that are actually working in your / niche and ranks them by how far each beat its own account. One writes the caption / and shows you exactly what the feed shows before the "... more". One scores your” · [crop](shots/shot_004_el_03.jpg)

**Motion #5 11.6–18.9s (wipe in) · 2 events**

- Ground #f8f7f5; other main colours #fcfdff #dbdad8 #a5a2a0 #797777; drawn layer #161413 #b5adaa #7d7978 #484646
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_005_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #a09e9f · [crop](shots/shot_005_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d1cfcb · [crop](shots/shot_005_st_03.jpg)
- [crop L1](shots/shot_005_ly_01.jpg) [crop L2](shots/shot_005_ly_02.jpg) · Continuous layer: 19% of the frame moves through the whole shot (x 7%–91%, y 30%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 13.53–15.07s · middle (x 11%–91%, y 16%–70%) · changes, moves downward, ease-in-out · #e3e1e1 · text “ONE SKILL? / lig-reel / 13” · [crop](shots/shot_005_el_01.jpg)
2. 17.80–18.07s · middle (x 4%–98%, y 25%–72%) · changes, moves rightward, ease-in-out · #979495 · text “lig-reel / CLAUDE / /ig-reel” · [crop](shots/shot_005_el_02.jpg)

**Motion #6 18.9–22.4s (blur in) · 4 events**

- Ground #f9f8f6; other main colours #c3c0c1 #e0e0de #a7a4a2 #d77a55; drawn layer #241f1e #75706e #b1adaa #df7d56
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2d1 · [crop](shots/shot_006_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #a09d9d · [crop](shots/shot_006_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d2d0cc · [crop](shots/shot_006_st_03.jpg)
- [crop L1](shots/shot_006_ly_01.jpg) [crop L2](shots/shot_006_ly_02.jpg) · Continuous layer: 3% of the frame moves through the whole shot (x 9%–91%, y 25%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 18.93–19.40s · middle (x 0%–96%, y 18%–71%) · appears, slides downward, linear · #ca857f · text “/ig-reel / 26 / HOOK FORMULAS” · [crop](shots/shot_006_el_01.jpg)
2. 20.13–20.60s · top (x 4%–96%, y 18%–48%) · changes, moves downward, ease-out · #c5c0be · text “/ig-reel / REEL DRAFT / HOOK” · [crop](shots/shot_006_el_02.jpg)
3. 21.33–21.53s · bottom (x 24%–76%, y 78%–81%) · changes, linear · #f4e7e0 · text “THE FIRST ONE WRITES / YOUR REELS USING 26” · [crop](shots/shot_006_el_03.jpg)
4. 21.40–22.27s · middle (x 7%–93%, y 25%–69%) · changes, moves rightward, linear · #a98688 · text “/ig-reel / 26 / HOOK FORMULAS” · [crop](shots/shot_006_el_04.jpg)

**Motion #7 22.4–25.0s · 2 events**

- Ground #f8f7f5; other main colours #fcfdff #e0dddb #9f9f9f #c6beba; drawn layer #211e1e #6c6865 #aca6a3 #df7f58
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2d1 · [crop](shots/shot_007_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #a09d9d · [crop](shots/shot_007_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d2d0cc · [crop](shots/shot_007_st_03.jpg)
- [crop L1](shots/shot_007_ly_01.jpg) [crop L2](shots/shot_007_ly_02.jpg) · Continuous layer: 7% of the frame moves through the whole shot (x 4%–89%, y 46%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 22.47–23.33s · middle (x 4%–96%, y 18%–66%) · appears, slides downward, ease-out · #b98a82 · text “HOOK / "Nobody tells you that your first 30 / reels are supposed to f..."” · [crop](shots/shot_007_el_01.jpg)
2. 22.60–22.73s · middle right (x 73%–80%, y 54%–58%) · appears, instant · #f2f0f0 · text “100” · [crop](shots/shot_007_el_02.jpg)

**Motion #8 25.0–28.3s (blur in) · 3 events**

- Ground #f9f8f6; other main colours #e5e0db #de7b52 #bfbbb8 #a19b98; drawn layer #e07f59 #29201d #71655f #b2aca8
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_008_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #9e918f · [crop](shots/shot_008_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d2d0cc · [crop](shots/shot_008_st_03.jpg)
- Continuous layer: 3% of the frame moves through the whole shot (x 16%–84%, y 64%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 25.07–25.33s · top left (x 4%–36%, y 18%–28%) · appears, slides rightward, ease-out · #e27d53 · text “/ig-comment” · [crop](shots/shot_008_el_01.jpg)
2. 25.13–25.93s · middle (x 13%–96%, y 29%–71%) · appears, unfolds downward (draw-on / grow / wipe), linear · #e8e1db · text “@another_creator / ADD A COMMENT... / ILLUSTRATIVE” · [crop](shots/shot_008_el_02.jpg)
3. 25.47–25.73s · top (x 38%–78%, y 20%–24%) · appears, slides rightward, ease-out · #c0bdba · text “9 COMMENT TYPES” · [crop](shots/shot_008_el_03.jpg)

**Motion #9 28.3–30.9s · 3 events**

- Ground #faf9f7; other main colours #dd7c54 #e8e3e0 #d4cfcc #bfb4af; drawn layer #e07d55 #2a2321 #716764 #b5ada9
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_009_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #7b7958 · [crop](shots/shot_009_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d2d0cc · [crop](shots/shot_009_st_03.jpg)
- [crop L1](shots/shot_009_ly_01.jpg) [crop L2](shots/shot_009_ly_02.jpg) · Continuous layer: 9% of the frame moves through the whole shot (x 18%–93%, y 40%–79%), e.g. drifting gradients, particle flow, breathing glow
1. 28.33–29.20s · middle (x 4%–100%, y 18%–71%) · appears, unfolds downward (draw-on / grow / wipe), ease-out · #e18985 · text “YOUR POST / /ig-reply / COMMENTS” · [crop](shots/shot_009_el_01.jpg)
2. 28.33–28.40s · bottom (x 16%–84%, y 80%–81%) · disappears, instant · #ccc9c6 · [crop](shots/shot_009_el_02.jpg)
3. 29.47–29.80s · bottom (x 13%–87%, y 74%–80%) · changes, moves leftward, ease-in · #dea393 · text “ONE DRAFTS REPLIES TO / YOUR OWN COMMENTS.” · [crop](shots/shot_009_el_03.jpg)

**Motion #10 30.9–33.6s · 2 events**

- Ground #f9f9f9; other main colours #e1ddda #b6b2b1 #d67b56 #807d7c; drawn layer #24201f #6d6663 #b0aaa7 #dd7d57
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_010_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #646153 · [crop](shots/shot_010_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d2d0cc · [crop](shots/shot_010_st_03.jpg)
- Continuous layer: 3% of the frame moves through the whole shot (x 16%–84%, y 74%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 30.97–31.43s · middle (x 4%–98%, y 15%–74%) · appears, slides rightward, ease-out · #ddbfbd · text “22 / your_account / / 100” · [crop](shots/shot_010_el_01.jpg)
2. 32.70–33.57s · middle (x 9%–82%, y 38%–75%) · changes, unfolds downward (draw-on / grow / wipe), ease-in · #d37c55 · text “NAME FIELD / Sam· coffee lover / BIO, LINE ONE” · [crop](shots/shot_010_el_02.jpg)

**Motion #11 33.6–35.7s · 2 events**

- Ground #f9f8f6; other main colours #e17d54 #e3dfdc #a8a19d #c8c1be; drawn layer #e07e56 #27211e #6f5b53 #ada7a4
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_011_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #494847 · [crop](shots/shot_011_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d2d0cc · [crop](shots/shot_011_st_03.jpg)
- [crop L1](shots/shot_011_ly_01.jpg) [crop L2](shots/shot_011_ly_02.jpg) · Continuous layer: 22% of the frame moves through the whole shot (x 7%–84%, y 24%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 33.70–33.97s · middle (x 4%–96%, y 16%–71%) · appears, slides leftward, linear · #e4e0db · text “/ig-plan / YOUR WEEK · 5 POSTS, 3 REELS / MON” · [crop](shots/shot_011_el_01.jpg)
2. 34.23–34.83s · middle (x 7%–80%, y 30%–64%) · appears, unfolds rightward (draw-on / grow / wipe), ease-in-out · #e37d53 · text “MON / TUE / WED” · [crop](shots/shot_011_el_02.jpg)

**Motion #12 35.7–38.9s · 4 events**

- Ground #f8f7f5; other main colours #fcfdff #e1ddda #b2afb0 #827c7c; drawn layer #222020 #726f6e #aeaaa9 #d67d5a
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_012_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #494847 · [crop](shots/shot_012_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d2d0cc · [crop](shots/shot_012_st_03.jpg)
- [crop L1](shots/shot_012_ly_01.jpg) [crop L2](shots/shot_012_ly_02.jpg) · Continuous layer: 5% of the frame moves through the whole shot (x 9%–91%, y 55%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 35.77–35.97s · middle (x 4%–96%, y 18%–71%) · appears, slides upward, linear · #e7e1db · text “THURSDAY / WHAT / REEL” · [crop](shots/shot_012_el_01.jpg)
2. 36.63–36.83s · middle (x 7%–93%, y 40%–56%) · appears, slides rightward, linear · #6e6c66 · text “WHEN / TIME / EARLY EVENING” · [crop](shots/shot_012_el_02.jpg)
3. 37.57–37.77s · middle (x 7%–93%, y 55%–71%) · changes, moves leftward, ease-in-out · #83786f · text “WHO / 5 REACH 3 PEERS 2 BUYERS” · [crop](shots/shot_012_el_03.jpg)
4. 37.77–38.03s · bottom (x 22%–78%, y 74%–81%) · changes, moves leftward, ease-in-out · #eecfc9 · text “WHAT TO POST, WHEN TO / POST, AND WHO TO / ENGAGE WITH.” · [crop](shots/shot_012_el_04.jpg)

**Motion #13 38.9–41.0s (wipe in) · 2 events**

- Ground #f8f7f5; other main colours #12110f #dfddda #bcb5b1 #5e5d5c; drawn layer #141310 #b6a8a1 #807c78 #403e3b
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_013_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #484745 · [crop](shots/shot_013_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d1cfcb · [crop](shots/shot_013_st_03.jpg)
- [crop L1](shots/shot_013_ly_01.jpg) [crop L2](shots/shot_013_ly_02.jpg) · Continuous layer: 11% of the frame moves through the whole shot (x 13%–87%, y 20%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 38.97–39.23s · middle (x 4%–96%, y 46%–56%) · appears, slides rightward, linear · #13120f · text “/ig-reel / /ig-comment / /ig-reply” · [crop](shots/shot_013_el_01.jpg)
2. 39.17–39.37s · middle (x 4%–96%, y 57%–66%) · appears, slides rightward, linear · #13120f · text “/ig-profile / /ig-plan / one more” · [crop](shots/shot_013_el_02.jpg)

**Motion #14 41.0–45.7s · 4 events**

- Ground #f8f7f5; other main colours #9b9a98 #dfdedd #bfbcbb #df7c55; drawn layer #fbf8f7 #171512 #a8968f #5b5856
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: shape / text block · x 0%–100%, y 0%–24% · #faf7f4 · [crop](shots/shot_014_st_01.jpg)
- S2. never moves: shape / text block · x 0%–100%, y 68%–100% · #faf7f4 · text “BUT THEN, THERE'S THE / /ig-audit” · [crop](shots/shot_014_st_02.jpg)
- [crop L1](shots/shot_014_ly_01.jpg) [crop L2](shots/shot_014_ly_02.jpg) · Continuous layer: 19% of the frame moves through the whole shot (x 11%–100%, y 24%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 42.10–43.83s · middle (x 0%–100%, y 19%–68%) · changes, moves leftward, linear · #9e9c9a · text “/ig-reel / /ig-viral / /ig-caption” · [crop](shots/shot_014_el_01.jpg)
2. 42.77–43.17s · bottom (x 18%–84%, y 74%–81%) · changes, moves leftward, ease-in · #ebc9bd · text “BUT THEN, THERE'S THE” · [crop](shots/shot_014_el_02.jpg)
3. 44.70–45.03s · middle (x 22%–78%, y 30%–71%) · changes, moves downward, linear · #e27d53 · text “/ig-carousel / /ig-story / /ig-plan” · [crop](shots/shot_014_el_03.jpg)
4. 45.63–45.70s · bottom (x 24%–76%, y 74%–80%) · changes, instant · #b1a69d · text “BUT THEN, THERE'S THE” · [crop](shots/shot_014_el_04.jpg)

**Motion #15 45.7–47.6s · 5 events**

- Ground #f9f8f6; other main colours #e4e0dd #c9c5c2 #aba7a4 #c67758; drawn layer #251f1d #6c615e #aaa39f #d77e5c
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_015_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #4a4948 · [crop](shots/shot_015_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d2d0cc · [crop](shots/shot_015_st_03.jpg)
- [crop L1](shots/shot_015_ly_01.jpg) [crop L2](shots/shot_015_ly_02.jpg) · Continuous layer: 7% of the frame moves through the whole shot (x 4%–96%, y 25%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 45.73–45.93s · top left (x 4%–58%, y 18%–22%) · appears, linear · #c57955 · text “YOU PICK 6–12 ACCOUNTS / VIEWS ÷ THAT ACCOUNT'S MEDIAN” · [crop](shots/shot_015_el_01.jpg)
2. 45.73–47.00s · middle (x 4%–96%, y 25%–59%) · appears, slides downward, ease-out · #dfd8d4 · text “@niche_01 / @niche_02 / @niche_03” · [crop](shots/shot_015_el_02.jpg)
3. 45.80–45.93s · top right (x 73%–96%, y 19%–23%) · appears, instant · #b8b5b2 · text “ILLUSTRATIVE” · [crop](shots/shot_015_el_03.jpg)
4. 45.87–46.07s · middle (x 7%–87%, y 60%–69%) · appears, slides rightward, ease-in-out · #e6e1db · text “@niche_07 / @niche_08 / EACH BAR = ONE REEL” · [crop](shots/shot_015_el_04.jpg)
5. 47.00–47.47s · middle (x 4%–96%, y 60%–71%) · changes, moves rightward, linear · #cd7c56 · text “@niche_07 / @niche_08 / EACH BAR = ONE REEL” · [crop](shots/shot_015_el_05.jpg)

**Motion #16 47.6–51.0s · 4 events**

- Ground #f8f7f5; other main colours #fcfdff #dfdcda #dd7c54 #c8c1be; drawn layer #e07d55 #24201e #695e5a #a6a09d
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_016_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #484745 · [crop](shots/shot_016_st_02.jpg)
- S3. never moves: horizontal line · x 11%–44%, y 61%–63% · #828180 · text “EACH BAR = ONE REEL” · [crop](shots/shot_016_st_03.jpg)
- S4. never moves: horizontal line · x 0%–100%, y 99%–100% · #d2d0cc · [crop](shots/shot_016_st_04.jpg)
- [crop L1](shots/shot_016_ly_01.jpg) [crop L2](shots/shot_016_ly_02.jpg) · Continuous layer: 3% of the frame moves through the whole shot (x 11%–89%, y 46%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 47.67–48.80s · middle (x 4%–96%, y 18%–71%) · appears, slides downward, ease-in-out · #da7d61 · text “VIEWS ÷ THAT ACCOUNT'S MEDIAN / 7.4× / 5.1×” · [crop](shots/shot_016_el_01.jpg)
2. 48.07–48.60s · middle (x 51%–71%, y 35%–44%) · changes, moves leftward, ease-in-out · #9f9d9f · text “5.1×” · [crop](shots/shot_016_el_02.jpg)
3. 49.07–49.27s · middle (x 9%–93%, y 46%–66%) · changes, linear · #e9b9a1 · text “2.2× / 1.4× / 1.1×” · [crop](shots/shot_016_el_03.jpg)
4. 50.93–51.00s · bottom (x 9%–91%, y 74%–80%) · changes, instant · #a6a39f · text “RANKS THE REELS BY HOW / FAR THEY BEAT THEIR / OWN ACCOUNT'S AVERAGE,” · [crop](shots/shot_016_el_04.jpg)

**Motion #17 51.0–53.0s · 2 events**

- Ground #f9f8f6; other main colours #dcdbd9 #bab7b5 #979493 #1d1b1c; drawn layer #201d1c #716d6c #aea6a2 #da7c57
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_017_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #484745 · [crop](shots/shot_017_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d2d0cc · [crop](shots/shot_017_st_03.jpg)
- [crop L1](shots/shot_017_ly_01.jpg) [crop L2](shots/shot_017_ly_02.jpg) · Continuous layer: 8% of the frame moves through the whole shot (x 4%–84%, y 50%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 51.03–51.43s · middle (x 2%–96%, y 18%–68%) · appears, slides leftward, ease-out · #a27c61 · text “TOP REELS· NAMED HOOK / 7.4× / #3 Nobody Tells You” · [crop](shots/shot_017_el_01.jpg)
2. 52.10–52.17s · bottom (x 4%–69%, y 70%–71%) · appears, instant · #afa9a7 · text “ABOUT HALF OF REAL HOOKS MATCH A FORMULA” · [crop](shots/shot_017_el_02.jpg)

**Motion #18 53.0–57.7s (blur in) · 3 events**

- Ground #f9f9f9; other main colours #b8b4b3 #dcdbd9 #706462 #969696; drawn layer #1b1818 #967b71 #494442 #bab2ae
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_018_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–15% · #68655c · [crop](shots/shot_018_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d2d0cc · [crop](shots/shot_018_st_03.jpg)
- Continuous layer: 3% of the frame moves through the whole shot (x 18%–96%, y 66%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 53.03–53.23s · middle (x 4%–96%, y 14%–53%) · changes, linear · #cccac8 · text “@niche_02 / 7.4× / #3 Nobody Tells You” · [crop](shots/shot_018_el_01.jpg)
2. 54.83–55.03s · middle (x 4%–96%, y 45%–71%) · appears, slides downward, linear · #868284 · text “your version / #3 Nobody Tells You / REWRITE” · [crop](shots/shot_018_el_02.jpg)
3. 56.77–56.90s · bottom right (x 56%–96%, y 64%–71%) · changes, instant · #c97b54 · [crop](shots/shot_018_el_03.jpg)

**Motion #19 57.7–62.3s · 4 events**

- Ground #f9f8f6; other main colours #e6e1de #a8a8a8 #c3bfbe #191917; drawn layer #1b1816 #a29e9b #de805a #5e5754
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_019_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #484746 · [crop](shots/shot_019_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d3d1cd · [crop](shots/shot_019_st_03.jpg)
- [crop L1](shots/shot_019_ly_01.jpg) [crop L2](shots/shot_019_ly_02.jpg) · Continuous layer: 12% of the frame moves through the whole shot (x 9%–82%, y 19%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 57.77–58.03s · middle (x 2%–96%, y 18%–71%) · appears, slides rightward, ease-out · #e8e1db · text “SWIPE FILE / O HOURS / IDEA 1” · [crop](shots/shot_019_el_01.jpg)
2. 58.63–59.03s · middle left (x 0%–58%, y 34%–49%) · appears, slides rightward, ease-in · #54463c · text “IDEA 2 / NO MORE / 5.1×” · [crop](shots/shot_019_el_02.jpg)
3. 61.37–62.17s · middle (x 7%–96%, y 18%–71%) · changes, unfolds leftward (draw-on / grow / wipe), ease-out · #e9e1db · text “SWIPE FILE / O HOURS / IDEA 1” · [crop](shots/shot_019_el_03.jpg)
4. 62.23–62.30s · bottom (x 24%–78%, y 74%–80%) · changes, instant · #a9a69f · text “NO MORE SCROLLING FOR / HOURS HUNTING FOR / CONTENT IDEAS.” · [crop](shots/shot_019_el_04.jpg)

**Motion #20 62.3–67.4s · 9 events**

- Ground #f9f8f6; other main colours #c6c1be #dedddb #1c1b1a #a4a3a1; drawn layer #231f1f #6f6b6a #aaa5a3 #dd7e59
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_020_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #151211 · [crop](shots/shot_020_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d3d1cd · [crop](shots/shot_020_st_03.jpg)
- Continuous layer: 2% of the frame moves through the whole shot (x 18%–82%, y 75%–79%), e.g. drifting gradients, particle flow, breathing glow
- In sequence: 3 same-size elements, 1.14s apart, about 0.14s each (items 2, 3, 4 below)
1. 62.33–62.80s · middle (x 4%–93%, y 18%–61%) · appears, slides downward, linear · #bfb8b5 · text “OPEN CLAUDE / PASTE ONE LINK / github.com/Jakeschincariol/” · [crop](shots/shot_020_el_01.jpg)
2. 63.93–64.07s · top (x 4%–96%, y 18%–28%) · changes, instant · #9e7d53 · text “OPEN CLAUDE” · [crop](shots/shot_020_el_02.jpg)
3. 65.07–65.27s · middle (x 4%–96%, y 28%–43%) · changes, moves leftward, ease-in-out · #c87d53 · text “PASTE ONE LINK / github.com/Jakeschincariol/ / instagram-agent-skill” · [crop](shots/shot_020_el_03.jpg)
4. 66.20–66.33s · middle (x 4%–96%, y 42%–59%) · changes, instant · #c77c53 · text “TELLIT / Install this skill, then confirm / /ig-reel works.” · [crop](shots/shot_020_el_04.jpg)
5. 66.40–66.73s · bottom (x 18%–82%, y 74%–81%) · changes, moves leftward, ease-in · #faf7f4 · text “AND THE SETUP IS EASY. / OPEN CLAUDE, PASTE ONE” · [crop](shots/shot_020_el_05.jpg)
6. 66.87–67.13s · middle (x 4%–96%, y 61%–71%) · changes, moves leftward, linear · #161312 · text “WORKS IN CLAUDE CODE / 13 SKILLS, READY TO INSTALL” · [crop](shots/shot_020_el_06.jpg)
7. 66.93–67.07s · top (x 24%–44%, y 12%–15%) · appears, slides rightward, instant · #161311 · [crop](shots/shot_020_el_07.jpg)
8. 67.07–67.27s · top right (x 73%–93%, y 12%–15%) · appears, slides rightward, ease-in-out · #151211 · [crop](shots/shot_020_el_08.jpg)
9. 67.33–67.40s · bottom (x 31%–69%, y 74%–80%) · changes, instant · #4c4948 · text “AND THE SETUP IS EASY. / OPEN CLAUDE, PASTE ONE” · [crop](shots/shot_020_el_09.jpg)

**Motion #21 67.4–71.6s · 7 events**

- Ground #f8f7f5; other main colours #fcfdff #d57b58 #c9bfbb #e8e0dc; drawn layer #d97a56 #1c1a19 #79706d #b9b1ad
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: horizontal line · x 0%–100%, y 0%–1% · #d5d2cf · [crop](shots/shot_021_st_01.jpg)
- S2. never moves: horizontal line · x 5%–96%, y 12%–16% · #131210 · [crop](shots/shot_021_st_02.jpg)
- S3. never moves: horizontal line · x 0%–100%, y 99%–100% · #d3d1cd · [crop](shots/shot_021_st_03.jpg)
- [crop L1](shots/shot_021_ly_01.jpg) [crop L2](shots/shot_021_ly_02.jpg) · Continuous layer: 8% of the frame moves through the whole shot (x 13%–87%, y 20%–80%), e.g. drifting gradients, particle flow, breathing glow
1. 67.47–67.80s · top (x 16%–84%, y 18%–46%) · appears, slides leftward, linear · #d9a297 · text “INSTAGRAM AGENT SKILL” · [crop](shots/shot_021_el_01.jpg)
2. 67.47–67.53s · top (x 44%–56%, y 28%–34%) · appears, instant · #cd704b · [crop](shots/shot_021_el_02.jpg)
3. 67.47–67.53s · bottom (x 18%–82%, y 80%–81%) · disappears, instant · #bdbbb8 · [crop](shots/shot_021_el_03.jpg)
4. 67.53–67.80s · middle (x 4%–96%, y 48%–57%) · appears, slides leftward, ease-in-out · #6f6c6d · text “TYPE“SKILL” / POST / SKILL” · [crop](shots/shot_021_el_04.jpg)
5. 69.73–70.27s · middle (x 16%–93%, y 50%–55%) · changes, unfolds rightward (draw-on / grow / wipe), ease-in-out · #c97d58 · text “TYPE“SKILL” / POST / SKILL” · [crop](shots/shot_021_el_05.jpg)
6. 70.80–71.07s · middle (x 4%–96%, y 59%–70%) · appears, slides leftward, linear · #6a6766 · text “YOUR DMS / NEW MESSAGE / FULL SETUP GUIDE” · [crop](shots/shot_021_el_06.jpg)
7. 70.93–71.20s · bottom (x 20%–80%, y 78%–81%) · changes, moves leftward, ease-in-out · #faf7f4 · text “IF YOU WANT THE FULL / SETUP GUIDE, COMMENT / SKILL, AND I'LL DM IT” · [crop](shots/shot_021_el_07.jpg)

### Real material in the picture (the original files are needed)

8 shots, 25.7s (36%) contain real material (screen recordings, screenshots, photos, embedded video); a model cannot stand in for them:

- **screen recording** (part of the frame x5% y18% w90% h51%): shots #4, 3.6s in all
- **UI screenshot** (part of the frame x5% y47% w90% h24%): shots #6, 3.5s in all
- **screen recording** (part of the frame x5% y28% w90% h43%): shots #9, 2.6s in all
- **screen recording** (part of the frame x5% y12% w93% h50%): shots #10, 2.7s in all
- **screen recording** (part of the frame x5% y17% w90% h55%): shots #11, 2.1s in all
- **screen recording** (part of the frame x5% y18% w90% h54%): shots #12, #16, 6.6s in all
- **UI screenshot** (part of the frame x48% y18% w47% h54%): shots #19, 4.6s in all
