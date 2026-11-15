"""'Comment SCRIPT' Reel: Seedance clips (scenes 1, 3, 4) + our paper engine for everything else.
  python3 reel.py frames   -> extract clip frames (clips/*.mp4 -> clipframes/<k>/f%04d.jpg)
  python3 reel.py html     -> reel.html + timeline_reel.json
  node render_reel.mjs     -> ../build/reel_video.mp4
  python3 reel.py mix      -> out/script_reel_9x16.mp4 (+ _nomusic version for IG trending audio)
"""
import json, os, re, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
studio = os.path.abspath(os.path.join(here, ".."))
build = os.path.join(studio, "build")
V = {"__file__": os.path.join(studio, "storyboards", "coach-compare", "video.py"), "__name__": "lib"}
exec(open(V["__file__"]).read(), V)  # brings B (components), P (paper anim engine), words, caption_html, CSS
B, P = V["B"], V["P"]
C, phone, tag = B["C"], B["phone"], B["tag"]
K, O, T_, A = B["K"], B["O"], B["T_"], B["A"]
LOGO = open(os.path.join(studio, "brand", "logo", "svg", "mark_primary.svg")).read()
TEMPO = {"narrator": 1.22, "ben": 1.1}
GAP = 0.14
CLIPS = {"c1": "s1_night_buzz", "c3": "s3_morning_shock", "c4": "s4_cloud_setter"}


def ben(expr, size, x, y):
    return f'<div class="chr" style="left:{x}px;top:{y}px">{C.char_svg("low", expr, size)}</div>'


def say(text, x, y, who="BEN"):
    return f'<div class="say" style="left:{x}px;top:{y}px"><b>{who}</b>{text}</div>'


SCENES = [
    dict(label="For coaches", right="11:41 PM", num="", clip="c1", dark=True,
         vis=f'<div class="tag xl" style="left:22px;top:-10px;background:{O};transform:rotate(-4deg);--at:100ms">COACHES 👇</div>'
             '<div class="notif2" style="--at:700ms"><i></i><div><b>New lead · now</b>hey! how much is your coaching? 👀</div></div>',
         cap='If this happens in your DMs <span class="hl">every week…</span>', lines=[("s1", "narrator")],
         sfx=[(0.0, "boom", -9), (0.65, "buzz", -8), (1.4, "buzz", -10)]),
    dict(label="11 minutes later", right="11:52 PM", num="11",
         vis=phone([("in", "how much is your coaching?"), ("in", "nvm, went with another coach 🙏")], x=120, y=20, rot=2, w=300, h=380, seen=False, name="New lead", hl=1)
             + '<div class="ring" style="--at:2600ms"></div>' + ben("asleep", 130, 360, 330),
         cap='11 minutes later… <span class="hlo">they’re gone.</span>', lines=[("s2", "narrator")], msgs=[0, (0, 2.2)],
         sfx=[(2.65, "whoosh", -12)]),
    dict(label="Next morning", right="9:02 AM", num="", clip="c3",
         vis=say("Sorry, just saw this…", 290, 170) + '<div class="sorry" style="--at:300ms">Hey! Sorry, just saw this 😅</div>',
         cap='You didn’t lose them to price. <span class="hl">You lost them to time.</span>', lines=[("s3a", "ben"), ("s3b", "narrator")], says=[0],
         sfx=[(0.2, "pop", -12), (2.3, "boom", -10)]),
    dict(label="With DMSetter", right="11:41 PM", num="", clip="c4", dark=True,
         vis=phone([("in", "how much is your coaching?"), ("out", "Hey! Love that you reached out 🙌 What's your goal?"), ("in", "drop 8kg before summer"),
                    ("out", "Quick call Thursday 3 PM?"), ("in", "yes!! 🙌")], x=14, y=6, rot=-3, w=290, h=380, seen=False, name="New lead", hl=1)
             + '<div class="clock2" style="--at:1400ms">replied in 38 sec</div><div class="stamp3" style="--at:5000ms">BOOKED</div>',
         cap='With <span class="hlo">DMSetter</span>, you wake up to <span class="hl">booked calls.</span>', lines=[("s4", "narrator")],
         msgs=[0, (0, 1.2), (0, 2.2), (0, 3.2), (0, 4.2)], sfx=[(5.0, "boom", -8), (5.3, "ding", -9)]),
    dict(label="The fix", right="7 replies", num="7",
         vis="".join(f'<div class="card7" style="left:{40 + i * 62}px;top:{110 + abs(3 - i) * 14}px;rotate:{(i - 3) * 7}deg;--k:{i}"><div class="cin" style="background:{[O, K, T_, "#FBFAF6", O, T_, K][i]}"><b>{i + 1}</b><i></i><i></i><i></i></div></div>' for i in range(7))
             + ben("confused", 140, 200, 310) + f'<div class="tag" style="left:300px;top:40px;background:{A};transform:rotate(6deg)">copy-paste ready</div>',
         cap='7 replies that turn <span class="hlo">“how much?”</span> into a booked call.', lines=[("s5", "narrator")],
         sfx=[(0.3, "whoosh", -14)]),
    dict(label="Free for coaches", right="Now", num="→",
         vis='<div class="key press">SCRIPT</div><div class="cbox"><i></i><span class="typed">SCRIPT</span><b>&#10148;</b></div>'
             + f'<div class="tag" style="left:330px;top:30px;background:{O};transform:rotate(8deg)">I’ll DM it to you</div>' + ben("tired", 120, 20, 330),
         cap='Comment <span class="hl">“SCRIPT”</span> and I’ll send them to you.', lines=[("s6", "narrator")], cta=True,
         sfx=[(1.1, "click", -6)]),
    dict(label="DMSetter", right="Your DMs, handled", num="",
         vis=f'<div class="endlogo">{LOGO.replace("width=\"260\" height=\"260\"", "width=\"240\" height=\"240\"")}</div>'
             + '<div class="wm">DM<span>Setter</span></div><div class="outc">'
             + "".join(f'<div class="o" style="--k:{i}"><i>✓</i>{t}</div>' for i, t in enumerate(["Replies in seconds, 24/7", "Qualifies every lead", "Follows up until they answer", "Books calls into your calendar"])) + '</div>',
         cap='More booked calls. <span class="hlo">Zero DMs at 2 AM.</span>', lines=[("s7", "narrator")], end=True,
         sfx=[(0.2, "boom", -9)]),
]

