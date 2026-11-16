"""Host + effects Reel (31.2s): realistic host speaks, then Screen-in-Screen -> Zoom-Through -> Grid Dive -> Cube Spin -> Shatter -> Phone Fan.
  python3 host.py html -> host.html + timeline_host.json ; node render_host.mjs -> ../../build/host_video.mp4 ; python3 host.py mix -> out/host_viral_9x16.mp4"""
import json, os, random, re, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__)); studio = os.path.abspath(os.path.join(here, "..", "..")); build = os.path.join(studio, "build")
NS = {"__file__": os.path.join(studio, "storyboards", "viral-remake", "build.py"), "__name__": "lib"}
exec(open(NS["__file__"]).read(), NS)
phone, PHONE_CSS, logo = NS["phone"], NS["PHONE_CSS"], NS["logo"]
K, O, CR = "#1B1B1B", "#D8541E", "#F4F0E8"
HOOKN = len(os.listdir(os.path.join(here, "hookframes"))); CTAN = len(os.listdir(os.path.join(here, "ctaframes")))
rnd = random.Random(7)


def words(txt, start=250, step=95):
    out, i = [], 0
    for m in re.finditer(r'(\{o\})?([^\s{}]+)', txt):
        out.append(f'<span class="w {"o" if m.group(1) else ""}" style="--d:{start + i * step}ms">{m.group(2)}</span>'); i += 1
    return " ".join(out)


def cap(txt, start=250): return f'<div class="cap"><b>{words(txt, start)}</b></div>'


def coach(i, name, ico, x, y, rot, win=False):
    t = f'<div class="tm" data-k="{"win" if win else "slow"}">0:00</div>'
    return (f'<div class="cc{" win" if win else ""}" id="{"winner" if win else ""}" style="left:{x}px;top:{y}px;--r:{rot}deg;--i:{i}"><div class="ci">{logo(46) if win else ico}</div><b>{name}</b>{t}</div>')


def board():
    pos = [(30, 120, -3), (195, 105, 2), (360, 125, -2), (100, 330, 2), (290, 340, -3)]
    items = [("Business", "💼"), ("Mindset", "🧠"), ("Career", "🚀"), ("Relationship", "💬"), ("DMSetter", "")]
    return "".join(coach(i, n, e, *pos[i], win=(i == 4)) for i, (n, e) in enumerate(items))


WK = '<div class="wk">' + "".join(f'<div style="--i:{j}"><small>{d}</small><i class="{"b" if d == "THU" else ""}">{"CALL" if d == "THU" else ""}</i></div>' for j, d in enumerate(["MON", "TUE", "WED", "THU", "FRI"])) + '</div>'
S5_BODY = f'<div class="calcard">{WK}<div class="foot">BOOKED WHILE SHE SLEPT</div></div><div class="stampb">BOOKED</div><div class="ill">VALUES ILLUSTRATIVE</div>'


def shards(body):
    cols, rows, out = 4, 6, ""
    W, H = 540, 960
    for r in range(rows):
        for c in range(cols):
            x0, x1, y0, y1 = c * W / cols, (c + 1) * W / cols, r * H / rows, (r + 1) * H / rows
            for poly in ([(x0, y0), (x1, y0), (x0, y1)], [(x1, y0), (x1, y1), (x0, y1)]):
                cx = sum(p[0] for p in poly) / 3 - W / 2; cy = sum(p[1] for p in poly) / 3 - H / 2
                clip = "polygon(" + ",".join(f"{p[0]:.1f}px {p[1]:.1f}px" for p in poly) + ")"
                dx, dy, rot = cx * rnd.uniform(1.2, 2.6), cy * rnd.uniform(.8, 2.0) + rnd.uniform(200, 700), rnd.uniform(-160, 160)
                out += f'<div class="sh" style="clip-path:{clip};--dx:{dx:.0f}px;--dy:{dy:.0f}px;--rot:{rot:.0f}deg;--sd:{rnd.uniform(0, .18):.2f}s"><div class="shin">{body}</div></div>'
    return out


def pf(img, rot, x, y, z, delay, inner):
    return f'<div class="pfp" style="left:{x}px;top:{y}px;--r:{rot}deg;z-index:{z};--dl:{delay}ms"><div class="pfs">{inner}</div></div>'


