"""Track the orange ball in a pendulum plate and fit the pendulum circle (pivot, radius).
python3 track.py <video.mp4> <out.json>   -> per-frame ball (x,y) in plate pixels + pivot + cable x at text row"""
import json, subprocess, sys, os, glob
import numpy as np
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
fd = os.path.join(os.path.dirname(os.path.abspath(out)), "frames_" + os.path.splitext(os.path.basename(src))[0])
os.makedirs(fd, exist_ok=True)
for f in glob.glob(fd + "/*.png"): os.remove(f)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vsync", "0", os.path.join(fd, "f%04d.png")], check=True)
fps = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.split("/")[0].replace("\n", "") or 24)
fr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip().split("/")
fps = float(fr[0]) / float(fr[1]) if len(fr) == 2 else float(fr[0])
P = []
files = sorted(glob.glob(fd + "/*.png"))
for i, f in enumerate(files):
    a = np.asarray(Image.open(f).convert("RGB")).astype(np.int32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (r > 170) & (g < 130) & (b < 90) & (r - g > 90)
    ys, xs = np.nonzero(m)
    if len(xs) < 30: P.append(None); continue
    P.append([float(xs.mean()), float(ys.mean()), float(np.sqrt(len(xs) / np.pi))])
H, W = a.shape[:2]
ok = [(i, p) for i, p in enumerate(P) if p]
X = np.array([p[0] for _, p in ok]); Y = np.array([p[1] for _, p in ok])
A = np.c_[2 * X, 2 * Y, np.ones(len(X))]; Bv = X ** 2 + Y ** 2
cx0, cy0, c = np.linalg.lstsq(A, Bv, rcond=None)[0]; R = float(np.sqrt(c + cx0 ** 2 + cy0 ** 2))
json.dump({"fps": fps, "w": W, "h": H, "n": len(files), "pivot": [float(cx0), float(cy0)], "radius": R, "ball": P}, open(out, "w"))
print(f"{len(files)} frames @ {fps:.2f}fps, {W}x{H}; tracked {len(ok)}; pivot=({cx0:.1f},{cy0:.1f}) R={R:.1f}; x range {X.min():.0f}-{X.max():.0f}; y range {Y.min():.0f}-{Y.max():.0f}")