EXTRA = f"""
.clip{{position:absolute;inset:0;width:540px;height:960px;object-fit:cover;z-index:0}}
.fr.hasclip .num{{display:none}}
.fr.hasclip .capbg{{position:absolute;left:0;right:0;bottom:0;height:420px;z-index:1;background:linear-gradient(rgba(244,240,232,0),rgba(244,240,232,.93) 38%,rgba(244,240,232,.98))}}
.fr.hasclip .vis,.fr.hasclip header,.fr.hasclip .cap{{z-index:3}}
.fr.dark header{{color:#F4F0E8;border-top-color:#F4F0E8;text-shadow:0 1px 8px rgba(0,0,0,.9)}}.fr.dark header .rule{{background:#F4F0E8}}
.fr.hasclip .scrub{{display:none}}
.chr{{position:absolute;z-index:4}}
.vis .ph .m{{animation:msgIn .32s cubic-bezier(.2,.9,.3,1.3) calc(var(--at,0ms) - var(--pre)) both}}
.notif2{{position:absolute;left:40px;right:40px;top:90px;z-index:6;display:flex;gap:12px;align-items:center;padding:14px 16px;border-radius:20px;background:rgba(250,248,244,.94);
 box-shadow:0 18px 40px rgba(0,0,0,.35);font:600 16px/1.3 Inter;color:{K};animation:dropN .55s cubic-bezier(.2,.9,.3,1.25) calc(var(--at) - var(--pre)) both}}
.notif2 i{{width:40px;height:40px;flex:none;border-radius:11px;background:linear-gradient(135deg,#F58529,#DD2A7B,#8134AF)}}
.notif2 b{{display:block;font:800 12px Inter;color:#6D665B;margin-bottom:2px}}
@keyframes dropN{{from{{translate:0 -160px;opacity:0}}}}
.ring{{position:absolute;left:112px;top:262px;width:300px;height:70px;border:5px solid #E8322D;border-radius:50%;rotate:-3deg;z-index:6;
 animation:ringIn .45s ease-out calc(var(--at) - var(--pre)) both}}@keyframes ringIn{{from{{clip-path:inset(0 100% 0 0);scale:1.15}}}}
.say{{position:absolute;z-index:8;max-width:160px;background:#fff;border:2.5px solid {K};border-radius:16px;padding:7px 11px;font:800 15px/1.2 Inter;box-shadow:0 5px 0 rgba(0,0,0,.15);
 animation:pop .42s cubic-bezier(.2,.9,.3,1.6) calc(var(--at,0ms) - var(--pre)) both}}
.say b{{display:block;font:900 9px Inter;letter-spacing:.14em;color:{O};margin-bottom:2px}}
.sorry{{position:absolute;left:150px;top:90px;z-index:6;background:linear-gradient(135deg,#3797F0,#A033FF);color:#fff;font:500 16px Inter;padding:10px 14px;border-radius:18px;
 box-shadow:0 10px 24px rgba(0,0,0,.25);animation:pop .4s cubic-bezier(.2,.9,.3,1.6) calc(var(--at) - var(--pre)) both}}
.clock2{{position:absolute;left:330px;top:40px;z-index:7;background:#fff;color:{O};font:800 15px Inter;padding:6px 12px;border-radius:16px;box-shadow:0 3px 0 #d0c8b8;rotate:4deg;
 animation:pop .45s cubic-bezier(.2,.9,.3,1.6) calc(var(--at) - var(--pre)) both}}
.stamp3{{position:absolute;left:150px;top:330px;z-index:9;padding:4px 12px;border:5px solid {O};color:{O};font:900 34px Inter;border-radius:10px;rotate:-12deg;background:rgba(244,240,232,.9);
 animation:stamp .32s cubic-bezier(.5,0,.8,.5) calc(var(--at) - var(--pre)) both}}
.card7{{position:absolute;width:80px;height:118px;animation:fan .6s cubic-bezier(.2,.9,.3,1.3) calc(var(--k)*90ms + 150ms - var(--pre)) both}}
@keyframes fan{{from{{translate:200px 120px;rotate:0deg;opacity:0}}}}
.cin{{width:100%;height:100%;border-radius:10px;box-shadow:0 6px 0 rgba(0,0,0,.2),0 14px 24px rgba(0,0,0,.18);padding:10px;color:#fff}}
.cin b{{font:900 26px Inter}}.cin i{{display:block;height:5px;border-radius:3px;background:rgba(255,255,255,.55);margin-top:9px}}
.card7:nth-of-type(4) .cin{{color:{K}}}.card7:nth-of-type(4) .cin i{{background:rgba(0,0,0,.25)}}
.key{{top:70px}}.cbox{{top:270px;font-weight:700;color:{K}}}
.typed{{display:inline-block;overflow:hidden;white-space:nowrap;animation:type .7s steps(6) calc(500ms - var(--pre)) both}}@keyframes type{{from{{width:0}}}}
.endlogo{{position:absolute;left:150px;top:10px;animation:phIn .7s cubic-bezier(.2,.9,.3,1.2) calc(0ms - var(--pre)) both}}
.wm{{position:absolute;left:0;right:0;top:250px;text-align:center;font:900 64px Inter;letter-spacing:-.04em;color:{K};animation:fadeUp .5s ease calc(250ms - var(--pre)) both}}.wm span{{color:{O}}}
.outc{{position:absolute;left:70px;right:70px;top:340px;display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.o{{background:#FBFAF6;border-radius:12px;padding:10px 12px;font:800 14px/1.25 Inter;display:flex;gap:8px;align-items:center;box-shadow:0 3px 0 #d8d1c3;
 animation:pop .45s cubic-bezier(.2,.9,.3,1.5) calc(var(--k)*180ms + 600ms - var(--pre)) both}}
.o i{{font-style:normal;flex:none;width:24px;height:24px;border-radius:50%;background:{O};color:#fff;display:grid;place-items:center;font:900 13px Inter}}
"""


