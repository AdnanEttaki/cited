"""DMSetter brand palette card. python3 palette.py -> palette.html ; node shoot.mjs -> palette.png"""
import os

here = os.path.dirname(os.path.abspath(__file__))
logo = open(os.path.join(here, "..", "logo", "svg", "mark_primary.svg")).read().replace('width="260" height="260"', 'width="150" height="150"')

COLORS = [
    ("Signal Orange", "#D8541E", "Primary accent: CTAs, highlight boxes, the $50K side, logo cloud", "#fff"),
    ("Ink", "#1B1B1B", "Text, headlines, badges, the $5K side", "#fff"),
    ("Paper", "#F4F0E8", "Backgrounds, cards, light surfaces", "#1B1B1B"),
    ("Teal", "#1E9E95", "Secondary accent: stickers, ✓ states, 'setter' tags", "#fff"),
    ("Amber", "#F2A33A", "Highlights: glowing key message, sparkles, warnings", "#1B1B1B"),
]
SUPPORT = [("Sand", "#ECE6DA"), ("Dune", "#E2DBCD"), ("Stone grey", "#9A9286"), ("Magenta", "#D9257E"), ("Alert red", "#FF3B5C"), ("DM blue", "#3797F0"), ("DM purple", "#A033FF")]


def rgb(h):
    h = h.lstrip("#"); return ", ".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def main_card(n, h, use, fg):
    return (f'<div class="sw" style="background:{h};color:{fg}"><div class="nm">{n}</div>'
            f'<div class="hx">{h}</div><div class="rg">RGB {rgb(h)}</div><p>{use}</p></div>')


html = f'''<!doctype html><html><head><meta charset="utf-8"><title>DMSetter Palette</title><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1600px;padding:60px;font-family:Inter,sans-serif;color:#1B1B1B;background:radial-gradient(120% 90% at 40% 30%,#F4F0E8,#ECE6DA 70%,#E2DBCD)}}
body::before{{content:"";position:fixed;inset:0;z-index:-1;background:repeating-linear-gradient(0deg,rgba(0,0,0,.035) 0 1px,transparent 1px 36px),repeating-linear-gradient(90deg,rgba(0,0,0,.035) 0 1px,transparent 1px 36px)}}
.top{{display:flex;align-items:center;gap:26px;border-bottom:1px solid #1B1B1B;padding-bottom:22px;margin-bottom:34px}}
h1{{font:900 56px Inter;letter-spacing:-.035em}}h1 span{{color:#D8541E}}
.sub{{font:700 15px Inter;letter-spacing:.3em;text-transform:uppercase;color:#6D665B;margin-top:6px}}
.main{{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr 1fr;gap:18px;height:420px}}
.sw{{border-radius:20px;padding:24px;display:flex;flex-direction:column;box-shadow:0 8px 0 rgba(0,0,0,.18),0 24px 40px rgba(70,50,20,.18)}}
.nm{{font:900 26px Inter;letter-spacing:-.02em}}.hx{{font:800 22px Inter;margin-top:auto}}.rg{{font:600 14px Inter;opacity:.75;margin:4px 0 12px}}
.sw p{{font:600 14px/1.4 Inter;opacity:.85}}
h2{{font:900 22px Inter;letter-spacing:-.01em;margin:40px 0 16px}}
.sup{{display:flex;gap:14px}}.s{{flex:1;background:#FBFAF6;border-radius:14px;padding:10px;box-shadow:0 2px 0 #d8d1c3,0 12px 20px rgba(70,50,20,.12)}}
.s i{{display:block;height:70px;border-radius:9px}}.s b{{display:block;font:800 14px Inter;margin-top:8px}}.s small{{font:600 12px Inter;color:#6D665B}}
.row{{display:flex;gap:18px}}.box{{flex:1;background:#FBFAF6;border-radius:18px;padding:24px;box-shadow:0 2px 0 #d8d1c3,0 12px 20px rgba(70,50,20,.12)}}
.t1{{font:900 54px Inter;letter-spacing:-.035em;line-height:1}}.t2{{font:400 30px 'Playfair Display',serif;font-style:italic;margin-top:10px}}
.t3{{font:500 17px/1.5 Inter;color:#6D665B;margin-top:10px}}.lab{{font:800 12px Inter;letter-spacing:.2em;color:#9A9286;margin-bottom:10px}}
.hl{{background:#1B1B1B;color:#fff;padding:0 .12em}}.hlo{{background:#D8541E;color:#fff;padding:0 .12em}}
.ratio{{display:flex;height:34px;border-radius:10px;overflow:hidden;margin-top:12px}}
</style></head><body>
<div class="top">{logo}<div><h1>DM<span>Setter</span> brand palette</h1><div class="sub">Paper · Orange · Ink</div></div></div>
<div class="main">{"".join(main_card(*c) for c in COLORS)}</div>
<h2>Supporting colours</h2>
<div class="sup">{"".join(f'<div class="s"><i style="background:{h}"></i><b>{n}</b><small>{h}</small></div>' for n, h in SUPPORT)}</div>
<h2>Type &amp; usage</h2>
<div class="row">
 <div class="box"><div class="lab">TYPOGRAPHY</div><div class="t1">Inter Black</div><div class="t3">Headlines &amp; captions · weight 800–900 · tight tracking (-3.5%)</div>
  <div class="t1" style="font-size:34px;margin-top:18px">Same DMs. <span class="hlo">Different results.</span></div></div>
 <div class="box"><div class="lab">COLOUR BALANCE</div>
  <div class="ratio"><i style="flex:60;background:#F4F0E8"></i><i style="flex:20;background:#1B1B1B"></i><i style="flex:12;background:#D8541E"></i><i style="flex:5;background:#1E9E95"></i><i style="flex:3;background:#F2A33A"></i></div>
  <div class="t3">60% Paper · 20% Ink · 12% Orange · 5% Teal · 3% Amber.<br>One orange highlight per frame; ink boxes for the second key word.<br>DM blue/purple only inside Instagram-style chat bubbles.</div></div>
</div>
</body></html>'''

if __name__ == "__main__":
    open(os.path.join(here, "palette.html"), "w").write(html)
    print("ok")
