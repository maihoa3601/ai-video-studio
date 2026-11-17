"""
High-End Dynamic Visual Scene Components for AI TikTok Video Factory.
Ultra-premium dark tech aesthetics inspired by Apple, Linear, and Vercel:
- Multi-colored ambient glow orbs & cyber perspective grids
- Frosted glassmorphism panels with neon borders
- Viral CapCut / TikTok kinetic subtitles with keyword aura
- 10 distinct, highly-polished scene components
"""

import math
import os
import random
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import config
from utils.text import extract_highlight_keywords

def get_font(size: int = 48, bold: bool = True) -> ImageFont.FreeTypeFont:
    """Load high-quality modern Vietnamese Unicode font (prioritizing Segoe UI / SF Pro)."""
    # 1. Prefer modern clean geometric sans-serif fonts on system
    sys_candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/seguisb.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/tahomabd.ttf" if bold else "C:/Windows/Fonts/tahoma.ttf",
        "/System/Library/Fonts/SFCompact.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]
    for p in sys_candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue

    # 2. Local fonts directory fallback
    font_files = list(config.FONTS_DIR.glob("*.ttf")) + list(config.FONTS_DIR.glob("*.otf"))
    if font_files:
        try:
            return ImageFont.truetype(str(font_files[0]), size)
        except Exception:
            pass

    return ImageFont.load_default()

def draw_luxury_cyber_background(
    width: int = 1080,
    height: int = 1920,
    top_color=(8, 11, 24),
    bottom_color=(12, 17, 36),
    orb1_color=(99, 102, 241),   # Indigo
    orb2_color=(6, 182, 212)    # Cyan
) -> Image.Image:
    """
    Generate an ultra-premium dark background with multi-colored ambient radial glow orbs,
    subtle cyber perspective grid, floating luminous dust particles, and corner HUD accents.
    """
    img = Image.new("RGB", (width, height), top_color)
    draw = ImageDraw.Draw(img)
    
    # 1. Base vertical gradient
    for y in range(0, height, 2):
        ratio = y / height
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b), width=2)

    # 2. Ambient radial glow orbs
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow_layer)
    
    # Orb 1: Upper-right atmospheric glow (Indigo/Purple)
    ox1, oy1 = width - 160, 380
    for r in range(340, 20, -25):
        alpha = int(34 * (1.0 - r / 340))
        g_draw.ellipse([ox1 - r, oy1 - r, ox1 + r, oy1 + r], fill=(orb1_color[0], orb1_color[1], orb1_color[2], alpha))
        
    # Orb 2: Center-left cyan aura
    ox2, oy2 = 160, 820
    for r in range(300, 20, -25):
        alpha = int(30 * (1.0 - r / 300))
        g_draw.ellipse([ox2 - r, oy2 - r, ox2 + r, oy2 + r], fill=(orb2_color[0], orb2_color[1], orb2_color[2], alpha))

    # Orb 3: Bottom ambient warmth / tech depth
    ox3, oy3 = width // 2, height - 380
    for r in range(320, 20, -30):
        alpha = int(22 * (1.0 - r / 320))
        g_draw.ellipse([ox3 - r, oy3 - r, ox3 + r, oy3 + r], fill=(15, 23, 42, alpha))

    # 3. Fine high-tech grid overlay
    spacing = 90
    for x in range(0, width + 1, spacing):
        g_draw.line([(x, 0), (x, height)], fill=(0, 240, 255, 10), width=1)
    for y in range(0, height + 1, spacing):
        g_draw.line([(0, y), (width, y)], fill=(0, 240, 255, 10), width=1)

    # 4. Floating tech coordinate micro-particles
    rng = random.Random(99)
    for _ in range(24):
        px = rng.randint(40, width - 40)
        py = rng.randint(120, height - 200)
        p_alpha = rng.randint(40, 180)
        p_size = rng.choice([2, 3])
        g_draw.ellipse([px - p_size, py - p_size, px + p_size, py + p_size], fill=(255, 255, 255, p_alpha))

    # 5. Luxury Cyber Corner HUD Brackets
    hud_c = (0, 240, 255, 90)
    c_len = 24
    c_pad = 32
    # Top-Left
    g_draw.line([(c_pad, c_pad), (c_pad + c_len, c_pad)], fill=hud_c, width=2)
    g_draw.line([(c_pad, c_pad), (c_pad, c_pad + c_len)], fill=hud_c, width=2)
    # Top-Right
    g_draw.line([(width - c_pad, c_pad), (width - c_pad - c_len, c_pad)], fill=hud_c, width=2)
    g_draw.line([(width - c_pad, c_pad), (width - c_pad, c_pad + c_len)], fill=hud_c, width=2)
    # Bottom-Left
    g_draw.line([(c_pad, height - c_pad), (c_pad + c_len, height - c_pad)], fill=hud_c, width=2)
    g_draw.line([(c_pad, height - c_pad), (c_pad, height - c_pad - c_len)], fill=hud_c, width=2)
    # Bottom-Right
    g_draw.line([(width - c_pad, height - c_pad), (width - c_pad - c_len, height - c_pad)], fill=hud_c, width=2)
    g_draw.line([(width - c_pad, height - c_pad), (width - c_pad, height - c_pad - c_len)], fill=hud_c, width=2)

    img.paste(glow_layer, (0, 0), glow_layer)
    return img

