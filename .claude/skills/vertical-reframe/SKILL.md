---
name: vertical-reframe
description: Export one edit as 9:16 (Reels/TikTok/Shorts) and 1:1 (feed/LinkedIn) with layouts designed per format, not just cropped. Use when the user needs multiple aspect ratios.
---
# Vertical Reframe

`node video-studio/render.mjs projects/<name> both` renders both layouts from the same timeline:
- **916** (1080×1920): label → big type on top (y 180–620), phone window centred (606×1030), caption pill below, everything inside the platform safe zone (top 120, bottom ~250 reserved).
- **11** (1080×1080): editorial split: type stack left (350 px column), phone right (577×980).
Preview stills first: `--preview 0.6,16.8,33.8,44.8` → `projects/<name>/out/preview_*.jpg`. Workers default 4 (`--workers N`).
