// "Why leads ghost you": a lamp in the dark, swinging cones of light reveal each reason; the room brightens
// from black to cream when the message turns to the fix. Pure function of time (window.seek). 60 bpm: 1 beat = 1 s.
// Designed on a 540x960 grid, scaled x2 to 1080x1920.
import * as M from './lib/motion.js';

const { W, H, clamp, lerp, font, text, hash01, mulberry32 } = M;
const K = W / 540;
const C = { ink: '#16171C', cream: '#EBE4D2', accent: '#E5471E', dark: '#14151A', mute: '#8F8975', white: '#FFFFFF' };
const DISPLAY = 'Display', UI = 'UI';

const cl = (x) => clamp(x, 0, 1);
const eo = (p) => 1 - Math.pow(1 - cl(p), 3);
const ei = (p) => Math.pow(cl(p), 3);
const eio = (p) => { p = cl(p); return p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2; };
const eob = (p) => { p = cl(p); const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); };
const tw = (ctx, str, f, track = 0) => { ctx.font = f; ctx.letterSpacing = `${track}px`; const w = ctx.measureText(str).width - track; ctx.letterSpacing = '0px'; return w; };
const RAD = Math.PI / 180;

// ------------------------------------------------------------ the story: four statements, then the fix
const LAMP = [270, 140];
const FLOOD = 14.0;                                  // the turn: dark -> light
const STM = [
  { u0: 0.0, label: null, l1: "THEY DON'T GHOST", l2: 'BECAUSE OF PRICE.', size: 41 },
  { u0: 3.5, label: 'REASON 1', l1: 'YOU REPLIED', l2: 'TOO LATE.', size: 56 },
  { u0: 7.0, label: 'REASON 2', l1: 'YOU ASKED', l2: 'NO QUESTION.', size: 56 },
  { u0: 10.5, label: 'REASON 3', l1: 'YOU NEVER', l2: 'FOLLOWED UP.', size: 56 },
];
const DUR = 3.5;

// Cone angle (rad from straight down) over a statement: arrives from one side, holds, leaves to the other.
function coneAngle(u) {
  const k = Math.min(3, Math.max(0, Math.floor(u / DUR))), s = k % 2 === 0 ? -1 : 1, l = u - k * DUR;
  const a0 = s * 36 * RAD;
  if (l < 1.0) return lerp(a0, 0, eo(l / 1.0));                     // arrives
  if (l < 2.7) return Math.sin(l * 2.1) * 0.012;                    // holds (breathes)
  return lerp(0, -s * 36 * RAD, ei((l - 2.7) / 0.8));               // leaves, to the other side
}
// first statement is already lit on frame 0: the cone is mid-swing, not waiting
function coneSpread(u) {
  const k = Math.min(3, Math.floor(u / DUR)), l = u - k * DUR;
  const hold = (36 + 1.0 * k) * RAD, narrow = 14 * RAD;                 // opens wide enough to read the whole line
  if (l < 1.0) return lerp(narrow, hold, eo(l / 1.0));
  if (l < 2.7) return hold;
  return lerp(hold, 17 * RAD, ei((l - 2.7) / 0.8));
}

function ballPos(u) {
  if (u < FLOOD + 2.5) return [LAMP[0] + Math.sin(u * 1.7) * 1.5, LAMP[1] + Math.sin(u * 2.3) * 1.5];
  if (u < 17.2) return [LAMP[0], lerp(LAMP[1], 276, eio((u - (FLOOD + 2.5)) / 0.7))];
  return [270, 276];
}

// ------------------------------------------------------------ drawing
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
function fan(ax, ay, a, h) {
  const pts = [[ax, ay]], n = Math.max(2, Math.ceil((h * 2) / 0.26));
  for (let i = 0; i <= n; i++) { const ang = a - h + (2 * h * i) / n; pts.push([ax + 2400 * Math.sin(ang), ay + 2400 * Math.cos(ang)]); }
  return pts;
}
function poly(ctx, pts) { ctx.beginPath(); pts.forEach((p, i) => (i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]))); ctx.closePath(); }
function creamFill(ctx) {
  const g = ctx.createLinearGradient(0, 0, 0, 960);
  g.addColorStop(0, '#F4EEDD'); g.addColorStop(0.55, '#E8E0CA'); g.addColorStop(1, '#D9CFB4');
  ctx.fillStyle = g; ctx.fillRect(-20, -20, 580, 1000);
}
function statement(ctx, s) {
  if (s.label) text(ctx, s.label, 270, 390, font(14, 700, DISPLAY), C.accent, 'center', 2.2);
  const f = font(s.size, 900, DISPLAY), tr = -0.04 * s.size;
  text(ctx, s.l1, 270, 446, f, C.ink, 'center', tr);
  text(ctx, s.l2, 270, 446 + s.size * 1.04, f, C.accent, 'center', tr);
}
function fixText(ctx) {
  text(ctx, 'FIX THE', 270, 440, font(70, 900, DISPLAY), C.ink, 'center', -2.8);
  text(ctx, 'reply.', 270, 522, font(80, 500, UI), C.accent, 'center', -1.2);
}