def render_top_header(img: Image.Image, category_tag: str, beat_idx: int, total_beats: int):
    """
    Render high-end top brand status bar in TikTok safe zone (y=120 to y=200).
    Features glowing pill badge, pulsing green status indicator, dynamic step counter,
    and smart truncation to prevent text overflow.
    """
    header_layer = Image.new("RGBA", (img.width, img.height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(header_layer)
    
    tag_font = get_font(26, bold=True)
    cat_font = get_font(22, bold=True)
    status_font = get_font(22, bold=True)
    
    # Glowing Brand Pill Badge
    pill_x1, pill_y1 = 60, 130
    pill_x2, pill_y2 = 320, 185
    draw.rounded_rectangle([pill_x1, pill_y1, pill_x2, pill_y2], radius=16, fill=(15, 23, 42, 230), outline=(0, 240, 255, 220), width=2)
    
    # Live pulsing indicator dot with outer glow halo
    draw.ellipse([pill_x1 + 14, pill_y1 + 18, pill_x1 + 34, pill_y1 + 38], fill=(34, 197, 94, 60))
    draw.ellipse([pill_x1 + 18, pill_y1 + 22, pill_x1 + 30, pill_y1 + 34], fill=(34, 197, 94, 255))
    draw.text((pill_x1 + 42, pill_y1 + 14), config.CHANNEL_NAME.upper(), fill=(0, 240, 255), font=tag_font)

    # Category breadcrumb with available width calculation (never clip into STEP badge)
    avail_w = (img.width - 270) - 350 - 20
    cat_str = f"/  {category_tag.upper()}"
    while cat_font.getbbox(cat_str)[2] > avail_w and len(cat_str) > 10:
        cat_str = cat_str[:-4] + "..."
    draw.text((345, 146), cat_str, fill=(190, 205, 225), font=cat_font)
    
    # Progress Step Indicator
    counter_str = f"STEP {beat_idx + 1:02d} / {total_beats:02d}"
    draw.rounded_rectangle([img.width - 260, 132, img.width - 60, 185], radius=14, fill=(30, 41, 59, 210), outline=(100, 116, 139, 140), width=1)
    draw.text((img.width - 240, 145), counter_str, fill=(226, 232, 240), font=status_font)
    
    # Cyan Glowing Gradient Divider Rule (fades in and out smoothly)
    div_y = 205
    for x in range(60, img.width - 60):
        # Peak opacity in center, 0 at borders
        dist = abs(x - img.width // 2) / (img.width // 2 - 60)
        alpha = int(140 * max(0, 1.0 - dist * dist))
        if alpha > 0:
            draw.line([(x, div_y), (x, div_y)], fill=(0, 240, 255, alpha), width=1)

    img.paste(header_layer, (0, 0), header_layer)

def render_dynamic_caption(img: Image.Image, caption_text: str, highlight_words: List[str] = None, enabled: bool = False):
    """
    Render CapCut / TikTok viral kinetic caption.
    Disabled by default when dynamic ASS subtitles are burned in post-processing,
    preventing double-exposure ghosting during scene xfade transitions.
    """
    if not enabled or not caption_text:
        return

    words = caption_text.strip().split()
    if not words:
        return

    # Balanced line break (max 3-4 words per line)
    if len(words) <= 4:
        lines = [" ".join(words)]
    else:
        half = (len(words) + 1) // 2
        lines = [" ".join(words[:half]), " ".join(words[half:])]

    # Auto font size calculation to guarantee comfortable margins
    max_len = max(len(l) for l in lines)
    if max_len > 24:
        font_size = 46
        line_spacing = 68
    elif max_len > 18:
        font_size = 52
        line_spacing = 76
    else:
        font_size = 58
        line_spacing = 82

    font = get_font(font_size, bold=True)
    
    caption_layer = Image.new("RGBA", (img.width, img.height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(caption_layer)
    
    y_start = 1285
    hl_set = set(w.lower().rstrip(".,!?") for w in (highlight_words or extract_highlight_keywords(caption_text)))
    
    for idx, line in enumerate(lines):
        line_y = y_start + idx * line_spacing
        line_words = line.split()
        
        # Measure word dimensions
        word_data = []
        total_w = 0
        for w in line_words:
            bbox = font.getbbox(w)
            w_width = bbox[2] - bbox[0]
            word_data.append((w, w_width))
            total_w += w_width
        
        space_w = font.getbbox(" ")[2] - font.getbbox(" ")[0]
        total_w += space_w * (len(line_words) - 1)
        
        # Frosted glass dark capsule backing
        pad_x = 28
        pad_y = 10
        pill_x1 = max(40, (img.width - total_w) // 2 - pad_x)
        pill_x2 = min(img.width - 40, (img.width + total_w) // 2 + pad_x)
        draw.rounded_rectangle([pill_x1, line_y - pad_y, pill_x2, line_y + font_size + pad_y + 4], radius=20, fill=(10, 15, 30, 235), outline=(0, 240, 255, 60), width=1)
        
        # Word-by-word typography
        curr_x = (img.width - total_w) // 2
        for w, w_width in word_data:
            clean_w = w.lower().rstrip(".,!?")
            is_highlight = clean_w in hl_set or (w.isupper() and len(w) > 1)
            
            if is_highlight:
                fill_color = (255, 230, 0, 255)  # Neon Gold
                # Neon glow effect
                draw.text((curr_x - 1, line_y), w, fill=(255, 230, 0, 100), font=font)
                draw.text((curr_x + 1, line_y), w, fill=(255, 230, 0, 100), font=font)
                draw.text((curr_x, line_y - 1), w, fill=(255, 230, 0, 100), font=font)
                draw.text((curr_x, line_y + 1), w, fill=(255, 230, 0, 100), font=font)
            else:
                fill_color = (255, 255, 255, 255)
            
            # Text shadow
            draw.text((curr_x + 3, line_y + 3), w, fill=(0, 0, 0, 220), font=font)
            draw.text((curr_x, line_y), w, fill=fill_color, font=font)
            curr_x += w_width + space_w

    img.paste(caption_layer, (0, 0), caption_layer)

# =========================================================================
# COMPONENT 1: KineticTextScene (Jaw-Dropping Hook Typography)
# =========================================================================
def render_kinetic_text_scene(
    headline_top: str,
    headline_main: str,
    tag: str = "THÔNG ĐIỆP CỐT LÕI",
    caption_text: str = "",
    beat_idx: int = 0,
    total_beats: int = 10
) -> Image.Image:
    """Render cinematic holographic kinetic headline with cyber glowing brackets and focal rings."""
    img = draw_luxury_cyber_background(
        top_color=(10, 8, 26),
        bottom_color=(18, 14, 44),
        orb1_color=(168, 85, 247),
        orb2_color=(0, 240, 255)
    )
    render_top_header(img, tag, beat_idx, total_beats)
    
    draw = ImageDraw.Draw(img)
    center_y = 660
    
    overlay = Image.new("RGBA", (img.width, img.height), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(overlay)
    
    # Futuristic L-Shaped Tech Brackets
    bx1, bx2 = 80, 1000
    by1, by2 = 360, 960
    b_len = 65
    b_color = (0, 240, 255, 220)
    
    o_draw.line([(bx1, by1), (bx1 + b_len, by1)], fill=b_color, width=4)
    o_draw.line([(bx1, by1), (bx1, by1 + b_len)], fill=b_color, width=4)
    o_draw.line([(bx2, by1), (bx2 - b_len, by1)], fill=b_color, width=4)
    o_draw.line([(bx2, by1), (bx2, by1 + b_len)], fill=b_color, width=4)
    o_draw.line([(bx1, by2), (bx1 + b_len, by2)], fill=b_color, width=4)
    o_draw.line([(bx1, by2), (bx1, by2 - b_len)], fill=b_color, width=4)
    o_draw.line([(bx2, by2), (bx2 - b_len, by2)], fill=b_color, width=4)
    o_draw.line([(bx2, by2), (bx2, by2 - b_len)], fill=b_color, width=4)
    
    # Pulsing glowing focal rings behind center
    mid_x = img.width // 2
    for r in [280, 190, 100]:
        o_draw.ellipse([mid_x - r, center_y - r, mid_x + r, center_y + r], outline=(168, 85, 247, 40), width=2)
    # Crosshairs tick marks
    o_draw.line([(mid_x - 30, center_y), (mid_x + 30, center_y)], fill=(0, 240, 255, 60), width=1)
    o_draw.line([(mid_x, center_y - 30), (mid_x, center_y + 30)], fill=(0, 240, 255, 60), width=1)

    img.paste(overlay, (0, 0), overlay)

    # 1. Top Sub-headline in crisp ice-white
    font_top = get_font(52, bold=True)
    bbox_top = font_top.getbbox(headline_top)
    w_top = bbox_top[2] - bbox_top[0]
    draw.text(((img.width - w_top) // 2, center_y - 130), headline_top, fill=(224, 231, 255), font=font_top)
    
    # 2. Main Kinetic Headline in vibrant Electric Cyan with double drop shadow
    font_main = get_font(84, bold=True)
    bbox_main = font_main.getbbox(headline_main)
    w_main = bbox_main[2] - bbox_main[0]
    draw.text(((img.width - w_main) // 2 + 5, center_y - 20 + 5), headline_main, fill=(0, 80, 140), font=font_main)
    draw.text(((img.width - w_main) // 2, center_y - 20), headline_main, fill=(0, 240, 255), font=font_main)

    # 3. Gold Insight Tag at bottom
    font_badge = get_font(30, bold=True)
    b_text = "[ ĐÃ ĐẾN LÚC BẠN CẦN BIẾT ]"
    b_box = font_badge.getbbox(b_text)
    b_w = b_box[2] - b_box[0]
    
    # Pill around badge
    px1 = (img.width - b_w) // 2 - 24
    px2 = (img.width + b_w) // 2 + 24
    draw.rounded_rectangle([px1, center_y + 125, px2, center_y + 180], radius=14, fill=(30, 41, 59, 210), outline=(255, 230, 0, 190), width=2)
    draw.text(((img.width - b_w) // 2, center_y + 135), b_text, fill=(255, 230, 0), font=font_badge)

    render_dynamic_caption(img, caption_text)
    return img

# =========================================================================
# COMPONENT 2: WorkflowScene (DATA -> MODEL -> RESULT Flowchart)
# =========================================================================
def render_workflow_scene(
    active_step: int = 1,
    caption_text: str = "",
    beat_idx: int = 0,
    total_beats: int = 10
) -> Image.Image:
    """Render high-tech 3-stage flowchart with glowing nodes and energy pulses."""
    img = draw_luxury_cyber_background(
        top_color=(8, 16, 28),
        bottom_color=(12, 28, 48),
        orb1_color=(6, 182, 212),
        orb2_color=(34, 197, 94)
    )
    render_top_header(img, "SƠ ĐỒ NGUYÊN LÝ HOẠT ĐỘNG", beat_idx, total_beats)
    
    overlay = Image.new("RGBA", (img.width, img.height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    nodes = [
        {"num": "01", "badge": "INPUT", "title": "DỮ LIỆU ĐẦU VÀO", "desc": "Văn bản, hình ảnh, mã nguồn", "color": (6, 182, 212)},
        {"num": "02", "badge": "AI CORE", "title": "MÔ HÌNH HỌC TẬP", "desc": "Nhận diện mẫu & quy luật", "color": (168, 85, 247)},
        {"num": "03", "badge": "OUTPUT", "title": "DỰ ĐOÁN & KẾT QUẢ", "desc": "Tạo giải pháp & nội dung", "color": (34, 197, 94)}
    ]
    
    y_starts = [360, 580, 800]
    card_w = 920
    card_h = 160
    x1 = (img.width - card_w) // 2
    x2 = x1 + card_w
    
    font_num = get_font(40, bold=True)
    font_badge = get_font(24, bold=True)
    font_title = get_font(42, bold=True)
    font_desc = get_font(28, bold=False)
    
    for idx, (node, y1) in enumerate(zip(nodes, y_starts), 1):
        y2 = y1 + card_h
        is_active = (idx <= active_step)
        is_current = (idx == active_step)
        accent = node["color"]
        
        bg_fill = (18, 28, 52, 245) if is_active else (10, 16, 28, 160)
        border_color = (accent[0], accent[1], accent[2], 240) if is_current else ((accent[0], accent[1], accent[2], 140) if is_active else (71, 85, 105, 80))
        border_w = 3 if is_current else (2 if is_active else 1)
        
        # Frosted glass card
        draw.rounded_rectangle([x1, y1, x2, y2], radius=24, fill=bg_fill, outline=border_color, width=border_w)
        
        # Left Accent Bar with glow
        if is_active:
            draw.rounded_rectangle([x1, y1, x1 + 12, y2], radius=6, fill=accent)
        
        # Step Number & Tag
        draw.text((x1 + 45, y1 + 38), node["num"], fill=accent if is_active else (148, 163, 184), font=font_num)
        
        # Badge Pill
        draw.rounded_rectangle([x1 + 40, y1 + 96, x1 + 150, y1 + 130], radius=8, fill=(accent[0], accent[1], accent[2], 40), outline=(accent[0], accent[1], accent[2], 160), width=1)
        draw.text((x1 + 52, y1 + 100), node["badge"], fill=accent, font=font_badge)
        
        # Title & Description
        draw.text((x1 + 185, y1 + 36), node["title"], fill=(255, 255, 255) if is_active else (148, 163, 184), font=font_title)
        draw.text((x1 + 185, y1 + 95), node["desc"], fill=(186, 230, 253) if is_active else (100, 116, 139), font=font_desc)
        
        # Connecting Pulse Arrow
        if idx < len(nodes):
            ay1 = y2 + 8
            ay2 = ay1 + 42
            mid_x = img.width // 2
            a_color = (0, 240, 255, 240) if is_active else (71, 85, 105, 90)
            draw.line([(mid_x, ay1), (mid_x, ay2)], fill=a_color, width=4)
            draw.polygon([(mid_x - 12, ay2 - 10), (mid_x + 12, ay2 - 10), (mid_x, ay2 + 6)], fill=a_color)

    img.paste(overlay, (0, 0), overlay)
    render_dynamic_caption(img, caption_text)
    return img

# =========================================================================
# COMPONENT 3: ChatUIScene (Sleek Smartphone AI Chat Mockup)
# =========================================================================
def render_chat_ui_scene(
    user_prompt: str = "Hôm nay tôi đã dùng AI ở đâu?",
    ai_response: str = "Tìm kiếm, bản đồ, lọc email và camera điện thoại của bạn đều có AI!",
    caption_text: str = "",
    beat_idx: int = 0,
    total_beats: int = 10
) -> Image.Image:
    """Render high-polish smartphone AI chat assistant interface with avatars."""
    img = draw_luxury_cyber_background(
        top_color=(10, 14, 30),
        bottom_color=(16, 24, 48),
        orb1_color=(59, 130, 246),
        orb2_color=(147, 51, 234)
    )
    render_top_header(img, "GIAO DIỆN TƯƠNG TÁC AI", beat_idx, total_beats)
    
    overlay = Image.new("RGBA", (img.width, img.height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Outer Smartphone Mockup Container (y=340 to y=1040)
    wx1, wy1 = 80, 340
    wx2, wy2 = 1000, 1040
    draw.rounded_rectangle([wx1, wy1, wx2, wy2], radius=32, fill=(15, 23, 42, 245), outline=(0, 240, 255, 160), width=2)
    
    # Window Title Bar (macOS Traffic Lights)
    draw.ellipse([wx1 + 40, wy1 + 35, wx1 + 58, wy1 + 53], fill=(239, 68, 68))
    draw.ellipse([wx1 + 72, wy1 + 35, wx1 + 90, wy1 + 53], fill=(234, 179, 8))
    draw.ellipse([wx1 + 104, wy1 + 35, wx1 + 122, wy1 + 53], fill=(34, 197, 94))
    
    font_bar = get_font(26, bold=True)
    draw.text((wx1 + 150, wy1 + 32), f"AI MASTER ASSISTANT • GPT-4o", fill=(148, 163, 184), font=font_bar)
    draw.line([(wx1, wy1 + 80), (wx2, wy1 + 80)], fill=(255, 255, 255, 25), width=1)
    
    font_bubble = get_font(36, bold=False)
    font_label = get_font(26, bold=True)
    font_avatar = get_font(20, bold=True)
    
    # 1. User Message (Right-aligned, Blue Gradient)
    u_y1 = wy1 + 120
    # User Avatar Tag Circle
    draw.ellipse([wx2 - 100, u_y1 - 6, wx2 - 60, u_y1 + 34], fill=(59, 130, 246))
    draw.text((wx2 - 88, u_y1), "U", fill=(255, 255, 255), font=font_avatar)
    draw.text((wx2 - 250, u_y1 + 2), "BẠN (USER)", fill=(148, 163, 184), font=font_label)
    
    draw.rounded_rectangle([wx1 + 180, u_y1 + 42, wx2 - 40, u_y1 + 155], radius=20, fill=(37, 99, 235, 235), outline=(96, 165, 250, 190), width=1)
    draw.text((wx1 + 215, u_y1 + 70), user_prompt, fill=(255, 255, 255), font=font_bubble)
    
    # 2. AI Response (Left-aligned, Dark Frosted with Cyan border)
    ai_y1 = u_y1 + 205
    # AI Avatar Circle
    draw.ellipse([wx1 + 40, ai_y1 - 6, wx1 + 80, ai_y1 + 34], fill=(0, 240, 255))
    draw.text((wx1 + 48, ai_y1), "AI", fill=(15, 23, 42), font=font_avatar)
    draw.text((wx1 + 95, ai_y1 + 2), f"{config.CHANNEL_NAME.upper()} (ASSISTANT)", fill=(0, 240, 255), font=font_label)
    
    draw.rounded_rectangle([wx1 + 40, ai_y1 + 42, wx2 - 80, ai_y1 + 270], radius=22, fill=(26, 36, 56, 245), outline=(0, 240, 255, 210), width=2)
    
    # Wrap text lines
    words = ai_response.split()
    half = (len(words) + 1) // 2
    l1 = " ".join(words[:half])
    l2 = " ".join(words[half:])
    
    draw.text((wx1 + 75, ai_y1 + 72), l1, fill=(241, 245, 249), font=font_bubble)
    draw.text((wx1 + 75, ai_y1 + 132), l2, fill=(241, 245, 249), font=font_bubble)
    
    # Blinking prompt cursor
    draw.rectangle([wx1 + 75, ai_y1 + 200, wx1 + 105, ai_y1 + 208], fill=(0, 240, 255))

    img.paste(overlay, (0, 0), overlay)
    render_dynamic_caption(img, caption_text)
    return img

# =========================================================================
# COMPONENT 4: IconGridScene (2x2 Bento Grid with Glowing Tags)
# =========================================================================
# =========================================================================
# COMPONENT 4: IconGridScene (2x2 Bento Grid with Glowing Vector Accents)
# =========================================================================
def render_icon_grid_scene(
    highlight_card: int = 0,
    caption_text: str = "",
    beat_idx: int = 0,
    total_beats: int = 10
) -> Image.Image:
    """Render 4 sleek Bento grid cards with glowing colored accent borders and custom vector icons."""
    img = draw_luxury_cyber_background(
        top_color=(8, 14, 28),
        bottom_color=(14, 24, 46),
        orb1_color=(6, 182, 212),
        orb2_color=(245, 158, 11)
    )
    render_top_header(img, "KHẢ NĂNG THỰC CHIẾN CỦA AI", beat_idx, total_beats)
    
    overlay = Image.new("RGBA", (img.width, img.height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    cards = [
        {"id": 1, "badge": "AUTO", "title": "TỰ ĐỘNG HÓA", "desc": "Tác vụ lặp đi lặp lại", "color": (6, 182, 212)},
        {"id": 2, "badge": "DATA", "title": "TỔNG HỢP DỮ LIỆU", "desc": "Tóm tắt tài liệu nhanh", "color": (168, 85, 247)},
        {"id": 3, "badge": "MEDIA", "title": "TẠO ẢNH & VIDEO", "desc": "Thiết kế đồ họa tức thì", "color": (236, 72, 153)},
        {"id": 4, "badge": "VOICE", "title": "GIỌNG NÓI AI", "desc": "Lồng tiếng đa ngôn ngữ", "color": (34, 197, 94)}
    ]
    
    col1_x1, col1_x2 = 70, 515
    col2_x1, col2_x2 = 565, 1010
    row1_y1, row1_y2 = 360, 640
    row2_y1, row2_y2 = 680, 960
    
    coords = [
        (col1_x1, row1_y1, col1_x2, row1_y2),
        (col2_x1, row1_y1, col2_x2, row1_y2),
        (col1_x1, row2_y1, col1_x2, row2_y2),
        (col2_x1, row2_y1, col2_x2, row2_y2),
    ]
    
    font_badge = get_font(26, bold=True)
    font_t = get_font(36, bold=True)
    font_d = get_font(26, bold=False)
    
    for c, (x1, y1, x2, y2) in zip(cards, coords):
        is_hl = (highlight_card == 0 or highlight_card == c["id"])
        accent = c["color"]
        
        bg_color = (20, 30, 52, 245) if is_hl else (12, 18, 30, 160)
        border_color = (accent[0], accent[1], accent[2], 230) if is_hl else (71, 85, 105, 80)
        
        draw.rounded_rectangle([x1, y1, x2, y2], radius=24, fill=bg_color, outline=border_color, width=3 if is_hl else 1)
        
        # Colored top-left tag
        draw.rounded_rectangle([x1 + 32, y1 + 35, x1 + 165, y1 + 78], radius=10, fill=(accent[0], accent[1], accent[2], 40), outline=(accent[0], accent[1], accent[2], 160), width=1)
        draw.text((x1 + 46, y1 + 43), f"#{c['badge']}", fill=accent, font=font_badge)
        
        # Draw custom high-tech vector graphic in top-right of card
        icon_cx, icon_cy = x2 - 55, y1 + 55
        if c["id"] == 1:
            # Gear / sync loop accent
            draw.ellipse([icon_cx - 18, icon_cy - 18, icon_cx + 18, icon_cy + 18], outline=accent, width=2)
            draw.ellipse([icon_cx - 6, icon_cy - 6, icon_cx + 6, icon_cy + 6], fill=accent)
        elif c["id"] == 2:
            # Data bars accent
            draw.line([(icon_cx - 16, icon_cy - 10), (icon_cx + 16, icon_cy - 10)], fill=accent, width=3)
            draw.line([(icon_cx - 16, icon_cy), (icon_cx + 8, icon_cy)], fill=accent, width=3)
            draw.line([(icon_cx - 16, icon_cy + 10), (icon_cx + 12, icon_cy + 10)], fill=accent, width=3)
        elif c["id"] == 3:
            # Camera / play frame accent
            draw.rounded_rectangle([icon_cx - 16, icon_cy - 14, icon_cx + 16, icon_cy + 14], radius=4, outline=accent, width=2)
            draw.polygon([(icon_cx - 4, icon_cy - 7), (icon_cx - 4, icon_cy + 7), (icon_cx + 7, icon_cy)], fill=accent)
        elif c["id"] == 4:
            # Equalizer waves accent
            for i, bh in enumerate([10, 22, 16, 26, 12]):
                bx = icon_cx - 16 + i * 8
                draw.line([(bx, icon_cy - bh // 2), (bx, icon_cy + bh // 2)], fill=accent, width=3)

        # Title & desc
        draw.text((x1 + 32, y1 + 115), c["title"], fill=(255, 255, 255) if is_hl else (148, 163, 184), font=font_t)
        draw.text((x1 + 32, y1 + 185), c["desc"], fill=(186, 230, 253) if is_hl else (100, 116, 139), font=font_d)

    img.paste(overlay, (0, 0), overlay)
    render_dynamic_caption(img, caption_text)
    return img

# =========================================================================
# COMPONENT 5: ComparisonScene (Dramatic Contrast: Red vs Green)
# =========================================================================
def render_comparison_scene(
    active_side: str = "all",
    caption_text: str = "",
    beat_idx: int = 0,
    total_beats: int = 10
) -> Image.Image:
    """Render side-by-side contrasting cards (Wrong approach vs Right approach) with active side focus."""
    img = draw_luxury_cyber_background(
        top_color=(18, 10, 16),
        bottom_color=(26, 14, 24),
        orb1_color=(239, 68, 68),
        orb2_color=(34, 197, 94)
    )
    render_top_header(img, "TƯ DUY SỬ DỤNG AI ĐÚNG ĐẮN", beat_idx, total_beats)
    
    overlay = Image.new("RGBA", (img.width, img.height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    font_tag = get_font(34, bold=True)
    font_item = get_font(36, bold=False)
    font_icon = get_font(24, bold=True)
    
    # Check side highlighting
    left_active = (active_side in ("left", "all"))
    right_active = (active_side in ("right", "all"))
    
    # 1. Left Card: The Mistake (Muted Crimson)
    lx1, lx2 = 70, 515
    y1, y2 = 360, 960
    l_bg = (38, 18, 24, 240) if left_active else (24, 12, 16, 150)
    l_border = (239, 68, 68, 230) if left_active else (239, 68, 68, 70)
    l_border_w = 4 if active_side == "left" else 2
    
    draw.rounded_rectangle([lx1, y1, lx2, y2], radius=24, fill=l_bg, outline=l_border, width=l_border_w)
    
    # Red Cross Icon Circle
    draw.ellipse([lx1 + 40, y1 + 42, lx1 + 80, y1 + 82], fill=(239, 68, 68))
    draw.text((lx1 + 52, y1 + 48), "X", fill=(255, 255, 255), font=font_icon)
    draw.text((lx1 + 95, y1 + 45), "[ SAI LẦM ]", fill=(239, 68, 68) if left_active else (248, 113, 113, 160), font=font_tag)
    draw.line([(lx1 + 40, y1 + 110), (lx2 - 40, y1 + 110)], fill=(239, 68, 68, 80), width=1)
    
    wrong_points = [
        ("Dùng quá nhiều", True),
        ("công cụ cùng lúc", False),
        ("Thủ công, rời rạc", True),
        ("Mất phương hướng", True),
        ("Lãng phí thời gian", True)
    ]
    curr_y = y1 + 150
    for text, has_icon in wrong_points:
        if has_icon:
            # Clean vector red cross
            ix = lx1 + 42
            iy = curr_y + 20
            draw.line([(ix - 7, iy - 7), (ix + 7, iy + 7)], fill=(239, 68, 68, 255) if left_active else (239, 68, 68, 110), width=3)
            draw.line([(ix - 7, iy + 7), (ix + 7, iy - 7)], fill=(239, 68, 68, 255) if left_active else (239, 68, 68, 110), width=3)
        text_x = lx1 + 62 if has_icon else lx1 + 62
        draw.text((text_x, curr_y), text, fill=(248, 113, 113) if left_active else (248, 113, 113, 130), font=font_item)
        curr_y += 65

    # 2. Right Card: The Right Way (Vibrant Neon Emerald)
    rx1, rx2 = 565, 1010
    r_bg = (18, 44, 34, 245) if right_active else (12, 28, 22, 150)
    r_border = (34, 197, 94, 240) if right_active else (34, 197, 94, 70)
    r_border_w = 4 if active_side == "right" else 2
    
    draw.rounded_rectangle([rx1, y1, rx2, y2], radius=24, fill=r_bg, outline=r_border, width=r_border_w)
    
    # Green Check Icon Circle
    draw.ellipse([rx1 + 40, y1 + 42, rx1 + 80, y1 + 82], fill=(34, 197, 94))
    draw.text((rx1 + 52, y1 + 48), "V", fill=(10, 30, 20), font=font_icon)
    draw.text((rx1 + 95, y1 + 45), "[ CHỌN ĐÚNG ]", fill=(34, 197, 94) if right_active else (187, 247, 208, 160), font=font_tag)
    draw.line([(rx1 + 40, y1 + 110), (rx2 - 40, y1 + 110)], fill=(34, 197, 94, 100), width=1)
    
    right_points = [
        ("1-2 công cụ chuẩn", True),
        ("cho đúng việc", False),
        ("Quy trình tinh gọn", True),
        ("Nắm vững câu lệnh", True),
        ("Năng suất bứt phá", True)
    ]
    curr_y = y1 + 150
    for text, has_icon in right_points:
        if has_icon:
            # Clean vector emerald checkmark
            ix = rx1 + 42
            iy = curr_y + 20
            draw.line([(ix - 8, iy), (ix - 2, iy + 7)], fill=(34, 197, 94, 255) if right_active else (34, 197, 94, 110), width=3)
            draw.line([(ix - 2, iy + 7), (ix + 9, iy - 6)], fill=(34, 197, 94, 255) if right_active else (34, 197, 94, 110), width=3)
        text_x = rx1 + 62 if has_icon else rx1 + 62
        draw.text((text_x, curr_y), text, fill=(187, 247, 208) if right_active else (187, 247, 208, 130), font=font_item)
        curr_y += 65

    img.paste(overlay, (0, 0), overlay)
    render_dynamic_caption(img, caption_text)
    return img

# =========================================================================
# COMPONENT 6: ImageScene (Generative AI Prompt & Waveform Art Canvas)
# =========================================================================
def render_image_scene(
    prompt_text: str = "Tạo nội dung, hình ảnh và giọng nói AI chân thực...",
    caption_text: str = "",
    beat_idx: int = 0,
    total_beats: int = 10
) -> Image.Image:
    """Render Generative AI canvas with prompt capsule and rich gradient audio waveform."""
    img = draw_luxury_cyber_background(
        top_color=(12, 10, 30),
        bottom_color=(22, 16, 50),
        orb1_color=(168, 85, 247),
        orb2_color=(236, 72, 153)
    )
    render_top_header(img, "SÁNG TẠO ĐA PHƯƠNG TIỆN", beat_idx, total_beats)
    
    overlay = Image.new("RGBA", (img.width, img.height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Prompt Bar at Top (y=360 to y=460)
    px1, py1 = 80, 360
    px2, py2 = 1000, 460
    draw.rounded_rectangle([px1, py1, px2, py2], radius=20, fill=(24, 30, 52, 235), outline=(168, 85, 247, 190), width=2)
    
    font_prompt = get_font(32, bold=False)
    draw.text((px1 + 35, py1 + 32), f"Prompt: \"{prompt_text[:38]}...\"", fill=(233, 213, 255), font=font_prompt)

    # Generated Art Frame (y=500 to y=980)
    fx1, fy1 = 80, 500
    fx2, fy2 = 1000, 980
    draw.rounded_rectangle([fx1, fy1, fx2, fy2], radius=28, fill=(18, 22, 44, 245), outline=(0, 240, 255, 210), width=3)
    
    mid_x = img.width // 2
    mid_y = (fy1 + fy2) // 2
    
    # Concentric glowing rings
    for r in [200, 140, 70]:
        draw.ellipse([mid_x - r, mid_y - r, mid_x + r, mid_y + r], outline=(0, 240, 255, 80), width=2)
        
    # Audio waveform bars with smooth rainbow gradient across center
    bar_x = mid_x - 280
    wave_heights = [24, 45, 75, 110, 85, 130, 95, 140, 115, 150, 120, 140, 90, 125, 80, 105, 65, 40, 25]
    for idx, bar_h in enumerate(wave_heights):
        by1 = mid_y - bar_h // 2
        by2 = mid_y + bar_h // 2
        # Color gradient: Cyan -> Purple -> Pink
        t = idx / len(wave_heights)
        cr = int(6 + t * (236 - 6))
        cg = int(182 - t * (182 - 72))
        cb = int(212 + t * (255 - 212))
        draw.rounded_rectangle([bar_x, by1, bar_x + 18, by2], radius=6, fill=(cr, cg, cb, 230))
        bar_x += 30

    # High-Tech Badges
    font_b = get_font(28, bold=True)
    draw.rounded_rectangle([fx1 + 40, fy2 - 70, fx1 + 220, fy2 - 25], radius=12, fill=(0, 240, 255, 40), outline=(0, 240, 255), width=1)
    draw.text((fx1 + 55, fy2 - 62), "4K ULTRA HD", fill=(0, 240, 255), font=font_b)

    draw.rounded_rectangle([fx2 - 240, fy2 - 70, fx2 - 40, fy2 - 25], radius=12, fill=(34, 197, 94, 40), outline=(34, 197, 94), width=1)
    draw.text((fx2 - 225, fy2 - 62), "GENERATED", fill=(34, 197, 94), font=font_b)

    img.paste(overlay, (0, 0), overlay)
    render_dynamic_caption(img, caption_text)
    return img

# =========================================================================
# COMPONENT 7: CTAScene (High Conversion Channel Branding & Follow)
# =========================================================================
def render_cta_scene(
    mode: str = "action",
    caption_text: str = "",
    beat_idx: int = 0,
    total_beats: int = 10
) -> Image.Image:
    """Render high-conversion call-to-action scene for AI Master channel with question & action modes."""
    img = draw_luxury_cyber_background(
        top_color=(12, 18, 36),
        bottom_color=(20, 32, 64),
        orb1_color=(239, 68, 68),
        orb2_color=(255, 223, 0)
    )
    
    # Auto-detect question mode if caption asks a question
    if "test" in caption_text.lower() or mode == "question":
        render_top_header(img, "CỘNG ĐỒNG AI MASTER", beat_idx, total_beats)
        overlay = Image.new("RGBA", (img.width, img.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Question Card (y=350 to y=980)
        qx1, qy1 = 80, 350
        qx2, qy2 = 1000, 980
        draw.rounded_rectangle([qx1, qy1, qx2, qy2], radius=32, fill=(18, 28, 52, 245), outline=(0, 240, 255, 220), width=3)
        
        font_q_tag = get_font(30, bold=True)
        font_q_title = get_font(52, bold=True)
        font_opt = get_font(34, bold=False)
        font_hint = get_font(36, bold=True)
        
        # Header Badge
        draw.rounded_rectangle([qx1 + 40, qy1 + 40, qx1 + 380, qy1 + 95], radius=14, fill=(255, 230, 0, 35), outline=(255, 230, 0), width=1)
        draw.text((qx1 + 56, qy1 + 50), "[ GÓC HỎI ĐÁP AI ]", fill=(255, 230, 0), font=font_q_tag)
        
        # Main Question
        draw.text((qx1 + 40, qy1 + 125), "BẠN MUỐN MÌNH TEST", fill=(255, 255, 255), font=font_q_title)
        draw.text((qx1 + 40, qy1 + 195), "CÔNG CỤ NÀO TIẾP THEO?", fill=(0, 240, 255), font=font_q_title)
        
        # Interactive Poll Options
        options = [
            "1. Tự động hóa công việc (n8n, Make)",
            "2. AI Tạo ảnh & Video (Midjourney, Runway)",
            "3. AI Viết lách & Lập trình (ChatGPT, Claude)"
        ]
        oy = qy1 + 295
        for opt in options:
            draw.rounded_rectangle([qx1 + 40, oy, qx2 - 40, oy + 75], radius=16, fill=(30, 41, 68, 220), outline=(100, 116, 139, 140), width=1)
            draw.text((qx1 + 65, oy + 18), opt, fill=(226, 232, 240), font=font_opt)
            oy += 95
            
        # Bottom Prompt Bar
        draw.rounded_rectangle([qx1 + 40, oy + 15, qx2 - 40, oy + 90], radius=18, fill=(239, 68, 68, 230), outline=(255, 255, 255), width=2)
        draw.text((qx1 + 80, oy + 32), ">> Comment tên công cụ bạn tò mò bên dưới!", fill=(255, 255, 255), font=font_hint)
        
        img.paste(overlay, (0, 0), overlay)
        render_dynamic_caption(img, caption_text)
        return img
        
    # Action Mode: Channel Follow & Resource Download
    render_top_header(img, "KÊNH CHÍNH THỨC", beat_idx, total_beats)
    overlay = Image.new("RGBA", (img.width, img.height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # 1. Main Channel Card (y=360 to y=640)
    cx1, cy1 = 80, 360
    cx2, cy2 = 1000, 640
    draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=32, fill=(18, 28, 52, 245), outline=(0, 240, 255, 220), width=3)
    
    font_brand = get_font(76, bold=True)
    font_sub = get_font(34, bold=False)
    
    brand_title = config.CHANNEL_NAME.upper()
    bbox_b = font_brand.getbbox(brand_title)
    bw = bbox_b[2] - bbox_b[0]
    draw.text(((img.width - bw) // 2, cy1 + 60), brand_title, fill=(255, 223, 0), font=font_brand)
    
    sub_title = "Kiến thức & Công cụ AI thực chiến mỗi ngày"
    bbox_s = font_sub.getbbox(sub_title)
    sw = bbox_s[2] - bbox_s[0]
    draw.text(((img.width - sw) // 2, cy1 + 160), sub_title, fill=(210, 225, 245), font=font_sub)

    # 2. Glowing Red Follow Button (y=700 to y=810)
    btn_x1, btn_y1 = 120, 700
    btn_x2, btn_y2 = 960, 810
    draw.rounded_rectangle([btn_x1, btn_y1, btn_x2, btn_y2], radius=28, fill=(239, 68, 68), outline=(255, 255, 255), width=2)
    
    font_btn = get_font(52, bold=True)
    btn_text = "[+] FOLLOW KÊNH NGAY"
    bb_btn = font_btn.getbbox(btn_text)
    btn_w = bb_btn[2] - bb_btn[0]
    draw.text(((img.width - btn_w) // 2, btn_y1 + 25), btn_text, fill=(255, 255, 255), font=font_btn)

    # 3. Comment Incentive Card (y=850 to y=980)
    com_x1, com_y1 = 120, 850
    com_x2, com_y2 = 960, 980
    draw.rounded_rectangle([com_x1, com_y1, com_x2, com_y2], radius=24, fill=(20, 32, 58, 235), outline=(0, 240, 255, 190), width=2)
    
    font_com = get_font(40, bold=True)
    com_text = ">> Comment \"AI\" để nhận tài liệu!"
    bb_com = font_com.getbbox(com_text)
    com_w = bb_com[2] - bb_com[0]
    draw.text(((img.width - com_w) // 2, com_y1 + 40), com_text, fill=(0, 240, 255), font=font_com)

    img.paste(overlay, (0, 0), overlay)
    render_dynamic_caption(img, caption_text)
    return img
