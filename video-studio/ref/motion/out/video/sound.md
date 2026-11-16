---
videomd: 1
part: sound
tokens: 604
---

## Sound

- loudness -16.4 dBFS, peak -1.6 dBFS; sound runs across cuts, laid in post as one bed (background changes 17.3dB at cuts vs 42.2dB within shots)
- Sources: Video type: music bed only (no voice) → music: stock library music (leaning, to confirm); SFX: added in post from an SFX library / editor (leaning, to confirm)

**Voice**

- None / very little

**Music**

- Tempo: 178.2 BPM (or 89.1/356.4); key C major (confidence 0.81); 95% of the duration (0.0–20.0s); section changes at 12.0s; ending: cut off hard
- Cuts vs beat: 14% of cuts land on a beat (chance: about 39%)
- Source: to confirm (stock library music 63%, well-known song 23%, AI-generated music 13%)
  - The music is a bed under the picture: in a regular video the bed usually comes from a stock library (prior)
  - The music is hard-cut at the end (still at full level when the video stops): typical of a trimmed existing track
  - Nothing about this track beyond the format prior and weak cues like the ending (no source heard, no platform music tag): source to confirm; an AI-generated bed cannot be told from a library bed here
  - How to confirm: Check the music tag on the original Douyin / Xiaohongshu / TikTok post: a song title → existing track; "original sound - @creator" → uploaded by the creator (for music videos, usually an AI song)
  - How to confirm: Run it through Shazam / ACRCloud or another song-ID service: a hit means an existing song
- Remake: The original track leans stock library music: search a library by BPM / mood / key for a similar track, or generate a royalty-free track in a similar style with AI

**Sound effects** (13 hits, 4 distinct sounds)

| Sound | Listen | Type | Times used | At | On screen |
|---|---|---|---|---|---|
| F1 | [listen](sfx/sfx_01.wav) | whoosh | 7 | 0.2s, 1.2s, 2.2s, 3.2s, 4.2s, 5.2s, 17.6s | — |
| F2 | [listen](sfx/sfx_02.wav) | whoosh | 3 | 7.1s, 11.1s, 13.5s | cut |
| F3 | [listen](sfx/sfx_03.wav) | pop | 1 | 9.6s | subtitle "• navkapoor.ai" appears |
| F4 | [listen](sfx/sfx_04.wav) | click | 2 | 13.2s, 17.2s | — |

- Remake: play each sound first (separated out, without voice or music), find one similar effect in the editor's library, and place it at every time listed under “At”

- Separated stems: `stems/original.wav` (original), `stems/vocals.wav` (dry voice), `stems/music.wav` (music + ambience), `stems/effects.wav` (effects track)
<!--stems-->
