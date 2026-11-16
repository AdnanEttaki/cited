---
videomd: 1
part: remake
tokens: 4952
---

## Remake plan

### Step by step

This is a motion-graphics explainer. Every number in the steps below was measured on the original; follow them and check yours against it.

1. **Write the content**: one picture of your own for each of the 8 shots in the shot list
2. **Motion graphics**: `rea-video code-remake <report dir>` writes an editable project and a first cut from the measured layout and motion; change the text and data and rerun; elements and timing per scene under “Code build” below
3. **Subtitles and styled text**: the subtitle timing is saved as `packaging/subtitles.srt` (standard SRT), which any editor that imports SRT can use; replace the words; the other styled text and stickers, with timing and style, under “Packaging layer”
4. **Music**: source: to confirm, about 178 BPM, C major; find a track at the same tempo and mood, style and sections under “Sound”
5. **Sound effects**: 13, with the time and the picture event each one hits under “Sound”; each can be played first
6. **Put it together and compare**: hand the shots you made to the agent; `rea-video remake` places them on the original timeline, keeps the original where yours are missing, and renders a side-by-side comparison with the original

**4 3D render shots → 3 generation units, 3 Seedance 2.0 calls; code render / screen capture 4 shots → 1 code project (2 parts)**

- Grouping: AI shots in the same scene joined by hard cuts are generated in one call; ≤15s per call; consecutive hard cuts inside a unit preferably ≤8s, at most 10s; split at dissolves / fades and scene changes
- Audio: the model can generate action sound effects and ambience along with the picture
- Packaging: the text label, styled text on the generated shots is post-production packaging: keep it out of the prompts, erase it from reference frames, and lay it back on from the packaging timeline after generation
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
| G1 | #3–#4 | 7.5–8.5s | 0.9s | multi-shot | first frame | — |
| G2 | #5 | 8.5–8.8s | 0.4s | single shot | first frame + last frame | — |
| G3 | #6 | 8.8–9.3s | 0.5s | single shot | first frame + last frame | — |

**G1 · shots #3, #4 · 0.9s · first-frame image to video**

| Input | Needed | From | Why |
|---|---|---|---|
| text prompt | yes | see the prompt below | describes picture, action and camera; every other input only constrains it |
| first frame | yes | source frame `shots/shot_003_first.jpg` (to change product, person or style, redraw it with an image model from the first-frame prompt below) | locks composition, shot size and subject position; with text alone every generation frames it differently |
| last frame | no | — | several shots in one call; a last frame would only constrain the final shot |
| reference video | no | — | this unit locks framing with first / last frames; the model takes no reference video alongside them, so put action and camera move in the prompt |

- Generate 4s and trim to 0.9s (very short shots are unstable when generated on their own)
- Alternative: a 3D project. Have an LLM write a Blender script or a Three.js scene; model the characters / props once and render each shot from its own camera. Best for multiple angles and character consistency, and changing copy or shots is just a code change
- Shots #3, #4 have no prompt

```text
Vertical 9:16; night / low-light ambient, no dedicated fill, hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). Hard cuts between shots.
Shot 1 (0.0–0.6s): (prompt missing: run --vlm or have the agent write one from the frames)
Shot 2 (0.6–0.9s): (prompt missing: run --vlm or have the agent write one from the frames)
```

**G2 · shots #5 · 0.4s · first + last frame to video**

| Input | Needed | From | Why |
|---|---|---|---|
| text prompt | yes | see the prompt below | describes picture, action and camera; every other input only constrains it |
| first frame | yes | source frame `shots/shot_005_first.jpg` (to change product, person or style, redraw it with an image model from the first-frame prompt below) | locks composition, shot size and subject position; with text alone every generation frames it differently |
| last frame | worth it | source frame `shots/shot_005_last.jpg`, treated like the first frame | the shot moves; pinning the end frame leaves the model only the in-between, so motion and the final framing stay close to the source |
| reference video | no | — | this unit locks framing with first / last frames; the model takes no reference video alongside them, so put action and camera move in the prompt |

- Generate 4s and trim to 0.4s (very short shots are unstable when generated on their own)
- Alternative: a 3D project. Have an LLM write a Blender script or a Three.js scene; model the characters / props once and render each shot from its own camera. Best for multiple angles and character consistency, and changing copy or shots is just a code change
- Shots #5 have no prompt

```text
Vertical 9:16; night / low-light ambient, no dedicated fill, hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode).
(prompt missing: run --vlm or have the agent write one from the frames)
```

**G3 · shots #6 · 0.5s · first + last frame to video**

