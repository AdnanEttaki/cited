"""Paper-data style storyboard for the AI DM setter video (12 frames, 9:16).
Style: cream paper + grid, editorial header, tactile 3D bars/cards/stickers, big black captions, 24h scrubber.
Usage: python3 build.py  -> storyboard.html (render with shoot.mjs)"""
import os

here = os.path.dirname(os.path.abspath(__file__))
O, T, M, A, K = "#D8541E", "#1E9E95", "#D9257E", "#F2A33A", "#1B1B1B"  # orange teal magenta amber ink


def bar(w, color, h=46, label="", inner="", z=""):
    return (f'<div class="bar" style="width:{w}px;height:{h}px;--c:{color};{z}">'
            f'{f"<b>{label}</b>" if label else ""}{inner}</div>')


def card(html, x, y, w, rot=0, extra=""):
    return f'<div class="card" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);{extra}">{html}</div>'


def tag(txt, color, x, y, rot=0):
    return f'<div class="tag" style="left:{x}px;top:{y}px;background:{color};transform:rotate({rot}deg)">{txt}</div>'


def bubble(who, txt, lead=True):
    av = "L" if lead else "AI"
    return (f'<div class="bub"><div class="who"><i class="{"" if lead else "ai"}">{av}</i>{who}<span>now</span></div>'
            f'<div class="txt">{txt}</div></div>')


DMS = ["how much is it?", "still taking clients?", "price??", "is this a bot?", "can we hop on a call",
       "what's the cost?", "u there?", "interested!!"]
COLS = [K, O, T, M, A, K, O, T]

frames = []

# 1 — DM avalanche
stack = "".join(
    f'<div class="row" style="top:{30 + i * 54}px;left:{-30 + (i % 3) * 14}px">'
    + bar(470 - (i % 4) * 30, COLS[i], 50, inner=f'<span class="dm"><em></em>{DMS[i]}</span>') + '</div>'
    for i in range(8))
frames.append(dict(label="Unread DMs", right="02:14 AM", num="48", knob=1,
                   vis=stack + '<div class="badge" style="left:430px;top:6px">48</div>',
                   cap='<span class="hl">48 DMs</span> at 2&nbsp;AM.'))

# 2 — reply time race
race = (f'<div class="lbl" style="top:70px">YOU</div><div class="row" style="top:96px;left:-20px">{bar(490, K, 70, inner="<span class='big pl'>6h 12m</span>")}</div>'
        f'<div class="lbl" style="top:220px">AI SETTER</div><div class="row" style="top:246px;left:-20px">{bar(150, O, 70, inner="<span class='big pl'>4s</span>")}</div>'
        + tag("&#9889; 5,580× faster", T, 250, 268, -4))
frames.append(dict(label="Reply time · you vs AI", right="02:15 AM", num="4s", knob=1,
                   vis=race, cap='You reply in <span class="g">6 hours.</span> It replies in <span class="hlo">4 seconds.</span>'))

# 3 — is this a bot
frames.append(dict(label="The lead asked", right="02:16 AM", num="?", knob=2,
                   vis=card(bubble("The lead", "am I talking to a real person or is this an <mark>AI/bot?</mark>"), 40, 60, 400, -3)
                   + card(bubble("AI setter", "I'm Jake's <mark class=o>AI assistant</mark>, Jake takes over on the call.", False), 70, 250, 400, 2)
                   + tag("honest", O, 380, 230, 8),
                   cap='They asked: <span class="hl">is this a bot?</span>'))

# 4 — price objection with tags
frames.append(dict(label="The price question", right="02:18 AM", num="$", knob=2,
                   vis=card(bubble("The lead", "is it more like <mark>$50/month</mark> or <mark>$500/month?</mark>"), 50, 40, 420, -2)
                   + '<div class="ptag" style="left:70px;top:250px;transform:rotate(-8deg)"><s>$50</s><small>discount?</small></div>'
                   + '<div class="ptag dark" style="left:270px;top:240px;transform:rotate(6deg)">no dodge<small>qualify first</small></div>',
                   cap='No dodge. <span class="hl">No discount.</span>'))

