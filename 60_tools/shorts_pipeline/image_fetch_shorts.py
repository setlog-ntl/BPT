"""쇼츠 씬별 이미지 수집 — loremflickr"""
import os, sys, time, urllib.request, ssl, hashlib
from scenes_shorts import SCENES

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(HERE, "images")
os.makedirs(IMG_DIR, exist_ok=True)
W, H = 1080, 1920

def fetch(scene_id, keywords):
    out = os.path.join(IMG_DIR, f"scene_{scene_id:02d}.jpg")
    if os.path.exists(out) and os.path.getsize(out) > 5000:
        return out, "cached"
    seed = int(hashlib.md5(f"{scene_id}_{keywords}".encode()).hexdigest()[:6], 16)
    url = f"https://loremflickr.com/{W}/{H}/{keywords}?lock={seed}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=25, context=ssl.create_default_context()) as r:
            data = r.read()
        if len(data) < 5000:
            return None, "too small"
        with open(out, "wb") as f:
            f.write(data)
        return out, "ok"
    except Exception as e:
        return None, str(e)


def make_fallback(scene_id, out_path, accent_idx=0):
    from PIL import Image, ImageDraw, ImageFilter
    palette = [
        (255, 209, 102), (6, 214, 160), (239, 71, 111), (90, 196, 224)
    ]
    base = palette[accent_idx % len(palette)]
    img = Image.new("RGB", (W, H), (15, 17, 21))
    d = ImageDraw.Draw(img)
    for r in range(800, 100, -30):
        a = int(40 * (r / 800) ** 0.5)
        c = tuple(min(255, c + a) for c in (15, 17, 21))
        c = tuple(int(c0 * 0.85 + b * 0.15) for c0, b in zip(c, base))
        d.ellipse((-200 - r//2, -200 - r//2, 800 + r//2, 800 + r//2), fill=c)
    img = img.filter(ImageFilter.GaussianBlur(60))
    img.save(out_path, "JPEG", quality=85)


def main():
    ok = 0; fb = 0
    for i, sc in enumerate(SCENES):
        kw = sc.get("keyword", "abstract")
        path, status = fetch(sc["id"], kw)
        if path:
            print(f"  [{status:>6}] scene_{sc['id']:02d}.jpg  ({kw})")
            ok += 1
        else:
            print(f"  [FAIL]  scene_{sc['id']:02d}: {status[:60]}")
            out = os.path.join(IMG_DIR, f"scene_{sc['id']:02d}.jpg")
            make_fallback(sc["id"], out, i)
            fb += 1
        time.sleep(0.3)
    print(f"\nSummary: ok={ok} fallback={fb}")


if __name__ == "__main__":
    main()
