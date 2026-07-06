"""
v2 슬라이드 렌더러 — 사진 배경 + 영화적 처리 + 키네틱 타이포 오버레이

레이아웃 패턴 (씬 part에 따라 다르게):
  HOOK   : 사진 풀블리드 + 강한 비넷 + 큰 텍스트 우/하 정렬
  INTRO  : 사진 + 어두운 그라데이션 + 중앙 정렬 (메인 메시지 강조)
  BODY?  : 사진 좌측 50% / 텍스트 우측 50% 분할
  실전   : 사진 풀블리드 + 좌하단 큰 숫자 1/2/3
  CTA    : 사진 + 페이드 + 중앙 정렬
  전환   : 단색 + 텍스트 (전환은 짧으니 단순)
이미지가 없거나 너무 작으면 v1 그라데이션으로 폴백
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1920, 1080
FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
IMG_DIR  = os.path.join(os.path.dirname(__file__), "images")

COLORS = {
    "bg":     (15, 17, 21),
    "text":   (255, 255, 255),
    "muted":  (200, 207, 222),
    "gold":   (255, 209, 102),
    "green":  (6, 214, 160),
    "red":    (239, 71, 111),
    "info":   (90, 196, 224),
    "white":  (255, 255, 255),
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


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def get_fonts():
    return {
        "label":     font("NanumGothicBold.ttf", 32),
        "big":       font("NanumGothicExtraBold.ttf", 132),
        "big_sm":    font("NanumGothicExtraBold.ttf", 96),
        "big_xs":    font("NanumGothicExtraBold.ttf", 76),
        "caption":   font("NanumGothic.ttf", 36),
        "part":      font("NanumGothicBold.ttf", 22),
        "watermark": font("NanumGothic.ttf", 22),
        "counter":   font("NanumGothicExtraBold.ttf", 56),
        "huge_num":  font("NanumGothicExtraBold.ttf", 320),
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
            # cover-fit to 1920x1080
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


def cinematic_treat(img, dim=0.45, blur=0):
    """Movie-feel: lower brightness + slight blur + subtle vignette."""
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(dim)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.05)
    # vignette
    vignette = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vignette)
    for r in range(900, 200, -60):
        alpha = int(140 * (1 - (r / 900) ** 1.4))
        if alpha < 0: alpha = 0
        vd.ellipse((-100 - r//2, -100 - r//2, 600 + r//2, 400 + r//2),
                    fill=255 - alpha)
    vignette = vignette.filter(ImageFilter.GaussianBlur(160))
    black = Image.new("RGB", (W, H), (0, 0, 0))
    img = Image.composite(img, black, vignette)
    return img


def gradient_bg(part):
    img = Image.new("RGB", (W, H), COLORS["bg"])
    accent = PART_COLORS.get(part, COLORS["gold"])
    glow = Image.new("RGB", (W, H), COLORS["bg"])
    gd = ImageDraw.Draw(glow)
    for r in range(900, 100, -40):
        alpha = int(28 * (r / 900) ** 0.5)
        c = tuple(min(255, c + alpha) for c in COLORS["bg"])
        g = tuple(int(c0 * 0.92 + a * 0.08) for c0, a in zip(c, accent))
        gd.ellipse((-200 - r//2, -300 - r//2, 600 + r//2, 400 + r//2), fill=g)
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    return Image.blend(img, glow, 0.55)


def draw_text_with_shadow(draw, pos, text, fnt, fill, shadow=(0, 0, 0, 200)):
    x, y = pos
    # shadow underlay
    for ox, oy in [(2, 2), (3, 3), (-1, 1), (1, -1)]:
        draw.text((x + ox, y + oy), text, font=fnt, fill=(0, 0, 0))
    # main
    draw.text((x, y), text, font=fnt, fill=fill)


def draw_corner_marks(draw, accent):
    return
    draw.line([(80, 80), (160, 80)], fill=accent, width=3)
    draw.line([(80, 80), (80, 160)], fill=accent, width=3)
    draw.line([(W - 160, H - 80), (W - 80, H - 80)], fill=accent, width=3)
    draw.line([(W - 80, H - 160), (W - 80, H - 80)], fill=accent, width=3)


def draw_part_badge(draw, part, fonts):
    return
    pw, ph = text_size(draw, part, fonts["part"])
    pad = 18
    x, y = 110, 110
    color = PART_COLORS.get(part, COLORS["gold"])
    draw.rounded_rectangle((x, y, x + pw + pad * 2, y + ph + pad + 4),
                           radius=10, fill=color)
    draw.text((x + pad, y + pad // 2), part, font=fonts["part"], fill=(20, 20, 20))


def draw_counter(draw, n, total, fonts):
    return
    text = f"{n:02d} / {total:02d}"
    cw, _ = text_size(draw, text, fonts["counter"])
    draw_text_with_shadow(draw, (W - 110 - cw, 100), text,
                           fonts["counter"], COLORS["muted"])


def draw_watermark(draw, fonts):
    return
    wm = "비즈PT · AI 시대 왜 책을 읽어야 할까"
    ww, _ = text_size(draw, wm, fonts["watermark"])
    draw_text_with_shadow(draw, (W - 110 - ww, H - 100), wm,
                           fonts["watermark"], COLORS["muted"])


def fit_font(draw, text, base_font, alt_font, alt2_font, max_w=W - 240):
    if not text: return base_font
    if text_size(draw, text, base_font)[0] <= max_w: return base_font
    if text_size(draw, text, alt_font)[0] <= max_w: return alt_font
    return alt2_font


def render_centered(scene, scene_num, total_scenes, out_path):
    """Default centered layout (HOOK, INTRO, BODY1 main shots, CTA)."""
    img_bg = load_scene_image(scene["id"])
    if img_bg is not None:
        bg = cinematic_treat(img_bg, dim=0.42)
    else:
        bg = gradient_bg(scene["part"])
    draw = ImageDraw.Draw(bg)
    fonts = get_fonts()
    accent_key = scene.get("accent", "gold")
    accent = COLORS.get(accent_key, COLORS["gold"])

    draw_corner_marks(draw, PART_COLORS.get(scene["part"], COLORS["gold"]))
    draw_part_badge(draw, scene["part"], fonts)
    draw_counter(draw, scene_num, total_scenes, fonts)

    if scene.get("title"):
        title = scene["title"]
        tw, _ = text_size(draw, title, fonts["label"])
        draw_text_with_shadow(draw, ((W - tw) // 2, 270),
                               title, fonts["label"], COLORS["muted"])

    big1 = scene.get("big1", "")
    big2 = scene.get("big2", "")
    f1 = fit_font(draw, big1, fonts["big"], fonts["big_sm"], fonts["big_xs"])
    f2 = fit_font(draw, big2, fonts["big"], fonts["big_sm"], fonts["big_xs"])

    h1 = text_size(draw, big1, f1)[1] if big1 else 0
    h2 = text_size(draw, big2, f2)[1] if big2 else 0
    gap = 24 if (big1 and big2) else 0
    block_h = h1 + gap + h2
    y0 = (H - block_h) // 2 - 20

    if big1:
        w1 = text_size(draw, big1, f1)[0]
        draw_text_with_shadow(draw, ((W - w1) // 2, y0), big1, f1, COLORS["white"])
    if big2:
        w2 = text_size(draw, big2, f2)[0]
        draw_text_with_shadow(draw, ((W - w2) // 2, y0 + h1 + gap), big2, f2, accent)

    if big1 or big2:
        ux = W // 2 - 60
        uy = y0 + block_h + 40
        draw.rectangle((ux, uy, ux + 120, uy + 6), fill=accent)

    if scene.get("caption"):
        cap = scene["caption"]
        cw_, _ = text_size(draw, cap, fonts["caption"])
        if cw_ > W - 240:
            mid = len(cap) // 2
            split = cap.rfind(" ", 0, mid + 8)
            if split <= 0: split = mid
            l1, l2 = cap[:split].strip(), cap[split:].strip()
            for i, line in enumerate([l1, l2]):
                lw, lh = text_size(draw, line, fonts["caption"])
                draw_text_with_shadow(draw, ((W - lw) // 2, H - 220 + i * (lh + 8)),
                                       line, fonts["caption"], COLORS["muted"])
        else:
            draw_text_with_shadow(draw, ((W - cw_) // 2, H - 200), cap,
                                   fonts["caption"], COLORS["muted"])

    draw_watermark(draw, fonts)
    bg.save(out_path, "PNG", optimize=True)
    return out_path


def render_split(scene, scene_num, total_scenes, out_path):
    """Split layout — image on left 55%, text right 45%. Used for BODY 2~5."""
    bg = Image.new("RGB", (W, H), COLORS["bg"])

    # Left: image
    img_bg = load_scene_image(scene["id"])
    if img_bg is not None:
        left = img_bg.crop((0, 0, int(W * 0.55), H))
        # darken edge
        mask = Image.new("L", left.size, 255)
        md = ImageDraw.Draw(mask)
        for x in range(left.size[0] - 200, left.size[0]):
            a = int(255 * (left.size[0] - x) / 200)
            md.line([(x, 0), (x, left.size[1])], fill=a)
        left.putalpha(mask)
        bg.paste(left, (0, 0), left.convert("RGBA"))
        # subtle dim
        overlay = Image.new("RGB", left.size, (0, 0, 0))
        bg.paste(overlay, (0, 0), Image.eval(mask, lambda v: int(v * 0.25)))
    else:
        # gradient half
        grad = gradient_bg(scene["part"])
        bg.paste(grad.crop((0, 0, int(W * 0.55), H)), (0, 0))

    draw = ImageDraw.Draw(bg)
    fonts = get_fonts()
    accent = COLORS.get(scene.get("accent", "gold"), COLORS["gold"])

    draw_corner_marks(draw, PART_COLORS.get(scene["part"], COLORS["gold"]))
    draw_part_badge(draw, scene["part"], fonts)
    draw_counter(draw, scene_num, total_scenes, fonts)

    # right text region: x = 0.55W .. W
    rx = int(W * 0.58)
    rw = W - rx - 110

    if scene.get("title"):
        draw_text_with_shadow(draw, (rx, 280), scene["title"],
                               fonts["label"], COLORS["muted"])

    big1 = scene.get("big1", "")
    big2 = scene.get("big2", "")
    # Use smaller base font for split
    f1 = fit_font(draw, big1, fonts["big_sm"], fonts["big_xs"], fonts["caption"], max_w=rw)
    f2 = fit_font(draw, big2, fonts["big_sm"], fonts["big_xs"], fonts["caption"], max_w=rw)

    h1 = text_size(draw, big1, f1)[1] if big1 else 0
    h2 = text_size(draw, big2, f2)[1] if big2 else 0
    gap = 18 if (big1 and big2) else 0
    block_h = h1 + gap + h2
    y0 = (H - block_h) // 2 - 20

    if big1:
        draw_text_with_shadow(draw, (rx, y0), big1, f1, COLORS["white"])
    if big2:
        draw_text_with_shadow(draw, (rx, y0 + h1 + gap), big2, f2, accent)

    if big1 or big2:
        draw.rectangle((rx, y0 + block_h + 30, rx + 120, y0 + block_h + 36), fill=accent)

    if scene.get("caption"):
        cap = scene["caption"]
        # wrap into right region
        words = cap.split()
        lines = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if text_size(draw, test, fonts["caption"])[0] <= rw:
                cur = test
            else:
                lines.append(cur); cur = w
        if cur: lines.append(cur)
        for i, ln in enumerate(lines[:3]):
            draw_text_with_shadow(draw, (rx, H - 220 + i * 44),
                                   ln, fonts["caption"], COLORS["muted"])

    draw_watermark(draw, fonts)
    bg.save(out_path, "PNG", optimize=True)
    return out_path


def render_huge_num(scene, scene_num, total_scenes, out_path):
    """For 실전 1/2/3 — huge number left, text right, photo background."""
    img_bg = load_scene_image(scene["id"])
    if img_bg is not None:
        bg = cinematic_treat(img_bg, dim=0.35)
    else:
        bg = gradient_bg(scene["part"])
    draw = ImageDraw.Draw(bg)
    fonts = get_fonts()
    accent = COLORS.get(scene.get("accent", "green"), COLORS["green"])

    draw_corner_marks(draw, PART_COLORS.get(scene["part"], COLORS["gold"]))
    draw_part_badge(draw, scene["part"], fonts)
    draw_counter(draw, scene_num, total_scenes, fonts)

    # huge number on left
    num = scene.get("title", "1")
    num_w, num_h = text_size(draw, num, fonts["huge_num"])
    nx = 200
    ny = (H - num_h) // 2 - 60
    draw_text_with_shadow(draw, (nx, ny), num, fonts["huge_num"], accent)

    # text right
    rx = nx + num_w + 80
    rw = W - rx - 140
    big1 = scene.get("big1", "")
    big2 = scene.get("big2", "")
    f1 = fit_font(draw, big1, fonts["big_sm"], fonts["big_xs"], fonts["caption"], max_w=rw)
    f2 = fit_font(draw, big2, fonts["big_sm"], fonts["big_xs"], fonts["caption"], max_w=rw)
    h1 = text_size(draw, big1, f1)[1] if big1 else 0
    h2 = text_size(draw, big2, f2)[1] if big2 else 0
    gap = 20
    block_h = h1 + gap + h2
    y0 = (H - block_h) // 2 - 20
    if big1:
        draw_text_with_shadow(draw, (rx, y0), big1, f1, COLORS["white"])
    if big2:
        draw_text_with_shadow(draw, (rx, y0 + h1 + gap), big2, f2, accent)
    if big1 or big2:
        draw.rectangle((rx, y0 + block_h + 30, rx + 120, y0 + block_h + 36), fill=accent)

    if scene.get("caption"):
        cap = scene["caption"]
        words = cap.split()
        lines = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if text_size(draw, test, fonts["caption"])[0] <= rw:
                cur = test
            else:
                lines.append(cur); cur = w
        if cur: lines.append(cur)
        for i, ln in enumerate(lines[:2]):
            draw_text_with_shadow(draw, (rx, H - 220 + i * 44),
                                   ln, fonts["caption"], COLORS["muted"])

    draw_watermark(draw, fonts)
    bg.save(out_path, "PNG", optimize=True)
    return out_path


def render_scene(scene, scene_num, total_scenes, out_path):
    part = scene["part"]
    # 실전 1/2/3 with single-digit titles use huge_num
    if part == "실전" and scene.get("title", "").strip() in {"1", "2", "3"}:
        return render_huge_num(scene, scene_num, total_scenes, out_path)
    # BODY 2~5 use split
    if part in {"BODY2", "BODY3", "BODY4", "BODY5"}:
        return render_split(scene, scene_num, total_scenes, out_path)
    # default: centered
    return render_centered(scene, scene_num, total_scenes, out_path)


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
    out = os.path.join(os.path.dirname(__file__), "slides")
    paths = render_all(SCENES, out)
    print(f"Done. {len(paths)} slides -> {out}")
