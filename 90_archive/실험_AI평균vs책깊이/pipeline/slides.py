"""
PIL 기반 슬라이드 렌더러 — 키네틱 타이포 정적 프레임 생성
'AI는 평균을 주고, 책은 깊이를 준다' 영상의 디자인 토큰 적용
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080  # 풀HD 16:9
FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")

COLORS = {
    "bg":      (15, 17, 21),
    "panel":   (23, 26, 33),
    "line":    (38, 43, 54),
    "text":    (231, 233, 238),
    "muted":   (154, 163, 178),
    "gold":    (255, 209, 102),
    "green":   (6, 214, 160),
    "red":     (239, 71, 111),
    "info":    (17, 138, 178),
    "white":   (255, 255, 255),
}

PART_COLORS = {
    "HOOK":   COLORS["red"],
    "INTRO":  COLORS["gold"],
    "BODY1":  COLORS["gold"],
    "BODY2":  COLORS["info"],
    "BODY3":  COLORS["info"],
    "BODY4":  COLORS["info"],
    "BODY5":  COLORS["info"],
    "실전":   COLORS["green"],
    "CTA":    COLORS["green"],
    "전환":   COLORS["muted"],
}


def load_font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def get_fonts():
    return {
        "label":  load_font("NanumGothicBold.ttf", 32),
        "big":    load_font("NanumGothicExtraBold.ttf", 132),
        "big_sm": load_font("NanumGothicExtraBold.ttf", 96),
        "caption":load_font("NanumGothic.ttf", 36),
        "part":   load_font("NanumGothicBold.ttf", 22),
        "watermark": load_font("NanumGothic.ttf", 22),
        "counter": load_font("NanumGothicExtraBold.ttf", 56),
    }


def text_size(draw, text, font):
    if not text:
        return 0, 0
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def gradient_bg(part):
    img = Image.new("RGB", (W, H), COLORS["bg"])
    accent = PART_COLORS.get(part, COLORS["gold"])
    glow = Image.new("RGB", (W, H), COLORS["bg"])
    gd = ImageDraw.Draw(glow)
    for r in range(900, 100, -40):
        alpha = int(28 * (r / 900) ** 0.5)
        color = tuple(min(255, c + alpha) for c in COLORS["bg"])
        g = tuple(int(c * 0.92 + a * 0.08) for c, a in zip(color, accent))
        gd.ellipse((-200 - r//2, -300 - r//2, 600 + r//2, 400 + r//2), fill=g)
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img = Image.blend(img, glow, 0.55)
    return img


def draw_corner_marks(draw, accent):
    draw.line([(80, 80), (160, 80)], fill=accent, width=3)
    draw.line([(80, 80), (80, 160)], fill=accent, width=3)
    draw.line([(W - 160, H - 80), (W - 80, H - 80)], fill=accent, width=3)
    draw.line([(W - 80, H - 160), (W - 80, H - 80)], fill=accent, width=3)


def render_scene(scene, scene_num, total_scenes, out_path):
    img = gradient_bg(scene["part"])
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    accent_key = scene.get("accent", "gold")
    accent = COLORS.get(accent_key, COLORS["gold"])
    part_color = PART_COLORS.get(scene["part"], COLORS["gold"])

    draw_corner_marks(draw, part_color)

    # part badge
    part_text = scene["part"]
    pw, ph = text_size(draw, part_text, fonts["part"])
    badge_pad = 18
    bx, by = 110, 110
    draw.rounded_rectangle(
        (bx, by, bx + pw + badge_pad * 2, by + ph + badge_pad + 4),
        radius=10, fill=part_color)
    draw.text((bx + badge_pad, by + badge_pad // 2), part_text,
              font=fonts["part"], fill=(20, 20, 20))

    # scene counter
    counter = f"{scene_num:02d} / {total_scenes:02d}"
    cw, ch = text_size(draw, counter, fonts["counter"])
    draw.text((W - 110 - cw, 100), counter, font=fonts["counter"], fill=COLORS["muted"])

    # title
    if scene.get("title"):
        title = scene["title"]
        tw, th = text_size(draw, title, fonts["label"])
        draw.text(((W - tw) // 2, 280), title, font=fonts["label"], fill=COLORS["muted"])

    big1, big2 = scene.get("big1", ""), scene.get("big2", "")

    def fit_font(text, base_font, alt_font):
        if not text:
            return base_font
        tw = text_size(draw, text, base_font)[0]
        return base_font if tw < W - 240 else alt_font

    f1 = fit_font(big1, fonts["big"], fonts["big_sm"])
    f2 = fit_font(big2, fonts["big"], fonts["big_sm"])

    h1 = text_size(draw, big1, f1)[1] if big1 else 0
    h2 = text_size(draw, big2, f2)[1] if big2 else 0
    gap = 24 if (big1 and big2) else 0
    block_h = h1 + gap + h2
    y0 = (H - block_h) // 2 - 20

    if big1:
        w1 = text_size(draw, big1, f1)[0]
        draw.text(((W - w1) // 2, y0), big1, font=f1, fill=COLORS["white"])
    if big2:
        w2 = text_size(draw, big2, f2)[0]
        draw.text(((W - w2) // 2, y0 + h1 + gap), big2, font=f2, fill=accent)

    if big1 or big2:
        ux = W // 2 - 60
        uy = y0 + block_h + 40
        draw.rectangle((ux, uy, ux + 120, uy + 6), fill=accent)

    # caption
    if scene.get("caption"):
        cap = scene["caption"]
        cw_, ch_ = text_size(draw, cap, fonts["caption"])
        if cw_ > W - 240:
            mid = len(cap) // 2
            split = cap.rfind(" ", 0, mid + 8)
            if split <= 0:
                split = mid
            line1, line2 = cap[:split].strip(), cap[split:].strip()
            for i, line in enumerate([line1, line2]):
                lw, lh = text_size(draw, line, fonts["caption"])
                draw.text(((W - lw) // 2, H - 220 + i * (lh + 8)), line,
                          font=fonts["caption"], fill=COLORS["muted"])
        else:
            draw.text(((W - cw_) // 2, H - 200), cap,
                      font=fonts["caption"], fill=COLORS["muted"])

    wm = "비즈PT · AI 시대 왜 책을 읽어야 할까"
    ww, wh = text_size(draw, wm, fonts["watermark"])
    draw.text((W - 110 - ww, H - 100), wm, font=fonts["watermark"], fill=COLORS["muted"])

    img.save(out_path, "PNG", optimize=True)
    return out_path


def render_all(scenes, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    n = len(scenes)
    for i, sc in enumerate(scenes, start=1):
        p = os.path.join(out_dir, f"scene_{i:02d}.png")
        render_scene(sc, i, n, p)
        paths.append(p)
    return paths


if __name__ == "__main__":
    from scenes import SCENES
    here = os.path.dirname(__file__)
    out = os.path.join(here, "slides")
    paths = render_all(SCENES, out)
    print(f"Done. {len(paths)} slides -> {out}")