def cmd_frames():
    for k, name in CLIPS.items():
        src = os.path.join(here, "clips", name + ".mp4"); dst = os.path.join(here, "clipframes", k)
        os.makedirs(dst, exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", "fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                        "-q:v", "3", os.path.join(dst, "f%04d.jpg")], check=True)
        print(k, len(os.listdir(dst)), "frames")


def cmd_html():
    t, secs, cues, sfx = 0.0, [], [], []
    n = len(SCENES)
    for si, s in enumerate(SCENES):
        cur = 0.12 if si else 0.05
        lines, wt = [], []
        for key, spk in s["lines"]:
            al = json.load(open(os.path.join(build, "vo", f"sr_{key}.json")))["alignment"]
            tp = TEMPO[spk]; al = {k: ([x / tp for x in v] if k.endswith("_seconds") else v) for k, v in al.items()}
            ws = V["words"](al); dur = al["character_end_times_seconds"][-1]
            lines.append(dict(at=cur, dur=dur, spk=spk)); cues.append({"id": f"sr_{key}_f", "at": round(t + cur, 3)})
            if spk == "narrator": wt += [cur + a for _, a, _ in ws]
            cur += dur + GAP
        dur = max(2.4, cur + 0.4) + (1.2 if s.get("end") else 0)
        vis = s["vis"]
        if "msgs" in s:
            L = lambda r: (lines[r[0]]["at"] + r[1]) if isinstance(r, tuple) else lines[r]["at"]
            it = iter([L(r) * 1000 for r in s["msgs"]])
            vis = re.sub(r'<div class="m (in|out)" style="--i:\d+">', lambda m: f'<div class="m {m.group(1)}" style="--at:{int(next(it, 0))}ms">', vis)
            for r in s["msgs"]: sfx.append({"file": "pop", "at": round(t + L(r), 3), "gain": -12})
        if "says" in s:
            vis = V["set_at"](vis, "say", [lines[i]["at"] * 1000 for i in s["says"]])
        if s.get("cta"): vis += P["confetti"](22, 7, 1100)
        if s.get("end"): vis += P["confetti"](30, 9, 300)
        for off, f, g in s["sfx"]: sfx.append({"file": f, "at": round(t + off, 3), "gain": g})
        if si: sfx.append({"file": "whoosh", "at": round(t - 0.12, 3), "gain": -15})
        cap = V["caption_html"](s["cap"], wt or [lines[-1]["at"]], 10 if si == 0 else 0)
        clip = s.get("clip")
        cls = "fr" + (" hasclip" if clip else "") + (" dark" if s.get("dark") else "")
        clip_html = f'<img class="clip" data-clip="{clip}"><div class="capbg"></div>' if clip else ""
        secs.append(f'''<section class="{cls}" data-t0="{t:.3f}" data-dur="{dur:.3f}" style="--dur:{dur:.2f}s;--pre:{300 if si == 0 else 0}ms">{clip_html}
<div class="num">{s["num"]}</div><header><div class="rule"></div><span>{s["label"]}</span><em>{s["right"]}</em></header>
<div class="vis">{vis}</div><div class="cap">{cap}</div></section>''')
        t += dur
    nframes = {k: len(os.listdir(os.path.join(here, "clipframes", k))) for k in CLIPS}
    css = B["BASE_CSS"] + B["EXTRA_CSS"] + P["ANIM_CSS"] + V["CSS"] + EXTRA
    html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Script Reel</title><style>{css}</style></head>
