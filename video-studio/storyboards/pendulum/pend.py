"""Pendulum-style motion-graphics reel in DMSetter colors. Effects-only sound (no voice, no music).
python3 pend.py html -> pend.html + timeline_pend.json ; node render_pend.mjs -> ../../build/pend_video.mp4 ; python3 pend.py mix -> out/pendulum_effects_only.mp4"""
import json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__)); studio = os.path.abspath(os.path.join(here, "..", "..")); build = os.path.join(studio, "build")
D = 21.0
def logo():
    s = open(os.path.join(studio, "brand", "logo", "svg", "mark_primary.svg")).read()
    return s.replace('width="260" height="260"', 'width="120" height="120"')
def X(L, f, at, g, d="sfx"): L.append({"file": f, "at": round(at, 3), "gain": g, "dir": d})
def cmd_html():
    open(os.path.join(here, "pend.html"), "w").write(open(os.path.join(here, "template.html")).read().replace("{{LOGO}}", logo()))
    S = []
    for k in range(6): X(S, "swish", 0.2 + k, -13, "sfx3")               # pendulum passes, once a second
    for tt in (0.25, 2.25, 4.25): X(S, "tick2", tt, -11, "sfx3")           # text reveals
    X(S, "whoosh", 5.4, -9); X(S, "thud", 5.95, -10, "sfx3"); X(S, "lamp", 6.05, -10, "sfx3")
    for tt in (6.6, 7.7, 8.6): X(S, "swish", tt, -16, "sfx3")             # lamp swings
    X(S, "whoosh", 9.25, -11); X(S, "pop", 9.55, -12); X(S, "ding", 9.62, -13)
    X(S, "whoosh", 11.2, -16); X(S, "click", 11.75, -9)                    # step 1
    X(S, "whoosh", 13.4, -14); X(S, "click", 13.6, -9)                     # step 2
    X(S, "whoosh", 15.5, -15); X(S, "click", 15.7, -9)                     # step 3
    for j in range(10): X(S, "tick2", 16.35 + j * 0.1, -16 + j * 0.4, "sfx3")  # progress ticks
    X(S, "ding", 17.5, -9)
    X(S, "whoosh", 17.8, -14); X(S, "pop", 18.15, -12); X(S, "pop", 19.05, -10); X(S, "click", 19.4, -9); X(S, "tick2", 20.0, -12, "sfx3")
    json.dump({"duration": D, "fps": 30, "sfx": S}, open(os.path.join(here, "timeline_pend.json"), "w"), indent=1); print("ok", len(S), "sfx")
def cmd_mix():
    T = json.load(open(os.path.join(here, "timeline_pend.json"))); out = os.path.join(here, "out"); os.makedirs(out, exist_ok=True)
    inputs, filt, fx = [], [], []
    for s in T["sfx"]:
        inputs += ["-i", os.path.join(build, s["dir"], s["file"] + ".mp3")]; i = len(fx); ms = int(max(0, s["at"]) * 1000)
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={s['gain']}dB,adelay={ms}|{ms}[x{i}]"); fx.append(f"[x{i}]")
    filt.append(f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0,apad,atrim=0:{D},loudnorm=I=-17:TP=-1.5:LRA=7,aresample=48000[out]")
    mix = os.path.join(build, "pend_mix.m4a")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-c:a", "aac", "-b:a", "192k", mix], check=True)
    final = os.path.join(out, "pendulum_effects_only.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(build, "pend_video.mp4"), "-i", mix, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", final], check=True); print("final ->", final)
if __name__ == "__main__": {"html": cmd_html, "mix": cmd_mix}[sys.argv[1]]()
