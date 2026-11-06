"""Animated paper-style videos: one shared body (storyboard frames 2-12) + one hook per video.
Steps:  python3 video.py vo        -> ElevenLabs VO per scene (build/vo/paper_*.mp3/json)
        python3 video.py html      -> video_<hook>.html + timeline_<hook>.json for hooks A, B, C
then    node render_video.mjs <hook> ; python3 video.py mix <hook>
"""
import json, os, re, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
studio = os.path.abspath(os.path.join(here, "..", ".."))
build = os.path.join(studio, "build")
ns = {"__file__": os.path.join(here, "build.py")}
exec(open(os.path.join(here, "build.py")).read(), ns)  # storyboard components + frames
K, O, T_, M, A = ns["K"], ns["O"], ns["T"], ns["M"], ns["A"]
bar, tag, frames = ns["bar"], ns["tag"], ns["frames"]
BASE_CSS = re.search(r"<style>(.*?)</style>", ns["html"], re.S).group(1)
VOICE = "EXAVITQu4vr4xnSDxMaL"  # Sarah

DMS = ["still taking clients?", "how does it work?", "saw your post 🔥", "is this for beginners?", "can we hop on a call",
       "how do I start?", "u there?", "interested!!"]
COLS = [K, O, T_, M, A, K, O, T_]


def stack(fall=False):
    return "".join(
        f'<div class="row" style="top:{30 + i * 54}px;left:{-30 + (i % 3) * 14}px">'
        + bar(470 - (i % 4) * 30, COLS[i], 50, inner=f'<span class="dm"><em></em>{DMS[i]}</span>',
              z=f"--f:{7 - i};" if fall else "").replace('class="bar"', 'class="bar fall"' if fall else 'class="bar"') + '</div>'
        for i in range(8))


HOOKS = {
    "A": dict(label="Unread DMs", right="02:14 AM", num="12",
              vis=stack() + '<div class="badge" style="left:430px;top:6px">12</div>'
                  + '<div class="tag xl" style="left:22px;top:-14px;background:#D8541E;transform:rotate(-4deg)">FOR COACHES</div>',
              cap='<span class="hl">12 DMs</span> at 2&nbsp;AM. You\'re <span class="hlo">asleep.</span>',
              vo="Twelve DMs at 2 AM. You're asleep."),
    "B": dict(label="Your DMs", right="Right now", num="↓",
              vis=stack(fall=True) + '<div class="badge" style="left:430px;top:6px">48</div>',
              cap='Stop posting more content. Your DMs are <span class="hlo">leaking clients.</span>',
              vo="Stop posting more content. Your DMs are leaking clients."),
    "C": dict(label="Speed to lead", right="HBR · 2011", num="7×",
              vis=f'<div class="lbl" style="top:40px">ANSWERED WITHIN 1 HOUR</div><div class="row" style="top:66px;left:-20px">{bar(490, O, 96, inner="<span class=\'huge pl\'>7×</span>")}</div>'
                  f'<div class="lbl" style="top:230px">AN HOUR LATER</div><div class="row" style="top:256px;left:-20px">{bar(130, K, 96, inner="<span class=\'huge pl\'>1×</span>")}</div>'
                  + tag("Harvard Business Review, 2011", T_, 190, 390, -3),
              cap='Reply within an hour. <span class="hl">7×</span> more real conversations.',
              vo="Reply within an hour. Seven-times more real conversations."),
}
BODY_VO = ["You reply in six hours. We reply in minutes.", "Every lead gets a real conversation.",
           "The cost question? Handled.", "We qualify them first.", "Three slots. They pick one.",
           "Booked. Hands-free.", "No missed leads.", "No lead left on read.", 'Comment "SETTER",',
           "and we'll DM you.", "Your DMs, handled."]