# 5 — qualification checklist (index cards)
chk = "".join(
    f'<div class="row" style="top:{50 + i * 92}px;left:{30 + i * 18}px">{bar(380, c, 68, inner=f"<span class=chk>&#10003;</span><span class=big2>{t}</span>")}</div>'
    for i, (t, c) in enumerate([("Goal", T), ("Budget", O), ("Timeline", M), ("Decision maker", K)]))
frames.append(dict(label="Qualified in the DMs", right="02:21 AM", num="4/4", knob=3, vis=chk,
                   cap='It <span class="hlo">qualifies</span> them first.'))

# 6 — slots
slots = "".join(
    f'<div class="slot{" up" if i == 1 else ""}" style="left:{30 + i * 158}px">'
    f'<small>MON 26</small><b>{t}</b>{"<em>picked</em>" if i == 1 else ""}</div>'
    for i, t in enumerate(["1:00", "3:00", "6:00"]))
frames.append(dict(label="Slots offered", right="02:23 AM", num="3", knob=3,
                   vis=slots + '<div class="flag" style="left:240px;top:40px"></div>',
                   cap='Three slots. <span class="hl">They pick one.</span>'))

# 7 — booked stamp
frames.append(dict(label="Calendar", right="02:24 AM", num="✓", knob=4,
                   vis=card('<div class="cal"><div class="calh">MONDAY · OCT 26</div><div class="calb"><b>3:00 PM</b><span>Strategy call · 30 min</span></div></div>', 60, 60, 400, -2)
                   + '<div class="stamp">BOOKED</div>',
                   cap='<span class="hlo">Booked.</span> Hands-free.'))

# 8 — leads per week (illustrative)
vals = [3, 4, 3, 9, 13, 16, 19]
chart = "".join(
    f'<div class="col" style="left:{20 + i * 66}px;height:{v * 17}px;--c:{K if i < 3 else O}"><span>{v}</span></div>'
    for i, v in enumerate(vals))
frames.append(dict(label="Calls booked per week", right="Week 7", num="19", knob=5,
                   vis=f'<div class="chart">{chart}<div class="base"></div>'
                       f'<div class="cut" style="left:213px"><i>AI on</i></div></div>',
                   cap='No missed <span class="hl">leads.</span>'))

# 9 — setter salary vs AI
frames.append(dict(label="Cost per month", right="Week 8", num="0", knob=5,
                   vis=f'<div class="lbl" style="top:40px">HUMAN SETTER</div><div class="row" style="top:66px;left:-20px">{bar(460, M, 74, inner="<span class='big pl'>salary + commission</span>")}</div>'
                       f'<div class="lbl" style="top:200px">AI SETTER</div><div class="row" style="top:226px;left:-20px">{bar(200, T, 74, inner="<span class='big pl'>flat</span>")}</div>'
                       + tag("no sick days", A, 270, 250, -5) + tag("24/7", K, 330, 310, 4),
                   cap='No setter <span class="hlo">salary.</span>'))

# 10 — CTA key
frames.append(dict(label="Try it", right="Now", num="→", knob=6,
                   vis='<div class="key">SETTER</div><div class="cbox"><i></i>Add a comment…<b>&#10148;</b></div>'
                       + tag("free demo", O, 360, 40, 10),
                   cap='Comment <span class="hl">"SETTER"</span>'))

# 11 — DM arrives
frames.append(dict(label="Your DMs", right="Now", num="1", knob=6,
                   vis=card(bubble("AI setter", "Hey! Here's the demo you asked for &#128071; want to see it on <mark class=o>your</mark> DMs?", False), 50, 90, 420, -2)
                       + '<div class="badge" style="left:420px;top:60px">1</div>',
                   cap="and I'll send you <span class=\"hlo\">the demo.</span>"))

