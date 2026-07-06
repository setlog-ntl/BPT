"""
Pollinations.ai로 씬별 AI 이미지 생성 (무료, 키 불필요)
URL: https://image.pollinations.ai/prompt/{URL}?width=1080&height=1920&model=flux&seed={n}
"""
import os, sys, time, urllib.request, urllib.parse, ssl, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(HERE, "images_v10")
os.makedirs(IMG_DIR, exist_ok=True)
W, H = 1080, 1920


def fetch(scene_id, prompt):
    out = os.path.join(IMG_DIR, f"scene_{scene_id:02d}.jpg")
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        return out, "cached"
    seed = int(hashlib.md5(f"{scene_id}_{prompt}".encode()).hexdigest()[:6], 16)
    encoded = urllib.parse.quote(prompt[:300])
    url = (f"https://image.pollinations.ai/prompt/{encoded}"
           f"?width={W}&height={H}&seed={seed}&model=flux&nologo=true")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=90, context=ssl.create_default_context()) as r:
            data = r.read()
        if len(data) < 10000:
            return None, "too small"
        with open(out, "wb") as f:
            f.write(data)
        return out, "ok"
    except Exception as e:
        return None, str(e)


def make_fallback(scene_id, accent_idx, out):
    from PIL import Image, ImageDraw, ImageFilter
    palette = [(255, 209, 102), (6, 214, 160), (239, 71, 111), (90, 196, 224)]
    base = palette[accent_idx % 4]
    img = Image.new("RGB", (W, H), (15, 17, 21))
    d = ImageDraw.Draw(img)
    for r in range(800, 100, -30):
        a = int(40 * (r/800)**0.5)
        c = tuple(min(255, c + a) for c in (15, 17, 21))
        c = tuple(int(c0*0.85 + b*0.15) for c0, b in zip(c, base))
        d.ellipse((-200-r//2, -200-r//2, 800+r//2, 800+r//2), fill=c)
    img.filter(ImageFilter.GaussianBlur(60)).save(out, "JPEG", quality=85)


def main():
    from scenes_shorts_v10 import SCENES
    ok = fb = 0
    for i, sc in enumerate(SCENES):
        path, status = fetch(sc["id"], sc["prompt"])
        if path:
            print(f"  [{status:>6}] scene_{sc['id']:02d}.jpg ({sc['prompt'][:50]}...)")
            ok += 1
        else:
            print(f"  [FAIL] scene_{sc['id']:02d}: {status[:80]}")
            out = os.path.join(IMG_DIR, f"scene_{sc['id']:02d}.jpg")
            make_fallback(sc["id"], i, out)
            fb += 1
        time.sleep(0.5)
    print(f"\nSummary: ok={ok} fallback={fb}")


if __name__ == "__main__":
    main()