# per-scene sound design: (offset seconds, sfx, gain dB)
BODY_SFX = [[(0.12, "whoosh", -16), (0.55, "pop", -12)], [(0.35, "pop", -13), (0.73, "pop", -13), (1.11, "pop", -13)],
            [(0.35, "pop", -13), (0.73, "pop", -13), (1.11, "pop", -13)], [(0.2, "ding", -12), (0.5, "ding", -13), (0.8, "ding", -14), (1.1, "ding", -15)],
            [(0.35, "pop", -13), (0.73, "pop", -13), (1.11, "pop", -13), (1.49, "pop", -13), (1.9, "ding", -9)],
            [(0.55, "boom", -8)], [(0.2, "whoosh", -16), (0.8, "ding", -12)], [(0.6, "pop", -12)],
            [(0.15, "whoosh", -14), (1.1, "click", -6)], [(0.35, "pop", -12), (0.73, "pop", -12), (1.1, "pop", -12)],
            [(0.2, "boom", -9), (0.7, "ding", -10)]]
HOOK_SFX = {"A": [(0.0, "boom", -7), (0.3, "pop", -12)], "B": [(0.0, "boom", -7), (1.4, "whoosh", -12)],
            "C": [(0.0, "boom", -7), (0.4, "riser", -16)]}

