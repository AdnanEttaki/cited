"""Animated story video: Ben ($5K, fitness) vs Mia ($50K, nutrition), same 50 DMs a week.
Multi-voice ElevenLabs dialogue (narrator, Ben, Mia, Lucy), living characters, synced phone messages and bubbles.
  python3 video.py vo    -> one TTS file per line (build/vo/cc_*)
  python3 video.py html  -> video_story.html + timeline_story.json
  node render_video.mjs story && python3 video.py mix  -> out/story_9x16.mp4
"""
import base64, json, os, re, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
studio = os.path.abspath(os.path.join(here, "..", ".."))
build = os.path.join(studio, "build")
B = {"__file__": os.path.join(here, "build.py"), "__name__": "lib"}
exec(open(os.path.join(here, "build.py")).read(), B)          # storyboard components (phone, nametag, say, split, C)
P = {"__file__": os.path.join(studio, "storyboards", "paper-data", "video.py"), "__name__": "lib"}
exec(open(os.path.join(studio, "storyboards", "paper-data", "video.py")).read(), P)  # ANIM_CSS + transitions engine
C, mini, nametag, say, split, phone = B["C"], B["mini"], B["nametag"], B["say"], B["split"], B["phone"]
K, O = B["K"], B["O"]

VOICES = {"narrator": "JBFqnCBsd6RMkjVDRZzb",  # George
          "ben": "iP95p4xoKVk53GoZ742B",       # Chris
          "mia": "EXAVITQu4vr4xnSDxMaL",       # Sarah
          "lucy": "FGY2WhTYpPnrIDTdsKH5"}      # Laura
STYLE = {"narrator": 0.3, "ben": 0.45, "mia": 0.35, "lucy": 0.5}
GAP = 0.1
TEMPO = {"narrator": 1.3, "ben": 1.15, "mia": 1.15, "lucy": 1.15}  # v3 ignores speed -> pitch-preserving atempo
SPEED = {"narrator": 1.15, "ben": 1.08, "mia": 1.08, "lucy": 1.1}
ASK = ("in", "Hey! How do I join?")


def half(side, msgs, exprs, mark, clock=None, extra="", seen=False):
    """exprs: [(expr, line_index_from)] (max 2) — character switches expression on that line."""
    x0 = 0 if side == "l" else 270
    who = "low" if side == "l" else "high"
    layers = "".join(f'<div class="ex ex{j}" data-line="{ln}">{C.char_svg(who, e, 150)}</div>' for j, (e, ln) in enumerate(exprs))
    return (f'<div class="half {side}" style="left:{x0}px">' + nametag(side)
            + (f'<div class="clock {side}">{clock}</div>' if clock else "")
            + mini(msgs, 26, "Lucy", seen=seen)
            + f'<div class="who" data-side="{side}"><div class="bobw">{layers}</div></div>'
            + f'<div class="mark {side}">{"✕" if mark == "x" else "✓"}</div>{extra}</div>')


