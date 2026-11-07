"""DMSetter logo: cloud mascot with eyes + paper-plane DM arrow, in the paper-video branding.
python3 logo.py -> sheet.html + svg/*.svg ; node shoot.mjs -> sheet.png + png/*.png"""
import os

here = os.path.dirname(os.path.abspath(__file__))
INK, ORANGE, CREAM, TEAL, AMBER, SHADOW = "#1B1B1B", "#D8541E", "#F4F0E8", "#1E9E95", "#F2A33A", "#5A3C1E"

# puffy cloud built from circles (same look as a Youri-style blob)
CLOUD = [(70, 118, 44), (112, 86, 52), (162, 96, 46), (190, 132, 38), (128, 140, 50), (82, 150, 36), (170, 156, 34)]


def cloud(fill, stroke=None, dx=0, dy=0):
    circles = "".join(f'<circle cx="{x + dx}" cy="{y + dy}" r="{r}"/>' for x, y, r in CLOUD)
    base = f'<rect x="{46 + dx}" y="{126 + dy}" width="{168}" height="{58}" rx="29"/>'
    if stroke:  # outline: draw stroked shapes, then fill on top to hide inner seams
        return (f'<g fill="{stroke}" stroke="{stroke}" stroke-width="12" stroke-linejoin="round">{circles}{base}</g>'
                f'<g fill="{fill}">{circles}{base}</g>')
    return f'<g fill="{fill}">{circles}{base}</g>'


def eyes(color=INK, look=0):
    return (f'<rect x="{112 + look}" y="96" width="15" height="30" rx="7.5" fill="{color}" transform="rotate(-10 {119 + look} 111)"/>'
            f'<rect x="{144 + look}" y="96" width="15" height="30" rx="7.5" fill="{color}" transform="rotate(-10 {151 + look} 111)"/>')


def plane(color="#fff", fold="#C9D3E3"):
    """Generic paper plane (send arrow), drawn in a 0..40 box."""
    return (f'<path d="M3 19 L37 4 L27 36 L19 24 Z" fill="{color}" stroke="{color}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<path d="M19 24 L37 4" stroke="{fold}" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M19 24 L19 33 L24 28" fill="{fold}"/>')


def badge(bg, plane_col="#fff", fold=None, cx=200, cy=172, r=34, ring=CREAM):
    fold = fold or ("#F2C8A8" if bg == ORANGE else "#C9D3E3")
    return (f'<circle cx="{cx}" cy="{cy + 4}" r="{r + 6}" fill="{SHADOW}" opacity=".22"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 6}" fill="{ring}"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}"/>'
            f'<g transform="translate({cx - 21} {cy - 21}) scale(1.05)">{plane(plane_col, fold)}</g>')


def mark(cloud_fill=ORANGE, eye=INK, badge_bg=INK, outline=None, trail=False, size=260):
    shadow = cloud(SHADOW, dx=0, dy=7).replace(f'fill="{SHADOW}"', f'fill="{SHADOW}" opacity=".22"', 1)
    body = cloud(cloud_fill, outline)
    tr = ""
    if trail:  # dotted flight path from the cloud to the plane badge (nod to the carousel 'DM' trail)
        tr = f'<path d="M60 205 C 90 245, 150 240, 176 196" fill="none" stroke="{INK}" stroke-width="4" stroke-dasharray="1 10" stroke-linecap="round"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="20 30 240 230" width="{size}" height="{size * 230 / 240:.0f}">'
            f'{shadow}{body}{eyes(eye)}{tr}{badge(badge_bg)}</svg>')


def app_icon(bg=CREAM, cloud_fill=ORANGE, badge_bg=INK, eye=INK, size=220):
    inner = mark(cloud_fill, eye, badge_bg)[mark(cloud_fill, eye, badge_bg).index('>') + 1:-6]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" width="{size}" height="{size}">'
            f'<rect width="300" height="300" rx="66" fill="{bg}"/>'
            f'<g transform="translate(18 22)">{inner}</g></svg>')


def wordmark(dark=False, size=520):
    ink = CREAM if dark else INK
    inner = mark()[mark().index('>') + 1:-6]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 230" width="{size}" height="{size * 230 / 640:.0f}">'
            f'<g transform="translate(-20 -20)">{inner}</g>'
            f'<text x="262" y="138" font-family="Inter" font-weight="900" font-size="78" letter-spacing="-3.5" fill="{ink}">DM<tspan fill="{ORANGE}">Setter</tspan></text>'
            f'<text x="266" y="174" font-family="Inter" font-weight="700" font-size="17" letter-spacing="5" fill="{ink}" opacity=".6">YOUR DMs, HANDLED.</text></svg>')


