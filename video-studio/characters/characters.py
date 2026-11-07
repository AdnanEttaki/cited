"""Paper cut-out characters for the $5K vs $50K coach video.
char_svg(who, expr) -> inline SVG (viewBox 240x300). who: 'low' ($5K coach, man) | 'high' ($50K coach, woman)
python3 characters.py -> sheet.html (render with shoot_sheet.mjs)"""
import os

here = os.path.dirname(os.path.abspath(__file__))
INK, ORANGE, CREAM, AMBER, TEAL = "#1B1B1B", "#D8541E", "#F4F0E8", "#F2A33A", "#1E9E95"

LOW = dict(skin="#E7B48E", skin_d="#C98E68", hair="#3B2A20", top="#6B6862", top_d="#55524D")
HIGH = dict(skin="#F2C8A8", skin_d="#D9A07F", hair="#E6BC5C", hair_d="#C2933A", top=ORANGE, top_d="#A93F14")

EXPR = {
    "low": ["tired", "stressed", "asleep", "panic", "confused", "2am"],
    "high": ["calm", "coffee", "focused", "happy", "asleep", "thumbs"],
}
LABEL = {"tired": "Tired (default)", "stressed": "Stressed · 50 DMs", "asleep": "Asleep on desk", "panic": "Panic · cost question",
         "confused": "Confused · left on Seen", "2am": "2 AM, red eyes", "calm": "Calm (default)", "coffee": "Coffee sip",
         "focused": "Typing a question", "happy": "Happy nod", "asleep_h": "Asleep peacefully", "thumbs": "Thumbs up · CTA"}


def eyes(c, kind, x1=100, x2=140, y=125):
    if kind == "closed":
        return "".join(f'<path d="M{x-9} {y} q9 7 18 0" stroke="{INK}" stroke-width="3.2" fill="none" stroke-linecap="round"/>' for x in (x1, x2))
    if kind == "happy":
        return "".join(f'<path d="M{x-9} {y+3} q9 -9 18 0" stroke="{INK}" stroke-width="3.4" fill="none" stroke-linecap="round"/>' for x in (x1, x2))
    big = kind == "wide"
    rx, ry, pr = (11, 13, 4) if big else (9, 10, 4.6)
    sclera = "#FFD9D2" if kind == "red" else "#FFFFFF"
    dy = 3 if kind == "down" else 0
    out = ""
    for x in (x1, x2):
        out += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{sclera}"/>'
        if kind == "red":
            out += f'<path d="M{x-8} {y-2} l5 2 M{x+8} {y+1} l-5 -1" stroke="#E0533A" stroke-width="1.2"/>'
        out += f'<circle cx="{x}" cy="{y+dy}" r="{pr}" fill="{INK}"/><circle cx="{x+1.6}" cy="{y-1.6+dy}" r="1.4" fill="#fff"/>'
        if kind in ("tired", "red"):  # heavy lids
            out += f'<path d="M{x-rx-1} {y-2} Q{x} {y-ry-1} {x+rx+1} {y-2} L{x+rx+1} {y-ry-3} L{x-rx-1} {y-ry-3} Z" fill="{c["skin"]}"/>'
            out += f'<path d="M{x-rx} {y-2} Q{x} {y-6} {x+rx} {y-2}" stroke="{c["skin_d"]}" stroke-width="2" fill="none"/>'
    return out


def brows(kind, x1=100, x2=140, y=107):
    d = {"flat": (0, 0, 0, 0), "worried": (4, -3, -3, 4), "angryup": (-2, 3, 3, -2), "raised": (0, 0, -6, -6),
         "high": (-5, -5, -5, -5), "soft": (1, -1, -1, 1)}[kind]
    a, b, c_, e = d
    return (f'<path d="M{x1-11} {y+a} L{x1+9} {y+b}" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>'
            f'<path d="M{x2-9} {y+c_} L{x2+11} {y+e}" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>')


