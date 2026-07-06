"""
쇼츠 슬라이드 렌더러 — 9:16 1080x1920 키네틱 타이포

- 풀블리드 사진 배경 + 어두운 오버레이
- 큰 텍스트 (Shorts 스타일, 모바일 가독)
- 강한 강조색
- 자막 영역 하단 (별도 자막은 ffmpeg burn-in)
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1920  # 9:16 vertical
FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
IMG_DIR  = os.path.join(os.path.dirname(__file__), "images")

COLORS = {
    "bg":    (15, 17, 21),
    "white": (255, 255, 255),
    "muted": (200, 207, 222),
    "gold":  (255, 209, 102),
    "green": (6, 214, 160),
    "red":   (239, 71, 111),
    "info":  (90, 196, 224),
}


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def get_fonts():
    return {
        "small":   font("NanumGothicBold.ttf", 48),
        "huge":    font("NanumGothicExtraBold.ttf", 180),
        "huge_sm": font("NanumGothicExtraBold.ttf", 130),
        "huge_xs": font("NanumGothicExtraBold.ttf", 95),
        "caption": font("NanumGothic.ttf", 56),
    }


def text_size(draw, text, fnt):
    if not text: return 0, 0
    bb = draw.textbbox((0, 0), text, font=fnt)
    return bb[2] - bb[0], bb[3] - bb[1]


def load_scene_image(scene_id):
    p = os.path.join(IMG_DIR, f"scene_{scene_id:02d}.jpg")
    if os.path.exists(p) and os.path.getsize(p) > 5000:
        try:
            img = Image.open(p).convert("RGB")
            iw, ih = img.size
            sw, sh = W / iw, H / ih
            scale = max(sw, sh)
            nw, nh = int(iw * scale), int(ih * scale)
            img = img.resize((nw, nh), Image.LANCZOS)
            x0 = (nw - W) // 2
            y0 = (nh - H) // 2
            return img.crop((x0, y0, x0 + W, y0 + H))
        except Exception as e:
            print(f"  load fail scene_{scene_id:02d}: {e}")
    return None


def cinematic_treat(img, dim=0.4):
    """Movie-feel: lower brightness + slight gradient overlay for text legibility"""
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(dim)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.05)
    return img


def gradient_bg(accent_color):
    img = Image.new("RGB", (W, H), COLORS["bg"])
    glow = Image.new("RGB", (W, H), COLORS["bg"])
    gd = ImageDraw.Draw(glow)
    for r in range(900, 100, -30):
        a = int(40 * (r / 900) ** 0.5)
        c = tuple(min(255, c + a) for c in COLORS["bg"])
        c = tuple(int(c0 * 0.85 + b * 0.15) for c0, b in zip(c, accent_color))
        gd.ellipse((-200 - r//2, -200 - r//2, 800 + r//2, 800 + r//2), fill=c)
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    return Image.blend(img, glow, 0.6)


def draw_text_with_shadow(draw, pos, text, fnt, fill):
    x, y = pos
    for ox, oy in [(3, 3), (4, 4), (-1, 1)]:
        draw.text((x + ox, y + oy), text, font=fnt, fill=(0, 0, 0))
    draw.text((x, y), text, font=fnt, fill=fill)


def fit_font(draw, text, base_font, alt_font, alt2_font, max_w=W - 80):
    if not text: return base_font
    if text_size(draw, text, base_font)[0] <= max_w: return base_font
    if text_size(draw, text, alt_font)[0] <= max_w: return alt_font
    return alt2_font


def render_scene(scene, out_path):
    accent = COLORS.get(scene.get("accent", "gold"), COLORS["gold"])

    img_bg = load_scene_image(scene["id"])
    if img_bg is not None:
        bg = cinematic_treat(img_bg, dim=0.35)
    else:
        bg = gradient_bg(accent)
    draw = ImageDraw.Draw(bg)
    fonts = get_fonts()

    big1 = scene.get("big1", "")
    big2 = scene.get("big2", "")
    caption = scene.get("caption", "")

    # Choose font sizes that fit
    f1 = fit_font(draw, big1, fonts["huge"], fonts["huge_sm"], fonts["huge_xs"])
    f2 = fit_font(draw, big2, fonts["huge"], fonts["huge_sm"], fonts["huge_xs"])

    h1 = text_size(draw, big1, f1)[1] if big1 else 0
    h2 = text_size(draw, big2, f2)[1] if big2 else 0
    gap = 30 if (big1 and big2) else 0
    block_h = h1 + gap + h2

    # Center vertically (slightly above middle for visual balance)
    y0 = (H - block_h) // 2 - 100

    if big1:
        w1 = text_size(draw, big1, f1)[0]
        draw_text_with_shadow(draw, ((W - w1) // 2, y0), big1, f1, COLORS["white"])
    if big2:
        w2 = text_size(draw, big2, f2)[0]
        draw_text_with_shadow(draw, ((W - w2) // 2, y0 + h1 + gap),
                                big2, f2, accent)

    # Accent underline
    if big1 or big2:
        ux = W // 2 - 120
        uy = y0 + block_h + 60
        draw.rectangle((ux, uy, ux + 240, uy + 12), fill=accent)

    # Caption (subtle, below)
    if caption:
        cw, ch = text_size(draw, caption, fonts["caption"])
        if cw > W - 120:
            # split
            mid = len(caption) // 2
            split = caption.rfind(" ", 0, mid + 8)
            if split <= 0: split = mid
            l1, l2 = caption[:split].strip(), caption[split:].strip()
            for i, line in enumerate([l1, l2]):
                lw, lh = text_size(draw, line, fonts["caption"])
                draw_text_with_shadow(draw, ((W - lw) // 2, H - 380 + i * 70),
                                       line, fonts["caption"], COLORS["muted"])
        else:
            draw_text_with_shadow(draw, ((W - cw) // 2, H - 350),
                                   caption, fonts["caption"], COLORS["muted"])

    bg.save(out_path, "PNG", optimize=True)
    return out_path


def render_all(scenes, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for sc in scenes:
        p = os.path.join(out_dir, f"scene_{sc['id']:02d}.png")
        render_scene(sc, p)
        paths.append(p)
    return paths


if __name__ == "__main__":
    from scenes_shorts import SCENES
    here = os.path.dirname(__file__)
    paths = render_all(SCENES, os.path.join(here, "slides"))
    print(f"Done. {len(paths)} slides 1080x1920")