# Each scene: lines (speaker, text); msgs timing: line index (+ seconds) per message in DOM order (left phone, then right);
# says: line index per speech bubble in DOM order; marks/clocks: line index; fx: extra element timings.
SCENES = [
    dict(label="Meet Ben & Mia", right="50 DMs / week", num="50", hook=True,
         vis=f'<div class="hook-l who" data-side="l"><div class="bobw"><div class="ex ex0" data-line="0">{C.char_svg("low", "tired", 230)}</div></div></div>'
             f'<div class="hook-r who" data-side="r"><div class="bobw"><div class="ex ex0" data-line="0">{C.char_svg("high", "calm", 230)}</div></div></div>'
             + nametag("l", "top:8px;left:24px") + nametag("r", "top:8px;right:24px;left:auto")
             + '<div class="dmc l">50 DMs<small>/ week</small></div><div class="dmc r">50 DMs<small>/ week</small></div><div class="vs">VS</div>',
         cap='Same 50 DMs a week. <span class="hl">Different results.</span>',
         lines=[("narrator", "Ben. Fitness coach. Five K a month. Mia. Nutrition coach. Fifty K. Same fifty DMs a week.")],
         kw={".money.l": ("Ben", 0), ".money.r": ("Mia", 0), ".dmc.l": ("Same", 0), ".dmc.r": ("Same", 0.15), ".vs": ("Mia", -0.4)}),
    dict(label="Round 1 · Speed", right="Score ✓ 1", num="1",
         vis=split(half("l", [ASK], [("asleep", 0), ("stressed", 2)], "x", "14 hrs later", extra=say("l", "Oh no… 14 hours ago.", "BEN")),
                   half("r", [ASK, ("out", "Hey! Love that you reached out 🙌 What's your goal right now?")], [("focused", 0)], "ok", "12 sec")),
         cap='Ben sees it tomorrow. Mia’s DMs answer in <span class="hlo">seconds.</span>',
         lines=[("lucy", "[excited] Hey! How do I join?"), ("narrator", "Ben sees it the next morning."), ("ben", "[yawns] Oh no… fourteen hours ago."),
                ("narrator", "Mia's DMs answer in seconds.")],
         msgs=[0, 0, (3, 0.3)], says=[2], clocks={"l": 1, "r": 3}, marks=3),
    dict(label="Round 2 · First reply", right="Score ✓ 2", num="2",
         vis=split(half("l", [ASK, ("out", "Here's my link 👉 join.link")], [("tired", 0)], "x"),
                   half("r", [ASK, ("out", "Love that! What's the main thing you want to change?"), ("in", "I just want to finally be consistent")], [("calm", 0)], "ok")),
         cap='Ben sends a link. Mia’s DMs <span class="hlo">ask a question.</span>',
         lines=[("narrator", "Ben sends a link. Mia's DMs ask a question."), ("lucy", "[hopeful] I just want to finally be consistent.")],
         msgs=[0, (0, 0.4), 0, (0, 1.5), 1], says=[], marks=1),
    dict(label="Round 3 · The cost question", right="Score ✓ 3", num="3",
         vis=split(half("l", [("in", "How much is it?"), ("out", "Uh… I can do a discount?")], [("tired", 0), ("panic", 1)], "x", extra=say("l", "Uh… discount?", "BEN")),
                   half("r", [("in", "How much is it?"), ("out", "Depends on your goal. Quick call to see if it's a fit?"), ("in", "Sure!")], [("calm", 0), ("happy", 3)], "ok")),
         cap='Mia’s DMs don’t drop a price. They <span class="hlo">book a call.</span>',
         lines=[("lucy", "[curious] How much is it?"), ("ben", "[nervous] Uh… I can do a discount?"), ("narrator", "Mia's DMs don't drop a price. They book a call."), ("lucy", "[happy] Sure!")],
         msgs=[0, 1, 0, (2, 0.6), 3], says=[1], marks=3),
    dict(label="Round 4 · Ghosted", right="Score ✓ 4", num="4",
         vis=split(half("l", [("out", "So… do you want to join?")], [("tired", 0), ("confused", 1)], "x", "no reply", seen=True, extra=say("l", "Guess she’s not interested.", "BEN")),
                   half("r", [("out", "Day 1: still keen to sort this?"), ("out", "Day 3: saved you a spot for Thursday 👀"), ("in", "Omg sorry! Yes, let's do it")],
                        [("coffee", 0), ("happy", 3)], "ok", "day 1 · 3")),
         cap='Ben gives up. Mia’s DMs <span class="hlo">follow up.</span>',
         lines=[("narrator", "Ben gets left on seen… and gives up."), ("ben", "[sighs] Guess she's not interested."),
                ("narrator", "Mia's DMs follow up. Day one. Day three."), ("lucy", "[apologetic] Omg sorry! Yes, let's do it.")],
         msgs=[0, (2, 0.2), (2, 1.4), 3], says=[1], clocks={"l": 0, "r": 2}, marks=3),
    dict(label="Round 5 · The twist", right="Score ✓ 5", num="5", twist=True,
         vis=split(half("l", [("in", "hello??"), ("in", "u there?"), ("in", "still taking clients?")], [("2am", 0)], "x", "02:14 AM",
                        extra=say("l", "Why am I always in my DMs?", "BEN")),
                   half("r", [("in", "Yes, let's do it"), ("out", "Booked ✓ Thursday 3 PM. Mia's excited to meet you!"), ("in", "🙌🙌")], [("asleep", 0)], "ok", "asleep",
                        extra='<div class="setter">HER SETTER</div><div class="stamp2">BOOKED</div>')),
         cap='Mia doesn’t answer her DMs. <span class="hlo">Her setter does.</span>',
         lines=[("narrator", "Two AM. Ben is still typing."), ("ben", "[exhausted] Why am I always in my DMs?"),
                ("narrator", "Mia is asleep. [dramatic pause] Because Mia doesn't answer her DMs… [whispers] her setter does.")],
         msgs=[0, (0, 0.5), (0, 1.0), (2, 0.2), (2, 1.0), (2, 1.6)], says=[1], clocks={"l": 0, "r": 2}, marks=2,
         kw={".setter": ("setter", 0), ".stamp2": ("does.", 0.15)}),
    dict(label="Your turn", right="Now", num="→", cta=True,
         vis='<div class="key press">SETTER</div><div class="cbox"><i></i>Add a comment…<b>&#10148;</b></div>'
             + f'<div class="cta-chr who" data-side="r"><div class="bobw"><div class="ex ex0" data-line="0">{C.char_svg("high", "thumbs", 170)}</div></div></div>'
             + f'<div class="cta-ben who" data-side="l"><div class="bobw"><div class="ex ex0" data-line="0">{C.char_svg("low", "confused", 120)}</div></div></div>'
             + say("r", "Want your DMs handled like mine?", "MIA", "left:250px;top:330px")
             + say("l", "Wait… what’s a setter?", "BEN", "left:8px;top:300px"),
         cap='Comment <span class="hl">"SETTER"</span>',
         lines=[("mia", "[confident] Want your DMs handled like mine? [playful] Comment SETTER."), ("ben", "[confused] Wait… what's a setter? [laughs]")],
         says=[0, 1]),
]


