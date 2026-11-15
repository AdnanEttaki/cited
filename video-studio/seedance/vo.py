"""Eleven v3 voice lines for the 'Comment SCRIPT' Reel. python3 vo.py -> ../build/vo/sr_*.mp3/json (+ _f tempo versions)"""
import base64, json, os, subprocess

here = os.path.dirname(os.path.abspath(__file__))
build = os.path.join(here, "..", "build", "vo")
VOICES = {"narrator": "JBFqnCBsd6RMkjVDRZzb", "ben": "iP95p4xoKVk53GoZ742B"}  # George, Chris
TEMPO = {"narrator": 1.22, "ben": 1.1}
LINES = [
    ("s1", "narrator", "[serious] Coaches. If this happens in your DMs every week…"),
    ("s2", "narrator", "A lead asks the price at eleven forty-one. Eleven minutes later… they're gone."),
    ("s3a", "ben", "[groans] Sorry, just saw this…"),
    ("s3b", "narrator", "You didn't lose them to price. You lost them to time."),
    ("s4", "narrator", "With DMSetter, that same DM gets answered in seconds, qualified, and booked… [whispers] while you sleep."),
    ("s5", "narrator", "Here are seven replies that turn 'how much?' into a booked call."),
    ("s6", "narrator", "Comment SCRIPT, and I'll send them to you."),
    ("s7", "narrator", "DMSetter. More booked calls. Zero DMs at two A.M."),
]

if __name__ == "__main__":
    os.makedirs(build, exist_ok=True)
    for key, spk, text in LINES:
        p = os.path.join(build, f"sr_{key}")
        if not os.path.exists(p + ".json"):
            json.dump({"text": text, "model_id": "eleven_v3", "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}}, open(p + ".req", "w"))
            subprocess.run(["curl", "-sS", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[spk]}/with-timestamps?output_format=mp3_44100_128",
                            "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json", "-d", "@" + p + ".req", "-o", p + ".json"], check=True)
            d = json.load(open(p + ".json")); assert "audio_base64" in d, d
            open(p + ".mp3", "wb").write(base64.b64decode(d.pop("audio_base64"))); json.dump(d, open(p + ".json", "w"))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p + ".mp3", "-filter:a", f"atempo={TEMPO[spk]}", p + "_f.mp3"], check=True)
        d = json.load(open(p + ".json"))
        print(key, spk, round(d["alignment"]["character_end_times_seconds"][-1] / TEMPO[spk], 2))
