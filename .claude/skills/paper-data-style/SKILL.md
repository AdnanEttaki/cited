---
name: paper-data-style
description: Reference style "Paper Data" - cream paper + grid, editorial header, tactile 3D bars/cards/stickers, Instagram-style DM phone screens, big black captions with boxed highlight words, progress scrubber with flag. Use when the user asks for "the paper style", "the reference style", "like the storyboard", or data-story / explainer reels.
---
# Paper Data style (reference)

Reference board: `video-studio/storyboards/paper-data/storyboard.jpg` (12 frames, AI DM setter story).
Source: `video-studio/storyboards/paper-data/build.py` (all components + CSS) -> `node shoot.mjs` renders grid + single frames.
Look at the board before designing; match it.

## Tokens
- Paper: radial #F4F0E8 -> #ECE6DA -> #E2DBCD, 36px grid lines at 3.5% black, giant faded numeral bottom-left (430px, 6% brown).
- Ink #1B1B1B · Orange #D8541E (primary accent) · Teal #1E9E95 · Magenta #D9257E · Amber #F2A33A.
- Type: Inter 800, tight tracking (-.035em). Captions 44px/540w frame, left aligned.

## Frame anatomy (540x960, scale x2 for 1080x1920)
1. Header y78: 1px ink rule + 46x5 ink tab, UPPERCASE label left, time/step right (13px 800, .08em).
2. Visual zone y125-595: ONE tactile idea per frame (bar stack, bar race, chat cards, price tags, checklist bars, slot tiles, calendar + stamp, 3D column chart, big key-cap button).
3. Caption y620: max ~8 words; 1-2 words boxed (`.hl` ink, `.hlo` orange); de-emphasized words grey #9A9286.
4. Scrubber y820: progress line, knob = frame index, orange flag at the payoff frame, "Values illustrative" + "Frame n of N".

## Components (classes in build.py)
`bar` (extruded: gradient + 8px darker bottom edge + soft drop shadow), `card` + `bubble` (chat), `tag` (sticker), `slot`/`.up` (picked tile), `cal` + `stamp`, `chart`/`col`, `key` (3D key-cap CTA), `cbox` (comment field), `badge` (unread count).

## Rules
- No prices and no AI mentions in this brand's content. Chats always shown in the `phone()` Instagram-style DM screen (dark mode, gradient outgoing bubbles, Seen, message bar), using real conversations; never add the Instagram logo.
- Original content only: never copy other creators' logos, names or exact layouts.
- Any number that is not real must be labelled "Values illustrative" or replaced with the user's real data before ads.
- Motion (when animated): bars slide in from left with overshoot, numbers count up, cards drop with slight rotation, stamps slam with shake, captions word-by-word with box wipe.
