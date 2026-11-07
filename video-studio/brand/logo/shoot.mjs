// Renders sheet.html -> sheet.png and each svg/*.svg -> png/*.png (1024px, transparent where the SVG is)
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const { chromium } = createRequire(import.meta.url)('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1720, height: 900 }, deviceScaleFactor: 1 });
await p.goto(pathToFileURL(path.join(here, 'sheet.html')).href);
await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: path.join(here, 'sheet.png'), fullPage: true });
fs.mkdirSync(path.join(here, 'png'), { recursive: true });
for (const f of fs.readdirSync(path.join(here, 'svg'))) {
  const svg = fs.readFileSync(path.join(here, 'svg', f), 'utf8').replace(/width="\d+" height="\d+"/, 'width="1024" height="1024" preserveAspectRatio="xMidYMid meet"');
  const q = await b.newPage({ viewport: { width: 1024, height: 1024 } });
  await q.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
  await q.evaluate(() => document.fonts.ready);
  await q.locator('svg').screenshot({ path: path.join(here, 'png', f.replace('.svg', '.png')), omitBackground: true });
  await q.close();
}
await b.close();
console.log('ok');
