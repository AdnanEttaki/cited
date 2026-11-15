"""Viral-reel remake storyboard: same 21 shots / same timings as the reference (71.6s), DMSetter context.
python3 build.py -> storyboard.html ; node shoot.mjs -> storyboard.jpg + frames/frame_XX.png"""
import os, re, sys

here = os.path.dirname(os.path.abspath(__file__))
studio = os.path.abspath(os.path.join(here, "..", ".."))
pd = os.path.join(studio, "storyboards", "paper-data")
ns = {"__file__": os.path.join(pd, "build.py")}
exec(open(os.path.join(pd, "build.py")).read(), ns)
K, O, T_, A = ns["K"], ns["O"], ns["T"], ns["A"]
phone, PHONE_CSS = ns["phone"], ns["PHONE_CSS"]
LOGO = open(os.path.join(studio, "brand", "logo", "svg", "mark_primary.svg")).read()
HOOK = os.path.join(here, "hook.png")  # Higgsfield hook still (optional)


def logo(px):
    return LOGO.replace('width="260" height="260"', f'width="{px}" height="{px}"')


def cap(parts):
    """parts: list of (text, kind) kind in '', 'o' (orange)"""
    return "".join(f'<span class="{k}">{t}</span>' if k else t for t, k in parts)


def tagc(txt, x, y, rot=0, dark=True):
    return f'<div class="tg {"d" if dark else "l"}" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)">{txt}</div>'


def panel(inner, x=50, y=110, w=440, h=520, extra=""):
    return f'<div class="pn" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{extra}">{inner}</div>'


def lines(n, w="100%"):
    return "".join(f'<i class="ln" style="width:{w if i % 3 else "70%"}"></i>' for i in range(n))


def row(label, sub="", on=False):
    return f'<div class="rw{" on" if on else ""}"><i></i><b>{label}</b><small>{sub}</small></div>'


