"""The Race Reel, animated (adapted from viral-remake): 21 shots at the reference timings (71.6s), DMSetter context.
  python3 viral.py frames  -> hook clip frames (hook_clip.mp4 -> clipframes/f%04d.jpg)
  python3 viral.py html    -> race.html + timeline_race.json
  node render_viral.mjs    -> ../../build/race_video.mp4
  python3 viral.py mix     -> out/viral_9x16.mp4 (+ _nomusic)"""
import json, os, re, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
studio = os.path.abspath(os.path.join(here, "..", ".."))
build = os.path.join(studio, "build")
NS = {"__file__": os.path.join(here, "build.py"), "__name__": "lib"}
exec(open(os.path.join(here, "build.py")).read(), NS)
S, SBCSS, K, O = [(a, b, c, d) for a, b, c, d in NS["S"]], NS["CSS"], NS["K"], NS["O"]
FIT = json.load(open(os.path.join(here, "vo_fit.json"))) if os.path.exists(os.path.join(here, "vo_fit.json")) else {}

VCSS = f"""
html,body{{margin:0;background:#000}}
body{{display:block;width:1080px;height:1920px;overflow:hidden;gap:0}}
#stage{{width:540px;height:960px;zoom:2;position:relative;overflow:hidden}}
.fr{{position:absolute;inset:0;opacity:0;--pre:0ms}}.fr.on{{opacity:1}}
.vis>*{{animation:vin .55s cubic-bezier(.2,.9,.3,1.3) calc(var(--e,0)*130ms + 140ms) both}}
.vis>*:nth-child(1){{--e:0}}.vis>*:nth-child(2){{--e:1}}.vis>*:nth-child(3){{--e:2}}.vis>*:nth-child(4){{--e:3}}.vis>*:nth-child(5){{--e:4}}.vis>*:nth-child(6){{--e:5}}
@keyframes vin{{from{{opacity:0;translate:0 40px;scale:.92}}}}
.hookvid{{position:absolute;left:0;top:-120px;width:540px;height:960px;object-fit:cover;z-index:0;animation:none!important}}
.fr.hasclip .scrub{{opacity:.0}}
.cap b .w{{display:inline-block;animation:wIn .28s cubic-bezier(.2,.9,.3,1.4) calc(var(--wd) - var(--pre)) both}}
@keyframes wIn{{from{{opacity:0;translate:0 14px;scale:.9}}}}
.cap{{animation:capIn .4s cubic-bezier(.2,.9,.3,1.3) 80ms both}}@keyframes capIn{{from{{opacity:0;translate:0 30px}}}}
.ph .m{{animation:msgIn .32s cubic-bezier(.2,.9,.3,1.3) calc(var(--i)*650ms + 500ms) both}}
@keyframes msgIn{{from{{opacity:0;translate:0 18px;scale:.9}}}}
.bars i{{transform-origin:bottom;animation:grow .7s cubic-bezier(.2,.9,.3,1.2) calc(var(--k,0)*140ms + 250ms) both}}@keyframes grow{{from{{scale:1 0}}}}
.meter i{{animation:fill 1s ease-out .5s both}}@keyframes fill{{from{{width:0!important}}}}
.big0{{animation:stampIn .5s cubic-bezier(.3,1.6,.5,1) .2s both!important}}@keyframes stampIn{{from{{opacity:0;scale:2.4}}}}
.cl{{animation:vin .6s cubic-bezier(.2,.9,.3,1.3) .1s both}}
.wm2{{animation:vin .5s ease .5s both}}
.g{{animation:vin .4s cubic-bezier(.2,.9,.3,1.4) calc(var(--k,0)*70ms + 100ms) both}}
.fr .scrub i.o{{animation:blink 1.2s steps(2) infinite}}@keyframes blink{{50%{{opacity:.55}}}}
"""


def cmd_frames():
    dst = os.path.join(here, "clipframes"); os.makedirs(dst, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(here, "hook_clip.mp4"), "-vf", "fps=30,scale=1080:-2",
                    "-q:v", "3", os.path.join(dst, "f%04d.jpg")], check=True)
    print(len(os.listdir(dst)), "frames")


