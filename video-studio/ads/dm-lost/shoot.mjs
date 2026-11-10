// Renders html/*.html -> out/*.png (1080x1920) and out/sheet.png (all variants side by side)
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const { chromium } = createRequire(import.meta.url)('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
fs.mkdirSync(path.join(here, 'out'), { recursive: true });
const b = await chromium.launch();
const files = fs.readdirSync(path.join(here, 'html')).filter(f => f.endsWith('.html')).sort();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
for (const f of files) {
  await p.goto(pathToFileURL(path.join(here, 'html', f)).href);
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(here, 'out', f.replace('.html', '.png')) });
}
const imgs = files.map(f => `<figure><img src="${pathToFileURL(path.join(here, 'out', f.replace('.html', '.png'))).href}"><figcaption>${f.replace('.html', '').replace('_', ' · ')}</figcaption></figure>`).join('');
const s = await b.newPage({ viewport: { width: files.length * 380 + 40, height: 760 } });
await s.setContent(`<html><body style="margin:0;padding:20px;background:#1a1a1a;display:flex;gap:20px;font-family:Inter">${imgs}</body></html>`.replace(/<figure>/g, '<figure style="margin:0;width:360px">').replace(/<img /g, '<img style="width:360px;border-radius:12px" ').replace(/<figcaption>/g, '<figcaption style="color:#fff;font:700 15px Inter;margin-top:10px">'));
await s.waitForLoadState('load');
await s.screenshot({ path: path.join(here, 'out', 'sheet.png'), fullPage: true });
await b.close();
console.log('ok', files.length);
