"""'The Race' Reel storyboard: 5 coaches (different niches), one lead at 11 PM, first reply wins. Same paper frame branding.
python3 build.py -> storyboard.html ; node shoot.mjs -> storyboard.jpg + frames/"""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(here, "..", "viral-remake")
NS = {"__file__": os.path.join(V, "build.py"), "__name__": "lib"}
exec(open(os.path.join(V, "build.py")).read(), NS)
K, O, T_, A = NS["K"], NS["O"], NS["T"] if "T" in NS else "#1E9E95", NS["A"]
phone, panel, tagc, logo, cap, BASE = NS["phone"], NS["panel"], NS["tagc"], NS["logo"], NS["cap"], NS["CSS"]
NICHES = [("Business", "💼"), ("Mindset", "🧠"), ("Career", "🚀"), ("Relationship", "💬"), ("Nutrition", "🥗")]


def coach(i, name, ico, state, timer, win=False, x=0, y=0, rot=0):
    return (f'<div class="cc{" win" if win else ""}" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)"><div class="ci">{ico}</div>'
            f'<b>{name} coach</b><div class="tm">{timer}</div><small>{state}</small></div>')


def cards(states, timers, win=-1, dyn=False):
    pos = [(20, 20, -3), (190, 0, 2), (360, 24, -2), (70, 250, 2), (280, 262, -3)]
    out = ""
    for i, (n, ico) in enumerate(NICHES):
        x, y, r = pos[i]
        w = i == win
        c = coach(i, n if not w else "DMSetter", ico if not w else logo(52), states[i], timers[i], w, x, y, r)
        if dyn: c = c.replace('class="tm"', f'class="tm" data-k="{"win" if w else "slow"}"')
        out += c
    return out


S = [
 (0, 4, [("A LEAD MESSAGED ", ""), ("FIVE COACHES", "o"), (" AT 11 PM.", ""), (" ONLY ONE GOT THE CALL.", "")],
  phone([("out", "Hi! How does your coaching work? 🙌")], x=150, y=30, rot=-3, w=240, h=250, seen=False, name="New lead")
  + '<div class="fan">' + "".join(f'<i style="--r:{r}deg;left:{x}px">{e}</i>' for (r, x, e) in [(-30, 40, "💼"), (-15, 130, "🧠"), (0, 220, "🚀"), (15, 310, "💬"), (30, 400, "🥗")]) + '</div>'
  + tagc("11:41 PM", 40, 20, -5)),
 (4, 9, [("SAME MESSAGE. SAME MINUTE. ", ""), ("FIVE DIFFERENT COACHES.", "o")],
  cards(["waiting…"] * 5, ["0:00"] * 5)),
 (9, 16, [("FOUR WERE ", ""), ("ASLEEP OR BUSY.", "o"), (" ONE REPLIED IN ", ""), ("38 SECONDS.", "o")],
  cards(["😴 asleep", "✈ on a flight", "🍽 at dinner", "📞 in a call", "replied ✓"], ["9:14", "9:14", "9:14", "9:14", "0:38"], win=4, dyn=True)),
 (16, 22, [("SHE DIDN'T PICK THE BEST. ", ""), ("SHE PICKED THE FIRST.", "o")],
  phone([("in", "Hi! How does your coaching work? 🙌"), ("out", "Hey! Love that you reached out 🙌 What's your goal right now?"), ("in", "grow my client list"), ("out", "Got you. Quick call tomorrow 3 PM to see if it's a fit?")], x=80, y=20, rot=-2, w=290, h=420, seen=False, name="New lead", hl=1)
  + f'<div class="cl" style="left:350px;top:20px">{logo(120)}</div>' + tagc("FIRST TO ANSWER", 330, 170, 6)),
 (22, 27, [("BY MORNING, THE CALL WAS ", ""), ("BOOKED.", "o")],
  panel('<div class="wk">' + "".join(f'<div><small>{d}</small><i class="{"b" if d == "THU" else ""}">{"CALL" if d == "THU" else ""}</i></div>' for d in ["MON", "TUE", "WED", "THU", "FRI"]) + '</div><div class="foot">BOOKED WHILE YOU SLEPT</div>', y=120, h=320)
  + '<div class="stampb">BOOKED</div>' + tagc("VALUES ILLUSTRATIVE", 300, 60, 6)),
 (27, 31, [("THE OTHER FOUR REPLIED IN THE MORNING. ", ""), ("TOO LATE.", "o")],
  phone([("in", "Hi! How does your coaching work? 🙌"), ("in", "Thanks, but I already booked with another coach 🙏"), ("out", "Sorry, just saw this…")], x=130, y=40, rot=2, w=280, h=330, seen=False, name="New lead", hl=1)
  + '<div class="tg d" style="left:40px;top:330px;transform:rotate(-4deg)">9:02 AM</div>'),
 (31, 35, [("COMMENT ", ""), ("“SPEED”", "o"), (" AND I'LL SEND YOU THE REPLIES THAT WIN.", "")],
  f'<div class="cl" style="left:150px;top:90px">{logo(240)}</div><div class="wm2" style="top:380px">DM<span>Setter</span></div>' + '<div class="cbox2">SPEED &#10148;</div>'),
]

