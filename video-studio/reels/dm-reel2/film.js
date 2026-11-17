// DMSetter pendulum: pure function of time. window.seek(t) paints frame t (see lib/motion.js).
// Designed on a 540x960 grid and scaled x2 to the 1080x1920 canvas. 60 bpm: 1 beat = 1 second.
// One ball is the thread of the whole film: pendulum -> lamp -> step marker -> logo.
import * as M from './lib/motion.js';

const { W, H, clamp, lerp, springU, SPRING, font, text, layout, hash01, mulberry32 } = M;
const K = W / 540;
const C = { ink: '#16171C', cream: '#EBE4D2', accent: '#E5471E', dark: '#14151A', mute: '#8F8975', white: '#FFFFFF' };
const DISPLAY = 'Display', UI = 'UI';

// ------------------------------------------------------------ easing + helpers
const cl = (x) => clamp(x, 0, 1);
const eo = (p) => 1 - Math.pow(1 - cl(p), 3);
const eio = (p) => { p = cl(p); return p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2; };
const eob = (p) => { p = cl(p); const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); };
const tw = (ctx, str, f, track = 0) => { ctx.font = f; ctx.letterSpacing = `${track}px`; const w = ctx.measureText(str).width - track; ctx.letterSpacing = '0px'; return w; };

// ------------------------------------------------------------ geometry
const PIV = [270, -30], LEN = 560, TH = (26 * Math.PI) / 180;
const LAMP = [270, 140];
const START = [406.5, 507.3], ANCH = [271.5, -7.5];   // where the Higgsfield plate ends: ball + cable anchor
const TT = [0.2, 2.2, 4.2];                       // a text line is wiped in on these passes, erased on the next
const LINES = [
  [['A LEAD MESSAGES', C.ink], ['AT 11 PM.', C.accent]],
  [["YOU'RE ASLEEP.", C.ink], ["THEY'RE GONE.", C.accent]],
  [['NOT', C.ink], ['ANYMORE.', C.accent]],
];
const pend = (u) => { const th = TH * Math.sin(Math.PI * (u - 0.2)); return [PIV[0] + LEN * Math.sin(th), PIV[1] + LEN * Math.cos(th), th]; };

function ballPos(u) {
  if (u < 5.5) return START;
  const P = START;
  if (u < 6.1) { const e = eio((u - 5.5) / 0.6); return [lerp(P[0], LAMP[0], e), lerp(P[1], LAMP[1], e)]; }
  if (u < 9.3) return [LAMP[0] + Math.sin(u * 1.7) * 1.5, LAMP[1] + Math.sin(u * 2.3) * 1.5];
  if (u < 11.2) return [LAMP[0], lerp(LAMP[1], 320, eio((u - 9.3) / 1.1))];
  if (u < 11.6) { const e = eio((u - 11.2) / 0.4); return [lerp(270, 48, e), lerp(320, 299, e)]; }
  if (u < 13.4) return [48, 299];
  if (u < 13.8) return [48, lerp(299, 493, eio((u - 13.4) / 0.4))];
  if (u < 15.5) return [48, 493];
  if (u < 15.9) return [48, lerp(493, 667, eio((u - 15.5) / 0.4))];
  if (u < 17.8) return [48, 667];
  if (u < 18.5) { const e = eio((u - 17.8) / 0.7); return [lerp(48, 270, e), lerp(667, 276, e)]; }
  return [270, 276];
}

// ------------------------------------------------------------ drawing
function bg(ctx) {
  const g = ctx.createRadialGradient(270, 460, 0, 270, 460, 540);
  g.addColorStop(0, '#F1EBDA'); g.addColorStop(0.62, '#E9E1CC'); g.addColorStop(1, '#DDD3BA');
  ctx.fillStyle = g; ctx.fillRect(-20, -20, 580, 1000);
}

