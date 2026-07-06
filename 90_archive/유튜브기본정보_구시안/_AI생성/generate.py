# -*- coding: utf-8 -*-
"""
OpenAI 이미지 생성 스크립트 — 채널 "그럼에도 한 페이지"
- API 키는 코드에 하드코딩하지 않고 프로젝트 루트 .env(OPENAI_API_KEY)에서 읽는다.
- gpt-image-1 우선, 실패 시 dall-e-3 폴백.
- 한글 텍스트는 생성하지 않음(AI가 깨뜨림) → 배경/비주얼만. 텍스트는 Canva/Figma 오버레이.
사용법:  python generate.py
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

# 프롬프트는 ../이미지프롬프트_*.md 의 원문 그대로 사용 (Midjourney 파라미터 --ar/--style/--v 만 제외)
JOBS = [
    # 프로필 A안 (이미지프롬프트_01_프로필사진.md)
    ("01_프로필_AI.png", "1024x1024", "1024x1024",
     "A single open book seen from above, one page softly glowing with warm golden light (#FFD166), "
     "deep black background (#0F1115), minimalist icon, centered composition, lots of negative space, "
     "subtle paper texture, soft rim light, cinematic low-key, premium literary logo, "
     "flat-ish vector-photographic hybrid, no text, no letters"),
    # 배너 A안 (이미지프롬프트_02_배너.md)
    ("02_배너_AI.png", "1536x1024", "1792x1024",
     "Wide cinematic banner of a quiet dark study at night, a single open book on a wooden desk lit by "
     "one warm golden light (#FFD166), deep black surroundings (#0F1115), vast negative space on the "
     "right side for text, atmospheric, shallow depth of field, premium literary mood, subtle paper and "
     "wood texture, faceless, no people, moody editorial photography, no text"),
    # 썸네일 ① 선택형 (이미지프롬프트_03_썸네일.md)
    ("03_썸네일_AI.png", "1536x1024", "1792x1024",
     "Left-side cinematic close-up of a single open book glowing with warm golden light (#FFD166) in "
     "deep darkness (#0F1115), faceless, atmospheric night-reading mood, subtle paper texture, shallow "
     "depth of field, keep the right 40% as dark empty negative space for text, premium editorial "
     "thumbnail, no text"),
]

def call(model, prompt, size):
    body = {"model": model, "prompt": prompt, "size": size, "n": 1}
    if model == "gpt-image-1":
        body["quality"] = "high"          # gpt-image-1: always returns b64_json
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
            out = os.path.join(HERE, fname)
            with open(out, "wb") as f:
                f.write(base64.b64decode(b64))
            print("[OK] saved %s (%s)" % (fname, model), flush=True)
            saved = True
            ok += 1
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "ignore")[:400]
            print("[ERR] %s %s -> HTTP %s: %s" % (fname, model, e.code, msg), flush=True)
        except Exception as e:
            print("[ERR] %s %s -> %s" % (fname, model, str(e)[:300]), flush=True)
    if not saved:
        print("[FAIL] %s — both models failed" % fname, flush=True)

print("\nDONE: %d/%d images generated." % (ok, len(JOBS)))
