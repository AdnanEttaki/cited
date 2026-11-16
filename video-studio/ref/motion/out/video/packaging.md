---
videomd: 1
part: packaging
tokens: 467
---

## Packaging layer (subtitles / styled text / stickers / sound-effect hits)

- 2 subtitle lines (bottom, up to 1 rows): black text, keywords highlighted in orange, line height 2.5%; entrance: scale pop×1, hard in×1
- styled text ×1 (large size, orange fill, multi-colour / gradient): "ng."
- text label ×3 (1 of them follow an object): "HE DOE", "editing.", "KIL THE"
- SFX hits on: subtitle in ×1, cut ×1
- Exports: `packaging/subtitles.srt`, `packaging/overlays.ass`, `packaging/timeline.json` (SRT is the subtitle timeline; ASS carries colour, outline, position and entrance animation, swap in the original font; timeline.json is the full timeline)

| Time | Kind | Text | Style | In / out | SFX |
|---|---|---|---|---|---|
| 7.50–8.10s | text label | HE ⏎ DOE | black text, white outline, line height 9.3% (about 120px) | hard in / slide out | — |
| 7.50–10.60s | text label · follows an object | editing. | orange text, orange outline, keywords highlighted in white, line height 16.3% (about 209px) | hard in / shrink out (bounces / changes colour midway) | — |
| 8.50–8.60s | text label | KIL ⏎ THE | black text, white outline, line height 9.0% (about 116px) | hard in / hard out | — |
| 8.50–8.60s | styled text | ng. | orange text, keywords highlighted in grey, line height 14.4% (about 185px) | hard in / hard out | — |
| 9.50–11.10s | subtitle | • navkapoor.ai | black text, keywords highlighted in orange, line height 2.5% (about 32px) | pop / hard out | pop |
| 16.00–16.10s | subtitle | 0% | grey text, line height 2.6% (about 33px) | hard in / hard out | — |

Remake: burn subtitles and styled text in with `packaging/overlays.ass` (ffmpeg -vf ass=overlays.ass), or rebuild them from timeline.json in CapCut / Remotion; stickers and GIFs need matching assets (meme / GIF libraries), crops are under packaging/.