ANIM_CSS = """
#stage{width:540px;height:960px;zoom:2;position:relative;overflow:hidden;background:#ECE6DA}
body{width:1080px;height:1920px;padding:0;display:block;background:#ECE6DA}
.fr{position:absolute;inset:0;opacity:0}
.fr.on{opacity:1}
.fr *{animation-fill-mode:both;animation-play-state:paused}
.fr{animation:push var(--dur) linear both paused}
@keyframes push{from{scale:1}to{scale:1.06}}
.num{animation:numIn .9s cubic-bezier(.2,.8,.2,1) calc(0ms - var(--pre)) both}
@keyframes numIn{from{translate:0 80px;opacity:0}}
header{animation:fadeIn .5s ease calc(0ms - var(--pre)) both}
@keyframes fadeIn{from{opacity:0;translate:0 -8px}}
.row{animation:barIn .7s cubic-bezier(.2,.9,.3,1.12) calc(var(--k,0)*70ms + 80ms - var(--pre)) both}
@keyframes barIn{from{translate:-115% 0}}
.bar.fall{animation:fall .65s cubic-bezier(.5,0,.9,.4) calc(1300ms + var(--f,0)*110ms - var(--pre)) both}
@keyframes fall{to{translate:60px 900px;rotate:24deg;opacity:.0}}
.lbl{animation:fadeIn .4s ease calc(var(--k,0)*150ms - var(--pre)) both}
.ph{animation:phIn .75s cubic-bezier(.2,.9,.3,1.1) calc(40ms - var(--pre)) both}
@keyframes phIn{from{translate:0 140px;opacity:0;scale:.9}}
.card{animation:phIn .7s cubic-bezier(.2,.9,.3,1.1) calc(var(--k,0)*150ms + 40ms - var(--pre)) both}
.m{animation:msgIn .32s cubic-bezier(.2,.9,.3,1.3) calc(350ms + var(--i,0)*380ms - var(--pre)) both}
.seen{animation:fadeIn .3s ease calc(350ms + var(--i,0)*380ms - var(--pre)) both}
@keyframes msgIn{from{opacity:0;translate:0 14px;scale:.85}}
.badge{animation:pop .45s cubic-bezier(.2,.9,.3,1.6) calc(320ms - var(--pre)) both}
.tag{animation:pop .45s cubic-bezier(.2,.9,.3,1.6) calc(var(--k,0)*160ms + 650ms - var(--pre)) both}
.tag.xl{font-size:22px;padding:10px 16px 10px 28px;animation-delay:calc(150ms - var(--pre))}
@keyframes pop{from{scale:0;opacity:0}}
.slot{animation:phIn .6s cubic-bezier(.2,.9,.3,1.2) calc(var(--k,0)*120ms + 80ms - var(--pre)) both}
.flag{animation:pop .4s cubic-bezier(.2,.9,.3,1.6) calc(1950ms - var(--pre)) both}
.stamp{animation:stamp .32s cubic-bezier(.5,0,.8,.5) calc(520ms - var(--pre)) both}
@keyframes stamp{from{scale:2.8;opacity:0}}
.vis.shake{animation:shake .45s linear calc(840ms - var(--pre)) both}
@keyframes shake{0%,100%{translate:0 0}15%{translate:-7px 4px}30%{translate:6px -5px}45%{translate:-5px 3px}60%{translate:4px -2px}80%{translate:-2px 1px}}
.col{transform-origin:bottom;animation:grow .6s cubic-bezier(.2,.9,.3,1.1) calc(var(--k,0)*90ms + 100ms - var(--pre)) both}
@keyframes grow{from{scale:1 0}}
.cut{animation:fadeIn .4s ease calc(800ms - var(--pre)) both}
.key{animation:keyIn .6s cubic-bezier(.2,.9,.3,1.2) calc(60ms - var(--pre)) both}
@keyframes keyIn{from{translate:0 -60px;opacity:0}}
.key.press{animation:keyIn .6s cubic-bezier(.2,.9,.3,1.2) calc(60ms - var(--pre)) both,press .28s ease calc(1050ms - var(--pre)) both}
@keyframes press{50%{scale:.94 .9}}
.cbox{animation:fadeUp .5s ease calc(450ms - var(--pre)) both}
@keyframes fadeUp{from{opacity:0;translate:0 20px}}
.huge{font:900 64px Inter;letter-spacing:-.04em}
.cap{z-index:5}
.ph,.card,.slot.up,.key{animation-composition:replace}
.ph{animation:phIn .75s cubic-bezier(.2,.9,.3,1.1) calc(40ms - var(--pre)) both,bob 2.6s ease-in-out calc(800ms - var(--pre)) infinite alternate none}
.card{animation:phIn .7s cubic-bezier(.2,.9,.3,1.1) calc(var(--k,0)*150ms + 40ms - var(--pre)) both,bob 2.2s ease-in-out calc(800ms - var(--pre)) infinite alternate none}
.tag{animation:pop .45s cubic-bezier(.2,.9,.3,1.6) calc(var(--k,0)*160ms + 650ms - var(--pre)) both,wig 1.4s ease-in-out calc(1100ms - var(--pre)) infinite alternate none}
.tag.xl{animation:pop .45s cubic-bezier(.2,.9,.3,1.6) calc(150ms - var(--pre)) both,wig 1.2s ease-in-out calc(600ms - var(--pre)) infinite alternate none}
.badge{animation:pop .45s cubic-bezier(.2,.9,.3,1.6) calc(320ms - var(--pre)) both,beat .9s ease-in-out calc(800ms - var(--pre)) infinite none}
@keyframes bob{from{rotate:-.9deg}to{rotate:.9deg}}
@keyframes wig{from{rotate:-3deg}to{rotate:3deg}}
@keyframes beat{0%,100%{scale:1}15%{scale:1.14}30%{scale:1}}
.b.hl{animation:glow 1s ease-in-out calc(700ms + var(--i,0)*380ms - var(--pre)) infinite alternate none}
@keyframes glow{to{box-shadow:0 0 0 3.5px #F2A33A,0 0 34px rgba(242,163,58,.9)}}
.num{animation:numIn .9s cubic-bezier(.2,.8,.2,1) calc(0ms - var(--pre)) both,drift 4s linear calc(900ms - var(--pre)) infinite alternate none}
@keyframes drift{to{translate:-26px 0}}
.row{animation:barIn .7s cubic-bezier(.2,.9,.3,1.12) calc(var(--k,0)*70ms + 80ms - var(--pre)) both,sway 2.4s ease-in-out calc(900ms + var(--k,0)*90ms - var(--pre)) infinite alternate none}
@keyframes sway{to{translate:10px 0}}
.wipe{position:absolute;inset:-10%;z-index:20;pointer-events:none;opacity:0}
.cf{position:absolute;left:50%;top:45%;width:9px;height:14px;border-radius:2px;background:var(--c);z-index:6;
 animation:conf 1.3s cubic-bezier(.15,.7,.4,1) calc(var(--cd) - var(--pre)) both}
@keyframes conf{from{translate:0 0;rotate:0deg;opacity:1}75%{opacity:1}to{translate:var(--x) var(--y);rotate:var(--r);opacity:0}}
.key.press::after{content:"";position:absolute;left:50%;top:50%;width:40px;height:40px;margin:-20px;border-radius:50%;border:4px solid #fff;animation:ripple .6s ease-out calc(1080ms - var(--pre)) both}
@keyframes ripple{from{scale:.2;opacity:.9}to{scale:9;opacity:0}}

.w{display:inline-block;animation:wordIn .26s cubic-bezier(.2,.9,.3,1.3) var(--wd) both}
@keyframes wordIn{from{opacity:0;translate:0 18px;scale:.6}}
.hl,.hlo{background:linear-gradient(var(--hb),var(--hb)) no-repeat 0 0/0% 100%;color:#1B1B1B;animation:wipe .3s ease var(--wd) both}
.hl{--hb:#1B1B1B}.hlo{--hb:#D8541E}
@keyframes wipe{to{background-size:100% 100%;color:#fff}}
.scrub .knob{animation:slideK .5s cubic-bezier(.3,.9,.3,1) both}
@keyframes slideK{from{left:var(--from)}}
.scrub .prog{animation:slideP .5s cubic-bezier(.3,.9,.3,1) both}
@keyframes slideP{from{width:var(--pfrom)}}
"""


