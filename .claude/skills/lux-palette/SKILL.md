---
name: lux-palette
description: Apply the "Lux Blue" brand system (electric blue, midnight navy, white, platinum; Anton + Playfair italic + Inter) to any video edit, thumbnail or graphic. Use when the user asks for luxury blue/white branding, brand colours, or "make it look expensive".
---
# Lux Palette

Source of truth: `video-studio/brand/lux-blue.json`. Never invent new colours mid-project.

| Token | Hex | Use |
|---|---|---|
| electric | #0069FF | ONE accent per frame: key word, button, checkmarks |
| electricGlow | #3D8BFF | glows, active caption word |
| midnight | #0B1F3A | background mid-tone |
| abyss | #050D1C | background base / edges |
| white | #FFFFFF | headline type |
| mist | #EEF4FF | soft panels |
| platinum | #C9D3E3 | hairlines, labels, serif words |

Type: **Anton** uppercase for punch words, **Playfair Display italic** for connective words ("asked for the", "it's my"), **Inter** for UI/captions (tracking .34em for tiny uppercase labels).

Luxury finish checklist (all are already in `video-studio/composition.html`):
1. Radial navy gradient + two slow-drifting blurred blue orbs (never flat black).
2. 7% overlay film grain, re-offset every frame.
3. Soft vignette + 1px platinum inset frame line.
4. Eased motion only (expo-out reveals, quint-in-out camera). No bounce, no linear.
5. Thin electric progress bar at top (retention).
Do not use other companies' logos, names or trademarked signature colours.