for _i, _s in enumerate(SCENES): _s["key"] = f"s{_i}"


def half_plain(side, msgs, exprs):
    x0 = 0 if side == "l" else 270
    who = "low" if side == "l" else "high"
    layers = "".join(f'<div class="ex ex{j}" data-line="{ln}">{C.char_svg(who, e, 150)}</div>' for j, (e, ln) in enumerate(exprs))
    return (f'<div class="half {side}" style="left:{x0}px">' + nametag(side) + mini(msgs, 26, "Lucy")
            + f'<div class="who" data-side="{side}"><div class="bobw">{layers}</div></div></div>')


ASK_VIS = (split(half_plain("l", [ASK], [("tired", 0)]), half_plain("r", [ASK], [("calm", 0)]))
           + '<div class="askbig" style="--at:-400ms"><b><i></i>LUCY · NEW MESSAGE · TO BOTH</b>Hey! How do I join?</div>')
S0A = dict(key="s0A", label="Same DMs", right="Two coaches", num="?", hook=True, vis=ASK_VIS,
           cap='Same DMs. What happens after <span class="hl">“How do I join?”</span>',
           lines=[("narrator", "Two coaches. Same number of DMs. Ben makes five K a month. Mia makes fifty K. [curious] What happens after…"),
                  ("lucy", "[excited] Hey! How do I join?")],
           msgs=[1, (1, 0.12)], kw={".money.l": ("Ben", 0), ".money.r": ("Mia", 0)})
