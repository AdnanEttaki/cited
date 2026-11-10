"""Winning static ad 'If this happens in your DMs every week…' + one-variable variants (1080x1920).
python3 build.py -> html/*.html ; node shoot.mjs -> out/*.png + out/sheet.png"""
import os

here = os.path.dirname(os.path.abspath(__file__))
HEAD = "If this happens in your DMs every week…"
BASE = dict(head=HEAD, handle="sarah.fitjourney", seen="Active 9h ago", grad="linear-gradient(135deg,#F58529,#DD2A7B,#8134AF)",
            t1="Yesterday 11:41 PM", m1="hey! saw your transformation post 🔥", m2="how much is your coaching?",
            t2="Yesterday 11:52 PM", lost="nvm, went with another coach 🙏", t3="Today 9:02 AM", reply="Hey! Sorry, just saw this 😅")

VARIANTS = [
    ("V0_control", "Original (winner)", {}),
    ("V1_lost-found-someone", "Lost line: found someone else", dict(lost="never mind, found someone else 🙏")),
    ("V2_lost-signed-up", "Lost line: signed up elsewhere", dict(lost="all good, signed up elsewhere 👍")),
    ("V3_niche-business", "Niche: business coach", dict(handle="jess.buildsbrands", grad="linear-gradient(135deg,#1E9E95,#3797F0)",
        m1="loved your reel on scaling to 10k 🔥", m2="do you still have spots for 1:1?", lost="nvm, signed with another mentor 🙏")),
    ("V4_niche-nutrition", "Niche: nutrition coach", dict(handle="emma.eatswell", grad="linear-gradient(135deg,#F2A33A,#D8541E)",
        m1="your meal plan post was so good 😍", m2="is your program still open?", lost="never mind, joined another program 🙏")),
    ("V5_head-cost-client", "Headline: this DM cost you a client", dict(head="This DM cost you a client.")),
    ("V6_head-how-many", "Headline: how many of these…", dict(head="Coaches: how many of these are in your DMs?")),
]


def page(v):
    d = dict(BASE, **v)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;background:#F1ECE4;font-family:Inter,-apple-system,sans-serif;position:relative;overflow:hidden}}
h1{{position:absolute;left:70px;right:70px;top:300px;text-align:center;font:900 76px/1.08 Inter;letter-spacing:-.055em;color:#1B1B1B}}
.ph{{position:absolute;left:172px;top:560px;width:736px;height:800px;background:#000;border:10px solid #1D1D1D;border-radius:58px;box-shadow:0 30px 60px rgba(60,40,20,.25);padding:38px 34px}}
.hd{{display:flex;align-items:center;gap:18px;padding-bottom:26px;border-bottom:1px solid #2A2A2A}}
.av{{width:62px;height:62px;border-radius:50%;background:{d["grad"]}}}
.hd b{{display:block;color:#fff;font:600 28px Inter}}.hd small{{color:#A8A8A8;font:400 22px Inter}}
.ts{{text-align:center;color:#A8A8A8;font:400 20px Inter;margin:36px 0 16px}}
.b{{display:inline-block;background:#262626;color:#fff;font:400 30px/1.3 Inter;padding:20px 28px;border-radius:40px;margin-bottom:12px;max-width:620px}}
.row{{display:block}}.out{{text-align:right}}.out .b{{background:#3797F0}}
.lost{{position:relative;display:inline-block}}
.lost svg{{position:absolute;left:-30px;top:-22px;width:calc(100% + 60px);height:calc(100% + 34px);overflow:visible}}
.ft{{position:absolute;top:1486px;left:0;right:0;text-align:center;font:800 30px Inter;letter-spacing:-.03em;color:#1B1B1B}}
.ex{{position:absolute;top:1492px;right:56px;font:400 20px Inter;color:#6D665B}}
</style></head><body>
<h1>{d["head"]}</h1>
<div class="ph"><div class="hd"><i class="av"></i><div><b>{d["handle"]}</b><small>{d["seen"]}</small></div></div>
<div class="ts">{d["t1"]}</div><div class="row"><span class="b">{d["m1"]}</span></div><div class="row"><span class="b">{d["m2"]}</span></div>
<div class="ts">{d["t2"]}</div><div class="row"><span class="lost"><span class="b" style="margin:0">{d["lost"]}</span>
<svg viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M50 3 C 82 2, 99 30, 98 50 C 97 78, 70 98, 46 97 C 20 96, 1 78, 2 50 C 3 22, 24 4, 60 6" fill="none" stroke="#E8322D" stroke-width="1.6" vector-effect="non-scaling-stroke" style="stroke-width:5px"/></svg></span></div>
<div class="ts">{d["t3"]}</div><div class="row out"><span class="b">{d["reply"]}</span></div></div>
<div class="ft">DMSetter</div><div class="ex">Example conversation</div>
</body></html>'''


if __name__ == "__main__":
    os.makedirs(os.path.join(here, "html"), exist_ok=True)
    for key, _, v in VARIANTS:
        open(os.path.join(here, "html", key + ".html"), "w").write(page(v))
    print("ok", len(VARIANTS))
