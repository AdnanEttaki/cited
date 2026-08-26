#!/usr/bin/env python3
"""Convert snapshot markdown files into styled HTML pages matching the Cited design."""
import html, re, pathlib

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Cited sample snapshot</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,600;1,6..72,500&display=swap" rel="stylesheet">
<style>
  :root{{--bg:#0b0d0b;--panel:#131613;--line:#262b26;--ink:#e8ebe6;--dim:#9aa398;--accent:#c8f04b;--accent-ink:#0b0d0b}}
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{background:var(--bg);color:var(--ink);font-family:Inter,system-ui,sans-serif;line-height:1.65;-webkit-font-smoothing:antialiased}}
  .wrap{{max-width:780px;margin:0 auto;padding:0 24px}}
  nav{{border-bottom:1px solid var(--line)}}
  nav .wrap{{display:flex;align-items:center;justify-content:space-between;height:64px}}
  .logo{{font-family:Newsreader,serif;font-size:24px;font-weight:600;text-decoration:none;color:var(--ink)}}
  .logo em{{color:var(--accent);font-style:normal}}
  .btn{{display:inline-block;background:var(--accent);color:var(--accent-ink);font-weight:600;font-size:15px;padding:12px 22px;border-radius:8px;text-decoration:none}}
  .btn.small{{padding:9px 16px;font-size:14px}}
  article{{padding:64px 0 32px}}
  h1{{font-family:Newsreader,serif;font-weight:500;font-size:clamp(30px,4.6vw,44px);line-height:1.15;margin-bottom:28px}}
  h2{{font-family:Newsreader,serif;font-weight:600;font-size:26px;color:var(--accent);margin:40px 0 14px}}
  h3{{font-size:17px;font-weight:600;margin:28px 0 8px}}
  p{{color:var(--dim);font-size:16px;margin-bottom:14px}}
  strong{{color:var(--ink)}}
  em{{color:var(--ink)}}
  .cta{{border-top:1px solid var(--line);margin-top:56px;padding:48px 0;text-align:center}}
  .cta p{{margin-bottom:24px}}
  footer{{border-top:1px solid var(--line);padding:28px 0;font-size:13px;color:var(--dim)}}
</style>
</head>
<body>
<nav><div class="wrap">
  <a class="logo" href="../">Cited<em>.</em></a>
  <a class="btn small" href="../#pricing">Get your audit — $950</a>
</div></nav>
<article><div class="wrap">
{body}
</div></article>
<div class="cta"><div class="wrap">
  <p>This is the free 5-question teaser. The full audit measures 50 buyer questions across ChatGPT, Perplexity, Gemini and Google AI Overviews — with a page-by-page fix list and 30-day plan.</p>
  <a class="btn" href="mailto:adnanettaki6@gmail.com?subject=AI%20Visibility%20Audit%20—%20my%20store">Start your audit — $950</a>
</div></div>
<footer><div class="wrap">Cited. — AI Visibility Audits for e-commerce brands</div></footer>
</body>
</html>
"""

def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\w)\*([^*\n]+?)\*(?!\w)", r"<em>\1</em>", s)
    return s

def convert(md):
    out, para = [], []
    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()
    for line in md.splitlines():
        line = line.rstrip()
        if not line:
            flush(); continue
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            flush()
            level = len(m.group(1))
            out.append(f"<h{level}>" + inline(m.group(2)) + f"</h{level}>")
        else:
            para.append(line)
    flush()
    return "\n".join(out)

src = pathlib.Path(__file__).parent / "snapshots"
dst = pathlib.Path(__file__).parent / "samples"
dst.mkdir(exist_ok=True)
for f in sorted(src.glob("*.md")):
    md = f.read_text(encoding="utf-8")
    title = re.search(r"^#\s+(.*)$", md, re.M).group(1)
    body = convert(md)
    page = TEMPLATE.format(title=html.escape(title), desc=html.escape(title + " — real ChatGPT citation data from Cited."), body=body)
    out = dst / (f.stem + ".html")
    out.write_text(page, encoding="utf-8")
    print("built", out.name)
