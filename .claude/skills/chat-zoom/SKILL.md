---
name: chat-zoom
description: Virtual camera that punches in on the exact chat bubble / UI moment in a screen recording (DM, CRM, app demo). Use when a screen recording needs to be watchable on a phone.
---
# Chat Zoom

`timeline.json` → `camera`: keyframes `[time, cx, cy, scale]` in cropped-source pixels (`crop` = the phone/UI area; `rawCrop` = ffmpeg crop `w:h:x:y`, find it with `ffmpeg -vf cropdetect`).
Interpolated with quint ease-in-out, clamped so edges never show, plus a tiny 0.6% breathing drift.

Workflow:
1. Grid key frames: `ffmpeg -ss T -i raw.mp4 -frames:v 1 -vf "crop=...,drawgrid=w=..:h=.."` and read bubble centres.
2. Scene-change times for message arrivals: `ffmpeg -i raw.mp4 -vf "select='gt(scene,0.02)',showinfo" -f null -`.
3. Pattern per key message: wide (1.0–1.1) → move in 0.6 s → hold at 1.4–1.65 while it is read → pull back before the chat scrolls.
Zoom only on proof moments (objection, answer, offer, booking). Wide shots in between let the viewer re-orient.
