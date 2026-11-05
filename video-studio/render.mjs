// Frame-accurate renderer: drives composition.html in Chromium and encodes with ffmpeg.
// Usage: node render.mjs <project_dir> <format: 916|11|both> [--preview t1,t2,...] [--workers N]
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const [projDir, fmtArg = 'both', ...rest] = process.argv.slice(2);
const opt = (k, d) => { const i = rest.indexOf(k); return i >= 0 ? rest[i + 1] : d; };
const preview = opt('--preview', null);
const WORKERS = +opt('--workers', 4);

const T = JSON.parse(fs.readFileSync(path.join(projDir, 'timeline.json'), 'utf8'));
const build = path.join(here, 'build');
const framesDir = path.join(build, 'frames');
const nRaw = fs.readdirSync(framesDir).filter(f => f.endsWith('.jpg')).length;

// ---- captions from ElevenLabs alignments ----
const cues = JSON.parse(fs.readFileSync(path.join(projDir, 'vo_cues.json'), 'utf8'));
const chunks = [];
for (const c of cues) {
  const a = JSON.parse(fs.readFileSync(path.join(build, 'vo', c.id + '.json'), 'utf8')).alignment;
  const words = []; let cur = '', s = 0, e = 0;
  a.characters.forEach((ch, i) => {
    if (ch === ' ') { if (cur) words.push({ w: cur, t0: c.at + s, t1: c.at + e }); cur = ''; }
    else { if (!cur) s = a.character_start_times_seconds[i]; cur += ch; e = a.character_end_times_seconds[i]; }
  });
  if (cur) words.push({ w: cur, t0: c.at + s, t1: c.at + e });
  let grp = [];
  const flush = () => { if (grp.length) chunks.push({ words: grp, t0: grp[0].t0 - 0.05, t1: grp.at(-1).t1 + 0.35 }); grp = []; };
  words.forEach(w => { grp.push(w); if (/[.,?!]$/.test(w.w) || grp.length >= 3) flush(); });
  flush();
}
chunks.forEach((c, i) => { if (chunks[i + 1] && chunks[i + 1].t0 < c.t1) c.t1 = chunks[i + 1].t0; });
T.chunks = chunks;

const LAYOUTS = {
  916: {
    W: 1080, H: 1920, frameInset: 40,
    type: { x: 90, y: 180, w: 900, h: 440, align: 'center', sans: 128, serif: 82, check: 74 },
    win: { x: 237, y: 650, w: 606, h: 1030, r: 58 },
    cap: { glass: true, style: { left: '50%', top: '1712px', transform: 'translateX(-50%)', fontSize: '40px', whiteSpace: 'nowrap' } },
    label: { left: '50%', top: '120px', transform: 'translateX(-50%)' },
    end: { serif: 110, sans: 200, btn: 44, sub: 22 },
  },
  11: {
    W: 1080, H: 1080, frameInset: 26,
    type: { x: 64, y: 150, w: 350, h: 680, align: 'left', sans: 124, serif: 76, check: 64 },
    win: { x: 453, y: 50, w: 577, h: 980, r: 52 },
    cap: { glass: false, style: { left: '64px', top: '890px', width: '350px', fontSize: '34px', lineHeight: '1.25' } },
    label: { left: '64px', top: '78px' },
    end: { serif: 84, sans: 160, btn: 36, sub: 18 },
  },
};

const frameSrc = t => pathToFileURL(path.join(framesDir, `f${String(Math.min(nRaw, Math.floor(t * T.fps) + 1)).padStart(4, '0')}.jpg`)).href;

async function openPage(browser, L) {
  const page = await browser.newPage({ viewport: { width: L.W, height: L.H }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(path.join(here, 'composition.html')).href);
  await page.evaluate(([t, l]) => window.setup(t, l), [T, L]);
  return page;
}

async function renderFormat(browser, fmt) {
  const L = LAYOUTS[fmt];
  const outDir = path.join(projDir, 'out'); fs.mkdirSync(outDir, { recursive: true });
  if (preview) {
    const page = await openPage(browser, L);
    for (const t of preview.split(',').map(Number)) {
      await page.evaluate(([t, s]) => window.render(t, s), [t, frameSrc(t)]);
      await page.screenshot({ path: path.join(outDir, `preview_${fmt}_${t}.jpg`), type: 'jpeg', quality: 85 });
    }
    await page.close(); return;
  }
  const total = Math.round(T.duration * T.fps), per = Math.ceil(total / WORKERS);
  const segs = await Promise.all([...Array(WORKERS)].map(async (_, w) => {
    const a = w * per, b = Math.min(total, a + per); const seg = path.join(build, `seg_${fmt}_${w}.mp4`);
    const page = await openPage(browser, L);
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(T.fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', seg], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = a; i < b; i++) {
      const t = i / T.fps;
      await page.evaluate(([t, s]) => window.render(t, s), [t, frameSrc(t)]);
      const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (w === 0 && i % 60 === 0) console.log(`[${fmt}] ${Math.round((i - a) / (b - a) * 100)}%`);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); await page.close();
    return seg;
  }));
  const list = path.join(build, `segs_${fmt}.txt`);
  fs.writeFileSync(list, segs.map(s => `file '${s}'`).join('\n'));
  const silent = path.join(build, `video_${fmt}.mp4`);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', silent]);
  console.log('video ->', silent);
}

const browser = await chromium.launch();
for (const f of fmtArg === 'both' ? ['916', '11'] : [fmtArg]) await renderFormat(browser, f);
await browser.close();
