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

ASK = ("in", "Hey! How do I join?")
PEOPLE = {"l": ("BEN", "Fitness coach", "$5K/mo"), "r": ("MIA", "Nutrition coach", "$50K/mo")}


def mini(msgs, x, name, **kw):
    """Scaled-down DM phone for one half of the split."""
    return f'<div class="mini" style="left:{x}px">{phone(msgs, x=0, y=0, rot=0, w=300, h=350, name=name, **kw)}</div>'


def nametag(side, style=""):
    n, niche, money = PEOPLE[side]
    return f'<div class="money {side}" style="{style}">{n}<small>{niche} · {money}</small></div>'


def say(side, text, who="", style=""):
    """Comic speech bubble for a character line (voiced)."""
    return f'<div class="say {side}" style="{style}"><b>{who}</b>{text}</div>'


def half(side, msgs, expr, mark, clock=None, extra="", seen=False):
    x0 = 0 if side == "l" else 270
    who = "low" if side == "l" else "high"
    return (f'<div class="half {side}" style="left:{x0}px">' + nametag(side)
            + (f'<div class="clock {side}">{clock}</div>' if clock else "")
            + mini(msgs, 26, "Lucy", seen=seen)
            + f'<div class="who">{C.char_svg(who, expr, 150)}</div>'
            + f'<div class="mark {side}">{"✕" if mark == "x" else "✓"}</div>{extra}</div>')


def split(left, right):
    return f'<div class="split">{left}{right}<div class="divider"></div></div>'