function drawBall(ctx, x, y, scale = 1, alpha = 1) {
  if (alpha <= 0) return;
  ctx.save(); ctx.translate(x, y); ctx.scale(scale, scale); ctx.globalAlpha = alpha;
  const glow = ctx.createRadialGradient(0, 0, 8, 0, 0, 74);
  glow.addColorStop(0, 'rgba(229,71,30,.55)'); glow.addColorStop(0.4, 'rgba(229,71,30,.2)'); glow.addColorStop(1, 'rgba(229,71,30,0)');
  ctx.fillStyle = glow; ctx.beginPath(); ctx.arc(0, 0, 74, 0, M.TAU); ctx.fill();
  const g = ctx.createRadialGradient(-6, -7, 1, 0, 0, 20);
  g.addColorStop(0, '#FFA27A'); g.addColorStop(0.38, '#F2602F'); g.addColorStop(0.78, '#D73A12'); g.addColorStop(1, '#B22C0B');
  ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, 20, 0, M.TAU); ctx.fill();
  ctx.restore();
}

function textLines(ctx, lines, wipeVis, y1 = 438, y2 = 490) {
  if (wipeVis <= 0) return;
  ctx.save(); ctx.beginPath(); ctx.rect(0, 0, 540 * wipeVis, 960); ctx.clip();
  const f = font(50, 900, DISPLAY), tr = -2;
  text(ctx, lines[0][0], 270, y1, f, lines[0][1], 'center', tr);
  text(ctx, lines[1][0], 270, y2, f, lines[1][1], 'center', tr);
  ctx.restore();
}

function fan(ax, ay, a, h) {
  const pts = [[ax, ay]], n = Math.max(2, Math.ceil((h * 2) / 0.26));
  for (let i = 0; i <= n; i++) { const ang = a - h + (2 * h * i) / n; pts.push([ax + 2400 * Math.sin(ang), ay + 2400 * Math.cos(ang)]); }
  return pts;
}
function poly(ctx, pts) { ctx.beginPath(); pts.forEach((p, i) => (i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]))); ctx.closePath(); }

function spotText(ctx) {
  text(ctx, 'THE REPLY', 270, 430, font(60, 900, DISPLAY), C.ink, 'center', -2.4);
  text(ctx, 'DOES THE', 270, 492, font(60, 900, DISPLAY), C.ink, 'center', -2.4);
  text(ctx, 'booking.', 270, 560, font(66, 500, UI), C.accent, 'center', -1);
}

// ------------------------------------------------------------ scenes
function scenePendulum(ctx, u, bp) {
  bg(ctx);
  if (u < 5.9) textLines(ctx, LINES[2], 1, 398, 450);          // "NOT ANYMORE." exactly where the plate left it
  if (u < 5.75) {                                              // the cable, from its anchor to the ball, fading as the ball takes off
    const f = u < 5.5 ? 1 : 1 - cl((u - 5.5) / 0.25);
    ctx.save(); ctx.globalAlpha = f; ctx.strokeStyle = C.ink; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(ANCH[0], ANCH[1]); ctx.lineTo(bp[0], bp[1]); ctx.stroke(); ctx.restore();
  }
}

function sceneDark(ctx, u, bp) {
  // 5.5-6.1: dark panel wipes in diagonally from the right; then it holds until the cone opens fully
  if (u < 5.5 || u >= 9.95) return;
  if (u < 6.1) {
    const wp = eio((u - 5.5) / 0.45), xt = 540 - wp * 840, xb = xt + 230;
    ctx.fillStyle = C.dark; poly(ctx, [[xt, 0], [550, 0], [550, 960], [xb, 960]]); ctx.fill();
  } else { ctx.fillStyle = C.dark; ctx.fillRect(-20, -20, 580, 1000); }
}