S0C = dict(key="s0C", label="Meet Ben & Mia", right="Same DMs", num="?", hook=True, vis=ASK_VIS,
           cap='Same DMs. Different coaches. <span class="hl">What happens next?</span>',
           lines=[("narrator", "This is Ben. Fitness coach, five K a month. This is Mia. Nutrition coach, fifty K. Same DMs. [curious] What happens after…"),
                  ("lucy", "[excited] Hey! How do I join?")],
           msgs=[1, (1, 0.12)], kw={".money.l": ("Ben", 0), ".money.r": ("Mia", 0)})
S1N = dict(SCENES[1], key="s1n",
           vis=split(half("l", [ASK], [("asleep", 0), ("stressed", 1)], "x", "14 hrs later", extra=say("l", "Oh no… 14 hours ago.", "BEN")),
                     half("r", [ASK, ("out", "Hey! Love that you reached out 🙌 What's your goal right now?")], [("focused", 0)], "ok", "12 sec")),
           lines=[("narrator", "Ben sees it the next morning."), ("ben", "[yawns] Oh no… fourteen hours ago."), ("narrator", "Mia's DMs answer in seconds.")],
           msgs=[0, 0, (2, 0.3)], says=[1], clocks={"l": 0, "r": 2}, marks=2)
BODY = SCENES[2:]
VARIANTS = {"A": [S0A, S1N] + BODY, "B": SCENES, "C": [S0C, S1N] + BODY}


def lid(key, li):
    return f"cc3_{key}_l{li}"


def cmd_vo():
    os.makedirs(os.path.join(build, "vo"), exist_ok=True)
    uniq = {s["key"]: s for v in VARIANTS.values() for s in v}
    for s in uniq.values():
        for li, (spk, text) in enumerate(s["lines"]):
            p = os.path.join(build, "vo", lid(s["key"], li))
            if os.path.exists(p + ".json"): continue
            body = {"text": text, "model_id": "eleven_v3",
                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": STYLE[spk], "use_speaker_boost": True, "speed": SPEED[spk]}}
            json.dump(body, open(p + ".req", "w"))
            subprocess.run(["curl", "-sS", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[spk]}/with-timestamps?output_format=mp3_44100_128",
                            "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json", "-d", "@" + p + ".req", "-o", p + ".json"], check=True)
            d = json.load(open(p + ".json")); assert "audio_base64" in d, d
            open(p + ".mp3", "wb").write(base64.b64decode(d.pop("audio_base64"))); json.dump(d, open(p + ".json", "w"))
            print(lid(s["key"], li), spk, round(d["alignment"]["character_end_times_seconds"][-1], 2))


def words(al):
    ch, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    out, cur, s0 = [], "", 0
    for i, c in enumerate(ch):
        if c == " ":
            if cur: out.append((cur, s0, en[i - 1]))
            cur = ""
        else:
            if not cur: s0 = st[i]
            cur += c
    if cur: out.append((cur, s0, en[-1]))
    return [w for w in out if not w[0].startswith("[")]  # drop v3 emotion tags


def set_at(html, selector_class, times_ms):
    """Inject --at:<ms> into successive elements carrying class selector_class (exact class token)."""
    it = iter(times_ms)
    def sub(m):
        try: t = next(it)
        except StopIteration: return m.group(0)
        return m.group(0).replace('style="', f'style="--at:{int(t)}ms;', 1) if 'style="' in m.group(0) else m.group(0)[:-1] + f' style="--at:{int(t)}ms">'
    return re.sub(rf'<div class="{selector_class}(?: [^"]*)?"(?: style="[^"]*")?(?: data-line="\d+")?>', sub, html)


def caption_html(cap, wt, shift=0.0):
    parts, pos = [], 0
    for m in re.finditer(r'<span class="(hl|hlo|g)">(.*?)</span>', cap):
        if m.start() > pos: parts.append((cap[pos:m.start()], None))
        parts.append((m.group(2), m.group(1))); pos = m.end()
    if pos < len(cap): parts.append((cap[pos:], None))
    toks = [w for txt, _ in parts for w in txt.split()]
    n, nv = len(toks), len(wt)
    delay = [wt[min(nv - 1, round(k * nv / n))] - shift for k in range(n)]
    out, k = [], 0
    for txt, cls in parts:
        ws = txt.split()
        if not ws: continue
        inner = " ".join(f'<span class="w" style="--wd:{int(delay[k + j] * 1000)}ms">{w}</span>' for j, w in enumerate(ws))
        if cls in ("hl", "hlo"): inner = f'<span class="{cls}" style="--wd:{int(delay[k] * 1000)}ms">{inner}</span>'
        out.append(inner); k += len(ws)
    return " ".join(out)


