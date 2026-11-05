// FX layer: visual hooks, 3D phone, pop-out chat cards, camera shake, shockwave rings, particle bursts.
// Data-driven from timeline.json: hook, pops, shakes, bursts.
(function () {
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const lerp = (a, b, k) => a + (b - a) * k;
  const prog = (t, t0, d) => clamp((t - t0) / d);
  const expoOut = x => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x));
  const backOut = x => { const c = 1.6; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
  const cubicIn = x => x * x * x;
  // deterministic random
  const rnd = seed => () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646;

  let T, L, $, fx, cv, ctx, pops = [], notifs = [], badge, particles = {};

  const NOTIFS = ['how much is it?', 'are you still taking clients?', 'price??', 'is this a bot?', "what's the cost?",
    'can we hop on a call', 'u there?', 'interested!!', 'how does it work?', 'DM me the price', 'is it worth it?',
    'do you do payment plans?', 'hello??', 'saw your post 🔥', 'how fast can I start?', 'still available?'];

  function esc(s) { return s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c])); }
  function mark(text, hl = []) {
    let h = esc(text);
    hl.forEach(x => { h = h.replace(esc(x), `<mark>${esc(x)}</mark>`); });
    return h;
  }

  window.FX = {
    async setup(timeline, layout, refs) {
      T = timeline; L = layout; $ = refs; fx = document.getElementById('fx');
      cv = document.getElementById('burst'); cv.width = L.W; cv.height = L.H; ctx = cv.getContext('2d');
      fx.innerHTML = ''; pops = []; notifs = [];
      const P = L.pop;
      (T.pops || []).forEach(p => {
        const el = document.createElement('div');
        el.className = 'pop ' + p.side;
        el.style.width = P.w + 'px'; el.style.fontSize = P.font + 'px';
        el.innerHTML = `<div class="who"><i></i>${p.side === 'ai' ? 'AI setter' : 'The lead'}</div>${mark(p.text, p.hl)}`;
        fx.appendChild(el); pops.push({ ...p, el });
      });
      if (T.hook && T.hook.mode === 'storm') {
        const r = rnd(7), w = L.win, N = L.storm.n;
        for (let i = 0; i < N; i++) {
          const el = document.createElement('div'); el.className = 'notif';
          el.style.width = L.storm.w + 'px'; el.style.fontSize = L.storm.font + 'px';
          el.innerHTML = `<b class="app"></b><div><div class="ttl">New message <span>now</span></div><div class="msg">${NOTIFS[i % NOTIFS.length]}</div></div>`;
          fx.appendChild(el);
          notifs.push({ el, at: -0.4 + i * 0.065, x: w.x - 40 + r() * (w.w - L.storm.w + 80), y: w.y + 40 + r() * (w.h - 260), rot: (r() - 0.5) * 12, dir: r() > 0.5 ? 1 : -1 });
        }
        badge = document.createElement('div'); badge.className = 'badge'; badge.style.fontSize = L.storm.font * 1.15 + 'px'; fx.appendChild(badge);
      }
      // particle sets
      (T.bursts || []).forEach((b, bi) => {
        const r = rnd(101 + bi * 13), arr = [];
        if (b.sparks) for (let i = 0; i < 70; i++) {
          const a = r() * Math.PI * 2, sp = 500 + r() * 1300;
          arr.push({ vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - 300, s: 2 + r() * 5, c: r() > 0.4 ? '#3D8BFF' : (r() > 0.5 ? '#FFFFFF' : '#C9D3E3'), life: 0.7 + r() * 0.7 });
        }
        particles[bi] = arr;
      });
    },

    // phone window modifiers
    win(t) {
      const m = { tx: 0, ty: 0, rot: 0, rx: 0, ry: 0, s: 1, op: 1, dim: 1, blur: 0, override: false };
      // 3D float
      m.ry = 5 * Math.sin(t * 0.35); m.rx = 3 * Math.cos(t * 0.27);
      // shake
      (T.shakes || []).forEach(([at, amp], i) => {
        const d = t - at; if (d < 0 || d > 0.6) return; const k = amp * Math.exp(-7 * d);
        m.tx += k * Math.sin(d * 83 + i); m.ty += k * Math.cos(d * 71 + i * 2); m.rot += k * 0.06 * Math.sin(d * 57);
      });
      // slam hook: phone falls from the camera
      if (T.hook && T.hook.mode === 'slam') {
        const p = prog(t, -0.45, 0.57), e = cubicIn(p);
        m.override = true; m.s *= lerp(2.6, 1, e); m.rx += lerp(48, 0, e); m.ty += lerp(-260, 0, e); m.op = clamp(p * 4);
        m.blur += (1 - p) * 6 * (p > 0 ? 1 : 0);
      }
      // dim + push back while a pop card is up
      let up = 0; pops.forEach(p => { up = Math.max(up, Math.min(expoOut(prog(t, p.t0, 0.4)), 1 - prog(t, p.t1, 0.3))); });
      if (T.hook && T.hook.mode === 'storm') { up = Math.max(up, 1 - prog(t, 1.15, 0.45)) * 0.85; }
      m.dim = lerp(1, 0.42, up); m.blur += up * 3; m.s *= lerp(1, 0.96, up);
      return m;
    },

    render(t) {
      const W = L.W, H = L.H, w = L.win, cx = w.x + w.w / 2, cy = w.y + w.h / 2;
      // pop cards
      pops.forEach((p, i) => {
        const inP = prog(t, p.t0, p.enter === 'macro' ? 0.75 : 0.5), outP = prog(t, p.t1, 0.28);
        const vis = t >= p.t0 - 0.02 && outP < 1; p.el.style.display = vis ? 'block' : 'none'; if (!vis) return;
        const e = p.enter === 'macro' ? expoOut(inP) : backOut(inP);
        const tilt = (i % 2 ? 2 : -2) + Math.sin(t * 1.3) * 0.6;
        let s = p.enter === 'macro' ? lerp(1.55, 1, e) : lerp(0.55, 1, e);
        s *= lerp(1, 0.85, outP);
        const rx = p.enter === 'macro' ? 0 : lerp(38, 0, expoOut(inP));
        const y = cy + (p.dy || 0) + lerp(p.enter === 'macro' ? 0 : 140, 0, expoOut(inP)) + Math.sin(t * 1.7) * 6 - outP * 60;
        const h = p.el.offsetHeight;
        p.el.style.transform = `translate(${cx - L.pop.w / 2 + (p.side === 'ai' ? -L.pop.shift : L.pop.shift)}px,${y - h / 2}px) perspective(1600px) rotateX(${rx}deg) rotate(${tilt}deg) scale(${s})`;
        p.el.style.opacity = (p.enter === 'macro' ? 1 : clamp(inP * 3)) * (1 - outP);
        p.el.style.filter = `blur(${(p.enter === 'macro' ? (1 - expoOut(inP)) * 4 : 0) + outP * 8}px)`;
        const hp = expoOut(prog(t, p.t0 + (p.enter === 'macro' ? -0.05 : 0.35), 0.45));
        p.el.querySelectorAll('mark').forEach(mk => mk.style.backgroundSize = `${hp * 100}% 100%`);
      });
      // notification storm
      if (notifs.length) {
        let landed = 0;
        notifs.forEach((n, i) => {
          const p = prog(t, n.at, 0.32), out = prog(t, 1.12 + (n.y - w.y) / w.h * 0.3, 0.38);
          if (p > 0) landed++;
          const vis = p > 0 && out < 1; n.el.style.display = vis ? 'flex' : 'none'; if (!vis) return;
          const e = backOut(p), oe = out * out;
          n.el.style.transform = `translate(${n.x + oe * n.dir * W}px,${lerp(n.y - 420, n.y, e)}px) rotate(${n.rot * e + oe * n.dir * 25}deg) scale(${lerp(1.25, 1, e)})`;
          n.el.style.opacity = clamp(p * 4) * (1 - out);
          n.el.classList.toggle('done', out > 0);
        });
        const cleared = prog(t, 1.15, 0.6), bv = t < 2.2;
        badge.style.display = bv ? 'flex' : 'none';
        if (bv) {
          const n = cleared > 0 ? Math.round(lerp(landed * 3, 0, expoOut(cleared))) : landed * 3;
          badge.textContent = n > 0 ? n : '✓';
          badge.classList.toggle('zero', n === 0);
          badge.style.transform = `translate(${w.x + w.w - 70}px,${w.y - 50}px) scale(${1 + 0.18 * Math.max(0, Math.sin(t * 30)) * (t < 1.1 ? 1 : 0)})`;
          badge.style.opacity = 1 - prog(t, 1.8, 0.4);
        }
      }
      // rings + sparks
      ctx.clearRect(0, 0, W, H);
      (T.bursts || []).forEach((b, bi) => {
        const d = t - b.at; if (d < 0 || d > 1.6) return;
        let ox = cx, oy = cy;
        if (b.el === 'btn') { const r = document.getElementById('btn').getBoundingClientRect(); ox = r.x + r.width / 2; oy = r.y + r.height / 2; }
        if (b.ring) for (let k = 0; k < 2; k++) {
          const p = clamp((d - k * 0.09) / 0.75); if (p <= 0 || p >= 1) continue;
          ctx.beginPath(); ctx.arc(ox, oy, expoOut(p) * W * 0.62, 0, Math.PI * 2);
          ctx.strokeStyle = k ? `rgba(255,255,255,${(1 - p) * 0.5})` : `rgba(61,139,255,${(1 - p) * 0.9})`;
          ctx.lineWidth = lerp(k ? 4 : 14, 0.5, p); ctx.shadowColor = '#0069FF'; ctx.shadowBlur = 30; ctx.stroke();
        }
        ctx.shadowBlur = 12;
        (particles[bi] || []).forEach(q => {
          if (d > q.life) return; const a = 1 - d / q.life;
          const x = ox + q.vx * d * (1 - d * 0.35), y = oy + q.vy * d * (1 - d * 0.35) + 900 * d * d;
          ctx.globalAlpha = a; ctx.fillStyle = q.c; ctx.shadowColor = q.c;
          ctx.beginPath(); ctx.arc(x, y, q.s * (0.6 + a * 0.6), 0, Math.PI * 2); ctx.fill();
        });
        ctx.globalAlpha = 1; ctx.shadowBlur = 0;
      });
    },
  };
})();