CSS = BASE + f"""
.cc{{position:absolute;width:150px;height:200px;background:#FBFAF6;border:3px solid {K};border-radius:8px;box-shadow:6px 6px 0 rgba(0,0,0,.2);padding:14px;text-align:center}}
.cc.win{{border-color:{O};background:#FFF5EE;box-shadow:6px 6px 0 {O}}}
.ci{{font-size:44px;margin-top:4px}}.cc b{{display:block;font:800 13px Inter;margin-top:8px}}
.tm{{font:900 32px Inter;color:{K};margin-top:10px;font-variant-numeric:tabular-nums}}.cc.win .tm{{color:{O}}}.cc small{{display:block;font:700 12px Inter;color:#8a8372;margin-top:6px}}
.cc.win small{{color:{O}}}
.fan i{{position:absolute;top:330px;width:70px;height:90px;background:#fff;border:3px solid {K};border-radius:8px;font-style:normal;font-size:34px;display:grid;place-items:center;transform:rotate(var(--r));box-shadow:4px 4px 0 rgba(0,0,0,.2)}}
.wk{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;height:80%}}.wk div{{display:flex;flex-direction:column;gap:6px}}.wk small{{font:800 11px Inter;text-align:center;color:#8a8372}}
.wk i{{flex:1;border:2px solid #cfc8b8;border-radius:6px;background:#fff;font:900 12px Inter;font-style:normal;display:grid;place-items:center;color:#fff}}.wk i.b{{background:{O};border-color:{O}}}
.stampb{{position:absolute;left:140px;top:430px;z-index:9;padding:4px 14px;border:5px solid {O};color:{O};font:900 40px Inter;border-radius:10px;transform:rotate(-10deg);background:rgba(244,240,232,.9)}}
.cbox2{{position:absolute;left:100px;right:100px;top:500px;background:#fff;border:3px solid {K};border-radius:30px;padding:14px 22px;font:800 22px Inter;box-shadow:5px 5px 0 rgba(0,0,0,.2)}}
"""


def frame(i, s):
    a, b, c, v = s
    sc = "".join(f'<i class="{"on" if j < i else "o" if j == i else ""}"></i>' for j in range(len(S)))
    return f'<section class="fr"><div class="scrub">{sc}</div><div class="vis">{v}</div><div class="cap"><b>{cap(c)}</b></div><div class="time">#{i + 1} · {a}–{b}s</div></section>'


html = f'<!doctype html><html><head><meta charset="utf-8"><title>The Race</title><style>{CSS}body{{grid-template-columns:repeat(4,540px);width:{4 * 546}px}}</style></head><body>{"".join(frame(i, s) for i, s in enumerate(S))}</body></html>'
if __name__ == "__main__":
    open(os.path.join(here, "storyboard.html"), "w").write(html); print("ok", len(S))
