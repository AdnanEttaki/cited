"""Start frames for Seedance (1080x1920, our paper style, no text).
python3 startframes.py -> start/*.html ; node shoot_start.mjs -> start/*.png"""
import os, sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "characters"))
import characters as C  # noqa: E402

LOGO = open(os.path.join(here, "..", "brand", "logo", "svg", "mark_primary.svg")).read()
INK, ORANGE, CREAM, TEAL, AMBER = "#1B1B1B", "#D8541E", "#F4F0E8", "#1E9E95", "#F2A33A"


def page(body, night):
    bg = ("radial-gradient(120% 90% at 50% 35%,#2B3646 0%,#1E2632 60%,#151B24 100%)" if night
          else "radial-gradient(120% 90% at 50% 35%,#F7F2E9 0%,#ECE6DA 70%,#E2DBCD 100%)")
    grid = "rgba(255,255,255,.04)" if night else "rgba(0,0,0,.035)"
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden}}
#s{{width:540px;height:960px;zoom:2;position:relative;overflow:hidden;background:{bg}}}
#s::before{{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,{grid} 0 1px,transparent 1px 36px),repeating-linear-gradient(90deg,{grid} 0 1px,transparent 1px 36px)}}
.p{{position:absolute;box-shadow:0 6px 0 rgba(0,0,0,.18),0 18px 30px rgba(0,0,0,.18)}}
</style></head><body><div id="s">{body}</div></body></html>'''


def window(night, x=40, y=150):
    if night:
        inner = (f'<div style="position:absolute;inset:10px;background:#0F1A2B;border-radius:6px"></div>'
                 f'<div style="position:absolute;left:96px;top:30px;width:34px;height:34px;border-radius:50%;box-shadow:-9px 4px 0 0 {AMBER}"></div>'
                 + "".join(f'<i style="position:absolute;left:{a}px;top:{b}px;width:4px;height:4px;border-radius:50%;background:{CREAM}"></i>' for a, b in [(30, 40), (60, 90), (120, 100), (40, 120)]))
    else:
        inner = (f'<div style="position:absolute;inset:10px;background:#BFE3F0;border-radius:6px"></div>'
                 f'<div style="position:absolute;left:60px;top:40px;width:50px;height:50px;border-radius:50%;background:{AMBER};box-shadow:0 0 40px {AMBER}"></div>')
    return (f'<div class="p" style="left:{x}px;top:{y}px;width:170px;height:150px;background:{CREAM};border-radius:10px">{inner}'
            f'<div style="position:absolute;left:83px;top:10px;width:4px;height:130px;background:{CREAM}"></div></div>')


def bed(char_svg, cx=230, top=330, w=360):
    return (f'<div class="p" style="left:{cx - w // 2 - 20}px;top:{top - 30}px;width:{w + 40}px;height:300px;background:#9C5B32;border-radius:24px 24px 0 0"></div>'
            f'<div class="p" style="left:{cx - 130}px;top:{top}px;width:260px;height:110px;background:{CREAM};border-radius:40px"></div>'
            f'<div style="position:absolute;left:{cx - 150}px;top:{top - 30}px;z-index:2">{char_svg}</div>'
            f'<div class="p" style="left:{cx - w // 2 - 30}px;top:{top + 200}px;width:{w + 60}px;height:260px;background:{ORANGE};border-radius:30px 30px 0 0;z-index:3">'
            f'<div style="position:absolute;left:0;right:0;top:30px;height:6px;background:rgba(0,0,0,.12)"></div></div>')


def nightstand(phone_glow, x=420, y=560):
    return (f'<div class="p" style="left:{x}px;top:{y}px;width:110px;height:170px;background:#7A4A2A;border-radius:10px;z-index:4">'
            f'<div style="position:absolute;left:40px;top:70px;width:30px;height:8px;border-radius:4px;background:#5A351E"></div></div>'
            f'<div style="position:absolute;left:{x + 22}px;top:{y - 18}px;width:66px;height:22px;border-radius:6px;background:#111;z-index:5;'
            f'transform:perspective(200px) rotateX(55deg);box-shadow:0 0 30px 8px {phone_glow},inset 0 0 0 3px #111;"><div style="position:absolute;inset:3px;border-radius:4px;background:{phone_glow}"></div></div>')


SCENES = {
    "s1_night_buzz": (True, window(True) + bed(C.char_svg("low", "asleep", 300)) + nightstand("#3797F0")),
    "s3_morning_shock": (False, window(False) + bed(C.char_svg("low", "panic", 300))
                         + f'<div class="p" style="left:205px;top:560px;width:54px;height:92px;border-radius:10px;background:#111;z-index:4;transform:rotate(-6deg)">'
                           f'<div style="position:absolute;inset:5px;border-radius:6px;background:#3797F0;box-shadow:0 0 24px #3797F0"></div></div>'
                         + f'<div style="position:absolute;left:190px;top:625px;width:34px;height:26px;border-radius:13px;background:#E7B48E;z-index:5"></div>'
                           f'<div style="position:absolute;left:242px;top:620px;width:34px;height:26px;border-radius:13px;background:#E7B48E;z-index:5"></div>'),
    "s4_cloud_setter": (True, window(True) + bed(C.char_svg("low", "asleep", 300)) + nightstand(ORANGE)
                        + f'<div style="position:absolute;left:380px;top:300px;z-index:6;filter:drop-shadow(0 0 30px rgba(216,84,30,.6))">{LOGO.replace('width="260" height="260"', 'width="150" height="150"')}</div>'),
}

if __name__ == "__main__":
    out = os.path.join(here, "start"); os.makedirs(out, exist_ok=True)
    for k, (night, body) in SCENES.items():
        open(os.path.join(out, k + ".html"), "w").write(page(body, night))
    print("ok", len(SCENES))
