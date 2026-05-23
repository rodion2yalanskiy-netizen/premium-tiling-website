#!/usr/bin/env python3
"""
Generate 10 realistic stone/tile portfolio images for QSNera website.
Creates high-quality 2560x1920 PNG files with natural stone textures.
"""

import random
import math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "assets")
WIDTH, HEIGHT = 1920, 1280  # High-res but manageable size

def noise2d(x, y, seed=0):
    """Simple pseudo-random noise."""
    n = int(x) * 1619 + int(y) * 31337 + seed * 1013
    n = (n << 13) ^ n
    return ((n * (n * n * 60493 + 19990303) + 1376312589) & 0x7FFFFFFF) / 1073741824.0

def smooth_noise(x, y, seed=0):
    """Bicubic-ish smooth noise."""
    ix, iy = int(x), int(y)
    fx, fy = x - ix, y - iy
    # smoothstep
    fx = fx * fx * (3 - 2 * fx)
    fy = fy * fy * (3 - 2 * fy)
    n00 = noise2d(ix, iy, seed)
    n10 = noise2d(ix+1, iy, seed)
    n01 = noise2d(ix, iy+1, seed)
    n11 = noise2d(ix+1, iy+1, seed)
    return n00*(1-fx)*(1-fy) + n10*fx*(1-fy) + n01*(1-fx)*fy + n11*fx*fy

def turbulence(x, y, octaves=6, seed=0):
    """Multi-octave noise for marble/stone turbulence."""
    val = 0.0
    amp = 1.0
    freq = 1.0
    total_amp = 0.0
    for _ in range(octaves):
        val += smooth_noise(x * freq, y * freq, seed) * amp
        total_amp += amp
        amp *= 0.5
        freq *= 2.0
    return val / total_amp

def marble_vein(x, y, scale=4.0, seed=0):
    """Create marble vein pattern."""
    turb = turbulence(x/scale, y/scale, octaves=7, seed=seed)
    sine_val = math.sin(x/scale * 2.5 + turb * 8.0)
    return (sine_val + 1.0) / 2.0

def generate_image_from_pixels(width, height, pixel_func):
    """Generate image pixel by pixel using pixel_func(x, y) -> (r, g, b)."""
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            pixels[x, y] = pixel_func(x, y)
    return img

def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))

def lerp_color(c1, c2, t):
    t = max(0, min(1, t))
    return (
        clamp(c1[0] + (c2[0] - c1[0]) * t),
        clamp(c1[1] + (c2[1] - c1[1]) * t),
        clamp(c1[2] + (c2[2] - c1[2]) * t),
    )

def tri_lerp(c1, c2, c3, t):
    if t < 0.5:
        return lerp_color(c1, c2, t * 2)
    else:
        return lerp_color(c2, c3, (t - 0.5) * 2)

def add_lighting(img, ambient=0.85, light_x=0.7, light_y=0.3, intensity=0.25):
    """Add subtle directional lighting effect."""
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(ambient)
    draw = ImageDraw.Draw(img)
    w, h = img.size
    # Create a subtle radial gradient overlay
    overlay = Image.new('RGBA', (w, h), (0,0,0,0))
    d = ImageDraw.Draw(overlay)
    lx = int(w * light_x)
    ly = int(h * light_y)
    radius = max(w, h) * 0.8
    for r in range(int(radius), 0, -20):
        alpha = int(intensity * 255 * (1 - r/radius))
        d.ellipse([lx-r, ly-r, lx+r, ly+r], fill=(255,255,240,max(0,alpha)))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    return img

def apply_depth(img):
    """Add subtle emboss for stone depth texture."""
    return img.filter(ImageFilter.EMBOSS).convert('RGB')

def blend_emboss(original, strength=0.08):
    """Blend slight emboss with original for depth."""
    embossed = original.filter(ImageFilter.EMBOSS).convert('RGB')
    return Image.blend(original, embossed, strength)

