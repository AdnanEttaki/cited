"""$5K coach vs $50K coach — split-screen storyboard (paper style + characters + Instagram-style DM phones).
python3 build.py -> storyboard.html ; node shoot.mjs -> storyboard.jpg + frames/"""
import os, sys

here = os.path.dirname(os.path.abspath(__file__))
studio = os.path.abspath(os.path.join(here, "..", ".."))
pd = os.path.join(studio, "storyboards", "paper-data")
ns = {"__file__": os.path.join(pd, "build.py")}
exec(open(os.path.join(pd, "build.py")).read(), ns)  # paper style CSS + phone()
sys.path.insert(0, os.path.join(studio, "characters"))
import characters as C  # noqa: E402

K, O, T_, A = ns["K"], ns["O"], ns["T"], ns["A"]
phone, tag = ns["phone"], ns["tag"]
import re  # noqa: E402
BASE_CSS = re.search(r"<style>(.*?)</style>", ns["html"], re.S).group(1)

ASK = ("in", "How do I join?")


def mini(msgs, x, name, **kw):
    """Scaled-down DM phone for one half of the split."""
    return f'<div class="mini" style="left:{x}px">{phone(msgs, x=0, y=0, rot=0, w=300, h=350, name=name, **kw)}</div>'


def half(side, msgs, expr, mark, clock=None, extra="", seen=False):
    x0 = 0 if side == "l" else 270
    who = "low" if side == "l" else "high"
    money = "$5K" if side == "l" else "$50K"
    return (f'<div class="half {side}" style="left:{x0}px">'
            f'<div class="money {side}">{money}<small>/month · example</small></div>'
            + (f'<div class="clock {side}">{clock}</div>' if clock else "")
            + mini(msgs, 26, "Lead", seen=seen)
            + f'<div class="who">{C.char_svg(who, expr, 150)}</div>'
            + f'<div class="mark {side}">{"✕" if mark == "x" else "✓"}</div>{extra}</div>')


def split(left, right):
    return f'<div class="split">{left}{right}<div class="divider"></div></div>'


frames = [
    dict(label="For coaches", right="02:14 AM", num="DM",
         vis=f'<div class="tag xl" style="left:22px;top:-8px;background:{O};transform:rotate(-4deg)">FOR COACHES</div>'
             + phone([ASK], x=150, y=20, rot=-3, w=240, h=300, seen=False, name="New lead") + '<div class="badge" style="left:362px;top:4px">1</div>'
             + f'<div class="hook-l">{C.char_svg("low", "stressed", 150)}</div><div class="hook-r">{C.char_svg("high", "calm", 150)}</div>'
             + '<div class="money l" style="top:262px;left:14px;z-index:6">$5K<small>/month · example</small></div><div class="money r" style="top:262px;right:14px;left:auto;z-index:6">$50K<small>/month · example</small></div>',
         cap='Coaches: you said “DM me.” <span class="hl">What happens next?</span>',
         vo="Coaches. You said, DM me. What happens next?"),
    dict(label="Round 1 · Speed", right="Score ✓ 1", num="1",
         vis=split(half("l", [ASK], "asleep", "x", "tomorrow"),
                   half("r", [ASK, ("out", "Hey! Love that you reached out 🙌 What's your goal right now?")], "focused", "ok", "seconds")),
         cap='He replies <span class="g">tomorrow.</span> She replies in <span class="hlo">seconds.</span>',
         vo="He replies tomorrow. She replies in seconds."),
    dict(label="Round 2 · First reply", right="Score ✓ 2", num="2",
         vis=split(half("l", [ASK, ("out", "Here's my link 👉 join.link"), ], "tired", "x"),
                   half("r", [ASK, ("out", "Love that! What's the main thing you want to change?"), ("in", "Honestly… consistency 😅")], "calm", "ok")),
         cap='He sends a link. She asks <span class="hlo">what they want.</span>',
         vo="He sends a link. She asks what they want."),
    dict(label="Round 3 · The cost question", right="Score ✓ 3", num="3",
         vis=split(half("l", [("in", "How much is it?"), ("out", "It's normally more, but I can do a discount for you 🙏")], "panic", "x"),
                   half("r", [("in", "How much is it?"), ("out", "Depends on your goal. Quick call to see if it's a fit?"), ("in", "Sure!")], "happy", "ok")),
         cap='He drops the price. She <span class="hlo">qualifies first.</span>',
         vo="He drops the price. She qualifies first."),
    dict(label="Round 4 · Ghosted", right="Score ✓ 4", num="4",
         vis=split(half("l", [("out", "So do you want to join?")], "confused", "x", "no reply", seen=True),
                   half("r", [("out", "Day 1: still keen to sort this?"), ("out", "Day 3: saved you a spot for Thursday 👀"), ("in", "Omg sorry! Yes, let's do it")], "coffee", "ok", "day 1 · 3 · 7")),
         cap='He gives up. She <span class="hlo">follows up.</span>',
         vo="He gives up. She follows up."),
    dict(label="Round 5 · The difference", right="Score ✓ 5", num="5",
         vis=split(half("l", [("in", "hello??"), ("in", "u there?"), ("in", "still taking clients?")], "2am", "x", "02:14 AM"),
                   half("r", [("in", "How do I join?"), ("out", "Got you! Thursday 3 PM works?"), ("in", "Perfect 🙌")], "asleep", "ok", "asleep",
                        extra=f'<div class="setter">HER SETTER</div><div class="stamp2">BOOKED</div>')),
         cap='He’s still typing at 2&nbsp;AM. <span class="hlo">Her setter already booked the call.</span>',
         vo="He's still typing at 2 AM. Her setter already booked the call."),
    dict(label="Your turn", right="Now", num="→",
         vis='<div class="key">SETTER</div><div class="cbox"><i></i>Add a comment…<b>&#10148;</b></div>'
             + f'<div class="cta-chr">{C.char_svg("high", "thumbs", 170)}</div>',
         cap='Want DMs like the $50K coach? Comment <span class="hl">"SETTER"</span>',
         vo="Want your DMs run like the fifty K coach? Comment SETTER."),
]