frames = [
    dict(label="Meet Ben & Mia", right="50 DMs / week", num="50",
         vis=f'<div class="hook-l">{C.char_svg("low", "tired", 230)}</div><div class="hook-r">{C.char_svg("high", "calm", 230)}</div>'
             + nametag("l", "top:8px;left:24px") + nametag("r", "top:8px;right:24px;left:auto")
             + '<div class="dmc l">50 DMs<small>/ week</small></div><div class="dmc r">50 DMs<small>/ week</small></div>'
             + '<div class="vs">VS</div>',
         cap='Same 50 DMs a week. <span class="hl">Different results.</span>',
         vo=[("narrator", "This is Ben. Fitness coach. Five K a month. This is Mia. Nutrition coach. Fifty K a month. Same fifty DMs a week.")]),
    dict(label="Round 1 · Speed", right="Score ✓ 1", num="1",
         vis=split(half("l", [ASK], "asleep", "x", "14 hrs later", extra=say("l", "Oh no… 14 hours ago.", "BEN")),
                   half("r", [ASK, ("out", "Hey! Love that you reached out 🙌 What's your goal right now?")], "focused", "ok", "12 sec")),
         cap='Ben sees it tomorrow. Mia’s DMs answer in <span class="hlo">seconds.</span>',
         vo=[("lucy", "Hey! How do I join?"), ("narrator", "Ben sees it the next morning."), ("ben", "Oh no… fourteen hours ago."),
             ("narrator", "Mia's DMs answer in seconds.")]),
    dict(label="Round 2 · First reply", right="Score ✓ 2", num="2",
         vis=split(half("l", [ASK, ("out", "Here's my link 👉 join.link")], "tired", "x"),
                   half("r", [ASK, ("out", "Love that! What's the main thing you want to change?"), ("in", "I just want to finally be consistent")], "calm", "ok")),
         cap='Ben sends a link. Mia’s DMs <span class="hlo">ask a question.</span>',
         vo=[("narrator", "Ben sends a link. Mia's DMs ask a question."), ("lucy", "I just want to finally be consistent.")]),
    dict(label="Round 3 · The cost question", right="Score ✓ 3", num="3",
         vis=split(half("l", [("in", "How much is it?"), ("out", "Uh… I can do a discount?")], "panic", "x", extra=say("l", "Uh… discount?", "BEN")),
                   half("r", [("in", "How much is it?"), ("out", "Depends on your goal. Quick call to see if it's a fit?"), ("in", "Sure!")], "happy", "ok")),
         cap='Mia’s DMs don’t drop a price. They <span class="hlo">book a call.</span>',
         vo=[("lucy", "How much is it?"), ("ben", "Uh… I can do a discount?"), ("narrator", "Mia's DMs don't drop a price. They book a call."), ("lucy", "Sure!")]),
    dict(label="Round 4 · Ghosted", right="Score ✓ 4", num="4",
         vis=split(half("l", [("out", "So… do you want to join?")], "confused", "x", "no reply", seen=True,
                        extra=say("l", "Guess she’s not interested.", "BEN")),
                   half("r", [("out", "Day 1: still keen to sort this?"), ("out", "Day 3: saved you a spot for Thursday 👀"), ("in", "Omg sorry! Yes, let's do it")], "coffee", "ok", "day 1 · 3")),
         cap='Ben gives up. Mia’s DMs <span class="hlo">follow up.</span>',
         vo=[("narrator", "Ben gets left on seen… and gives up."), ("ben", "Guess she's not interested."),
             ("narrator", "Mia's DMs follow up. Day one. Day three."), ("lucy", "Omg sorry! Yes, let's do it.")]),
    dict(label="Round 5 · The twist", right="Score ✓ 5", num="5",
         vis=split(half("l", [("in", "hello??"), ("in", "u there?"), ("in", "still taking clients?")], "2am", "x", "02:14 AM",
                        extra=say("l", "Why am I always in my DMs?", "BEN")),
                   half("r", [("in", "Yes, let's do it"), ("out", "Booked ✓ Thursday 3 PM. Mia's excited to meet you!"), ("in", "🙌🙌")], "asleep", "ok", "asleep",
                        extra=f'<div class="setter">HER SETTER</div><div class="stamp2">BOOKED</div>')),
         cap='Mia doesn’t answer her DMs. <span class="hlo">Her setter does.</span>',
         vo=[("narrator", "Two AM. Ben is still typing."), ("ben", "Why am I always in my DMs?"),
             ("narrator", "Mia is asleep. Because Mia doesn't answer her DMs… her setter does.")]),
    dict(label="Your turn", right="Now", num="→",
         vis='<div class="key">SETTER</div><div class="cbox"><i></i>Add a comment…<b>&#10148;</b></div>'
             + f'<div class="cta-chr">{C.char_svg("high", "thumbs", 170)}</div><div class="cta-ben">{C.char_svg("low", "confused", 120)}</div>'
             + say("r", "Want your DMs handled like mine?", "MIA", "left:250px;top:330px")
             + say("l", "Wait… what’s a setter?", "BEN", "left:8px;top:300px"),
         cap='Comment <span class="hl">"SETTER"</span>',
         vo=[("mia", "Want your DMs handled like mine? Comment SETTER."), ("ben", "Wait… what's a setter?")]),
]