def cmd_html():
    secs, sfx = [], []
    for i, (a, b, c, v) in enumerate(S):
        dur = b - a
        n = len(re.findall(r"\S+", re.sub(r"<[^>]+>", "", NS["cap"](c))))
        cap = NS["cap"](c)
        # caption words: spread over the first 55% of the shot, starting right after the transition
        parts = []
        k = 0
        for m in re.finditer(r'(<span class="o">)?([^<]+)(</span>)?', cap):
            txt, hl = m.group(2), bool(m.group(1))
            ws = txt.split()
            span = max(0.45, min(2.4, dur * 0.55))
            inner = " ".join(f'<span class="w" style="--wd:{int(250 + (k + j) / max(1, n) * span * 1000)}ms">{w}</span>' for j, w in enumerate(ws))
            parts.append(f'<span class="o">{inner}</span>' if hl else inner); k += len(ws)
        capw = " ".join(parts)
        vis = v
        vis = vis.replace('<div class="grid13">', '<div class="grid13">').replace('class="g k"', 'class="g k"')
        vis = re.sub(r'<div class="g( k)?"', lambda m, c=iter(range(99)): f'<div class="g{m.group(1) or ""}" style="--k:{next(c)}"', vis) if 'grid13' in vis else vis
        scrub = "".join(f'<i class="{"on" if j < i else "o" if j == i else ""}"></i>' for j in range(len(S)))
        cls = "fr"
        secs.append(f'<section class="{cls}" data-t0="{a:.3f}" data-dur="{dur:.3f}"><div class="scrub">{scrub}</div><div class="vis">{vis}</div><div class="cap"><b>{capw}</b></div></section>')
    def X(f, at, g, d="sfx"): sfx.append({"file": f, "at": at, "gain": g, "dir": d})
    for i, (a_, b_, c_, v_) in enumerate(S):
        if i: X("whoosh", round(a_ - 0.12, 3), -15)
    X("sent", 0.35, -9, "sfx2"); X("shutter", 1.1, -12, "sfx2")
    for j, tt in enumerate([1.7, 1.95, 2.2, 2.45, 2.7]): X("bubble", tt, -13, "sfx2")
    X("drop", 0.05, -9, "sfx2")
    for tt in (5.2, 6.2, 7.2): X("beep", tt, -12, "sfx2")
    X("riser", 6.0, -17); X("beep", 8.55, -8, "sfx2")
    for tt in (9.0, 11.0, 13.0, 15.0): X("tick", tt, -17, "sfx2")
    X("heart", 12.3, -14, "sfx2")
    X("scratch", 10.15, -8, "sfx2"); X("drop", 10.4, -7, "sfx2"); X("win", 10.5, -12, "sfx2")
    X("snore", 11.1, -15, "sfx2")
    for tt in (11.7, 12.2, 12.7): X("bubble", tt, -13, "sfx2")
    for tt in (16.9, 18.0, 19.1, 20.2): X("sent", tt, -11, "sfx2")
    X("click", 22.5, -8); X("stamp", 23.55, -6, "sfx2"); X("ding", 23.7, -10)
    X("pop", 27.6, -12); X("sad", 29.05, -12, "sfx2")
    X("beep", 31.3, -10, "sfx2"); X("click", 33.1, -8); X("win", 33.3, -13, "sfx2"); X("ding", 33.4, -10)
    nclip = len(os.listdir(os.path.join(here, "clipframes"))) if os.path.isdir(os.path.join(here, "clipframes")) else 0
    css = re.sub(r"body\{\{?display:grid[^}]*\}", "", SBCSS) + VCSS
    html = f'''<!doctype html><html><head><meta charset="utf-8"><title>The Race</title><style>{css}</style></head>
<body><div id="stage">{"".join(secs)}</div><script>
const NC={nclip};
const S=[...document.querySelectorAll('.fr')].map(el=>({{el,t0:+el.dataset.t0,dur:+el.dataset.dur,clip:el.querySelector('[data-clip]')}}));
window.ready=(async()=>{{await document.fonts.ready;S.forEach(s=>{{s.anims=s.el.getAnimations({{subtree:true}});s.anims.forEach(a=>a.pause())}});}})();
const ease=x=>x>=1?1:1-Math.pow(2,-10*x),TR=.34,TYPES=['left','up','zoom'];
async function setClip(s,loc){{if(!s.clip||!NC)return;const i=Math.min(NC,Math.max(1,1+Math.floor(loc/1000*30)));
 const src='clipframes/f'+String(i).padStart(4,'0')+'.jpg';if(s.clip.dataset.src!==src){{s.clip.src=src;s.clip.dataset.src=src;await s.clip.decode().catch(()=>{{}})}}}}
const fmt=v=>{{v=Math.floor(v);return Math.floor(v/60)+':'+String(v%60).padStart(2,'0')}};
window.render=async t=>{{let cur=0;S.forEach((s,i)=>{{if(t>=s.t0)cur=i}});
 const lt=t-S[cur].t0,inT=cur>0&&lt<TR,p=ease(lt/TR),ty=TYPES[cur%3];
 for(const [i,s] of S.entries()){{const on=i===cur||(inT&&i===cur-1);s.el.classList.toggle('on',on);s.el.style.transform='';s.el.style.filter='';s.el.style.opacity='';s.el.style.zIndex=i===cur?2:1;
  if(!on)continue;const loc=(t-s.t0)*1000;s.el.querySelectorAll('.tm[data-k]').forEach(e=>{{const l=loc/1000;e.textContent=fmt(e.dataset.k==='win'?Math.min(38,l/1.2*38):Math.min(554,l/5*554))}});s.anims.forEach(a=>a.currentTime=Math.max(0,loc));await setClip(s,Math.min(loc,s.dur*1000));}}
 if(inT){{const a=S[cur].el,b=S[cur-1].el;
  if(ty==='left'){{a.style.transform=`translateX(${{(1-p)*100}}%) rotate(${{(1-p)*4}}deg)`;b.style.transform=`translateX(${{-p*60}}%) rotate(${{-p*3}}deg)`;b.style.filter=`blur(${{p*6}}px)`}}
  else if(ty==='up'){{a.style.transform=`translateY(${{(1-p)*100}}%)`;b.style.transform=`translateY(${{-p*40}}%) scale(${{1-p*.1}})`;b.style.filter=`blur(${{p*6}}px)`}}
  else{{a.style.transform=`scale(${{.7+.3*p}})`;a.style.opacity=p;b.style.transform=`scale(${{1+p*.6}})`;b.style.filter=`blur(${{p*10}}px)`}}
 }}}};
</script></body></html>'''
    open(os.path.join(here, "race.html"), "w").write(html)
    cues = [{"id": f"rc_{k}_f", "at": round(v["at"], 3)} for k, v in FIT.items()]
    json.dump({"duration": 35.0, "fps": 30, "cues": cues, "sfx": sfx}, open(os.path.join(here, "timeline_race.json"), "w"), indent=1)
    print("ok", len(S), "scenes", nclip, "clip frames")


