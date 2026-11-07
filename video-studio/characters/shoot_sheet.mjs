// Renders sheet.html -> sheet.png
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const { chromium } = createRequire(import.meta.url)('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 2160, height: 900 }, deviceScaleFactor: 1 });
await p.goto(pathToFileURL(path.join(here, 'sheet.html')).href);
await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: path.join(here, 'sheet.png'), fullPage: true });
await b.close();
console.log('ok');