CSS = """
.mini .m{animation:msgIn .32s cubic-bezier(.2,.9,.3,1.3) calc(var(--at,0ms) - var(--pre)) both}
.mini .seen{animation:fadeIn .3s ease calc(var(--at,0ms) - var(--pre)) both}
.say{animation:pop .42s cubic-bezier(.2,.9,.3,1.6) calc(var(--at,0ms) - var(--pre)) both;transform-origin:30% 100%}
.mark,.clock,.dmc,.vs{animation:pop .45s cubic-bezier(.2,.9,.3,1.6) calc(var(--at,0ms) - var(--pre)) both}
.money{animation:tagIn .5s cubic-bezier(.2,.9,.3,1.3) calc(var(--at,0ms) - var(--pre)) both}
@keyframes tagIn{from{translate:0 -30px;opacity:0}}
.setter{animation:pop .45s cubic-bezier(.2,.9,.3,1.6) calc(var(--at,0ms) - var(--pre)) both}
.stamp2{animation:stamp .32s cubic-bezier(.5,0,.8,.5) calc(var(--at,0ms) - var(--pre)) both}
.who{animation:whoIn .7s cubic-bezier(.2,.9,.3,1.15) calc(var(--at,0ms) - var(--pre)) both}
@keyframes whoIn{from{translate:0 120px;opacity:0}}
.bobw{position:relative}
.ex{transform-origin:50% 100%}
.ex1{position:absolute;left:0;bottom:0}
.ex .chr{animation:breathe 2.8s ease-in-out infinite alternate none;transform-origin:50% 100%}
@keyframes breathe{to{scale:1.012 1.025}}
.eyes{transform-box:fill-box;transform-origin:center;animation:blink 3.4s linear infinite none}
@keyframes blink{0%,93%,100%{scale:1 1}96%{scale:1 .08}}
.ex0.swap{animation:hideAt 1ms linear calc(var(--sw) - var(--pre)) both}
.ex1{animation:showAt 1ms linear calc(var(--sw) - var(--pre)) both}
@keyframes hideAt{from{opacity:1}to{opacity:0}}
@keyframes showAt{from{opacity:0}to{opacity:1}}
.cf{z-index:9}
.askbig{position:absolute;left:50%;top:62px;width:400px;margin-left:-200px;z-index:7;background:#262626;color:#fff;border-radius:26px;padding:16px 22px 18px;
 font:700 34px/1.15 Inter;letter-spacing:-.02em;text-align:center;box-shadow:0 0 0 4px #F2A33A,0 24px 50px rgba(0,0,0,.4);rotate:-2deg;
 animation:pop .5s cubic-bezier(.2,.9,.3,1.6) calc(var(--at,0ms) - var(--pre)) both,bob 2.4s ease-in-out .6s infinite alternate none}
.askbig b{display:flex;align-items:center;justify-content:center;gap:8px;font:800 11px Inter;letter-spacing:.14em;color:#F2A33A;margin-bottom:6px}
.askbig b i{width:10px;height:10px;border-radius:50%;background:#FF3B5C}
.hook-l.who,.hook-r.who,.cta-chr.who,.cta-ben.who{margin-left:0}.hook-r.who,.cta-chr.who{left:auto}
"""