// the whole dark scene: lamp, cone, text lit only inside the cone
function sceneLight(ctx, u, bp) {
  const flood = cl((u - FLOOD) / 0.8);
  // cream world underneath, revealed as the flood opens
  const fixA = 1 - cl((u - 16.0) / 0.4);
  if (flood >= 1) { ctx.fillStyle = '#EBE4D2'; ctx.fillRect(-20, -20, 580, 1000); const g = ctx.createRadialGradient(270, 460, 0, 270, 460, 540); g.addColorStop(0, '#F1EBDA'); g.addColorStop(0.62, '#E9E1CC'); g.addColorStop(1, '#DDD3BA'); ctx.fillStyle = g; ctx.fillRect(-20, -20, 580, 1000); }
  if (flood < 1) {
    ctx.fillStyle = C.dark; ctx.fillRect(-20, -20, 580, 1000);
    const ex = eio(flood), a = (u < FLOOD ? coneAngle(u) : 0) * (1 - ex);
    const k = Math.min(3, Math.floor(u / DUR));
    const h = u < FLOOD ? coneSpread(u) : coneSpread(13.4);
    const h2 = h + ex * ex * (3.3 - h);
    const ax = bp[0], ay = bp[1] + 6;
    // penumbra: a little brighter with each reason (the room is waking up)
    ctx.fillStyle = `rgba(240,232,212,${0.1 + 0.05 * k + 0.2 * ex})`; poly(ctx, fan(ax, ay, a, h2 + 0.13 + ex * 2)); ctx.fill();
    ctx.save(); poly(ctx, fan(ax, ay, a, h2)); ctx.clip();
    creamFill(ctx);
    if (u < FLOOD) statement(ctx, STM[k]); else fixText(ctx);
    ctx.restore();
  } else if (fixA > 0) {
    ctx.save(); ctx.globalAlpha = fixA; fixText(ctx); ctx.restore();
  }
}

function sceneEnd(ctx, u, IMG) {
  if (u < 17.4) return;
  const wp = eo((u - 17.8) / 0.5);
  if (wp > 0) {
    ctx.save(); ctx.globalAlpha = wp;
    const fa = font(62, 900, DISPLAY), fb = font(68, 500, UI), wa = tw(ctx, 'DM', fa, -2.8), wb = tw(ctx, 'Setter', fb, 0);
    const x0 = 270 - (wa + 2 + wb) / 2, y = 410 + (1 - wp) * 18;
    text(ctx, 'DM', x0, y, fa, C.ink, 'left', -2.8); text(ctx, 'Setter', x0 + wa + 2, y, fb, C.accent);
    ctx.restore();
  }
  const m = cl((u - 17.4) / 0.35);
  if (m > 0 && IMG.logo) {
    const s = 0.6 + 0.4 * eob(m), sz = 120 * s;
    ctx.save(); ctx.globalAlpha = eo(m); ctx.shadowColor = 'rgba(229,71,30,.35)'; ctx.shadowBlur = 18; ctx.shadowOffsetY = 10;
    ctx.drawImage(IMG.logo, 270 - sz / 2, 276 - sz / 2, sz, sz); ctx.restore();
  }
  const cp = eob((u - 18.8) / 0.5);
  if (cp > 0) {
    const q = clamp(cp, 0, 1);
    ctx.save(); ctx.translate(270, 506); ctx.scale(0.85 + 0.15 * q, 0.85 + 0.15 * q); ctx.globalAlpha = q;
    M.rrect(ctx, -176, -26, 352, 52, 26); ctx.fillStyle = C.ink; ctx.fill();
    const f1 = font(17, 600, DISPLAY), f2 = font(24, 500, UI), a = 'comment ', b = '“GHOST”', c2 = ' for the replies';
    const wA = tw(ctx, a, f1), wB = tw(ctx, b, f2), wC = tw(ctx, c2, f1), x = -(wA + wB + wC) / 2;
    text(ctx, a, x, 7, f1, C.white); text(ctx, b, x + wA, 8, f2, C.accent); text(ctx, c2, x + wA + wB, 7, f1, C.white);
    ctx.restore();
  }
  const ap = eo((u - 19.5) / 0.3);
  if (ap > 0) {
    ctx.save(); ctx.globalAlpha = ap; ctx.translate(270, 578 + Math.sin(u * 5) * 3); ctx.strokeStyle = C.ink; ctx.lineWidth = 2.2; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.beginPath(); ctx.moveTo(0, -12); ctx.lineTo(0, 12); ctx.moveTo(-8, 4); ctx.lineTo(0, 12); ctx.lineTo(8, 4); ctx.stroke(); ctx.restore();
  }
  const fp = eo((u - 19.8) / 0.4);
  if (fp > 0) { ctx.save(); ctx.globalAlpha = fp; text(ctx, 'follow for more DM builds', 270, 628, font(11, 500, DISPLAY), C.mute, 'center', 0.6); ctx.restore(); }
}

