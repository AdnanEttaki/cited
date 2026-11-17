// Text layer for the Higgsfield pendulum plate: black/orange type on WHITE, to be multiplied over the plate.
// The words are tied to the tracked cable: ahead of the cable the OLD words, behind it the NEW words,
// so each statement is erased right behind the cable and the next appears immediately after it.
import * as M from './lib/motion.js';
const { W, H, font, text, clamp } = M;
const K = W / 540;
const INK = '#16171C', ACC = '#F25A2E';
const TEXTS = [
  [['A LEAD MESSAGES', INK], ['AT 11 PM.', ACC]],
  [["YOU'RE ASLEEP.", INK], ["THEY'RE GONE.", ACC]],
  [['NOT', INK], ['ANYMORE.', ACC]],
];
let TR = null, APEX = [];          // tracked cable x (design units) per frame; apex times (direction reversals)
const cable = (t) => {             // linear interpolation of the 24 fps track
  const f = clamp(t * TR.fps, 0, TR.cx.length - 1), i = Math.floor(f), j = Math.min(TR.cx.length - 1, i + 1);
  return TR.cx[i] + (TR.cx[j] - TR.cx[i]) * (f - i);
};
function lines(ctx, ln) {
  const f = font(50, 900, 'Display');
  M.text(ctx, ln[0][0], 270, 398, f, ln[0][1], 'center', -2);
  M.text(ctx, ln[1][0], 270, 450, f, ln[1][1], 'center', -2);
}
M.film({
  fonts: [font(100, 900, 'Display')],
  samples: 1,
  async init() {
    const d = await (await fetch('assets/seed_cable.json')).json();
    TR = { fps: d.fps, cx: d.track.map((r) => (r ? r[2] * 0.75 : null)) };
    for (let i = 0; i < TR.cx.length; i++) if (TR.cx[i] == null) TR.cx[i] = TR.cx[Math.max(0, i - 1)];
    for (let i = 2; i < TR.cx.length - 2; i++) {
      if ((TR.cx[i] - TR.cx[i - 2]) * (TR.cx[i + 2] - TR.cx[i]) < 0 && (APEX.length === 0 || i / TR.fps - APEX[APEX.length - 1] > 0.5)) APEX.push(i / TR.fps);
    }
  },
  draw(ctx, u, t) {
    ctx.save(); ctx.fillStyle = '#FFFFFF'; ctx.fillRect(0, 0, W, H); ctx.scale(K, K);
    const x = cable(t), j = APEX.filter((a) => a <= t).length;      // pass index: 0 before the first apex, ...
    const dir = j % 2 === 0 ? 1 : -1;                                 // pass 0 moves right, pass 1 left, ...
    const old = j > 0 ? TEXTS[j - 1] : null, nw = TEXTS[Math.min(j, TEXTS.length - 1)];
    const edge = x - dir * 1;                                          // the wipe edge sits exactly under the cable
    // new words: BEHIND the cable
    ctx.save(); ctx.beginPath(); if (dir > 0) ctx.rect(-10, 0, edge + 10, 960); else ctx.rect(edge, 0, 560 - edge, 960); ctx.clip(); lines(ctx, nw); ctx.restore();
    // old words: AHEAD of the cable
    if (old) { ctx.save(); ctx.beginPath(); if (dir > 0) ctx.rect(edge, 0, 560 - edge, 960); else ctx.rect(-10, 0, edge + 10, 960); ctx.clip(); lines(ctx, old); ctx.restore(); }
    M.text(ctx, '@aidmsetter.co', 18, 22, font(10, 500, 'Display'), '#6F6B5C', 'left', 0.3);
    ctx.restore();
  },
});
