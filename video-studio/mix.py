"""Audio mix: VO lines placed on cues, looped music bed ducked under VO, SFX hits, loudness -14 LUFS.
Usage: python3 mix.py <project_dir>  -> build/mix.m4a, then muxes build/video_<fmt>.mp4 into <project>/out/final_<fmt>.mp4"""
import json, os, subprocess, sys

proj = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
build = os.path.join(here, "build")
T = json.load(open(os.path.join(proj, "timeline.json")))
cues = json.load(open(os.path.join(proj, "vo_cues.json")))
dur = T["duration"]

inputs, filt, vo_labels, fx_labels = [], [], [], []
idx = 0
def inp(path, loop=False):
    global idx
    if loop: inputs.extend(["-stream_loop", "-1"])
    inputs.extend(["-i", path]); idx += 1; return idx - 1

for c in cues:
    i = inp(os.path.join(build, "vo", c["id"] + ".mp3"))
    ms = int(c["at"] * 1000)
    filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]"); vo_labels.append(f"[v{i}]")
for s in T["sfx"]:
    for at in (s["at"] if isinstance(s["at"], list) else [s["at"]]):
        i = inp(os.path.join(build, "sfx", s["file"] + ".mp3"))
        ms = int(at * 1000)
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={s['gain']}dB,adelay={ms}|{ms}[x{i}]"); fx_labels.append(f"[x{i}]")
m = T["music"]
mi = inp(os.path.join(here, m["file"]), loop=True)
fade = dur - 2.5
filt.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},volume={m['gain']}dB,afade=t=in:d=0.6,afade=t=out:st={fade}:d=2.5[mus]")
filt.append(f"{''.join(vo_labels)}amix=inputs={len(vo_labels)}:normalize=0,asplit=2[vo][vokey]")
# sidechain: music ducks under VO
filt.append("[mus][vokey]sidechaincompress=threshold=0.02:ratio=12:attack=20:release=350:makeup=1[musd]")
filt.append(f"{''.join(fx_labels)}amix=inputs={len(fx_labels)}:normalize=0[fx]")
filt.append("[vo]highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,equalizer=f=3500:t=q:w=1:g=2[vop]")
filt.append(f"[vop][musd][fx]amix=inputs=3:normalize=0,atrim=0:{dur},loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000[out]")

mix = os.path.join(build, "mix.m4a")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-c:a", "aac", "-b:a", "256k", mix], check=True)
print("mix ->", mix)

out = os.path.join(proj, "out"); os.makedirs(out, exist_ok=True)
for fmt in ("916", "11"):
    v = os.path.join(build, f"video_{fmt}.mp4")
    if not os.path.exists(v): continue
    name = {"916": "final_9x16_reels.mp4", "11": "final_1x1_feed.mp4"}[fmt]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-i", mix, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy",
                    "-shortest", "-movflags", "+faststart", os.path.join(out, name)], check=True)
    print("final ->", os.path.join(out, name))
