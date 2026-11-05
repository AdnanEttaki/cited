"""ElevenLabs sound effects. Usage: python3 sfx.py outdir"""
import json,subprocess,sys
out=sys.argv[1]
fx={"whoosh":("fast clean cinematic whoosh transition, airy, premium",1.2),
    "pop":("soft subtle iphone message received pop, clean, short",0.6),
    "boom":("deep luxury cinematic sub bass boom impact with long tail, trailer hit",3.0),
    "riser":("smooth cinematic tension riser building up, airy shimmer",3.0),
    "ding":("elegant crystal bell chime, success notification, luxury",1.5),
    "click":("crisp mechanical keyboard click, single, clean",0.5)}
for k,(t,d) in fx.items():
    subprocess.run(["curl","-sS","-X","POST","https://api.elevenlabs.io/v1/sound-generation","-H","xi-api-key: proxy-injected",
      "-H","Content-Type: application/json","-d",json.dumps({"text":t,"duration_seconds":d,"prompt_influence":0.6}),"-o",f"{out}/{k}.mp3"],check=True)
    print(k, subprocess.run(["file","-b",f"{out}/{k}.mp3"],capture_output=True,text=True).stdout.strip()[:40])
