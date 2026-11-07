// Renders storyboard.html -> storyboard.jpg + frames/frame_XX.png
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const { chromium } = createRequire(import.meta.url)('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 3820, height: 990 }, deviceScaleFactor: 1 });
await p.goto(pathToFileURL(path.join(here, 'storyboard.html')).href);
await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: path.join(here, 'storyboard.jpg'), type: 'jpeg', quality: 92, fullPage: true });
fs.mkdirSync(path.join(here, 'frames'), { recursive: true });
const fr = await p.$$('.fr');
for (let i = 0; i < fr.length; i++) await fr[i].screenshot({ path: path.join(here, 'frames', `frame_${String(i + 1).padStart(2, '0')}.png`) });
await b.close();
console.log('frames', fr.length);
