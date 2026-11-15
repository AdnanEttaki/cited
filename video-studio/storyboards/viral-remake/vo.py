"""Eleven v3 voice-over for the viral-remake Reel: 9 groups, each fitted (atempo) to its shot window.
python3 vo.py -> ../../build/vo/vr_g*.mp3/json (+ _f tempo-fitted) and vo_fit.json"""
import base64, json, os, subprocess
here = os.path.dirname(os.path.abspath(__file__))
build = os.path.join(here, "..", "..", "build", "vo"); os.makedirs(build, exist_ok=True)
VOICE = "JBFqnCBsd6RMkjVDRZzb"  # George
# (key, window_start, window_end, text)
G = [
 ("g1", 0.0, 8.0, "DMSetter just killed unanswered DMs. Now, you can automate your entire inbox, and it's completely handled."),
 ("g2", 8.0, 18.9, "Here's how it works. It's called the DMSetter system, and it's not one reply. It's thirteen, built for coaches, that run your whole inbox."),
 ("g3", 18.9, 25.0, "The first one answers every new lead in seconds. And it qualifies them."),
 ("g4", 25.0, 30.9, "Another one follows up when they go quiet. One handles objections, without sounding pushy."),
 ("g5", 30.9, 38.9, "One scores every lead. One books your week. It knows what to say, when, and to who."),
 ("g6", 38.9, 47.6, "So you never have to type. But then, there's the full set. Thirteen replies, running through every inbox."),
 ("g7", 47.6, 57.7, "It ranks your leads by how ready they are, names the reply that works best, then sends it for you."),
 ("g8", 57.7, 67.4, "No more staying up for DMs. And the setup is easy. Connect Instagram, pick your replies, done."),
 ("g9", 67.4, 71.6, "If you want the full set, comment SCRIPT, and I'll send it to you."),
]
fit = {}
for key, a, b, text in G:
    p = os.path.join(build, "vr_" + key)
    if not os.path.exists(p + ".json"):
        json.dump({"text": text, "model_id": "eleven_v3", "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}}, open(p + ".req", "w"))
        subprocess.run(["curl", "-sS", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
                        "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json", "-d", "@" + p + ".req", "-o", p + ".json"], check=True)
        d = json.load(open(p + ".json")); assert "audio_base64" in d, d
        open(p + ".mp3", "wb").write(base64.b64decode(d.pop("audio_base64"))); json.dump(d, open(p + ".json", "w"))
    raw = json.load(open(p + ".json"))["alignment"]["character_end_times_seconds"][-1]
    tempo = round(min(1.6, max(1.0, raw / (b - a - 0.3))), 3)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p + ".mp3", "-filter:a", f"atempo={tempo}", p + "_f.mp3"], check=True)
    fit[key] = dict(at=a + 0.1, tempo=tempo, raw=round(raw, 2), fitted=round(raw / tempo, 2), window=round(b - a, 2))
    print(key, fit[key])
json.dump(fit, open(os.path.join(here, "vo_fit.json"), "w"), indent=1)
