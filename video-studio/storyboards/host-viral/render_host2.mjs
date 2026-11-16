// Motion-blur renderer: 4 sub-frames per output frame (120fps -> tmix -> 30fps). Usage: node render_host2.mjs [--preview t1,t2] [--workers 4]
import { createRequire } from 'node:module';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const { chromium } = createRequire(import.meta.url)('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const build = path.join(here, '..', '..', 'build');
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const T = JSON.parse(fs.readFileSync(path.join(here, 'timeline_host2.json'), 'utf8'));
const W = +opt('--workers', 4), fps = T.fps, total = Math.round(T.duration * fps), SUB = 4;
const url = pathToFileURL(path.join(here, 'host2.html')).href;
const browser = await chromium.launch();
const page = async () => { const p = await browser.newPage({ viewport: { width: 1080, height: 1920 } }); await p.goto(url); await p.evaluate(() => window.ready); return p; };
const preview = opt('--preview', null);
if (preview) {
  const p = await page(); fs.mkdirSync(path.join(here, 'out'), { recursive: true });
  for (const t of preview.split(',').map(Number)) { await p.evaluate(t => window.render(t), t); await p.screenshot({ path: path.join(here, 'out', `pv2_${t}.jpg`), type: 'jpeg', quality: 88 }); }
} else {
  const per = Math.ceil(total / W);
  const segs = await Promise.all([...Array(W)].map(async (_, w) => {
    const a = w * per, b = Math.min(total, a + per), seg = path.join(build, `h2seg_${w}.mp4`);
    if (a >= b) return null;
    const p = await page();
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps * SUB), '-c:v', 'mjpeg', '-i', '-',
      '-vf', `tmix=frames=${SUB}:weights='1 1 1 1',select='eq(mod(n\\,${SUB})\\,${SUB - 1})',setpts=N/(${fps}*TB)`,
      '-r', String(fps), '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', seg], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = a; i < b; i++) for (let k = 0; k < SUB; k++) {
      const t = (i + (k + 0.5) / SUB - 0.5) / fps;
      await p.evaluate(t => window.render(Math.max(0, t)), t);
      const buf = await p.screenshot({ type: 'jpeg', quality: 93 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); return seg;
  }));
  const ok = segs.filter(Boolean);
  const list = path.join(build, 'h2segs.txt');
  fs.writeFileSync(list, ok.map(s => `file '${s}'`).join('\n'));
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', path.join(build, 'host2_video.mp4')]);
  console.log('video ->', path.join(build, 'host2_video.mp4'));
}
await browser.close();
