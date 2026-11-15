"""'Comment SCRIPT' Reel storyboard — same paper style as the Ben vs Mia videos.
python3 build.py -> storyboard.html ; node ../coach-compare/shoot.mjs-style render via shoot.mjs"""
import os, re, sys

here = os.path.dirname(os.path.abspath(__file__))
studio = os.path.abspath(os.path.join(here, "..", ".."))
pd = os.path.join(studio, "storyboards", "paper-data")
ns = {"__file__": os.path.join(pd, "build.py")}
exec(open(os.path.join(pd, "build.py")).read(), ns)
sys.path.insert(0, os.path.join(studio, "characters"))
import characters as C  # noqa: E402

K, O, T_, A = ns["K"], ns["O"], ns["T"], ns["A"]
phone, tag = ns["phone"], ns["tag"]
LOGO = open(os.path.join(studio, "brand", "logo", "svg", "mark_primary.svg")).read()
BASE_CSS = re.search(r"<style>(.*?)</style>", ns["html"], re.S).group(1)


def ben(expr, size, x, y):
    return f'<div class="chr" style="left:{x}px;top:{y}px">{C.char_svg("low", expr, size)}</div>'


def say(text, x, y, who="BEN"):
    return f'<div class="say" style="left:{x}px;top:{y}px"><b>{who}</b>{text}</div>'


FRAMES = [
    dict(label="For coaches", right="11:41 PM", num="?",
         vis=f'<div class="tag xl" style="left:22px;top:-6px;background:{O};transform:rotate(-4deg)">COACHES 👇</div>'
             + phone([("in", "hey! saw your transformation post 🔥"), ("in", "how much is your coaching?")], x=150, y=40, rot=-3, w=270, h=330, seen=False, name="New lead")
             + '<div class="badge" style="left:396px;top:24px">1</div>' + ben("asleep", 150, 10, 300) + '<div class="zz">Z<small>z</small><small>z</small></div>',
         cap='If this happens in your DMs <span class="hl">every week…</span>',
         vo="NARRATOR: Coaches. If this happens in your DMs every week…"),
    dict(label="11 minutes later", right="11:52 PM", num="11",
         vis=phone([("in", "how much is your coaching?"), ("in", "nvm, went with another coach 🙏")], x=120, y=20, rot=2, w=300, h=380, seen=False, name="New lead", hl=1)
             + '<div class="ring"></div>' + ben("asleep", 130, 360, 330),
         cap='11 minutes later… <span class="hlo">they’re gone.</span>',
         vo="NARRATOR: …a lead asks the price at 11:41. Eleven minutes later, they’re gone."),
    dict(label="Next morning", right="9:02 AM", num="☀",
         vis=phone([("in", "nvm, went with another coach 🙏"), ("out", "Hey! Sorry, just saw this 😅")], x=40, y=30, rot=-3, w=270, h=330, seen=False, name="New lead")
             + ben("panic", 170, 320, 280) + say("Sorry, just saw this…", 300, 230),
         cap='You didn’t lose them to price. <span class="hl">You lost them to time.</span>',
         vo="BEN: [groans] Sorry, just saw this… / NARRATOR: You didn’t lose them to price. You lost them to time."),
    dict(label="With DMSetter", right="11:41 PM", num="✓",
         vis=phone([("in", "how much is your coaching?"), ("out", "Hey! Love that you reached out 🙌 What's your goal right now?"), ("in", "drop 8kg before summer"),
                    ("out", "Got you. Quick call Thursday 3 PM to see if it's a fit?"), ("in", "yes!! 🙌")], x=30, y=10, rot=-2, w=290, h=400, seen=False, name="New lead", hl=1)
             + f'<div class="mascot">{LOGO.replace('width="260" height="260"', 'width="130" height="130"')}</div>'
             + '<div class="clock2">replied in 38 sec</div><div class="stamp3">BOOKED</div>' + ben("asleep", 130, 380, 320),
         cap='With <span class="hlo">DMSetter</span>, you wake up to <span class="hl">booked calls.</span>',
         vo="NARRATOR: With DMSetter, that same DM gets answered in seconds, qualified, and booked… while you sleep."),
    dict(label="The fix", right="7 replies", num="7",
         vis="".join(f'<div class="card7" style="left:{40 + i * 62}px;top:{110 + abs(3 - i) * 14}px;transform:rotate({(i - 3) * 7}deg);background:{[O, K, T_, "#FBFAF6", O, T_, K][i]}"><b>{i + 1}</b><i></i><i></i><i></i></div>' for i in range(7))
             + ben("confused", 140, 200, 310) + tag("copy-paste ready", A, 300, 40, 6),
         cap='7 replies that turn <span class="hlo">“how much?”</span> into a booked call.',
         vo="NARRATOR: Here are 7 replies that turn ‘how much?’ into a booked call."),
    dict(label="Free for coaches", right="Now", num="→",
         vis='<div class="key press">SCRIPT</div><div class="cbox"><i></i>SCRIPT<b>&#10148;</b></div>'
             + tag("I’ll DM it to you", O, 330, 30, 8) + ben("tired", 120, 20, 330),
         cap='Comment <span class="hl">“SCRIPT”</span> and I’ll send them to you.',
         vo="NARRATOR: Comment SCRIPT, and I’ll send them to you."),
    dict(label="DMSetter", right="Your DMs, handled", num="✓",
         vis=f'<div class="endlogo">{LOGO.replace('width="260" height="260"', 'width="240" height="240"')}</div>'
             + '<div class="wm">DM<span>Setter</span></div><div class="outc">'
             + "".join(f'<div class="o"><i>✓</i>{t}</div>' for t in ["Replies in seconds, 24/7", "Qualifies every lead", "Follows up until they answer", "Books calls into your calendar"]) + '</div>',
         cap='More booked calls. <span class="hlo">Zero DMs at 2 AM.</span>',
         vo="NARRATOR: DMSetter. More booked calls. Zero DMs at two A.M."),
]

