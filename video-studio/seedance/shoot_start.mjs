// Renders start/*.html -> start/*.png (1080x1920)
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const { chromium } = createRequire(import.meta.url)('playwright');
const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), 'start');
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html'))) {
  await p.goto(pathToFileURL(path.join(dir, f)).href);
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(dir, f.replace('.html', '.png')) });
}
await b.close();
console.log('ok');