def cmd_html(v="B"):
    SC = VARIANTS[v]
    t, secs, cues, sfx = 0.0, [], [], []
    n = len(SC)
    for si, s in enumerate(SC):
        start = [0.0]; wt_narr, wt_all = [], []
        cur = 0.15 if si else 0.05
        lines = []
        for li, (spk, text) in enumerate(s["lines"]):
            base = os.path.join(build, "vo", lid(s["key"], li)); tp = TEMPO[spk]
            if not os.path.exists(base + "_f.mp3"):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", base + ".mp3", "-filter:a", f"atempo={tp}", base + "_f.mp3"], check=True)
            al = json.load(open(base + ".json"))["alignment"]
            al = {k: ([x / tp for x in v] if k.endswith("_seconds") else v) for k, v in al.items()}
            ws = words(al); dur = al["character_end_times_seconds"][-1]
            lines.append(dict(spk=spk, at=cur, dur=dur, words=[(w, cur + a, cur + b) for w, a, b in ws]))
            cues.append({"id": lid(s["key"], li) + "_f", "at": round(t + cur, 3)})
            if spk == "narrator": wt_narr += [cur + a for _, a, _ in ws]
            wt_all += [cur + a for _, a, _ in ws]
            cur += dur + GAP
        dur = max(2.2, cur + 0.45) + (1.6 if si == n - 1 else 0)
        L = lambda ref: (lines[ref[0]]["at"] + ref[1]) if isinstance(ref, tuple) else lines[ref]["at"]
        vis = s["vis"]
        # phone messages
        if "msgs" in s:
            mt = [L(r) * 1000 for r in s["msgs"]]
            it = iter(mt)
            vis = re.sub(r'<div class="m (in|out)" style="--i:\d+">', lambda m: f'<div class="m {m.group(1)}" style="--at:{int(next(it, mt[-1]))}ms">', vis)
            vis = re.sub(r'<div class="seen" style="--i:\d+">', f'<div class="seen" style="--at:{int(mt[0] + 900)}ms">', vis)
            for k, r in enumerate(s["msgs"]):
                sfx.append({"file": "pop", "at": round(t + L(r), 3), "gain": -12})
        if "says" in s:
            vis = set_at(vis, "say", [lines[i]["at"] * 1000 for i in s["says"]])
        if "clocks" in s:
            ct = [lines[s["clocks"][k]]["at"] * 1000 + 200 for k in ("l", "r") if k in s["clocks"]]
            vis = set_at(vis, "clock", ct)
        if "marks" in s:
            mk = lines[s["marks"]]["at"] * 1000 + 250
            vis = set_at(vis, "mark", [mk, mk + 180])
            sfx.append({"file": "ding", "at": round(t + mk / 1000 + 0.18, 3), "gain": -10})
        for sel, (word, off) in s.get("kw", {}).items():
            cls = sel.split(".")[1]; extra_cls = sel.split(".")[2] if sel.count(".") > 1 else None
            hit = next((b for ln in lines for (w, b, _) in ln["words"] if w.strip(".,…").lower() == word.strip(".").lower()), None)
            if hit is None: continue
            ms = int((hit + off) * 1000)
            pat = rf'<div class="{cls} {extra_cls}"' if extra_cls else rf'<div class="{cls}"'
            vis = re.sub(pat + r'( style="[^"]*")?', lambda m: m.group(0).replace('style="', f'style="--at:{ms}ms;', 1) if m.group(1) else m.group(0) + f' style="--at:{ms}ms"', vis)
            if cls in ("stamp2",): sfx.append({"file": "boom", "at": round(t + ms / 1000 + 0.3, 3), "gain": -8})
            if cls in ("setter",): sfx.append({"file": "pop", "at": round(t + ms / 1000, 3), "gain": -9})
        # expression swaps
        def swap(m):
            return m.group(0)
        def sw_sub(m):
            block = m.group(0)
            lines_idx = [int(x) for x in re.findall(r'class="ex ex\d" data-line="(\d+)"', block)]
            if len(lines_idx) > 1:
                ms = int(lines[lines_idx[1]]["at"] * 1000)
                block = block.replace('class="ex ex0"', f'class="ex ex0 swap" style="--sw:{ms}ms"', 1).replace('class="ex ex1"', f'class="ex ex1" style="--sw:{ms}ms"', 1)
            return block
        vis = re.sub(r'<div class="bobw">.*?</svg></div>(?:<div class="ex ex1".*?</svg></div>)?</div>', sw_sub, vis, flags=re.S)
        # talking windows per side
        talk = {"l": [], "r": []}
        for ln in lines:
            if ln["spk"] in ("ben", "mia"):
                talk["l" if ln["spk"] == "ben" else "r"].append(f'{int(ln["at"] * 1000)}:{int((ln["at"] + ln["dur"]) * 1000)}')
        vis = re.sub(r'class="([^"]*\bwho\b[^"]*)" data-side="(l|r)"', lambda m: f'class="{m.group(1)}" data-side="{m.group(2)}" data-talk="{";".join(talk[m.group(2)])}"', vis)
        if s.get("twist"): vis += P["confetti"](34, 5, int(lines[-1]["at"] * 1000 + lines[-1]["dur"] * 1000 - 600))
        if s.get("cta"): vis += P["confetti"](22, 7, 1100); sfx.append({"file": "click", "at": round(t + 1.1, 3), "gain": -6})
        if s.get("hook"): sfx.append({"file": "boom", "at": 0.0, "gain": -9})
        if si: sfx.append({"file": "whoosh", "at": round(t - 0.12, 3), "gain": -15})
        pre = 300 if s.get("hook") else 0
        wt = wt_narr or wt_all
        cap = caption_html(s["cap"], wt, 10 if s.get("hook") else 0)
        knob = 40 + si * (460 / (n - 1)); prev = 40 + max(0, si - 1) * (460 / (n - 1))
        ticks = "".join(f'<span style="left:{40 + j * (460 / (n - 1))}px">{h}</span>' for j, h in enumerate(B["TICKS"]))
        secs.append(f'''<section class="fr" data-t0="{t:.3f}" style="--dur:{dur:.2f}s;--pre:{pre}ms">
<div class="num">{s["num"]}</div>
<header><div class="rule"></div><span>{s["label"]}</span><em>{s["right"]}</em></header>
<div class="vis">{vis}</div>
<div class="cap">{cap}</div>
<div class="scrub"><div class="line"></div><div class="prog" style="width:{knob - 40}px;--pfrom:{prev - 40}px"></div><div class="fl" style="left:{40 + 5 * (460 / (n - 1))}px"></div>
<div class="knob" style="left:{knob - 9}px;--from:{prev - 9}px"></div>{ticks}<small class="l">A story · example conversations and income figures</small><small class="r">Frame {si + 1} of {n}</small></div>
</section>''')
        t += dur
    css = B["BASE_CSS"] + B["EXTRA_CSS"] + P["ANIM_CSS"] + CSS
    html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Ben vs Mia</title><style>{css}</style></head>