VARIANTS = [
    ("primary", "Primary · orange cloud, ink send badge", mark()),
    ("outline", "Paper outline · cream cloud, orange badge", mark(CREAM, INK, ORANGE, outline=INK)),
    ("trail", "With flight trail", mark(trail=True)),
    ("teal", "Accent · teal badge", mark(ORANGE, INK, TEAL)),
]
ICONS = [("icon_light", app_icon()), ("icon_dark", app_icon(INK, ORANGE, ORANGE, INK)), ("icon_orange", app_icon(ORANGE, CREAM, INK, INK))]


def sheet():
    cards = "".join(f'<div class="card"><div class="pad">{svg}</div><b>{label}</b></div>' for _, label, svg in VARIANTS)
    icons = "".join(f'<div class="ic">{svg}<b>{n.replace("icon_", "").title()} icon</b></div>' for n, svg in ICONS)
    return f'''<!doctype html><html><head><meta charset="utf-8"><title>DMSetter Logo</title><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1720px;padding:56px;font-family:Inter,sans-serif;color:{INK};background:radial-gradient(120% 90% at 40% 40%,#F4F0E8,#ECE6DA 70%,#E2DBCD)}}
body::before{{content:"";position:fixed;inset:0;z-index:-1;background:repeating-linear-gradient(0deg,rgba(0,0,0,.035) 0 1px,transparent 1px 36px),repeating-linear-gradient(90deg,rgba(0,0,0,.035) 0 1px,transparent 1px 36px)}}
h1{{font:900 46px Inter;letter-spacing:-.03em}}h1 span{{color:{ORANGE}}}
.lead{{font:600 17px Inter;color:#6D665B;border-top:1px solid {INK};padding-top:12px;margin:10px 0 30px}}
.row{{display:flex;gap:22px;margin-bottom:28px}}
.card{{flex:1;background:#FBFAF6;border-radius:20px;padding:16px 16px 18px;box-shadow:0 2px 0 #d8d1c3,0 18px 30px rgba(70,50,20,.15);text-align:center}}
.card .pad{{background:#F1ECE2;border-radius:14px;padding:18px 0;display:flex;justify-content:center}}
b{{display:block;font:800 14px Inter;margin-top:12px}}
.wm{{display:flex;gap:22px}}.wm>div{{flex:1;border-radius:20px;padding:34px;display:flex;align-items:center;justify-content:center;box-shadow:0 18px 30px rgba(70,50,20,.15)}}
.wm .l{{background:#FBFAF6}}.wm .d{{background:{INK}}}
.ics{{display:flex;gap:30px;align-items:flex-end}}.ic{{text-align:center}}.ic svg{{filter:drop-shadow(0 14px 22px rgba(70,50,20,.25))}}
.pal{{display:flex;gap:12px;margin-left:auto}}.pal i{{width:70px;height:70px;border-radius:14px;box-shadow:0 4px 0 rgba(0,0,0,.18);display:flex;align-items:flex-end;padding:6px;font:800 10px Inter;color:#fff;font-style:normal}}
</style></head><body>
<h1>DM<span>Setter</span> · logo system</h1>
<p class="lead">Cloud mascot with eyes + paper-plane send arrow. Cut-paper shadow, same palette and type as the videos.</p>
<div class="row">{cards}</div>
<div class="wm row"><div class="l">{wordmark()}</div><div class="d">{wordmark(True)}</div></div>
<div class="row ics">{icons}<div class="pal"><i style="background:{ORANGE}">#D8541E</i><i style="background:{INK}">#1B1B1B</i><i style="background:{CREAM};color:{INK}">#F4F0E8</i><i style="background:{TEAL}">#1E9E95</i><i style="background:{AMBER}">#F2A33A</i></div></div>
</body></html>'''


if __name__ == "__main__":
    os.makedirs(os.path.join(here, "svg"), exist_ok=True)
    for n, _, svg in VARIANTS: open(os.path.join(here, "svg", f"mark_{n}.svg"), "w").write(svg)
    for n, svg in ICONS: open(os.path.join(here, "svg", f"{n}.svg"), "w").write(svg)
    open(os.path.join(here, "svg", "wordmark_light.svg"), "w").write(wordmark())
    open(os.path.join(here, "svg", "wordmark_dark.svg"), "w").write(wordmark(True))
    open(os.path.join(here, "sheet.html"), "w").write(sheet())
    print("ok")