def mouth(kind, lip=None):
    col = lip or INK
    return {
        "flat": f'<path d="M110 157 L131 156" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>',
        "frown": f'<path d="M108 160 Q120 150 132 160" stroke="{INK}" stroke-width="3.5" fill="none" stroke-linecap="round"/>',
        "wavy": f'<path d="M106 158 q4 -4 8 0 t8 0 t8 0 t8 0" stroke="{INK}" stroke-width="3.2" fill="none" stroke-linecap="round"/>',
        "o": f'<ellipse cx="120" cy="160" rx="8" ry="10" fill="{INK}"/><ellipse cx="120" cy="164" rx="5" ry="4" fill="#B5473A"/>',
        "side": f'<path d="M110 158 Q122 154 133 151" stroke="{INK}" stroke-width="3.5" fill="none" stroke-linecap="round"/>',
        "smile": f'<path d="M106 153 Q120 166 134 153" stroke="{col}" stroke-width="4" fill="none" stroke-linecap="round"/>',
        "grin": f'<path d="M104 151 Q120 172 136 151 Z" fill="{INK}"/><path d="M107 152 L133 152 L131 157 L109 157 Z" fill="#fff"/>',
        "sleep": f'<path d="M113 157 Q120 161 127 157" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>',
    }[kind]


def extras_svg(items):
    out = ""
    for it in items:
        if it == "sweat":
            out += f'<path d="M176 92 q7 12 0 18 q-7 -6 0 -18z" fill="#7FC8F2" stroke="#3E8FC2" stroke-width="1.5"/>'
        if it == "sweat2":
            out += f'<path d="M60 96 q6 10 0 15 q-6 -5 0 -15z" fill="#7FC8F2" stroke="#3E8FC2" stroke-width="1.5"/>'
        if it == "zzz":
            out += f'<text x="168" y="70" font-family="Inter" font-weight="900" font-size="26" fill="{INK}">Z</text><text x="190" y="48" font-family="Inter" font-weight="900" font-size="18" fill="{INK}">z</text><text x="205" y="32" font-family="Inter" font-weight="900" font-size="13" fill="{INK}">z</text>'
        if it == "zzz_soft":
            out += f'<text x="172" y="68" font-family="Inter" font-weight="900" font-size="22" fill="{ORANGE}">z</text><text x="192" y="48" font-family="Inter" font-weight="900" font-size="15" fill="{ORANGE}">z</text>'
        if it == "q":
            out += f'<g transform="translate(176 40) rotate(8)"><rect x="0" y="0" width="40" height="40" rx="12" fill="#fff" stroke="{INK}" stroke-width="3"/><path d="M8 38 l-6 10 l14 -8" fill="#fff" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><text x="12" y="31" font-family="Inter" font-weight="900" font-size="28" fill="{ORANGE}">?</text></g>'
        if it == "moon":
            out += f'<path d="M30 40 a16 16 0 1 0 18 22 a13 13 0 1 1 -18 -22z" fill="{AMBER}"/>'
        if it == "buzz":
            out += f'<g transform="translate(168 196) rotate(-12)"><rect x="0" y="0" width="34" height="58" rx="7" fill="{INK}"/><rect x="4" y="6" width="26" height="44" rx="3" fill="#3797F0"/></g><path d="M162 196 l-8 -6 M160 212 l-10 0 M206 196 l8 -6 M208 212 l10 0" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><circle cx="200" cy="196" r="10" fill="#FF3B5C"/><text x="194" y="201" font-family="Inter" font-weight="900" font-size="12" fill="#fff">50</text>'
        if it == "coffee":
            out += (f'<path d="M162 186 q-6 -12 2 -20 q8 -8 0 -18" stroke="#B9AFA0" stroke-width="3" fill="none" stroke-linecap="round"/>'
                    f'<path d="M150 194 h40 l-5 50 h-30 z" fill="#FBFAF6" stroke="{INK}" stroke-width="2.5"/><rect x="152" y="206" width="36" height="12" fill="{ORANGE}"/>'
                    f'<path d="M190 204 q14 0 12 14 q-2 12 -14 10" stroke="{INK}" stroke-width="2.5" fill="none"/>'
                    f'<ellipse cx="162" cy="248" rx="16" ry="12" fill="{HIGH["skin"]}"/>')
        if it == "type":
            out += f'<g transform="translate(150 214) rotate(8)"><rect x="0" y="0" width="38" height="62" rx="8" fill="{INK}"/><rect x="4" y="6" width="30" height="46" rx="3" fill="#3797F0"/><rect x="8" y="14" width="18" height="6" rx="3" fill="#fff"/><rect x="8" y="26" width="22" height="6" rx="3" fill="#A033FF"/></g><ellipse cx="160" cy="276" rx="14" ry="10" fill="{HIGH["skin"]}"/>'
        if it == "thumb":
            out += (f'<g transform="translate(160 200)"><rect x="0" y="22" width="36" height="34" rx="12" fill="{HIGH["skin"]}"/>'
                    f'<rect x="10" y="-4" width="13" height="34" rx="6.5" fill="{HIGH["skin"]}"/><path d="M4 32 h20 M4 41 h20" stroke="{HIGH["skin_d"]}" stroke-width="2"/></g>')
        if it == "sparkle":
            out += f'<path d="M44 60 l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4 l10 -4z" fill="{AMBER}"/><path d="M196 92 l3 7 l7 3 l-7 3 l-3 7 l-3 -7 l-7 -3 l7 -3z" fill="{AMBER}"/>'
    return out


