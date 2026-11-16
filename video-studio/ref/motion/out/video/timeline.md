---
videomd: 1
part: timeline
shots: 8
tokens: 580
---

# Timeline

One shot per line: `#<n> start-end (s) | key value | …`. A key ending in `~` is the tools' inference; keys without it are visible on screen or measured directly.
`story` job in the story and the point · `seen` what is on screen · `act` acting (emotion, strength, face) · `camera` camera move · `overlay` overlays · `made~` how it was made (inferred) · `material~` where the material came from (inferred) · `remake` remake route · `flag` needs a second look
Full detail for a shot is in `video/shots/<n>.md` (e.g. `video/shots/07.md`).

```videomd-timeline
#01 0.0-5.5 | camera static | made~ code / template render 51% · runner-up 3D render 40% | material~ rendered by the creator | remake code render · Part 1 | flag low confidence
#02 5.5-7.5 | camera static (subject moves) | transition wipe 0.4s | made~ code / template render 59% · runner-up 3D render 20% | material~ rendered by the creator | remake code render · Part 1 | flag low confidence
#03 7.5-8.1 | camera static (subject moves) | overlay text, title | made~ 3D render 50% · runner-up code / template render 28% | material~ rendered by the creator | remake AI generation / 3D render · G1 | flag low confidence
#04 8.1-8.5 | camera static (subject moves) | overlay text, title | made~ 3D render 52% · runner-up code / template render 26% | material~ rendered by the creator | remake AI generation / 3D render · G1 | flag low confidence
#05 8.5-8.8 | camera static (subject moves) | transition slide 0.2s | overlay text, title | made~ 3D render 53% · runner-up code / template render 29% | material~ rendered by the creator | remake AI generation / 3D render · G2 | flag low confidence
#06 8.8-9.3 | camera smooth move | transition wipe 0.1s | overlay text, title | made~ 3D render 54% · runner-up code / template render 22% | material~ rendered by the creator | remake AI generation / 3D render · G3 | flag low confidence
#07 9.3-11.1 | camera static | transition wipe 0.4s | made~ code / template render 81% · runner-up 3D render 13% | material~ rendered by the creator | remake code render · Part 2
#08 11.1-20.9 | camera static | transition fade through 0.4s | made~ code / template render 73% · runner-up 3D render 9% | material~ rendered by the creator | remake code render · Part 2
```
