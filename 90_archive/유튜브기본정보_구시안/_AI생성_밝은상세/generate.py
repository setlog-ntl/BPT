# -*- coding: utf-8 -*-
"""
OpenAI 이미지 생성 — 밝은 디테일 버전 · 채널 "그럼에도 한 페이지"
- 프롬프트는 같은 폴더 프롬프트_01~03_*.md 의 '최종 프롬프트'와 동일.
- 키는 루트 .env(OPENAI_API_KEY)에서 로드. 한글 텍스트는 생성하지 않음(후처리 오버레이).
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

LOGO = ("A minimalist premium brand logo image of a single open hardcover book resting on a clean "
        "ivory surface, viewed from a gentle three-quarter top-down angle. Soft warm morning sunlight "
        "streams from the upper-left, casting delicate soft shadows, and the open pages catch a subtle "
        "warm golden glow (#FFD166). Creamy off-white and warm beige palette (#F5EFE2). Lots of bright "
        "airy negative space evenly around the book so it reads as a centered icon. Fine paper grain, "
        "crisp clean page edges, gentle page curve. Calm, sincere, literary mood. Premium editorial "
        "product photography, soft diffused studio daylight, shallow depth of field, 50mm lens look, "
        "perfectly centered composition. Faceless, no people, no text, no letters, no watermark. "
        "High detail, photorealistic.")

BANNER = ("A bright airy editorial banner photograph of a cozy reading nook beside a large bright "
          "window with soft morning sunlight pouring in. On the LEFT third: a light oak wooden desk "
          "with a single open book, a warm cup of coffee, a small green potted plant, and a pair of "
          "reading glasses arranged neatly and calmly. Sheer white curtains gently glowing with "
          "backlight. Creamy ivory and warm beige tones (#F5EFE2) with a warm golden light accent "
          "(#FFD166). The entire RIGHT 45% of the frame is bright, softly lit empty wall space "
          "intentionally reserved for a title — clean and uncluttered. Wide cinematic yet luminous "
          "composition, soft natural diffused daylight, gentle realistic shadows, fine paper and wood "
          "texture. Calm, sincere, literary atmosphere. Premium magazine editorial photography, 35mm "
          "lens, balanced exposure. Faceless, no people, no text, no letters, no watermark. "
          "High detail, photorealistic.")

THUMB = ("A bright clean YouTube thumbnail background photograph. On the LEFT 60%: a close-up of an "
         "open book on a light wooden table bathed in soft warm morning sunlight, a few pages gently "
         "lifting in the air, with a warm cup of coffee and a small plant softly blurred in the "
         "background. Creamy ivory and warm beige palette (#F5EFE2) with a warm golden glow (#FFD166) "
         "on the page edges. The RIGHT 40% is a soft, bright, slightly out-of-focus area kept mostly "
         "empty and uncluttered, ready for bold title text overlay. Shallow depth of field with creamy "
         "natural bokeh, calm and inviting morning-reading mood, fresh and hopeful. Premium editorial "
         "photography, natural diffused daylight, 50mm lens, high clarity on the book. Faceless, no "
         "people, no text, no letters, no watermark. High detail, photorealistic.")

JOBS = [
    ("01_로고_밝은.png", "1024x1024", "1024x1024", LOGO),
    ("02_배너_밝은.png", "1536x1024", "1792x1024", BANNER),
    ("03_썸네일_밝은.png", "1536x1024", "1792x1024", THUMB),
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