CHAT_MINI = '<div class="mi"><div class="mb a">How does your coaching work? 🙌</div><div class="mb b">Hey! What\'s your goal right now?</div><div class="mb a">Grow my client list</div><div class="mb b">Call tomorrow 3 PM?</div></div>'
CAL_MINI = '<div class="mi cal">' + "".join(f'<i class="{"b" if j == 3 else ""}"></i>' for j in range(10)) + '<b>BOOKED</b></div>'

T = {"s1": (0.0, 6.2), "s2": (5.5, 11.7), "s3": (10.5, 16.6), "s4": (16.2, 21.8), "s5": (21.4, 25.2), "s6": (23.8, 31.2)}
D = 31.2
SC = {}
SC["s1"] = (f'<img class="hostfull" data-clip="hook" data-off="0"><div class="s1bg"></div><div class="s1ph"></div>'
            f'<div class="tag1">11:41 PM</div>{cap("A lead messaged {o}five coaches {o}at 11 PM. Only one got the call.", 900)}', "s1")
SC["s2"] = (f'<div class="board">{board()}</div><div class="wrap2">{cap("Four replied in the morning. {o}One replied in 38 seconds.", 700)}</div>', "s2")
SC["s3"] = (phone([("in", "How does your coaching work? 🙌"), ("out", "Hey! Love that you reached out 🙌 What's your goal right now?"), ("in", "grow my client list"), ("out", "Got you. Quick call tomorrow 3 PM?")], x=95, y=120, rot=-2, w=300, h=470, seen=False, name="New lead", hl=1)
            + f'<div class="cl3">{logo(120)}</div><div class="first">FIRST TO ANSWER</div>' + cap("She picked the {o}first one who answered.", 600), "s3")
CUBE = (f'<div class="stage3d"><div class="cube">'
        f'<div class="face f1"><b>1</b>Reply<br>in seconds</div><div class="face f2"><b>2</b>Ask one<br>question</div><div class="face f3"><b>3</b>Move to<br>a call</div><div class="face f4">{logo(150)}</div></div></div>')
SC["s4"] = (CUBE + cap("Three steps. {o}Fast. {o}One question. {o}A call.", 500), "s4")
SC["s5"] = (f'<div class="base5">{S5_BODY}</div><div class="shs">{shards(S5_BODY)}</div>' + cap("By morning, the call was {o}booked.", 400), "s5")
SC["s6"] = (pf("l", -16, 20, 250, 1, 250, CHAT_MINI) + pf("r", 16, 300, 250, 1, 250, CAL_MINI)
            + pf("c", 0, 150, 210, 3, 100, '<img class="hostphone" data-clip="cta" data-off="1.1">')
            + f'<div class="end6"><div class="wm">DM<span>Setter</span></div></div>' + cap("Comment {o}“SPEED”", 1300), "s6")