EXTRA = f"""
.chr{{position:absolute;z-index:4}}
.zz{{position:absolute;left:120px;top:290px;font:900 30px Inter;color:{K}}}.zz small{{font-size:.6em;margin-left:4px}}
.ring{{position:absolute;left:112px;top:262px;width:300px;height:70px;border:5px solid #E8322D;border-radius:50%;transform:rotate(-3deg);z-index:6}}
.say{{position:absolute;z-index:8;max-width:150px;background:#fff;border:2.5px solid {K};border-radius:16px;padding:7px 11px;font:800 14px/1.2 Inter;box-shadow:0 5px 0 rgba(0,0,0,.15)}}
.say b{{display:block;font:900 9px Inter;letter-spacing:.14em;color:{O};margin-bottom:2px}}
.card7{{position:absolute;width:80px;height:118px;border-radius:10px;box-shadow:0 6px 0 rgba(0,0,0,.2),0 14px 24px rgba(0,0,0,.18);padding:10px;color:#fff}}
.card7 b{{font:900 26px Inter}}.card7 i{{display:block;height:5px;border-radius:3px;background:rgba(255,255,255,.55);margin-top:9px}}
.card7:nth-child(4){{color:{K}}}.card7:nth-child(4) i{{background:rgba(0,0,0,.25)}}
.mascot{{position:absolute;left:330px;top:40px;z-index:7;animation:none}}
.clock2{{position:absolute;left:340px;top:190px;z-index:7;background:#fff;color:{O};font:800 15px Inter;padding:6px 12px;border-radius:16px;box-shadow:0 3px 0 #d0c8b8;transform:rotate(4deg)}}
.stamp3{{position:absolute;left:330px;top:250px;z-index:7;padding:4px 12px;border:5px solid {O};color:{O};font:900 30px Inter;border-radius:10px;transform:rotate(-12deg);background:rgba(244,240,232,.85)}}
.endlogo{{position:absolute;left:150px;top:10px}}
.wm{{position:absolute;left:0;right:0;top:250px;text-align:center;font:900 64px Inter;letter-spacing:-.04em;color:{K}}}.wm span{{color:{O}}}
.outc{{position:absolute;left:70px;right:70px;top:340px;display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.o{{background:#FBFAF6;border-radius:12px;padding:10px 12px;font:800 14px/1.25 Inter;display:flex;gap:8px;align-items:center;box-shadow:0 3px 0 #d8d1c3}}
.o i{{font-style:normal;flex:none;width:24px;height:24px;border-radius:50%;background:{O};color:#fff;display:grid;place-items:center;font:900 13px Inter}}
.key{{top:70px}}.cbox{{top:270px;font-weight:700;color:{K}}}
"""


def frame(i, f):
    return f'''<section class="fr"><div class="num">{f["num"]}</div>
<header><div class="rule"></div><span>{f["label"]}</span><em>{f["right"]}</em></header>
<div class="vis">{f["vis"]}</div><div class="cap">{f["cap"]}</div>
<div class="vo">🎙 {f["vo"]}</div></section>'''


html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Script Reel</title><style>{BASE_CSS}{EXTRA}
body{{width:{12 + len(FRAMES) * 544}px;grid-template-columns:repeat({len(FRAMES)},540px)}}
.vo{{position:absolute;left:30px;right:30px;bottom:24px;font:600 13px/1.35 Inter;color:#6D665B;background:rgba(255,255,255,.6);border-radius:10px;padding:8px 10px}}</style></head>
<body>{"".join(frame(i, f) for i, f in enumerate(FRAMES))}</body></html>'''

if __name__ == "__main__":
    open(os.path.join(here, "storyboard.html"), "w").write(html)
    print("ok", len(FRAMES))
