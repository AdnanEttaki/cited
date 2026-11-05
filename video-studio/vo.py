"""ElevenLabs line-by-line voiceover with character timestamps. Usage: python3 vo.py cues.json voice_id outdir"""
import json,base64,subprocess,sys,os
cues=json.load(open(sys.argv[1])); voice=sys.argv[2]; out=sys.argv[3]; os.makedirs(out,exist_ok=True)
for i,c in enumerate(cues):
    body={"text":c["text"],"model_id":"eleven_multilingual_v2",
          "voice_settings":{"stability":0.45,"similarity_boost":0.8,"style":0.35,"use_speaker_boost":True},
          "previous_text":cues[i-1]["text"] if i else None,"next_text":cues[i+1]["text"] if i+1<len(cues) else None}
    p=f"{out}/{c['id']}.json"; json.dump(body,open(p+'.req','w'))
    subprocess.run(["curl","-sS","-X","POST",f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
        "-H","xi-api-key: proxy-injected","-H","Content-Type: application/json","-d","@"+p+".req","-o",p],check=True)
    d=json.load(open(p)); assert "audio_base64" in d, d
    open(f"{out}/{c['id']}.mp3","wb").write(base64.b64decode(d.pop("audio_base64"))); json.dump(d,open(p,"w"))
    print(c["id"], round(d["alignment"]["character_end_times_seconds"][-1],2))