<body><div id="stage">{"".join(secs)}</div>
<script>
const S=[...document.querySelectorAll('.fr')].map(el=>({{el,t0:+el.dataset.t0}}));
window.ready=(async()=>{{await document.fonts.ready;S.forEach(s=>{{s.anims=s.el.getAnimations({{subtree:true}});s.anims.forEach(a=>a.pause());
 s.talk=[...s.el.querySelectorAll('[data-talk]')].map(w=>({{b:w.querySelector('.bobw'),win:(w.dataset.talk||'').split(';').filter(Boolean).map(x=>x.split(':').map(Number))}}));}});}})();
const ease=x=>x>=1?1:1-Math.pow(2,-10*x),TR=.34,TYPES=['left','up','zoom'];
window.render=t=>{{let cur=0;S.forEach((s,i)=>{{if(t>=s.t0)cur=i}});
 const lt=t-S[cur].t0,inT=cur>0&&lt<TR,p=ease(lt/TR),ty=TYPES[cur%3];
 S.forEach((s,i)=>{{const on=i===cur||(inT&&i===cur-1);s.el.classList.toggle('on',on);s.el.style.transform='';s.el.style.filter='';s.el.style.zIndex=i===cur?2:1;
  if(!on)return;const loc=(t-s.t0)*1000;s.anims.forEach(a=>a.currentTime=Math.max(0,loc));
  s.talk.forEach(o=>{{const on2=o.win.some(([a,b])=>loc>=a&&loc<=b);const k=on2?Math.abs(Math.sin(loc/1000*13)):0;
   o.b.style.transform=`translateY(${{-k*5}}px) rotate(${{on2?Math.sin(loc/1000*7)*2:0}}deg) scale(${{1+k*.015}})`;}});}});
 if(inT){{const a=S[cur].el,b=S[cur-1].el;
  if(ty==='left'){{a.style.transform=`translateX(${{(1-p)*100}}%) rotate(${{(1-p)*4}}deg)`;b.style.transform=`translateX(${{-p*60}}%) rotate(${{-p*3}}deg)`;b.style.filter=`blur(${{p*6}}px)`}}
  else if(ty==='up'){{a.style.transform=`translateY(${{(1-p)*100}}%)`;b.style.transform=`translateY(${{-p*40}}%) scale(${{1-p*.1}})`;b.style.filter=`blur(${{p*6}}px)`}}
  else{{a.style.transform=`scale(${{.7+.3*p}})`;a.style.opacity=p;b.style.transform=`scale(${{1+p*.6}})`;b.style.filter=`blur(${{p*10}}px)`}}
 }} else S.forEach(s=>s.el.style.opacity='');}};