SPEC = {  # expr: (eyes, brows, mouth, extras, head tilt)
    "tired": ("tired", "flat", "flat", [], 0), "stressed": ("tired", "worried", "wavy", ["sweat", "buzz"], -3),
    "asleep": ("closed", "flat", "sleep", ["zzz"], 18), "panic": ("wide", "high", "o", ["sweat", "sweat2"], 0),
    "confused": ("normal", "raised", "side", ["q"], 6), "2am": ("red", "worried", "frown", ["moon", "buzz"], -2),
    "calm": ("normal", "soft", "smile", [], 0), "coffee": ("happy", "soft", "smile", ["coffee"], -4),
    "focused": ("down", "soft", "smile", ["type"], 4), "happy": ("happy", "high", "grin", ["sparkle"], -6),
    "thumbs": ("happy", "soft", "grin", ["thumb", "sparkle"], 0),
}


def low_body(c):
    return (f'<g filter="url(#cut)"><path d="M28 300 C34 226 70 200 120 200 C170 200 206 226 212 300 Z" fill="{c["top"]}"/>'
            f'<ellipse cx="120" cy="205" rx="50" ry="17" fill="{c["top_d"]}"/>'
            f'<path d="M108 212 L104 252 M132 212 L136 252" stroke="#E9E4DA" stroke-width="3" stroke-linecap="round"/>'
            f'<rect x="88" y="260" width="64" height="30" rx="10" fill="{c["top_d"]}"/></g>'
            f'<rect x="106" y="168" width="28" height="36" rx="8" fill="{c["skin_d"]}"/>')


def low_head(c, e, b, m, x):
    return (f'<g filter="url(#cut)"><circle cx="68" cy="128" r="10" fill="{c["skin_d"]}"/><circle cx="172" cy="128" r="10" fill="{c["skin_d"]}"/>'
            f'<ellipse cx="120" cy="122" rx="52" ry="60" fill="{c["skin"]}"/></g>'
            f'<path d="M98 140 q-6 4 0 6 M142 140 q6 4 0 6" stroke="{c["skin_d"]}" stroke-width="2" fill="none" opacity=".7"/>'
            f'<path d="M118 132 q-4 12 4 13" stroke="{c["skin_d"]}" stroke-width="3" fill="none" stroke-linecap="round"/>'
            f'<g filter="url(#cut)"><path d="M66 112 C58 70 90 48 120 50 C156 48 184 72 175 114 L166 96 L158 110 L150 88 L140 104 L128 84 L118 102 L106 86 L96 104 L86 90 L78 108 Z" fill="{c["hair"]}"/></g>'
            + eyes(c, e) + brows(b) + mouth(m))


def high_body(c):
    return (f'<g filter="url(#cut)"><path d="M26 300 C32 226 70 200 120 200 C170 200 208 226 214 300 Z" fill="{c["top"]}"/>'
            f'<path d="M96 204 L120 262 L144 204 Z" fill="{CREAM}"/>'
            f'<path d="M96 204 L84 236 L106 232 L120 262 Z M144 204 L156 236 L134 232 L120 262 Z" fill="{c["top_d"]}"/></g>'
            f'<rect x="106" y="168" width="28" height="38" rx="8" fill="{c["skin_d"]}"/>')