# ─────────────────────────────────────────────────────────────────────
# 1. BOOKMATCHED MARBLE ENTRY HALL — White/grey marble, strong veins
# ─────────────────────────────────────────────────────────────────────
def gen_portfolio_5(w, h, seed=42):
    BASE = (240, 235, 230)
    VEIN1 = (160, 155, 150)
    VEIN2 = (90, 85, 82)
    HIGHLIGHT = (255, 252, 248)

    def px(x, y):
        v = marble_vein(x, y, scale=w/3.5, seed=seed)
        v2 = marble_vein(x, y, scale=w/7, seed=seed+7)
        t = v * 0.65 + v2 * 0.35
        # Bookmatched: mirror at center X
        mx = x if x < w//2 else w - x
        bm = marble_vein(mx, y, scale=w/4, seed=seed+1)
        t = t * 0.5 + bm * 0.5
        if t < 0.25:
            c = lerp_color(VEIN2, VEIN1, t / 0.25)
        elif t < 0.55:
            c = lerp_color(VEIN1, BASE, (t-0.25)/0.3)
        elif t < 0.85:
            c = lerp_color(BASE, HIGHLIGHT, (t-0.55)/0.3)
        else:
            c = HIGHLIGHT
        # grout line at center
        if abs(x - w//2) < 3:
            c = lerp_color(c, (180,178,175), 0.7)
        return c

    img = generate_image_from_pixels(w, h, px)
    img = blend_emboss(img, 0.07)
    img = add_lighting(img, 0.9, 0.35, 0.2, 0.2)
    return img

# ─────────────────────────────────────────────────────────────────────
# 2. ZELLIGE MOROCCAN KITCHEN — Colorful handmade ceramic tiles
# ─────────────────────────────────────────────────────────────────────
def gen_portfolio_6(w, h, seed=77):
    COLORS = [
        (28, 80, 110),   # deep teal
        (20, 60, 95),    # navy
        (35, 100, 125),  # cerulean
        (42, 120, 108),  # green-teal
        (16, 50, 80),    # dark blue
        (50, 135, 145),  # aqua
        (25, 70, 100),   # mid blue
    ]
    GROUT = (210, 205, 198)
    TILE_W = w // 18
    TILE_H = h // 14

    def px(x, y):
        tx = x // TILE_W
        ty = y // TILE_H
        bx = x % TILE_W
        by = y % TILE_H
        # grout gap
        if bx < 2 or by < 2 or bx >= TILE_W-2 or by >= TILE_H-2:
            return GROUT
        # pick tile color with noise
        rnd = random.Random(tx * 997 + ty * 1009 + seed)
        base_col = rnd.choice(COLORS)
        # slight variation per tile
        v = turbulence(tx * 0.3, ty * 0.3, 3, seed + tx + ty)
        var = int((v - 0.5) * 20)
        col = (clamp(base_col[0]+var), clamp(base_col[1]+var), clamp(base_col[2]+var))
        # surface imperfection: zellige is handmade, slightly rough
        n = turbulence(x/8.0, y/8.0, 4, seed+2) * 25 - 12
        col = (clamp(col[0]+n), clamp(col[1]+n), clamp(col[2]+n))
        # slight highlight top-left of each tile
        highlight = max(0, 1 - (bx/TILE_W * 2 + by/TILE_H)) * 30
        col = (clamp(col[0]+highlight), clamp(col[1]+highlight), clamp(col[2]+highlight))
        return col

    img = generate_image_from_pixels(w, h, px)
    img = add_lighting(img, 0.88, 0.4, 0.25, 0.18)
    return img

# ─────────────────────────────────────────────────────────────────────
# 3. LARGE-FORMAT PORCELAIN LIVING — Greige/warm stone porcelain slabs
# ─────────────────────────────────────────────────────────────────────
def gen_portfolio_7(w, h, seed=33):
    BASE = (195, 188, 178)
    LIGHT = (220, 215, 208)
    DARK = (145, 138, 130)
    VEIN = (160, 152, 143)
    # Large tiles: 2 columns, 3 rows
    TILE_W = w // 2
    TILE_H = h // 3
    GROUT_W = 3

    def px(x, y):
        tx = x // TILE_W
        ty = y // TILE_H
        bx = x % TILE_W
        by = y % TILE_H
        if bx < GROUT_W or by < GROUT_W or bx >= TILE_W-GROUT_W or by >= TILE_H-GROUT_W:
            return (188, 183, 176)
        # stone texture within each tile
        t = marble_vein(x, y, scale=w/2.5, seed=seed + tx*3 + ty*7)
        t2 = turbulence(x/(w/6), y/(h/6), 5, seed + tx + ty)
        t = t * 0.6 + t2 * 0.4
        c = tri_lerp(DARK, BASE, LIGHT, t)
        # fine linear pattern (porcelain veining)
        v2 = marble_vein(x, y, scale=w/8, seed=seed+5)
        if v2 < 0.18:
            c = lerp_color(c, VEIN, 0.4)
        return c

    img = generate_image_from_pixels(w, h, px)
    img = blend_emboss(img, 0.05)
    img = add_lighting(img, 0.9, 0.6, 0.15, 0.15)
    return img

# ─────────────────────────────────────────────────────────────────────
# 4. HERRINGBONE TRAVERTINE TERRACE — Warm beige with fossils & pores
# ─────────────────────────────────────────────────────────────────────
def gen_portfolio_8(w, h, seed=55):
    BASE  = (210, 195, 168)
    LIGHT = (235, 220, 195)
    DARK  = (168, 150, 125)
    PORE  = (140, 128, 108)
    TILE  = 90   # tile unit size
    GROUT = (200, 188, 170)
    GROUT_W = 3

    def px(x, y):
        # Herringbone pattern: alternate horizontal/vertical tiles
        # Use a herringbone grid
        col_unit = TILE * 2
        row_unit = TILE
        # Determine which herringbone cell
        cx = x // col_unit
        cy = y // row_unit
        lx = x % col_unit
        ly = y % row_unit
        if cy % 2 == 0:
            # top row: horizontal tile | vertical tile
            if lx < TILE:
                tx, ty = cx*2, cy//2
                bx, by = lx, ly
                tile_w, tile_h = TILE, row_unit
            else:
                tx, ty = cx*2+1, cy//2
                bx, by = lx - TILE, ly
                tile_w, tile_h = TILE, row_unit
        else:
            if lx < TILE:
                tx, ty = cx*2+10, cy//2+100
                bx, by = lx, ly
                tile_w, tile_h = TILE, row_unit
            else:
                tx, ty = cx*2+11, cy//2+100
                bx, by = lx - TILE, ly
                tile_w, tile_h = TILE, row_unit
        if bx < GROUT_W or by < GROUT_W or bx >= tile_w-GROUT_W or by >= tile_h-GROUT_W:
            return (188, 175, 155)
        t = turbulence(x/55.0, y/55.0, 6, seed + tx + ty*7)
        c = tri_lerp(DARK, BASE, LIGHT, t)
        # pores
        pore = turbulence(x/4.0, y/4.0, 2, seed+11)
        if pore > 0.82:
            c = lerp_color(c, PORE, 0.5)
        return c

    img = generate_image_from_pixels(w, h, px)
    img = blend_emboss(img, 0.1)
    img = add_lighting(img, 0.88, 0.25, 0.3, 0.22)
    return img

# ─────────────────────────────────────────────────────────────────────
# 5. CALACATTA GOLD MASTER BATH — Bright white, dramatic gold veins
# ─────────────────────────────────────────────────────────────────────
def gen_portfolio_9(w, h, seed=91):
    BASE      = (248, 245, 240)
    VEIN_GOLD = (210, 170, 90)
    VEIN_GREY = (180, 175, 168)
    CREAM     = (255, 252, 245)

    def px(x, y):
        t = marble_vein(x, y, scale=w/2.2, seed=seed)
        t2 = marble_vein(x, y, scale=w/6, seed=seed+3)
        combined = t * 0.7 + t2 * 0.3
        # Gold vein threshold
        if combined < 0.12:
            c = VEIN_GOLD
        elif combined < 0.22:
            c = lerp_color(VEIN_GOLD, VEIN_GREY, (combined-0.12)/0.1)
        elif combined < 0.38:
            c = lerp_color(VEIN_GREY, BASE, (combined-0.22)/0.16)
        elif combined > 0.88:
            c = CREAM
        else:
            c = lerp_color(BASE, CREAM, (combined-0.38)/0.5)
        # subtle noise
        n = turbulence(x/30.0, y/30.0, 3, seed+20) * 10 - 5
        c = (clamp(c[0]+n), clamp(c[1]+n), clamp(c[2]+n))
        return c

    img = generate_image_from_pixels(w, h, px)
    img = blend_emboss(img, 0.04)
    img = add_lighting(img, 0.92, 0.7, 0.2, 0.15)
    return img

# ─────────────────────────────────────────────────────────────────────
# 6. SLATE FEATURE WALL — Dark grey, natural cleavage planes
# ─────────────────────────────────────────────────────────────────────
def gen_portfolio_10(w, h, seed=17):
    BASE  = (65, 70, 72)
    LIGHT = (95, 100, 102)
    DARK  = (38, 42, 45)
    SHINE = (110, 115, 118)

    def px(x, y):
        # Horizontal layering + turbulence for slate cleavage
        layer = (y / h) + turbulence(x/60.0, y/40.0, 5, seed) * 0.3
        t = turbulence(x/35.0, y/20.0, 7, seed+1) * 0.7 + layer * 0.3
        c = tri_lerp(DARK, BASE, LIGHT, t)
        # Shiny mineral flecks
        fleck = turbulence(x/3.0, y/3.0, 2, seed+5)
        if fleck > 0.87:
            c = lerp_color(c, SHINE, 0.6)
        return c

    img = generate_image_from_pixels(w, h, px)
    img = blend_emboss(img, 0.15)
    img = add_lighting(img, 0.85, 0.5, 0.3, 0.2)
    return img

# ─────────────────────────────────────────────────────────────────────
# 7. VENETIAN MOSAIC POOL DECK — Blue/aqua small mosaic tiles
# ─────────────────────────────────────────────────────────────────────
def gen_portfolio_11(w, h, seed=63):
    COLORS = [
        (0, 105, 148),    # deep pool blue
        (0, 130, 175),    # medium blue
        (0, 155, 196),    # bright blue
        (15, 170, 175),   # aqua
        (30, 145, 160),   # teal
        (5, 120, 165),    # cobalt
        (45, 180, 190),   # bright aqua
        (0, 90, 135),     # dark blue
    ]
    GROUT = (220, 218, 215)
    TILE_SIZE = 28
    GROUT_W = 2

    def px(x, y):
        tx = x // TILE_SIZE
        ty = y // TILE_SIZE
        bx = x % TILE_SIZE
        by = y % TILE_SIZE
        if bx < GROUT_W or by < GROUT_W or bx >= TILE_SIZE-GROUT_W or by >= TILE_SIZE-GROUT_W:
            return GROUT
        rnd = random.Random(tx * 881 + ty * 773 + seed)
        base = rnd.choice(COLORS)
        n = turbulence(x/6.0, y/6.0, 3, seed+tx+ty) * 22 - 11
        c = (clamp(base[0]+n), clamp(base[1]+n), clamp(base[2]+n))
        # highlight each tile top-left
        hl = max(0, (1 - bx/TILE_SIZE) * (1 - by/TILE_SIZE)) * 40
        c = (clamp(c[0]+hl), clamp(c[1]+hl), clamp(c[2]+hl))
        return c

    img = generate_image_from_pixels(w, h, px)
    img = add_lighting(img, 0.9, 0.45, 0.2, 0.2)
    return img

# ─────────────────────────────────────────────────────────────────────
# 8. STATUARIO MARBLE KITCHEN ISLAND — Bright white, bold grey veins
# ─────────────────────────────────────────────────────────────────────
def gen_portfolio_12(w, h, seed=29):
    BASE  = (252, 250, 248)
    VEIN1 = (175, 170, 165)
    VEIN2 = (110, 105, 102)
    WHITE = (255, 255, 253)

    def px(x, y):
        t = marble_vein(x, y, scale=w/3, seed=seed)
        t2 = marble_vein(x, y, scale=w/9, seed=seed+4)
        v = t * 0.6 + t2 * 0.4
        if v < 0.15:
            c = lerp_color(VEIN2, VEIN1, v/0.15)
        elif v < 0.3:
            c = lerp_color(VEIN1, BASE, (v-0.15)/0.15)
        else:
            c = lerp_color(BASE, WHITE, (v-0.3)/0.7)
        n = smooth_noise(x/20.0, y/20.0, seed+99) * 8 - 4
        c = (clamp(c[0]+n), clamp(c[1]+n), clamp(c[2]+n))
        return c

    img = generate_image_from_pixels(w, h, px)
    img = blend_emboss(img, 0.04)
    img = add_lighting(img, 0.93, 0.6, 0.2, 0.12)
    return img

# ─────────────────────────────────────────────────────────────────────
# 9. BLACK ONYX BATHROOM ACCENT — Deep black with purple/blue shimmer
# ─────────────────────────────────────────────────────────────────────
def gen_portfolio_13(w, h, seed=88):
    BASE   = (18, 15, 22)
    VEIN1  = (55, 45, 75)
    VEIN2  = (80, 60, 110)
    SHINE  = (120, 100, 160)
    PURPLE = (35, 28, 55)

    def px(x, y):
        t = marble_vein(x, y, scale=w/3.5, seed=seed)
        t2 = turbulence(x/(w/5), y/(h/5), 6, seed+2)
        v = t * 0.5 + t2 * 0.5
        if v < 0.2:
            c = lerp_color(BASE, PURPLE, v/0.2)
        elif v < 0.45:
            c = lerp_color(PURPLE, VEIN1, (v-0.2)/0.25)
        elif v < 0.7:
            c = lerp_color(VEIN1, VEIN2, (v-0.45)/0.25)
        else:
            c = lerp_color(VEIN2, SHINE, (v-0.7)/0.3)
        # iridescent flecks
        fl = turbulence(x/4.0, y/4.0, 2, seed+9)
        if fl > 0.86:
            c = lerp_color(c, SHINE, 0.5)
        return c

    img = generate_image_from_pixels(w, h, px)
    img = blend_emboss(img, 0.12)
    img = add_lighting(img, 0.82, 0.55, 0.25, 0.3)
    return img

# ─────────────────────────────────────────────────────────────────────
# 10. TERRAZZO COMMERCIAL LOBBY — Speckled multi-color chips in matrix
# ─────────────────────────────────────────────────────────────────────
def gen_portfolio_14(w, h, seed=44):
    BASE_COLOR = (228, 222, 215)
    CHIPS = [
        (80, 75, 70),     # dark grey chip
        (200, 190, 175),  # light beige chip
        (140, 130, 120),  # mid grey
        (185, 160, 130),  # warm tan
        (100, 95, 90),    # charcoal
        (210, 200, 185),  # cream chip
        (160, 148, 135),  # taupe
        (220, 215, 205),  # off-white
    ]
    TILE_W = w // 3
    TILE_H = h // 2
    GROUT = (180, 175, 170)
    GROUT_W = 4

    def px(x, y):
        # Grout lines for large tiles
        tx = x % TILE_W
        ty = y % TILE_H
        if tx < GROUT_W or ty < GROUT_W or tx >= TILE_W-GROUT_W or ty >= TILE_H-GROUT_W:
            return GROUT
        # Background terrazzo matrix
        t = turbulence(x/40.0, y/40.0, 4, seed) * 15 - 7
        base = (clamp(BASE_COLOR[0]+t), clamp(BASE_COLOR[1]+t), clamp(BASE_COLOR[2]+t))
        # Scattered chips using noise thresholding
        chip_n = turbulence(x/7.0, y/7.0, 2, seed+1)
        if chip_n > 0.72:
            # Pick chip color based on position
            rnd = random.Random(int(x/5) * 503 + int(y/5) * 701 + seed)
            chip = rnd.choice(CHIPS)
            # Chip edge: blend
            edge = turbulence(x/3.0, y/3.0, 2, seed+2)
            alpha = min(1.0, (chip_n - 0.72) / 0.08)
            base = lerp_color(base, chip, alpha)
        return base

    img = generate_image_from_pixels(w, h, px)
    img = blend_emboss(img, 0.08)
    img = add_lighting(img, 0.9, 0.4, 0.2, 0.15)
    return img

if __name__ == '__main__':
    generators = [
        (5,  "Bookmatched Marble Entry Hall",      gen_portfolio_5),
        (6,  "Zellige Moroccan Kitchen",            gen_portfolio_6),
        (7,  "Large-Format Porcelain Living",       gen_portfolio_7),
        (8,  "Herringbone Travertine Terrace",      gen_portfolio_8),
        (9,  "Calacatta Gold Master Bath",          gen_portfolio_9),
        (10, "Slate Feature Wall",                  gen_portfolio_10),
        (11, "Venetian Mosaic Pool Deck",           gen_portfolio_11),
        (12, "Statuario Marble Kitchen Island",     gen_portfolio_12),
        (13, "Black Onyx Bathroom Accent",          gen_portfolio_13),
        (14, "Terrazzo Commercial Lobby",           gen_portfolio_14),
    ]

    # Use smaller size for faster generation, still high quality for web
    W, H = 960, 640

    print(f"Generating {len(generators)} portfolio images ({W}x{H})...")
    for num, title, fn in generators:
        fname = f"portfolio-{num}.png"
        path = os.path.join(OUTPUT_DIR, fname)
        print(f"  [{num-4}/{len(generators)}] {fname} — {title} ...", end='', flush=True)
        img = fn(W, H)
        img.save(path, 'PNG', optimize=True)
        size_kb = os.path.getsize(path) // 1024
        print(f" {size_kb}KB ✓")

    print("\n✅ All 10 portfolio images generated successfully!")
