"""쇼츠 v10 슬라이드 — 1080x1920 + Pollinations AI 이미지 + 키네틱 타이포"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
IMG_DIR = os.path.join(HERE, "images_v10")
COLORS = {
    "bg": (15, 17, 21), "white": (255, 255, 255), "muted": (200, 207, 222),
    "gold": (255, 209, 102), "green": (6, 214, 160), "red": (239, 71, 111),
    "info": (90, 196, 224),
}


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def get_fonts():
    return {
        "huge": font("NanumGothicExtraBold.ttf", 160),
        "huge_sm": font("NanumGothicExtraBold.ttf", 120),
        "huge_xs": font("NanumGothicExtraBold.ttf", 90),
        "caption": font("NanumGothic.ttf", 56),
    }


def text_size(d, text, fnt):
    if not text: return 0, 0
    bb = d.textbbox((0, 0), text, font=fnt)
    return bb[2] - bb[0], bb[3] - bb[1]


def load_image(scene_id):
    p = os.path.join(IMG_DIR, f"scene_{scene_id:02d}.jpg")
    if os.path.exists(p) and os.path.getsize(p) > 5000:
        try:
            img = Image.open(p).convert("RGB")
            iw, ih = img.size
            scale = max(W/iw, H/ih)
            nw, nh = int(iw*scale), int(ih*scale)
            img = img.resize((nw, nh), Image.LANCZOS)
            return img.crop(((nw-W)//2, (nh-H)//2, (nw-W)//2 + W, (nh-H)//2 + H))
        except: return None
    return None


def cinematic(img, dim=0.55):
    """Higher dim (=less darkening) for AI images that are already polished"""
    img = ImageEnhance.Brightness(img).enhance(dim)
    img = ImageEnhance.Contrast(img).enhance(1.1)
    # Add slight bottom-fade gradient for text legibility (lower 40%)
    overlay = Image.new("RGB", (W, H), (0, 0, 0))
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    for y in range(int(H*0.5), H):
        a = int(180 * (y - H*0.5) / (H*0.5))
        md.line([(0, y), (W, y)], fill=a)
    img = Image.composite(overlay, img, mask)
    return img


def draw_shadow_text(d, pos, text, fnt, fill):
    x, y = pos
    for ox, oy in [(3, 3), (4, 4), (-1, 1)]:
        d.text((x+ox, y+oy), text, font=fnt, fill=(0, 0, 0))
    d.text((x, y), text, font=fnt, fill=fill)


def fit_font(d, text, base, alt, alt2, max_w=W - 80):
    if not text: return base
    if text_size(d, text, base)[0] <= max_w: return base
    if text_size(d, text, alt)[0] <= max_w: return alt
    return alt2


def render_scene(scene, out_path):
    accent = COLORS.get(scene.get("accent", "gold"), COLORS["gold"])
    img_bg = load_image(scene["id"])
    if img_bg:
        bg = cinematic(img_bg, dim=0.55)
    else:
        bg = Image.new("RGB", (W, H), COLORS["bg"])
    d = ImageDraw.Draw(bg)
    fonts = get_fonts()

    big1 = scene.get("big1", "")
    big2 = scene.get("big2", "")
    caption = scene.get("caption", "")

    f1 = fit_font(d, big1, fonts["huge"], fonts["huge_sm"], fonts["huge_xs"])
    f2 = fit_font(d, big2, fonts["huge"], fonts["huge_sm"], fonts["huge_xs"])
    h1 = text_size(d, big1, f1)[1] if big1 else 0
    h2 = text_size(d, big2, f2)[1] if big2 else 0
    gap = 30 if (big1 and big2) else 0
    block = h1 + gap + h2

    # Place text in bottom 40% area for shorts feel
    y0 = int(H * 0.55)

    if big1:
        w1 = text_size(d, big1, f1)[0]
        draw_shadow_text(d, ((W-w1)//2, y0), big1, f1, COLORS["white"])
    if big2:
        w2 = text_size(d, big2, f2)[0]
        draw_shadow_text(d, ((W-w2)//2, y0 + h1 + gap), big2, f2, accent)

    # underline
    if big1 or big2:
        ux = W//2 - 120
        uy = y0 + block + 60
        d.rectangle((ux, uy, ux+240, uy+12), fill=accent)

    if caption:
        cw, ch = text_size(d, caption, fonts["caption"])
        if cw > W - 120:
            mid = len(caption)//2
            split = caption.rfind(" ", 0, mid+8)
            if split <= 0: split = mid
            l1, l2 = caption[:split].strip(), caption[split:].strip()
            for i, line in enumerate([l1, l2]):
                lw, lh = text_size(d, line, fonts["caption"])
                draw_shadow_text(d, ((W-lw)//2, H - 280 + i*70), line,
                                  fonts["caption"], COLORS["muted"])
        else:
            draw_shadow_text(d, ((W-cw)//2, H - 250), caption,
                              fonts["caption"], COLORS["muted"])

    bg.save(out_path, "PNG", optimize=True)
    return out_path


def render_all(scenes, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for sc in scenes:
        render_scene(sc, os.path.join(out_dir, f"scene_{sc['id']:02d}.png"))


if __name__ == "__main__":
    from scenes_shorts_v10 import SCENES
    render_all(SCENES, os.path.join(HERE, "slides_v10"))
    print(f"Done. {len(SCENES)} slides")
