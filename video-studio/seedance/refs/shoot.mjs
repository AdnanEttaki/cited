import { createRequire } from 'node:module';
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath, pathToFileURL } from 'node:url';
const { chromium } = createRequire(import.meta.url)('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1024, height: 1280 } });
for (const f of fs.readdirSync(here).filter(f => f.endsWith('.html'))) {
  await p.goto(pathToFileURL(path.join(here, f)).href);
  await p.screenshot({ path: path.join(here, f.replace('.html', '.png')) });
}
await b.close(); console.log('ok');
