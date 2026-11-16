"""Animated LinkedIn carousel-video (1080x1350, 4:5): 8 slides, swipe transitions, live timers, no voice needed (autoplays muted).
  python3 post.py html -> post.html + timeline_post.json ; node render_post.mjs -> ../../build/post_video.mp4 ; python3 post.py mix -> out/linkedin_carousel.mp4"""
import json, os, re, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__)); studio = os.path.abspath(os.path.join(here, "..", "..")); build = os.path.join(studio, "build")
LOGO = open(os.path.join(studio, "brand", "logo", "svg", "mark_primary.svg")).read()
K, O, CR = "#1B1B1B", "#D8541E", "#F4F0E8"
def logo(px): return LOGO.replace('width="260" height="260"', f'width="{px}" height="{px}"')
def words(txt, start=200, step=110, cls=""):
    out, i = [], 0
    for m in re.finditer(r'(\{o\})?([^\s{}]+)', txt):
        c = "o" if m.group(1) else ""
        out.append(f'<span class="w {c} {cls}" style="--d:{start + i * step}ms">{m.group(2)}</span>'); i += 1
    return " ".join(out)
def tm(k, v="0:00"): return f'<div class="tm" data-k="{k}">{v}</div>'
def coach(i, name, ico, x, y, rot, win=False):
    return (f'<div class="cc{" win" if win else ""}" style="left:{x}px;top:{y}px;--r:{rot}deg;--i:{i}"><div class="ci">{logo(46) if win else ico}</div><b>{name}</b>'
            + (tm("win" if win else "slow") if False else "") + '</div>')
NI = [("Business", "💼"), ("Mindset", "🧠"), ("Career", "🚀"), ("Relationship", "💬")]
def board(timers, status=None):
    pos = [(26, 0, -3), (200, -8, 2), (374, 6, -2), (110, 232, 2), (290, 244, -3)]
    out = ""
    for i in range(5):
        win = i == 4; name, ico = (NI[i] if not win else ("DMSetter", ""))
        x, y, r = pos[i]
        t = (tm("win") if win else tm("slow")) if timers else '<div class="tm">0:00</div>'
        st = ""
        if status: st = f'<small>{["asleep","on a flight","at dinner","in a call","replied"][i]}</small>'
        out += (f'<div class="cc{" win" if win else ""}" style="left:{x}px;top:{y}px;--r:{r}deg;--i:{i}"><div class="ci">{logo(46) if win else ico}</div><b>{name}</b>{t}{st}</div>')
    return out