<body><div id="stage">{"".join(secs)}</div><script>
const NF={json.dumps(nframes)};
const S=[...document.querySelectorAll('.fr')].map(el=>({{el,t0:+el.dataset.t0,dur:+el.dataset.dur,clip:el.querySelector('.clip')}}));
window.ready=(async()=>{{await document.fonts.ready;S.forEach(s=>{{s.anims=s.el.getAnimations({{subtree:true}});s.anims.forEach(a=>a.pause())}});}})();
const ease=x=>x>=1?1:1-Math.pow(2,-10*x),TR=.34,TYPES=['left','up','zoom'];
async function setClip(s,loc){{if(!s.clip)return;const k=s.clip.dataset.clip,n=NF[k];
 const i=Math.min(n,Math.max(1,1+Math.floor(loc/1000/s.dur*n)));const src='clipframes/'+k+'/f'+String(i).padStart(4,'0')+'.jpg';
 if(s.clip.dataset.src!==src){{s.clip.src=src;s.clip.dataset.src=src;await s.clip.decode().catch(()=>{{}})}}}}
window.render=async t=>{{let cur=0;S.forEach((s,i)=>{{if(t>=s.t0)cur=i}});
 const lt=t-S[cur].t0,inT=cur>0&&lt<TR,p=ease(lt/TR),ty=TYPES[cur%3];
 for(const [i,s] of S.entries()){{const on=i===cur||(inT&&i===cur-1);s.el.classList.toggle('on',on);s.el.style.transform='';s.el.style.filter='';s.el.style.zIndex=i===cur?2:1;
  if(!on)continue;const loc=(t-s.t0)*1000;s.anims.forEach(a=>a.currentTime=Math.max(0,loc));await setClip(s,Math.min(loc,s.dur*1000));}}
 if(inT){{const a=S[cur].el,b=S[cur-1].el;
  if(ty==='left'){{a.style.transform=`translateX(${{(1-p)*100}}%) rotate(${{(1-p)*4}}deg)`;b.style.transform=`translateX(${{-p*60}}%) rotate(${{-p*3}}deg)`;b.style.filter=`blur(${{p*6}}px)`}}
  else if(ty==='up'){{a.style.transform=`translateY(${{(1-p)*100}}%)`;b.style.transform=`translateY(${{-p*40}}%) scale(${{1-p*.1}})`;b.style.filter=`blur(${{p*6}}px)`}}
  else{{a.style.transform=`scale(${{.7+.3*p}})`;a.style.opacity=p;b.style.transform=`scale(${{1+p*.6}})`;b.style.filter=`blur(${{p*10}}px)`}}
 }} else S.forEach(s=>s.el.style.opacity='');}};
