"""Eleven v3 VO for The Race. python3 vo.py -> build/vo/rc_*.mp3 (+_f) and vo_fit.json"""
import base64, json, os, subprocess
here = os.path.dirname(os.path.abspath(__file__))
build = os.path.join(here, "..", "..", "build", "vo"); os.makedirs(build, exist_ok=True)
V = {"nar": "JBFqnCBsd6RMkjVDRZzb", "ben": "iP95p4xoKVk53GoZ742B"}
G = [  # key, voice, start, window_end, text
 ("g1", "nar", 0.1, 4.0, "A lead messaged five coaches at eleven PM. Only one got the call."),
 ("g2", "nar", 4.1, 9.0, "Same message. Same minute. Five different coaches."),
 ("g3", "nar", 9.1, 16.0, "Four were asleep, or busy. One replied in thirty-eight seconds."),
 ("g4", "nar", 16.1, 22.0, "She didn't pick the best coach. She picked the first one who answered."),
 ("g5", "nar", 22.2, 27.0, "By morning, the call was booked."),
 ("g6a", "ben", 27.2, 29.0, "[groans] Sorry, just saw this…"),
 ("g6b", "nar", 29.0, 31.0, "The other four replied in the morning. Too late."),
 ("g7", "nar", 31.1, 35.0, "Comment SPEED, and I'll send you the replies that win the race."),
]
fit = {}
for key, v, a, b, text in G:
    p = os.path.join(build, "rc_" + key)
    if not os.path.exists(p + ".json"):
        json.dump({"text": text, "model_id": "eleven_v3", "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}}, open(p + ".req", "w"))
        subprocess.run(["curl", "-sS", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{V[v]}/with-timestamps?output_format=mp3_44100_128",
                        "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json", "-d", "@" + p + ".req", "-o", p + ".json"], check=True)
        d = json.load(open(p + ".json")); assert "audio_base64" in d, d
        open(p + ".mp3", "wb").write(base64.b64decode(d.pop("audio_base64"))); json.dump(d, open(p + ".json", "w"))
    raw = json.load(open(p + ".json"))["alignment"]["character_end_times_seconds"][-1]
    tempo = round(min(1.6, max(1.0, raw / (b - a - 0.15))), 3)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p + ".mp3", "-filter:a", f"atempo={tempo}", p + "_f.mp3"], check=True)
    fit[key] = dict(at=a, tempo=tempo, raw=round(raw, 2), fitted=round(raw / tempo, 2), window=round(b - a, 2))
    print(key, fit[key])
json.dump(fit, open(os.path.join(here, "vo_fit.json"), "w"), indent=1)