S = [  # dur, headline, visual
 (3.6, "A lead messaged {o}5 coaches {o}at {o}11 PM. Only one got the call.",
  '<div class="msg">Hi! How does your coaching work? 🙌</div><div class="fan">' + "".join(f'<i style="--r:{r}deg;--i:{j}">{e}</i>' for j, (r, e) in enumerate([(-24, "💼"), (-12, "🧠"), (0, "🚀"), (12, "💬"), (24, "🥗")])) + '</div>'),
 (3.0, "Same message. Same minute. {o}Five different coaches.", '<div class="board">' + board(False) + '</div>'),
 (4.6, "Four replied in the morning. {o}One replied in 38 seconds.", '<div class="board">' + board(True, True) + '</div>'),
 (3.6, "She didn't pick the best coach. She picked the {o}first one who answered.", f'<div class="bigq">“</div><div class="cloudbig">{logo(150)}</div>'),
 (3.6, "Speed to reply decides more deals than your {o}offer does.",
  '<div class="bars2"><div><i style="--h:34%"></i><b>Offer</b></div><div class="hot"><i style="--h:92%"></i><b>Speed</b></div></div><div class="ill">VALUES ILLUSTRATIVE</div>'),
 (3.6, "A good reply is fast, asks {o}one question, and moves to a {o}call.",
  '<div class="steps"><div style="--i:0"><span>1</span>Reply in seconds</div><div style="--i:1"><span>2</span>Ask one question</div><div style="--i:2"><span>3</span>Move to a call</div></div>'),
 (3.2, "{o}Booked while she slept.",
  '<div class="wk">' + "".join(f'<div style="--i:{j}"><small>{d}</small><i class="{"b" if d == "THU" else ""}">{"CALL" if d == "THU" else ""}</i></div>' for j, d in enumerate(["MON", "TUE", "WED", "THU", "FRI"])) + '</div><div class="stampb">BOOKED</div><div class="ill">VALUES ILLUSTRATIVE</div>'),
 (4.4, "I put together the replies that win the race. {o}Comment SPEED {o}and I'll send them.",
  f'<div class="endlogo">{logo(190)}</div><div class="wm">DM<span>Setter</span></div><div class="cbox">SPEED &#10148;</div>'),
]
CSS = f"""@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{background:#000}}body{{width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif}}
#stage{{width:540px;height:675px;zoom:2;position:relative;overflow:hidden;background:{CR}}}
#stage::before{{content:"";position:absolute;inset:0;z-index:0;background:radial-gradient(120% 90% at 50% 35%,#F7F2E9 0%,#ECE6DA 70%,#E2DBCD 100%),repeating-linear-gradient(0deg,rgba(0,0,0,.035) 0 1px,transparent 1px 36px)}}
.sl{{position:absolute;inset:0;opacity:0;z-index:1}}.sl.on{{opacity:1}}
.brand{{position:absolute;left:22px;top:20px;z-index:20;display:flex;align-items:center;gap:6px;font:900 14px Inter;letter-spacing:-.02em;color:{K}}}.brand span{{color:{O}}}
.dots{{position:absolute;right:22px;top:26px;z-index:20;display:flex;gap:5px}}.dots i{{width:22px;height:5px;border-radius:3px;background:rgba(0,0,0,.15)}}.dots i.on{{background:{O}}}
.hint{{position:absolute;right:22px;bottom:18px;z-index:20;font:800 12px Inter;color:{K};background:#fff;border:2px solid {K};border-radius:20px;padding:5px 12px;box-shadow:3px 3px 0 {K}}}
.hl{{position:absolute;left:28px;right:28px;top:78px;font:900 40px/1.1 Inter;letter-spacing:-.035em;color:{K};z-index:5}}
.w{{display:inline-block;animation:wIn .42s cubic-bezier(.2,.9,.3,1.4) var(--d) both}}.w.o{{color:{O}}}
@keyframes wIn{{from{{opacity:0;translate:0 26px;scale:.88}}}}
.vis{{position:absolute;left:0;right:0;top:250px;bottom:50px}}
.vis>*{{animation:vin .6s cubic-bezier(.2,.9,.3,1.3) calc(var(--i,0)*120ms + 500ms) both}}@keyframes vin{{from{{opacity:0;translate:0 44px;scale:.9}}}}
.msg{{position:absolute;left:50px;top:20px;background:linear-gradient(135deg,#3797F0,#A033FF);color:#fff;font:500 18px Inter;padding:14px 18px;border-radius:22px;box-shadow:0 12px 26px rgba(0,0,0,.25)}}
.fan i{{position:absolute;top:140px;width:78px;height:100px;background:#fff;border:3px solid {K};border-radius:9px;font-style:normal;font-size:38px;display:grid;place-items:center;transform:rotate(var(--r));box-shadow:5px 5px 0 rgba(0,0,0,.2);left:calc(26px + var(--i)*96px);animation:vin .5s cubic-bezier(.2,.9,.3,1.4) calc(900ms + var(--i)*140ms) both}}
.board{{position:absolute;inset:0}}.cc{{position:absolute;width:150px;height:148px;background:#FBFAF6;border:3px solid {K};border-radius:9px;box-shadow:6px 6px 0 rgba(0,0,0,.2);padding:10px;text-align:center;transform:rotate(var(--r));animation:vin .5s cubic-bezier(.2,.9,.3,1.4) calc(var(--i)*140ms + 400ms) both}}
.cc.win{{border-color:{O};background:#FFF5EE;box-shadow:6px 6px 0 {O}}}.ci{{font-size:34px;height:46px;display:grid;place-items:center}}.cc b{{display:block;font:800 12px Inter;margin-top:2px}}
.tm{{font:900 28px Inter;margin-top:4px;font-variant-numeric:tabular-nums}}.cc.win .tm{{color:{O}}}.cc small{{display:block;font:700 11px Inter;color:#8a8372;margin-top:2px}}.cc.win small{{color:{O}}}
.bigq{{position:absolute;left:30px;top:-40px;font:900 200px/1 Inter;color:{O};opacity:.9}}.cloudbig{{position:absolute;right:50px;top:60px;filter:drop-shadow(0 12px 16px rgba(0,0,0,.25))}}
.bars2{{position:absolute;left:60px;right:60px;top:10px;height:290px;display:flex;gap:40px;align-items:flex-end}}.bars2>div{{flex:1;height:100%;display:flex;flex-direction:column;justify-content:flex-end;text-align:center;font:800 18px Inter}}
.bars2 i{{display:block;background:#bdb6a6;border:3px solid {K};box-shadow:6px 6px 0 rgba(0,0,0,.2);height:var(--h);transform-origin:bottom;animation:grow .9s cubic-bezier(.2,.9,.3,1.2) 700ms both}}.bars2 .hot i{{background:{O};animation-delay:1100ms}}.bars2 b{{margin-top:10px}}
@keyframes grow{{from{{scale:1 0}}}}.ill{{position:absolute;right:28px;top:330px;background:{O};color:#fff;font:800 11px Inter;padding:5px 10px;border-radius:4px;rotate:6deg}}
.steps{{position:absolute;left:36px;right:36px;top:0}}.steps div{{background:#fff;border:3px solid {K};box-shadow:6px 6px 0 rgba(0,0,0,.2);border-radius:10px;padding:18px 20px;margin-bottom:16px;font:800 24px Inter;display:flex;gap:16px;align-items:center;animation:vin .5s cubic-bezier(.2,.9,.3,1.4) calc(var(--i)*320ms + 600ms) both}}
.steps span{{width:40px;height:40px;border-radius:50%;background:{O};color:#fff;display:grid;place-items:center;font:900 20px Inter}}
.wk{{position:absolute;left:36px;right:36px;top:0;height:220px;display:grid;grid-template-columns:repeat(5,1fr);gap:10px}}.wk div{{display:flex;flex-direction:column;gap:6px}}.wk small{{font:800 11px Inter;text-align:center;color:#8a8372}}
.wk i{{flex:1;border:2px solid #cfc8b8;border-radius:8px;background:#fff;font:900 13px Inter;font-style:normal;display:grid;place-items:center;color:#fff}}.wk i.b{{background:{O};border-color:{O}}}
.stampb{{position:absolute;left:120px;top:150px;padding:6px 18px;border:6px solid {O};color:{O};font:900 54px Inter;border-radius:12px;rotate:-10deg;background:rgba(244,240,232,.92);animation:stamp .3s cubic-bezier(.5,0,.8,.5) 1200ms both!important}}@keyframes stamp{{from{{opacity:0;scale:3}}}}
.endlogo{{position:absolute;left:175px;top:-10px}}.wm{{position:absolute;left:0;right:0;top:190px;text-align:center;font:900 54px Inter;letter-spacing:-.04em;color:{K}}}.wm span{{color:{O}}}
.cbox{{position:absolute;left:130px;right:130px;top:280px;background:#fff;border:3px solid {K};border-radius:34px;padding:14px 24px;font:800 24px Inter;box-shadow:5px 5px 0 rgba(0,0,0,.2);text-align:left}}
.last .hint{{display:none}}"""
def cmd_html():
    secs, t, tl = [], 0.0, []
    for i, (d, hl, vis) in enumerate(S):
        secs.append(f'<section class="sl" data-t0="{t:.3f}" data-dur="{d}"><div class="hl">{words(hl)}</div><div class="vis">{vis}</div></section>'); tl.append((t, d)); t += d
    dots = "".join('<i></i>' for _ in S)
    html = f'''<!doctype html><html><head><meta charset="utf-8"><title>LinkedIn carousel</title><style>{CSS}</style></head><body><div id="stage">{"".join(secs)}
<div class="brand">{logo(26)}<div>DM<span>Setter</span></div></div><div class="dots">{dots}</div><div class="hint">swipe &#10140;</div></div><script>
const S=[...document.querySelectorAll('.sl')].map(el=>({{el,t0:+el.dataset.t0,dur:+el.dataset.dur}}));const D=[...document.querySelectorAll('.dots i')],H=document.querySelector('.hint');
window.ready=(async()=>{{await document.fonts.ready;S.forEach(s=>{{s.anims=s.el.getAnimations({{subtree:true}});s.anims.forEach(a=>a.pause())}})}})();
const ease=x=>x>=1?1:1-Math.pow(2,-9*x),TR=.38,fmt=v=>{{v=Math.floor(v);return Math.floor(v/60)+':'+String(v%60).padStart(2,'0')}};
window.render=async t=>{{let cur=0;S.forEach((s,i)=>{{if(t>=s.t0)cur=i}});const lt=t-S[cur].t0,inT=cur>0&&lt<TR,p=ease(lt/TR);
 S.forEach((s,i)=>{{const on=i===cur||(inT&&i===cur-1);s.el.classList.toggle('on',on);s.el.style.transform='';if(!on)return;const loc=(t-s.t0)*1000;
  s.anims.forEach(a=>a.currentTime=Math.max(0,loc));s.el.querySelectorAll('.tm[data-k]').forEach(e=>{{const l=Math.max(0,loc/1000-.4);e.textContent=fmt(e.dataset.k==='win'?Math.min(38,l/1.3*38):Math.min(554,l/3*554))}})}});
 if(inT){{S[cur].el.style.transform=`translateX(${{(1-p)*100}}%)`;S[cur-1].el.style.transform=`translateX(${{-p*100}}%)`}}
 D.forEach((d,i)=>d.classList.toggle('on',i<=cur));H.style.display=cur===S.length-1?'none':'block'}};
</script></body></html>'''
    open(os.path.join(here, "post.html"), "w").write(html)
    sfx = []
    def X(f, at, g, d="sfx"): sfx.append({"file": f, "at": round(at, 3), "gain": g, "dir": d})
    for i, (a, d) in enumerate(tl):
        if i: X("whoosh", a - 0.1, -14)
        X("pop", a + 0.35, -15)
    a2 = tl[2][0]; X("tick", a2 + 0.3, -17, "sfx2"); X("scratch", a2 + 1.7, -8, "sfx2"); X("drop", a2 + 1.95, -7, "sfx2"); X("win", a2 + 2.05, -12, "sfx2")
    X("stamp", tl[6][0] + 1.25, -6, "sfx2"); X("ding", tl[6][0] + 1.3, -10); X("win", tl[7][0] + 0.5, -13, "sfx2"); X("ding", tl[7][0] + 0.6, -10)
    X("snore", tl[2][0] + 1.0, -17, "sfx2")
    json.dump({"duration": round(t, 3), "fps": 30, "sfx": sfx}, open(os.path.join(here, "timeline_post.json"), "w"), indent=1); print("duration", round(t, 2))