TICKS = ["Hook", "R1", "R2", "R3", "R4", "R5", "CTA"]
N = len(frames)


def frame(i, f):
    knob = 40 + i * (460 / (N - 1))
    ticks = "".join(f'<span style="left:{40 + j * (460 / (N - 1))}px">{h}</span>' for j, h in enumerate(TICKS))
    return f'''<section class="fr">
<div class="num">{f["num"]}</div>
<header><div class="rule"></div><span>{f["label"]}</span><em>{f["right"]}</em></header>
<div class="vis">{f["vis"]}</div>
<div class="cap">{f["cap"]}</div>
<div class="scrub"><div class="line"></div><div class="prog" style="width:{knob - 40}px"></div><div class="fl" style="left:{40 + 5 * (460 / (N - 1))}px"></div>
<div class="knob" style="left:{knob - 9}px"></div>{ticks}<small class="l">Example conversations · income figures are examples</small><small class="r">Frame {i + 1} of {N}</small></div>
</section>'''


EXTRA_CSS = f"""
.split{{position:absolute;inset:0}}
.half{{position:absolute;top:0;width:270px;height:470px}}
.divider{{position:absolute;left:269px;top:20px;bottom:0;border-left:2px dashed rgba(0,0,0,.18)}}
.money{{position:absolute;top:-6px;left:18px;font:900 30px Inter;letter-spacing:-.03em;color:#fff;background:{K};padding:0 10px;border-radius:6px;z-index:3}}
.money.r{{background:{O};left:auto;right:18px}}
.money small{{display:block;font:700 8px Inter;letter-spacing:.08em;text-transform:uppercase;opacity:.75;margin:-4px 0 4px}}
.clock{{position:absolute;top:2px;font:800 14px Inter;background:#fff;padding:5px 10px;border-radius:16px;box-shadow:0 3px 0 #d0c8b8;z-index:3;white-space:nowrap}}
.clock.l{{right:18px}}.clock.r{{left:18px;color:{O}}}
.mini{{position:absolute;top:52px;width:300px;height:350px;transform:scale(.72);transform-origin:0 0}}
.mini .ph{{position:absolute}}
.who{{position:absolute;bottom:-14px;left:50%;margin-left:-75px;z-index:4}}
.who .chr{{display:block}}
.mark{{position:absolute;top:70px;width:44px;height:44px;border-radius:50%;background:{K};color:#fff;font:900 24px Inter;display:grid;place-items:center;z-index:5;transform:rotate(-8deg);box-shadow:0 4px 0 rgba(0,0,0,.25)}}
.mark.l{{right:12px}}.mark.r{{right:12px;background:{O}}}
.setter{{position:absolute;top:318px;left:2px;z-index:6;background:{T_};color:#fff;font:900 18px Inter;padding:6px 12px;border-radius:6px;transform:rotate(-6deg);box-shadow:0 4px 0 rgba(0,0,0,.25)}}
.stamp2{{position:absolute;top:290px;right:4px;z-index:6;padding:4px 10px;border:4px solid {O};color:{O};font:900 24px Inter;border-radius:8px;transform:rotate(-12deg);background:rgba(244,240,232,.8)}}
.cta-chr{{position:absolute;right:20px;bottom:-30px}}
.tag{{z-index:10}}
.mini .b{{font-size:15.5px;line-height:1.28}}
.mini .th{{padding:10px 8px 8px}}
.hook-l,.hook-r{{position:absolute;bottom:-20px;z-index:4}}.hook-l{{left:6px}}.hook-r{{right:6px}}
.key{{top:40px}}.cbox{{top:250px}}
"""

html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Coach Compare Storyboard</title><style>{BASE_CSS}{EXTRA_CSS}
body{{width:{12 + N * 544}px}}body{{grid-template-columns:repeat({N},540px)}}</style></head>
<body>{"".join(frame(i, f) for i, f in enumerate(frames))}</body></html>'''

if __name__ == "__main__":
    open(os.path.join(here, "storyboard.html"), "w").write(html)
    print("ok", N)