</script></body></html>'''
    open(os.path.join(here, "reel.html"), "w").write(html)
    json.dump({"duration": round(t, 3), "fps": 30, "cues": cues, "sfx": sfx}, open(os.path.join(here, "timeline_reel.json"), "w"), indent=1)
    print("duration", round(t, 2))


def cmd_mix():
    T = json.load(open(os.path.join(here, "timeline_reel.json"))); dur = T["duration"]
    out = os.path.join(here, "out"); os.makedirs(out, exist_ok=True)
    for music in (True, False):
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
        filt.append(f"{''.join(vo)}amix=inputs={len(vo)}:normalize=0[vo0]")
        filt.append("[vo0]highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,equalizer=f=3500:t=q:w=1:g=2[vop]")
        filt.append(f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0[fx]")
        if music:
            mi = inp(os.path.join(build, "bed.mp3"), loop=True)
            filt.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},volume=-23dB,afade=t=in:d=0.4,afade=t=out:st={dur - 2}:d=2[mus]")
            filt.append(f"[vop][mus][fx]amix=inputs=3:normalize=0,apad,atrim=0:{dur},loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000[out]")
        else:
            filt.append(f"[vop][fx]amix=inputs=2:normalize=0,apad,atrim=0:{dur},loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000[out]")
        mix = os.path.join(build, f"reel_mix_{int(music)}.m4a")
        subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-c:a", "aac", "-b:a", "256k", mix], check=True)
        final = os.path.join(out, "script_reel_9x16.mp4" if music else "script_reel_9x16_nomusic.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(build, "reel_video.mp4"), "-i", mix, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", final], check=True)
        print("final ->", final)


if __name__ == "__main__":
    {"frames": cmd_frames, "html": cmd_html, "mix": cmd_mix}[sys.argv[1]]()