TICKS = ["Meet", "R1", "R2", "R3", "R4", "R5", "CTA"]
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
<div class="knob" style="left:{knob - 9}px"></div>{ticks}<small class="l">A story · example conversations and income figures</small><small class="r">Frame {i + 1} of {N}</small></div>
</section>'''


EXTRA_CSS = f"""
.split{{position:absolute;inset:0}}
.half{{position:absolute;top:0;width:270px;height:470px}}
.divider{{position:absolute;left:269px;top:20px;bottom:0;border-left:2px dashed rgba(0,0,0,.18)}}
.money{{position:absolute;top:-6px;left:18px;font:900 30px Inter;letter-spacing:-.03em;color:#fff;background:{K};padding:0 10px;border-radius:6px;z-index:3}}
.money.r{{background:{O};left:auto;right:18px}}
.money small{{display:block;font:700 9px Inter;letter-spacing:.06em;text-transform:uppercase;opacity:.85;margin:-4px 0 5px}}
.clock{{position:absolute;top:2px;font:800 14px Inter;background:#fff;padding:5px 10px;border-radius:16px;box-shadow:0 3px 0 #d0c8b8;z-index:3;white-space:nowrap}}
.clock.l{{right:8px}}.clock.r{{left:8px;color:{O}}}
.half .clock{{top:46px;transform:rotate(-3deg);z-index:6}}
.mini{{position:absolute;top:52px;width:300px;height:350px;transform:scale(.72);transform-origin:0 0}}
.mini .ph{{position:absolute}}
.who{{position:absolute;bottom:-14px;left:50%;margin-left:-75px;z-index:4}}
.who .chr{{display:block}}
.mark{{position:absolute;top:70px;width:44px;height:44px;border-radius:50%;background:{K};color:#fff;font:900 24px Inter;display:grid;place-items:center;z-index:5;transform:rotate(-8deg);box-shadow:0 4px 0 rgba(0,0,0,.25)}}
.mark.l{{right:12px}}.mark.r{{right:12px;background:{O}}}
.setter{{position:absolute;top:318px;left:2px;z-index:6;background:{T_};color:#fff;font:900 18px Inter;padding:6px 12px;border-radius:6px;transform:rotate(-6deg);box-shadow:0 4px 0 rgba(0,0,0,.25)}}
.stamp2{{position:absolute;top:290px;right:4px;z-index:6;padding:4px 10px;border:4px solid {O};color:{O};font:900 24px Inter;border-radius:8px;transform:rotate(-12deg);background:rgba(244,240,232,.8)}}
.cta-chr{{position:absolute;right:20px;bottom:-30px}}
.cta-ben{{position:absolute;left:30px;bottom:-24px;z-index:4}}
.say{{position:absolute;z-index:8;max-width:150px;background:#fff;border:2.5px solid {K};border-radius:16px;padding:7px 11px;font:800 14px/1.2 Inter;letter-spacing:-.01em;box-shadow:0 5px 0 rgba(0,0,0,.15)}}
.say b{{display:block;font:900 9px Inter;letter-spacing:.14em;color:{O};margin-bottom:2px}}
.say::after{{content:"";position:absolute;bottom:-11px;width:16px;height:16px;background:#fff;border-right:2.5px solid {K};border-bottom:2.5px solid {K};transform:rotate(45deg) skew(10deg,10deg)}}
.half .say{{max-width:112px}}.half .say.l{{left:150px;top:300px}}.half .say.l::after{{left:14px}}
.half .say.r{{right:150px;top:300px}}.say.r::after{{right:14px}}
.dmc{{position:absolute;top:96px;z-index:6;background:#FF3B5C;color:#fff;font:900 22px Inter;padding:6px 12px;border-radius:22px;border:3px solid #fff;box-shadow:0 5px 0 #a8203b,0 12px 20px rgba(0,0,0,.2);transform:rotate(-5deg)}}
.dmc small{{font:800 11px Inter;margin-left:4px}}.dmc.l{{left:34px}}.dmc.r{{right:34px;transform:rotate(5deg)}}
.vs{{position:absolute;left:50%;top:200px;margin-left:-38px;width:76px;height:76px;border-radius:50%;background:{K};color:#fff;font:900 30px Inter;display:grid;place-items:center;z-index:6;box-shadow:0 6px 0 #000}}
.tag{{z-index:10}}
.mini .b{{font-size:15.5px;line-height:1.28}}
.mini .th{{padding:10px 8px 8px}}
.hook-l,.hook-r{{position:absolute;bottom:-30px;z-index:4}}.hook-l{{left:-6px}}.hook-r{{right:-6px}}
.key{{top:40px}}.cbox{{top:250px}}
"""

html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Coach Compare Storyboard</title><style>{BASE_CSS}{EXTRA_CSS}
body{{width:{12 + N * 544}px}}body{{grid-template-columns:repeat({N},540px)}}</style></head>
<body>{"".join(frame(i, f) for i, f in enumerate(frames))}</body></html>'''

if __name__ == "__main__":
    open(os.path.join(here, "storyboard.html"), "w").write(html)
    print("ok", N)