def cmd_mix():
    T = json.load(open(os.path.join(here, "timeline_post.json"))); dur = T["duration"]; out = os.path.join(here, "out"); os.makedirs(out, exist_ok=True)
    inputs, filt, fx = [], [], []
    def inp(p, loop=False):
        if loop: inputs.extend(["-stream_loop", "-1"])
        inputs.extend(["-i", p]); return inputs.count("-i") - 1
    for s in T["sfx"]:
        i = inp(os.path.join(build, s["dir"], s["file"] + ".mp3")); ms = int(max(0, s["at"]) * 1000)
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={s['gain']}dB,adelay={ms}|{ms}[x{i}]"); fx.append(f"[x{i}]")
    filt.append(f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0[fx]")
    mi = inp(os.path.join(build, "bed.mp3"), True)
    filt.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},volume=-21dB,afade=t=in:d=0.4,afade=t=out:st={dur-1.5}:d=1.5[mus]")
    filt.append(f"[mus][fx]amix=inputs=2:normalize=0,apad,atrim=0:{dur},loudnorm=I=-16:TP=-1.0:LRA=9,aresample=48000[out]")
    mix = os.path.join(build, "post_mix.m4a")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-c:a", "aac", "-b:a", "192k", mix], check=True)
    final = os.path.join(out, "linkedin_carousel_4x5.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(build, "post_video.mp4"), "-i", mix, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", final], check=True); print("final ->", final)
if __name__ == "__main__": {"html": cmd_html, "mix": cmd_mix}[sys.argv[1]]()