// ------------------------------------------------------------ hits (sound is voiced from this list)
const HITS = [
  [0.05, 'lamp already lit', 'thud', { pitch: 90, to: 50, gain: 0.3 }], [0.0, 'lamp', 'click', { gain: 0.18 }],
];
STM.forEach((s, k) => {
  const b = s.u0;
  HITS.push([b + 0.7, 'cone arrives', 'whoosh', { len: 0.45, from: 1700, to: 600, gain: 0.2 }]);
  HITS.push([b + 1.0, 'reason lit', 'pop', { pitch: ['A5', 'B5', 'C#6', 'D#6'][k], gain: 0.24 }]);
  HITS.push([b + 2.9, 'cone leaves', 'whoosh', { len: 0.4, from: 800, to: 1700, gain: 0.12 }]);
  HITS.push([b + 1.05, 'text on', 'tick', { gain: 0.1 }]);
});
HITS.push(
  [FLOOD, 'the turn: light floods the room', 'riser', { len: 1.6, gain: 0.35 }], [FLOOD, 'light on', 'bell', { pitch: 'D6', gain: 0.28 }], [FLOOD + 0.1, 'flood', 'whoosh', { len: 0.6, gain: 0.3 }],
  [FLOOD + 0.5, 'fix', 'pop', { pitch: 'G5', gain: 0.25 }],
  [16.5, 'to end card', 'whoosh', { len: 0.4, gain: 0.14 }], [17.4, 'ball becomes logo', 'pop', { pitch: 'C6', gain: 0.28 }], [17.9, 'wordmark', 'pop', { pitch: 'G5', gain: 0.22 }],
  [18.85, 'call to action', 'click', { gain: 0.25 }], [19.55, 'arrow', 'tick', { gain: 0.1 }],
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
    ctx.translate(270 + Math.sin(t * 0.9) * 1.6, 480 + Math.cos(t * 0.7) * 1.6);
    ctx.rotate(Math.sin(t * 0.45) * 0.0017); ctx.scale(1.022, 1.022); ctx.translate(-270, -480);
    const bp = ballPos(u);
    sceneLight(ctx, u, bp);
    sceneEnd(ctx, u, IMG);
    const dark = u < FLOOD + 0.4;
    text(ctx, '@aidmsetter.co', 18, 22, font(10, 500, DISPLAY), dark ? '#8A8A8F' : C.mute, 'left', 0.3);
    const m = clamp((u - 17.4) / 0.35, 0, 1);
    drawBall(ctx, bp[0], bp[1], u < FLOOD + 0.8 ? 1.35 : 1, 1 - eo(m));
    ctx.restore();
  },
  post(ctx, u, t) {
    const fi = Math.floor(t * 30 + 0.5), ox = hash01(fi, 3) * 256, oy = hash01(fi, 5) * 256;
    ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = 0.55;
    ctx.translate(ox, oy); ctx.fillStyle = ctx.createPattern(NOISE, 'repeat'); ctx.fillRect(-256, -256, W + 512, H + 512);
    ctx.restore();
    const g = ctx.createRadialGradient(W / 2, H * 0.47, W * 0.55, W / 2, H * 0.47, H * 0.75);
    g.addColorStop(0, 'rgba(20,10,0,0)'); g.addColorStop(1, 'rgba(20,10,0,.2)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  },
});
