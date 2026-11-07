// Renders video_<hook>.html frame-by-frame -> ../../build/paper_video_<hook>.mp4
// Usage: node render_video.mjs <hook> [--preview t1,t2] [--workers N]
import { createRequire } from 'node:module';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const { chromium } = createRequire(import.meta.url)('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const build = path.join(here, '..', '..', 'build');
const [hook, ...rest] = process.argv.slice(2);
const opt = (k, d) => { const i = rest.indexOf(k); return i >= 0 ? rest[i + 1] : d; };
const T = JSON.parse(fs.readFileSync(path.join(here, `timeline_${hook}.json`), 'utf8'));
const W = +opt('--workers', 4), fps = T.fps, total = Math.round(T.duration * fps);
const url = pathToFileURL(path.join(here, `video_${hook}.html`)).href;

const browser = await chromium.launch();
async function page() {
  const p = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto(url); await p.evaluate(() => window.ready); return p;
}
const preview = opt('--preview', null);
if (preview) {
  const p = await page(); fs.mkdirSync(path.join(here, 'out'), { recursive: true });
  for (const t of preview.split(',').map(Number)) {
    await p.evaluate(t => window.render(t), t);
    await p.screenshot({ path: path.join(here, 'out', `pv_${hook}_${t}.jpg`), type: 'jpeg', quality: 85 });
  }
} else {
  const per = Math.ceil(total / W);
  const segs = await Promise.all([...Array(W)].map(async (_, w) => {
    const a = w * per, b = Math.min(total, a + per), seg = path.join(build, `pseg_${hook}_${w}.mp4`);
    const p = await page();
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', seg], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = a; i < b; i++) {
      await p.evaluate(t => window.render(t), i / fps);
      const buf = await p.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); return seg;
  }));
  const list = path.join(build, `psegs_${hook}.txt`);
  fs.writeFileSync(list, segs.map(s => `file '${s}'`).join('\n'));
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', path.join(build, `paper_video_${hook}.mp4`)]);
  console.log('video ->', path.join(build, `paper_video_${hook}.mp4`));
}
await browser.close();