</script></body></html>'''
    open(os.path.join(here, f"video_story_{v}.html"), "w").write(html)
    json.dump({"duration": round(t, 3), "fps": 30, "cues": cues, "sfx": sfx}, open(os.path.join(here, f"timeline_story_{v}.json"), "w"), indent=1)
    print(v, "duration", round(t, 2))


def cmd_mix(v="B"):
    T = json.load(open(os.path.join(here, f"timeline_story_{v}.json"))); dur = T["duration"]
    inputs, filt, vo, fx = [], [], [], []
    def inp(p, loop=False):
        if loop: inputs.extend(["-stream_loop", "-1"])
        inputs.extend(["-i", p]); return inputs.count("-i") - 1
    for c in T["cues"]:
        i = inp(os.path.join(build, "vo", c["id"] + ".mp3")); ms = int(c["at"] * 1000)
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]"); vo.append(f"[v{i}]")
    for s in T["sfx"]:
        i = inp(os.path.join(build, "sfx", s["file"] + ".mp3")); ms = int(max(0, s["at"]) * 1000)
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={s['gain']}dB,adelay={ms}|{ms}[x{i}]"); fx.append(f"[x{i}]")
    mi = inp(os.path.join(build, "bed.mp3"), loop=True)
    filt.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},volume=-21dB,afade=t=in:d=0.4,afade=t=out:st={dur - 2}:d=2[mus]")
    filt.append(f"{''.join(vo)}amix=inputs={len(vo)}:normalize=0,asplit=2[vo][vk]")
    filt.append("[mus][vk]sidechaincompress=threshold=0.02:ratio=12:attack=20:release=350[musd]")
    filt.append(f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0[fx]")
    filt.append("[vo]highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,equalizer=f=3500:t=q:w=1:g=2[vop]")
    filt.append(f"[vop][musd][fx]amix=inputs=3:normalize=0,apad,atrim=0:{dur},loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000[out]")
    mix = os.path.join(build, f"cc_mix_{v}.m4a")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-c:a", "aac", "-b:a", "256k", mix], check=True)
    out = os.path.join(here, "out"); os.makedirs(out, exist_ok=True)
    final = os.path.join(out, f"ben_vs_mia_hook{v}_9x16.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(build, f"paper_video_story_{v}.mp4"), "-i", mix, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", final], check=True)
    print("final ->", final)


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "vo": cmd_vo()
    elif c == "html": [cmd_html(v) for v in (sys.argv[2:] or "ABC")]
    elif c == "mix": cmd_mix(sys.argv[2])