def words_of(alignment):
    ch, st = alignment["characters"], alignment["character_start_times_seconds"]
    out, cur, s = [], "", 0
    for i, c in enumerate(ch):
        if c == " ":
            if cur: out.append(s)
            cur = ""
        else:
            if not cur: s = st[i]
            cur += c
    if cur: out.append(s)
    return out, alignment["character_end_times_seconds"][-1]


def caption_html(cap, wtimes, vo_at):
    # tokenise into (text, cls) chunks
    parts, pos = [], 0
    for m in re.finditer(r'<span class="(hl|hlo|g)">(.*?)</span>', cap):
        if m.start() > pos: parts.append((cap[pos:m.start()], None))
        parts.append((m.group(2), m.group(1))); pos = m.end()
    if pos < len(cap): parts.append((cap[pos:], None))
    toks = [(w, cls) for txt, cls in parts for w in txt.split()]
    n, nv = len(toks), len(wtimes)
    delay = [vo_at + wtimes[min(nv - 1, round(k * nv / n))] for k in range(n)]
    html, k = [], 0
    for txt, cls in parts:
        ws = txt.split()
        if not ws: continue
        inner = " ".join(f'<span class="w" style="--wd:{int(delay[k + j] * 1000)}ms">{w}</span>' for j, w in enumerate(ws))
        if cls in ("hl", "hlo"):
            inner = f'<span class="{cls}" style="--wd:{int(delay[k] * 1000)}ms">{inner}</span>'
        elif cls == "g":
            inner = f'<span class="g">{inner}</span>'
        html.append(inner); k += len(ws)
    return " ".join(html)


def confetti(n=30, seed=3, delay=600):
    import random
    r = random.Random(seed); cols = ["#D8541E", "#1E9E95", "#D9257E", "#F2A33A", "#1B1B1B"]
    return "".join(f'<i class="cf" style="--c:{r.choice(cols)};--x:{r.uniform(-260, 260):.0f}px;--y:{r.uniform(-330, 120):.0f}px;'
                   f'--r:{r.uniform(-540, 540):.0f}deg;--cd:{delay + r.randint(0, 120)}ms"></i>' for _ in range(n))


def index_classes(vis):
    for cls in ("row", "slot", "col", "tag", "card", "lbl"):
        n = [0]
        def sub(m):
            n[0] += 1
            return m.group(0).replace('style="', f'style="--k:{n[0] - 1};', 1)
        vis = re.sub(rf'<div class="{cls}[^"]*" style="', sub, vis)
    return vis


def scenes_for(hook):
    return [dict(HOOKS[hook], id=f"paper_hook{hook}", sfx=HOOK_SFX[hook])] + [
        dict(frames[i + 1], id=f"paper_body{i + 2:02d}", vo=BODY_VO[i], sfx=BODY_SFX[i]) for i in range(11)]


