// Renders palette.html -> palette.png
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const { chromium } = createRequire(import.meta.url)('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
await p.goto(pathToFileURL(path.join(here, 'palette.html')).href);
await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: path.join(here, 'palette.png'), fullPage: true });
await b.close();
console.log('ok');
