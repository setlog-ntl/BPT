"""
씬별 이미지 자동 수집기

loremflickr.com에서 키워드 매칭 무료 사진 다운로드.
- API 키 불필요
- 1280x720 16:9 사이즈로 받음
- 다운로드 실패 시 재시도, 그래도 실패하면 PIL로 그라데이션 폴백 이미지 생성

CLI:
  python image_fetch.py            # 전부 다운로드 (없는 것만)
  python image_fetch.py --force    # 모두 다시 다운로드
"""
import os, sys, time, urllib.request, urllib.error, ssl, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(HERE, "images")
os.makedirs(IMG_DIR, exist_ok=True)

W, H = 1280, 720

# loremflickr endpoint: https://loremflickr.com/<w>/<h>/<keyword,keyword>?lock=<seed>
# lock=seed로 같은 키워드면 같은 이미지를 받게 해서 재현성 확보
def fetch_for_scene(scene_id, keywords, force=False):
    out = os.path.join(IMG_DIR, f"scene_{scene_id:02d}.jpg")
    if os.path.exists(out) and os.path.getsize(out) > 5000 and not force:
        return out, "cached"
    seed = int(hashlib.md5(f"{scene_id}_{keywords}".encode()).hexdigest()[:6], 16)
    url = f"https://loremflickr.com/{W}/{H}/{keywords}?lock={seed}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
            data = r.read()
        if len(data) < 5000:
            return None, "too small"
        with open(out, "wb") as f:
            f.write(data)
        return out, "ok"
    except Exception as e:
        return None, str(e)


def make_fallback(scene_id, out_path):
    """If download fails, generate a stylish gradient fallback."""
    from PIL import Image, ImageDraw, ImageFilter
    accent_palette = [
        (255, 209, 102),  # gold
        (6, 214, 160),    # green
        (239, 71, 111),   # red
        (17, 138, 178),   # info blue
    ]
    base_color = accent_palette[scene_id % len(accent_palette)]
    img = Image.new("RGB", (W, H), (15, 17, 21))
    draw = ImageDraw.Draw(img)
    for r in range(800, 100, -30):
        a = int(40 * (r / 800) ** 0.5)
        c = tuple(min(255, c + a) for c in (15, 17, 21))
        c = tuple(int(c0 * 0.85 + b * 0.15) for c0, b in zip(c, base_color))
        draw.ellipse((-200 - r//2, -200 - r//2, 600 + r//2, 600 + r//2), fill=c)
    img = img.filter(ImageFilter.GaussianBlur(60))
    img.save(out_path, "JPEG", quality=85)


def main():
    force = "--force" in sys.argv
    from scene_images import SCENE_KEYWORDS
    ok = 0
    fail = 0
    fallback = 0
    for scene_id, kw in sorted(SCENE_KEYWORDS.items()):
        path, status = fetch_for_scene(scene_id, kw, force=force)
        if path:
            print(f"  [{status:>6}] scene_{scene_id:02d}.jpg  ({kw})")
            ok += 1
        else:
            print(f"  [FAIL]  scene_{scene_id:02d}.jpg  ({status[:60]})")
            fail += 1
            fb = os.path.join(IMG_DIR, f"scene_{scene_id:02d}.jpg")
            make_fallback(scene_id, fb)
            fallback += 1
            print(f"  [fallback] generated for scene_{scene_id:02d}.jpg")
        time.sleep(0.3)  # gentle rate limit
    print(f"\n  Summary: ok={ok} fail={fail} fallback={fallback}")


if __name__ == "__main__":
    main()