CSS = f"""@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{background:#000}}body{{width:1080px;height:1920px;overflow:hidden;font-family:Inter,sans-serif}}
#stage{{width:540px;height:960px;zoom:2;position:relative;overflow:hidden;background:#000}}
.sc{{position:absolute;inset:0;visibility:hidden;overflow:hidden;background:radial-gradient(120% 90% at 50% 35%,#F7F2E9 0%,#ECE6DA 70%,#E2DBCD 100%)}}.sc.on{{visibility:visible}}
.sc::before{{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.035) 0 1px,transparent 1px 36px),repeating-linear-gradient(90deg,rgba(0,0,0,.035) 0 1px,transparent 1px 36px)}}
.cap{{position:absolute;left:28px;right:28px;top:760px;text-align:center;z-index:30;animation:capIn .4s cubic-bezier(.2,.9,.3,1.3) 80ms both}}@keyframes capIn{{from{{opacity:0;translate:0 30px}}}}
.cap b{{font:900 27px/1.55 Inter;background:#fff;border:3px solid {K};box-shadow:5px 5px 0 {K};padding:3px 10px;-webkit-box-decoration-break:clone;box-decoration-break:clone;letter-spacing:-.01em}}
.w{{display:inline-block;animation:wIn .28s cubic-bezier(.2,.9,.3,1.4) var(--d) both}}.w.o{{color:{O}}}@keyframes wIn{{from{{opacity:0;translate:0 14px;scale:.9}}}}
/* s1 host + screen-in-screen + zoom-through */
#s1{{background:#000;animation:z1 .7s cubic-bezier(.75,0,.9,.35) 5.5s both;transform-origin:270px 463px}}
@keyframes z1{{from{{scale:1;opacity:1}}85%{{opacity:1}}to{{scale:16;opacity:0}}}}
#s1::before{{display:none}}
.hostfull{{position:absolute;left:0;top:0;width:540px;height:960px;object-fit:cover;z-index:2;animation:shr .9s cubic-bezier(.6,0,.2,1) 4.6s both}}
@keyframes shr{{to{{left:150px;top:250px;width:240px;height:427px;border-radius:26px}}}}
.s1bg{{position:absolute;inset:0;z-index:1;background:radial-gradient(120% 90% at 50% 35%,#F7F2E9,#ECE6DA 70%,#E2DBCD);animation:fin .6s ease 4.6s both}}@keyframes fin{{from{{opacity:0}}}}
.s1ph{{position:absolute;left:138px;top:238px;width:264px;height:451px;border-radius:36px;border:8px solid #0b0b0b;box-shadow:0 30px 50px rgba(50,30,10,.35);z-index:3;animation:fin .5s ease 5.0s both}}
.tag1{{position:absolute;left:24px;top:36px;z-index:6;background:{O};color:#fff;font:900 18px Inter;padding:7px 14px;border-radius:4px;rotate:-4deg;animation:pop .45s cubic-bezier(.2,.9,.3,1.6) .4s both,fout .2s ease 4.5s forwards}}
@keyframes pop{{from{{opacity:0;scale:.3}}}}@keyframes fout{{to{{opacity:0}}}}
#s1 .cap{{z-index:8;animation:capIn .4s ease 80ms both,fout .25s ease 4.5s forwards}}
/* s2 grid dive */
#s2 .board,#s2 .wrap2{{position:absolute;inset:0}}#s2 .wrap2{{z-index:31}}
#s2 .board{{transform-origin:380px 440px;animation:ent2 .7s cubic-bezier(.2,.9,.3,1) both,dive 1.1s cubic-bezier(.7,0,.9,.4) 4.3s both}}
@keyframes ent2{{from{{scale:1.8;opacity:0}}}}@keyframes dive{{to{{scale:11;opacity:0}}}}
#s2 .wrap2{{animation:fout .3s ease 4.2s forwards}}
.cc{{position:absolute;width:150px;height:158px;background:#FBFAF6;border:3px solid {K};border-radius:9px;box-shadow:6px 6px 0 rgba(0,0,0,.2);padding:10px;text-align:center;transform:rotate(var(--r));animation:vin .5s cubic-bezier(.2,.9,.3,1.4) calc(var(--i)*130ms + 350ms) both}}
@keyframes vin{{from{{opacity:0;translate:0 40px;scale:.9}}}}
.cc.win{{border-color:{O};background:#FFF5EE;box-shadow:6px 6px 0 {O}}}.ci{{font-size:34px;height:48px;display:grid;place-items:center}}.cc b{{display:block;font:800 12px Inter;margin-top:2px}}.tm{{font:900 30px Inter;margin-top:6px;font-variant-numeric:tabular-nums}}.cc.win .tm{{color:{O}}}
/* s3 */
#s3{{animation:ent3 .8s cubic-bezier(.2,.9,.3,1) both}}@keyframes ent3{{from{{scale:.15;opacity:0}}}}
.cl3{{position:absolute;left:330px;top:60px;z-index:7;filter:drop-shadow(0 10px 14px rgba(0,0,0,.25));animation:vin .5s ease 1s both}}
.first{{position:absolute;left:280px;top:600px;z-index:8;background:{O};color:#fff;font:900 16px Inter;padding:6px 12px;border-radius:4px;rotate:6deg;animation:pop .4s cubic-bezier(.2,.9,.3,1.6) 2.2s both}}
{PHONE_CSS}
.ph .m{{animation:msgIn .32s cubic-bezier(.2,.9,.3,1.3) calc(var(--i)*600ms + 900ms) both}}@keyframes msgIn{{from{{opacity:0;translate:0 18px;scale:.9}}}}
/* s4 cube */
.stage3d{{position:absolute;left:0;right:0;top:140px;height:520px;perspective:1100px;perspective-origin:50% 40%}}
.cube{{position:absolute;left:120px;top:90px;width:300px;height:300px;transform-style:preserve-3d;animation:cubespin 5.4s linear both}}
.face{{position:absolute;width:300px;height:300px;border:4px solid {K};display:grid;place-items:center;text-align:center;font:900 36px/1.1 Inter;letter-spacing:-.03em;backface-visibility:hidden}}
.face b{{display:grid;place-items:center;width:56px;height:56px;border-radius:50%;background:{K};color:#fff;font:900 28px Inter;margin:0 auto 14px}}
.f1{{background:{O};color:#fff;transform:translateZ(150px)}}.f1 b{{background:#fff;color:{O}}}.f2{{background:{K};color:#fff;transform:rotateY(90deg) translateZ(150px)}}.f2 b{{background:{O}}}.f3{{background:#fff;color:{K};transform:rotateY(180deg) translateZ(150px)}}.f3 b{{background:{O}}}.f4{{background:#FFF5EE;transform:rotateY(270deg) translateZ(150px)}}
@keyframes cubespin{{0%{{transform:translateY(-500px) rotateX(-20deg) rotateY(-540deg) scale(.05)}}12%{{transform:translateY(0px) rotateX(-12deg) rotateY(0deg) scale(1)}}38%{{transform:translateY(0px) rotateX(-12deg) rotateY(0deg) scale(1)}}52%{{transform:translateY(0px) rotateX(-12deg) rotateY(-90deg) scale(1)}}70%{{transform:translateY(0px) rotateX(-12deg) rotateY(-90deg) scale(1)}}84%{{transform:translateY(0px) rotateX(-12deg) rotateY(-180deg) scale(1)}}100%{{transform:translateY(0px) rotateX(-12deg) rotateY(-180deg) scale(1)}}}}
/* s5 shatter */
#s5{{animation:bgfade .01s linear 2.2s forwards}}@keyframes bgfade{{to{{background:transparent}}}}#s5::before{{animation:fout .01s linear 2.2s forwards}}
.base5{{position:absolute;inset:0;animation:fout .01s linear 2.2s forwards}}.shs{{position:absolute;inset:0;opacity:0;animation:fin2 .01s linear 2.2s forwards}}@keyframes fin2{{to{{opacity:1}}}}
.sh{{position:absolute;inset:0;animation:fly 1.1s cubic-bezier(.3,.0,.7,1) calc(2.2s + var(--sd)) both}}.shin{{position:absolute;inset:0}}
@keyframes fly{{to{{translate:var(--dx) var(--dy);rotate:var(--rot);opacity:0;scale:.7}}}}
#s5 .cap{{animation:capIn .4s ease 80ms both,fout .2s ease 2.1s forwards}}
.calcard{{position:absolute;left:36px;right:36px;top:170px;height:330px;background:#FBFAF6;border:3px solid {K};border-radius:8px;box-shadow:7px 7px 0 rgba(0,0,0,.2);padding:18px}}
.wk{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;height:78%}}.wk div{{display:flex;flex-direction:column;gap:6px}}.wk small{{font:800 11px Inter;text-align:center;color:#8a8372}}
.wk i{{flex:1;border:2px solid #cfc8b8;border-radius:6px;background:#fff;font:900 12px Inter;font-style:normal;display:grid;place-items:center;color:#fff}}.wk i.b{{background:{O};border-color:{O}}}
.foot{{position:absolute;left:18px;right:18px;bottom:14px;text-align:center;background:#EFEADD;border:2px solid #cfc8b8;border-radius:6px;font:800 13px Inter;padding:9px;letter-spacing:.06em}}
.stampb{{position:absolute;left:130px;top:430px;padding:5px 16px;border:6px solid {O};color:{O};font:900 50px Inter;border-radius:12px;rotate:-10deg;background:rgba(244,240,232,.92);animation:stamp .3s cubic-bezier(.5,0,.8,.5) .8s both}}@keyframes stamp{{from{{opacity:0;scale:3}}}}
.ill{{position:absolute;right:34px;top:140px;background:{O};color:#fff;font:800 11px Inter;padding:4px 9px;border-radius:3px;rotate:5deg}}
/* s6 phone fan */
.pfp{{position:absolute;width:240px;height:440px;border-radius:30px;border:7px solid #0b0b0b;background:#000;box-shadow:0 26px 40px rgba(50,30,10,.35);transform:rotate(var(--r));overflow:hidden;animation:fan .8s cubic-bezier(.2,.9,.3,1.25) var(--dl) both}}
@keyframes fan{{from{{transform:rotate(0deg) translateY(120px) scale(.8);opacity:0}}}}
.pfs{{position:absolute;inset:0}}.hostphone{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.mi{{position:absolute;inset:0;background:#0b0b0b;padding:30px 10px;display:flex;flex-direction:column;justify-content:center;gap:8px}}.mb{{font:500 11px Inter;padding:7px 10px;border-radius:14px;max-width:85%}}.mb.a{{background:#262626;color:#fff}}.mb.b{{background:linear-gradient(135deg,#3797F0,#A033FF);color:#fff;align-self:flex-end}}
.mi.cal{{display:grid;grid-template-columns:repeat(2,1fr);gap:6px;align-content:center;background:#FBFAF6}}.mi.cal i{{height:46px;border:2px solid #cfc8b8;border-radius:6px;background:#fff}}.mi.cal i.b{{background:{O};border-color:{O}}}.mi.cal b{{grid-column:1/3;text-align:center;font:900 22px Inter;color:{O};margin-top:6px}}
.end6{{position:absolute;left:0;right:0;top:660px;text-align:center;animation:vin .6s ease 1.4s both}}.wm{{font:900 56px Inter;letter-spacing:-.04em;color:{K}}}.wm span{{color:{O}}}
#s6 .cap{{top:740px}}
"""