| Input | Needed | From | Why |
|---|---|---|---|
| text prompt | yes | see the prompt below | describes picture, action and camera; every other input only constrains it |
| first frame | yes | source frame `shots/shot_006_first.jpg` (to change product, person or style, redraw it with an image model from the first-frame prompt below) | locks composition, shot size and subject position; with text alone every generation frames it differently |
| last frame | worth it | source frame `shots/shot_006_last.jpg`, treated like the first frame | the shot moves; pinning the end frame leaves the model only the in-between, so motion and the final framing stay close to the source |
| reference video | no | — | this unit locks framing with first / last frames; the model takes no reference video alongside them, so put action and camera move in the prompt |

- Generate 4s and trim to 0.5s (very short shots are unstable when generated on their own)
- Alternative: a 3D project. Have an LLM write a Blender script or a Three.js scene; model the characters / props once and render each shot from its own camera. Best for multiple angles and character consistency, and changing copy or shots is just a code change
- Shots #6 have no prompt

```text
Vertical 9:16; night / low-light ambient, no dedicated fill, hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode).
(prompt missing: run --vlm or have the agent write one from the frames)
```

### Code composition

One Remotion / HTML project rebuilt from the text tracks and layout (text and UI are 100% controllable; changing copy is a data change). An LLM can write this project directly.

Start with `rea-video code-remake <breakdown folder>`: it writes `code/spec.json` + `code/render.py` from each scene's sampled points / cut-out, motion and background glow below, matches each scene's amount and brightness to the original, renders `code/remake.mp4` and scores it. Work from that version (edit spec.json, swap the points, or port it to Remotion) instead of writing one from scratch.

- Part 1: shots #1, #2 (0.0–7.5s)
- Part 2: shots #7, #8 (9.3–20.9s)

Remake assets (all in the report folder; hand them over together with the data below to whoever writes the code, or to an LLM):
- `shots/shot_XXX_first.jpg` / `_last.jpg`: first / last frame of each shot at full size, for layout, type size and margins
- `shots/shot_XXX_strip.jpg`: key frames about every 0.5 s, to follow the animation
- `shots/shot_XXX_elements.jpg` and `_el_NN.jpg` / `_st_NN.jpg` / `_ly_NN.jpg`: full-size crop of every element once settled, numbered as in the motion timeline; redraw shapes from them, cut out icons, logos and illustrations that cannot be redrawn
- `packaging/overlays.ass`, `packaging/timeline.json`: timing, position and colour of the text

How to build the pictures (by the measured picture type):
- kinetic type: Word-by-word spring() entrances (offset + scale + opacity), highlight boxes on key words; match font, size and leading from the frame
- data chart: SVG / D3 scales for axes and marks, numbers counted up with interpolate(), bars / lines grown with spring()

| Shot | Time | Build | Picture | Camera | Colours | On-screen text |
|---|---|---|---|---|---|---|
| #1 | 0.0–5.5s | kinetic type | (to fill from the images: what the elements form and how they move) | static | ground #dfd9c6 · #e8e2cf #14151a #d4cebb #473732 · drawn #1c1717 #f05e2b #85796d | @navkapoor.ai |
| #2 | 5.5–7.5s | kinetic type | (to fill from the images: what the elements form and how they move) | static frame, elements move inside it | ground #13151b · #222228 #bab2a6 #a0998f #d9d1bf · drawn #e4dac7 #b8aca0 #66372b | @navkapoor.ai |
| #7 | 9.3–11.1s | kinetic type | (to fill from the images: what the elements form and how they move) | static | ground #dfd9c6 · #e9e2cd #d7ccba #aaa59a #eea483 · drawn #1b1717 #6b635b #e35b2b #d8977a | THE SKILL / DOES THE / editing. / @navkapoor.ai |
| #8 | 11.1–20.9s | data chart | (to fill from the images: what the elements form and how they move) | static | ground #d7d1c0 · #e7e1ce #151415 #332927 #6b6760 · drawn #1d1817 #a59a8e #e37145 | how it works / @navkapoor.ai |

