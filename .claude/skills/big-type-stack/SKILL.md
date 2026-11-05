---
name: big-type-stack
description: Huge stacked headline typography that slams in line-by-line, synced to voiceover words (Anton + Playfair italic mix). Use for hooks, key claims, checklists, and CTAs in short-form videos.
---
# Big Type Stack

Defined per project in `projects/<name>/timeline.json` → `beats`:
```json
{ "t0": 0.25, "t1": 2.2, "lines": [["This lead","sans"],["asked for the","serif"],["price.","sans-blue"]] }
```
- styles: `sans` (white Anton), `sans-blue` (electric Anton + glow), `serif` (platinum Playfair italic), `check` (Anton with animated checkmark).
- Optional 3rd value = exact start time of that line (hit it on the VO word; get word times from `build/vo/<id>.json`).
- Lines auto-shrink to fit the type zone. Default stagger 80 ms, reveal 0.55 s expo-out with mask + blur; exit 0.3 s blur-up.

Writing rules: 2–3 lines, max ~3 words per line, one blue word per beat (the money word). Swap beats on the VO word, not between sentences. Use a `check` stack for step-by-step proof (time zone ✓ slots ✓ booked ✓).