# 12 — end card
frames.append(dict(label="AI DM setter", right="24/7", num="24", knob=7,
                   vis='<div class="key big">24/7</div>' + tag("replies in seconds", T, 60, 300, -4) + tag("books calls", O, 270, 330, 5),
                   cap='Your DMs, <span class="hl">handled.</span>'))

TICKS = ["F1", "F3", "F5", "F7", "F9", "F11"]


def frame(i, f):
    knob = 40 + i * (460 / 11)
    ticks = "".join(f'<span style="left:{40 + j * 2 * (460 / 11)}px">{h}</span>' for j, h in enumerate(TICKS))
    return f'''<section class="fr">
<div class="num">{f["num"]}</div>
<header><div class="rule"></div><span>{f["label"]}</span><em>{f["right"]}</em></header>
<div class="vis">{f["vis"]}</div>
<div class="cap">{f["cap"]}</div>
<div class="scrub"><div class="line"></div><div class="prog" style="width:{knob - 40}px"></div><div class="fl" style="left:{40 + 6 * (460 / 11)}px"></div>
<div class="knob" style="left:{knob - 9}px"></div>{ticks}<small class="l">Values illustrative</small><small class="r">Frame {i + 1} of 12</small></div>
</section>'''


html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Paper Data Storyboard</title><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#1a1a1a;font-family:Inter,sans-serif;width:3284px;padding:12px;display:grid;grid-template-columns:repeat(6,540px);gap:4px}}
.fr{{position:relative;width:540px;height:960px;overflow:hidden;color:{K};
 background:radial-gradient(120% 90% at 50% 40%,#F4F0E8 0%,#ECE6DA 70%,#E2DBCD 100%)}}
.fr::before{{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.035) 0 1px,transparent 1px 36px),repeating-linear-gradient(90deg,rgba(0,0,0,.035) 0 1px,transparent 1px 36px)}}
.num{{position:absolute;left:-20px;bottom:-120px;font:800 430px/1 Inter;letter-spacing:-.06em;color:rgba(60,45,25,.06);white-space:nowrap}}
header{{position:absolute;left:40px;right:40px;top:78px;border-top:1px solid {K};padding-top:10px;display:flex;justify-content:space-between;font:800 13px Inter;letter-spacing:.08em;text-transform:uppercase}}
header .rule{{position:absolute;left:0;top:-3px;width:46px;height:5px;background:{K}}}
header em{{font-style:normal}}
.vis{{position:absolute;left:0;right:0;top:125px;height:470px}}
.cap{{position:absolute;left:40px;right:40px;top:620px;font:800 44px/1.08 Inter;letter-spacing:-.035em}}
.hl,.hlo{{color:#fff;background:{K};padding:0 .12em;border-radius:.08em;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
.hlo{{background:{O}}}
.g{{color:#9A9286}}
.scrub{{position:absolute;left:0;right:0;top:820px;height:70px;font:700 11px Inter;color:#6D665B}}
.scrub .line{{position:absolute;left:40px;right:40px;top:0;height:2px;background:#bdb5a7}}
.scrub .prog{{position:absolute;left:40px;top:-1px;height:4px;background:{K}}}.scrub .prog::after{{content:"";position:absolute;left:{40+6*460/11-40}px;right:0;top:0;bottom:0;background:{O}}}
.scrub .knob{{position:absolute;top:-8px;width:18px;height:18px;border-radius:50%;background:{K};box-shadow:0 3px 6px rgba(0,0,0,.3)}}
.scrub .fl{{position:absolute;top:-26px;width:2px;height:26px;background:{O}}}.scrub .fl::after{{content:"";position:absolute;left:2px;top:0;border-left:14px solid {O};border-top:6px solid transparent;border-bottom:6px solid transparent}}
.scrub span{{position:absolute;top:14px;transform:translateX(-50%)}}
.scrub small{{position:absolute;top:34px;font:500 10px Inter}}.scrub .l{{left:40px}}.scrub .r{{right:40px}}
.row{{position:absolute}}
.bar{{position:relative;border-radius:7px;display:flex;align-items:center;padding:0 18px;color:#fff;
 background:linear-gradient(180deg,color-mix(in srgb,var(--c),#fff 22%) 0%,var(--c) 45%,color-mix(in srgb,var(--c),#000 18%) 100%);
 box-shadow:inset 0 2px 0 rgba(255,255,255,.35),0 8px 0 color-mix(in srgb,var(--c),#000 40%),0 22px 30px rgba(50,30,10,.28)}}
.bar b{{font:800 18px Inter}}
.dm{{display:flex;align-items:center;gap:10px;font:700 19px Inter;white-space:nowrap}}
.dm em{{width:24px;height:24px;border-radius:6px;background:rgba(255,255,255,.9);box-shadow:inset 0 0 0 5px rgba(0,0,0,.15)}}
.pl{{padding-left:24px}}
.big{{font:800 30px Inter;letter-spacing:-.02em;white-space:nowrap}}.big2{{font:800 28px Inter;letter-spacing:-.02em}}
.chk{{width:34px;height:34px;border-radius:50%;background:#fff;color:{K};display:grid;place-items:center;font:900 20px Inter;margin-right:14px}}
.lbl{{position:absolute;left:40px;font:800 13px Inter;letter-spacing:.12em}}
.badge{{position:absolute;min-width:62px;height:62px;padding:0 12px;border-radius:31px;background:{O};color:#fff;font:800 30px Inter;display:grid;place-items:center;box-shadow:0 5px 0 #8f3510,0 14px 24px rgba(0,0,0,.3);border:3px solid #fff}}
.tag{{position:absolute;padding:8px 14px 8px 22px;border-radius:6px;color:#fff;font:800 17px Inter;white-space:nowrap;box-shadow:0 4px 0 rgba(0,0,0,.25),0 12px 20px rgba(0,0,0,.2)}}
.tag::before{{content:"";position:absolute;left:8px;top:50%;width:7px;height:7px;margin-top:-3.5px;border-radius:50%;background:#F4F0E8}}
.card{{position:absolute;background:#FBFAF6;border-radius:16px;padding:18px;box-shadow:0 2px 0 #d8d1c3,0 24px 40px rgba(70,50,20,.22)}}
.bub .who{{display:flex;align-items:center;gap:10px;font:800 14px Inter;letter-spacing:.04em;text-transform:uppercase;margin-bottom:10px}}
.bub .who i{{width:30px;height:30px;border-radius:50%;background:{K};color:#fff;font:800 12px Inter;font-style:normal;display:grid;place-items:center}}
.bub .who i.ai{{background:{O}}}
.bub .who span{{margin-left:auto;font-weight:500;color:#9A9286;text-transform:none}}
.bub .txt{{font:700 26px/1.25 Inter;letter-spacing:-.02em}}
mark{{background:{K};color:#fff;padding:0 .1em;border-radius:.1em}}mark.o{{background:{O}}}
.ptag{{position:absolute;width:190px;padding:22px 16px 18px;border-radius:10px 10px 10px 10px;background:#F7F3EA;border:2px solid {K};font:800 34px Inter;text-align:center;box-shadow:0 6px 0 #c9c0b0,0 20px 30px rgba(0,0,0,.2)}}
.ptag::before{{content:"";position:absolute;left:50%;top:9px;width:12px;height:12px;margin-left:-6px;border-radius:50%;border:2px solid {K};background:#ECE6DA}}
.ptag small{{display:block;font:600 14px Inter;color:#7d766a;margin-top:4px}}.ptag s{{text-decoration-thickness:4px;text-decoration-color:{O}}}
.ptag.dark{{background:{K};color:#fff;font-size:30px}}.ptag.dark small{{color:#bdb5a7}}
.slot{{position:absolute;top:140px;width:140px;height:170px;border-radius:14px;background:#FBFAF6;box-shadow:0 6px 0 #d0c8b8,0 20px 30px rgba(0,0,0,.18);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px}}
.slot small{{font:800 12px Inter;letter-spacing:.12em;color:#8a8275}}.slot b{{font:800 42px Inter;letter-spacing:-.03em}}
.slot.up{{top:96px;background:{O};color:#fff;box-shadow:0 8px 0 #8f3510,0 28px 40px rgba(0,0,0,.28);transform:rotate(-3deg)}}.slot.up small{{color:#ffe1d3}}
.slot em{{font:800 12px Inter;font-style:normal;background:#fff;color:{O};padding:3px 8px;border-radius:4px;text-transform:uppercase;letter-spacing:.1em}}
.flag{{position:absolute;width:3px;height:60px;background:{K}}}.flag::after{{content:"";position:absolute;left:3px;top:0;border-left:30px solid {O};border-top:12px solid transparent;border-bottom:12px solid transparent}}
.cal .calh{{background:{O};color:#fff;font:800 15px Inter;letter-spacing:.12em;padding:12px 16px;border-radius:10px 10px 0 0;margin:-18px -18px 0}}
.cal .calb{{padding:26px 4px 10px}}.cal b{{display:block;font:800 72px Inter;letter-spacing:-.05em}}.cal span{{font:600 18px Inter;color:#7d766a}}
.stamp{{position:absolute;left:230px;top:250px;padding:10px 22px;border:6px solid {O};color:{O};font:900 50px Inter;letter-spacing:.06em;border-radius:12px;transform:rotate(-12deg);background:rgba(244,240,232,.6)}}
.chart{{position:absolute;left:40px;top:40px;width:460px;height:380px}}
.col{{position:absolute;bottom:40px;width:50px;border-radius:6px 6px 2px 2px;background:linear-gradient(90deg,color-mix(in srgb,var(--c),#fff 15%),var(--c));box-shadow:6px 0 0 color-mix(in srgb,var(--c),#000 40%),0 16px 22px rgba(0,0,0,.2)}}
.col span{{position:absolute;top:-30px;left:0;right:0;text-align:center;font:800 20px Inter;color:{K}}}
.base{{position:absolute;left:-10px;right:-10px;bottom:30px;height:10px;border-radius:4px;background:{K}}}
.cut{{position:absolute;top:0;bottom:30px;border-left:2px dashed {O}}}.cut i{{position:absolute;top:-6px;left:6px;background:{O};color:#fff;font:800 13px Inter;font-style:normal;padding:4px 8px;border-radius:4px;white-space:nowrap}}
.key{{position:absolute;left:60px;top:90px;width:420px;height:170px;border-radius:26px;display:grid;place-items:center;color:#fff;font:900 76px Inter;letter-spacing:-.02em;
 background:linear-gradient(180deg,#E8703C,{O} 50%,#B9441A);box-shadow:inset 0 3px 0 rgba(255,255,255,.4),0 16px 0 #7f2e0d,0 40px 50px rgba(0,0,0,.3)}}
.key.big{{font-size:110px;top:70px;height:200px}}
.cbox{{position:absolute;left:60px;top:320px;width:420px;height:58px;border-radius:29px;background:#FBFAF6;border:1px solid #d6cfc1;display:flex;align-items:center;gap:12px;padding:0 10px;font:500 19px Inter;color:#8a8275;box-shadow:0 10px 20px rgba(0,0,0,.12)}}
.cbox i{{width:38px;height:38px;border-radius:50%;background:{K}}}.cbox b{{margin-left:auto;color:{K}}}
</style></head><body>{"".join(frame(i, f) for i, f in enumerate(frames))}</body></html>'''
open(os.path.join(here, "storyboard.html"), "w").write(html)
print("ok", len(frames))