function sceneCone(ctx, u, bp) {
  if (u < 6.0 || u >= 11.2) return;
  const k = cl((u - 6.1) / 2.9), sa = (-34 * Math.PI) / 180;
  const alpha = lerp(sa, 0, eo(k)) + Math.sin((u - 6.1) * 3.2) * 0.06 * (1 - k);
  const hh = (lerp(13, 24, eo((u - 6.1) / 2.7)) * Math.PI) / 180;
  const ex = cl((u - 9.3) / 0.6), h2 = hh + ex * ex * (3.3 - hh);
  const ax = bp[0], ay = bp[1] + 6, a = alpha * (1 - ex);
  const fade = u < 10.6 ? 1 : 1 - cl((u - 10.6) / 0.5);
  ctx.save(); ctx.globalAlpha = fade;
  ctx.fillStyle = 'rgba(240,232,212,.13)'; poly(ctx, fan(ax, ay, a, h2 + 0.13 + ex * 2)); ctx.fill();   // penumbra
  ctx.save(); poly(ctx, fan(ax, ay, a, h2)); ctx.clip();
  const g = ctx.createLinearGradient(0, 0, 0, 960);
  g.addColorStop(0, '#F4EEDD'); g.addColorStop(0.55, '#E8E0CA'); g.addColorStop(1, '#D9CFB4');
  ctx.fillStyle = g; ctx.fillRect(-20, -20, 580, 1000);
  spotText(ctx);
  ctx.restore(); ctx.restore();
}

const STEPS = [
  { u: 11.7, y: 272, lab: 'STEP 01', a: 'Connect ', b: 'your Instagram', sub: 'Link your account.' },
  { u: 13.5, y: 462, lab: 'STEP 02', a: 'Choose ', b: 'your replies', sub: 'Pick the replies that fit you.' },
  { u: 15.6, y: 632, lab: 'STEP 03', a: 'Wake up ', b: 'to booked calls', sub: null },
];

function sceneHow(ctx, u) {
  const ho = cl((u - 11.0) / 0.5) * (1 - cl((u - 17.7) / 0.4));
  if (ho <= 0) return;
  ctx.save(); ctx.globalAlpha = ho;
  const f1 = font(40, 800, DISPLAY), w1 = tw(ctx, 'how it ', f1, -1.4);
  text(ctx, 'how it ', 28, 150, f1, C.ink, 'left', -1.4); text(ctx, 'works', 28 + w1 + 4, 150, font(44, 500, UI), C.accent);
  // the vertical line grows, with three nodes
  const lp = eo((u - 11.2) / 1.2);
  ctx.strokeStyle = C.accent; ctx.globalAlpha = ho * 0.5; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(47, 228); ctx.lineTo(47, 228 + 520 * lp); ctx.stroke();
  ctx.globalAlpha = ho; ctx.lineWidth = 1.6;
  [298.5, 492.5, 666.5].forEach((ny) => { ctx.fillStyle = C.cream; ctx.strokeStyle = C.accent; ctx.beginPath(); ctx.arc(47.5, ny, 6.5, 0, M.TAU); ctx.fill(); ctx.stroke(); });
  STEPS.forEach((s, i) => {
    const p = eo((u - s.u) / 0.5); if (p <= 0) return;
    const y = s.y + (1 - p) * 14; ctx.save(); ctx.globalAlpha = ho * p;
    text(ctx, s.lab, 76, y + 10, font(11, 700, DISPLAY), C.accent, 'left', 1.1);
    const fa = font(31, 800, DISPLAY), wa = tw(ctx, s.a, fa, -1.0);
    text(ctx, s.a, 76, y + 42, fa, C.ink, 'left', -1.0); text(ctx, s.b, 76 + wa, y + 42, font(34, 500, UI), C.ink);
    if (s.sub) text(ctx, s.sub, 76, y + 70, font(16, 500, DISPLAY), C.mute, 'left', 0);
    if (i === 2) {                    // progress bar: type + a thin bar only, no invented UI
      const bp = eio(cl((u - 16.3) / 1.1)), n = Math.min(3, Math.floor(bp * 3.999));
      text(ctx, `${n} / 3 calls booked`, 76, y + 72, font(16, 700, DISPLAY), C.ink, 'left', 0);
      M.rrect(ctx, 76, y + 86, 380, 8, 4); ctx.fillStyle = '#CFC6AE'; ctx.fill();
      M.rrect(ctx, 76, y + 86, Math.max(8, 380 * bp), 8, 4); ctx.fillStyle = C.accent; ctx.fill();
      text(ctx, 'VALUES ILLUSTRATIVE', 76, y + 116, font(11, 700, DISPLAY), C.mute, 'left', 0.9);
    }
    ctx.restore();
  });
  ctx.restore();
}