**Picture scenes** (a new scene whenever what is drawn moves or changes shape as a whole inside a shot. `frames/` holds first / middle / last full-size frames per scene, `scene_XX_layer.png` the drawn layer of the middle frame (background and text removed, alpha by how strongly it stands out), `frames/points/scene_XX.json` samples of that layer, one `x y r g b a` per row with x, y in 0–1. Place particles, trace lines or redraw shapes from these instead of guessing from a description. `track` in `frames/scenes.json` follows the layer's centre and spread over time)

| Scene | Shot | Time | Ground | Background glow | Drawn colours | Pieces | Area (x0 y0 x1 y1) | Motion |
|---|---|---|---|---|---|---|---|---|
| scene_01 | #1 | 0.0–5.5s | #dad7c4 | #9f9a8d, centre (0.52, 0.50), radius 0.21 | #2e261a #a19282 #d84d2c | 2 | 0.65 0.01 0.91 0.56 | zoom out 33%/s, turns anticlockwise 3.8°/s, pans (-24.6%, -7.6%)/s, points wander |
| scene_02 | #2 | 5.5–7.5s | #141519 | #321f1d, centre (0.50, 0.27), radius 0.12 | #6b2b1e #df4f2a #f38a63 | 1 | 0.45 0.24 0.54 0.29 | pans (+2.5%, +0.2%)/s |
| scene_03 | #7 | 9.3–11.1s | #cfccb9 | #9c968a, centre (0.50, 0.54), radius 0.23 | #ed9979 #ca4322 #df7755 | 1 | 0.45 0.28 0.50 0.28 | near still |
| scene_04 | #8 | 11.1–12.6s | #dad7c4 | #c8c2b2, centre (0.54, 0.55), radius 0.54 | #dc4b27 #eca387 #ec7048 | 1 | 0.11 0.36 0.17 0.39 | turns anticlockwise 0.9°/s, pans (-0.4%, +3.3%)/s |
| scene_05 | #8 | 12.6–16.4s | #dad7c4 | #c8c2b2, centre (0.56, 0.56), radius 0.46 | #ac9f91 #d75c39 #fbbca6 | 4 | 0.12 0.37 0.76 0.64 | morphs in from the last scene |
| scene_06 | #8 | 16.4–20.9s | #dad7c4 | #bcb6a8, centre (0.45, 0.48), radius 0.17 | #191714 #e06745 #867b6f | 15 | 0.11 0.14 0.89 0.50 | morphs in from the last scene |

When built, score it with `rea-video compare original remake --scenes frames/scenes.json -o dir` (each side's drawn layer is taken against its own ground, so a new ground colour still compares) and fix the lowest-scoring scenes first, from `compare_worst.jpg`.

Per-shot motion timeline (measured: positions in % of frame width / height, colours sampled once the element settles; read together with the key-frame strip)

**Motion #1 0.0–5.5s · 4 events**

- Ground #dfd9c6; other main colours #e8e2cf #14151a #d4cebb #473732; drawn layer #1c1717 #f05e2b #85796d
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: shape / text block · x 7%–21%, y 6%–8% · #aea797 · text “@navkapoor.ai” · [crop](shots/shot_001_st_01.jpg)
- S2. never moves: shape / text block · x 0%–22%, y 9%–46% · #e8dfcb · [crop](shots/shot_001_st_02.jpg)
- S3. never moves: shape / text block · x 44%–47%, y 15%–19% · #ebe2ce · [crop](shots/shot_001_st_03.jpg)
- S4. never moves: shape / text block · x 49%–53%, y 25%–44% · #ebe2ce · [crop](shots/shot_001_st_04.jpg)
- S5. never moves: shape / text block · x 36%–38%, y 28%–34% · #ebe2ce · [crop](shots/shot_001_st_05.jpg)
- S6. never moves: shape / text block · x 40%–44%, y 28%–44% · #ebe2ce · [crop](shots/shot_001_st_06.jpg)
- S7. never moves: shape / text block · x 31%–36%, y 35%–44% · #ebe2ce · [crop](shots/shot_001_st_07.jpg)
- S8. never moves: shape / text block · x 0%–58%, y 56%–100% · #ebe2ce · [crop](shots/shot_001_st_08.jpg)
- [crop L1](shots/shot_001_ly_01.jpg) [crop L2](shots/shot_001_ly_02.jpg) · Continuous layer: 7% of the frame moves through the whole shot (x 4%–96%, y 44%–58%), e.g. drifting gradients, particle flow, breathing glow
1. 0.20–4.53s · top left (x 16%–49%, y 0%–45%) · changes, moves rightward, ease-in-out · #ebe2ce · text “@navkapoor.ai / IMADE / WITHOUT” · [crop](shots/shot_001_el_01.jpg)
2. 0.20–4.53s · middle left (x 11%–42%, y 52%–60%) · appears, slides rightward, ease-in-out · #f96236 · [crop](shots/shot_001_el_02.jpg)
3. 3.80–4.27s · top left (x 0%–36%, y 0%–56%) · changes, moves downward, ease-in-out · #ebd4c4 · text “@navkapoor.ai” · [crop](shots/shot_001_el_03.jpg)
4. 4.53–5.47s · middle right (x 47%–100%, y 0%–100%) · appears, unfolds leftward (draw-on / grow / wipe), ease-in-out · #15151b · text “IMADE / THIS REEL / THIS REEL.” · [crop](shots/shot_001_el_04.jpg)

**Motion #2 5.5–7.5s (wipe in) · 3 events**

- Ground #13151b; other main colours #222228 #bab2a6 #a0998f #d9d1bf; drawn layer #e4dac7 #b8aca0 #66372b
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- [crop L1](shots/shot_002_ly_01.jpg) [crop L2](shots/shot_002_ly_02.jpg) · Continuous layer: 4% of the frame moves through the whole shot (x 0%–60%, y 0%–70%), e.g. drifting gradients, particle flow, breathing glow
1. 5.60–6.00s · top left (x 0%–49%, y 0%–41%) · disappears, unfolds leftward (draw-on / grow / wipe), ease-in-out · #ebe2ce · text “@navkapoor.ai” · [crop](shots/shot_002_el_01.jpg)
2. 6.93–7.47s · middle (x 0%–100%, y 30%–100%) · appears, unfolds rightward (draw-on / grow / wipe), ease-in-out · #3f393b · text “ES / litin / HE” · [crop](shots/shot_002_el_02.jpg)
3. 7.20–7.40s · bottom (x 47%–87%, y 61%–100%) · appears, slides rightward, linear · #242229 · text “litin” · [crop](shots/shot_002_el_03.jpg)

**Motion #7 9.3–11.1s (wipe in) · 2 events**

- Ground #dfd9c6; other main colours #e9e2cd #d7ccba #aaa59a #eea483; drawn layer #1b1717 #6b635b #e35b2b #d8977a
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

1. 9.40–9.53s · top (x 0%–100%, y 0%–24%) · disappears, instant · #15151b · text “@navkapoor.ai” · [crop](shots/shot_007_el_01.jpg)
2. 11.00–11.07s · top (x 38%–58%, y 20%–32%) · changes, instant · #ebdec9 · [crop](shots/shot_007_el_02.jpg)

**Motion #8 11.1–20.9s (fade in) · 12 events**

- Ground #d7d1c0; other main colours #e7e1ce #151415 #332927 #6b6760; drawn layer #1d1817 #a59a8e #e37145
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: shape / text block · x 7%–11%, y 6%–8% · #b4ad9e · [crop](shots/shot_008_st_01.jpg)
1. 11.23–17.97s · top (x 7%–71%, y 20%–43%) · changes, unfolds downward (draw-on / grow / wipe), ease-in-out · #ebe2ce · text “how it works / STEP 01 / Install the skill” · [crop](shots/shot_008_el_01.jpg)
2. 13.57–17.97s · middle left (x 7%–20%, y 38%–42%) · disappears, ease-out · #ecccb6 · [crop](shots/shot_008_el_02.jpg)
3. 15.70–17.90s · bottom (x 7%–93%, y 65%–89%) · changes, unfolds downward (draw-on / grow / wipe), ease-in-out · #ebe2ce · text “"a 15s reel for my brand. bold ty / “a 15s reel for my brand. bold type, a / swinging ball, sound on every move."” · [crop](shots/shot_008_el_03.jpg)
4. 17.57–18.63s · middle (x 9%–91%, y 44%–74%) · appears, unfolds upward (draw-on / grow / wipe), ease-in-out · #ebe2ce · text “reel skill ins / reel skill installed / STEP 02” · [crop](shots/shot_008_el_04.jpg)
5. 17.57–17.90s · bottom (x 36%–64%, y 80%–84%) · disappears, ease-in-out · #141217 · [crop](shots/shot_008_el_05.jpg)
6. 17.63–17.97s · top (x 7%–87%, y 12%–42%) · disappears, moves rightward, ease-in · #c0a494 · text “how it works / STEP 01 / Install the skill” · [crop](shots/shot_008_el_06.jpg)
7. 17.63–17.97s · bottom (x 7%–93%, y 72%–90%) · disappears, unfolds downward (draw-on / grow / wipe), ease-in · #181317 · text “STEP 03 / Render the reel / reel.mp4” · [crop](shots/shot_008_el_07.jpg)
8. 17.90–17.97s · top (x 7%–67%, y 0%–8%) · changes, instant · #e5dcc8 · text “@navkapoor.ai” · [crop](shots/shot_008_el_08.jpg)
9. 18.77–19.43s · middle (x 47%–56%, y 36%–40%) · appears, linear · #efcab2 · text “Install the skill” · [crop](shots/shot_008_el_09.jpg)
10. 19.03–20.83s · middle (x 11%–89%, y 54%–64%) · appears, scales up, ease-in-out · #171215 · text “STEP 02 / Describe your idea / "a 15s reel for my brand. bold ty” · [crop](shots/shot_008_el_10.jpg)
11. 19.10–19.43s · middle (x 44%–56%, y 38%–44%) · appears, slides rightward, ease-in-out · #ecc5ac · text “Install the skill / reel skill ins / reel skill installed” · [crop](shots/shot_008_el_11.jpg)
12. 19.43–20.83s · middle (x 9%–91%, y 48%–72%) · changes, ease-in-out · #744b3f · text “STEP 02 / Describe your idea / "a 15s reel for my brand. bold ty” · [crop](shots/shot_008_el_12.jpg)