S = [  # (start, end, caption parts, visual)
    (0.0, 4.5, [("DMSETTER JUST KILLED ", ""), ("UNANSWERED DMS.", "o")],
     (f'<img class="hookimg" src="hook.png">' if os.path.exists(HOOK) else f'<div class="ph3d">3D Instagram logo<br>sliced by the cloud</div><div class="cl" style="left:250px;top:210px">{logo(150)}</div>')),
    (4.5, 6.2, [("NOW, YOU CAN ", ""), ("AUTOMATE ", "o"), ("YOUR ENTIRE INBOX", "")],
     panel("".join(row(n, s, i < 2) for i, (n, s) in enumerate([("your_new_lead", "how much is it?"), ("lead_02", "still taking clients?"), ("lead_03", "saw your post 🔥"), ("lead_04", "can we hop on a call")])) + '<div class="foot">REPLIED, NOT GHOSTED</div>')
     + f'<div class="cl" style="left:12px;top:70px">{logo(110)}</div>' + tagc("IT REPLIES. <b>YOU SLEEP.</b>", 20, 520, -3)),
    (6.2, 8.0, [("AND IT'S ", ""), ("COMPLETELY HANDLED", "o")],
     '<div class="big0">0</div><div class="bigsub">missed DMs</div><div class="tg d" style="left:300px;top:90px;transform:rotate(8deg)">VALUES ILLUSTRATIVE</div>'),
    (8.0, 11.6, [("HERE'S HOW IT WORKS. IT'S CALLED THE ", ""), ("DMSETTER SYSTEM", "o")],
     panel(f'<div class="gh">dmsetter.co / <b>reply-system</b></div>{lines(7)}<div class="rd"><b>The DMSetter reply system</b><br>Thirteen replies that run a coach’s inbox. Qualify, follow up, book. One handles price. One handles ghosting. One books the call.</div>', y=90, h=560)),
    (11.6, 18.9, [("AND IT'S ", ""), ("NOT ONE", "o"), (" REPLY", "")],
     '<div class="cube"><div>/dm-<br>price</div></div>' + tagc("1 of 13", 340, 140, 6, False)),
    (18.9, 22.4, [("THE FIRST ONE ", ""), ("ANSWERS", "o")],
     tagc("/dm-first", 40, 100, -2) + phone([("in", "how much is your coaching?"), ("out", "Hey! Love that you reached out 🙌 What's your goal right now?")], x=130, y=190, rot=-2, w=280, h=330, seen=False, name="New lead")),
    (22.4, 25.0, [("AND IT ", ""), ("QUALIFIES", "o"), (" THE LEAD", "")],
     tagc("/dm-qualify", 40, 100, -2) + panel('<div class="q">“Goal? Timeline? Budget fit?”<br><small>Asked in a natural DM, never a form.</small></div>', y=210, h=200)),
    (25.0, 28.3, [("ANOTHER ONE ", ""), ("FOLLOWS UP", "o")],
     tagc("/dm-followup", 40, 100, -2) + phone([("out", "Hey, still thinking it over?"), ("in", "yes, sorry, busy week!")], x=130, y=190, rot=2, w=280, h=300, seen=False, name="New lead")),
    (28.3, 30.9, [("ONE ", ""), ("HANDLES OBJECTIONS", "o")],
     phone([("in", "I need to think about it"), ("out", "Totally fair. What would make it an easy yes?")], x=120, y=130, rot=-2, w=300, h=340, seen=False, name="New lead", hl=1) + tagc("/dm-objection", 280, 60, 5)),
    (30.9, 33.6, [("ONE ", ""), ("SCORES", "o"), (" EVERY LEAD", "")],
     panel('<div class="sc"><b>lead_02</b><div class="meter"><i style="width:82%"></i></div><small>HOT · 82 / 100</small></div><div class="sc"><b>lead_03</b><div class="meter"><i style="width:48%"></i></div><small>WARM · 48 / 100</small></div>', y=130, h=330) + tagc("/dm-score", 300, 70, 6)),
    (33.6, 35.7, [("AND ONE ", ""), ("BOOKS YOUR WEEK", "o")],
     panel('<div class="wk">' + "".join(f'<div><small>{d}</small><i class="{"b" if d in ("TUE", "THU") else ""}">{"CALL" if d in ("TUE", "THU") else ""}</i></div>' for d in ["MON", "TUE", "WED", "THU", "FRI"]) + '</div><div class="foot">+ 3 CALLS BOOKED, THIS WEEK</div>', y=150, h=330) + tagc("/dm-book", 300, 80, 6)),
    (35.7, 38.9, [("WHAT TO SAY, WHEN, ", ""), ("TO WHO", "o")],
     panel('<div class="tp"><small>WHAT</small><b>Reply</b><small>WHEN</small><b>Within seconds</b><small>WHO</small><b>Every lead</b></div>', y=130, h=330)),
    (38.9, 41.0, [("SO, YOU NEVER HAVE TO ", ""), ("TYPE", "o")],
     '<div class="qm">?</div>' + tagc("/dm-reply", 50, 360, -3, False)),
    (41.0, 45.7, [("BUT THEN, THERE'S THE ", ""), ("FULL SET", "o")],
     '<div class="grid13">' + "".join(f'<div class="g{" k" if i % 3 == 0 else ""}">/dm-{n}</div>' for i, n in enumerate(["price", "first", "qualify", "followup", "objection", "score", "book", "reengage", "booking", "noshow", "intro", "story", "close"])) + '</div>'),
    (45.7, 47.6, [("IT GOES THROUGH ", ""), ("EVERY INBOX", "o")],
     panel("".join(row(n, s) for n, s in [("lead_01", "in 38 sec"), ("lead_02", "in 41 sec"), ("lead_03", "in 29 sec")]), y=150, h=330) + '<div class="tg d" style="left:60px;top:90px">YOU PICK 0 – 12 CHATS</div>'),
    (47.6, 51.0, [("RANKS THE LEADS BY ", ""), ("HOW READY THEY ARE", "o")],
     panel('<div class="bars"><i style="height:85%"></i><i style="height:60%"></i><i style="height:42%"></i><i style="height:25%"></i></div><div class="foot">EACH BAR = ONE LEAD</div>', y=130, h=360)),
    (51.0, 53.0, [("AND NAMES THE ", ""), ("BEST REPLY", "o")],
     panel('<div class="hb"><span>7.4×</span> “Quick question: what’s your goal?”</div><div class="hb l"><span>5.1×</span> “Hey! Still keen?”</div>', y=170, h=260)),
    (53.0, 57.7, [("THEN, IT TAKES THOSE ", ""), ("REPLIES", "o"), (" AND SENDS THEM", "")],
     panel('<div class="qq"><b>#1 Replies in seconds</b><br>“Quick question: what’s your goal right now?”</div>', y=190, h=240)),
    (57.7, 62.3, [("NO MORE ", ""), ("STAYING UP", "o"), (" FOR", "")],
     '<div class="sk"><i></i><i></i><i></i></div><div class="moon">🌙</div>'),
    (62.3, 67.4, [("AND THE SETUP IS ", ""), ("EASY", "o")],
     panel('<div class="st"><span>1</span> Connect your Instagram</div><div class="st"><span>2</span> Pick your replies</div><div class="st"><span>3</span> Wake up to booked calls</div>', y=210, h=220)),
    (67.4, 71.6, [("IF YOU WANT THE FULL SET, ", ""), ("COMMENT “SCRIPT”", "o")],
     f'<div class="cl" style="left:150px;top:150px">{logo(240)}</div><div class="wm2">DM<span>Setter</span></div>'),
]

CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{display:grid;grid-template-columns:repeat(7,540px);gap:6px;background:#bbb;font-family:Inter,sans-serif;width:{7 * 546}px}}
.fr{{position:relative;width:540px;height:960px;overflow:hidden;background:radial-gradient(120% 90% at 50% 35%,#F7F2E9 0%,#ECE6DA 70%,#E2DBCD 100%)}}
.fr::before{{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.035) 0 1px,transparent 1px 36px),repeating-linear-gradient(90deg,rgba(0,0,0,.035) 0 1px,transparent 1px 36px)}}
.scrub{{position:absolute;left:28px;right:28px;top:40px;height:22px;border:2px solid {K};border-radius:5px;background:#fff;display:flex;gap:3px;padding:3px;z-index:5}}
.scrub i{{flex:1;border:1.5px solid {K};border-radius:2px;background:#fff}}.scrub i.on{{background:{K}}}.scrub i.o{{background:{O};border-color:{O}}}
.vis{{position:absolute;left:0;right:0;top:120px;height:640px}}
.cap{{position:absolute;left:30px;right:30px;top:790px;text-align:center;z-index:6}}
.cap b{{display:inline;font:900 26px/1.55 Inter;background:#fff;border:3px solid {K};box-shadow:5px 5px 0 {K};padding:3px 10px;-webkit-box-decoration-break:clone;box-decoration-break:clone;letter-spacing:-.01em}}
.cap .o{{color:{O}}}
.time{{position:absolute;left:12px;bottom:10px;font:700 12px Inter;color:#6D665B;background:rgba(255,255,255,.7);padding:3px 8px;border-radius:8px;z-index:9}}
.pn{{position:absolute;background:#FBFAF6;border:3px solid {K};border-radius:6px;box-shadow:7px 7px 0 rgba(0,0,0,.2);padding:18px;overflow:hidden}}
.ln{{display:block;height:8px;background:#D9D4C7;border-radius:4px;margin:12px 0}}
.rw{{display:flex;align-items:center;gap:12px;padding:12px;border:2px solid #cfc8b8;border-radius:8px;margin-bottom:12px;background:#fff}}.rw.on{{border-color:{O}}}
.rw i{{width:34px;height:34px;border-radius:50%;background:#8a9bb0;flex:none}}.rw b{{font:800 15px Inter}}.rw small{{margin-left:auto;font:600 12px Inter;color:#8a8372}}
.foot{{position:absolute;left:18px;right:18px;bottom:16px;text-align:center;background:#EFEADD;border:2px solid #cfc8b8;border-radius:6px;font:800 13px Inter;padding:9px;letter-spacing:.06em}}
.tg{{position:absolute;z-index:8;padding:7px 12px;font:800 14px Inter;border-radius:4px;box-shadow:0 4px 0 rgba(0,0,0,.2)}}
.tg.d{{background:{O};color:#fff}}.tg.l{{background:#fff;color:{K};border:2px solid {K}}}.tg b{{color:{K}}}
.cl{{position:absolute;z-index:7;filter:drop-shadow(0 10px 14px rgba(0,0,0,.25))}}
.hookimg{{position:absolute;left:50%;top:0;height:640px;transform:translateX(-50%);border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.25)}}
.ph3d{{position:absolute;left:90px;top:130px;width:300px;height:300px;border-radius:70px;background:linear-gradient(135deg,#515BD4,#DD2A7B,#F58529);color:#fff;font:800 18px/1.3 Inter;display:grid;place-items:center;text-align:center}}
.big0{{position:absolute;left:0;right:0;top:100px;text-align:center;font:900 300px/1 Inter;color:{K};transform:rotate(-4deg)}}
.bigsub{{position:absolute;left:0;right:0;top:420px;text-align:center;font:800 38px Inter;color:{O}}}
.gh{{font:700 15px Inter;color:#555;margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid #D9D4C7}}.rd{{font:600 15px/1.5 Inter;margin-top:16px}}
.cube{{position:absolute;left:120px;top:110px;width:300px;height:300px;background:{K};border-radius:10px;transform:rotate(-8deg);box-shadow:14px 14px 0 rgba(0,0,0,.25);display:grid;place-items:center}}
.cube div{{width:230px;height:200px;background:#fff;transform:rotate(-6deg);display:grid;place-items:center;font:900 34px/1.1 Inter;text-align:center}}
.q{{font:800 24px/1.4 Inter}}.q small{{font:600 15px Inter;color:#8a8372}}
.sc{{margin-bottom:26px}}.sc b{{font:800 18px Inter}}.sc small{{font:800 12px Inter;color:{O}}}.meter{{height:18px;border:2px solid {K};border-radius:9px;margin:8px 0;overflow:hidden;background:#fff}}.meter i{{display:block;height:100%;background:{O}}}
.wk{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;height:80%}}.wk div{{display:flex;flex-direction:column;gap:6px}}.wk small{{font:800 11px Inter;text-align:center;color:#8a8372}}
.wk i{{flex:1;border:2px solid #cfc8b8;border-radius:6px;background:#fff;font:900 12px Inter;font-style:normal;display:grid;place-items:center;color:#fff}}.wk i.b{{background:{O};border-color:{O}}}
.tp small{{display:block;font:800 13px Inter;letter-spacing:.12em;color:#8a8372;margin-top:20px}}.tp b{{display:block;font:900 28px Inter;margin-top:6px}}
.qm{{position:absolute;left:150px;top:60px;width:240px;height:260px;background:#fff;border:3px solid {K};box-shadow:8px 8px 0 rgba(0,0,0,.2);display:grid;place-items:center;font:900 150px Inter;color:#8a8372}}
.grid13{{position:absolute;left:30px;right:30px;top:20px;display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.g{{padding:30px 6px;background:#fff;border:3px solid {K};border-radius:6px;font:800 14px Inter;text-align:center;box-shadow:4px 4px 0 rgba(0,0,0,.2);transform:rotate(-2deg)}}.g.k{{background:{K};color:#fff;transform:rotate(2deg)}}
.bars{{display:flex;align-items:flex-end;gap:18px;height:85%;padding:10px 20px}}.bars i{{flex:1;background:{O};border:3px solid {K};box-shadow:5px 5px 0 rgba(0,0,0,.2)}}
.hb{{font:700 17px/1.4 Inter;padding:16px;border:2.5px solid {K};background:#fff;margin-bottom:14px;box-shadow:4px 4px 0 rgba(0,0,0,.18)}}.hb span{{background:{O};color:#fff;padding:2px 8px;font-weight:900;margin-right:8px}}.hb.l span{{background:#E6B8A8}}
.qq{{font:700 20px/1.5 Inter}}.qq b{{color:{O}}}
.sk{{position:absolute;left:150px;top:30px;width:240px}}.sk i{{display:block;height:120px;background:#E4DFD2;border:2px solid #cfc8b8;margin-bottom:12px}}.moon{{position:absolute;left:340px;top:20px;font-size:90px}}
.st{{font:800 22px Inter;margin-bottom:22px;display:flex;gap:14px;align-items:center}}.st span{{width:38px;height:38px;border-radius:50%;background:{O};color:#fff;display:grid;place-items:center;font:900 20px Inter;flex:none}}
.wm2{{position:absolute;left:0;right:0;top:420px;text-align:center;font:900 64px Inter;letter-spacing:-.04em;color:{K}}}.wm2 span{{color:{O}}}
{PHONE_CSS}
"""


def frame(i, s):
    a, b, c, v = s
    n = len(S)
    sc = "".join(f'<i class="{"on" if j < i else "o" if j == i else ""}"></i>' for j, _ in enumerate(S))
    return f'<section class="fr"><div class="scrub">{sc}</div><div class="vis">{v}</div><div class="cap"><b>{cap(c)}</b></div><div class="time">#{i + 1} · {a:.1f}–{b:.1f}s</div></section>'


html = f'<!doctype html><html><head><meta charset="utf-8"><title>Viral remake</title><style>{CSS}</style></head><body>{"".join(frame(i, s) for i, s in enumerate(S))}</body></html>'

if __name__ == "__main__":
    open(os.path.join(here, "storyboard.html"), "w").write(html)
    print("ok", len(S), "shots")