function sceneEnd(ctx, u, IMG, bp) {
  if (u < 18.2) return;
  const wp = eo((u - 18.2) / 0.5);
  ctx.save(); ctx.globalAlpha = wp;
  const fa = font(62, 900, DISPLAY), fb = font(68, 500, UI), wa = tw(ctx, 'DM', fa, -2.8), wb = tw(ctx, 'Setter', fb, 0);
  const x0 = 270 - (wa + 2 + wb) / 2, y = 410 + (1 - wp) * 18;
  text(ctx, 'DM', x0, y, fa, C.ink, 'left', -2.8); text(ctx, 'Setter', x0 + wa + 2, y, fb, C.accent);
  ctx.restore();
  // ball -> logo
  const m = cl((u - 19.0) / 0.35);
  if (m > 0 && IMG.logo) {
    const s = 0.6 + 0.4 * eob(m), sz = 120 * s;
    ctx.save(); ctx.globalAlpha = eo(m); ctx.shadowColor = 'rgba(229,71,30,.35)'; ctx.shadowBlur = 18; ctx.shadowOffsetY = 10;
    ctx.drawImage(IMG.logo, 270 - sz / 2, 276 - sz / 2, sz, sz); ctx.restore();
  }
  // call-to-action pill
  const cp = eob((u - 19.3) / 0.5);
  if (cp > 0) {
    ctx.save(); ctx.translate(270, 506); ctx.scale(0.85 + 0.15 * clamp(cp, 0, 1), 0.85 + 0.15 * clamp(cp, 0, 1)); ctx.globalAlpha = clamp(cp, 0, 1);
    M.rrect(ctx, -174, -26, 348, 52, 26); ctx.fillStyle = C.ink; ctx.fill();
    const f1 = font(17, 600, DISPLAY), f2 = font(24, 500, UI), a = 'comment ', b = '“SPEED”', c2 = ' for the replies';
    const wA = tw(ctx, a, f1), wB = tw(ctx, b, f2), wC = tw(ctx, c2, f1), x = -(wA + wB + wC) / 2;
    text(ctx, a, x, 7, f1, C.white); text(ctx, b, x + wA, 8, f2, C.accent); text(ctx, c2, x + wA + wB, 7, f1, C.white);
    ctx.restore();
  }
  const ap = eo((u - 19.9) / 0.3);
  if (ap > 0) {
    ctx.save(); ctx.globalAlpha = ap; ctx.translate(270, 578 + Math.sin(u * 5) * 3); ctx.strokeStyle = C.ink; ctx.lineWidth = 2.2; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.beginPath(); ctx.moveTo(0, -12); ctx.lineTo(0, 12); ctx.moveTo(-8, 4); ctx.lineTo(0, 12); ctx.lineTo(8, 4); ctx.stroke(); ctx.restore();
  }
  const fp = eo((u - 20.2) / 0.4);
  if (fp > 0) { ctx.save(); ctx.globalAlpha = fp; text(ctx, 'follow for more DM builds', 270, 628, font(11, 500, DISPLAY), C.mute, 'center', 0.6); ctx.restore(); }
}