HTML_SC = "".join(f'<section class="sc" id="{sid}" data-t0="{T[sid][0]}" data-t1="{T[sid][1]}">{body}</section>' for sid, (body, _) in SC.items())


def cmd_html():
    html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Host viral</title><style>{CSS}</style></head><body><div id="stage">{HTML_SC}</div><script>
const NH={HOOKN},NC={CTAN};
const S=[...document.querySelectorAll('.sc')].map((el,i)=>({{el,t0:+el.dataset.t0,t1:+el.dataset.t1,z:100-i,clips:[...el.querySelectorAll('[data-clip]')]}}));
window.ready=(async()=>{{await document.fonts.ready;S.forEach(s=>{{s.anims=s.el.getAnimations({{subtree:true}});s.anims.forEach(a=>a.pause())}});}})();
const fmt=v=>{{v=Math.floor(v);return Math.floor(v/60)+':'+String(v%60).padStart(2,'0')}};
async function setClip(e,loc){{const n=e.dataset.clip==='hook'?NH:NC,off=+e.dataset.off||0,i=Math.min(n,Math.max(1,1+Math.floor((loc/1000-off)*30)));
 const src=(e.dataset.clip==='hook'?'hookframes/':'ctaframes/')+'f'+String(i).padStart(4,'0')+'.jpg';if(e.dataset.src!==src){{e.src=src;e.dataset.src=src;await e.decode().catch(()=>{{}})}}}}