def high_head(c, e, b, m, x):
    hd = c.get("hair_d", c["hair"])
    hair_back = (f'<ellipse cx="120" cy="112" rx="64" ry="68" fill="{c["hair"]}"/>'
                 f'<path d="M62 108 C48 150 52 196 72 226 C92 222 90 186 92 150 Z" fill="{c["hair"]}"/>'
                 f'<path d="M178 108 C192 150 188 196 168 226 C148 222 150 186 148 150 Z" fill="{c["hair"]}"/>'
                 f'<path d="M64 150 q8 18 0 36 M176 150 q-8 18 0 36 M70 196 q6 10 2 22 M170 196 q-6 10 -2 22" stroke="{hd}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    bun = ""
    lashes = "" if e in ("happy", "closed") else f'<path d="M89 117 l-5 -4 M151 117 l5 -4" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
    return (f'<g filter="url(#cut)">{hair_back}{bun}</g>'
            f'<g filter="url(#cut)"><ellipse cx="120" cy="124" rx="50" ry="58" fill="{c["skin"]}"/></g>'
            f'<circle cx="70" cy="140" r="5" fill="{AMBER}"/><circle cx="170" cy="140" r="5" fill="{AMBER}"/>'
            f'<path d="M70 118 C70 62 160 52 172 112 C160 86 128 76 100 92 C88 100 78 108 70 118 Z" fill="{c["hair"]}"/>'
            f'<path d="M100 92 C120 80 150 84 166 104" stroke="{c.get("hair_d", c["hair"])}" stroke-width="3" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="94" cy="146" rx="9" ry="5" fill="#E8826E" opacity=".45"/><ellipse cx="146" cy="146" rx="9" ry="5" fill="#E8826E" opacity=".45"/>'
            f'<path d="M118 132 q-4 11 4 12" stroke="{c["skin_d"]}" stroke-width="3" fill="none" stroke-linecap="round"/>'
            + eyes(c, e) + lashes + brows(b) + mouth(m, "#B24A3E"))


def char_svg(who, expr, size=200):
    c = LOW if who == "low" else HIGH
    e, b, m, x, tilt = SPEC[expr]
    body = low_body(c) if who == "low" else high_body(c)
    head = low_head(c, e, b, m, x) if who == "low" else high_head(c, e, b, m, x)
    return (f'<svg class="chr" viewBox="0 0 240 300" width="{size}" height="{size * 1.25:.0f}" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><filter id="cut" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="4" stdDeviation="0" flood-color="#5A3C1E" flood-opacity=".22"/></filter></defs>'
            f'{body}<g transform="rotate({tilt} 120 170)">{head}</g>{extras_svg(x)}</svg>')


def sheet():
    rows = ""
    for who, title, sub, chips in [("low", "The $5K coach", "Does it all alone · reacts on the ❌ side", [LOW["top"], LOW["hair"], LOW["skin"], INK]),
                                   ("high", "The $50K coach", "Has a setter team · reacts on the ✅ side", [ORANGE, HIGH["hair"], HIGH["skin"], CREAM])]:
        cards = "".join(f'<div class="cell"><div class="pad">{char_svg(who, ex, 190)}</div><b>{LABEL["asleep_h" if (who == "high" and ex == "asleep") else ex]}</b></div>' for ex in EXPR[who])
        chip = "".join(f'<i style="background:{c}"></i>' for c in chips)
        rows += f'<div class="row"><div class="meta"><h2>{title}</h2><p>{sub}</p><div class="chips">{chip}</div></div>{cards}</div>'
    mock = (f'<div class="mock"><div class="mhead"><span>ROUND 1 · SPEED</span><em>02:14 AM</em></div>'
            f'<div class="split"><div class="side l"><div class="tagx">$5K</div><div class="clock">tomorrow</div>{char_svg("low", "asleep", 200)}<div class="x">✕</div></div>'
            f'<div class="side r"><div class="tagx o">$50K</div><div class="clock o">4 min</div>{char_svg("high", "focused", 200)}<div class="x ok">✓</div></div></div>'
            f'<div class="mcap">One replies <span class="hl">tomorrow.</span> One replies in <span class="hlo">minutes.</span></div></div>')
    return f'''<!doctype html><html><head><meta charset="utf-8"><title>Character Sheet</title><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:2160px;font-family:Inter,sans-serif;color:{INK};padding:56px;display:flex;gap:44px;
background:radial-gradient(120% 90% at 40% 40%,#F4F0E8,#ECE6DA 70%,#E2DBCD);}}
body::before{{content:"";position:fixed;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.035) 0 1px,transparent 1px 36px),repeating-linear-gradient(90deg,rgba(0,0,0,.035) 0 1px,transparent 1px 36px);z-index:-1}}
.main{{flex:1}}
h1{{font:900 46px Inter;letter-spacing:-.03em}}h1 span{{color:{ORANGE}}}
.lead{{font:600 18px Inter;color:#6D665B;margin:8px 0 34px;border-top:1px solid {INK};padding-top:12px}}
.row{{display:flex;gap:14px;margin-bottom:34px;align-items:stretch}}
.meta{{width:200px;flex:none;padding-top:30px}}.meta h2{{font:900 26px Inter;letter-spacing:-.02em}}.meta p{{font:600 14px/1.4 Inter;color:#6D665B;margin:8px 0 14px}}
.chips{{display:flex;gap:6px}}.chips i{{width:26px;height:26px;border-radius:6px;box-shadow:0 3px 0 rgba(0,0,0,.18)}}
.cell{{background:#FBFAF6;border-radius:16px;padding:10px 10px 14px;box-shadow:0 2px 0 #d8d1c3,0 18px 30px rgba(70,50,20,.15);text-align:center}}
.cell .pad{{background:#F1ECE2;border-radius:10px}}
.cell b{{display:block;font:800 13px Inter;margin-top:10px;letter-spacing:-.01em}}
.mock{{width:440px;flex:none;height:782px;border-radius:24px;overflow:hidden;position:relative;background:#ECE6DA;box-shadow:0 30px 60px rgba(0,0,0,.25);outline:8px solid {INK}}}
.mhead{{display:flex;justify-content:space-between;margin:40px 30px 0;border-top:1px solid {INK};padding-top:8px;font:800 11px Inter;letter-spacing:.08em}}.mhead em{{font-style:normal}}
.split{{display:flex;margin-top:40px;height:420px}}.side{{flex:1;position:relative;display:flex;flex-direction:column;align-items:center;justify-content:flex-end}}
.side.l{{border-right:2px dashed rgba(0,0,0,.2)}}
.tagx{{position:absolute;top:0;font:900 40px Inter;background:{INK};color:#fff;padding:0 12px;border-radius:6px}}.tagx.o{{background:{ORANGE}}}
.clock{{position:absolute;top:70px;font:800 18px Inter;background:#fff;padding:6px 12px;border-radius:20px;box-shadow:0 4px 0 #d0c8b8}}.clock.o{{color:{ORANGE}}}
.side .chr{{width:190px;height:auto}}
.x{{position:absolute;top:120px;right:22px;width:50px;height:50px;border-radius:50%;background:{INK};color:#fff;font:900 28px Inter;display:grid;place-items:center;transform:rotate(-8deg)}}.x.ok{{background:{ORANGE}}}
.mcap{{margin:34px 26px 0;font:800 30px/1.1 Inter;letter-spacing:-.03em}}
.hl,.hlo{{color:#fff;background:{INK};padding:0 .1em}}.hlo{{background:{ORANGE}}}
</style></head><body><div class="main"><h1>Character sheet · <span>$5K</span> vs <span>$50K</span> coach</h1>
<p class="lead">Paper cut-out cast for the comparison video. Each expression is a pose the character snaps to on the voice beat; idle breathing + blinking run underneath.</p>
{rows}</div>{mock}</body></html>'''


if __name__ == "__main__":
    open(os.path.join(here, "sheet.html"), "w").write(sheet())
    print("ok")