// ------------------------------------------------------------ hits (sound is voiced from this list)
const HITS = [];
for (const t of [0.83, 2.46, 4.54]) HITS.push([t, 'cable passes the words', 'whoosh', { len: 0.6, from: 1500, to: 600, gain: 0.2 }]);
for (const t of [1.6, 3.5, 5.3]) HITS.push([t, 'apex', 'tick', { gain: 0.1 }]);
for (const t of [0.55, 2.15, 4.2]) HITS.push([t, 'words written', 'tick', { gain: 0.1 }]);
HITS.push(
  [5.4, 'dark wipe', 'whoosh', { len: 0.5, gain: 0.3 }], [5.95, 'ball becomes the lamp', 'thud', { pitch: 95, to: 50, gain: 0.3 }], [6.05, 'lamp on', 'click', { gain: 0.2 }],
  [6.6, 'cone swing', 'whoosh', { len: 0.4, gain: 0.12 }], [7.7, 'cone swing', 'whoosh', { len: 0.4, gain: 0.12 }], [8.6, 'cone swing', 'whoosh', { len: 0.4, gain: 0.12 }],
  [9.25, 'cone opens', 'whoosh', { len: 0.5, gain: 0.22 }], [9.55, 'reveal', 'pop', { pitch: 'A5', gain: 0.25 }], [9.62, 'reveal', 'bell', { pitch: 'D6', gain: 0.18 }],
  [11.2, 'to steps', 'whoosh', { len: 0.35, gain: 0.1 }], [11.75, 'step 1', 'click', { gain: 0.22 }],
  [13.4, 'ball moves', 'whoosh', { len: 0.35, gain: 0.12 }], [13.6, 'step 2', 'click', { gain: 0.22 }],
  [15.5, 'ball moves', 'whoosh', { len: 0.35, gain: 0.12 }], [15.7, 'step 3', 'click', { gain: 0.22 }],
);
for (let j = 0; j < 10; j++) HITS.push([16.35 + j * 0.1, 'bar fills', 'tick', { gain: 0.07 + j * 0.006 }]);
HITS.push(
  [17.5, 'booked', 'bell', { pitch: 'E6', gain: 0.3 }], [17.8, 'to end card', 'whoosh', { len: 0.4, gain: 0.14 }], [18.15, 'wordmark', 'pop', { pitch: 'G5', gain: 0.22 }],
  [19.05, 'ball becomes logo', 'pop', { pitch: 'C6', gain: 0.28 }], [19.4, 'call to action', 'click', { gain: 0.25 }], [20.0, 'arrow', 'tick', { gain: 0.1 }],
);

// ------------------------------------------------------------ film
let NOISE = null;
M.film({
  fonts: [font(100, 900, DISPLAY), font(40, 500, UI)],
  images: { logo: 'assets/logo/mark_primary.svg' },
  hits: HITS,
  samples: 16,
  init() {
    NOISE = document.createElement('canvas'); NOISE.width = NOISE.height = 256;
    const c = NOISE.getContext('2d'), d = c.createImageData(256, 256), r = mulberry32(7);
    for (let i = 0; i < d.data.length; i += 4) { const v = 215 + r() * 40; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; }
    c.putImageData(d, 0, 0);
  },
  draw(ctx, u, t, IMG) {
    ctx.save();
    ctx.scale(K, K);
    // locked camera with a whisper of drift
    ctx.translate(270 + Math.sin(t * 0.9) * 1.6, 480 + Math.cos(t * 0.7) * 1.6);
    ctx.rotate(Math.sin(t * 0.45) * 0.0017); ctx.scale(1.022, 1.022); ctx.translate(-270, -480);
    const bp = ballPos(u);
    scenePendulum(ctx, u, bp);
    sceneDark(ctx, u, bp);
    sceneCone(ctx, u, bp);
    sceneHow(ctx, u);
    sceneEnd(ctx, u, IMG, bp);
    // the handle, always
    text(ctx, '@aidmsetter.co', 18, 22, font(10, 500, DISPLAY), u >= 6.0 && u < 9.9 ? '#8A8A8F' : C.mute, 'left', 0.3);
    // the ball is drawn last; it becomes the logo at 19.0
    const m = clamp((u - 19.0) / 0.35, 0, 1);
    drawBall(ctx, bp[0], bp[1], u >= 6.0 && u < 9.9 ? 1.35 : 1, 1 - eo(m));
    ctx.restore();
  },
  post(ctx, u, t) {
    // grain + vignette after the motion-blur accumulation so the sub-frame average can't erase them
    const fi = Math.floor(t * 30 + 0.5), ox = hash01(fi, 3) * 256, oy = hash01(fi, 5) * 256;
    ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = 0.55;
    ctx.translate(ox, oy); ctx.fillStyle = ctx.createPattern(NOISE, 'repeat'); ctx.fillRect(-256, -256, W + 512, H + 512);
    ctx.restore();
    const g = ctx.createRadialGradient(W / 2, H * 0.47, W * 0.55, W / 2, H * 0.47, H * 0.75);
    g.addColorStop(0, 'rgba(20,10,0,0)'); g.addColorStop(1, 'rgba(20,10,0,.2)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  },
});