window.render=async t=>{{for(const s of S){{const on=t>=s.t0&&t<s.t1;s.el.classList.toggle('on',on);s.el.style.zIndex=s.z;if(!on)continue;const loc=(t-s.t0)*1000;
  s.anims.forEach(a=>a.currentTime=Math.max(0,loc));
  s.el.querySelectorAll('.tm[data-k]').forEach(e=>{{const l=Math.max(0,loc/1000-1.0);e.textContent=fmt(e.dataset.k==='win'?Math.min(38,l/2.1*38):Math.min(554,l/3.2*554))}});
  for(const c of s.clips)await setClip(c,loc);}}}};
</script></body></html>'''
    open(os.path.join(here, "host.html"), "w").write(html)
    sfx = []
    def X(f, at, g, d="sfx"): sfx.append({"file": f, "at": at, "gain": g, "dir": d})
    X("whoosh", 5.3, -11); X("riser", 4.2, -17); X("boom", 5.9, -10)
    for tt in (6.6, 8.6): X("tick", tt, -17, "sfx2")
    X("scratch", 9.0, -8, "sfx2"); X("drop", 9.25, -7, "sfx2"); X("win", 9.35, -12, "sfx2"); X("whoosh", 9.9, -11)
    X("pop", 11.9, -13); X("sent", 12.4, -11, "sfx2"); X("sent", 13.0, -11, "sfx2"); X("ding", 13.9, -11)
    X("whoosh", 16.2, -13); X("click", 17.55, -8); X("whoosh", 17.5, -15); X("click", 19.1, -8); X("whoosh", 19.0, -15)
    X("pop", 21.7, -14); X("stamp", 22.3, -6, "sfx2"); X("ding", 22.4, -10); X("boom", 23.6, -9)
    X("whoosh", 24.0, -12); X("win", 26.0, -14, "sfx2"); X("click", 30.1, -9); X("ding", 30.2, -10)
    json.dump({"duration": D, "fps": 30, "sfx": sfx}, open(os.path.join(here, "timeline_host.json"), "w"), indent=1); print("ok", D)


def cmd_mix():
    A = os.path.join(here, "assets"); sh = os.path.join(A, "shatter.mp3"); out = os.path.join(here, "out"); os.makedirs(out, exist_ok=True)
    T_ = json.load(open(os.path.join(here, "timeline_host.json"))); dur = T_["duration"]
    vo = [(os.path.join(A, "hook_vc.mp3"), 0.0, 0, 1.0), (os.path.join(A, "four.mp3"), 6.45, -1, 1.0), (os.path.join(A, "pick.mp3"), 11.7, -1, 1.0), (os.path.join(A, "steps.mp3"), 16.55, -1, 1.25),
          (os.path.join(A, "booked.mp3"), 21.8, -1, 1.0), (os.path.join(A, "cta_vc.mp3"), 24.9, 0, 1.0)]
    inputs, filt, vl, fx = [], [], [], []
    def inp(p, loop=False):
        if loop: inputs.extend(["-stream_loop", "-1"])
        inputs.extend(["-i", p]); return inputs.count("-i") - 1
    for p, at, _, tempo in vo:
        i = inp(p); ms = int(at * 1000)
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atempo={tempo},adelay={ms}|{ms}[v{i}]"); vl.append(f"[v{i}]")
    for s in T_["sfx"]:
        i = inp(os.path.join(build, s["dir"], s["file"] + ".mp3")); ms = int(max(0, s["at"]) * 1000)
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={s['gain']}dB,adelay={ms}|{ms}[x{i}]"); fx.append(f"[x{i}]")
    if os.path.exists(sh):
        i = inp(sh); ms = 23800
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume=-6dB,adelay={ms}|{ms}[x{i}]"); fx.append(f"[x{i}]")
    filt.append(f"{''.join(vl)}amix=inputs={len(vl)}:normalize=0[vo0]")
    filt.append("[vo0]highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,equalizer=f=3500:t=q:w=1:g=2[vop]")
    filt.append(f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0[fx]")
    mi = inp(os.path.join(build, "bed.mp3"), True)
    filt.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},volume=-24dB,afade=t=in:d=0.4,afade=t=out:st={dur - 2}:d=2[mus]")
    filt.append(f"[vop][mus][fx]amix=inputs=3:normalize=0,apad,atrim=0:{dur},loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000[out]")
    mix = os.path.join(build, "host_mix.m4a")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-c:a", "aac", "-b:a", "256k", mix], check=True)
    final = os.path.join(out, "host_viral_9x16.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(build, "host_video.mp4"), "-i", mix, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", final], check=True)
    print("final ->", final)


if __name__ == "__main__":
    {"html": cmd_html, "mix": cmd_mix}[sys.argv[1]]()
