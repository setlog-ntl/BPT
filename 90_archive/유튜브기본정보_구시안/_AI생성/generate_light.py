# -*- coding: utf-8 -*-
"""
OpenAI 이미지 생성 — 밝은(라이트) 버전 · 채널 "그럼에도 한 페이지"
- 다크 대신 따뜻한 크림/아이보리 배경 + 자연광 + 골드 액센트. 채널 정체성(책·한 페이지·진정성) 유지.
- 키는 루트 .env(OPENAI_API_KEY)에서 로드. 텍스트는 생성하지 않음(후처리 오버레이).
사용법:  python generate_light.py
"""
import os, sys, json, base64, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

def load_env(path):
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

load_env(os.path.join(ROOT, ".env"))
KEY = os.environ.get("OPENAI_API_KEY", "").strip()
if not KEY:
    sys.exit("[ERROR] OPENAI_API_KEY not found in .env")

LIGHT = ("bright warm natural daylight, soft airy luminous atmosphere, cream ivory and warm beige "
         "tones, gentle soft shadows, warm golden accent (#FFD166), light clean and inviting, "
         "minimalist premium editorial, literary calm and sincere mood, subtle paper texture, "
         "faceless, no people, high-end book brand aesthetic, no text, no letters, no watermark")

JOBS = [
    ("01_로고_밝은_AI.png", "1024x1024", "1024x1024",
     "A single open book resting on a clean cream-colored surface, soft warm natural light from "
     "above creating a gentle glow on the pages, centered minimalist logo composition with lots of "
     "bright airy negative space around it, warm and welcoming. " + LIGHT),
    ("02_배너_밝은_AI.png", "1536x1024", "1792x1024",
     "A bright airy reading corner by a large window with soft morning daylight pouring in, a single "
     "open book on a light wooden desk with a small plant, cream and warm beige palette, wide cinematic "
     "but luminous composition, vast empty bright negative space on the right side for a title. " + LIGHT),
]

def call(model, prompt, size):
    body = {"model": model, "prompt": prompt, "size": size, "n": 1}
    if model == "gpt-image-1":
        body["quality"] = "high"
    else:
        body["quality"] = "hd"
        body["response_format"] = "b64_json"
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)

ok = 0
for fname, sz_gpt, sz_dalle, prompt in JOBS:
    saved = False
    for model, size in (("gpt-image-1", sz_gpt), ("dall-e-3", sz_dalle)):
        try:
            print("[..] %s via %s (%s)" % (fname, model, size), flush=True)
            res = call(model, prompt, size)
            b64 = res["data"][0]["b64_json"]
            with open(os.path.join(HERE, fname), "wb") as f:
                f.write(base64.b64decode(b64))
            print("[OK] saved %s (%s)" % (fname, model), flush=True)
            saved = True; ok += 1; break
        except urllib.error.HTTPError as e:
            print("[ERR] %s %s -> HTTP %s: %s" % (fname, model, e.code,
                  e.read().decode("utf-8", "ignore")[:400]), flush=True)
        except Exception as e:
            print("[ERR] %s %s -> %s" % (fname, model, str(e)[:300]), flush=True)
    if not saved:
        print("[FAIL] %s" % fname, flush=True)

print("\nDONE: %d/%d images generated." % (ok, len(JOBS)))
