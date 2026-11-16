"""Animated one-page 'blueprint' for a LinkedIn post: cursor clicks through 4 steps, numbers count up. 1080x1350, 9s loop.
python3 onepage.py html -> onepage.html + timeline_onepage.json ; node render_onepage.mjs -> ../../build/onepage_video.mp4 ; python3 onepage.py export -> out/onepage.mp4 + out/onepage.gif"""
import json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__)); studio = os.path.abspath(os.path.join(here, "..", "..")); build = os.path.join(studio, "build")
LOGO = open(os.path.join(studio, "brand", "logo", "svg", "mark_primary.svg")).read()
K, O, CR, BL = "#1B1B1B", "#D8541E", "#F4F0E8", "#3A6FF0"
D = 9.0
def logo(px): return LOGO.replace('width="260" height="260"', f'width="{px}" height="{px}"')
# cursor waypoints (time, x, y) in 540x675 space; click times
WP = [(0, 470, 640), (1.0, 470, 640), (1.9, 440, 140), (2.15, 440, 140), (2.9, 42, 266), (3.2, 42, 266), (3.5, 42, 291), (3.8, 42, 291), (4.1, 42, 316), (4.4, 42, 316), (5.0, 300, 400), (6.6, 400, 520), (7.6, 400, 520), (8.3, 360, 622), (8.6, 360, 622), (9.0, 360, 622)]
CLICKS = [2.15, 3.2, 3.8, 4.4, 8.6]
kf = "".join(f"{t / D * 100:.3f}%{{left:{x}px;top:{y}px;animation-timing-function:cubic-bezier(.45,0,.2,1)}}" for t, x, y in WP)
rings = "".join(f'<i class="ring" style="left:{x}px;top:{y}px;--t:{c}s"></i>' for c in CLICKS for (t, x, y) in [min(WP, key=lambda w: abs(w[0] - c))])
CSS = f"""@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1350px;overflow:hidden;background:#000;font-family:Inter,sans-serif}}
#s{{width:540px;height:675px;zoom:2;position:relative;overflow:hidden;background:radial-gradient(120% 90% at 50% 30%,#F7F2E9 0%,#ECE6DA 70%,#E2DBCD 100%)}}
#s::before{{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.04) 0 1px,transparent 1px 27px),repeating-linear-gradient(90deg,rgba(0,0,0,.04) 0 1px,transparent 1px 27px)}}
.mono{{font-family:'JetBrains Mono',monospace}}
.top{{position:absolute;left:22px;right:22px;top:14px;display:flex;justify-content:space-between;font:700 8.5px 'JetBrains Mono';color:#8a8372;letter-spacing:.06em}}.top b{{color:{O}}}
h1{{position:absolute;left:22px;right:22px;top:34px;font:900 31px/1.04 Inter;letter-spacing:-.04em;color:{K}}}h1 span{{color:{O}}}
.sub{{position:absolute;left:22px;top:100px;font:600 11px Inter;color:#6D665B}}
.cd{{position:absolute;left:22px;right:22px;background:#FBFAF6;border:2px solid {K};border-radius:8px;box-shadow:4px 4px 0 rgba(0,0,0,.18);padding:10px 14px;animation:cin .5s cubic-bezier(.2,.9,.3,1.3) var(--a) both}}
@keyframes cin{{from{{opacity:0;translate:0 26px;scale:.97}}}}
.cd .lb{{font:700 8.5px 'JetBrains Mono';color:{O};letter-spacing:.08em}}.cd h2{{font:800 15px Inter;letter-spacing:-.02em;margin:2px 0 6px}}
.tg{{position:absolute;right:16px;top:20px;width:46px;height:24px;border-radius:12px;background:#c9c2b2;animation:tgOn .2s ease 2.15s both}}.tg i{{position:absolute;left:3px;top:3px;width:18px;height:18px;border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.3);animation:kn .2s ease 2.15s both}}
@keyframes tgOn{{to{{background:{O}}}}}@keyframes kn{{to{{left:25px}}}}
.badge{{position:absolute;right:76px;top:22px;font:800 10px Inter;color:{O};border:2px solid {O};border-radius:6px;padding:2px 7px;animation:cin .3s ease 2.3s both}}
.ck{{display:flex;align-items:center;gap:8px;font:700 12px Inter;height:25px}}.ck u{{width:15px;height:15px;border:2px solid {K};border-radius:4px;background:#fff;display:grid;place-items:center;font:900 11px Inter;text-decoration:none;color:#fff;animation:ckOn .15s ease var(--c) both}}
@keyframes ckOn{{to{{background:{O};border-color:{O}}}}}
.chat{{font:500 11px Inter}}.b1{{display:inline-block;background:#262626;color:#fff;border-radius:12px;padding:5px 10px;margin:2px 0;animation:cin .3s ease 5.0s both}}.b2{{display:block;width:max-content;margin-left:auto;background:linear-gradient(135deg,#3797F0,#A033FF);color:#fff;border-radius:12px;padding:5px 10px;animation:cin .3s ease 5.9s both}}
.m{{display:flex;gap:10px;margin-top:2px}}.mc{{flex:1;background:#fff;border:2px solid #cfc8b8;border-radius:7px;padding:6px 8px}}.mc small{{display:block;font:700 7.5px 'JetBrains Mono';color:#8a8372;letter-spacing:.06em}}.mc b{{display:block;font:900 24px Inter;letter-spacing:-.03em;color:{K};font-variant-numeric:tabular-nums}}.mc.o b{{color:{O}}}
.meter{{height:9px;border:2px solid {K};border-radius:5px;margin-top:5px;overflow:hidden;background:#fff}}.meter i{{display:block;height:100%;background:{O};width:100%;transform-origin:left;animation:mf 1.2s ease-out 6.5s both}}@keyframes mf{{from{{scale:0 1}}}}
.ill{{position:absolute;right:14px;top:-9px;background:{O};color:#fff;font:800 8px Inter;padding:3px 8px;border-radius:3px;rotate:4deg;animation:cin .3s ease 6.6s both}}
.foot{{position:absolute;left:22px;right:22px;bottom:16px;height:36px;display:flex;align-items:center;gap:10px}}.foot .cb{{flex:1;height:36px;border:2px solid {K};border-radius:18px;background:#fff;padding:0 14px;display:flex;align-items:center;font:800 13px Inter;box-shadow:3px 3px 0 rgba(0,0,0,.18)}}.foot .cb span{{display:inline-block;overflow:hidden;white-space:nowrap;width:0;animation:ty .5s steps(5) 8.65s both}}@keyframes ty{{to{{width:48px}}}}
.cur{{position:absolute;z-index:30;width:22px;height:22px;margin:-2px 0 0 -2px;animation:cur {D}s linear both;filter:drop-shadow(1px 3px 2px rgba(0,0,0,.35))}}@keyframes cur{{{kf}}}
.ring{{position:absolute;z-index:29;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;border:3px solid {O};animation:rg .5s ease-out var(--t) forwards;opacity:0}}@keyframes rg{{0%{{opacity:.9;scale:.3}}100%{{opacity:0;scale:1.6}}}}
.lg{{position:absolute;right:22px;top:10px;}}
.fd{{position:absolute;inset:0;z-index:60;background:#EFE9DD;pointer-events:none;animation:fdk {D}s linear both}}@keyframes fdk{{0%{{opacity:1}}4%{{opacity:0}}94%{{opacity:0}}100%{{opacity:1}}}}"""
html = f'''<!doctype html><html><head><meta charset="utf-8"><title>onepage</title><style>{CSS}</style></head><body><div id="s">
<div class="top"><span>DRAWING NO. 038-2026 · SHEET 1 OF 1</span><span>REV <b>01</b></span></div>
<h1 style="animation:cin .5s ease 0s both">Reply to every lead <span>in seconds.</span></h1><div class="sub" style="animation:cin .5s ease .3s both">One page: how a coach's inbox runs itself.</div>
<div class="cd" style="top:122px;height:70px;--a:.6s"><div class="lb">01 · CONNECT</div><h2>Connect your Instagram</h2><div class="tg"><i></i></div><div class="badge">Connected ✓</div></div>
<div class="cd" style="top:204px;height:128px;--a:1.0s"><div class="lb">02 · PICK</div><h2>Choose the replies you want</h2>
<div class="ck"><u style="--c:3.2s">✓</u>First reply, in seconds</div><div class="ck"><u style="--c:3.8s">✓</u>One question about their goal</div><div class="ck"><u style="--c:4.4s">✓</u>Suggest a call time</div></div>
<div class="cd" style="top:344px;height:98px;--a:4.7s"><div class="lb">03 · ASK</div><div class="chat"><span class="b1">What's your goal right now?</span><span class="b2">Grow my client list</span></div></div>
<div class="cd" style="top:454px;height:112px;--a:6.2s"><div class="ill">VALUES ILLUSTRATIVE</div><div class="lb">04 · RESULT</div><h2>Booked while you sleep</h2><div class="m"><div class="mc o"><small>FIRST REPLY</small><b class="cnt" data-k="mmss" data-t0="6.4" data-t1="7.4" data-to="38">0:00</b></div><div class="mc"><small>CALLS BOOKED</small><b class="cnt" data-k="int" data-t0="6.8" data-t1="7.8" data-to="3">0</b></div></div><div class="meter"><i></i></div></div>
<div class="foot" style="animation:cin .4s ease 8.0s both"><div class="cb"><span>SPEED</span></div>{logo(34)}</div>
<div class="fd"></div>{rings}<svg class="cur" viewBox="0 0 24 24"><path d="M3 2l17 8-7 2-3 7z" fill="#1B1B1B" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>
</div><script>
const A=()=>document.getAnimations?document.getAnimations():[];window.ready=(async()=>{{await document.fonts.ready;A().forEach(a=>a.pause())}})();
const C=[...document.querySelectorAll('.cnt')],f=(v,k)=>k==='int'?String(Math.round(v)):Math.floor(v/60)+':'+String(Math.floor(v)%60).padStart(2,'0');
window.render=async t=>{{A().forEach(a=>{{a.pause();a.currentTime=t*1000}});C.forEach(e=>{{const t0=+e.dataset.t0,t1=+e.dataset.t1,to=+e.dataset.to,p=Math.min(1,Math.max(0,(t-t0)/(t1-t0)));e.textContent=f(to*(1-Math.pow(1-p,3)),e.dataset.k)}})}};
</script></body></html>'''
def cmd_html():
    open(os.path.join(here, "onepage.html"), "w").write(html); json.dump({"duration": D, "fps": 30}, open(os.path.join(here, "timeline_onepage.json"), "w")); print("ok")
def cmd_export():
    out = os.path.join(here, "out"); os.makedirs(out, exist_ok=True); src = os.path.join(build, "onepage_video.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart", os.path.join(out, "onepage.mp4")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", "fps=15,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=4", "-loop", "0", os.path.join(out, "onepage.gif")], check=True)
    for f in ("onepage.mp4", "onepage.gif"): print(f, round(os.path.getsize(os.path.join(out, f)) / 1e6, 2), "MB")
if __name__ == "__main__": {"html": cmd_html, "export": cmd_export}[sys.argv[1]]()