def cmd_mix():
    T = json.load(open(os.path.join(here, "timeline_race.json"))); dur = T["duration"]
    out = os.path.join(here, "out"); os.makedirs(out, exist_ok=True)
    for music in (True, False):
        inputs, filt, vo, fx = [], [], [], []
        def inp(p, loop=False):
            if loop: inputs.extend(["-stream_loop", "-1"])
            inputs.extend(["-i", p]); return inputs.count("-i") - 1
        for c in T["cues"]:
            if not os.path.exists(os.path.join(build, "vo", c["id"] + ".mp3")): continue
            i = inp(os.path.join(build, "vo", c["id"] + ".mp3")); ms = int(c["at"] * 1000)
            filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]"); vo.append(f"[v{i}]")
        for s in T["sfx"]:
            i = inp(os.path.join(build, s.get("dir", "sfx"), s["file"] + ".mp3")); ms = int(max(0, s["at"]) * 1000)
            filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={s['gain']}dB,adelay={ms}|{ms}[x{i}]"); fx.append(f"[x{i}]")
        filt.append(f"{''.join(vo)}amix=inputs={len(vo)}:normalize=0[vo0]")
        filt.append("[vo0]highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,equalizer=f=3500:t=q:w=1:g=2[vop]")
        filt.append(f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0[fx]")
        if music:
            mi = inp(os.path.join(build, "bed.mp3"), loop=True)
            filt.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},volume=-23dB,afade=t=in:d=0.4,afade=t=out:st={dur - 2}:d=2[mus]")
            filt.append(f"[vop][mus][fx]amix=inputs=3:normalize=0,apad,atrim=0:{dur},loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000[out]")
        else:
            filt.append(f"[vop][fx]amix=inputs=2:normalize=0,apad,atrim=0:{dur},loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000[out]")
        mix = os.path.join(build, f"race_mix_{int(music)}.m4a")
        subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-c:a", "aac", "-b:a", "256k", mix], check=True)
        final = os.path.join(out, "race_9x16.mp4" if music else "race_9x16_nomusic.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(build, "race_video.mp4"), "-i", mix, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", final], check=True)
        print("final ->", final)


if __name__ == "__main__":
    {"frames": cmd_frames, "html": cmd_html, "mix": cmd_mix}[sys.argv[1]]()
