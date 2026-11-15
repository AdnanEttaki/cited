---
videomd: 1
part: sound
tokens: 514
---

## Sound

- loudness -17.5 dBFS, peak -4.0 dBFS; each clip carries its own sound (background jumps 35.4dB at cuts vs 10.5dB within shots)
- Sources: Video type: voice-over / talking head + music → voice: TTS voice-over (leaning, to confirm); SFX: added in post from an SFX library / editor (leaning, to confirm)

**Voice**

- 56% of the duration; pitch about 158.1Hz (gender unclear)
- Source: to confirm (TTS voice-over 43%, human recording 43%, native dialogue from the AI video model 14%)
- Remake: capsule-cinema DoubaoTTSTool / UniversalTTSTool (or a MiniMax cloned voice); use duration-controlled TTS when it must fit the original time window; follow each line's delivery in the script, add tone tags only on the lines where the emotion turns, and write lines the way they are spoken (pauses, fillers), not as written copy

**Music**

- No sustained music bed detected

**Sound effects** (15 hits, 8 distinct sounds)

| Sound | Listen | Type | Times used | At | On screen |
|---|---|---|---|---|---|
| F1 | [listen](sfx/sfx_01.wav) | pop | 4 | 7.6s, 14.1s, 56.8s, 58.9s | subtitle "FREE." appears; subtitle "SKILLS" appears |
| F2 | [listen](sfx/sfx_02.wav) | pop | 1 | 8.2s | subtitle "last month" appears |
| F3 | [listen](sfx/sfx_03.wav) | click | 1 | 19.1s | subtitle "9" appears |
| F4 | [listen](sfx/sfx_04.wav) | click | 2 | 22.0s, 33.7s | cut |
| F5 | [listen](sfx/sfx_05.wav) | ding | 1 | 22.8s | — |
| F6 | [listen](sfx/sfx_06.wav) | click | 1 | 34.2s | — |
| F7 | [listen](sfx/sfx_07.wav) | pop | 2 | 36.7s, 37.6s | subtitle "5 REACH 3 PEERS " appears |
| F8 | [listen](sfx/sfx_08.wav) | ding | 3 | 40.4s, 67.3s, 71.2s | subtitle "IF YOU WANT THE " appears; subtitle "TO YOU." appears |

- Remake: play each sound first (separated out, without voice or music), find one similar effect in the editor's library, and place it at every time listed under “At”

- Separated stems: `stems/original.wav` (original), `stems/vocals.wav` (dry voice), `stems/music.wav` (music + ambience), `stems/effects.wav` (effects track)
<!--stems-->