def cmd_vo():
    os.makedirs(os.path.join(build, "vo"), exist_ok=True)
    allsc = [s for h in "ABC" for s in scenes_for(h)[:1]] + scenes_for("A")[1:]
    for i, s in enumerate(allsc):
        p = os.path.join(build, "vo", s["id"])
        if os.path.exists(p + ".json"): continue
        body = {"text": s["vo"], "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True}}
        json.dump(body, open(p + ".req", "w"))
        subprocess.run(["curl", "-sS", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
                        "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json", "-d", "@" + p + ".req", "-o", p + ".json"], check=True)
        d = json.load(open(p + ".json")); assert "audio_base64" in d, d
        import base64
        open(p + ".mp3", "wb").write(base64.b64decode(d.pop("audio_base64"))); json.dump(d, open(p + ".json", "w"))
        print(s["id"], round(d["alignment"]["character_end_times_seconds"][-1], 2))


def cmd_html(hook):
    sc = scenes_for(hook)
    t, secs, cues, sfx = 0.0, [], [], []
    n = len(sc)
    for i, s in enumerate(sc):
        al = json.load(open(os.path.join(build, "vo", s["id"] + ".json")))["alignment"]
        wt, vdur = words_of(al)
        pre = 450 if i == 0 else 0
        vo_at = 0.12 if i else 0.05
        dur = max(1.9, vo_at + vdur + 0.5) + (1.4 if i == n - 1 else 0)
        knob = 40 + i * (460 / 11)
        prev = 40 + max(0, i - 1) * (460 / 11)
        ticks = "".join(f'<span style="left:{40 + j * 2 * (460 / 11)}px">{h}</span>' for j, h in enumerate(ns["TICKS"]))
        vis = index_classes(s["vis"])
        vis_cls = "vis shake" if "stamp" in vis else "vis"
        if "stamp" in vis: vis += confetti(34, 5, 600)
        if "24/7" in s["vis"] and "key big" in s["vis"]: vis += confetti(30, 9, 250)
        if 'class="key' in vis and "SETTER" in vis: vis += confetti(22, 7, 1100)
        vis = re.sub(r'(<div class="col" style="--k:(\d+);[^"]*"><span>)(\d+)(</span>)',
                     lambda m: f'{m.group(1)}<b data-count="{m.group(3)}" data-cd="{int(m.group(2)) * 90 + 100}">{m.group(3)}</b>{m.group(4)}', vis)
        if "class=\"key\"" in vis and "SETTER" in vis: vis = vis.replace('class="key"', 'class="key press"')
        secs.append(f'''<section class="fr" data-t0="{t:.3f}" data-pre="{pre}" style="--dur:{dur:.2f}s;--pre:{pre}ms">
<div class="num">{s["num"]}</div>
<header><div class="rule"></div><span>{s["label"]}</span><em>{s["right"]}</em></header>
<div class="{vis_cls}">{vis}</div>
<div class="cap">{caption_html(s["cap"], wt, vo_at - (0.6 if i == 0 else 0))}</div>
<div class="scrub"><div class="line"></div><div class="prog" style="width:{knob - 40}px;--pfrom:{prev - 40}px"></div><div class="fl" style="left:{40 + 6 * (460 / 11)}px"></div>
<div class="knob" style="left:{knob - 9}px;--from:{prev - 9}px"></div>{ticks}<small class="l">Values illustrative</small><small class="r">Frame {i + 1} of 12</small></div>
</section>''')
        cues.append({"id": s["id"], "at": round(t + vo_at, 3)})
        for off, f, g in s["sfx"]: sfx.append({"file": f, "at": round(t + off, 3), "gain": g})
        if i: sfx.append({"file": "whoosh", "at": round(t - 0.12, 3), "gain": -15})
        t += dur
    html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Paper Video {hook}</title><style>{BASE_CSS}{ANIM_CSS}</style></head>
<body><div id="stage">{"".join(secs)}</div>
<script>
const S=[...document.querySelectorAll('.fr')].map(el=>({{el,t0:+el.dataset.t0}}));
window.ready=(async()=>{{await document.fonts.ready;S.forEach(s=>s.anims=s.el.getAnimations({{subtree:true}}));S.forEach(s=>s.anims.forEach(a=>a.pause()));}})();
const ease=x=>x>=1?1:1-Math.pow(2,-10*x),TR=.34,TYPES=['left','up','zoom'];
window.render=t=>{{let cur=0;S.forEach((s,i)=>{{if(t>=s.t0)cur=i}});
 const lt=t-S[cur].t0,inT=cur>0&&lt<TR,p=ease(lt/TR),ty=TYPES[cur%3];
 S.forEach((s,i)=>{{const on=i===cur||(inT&&i===cur-1);s.el.classList.toggle('on',on);s.el.style.transform='';s.el.style.filter='';s.el.style.zIndex=i===cur?2:1;
  if(!on)return;const loc=(t-s.t0)*1000;s.anims.forEach(a=>a.currentTime=Math.max(0,loc));
  s.el.querySelectorAll('[data-count]').forEach(e=>{{const q=Math.min(1,Math.max(0,(loc-(+e.dataset.cd))/800));e.textContent=Math.round(+e.dataset.count*(1-Math.pow(1-q,3)))}});}});
 if(inT){{const a=S[cur].el,b=S[cur-1].el;
  if(ty==='left'){{a.style.transform=`translateX(${{(1-p)*100}}%) rotate(${{(1-p)*4}}deg)`;b.style.transform=`translateX(${{-p*60}}%) rotate(${{-p*3}}deg)`;b.style.filter=`blur(${{p*6}}px)`}}
  else if(ty==='up'){{a.style.transform=`translateY(${{(1-p)*100}}%)`;b.style.transform=`translateY(${{-p*40}}%) scale(${{1-p*.1}})`;b.style.filter=`blur(${{p*6}}px)`}}
  else{{a.style.transform=`scale(${{.7+.3*p}})`;a.style.opacity=p;b.style.transform=`scale(${{1+p*.6}})`;b.style.filter=`blur(${{p*10}}px)`}}
 }} else S.forEach(s=>s.el.style.opacity='');}};
</script></body></html>'''
    open(os.path.join(here, f"video_{hook}.html"), "w").write(html)
    json.dump({"duration": round(t, 3), "fps": 30, "cues": cues, "sfx": sfx}, open(os.path.join(here, f"timeline_{hook}.json"), "w"), indent=1)
    print(hook, "duration", round(t, 2))


def cmd_mix(hook):
    T = json.load(open(os.path.join(here, f"timeline_{hook}.json"))); dur = T["duration"]
    inputs, filt, vo, fx = [], [], [], []
    def inp(p, loop=False):
        if loop: inputs.extend(["-stream_loop", "-1"])
        inputs.extend(["-i", p]); return len([x for x in inputs if x == "-i"]) - 1
    for c in T["cues"]:
        i = inp(os.path.join(build, "vo", c["id"] + ".mp3")); ms = int(c["at"] * 1000)
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]"); vo.append(f"[v{i}]")
    for s in T["sfx"]:
        i = inp(os.path.join(build, "sfx", s["file"] + ".mp3")); ms = int(s["at"] * 1000)
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={s['gain']}dB,adelay={ms}|{ms}[x{i}]"); fx.append(f"[x{i}]")
    mi = inp(os.path.join(build, "bed.mp3"), loop=True)
    filt.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},volume=-20dB,afade=t=in:d=0.4,afade=t=out:st={dur - 2}:d=2[mus]")
    filt.append(f"{''.join(vo)}amix=inputs={len(vo)}:normalize=0,asplit=2[vo][vk]")
    filt.append("[mus][vk]sidechaincompress=threshold=0.02:ratio=12:attack=20:release=350[musd]")
    filt.append(f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0[fx]")
    filt.append("[vo]highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,equalizer=f=3500:t=q:w=1:g=2[vop]")
    filt.append(f"[vop][musd][fx]amix=inputs=3:normalize=0,atrim=0:{dur},loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000[out]")
    mix = os.path.join(build, f"paper_mix_{hook}.m4a")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-c:a", "aac", "-b:a", "256k", mix], check=True)
    out = os.path.join(here, "out"); os.makedirs(out, exist_ok=True)
    final = os.path.join(out, f"paper_hook{hook}_9x16.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(build, f"paper_video_{hook}.mp4"), "-i", mix, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "copy", "-shortest", "-movflags", "+faststart", final], check=True)
    print("final ->", final)


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "vo": cmd_vo()
    elif c == "html": [cmd_html(h) for h in (sys.argv[2:] or "ABC")]
    elif c == "mix": cmd_mix(sys.argv[2])
