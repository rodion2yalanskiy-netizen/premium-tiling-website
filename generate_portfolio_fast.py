#!/usr/bin/env python3
"""
Fast vectorized portfolio image generator for QSNera website.
Uses NumPy for high-performance texture generation.
Generates portfolio-5.png through portfolio-14.png
"""

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import os, sys

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
W, H = 960, 640  # High quality for web, manageable size

# ─── Core noise functions (vectorized) ────────────────────────────────────────

def smooth_noise_arr(x_arr, y_arr, seed=0):
    """Vectorized value noise."""
    ix = np.floor(x_arr).astype(np.int64)
    iy = np.floor(y_arr).astype(np.int64)
    fx = x_arr - ix
    fy = y_arr - iy
    # smoothstep
    fx = fx * fx * (3 - 2 * fx)
    fy = fy * fy * (3 - 2 * fy)

    def hash_val(gx, gy):
        n = (gx * 1619 + gy * 31337 + seed * 1013).astype(np.int64)
        n = (n << 13) ^ n
        return ((n * (n * n * np.int64(60493) + np.int64(19990303)) + np.int64(1376312589)) & np.int64(0x7FFFFFFF)) / 1073741824.0

    n00 = hash_val(ix,   iy)
    n10 = hash_val(ix+1, iy)
    n01 = hash_val(ix,   iy+1)
    n11 = hash_val(ix+1, iy+1)
    return (n00*(1-fx)*(1-fy) + n10*fx*(1-fy) +
            n01*(1-fx)*fy      + n11*fx*fy)

def turbulence_arr(x_arr, y_arr, octaves=6, seed=0):
    """Vectorized multi-octave noise."""
    out = np.zeros_like(x_arr)
    amp, freq, total = 1.0, 1.0, 0.0
    for _ in range(octaves):
        out += smooth_noise_arr(x_arr * freq, y_arr * freq, seed) * amp
        total += amp
        amp  *= 0.5
        freq *= 2.0
    return out / total

def marble_vein_arr(x_arr, y_arr, scale=4.0, seed=0):
    """Marble vein pattern."""
    turb = turbulence_arr(x_arr/scale, y_arr/scale, octaves=7, seed=seed)
    sine = np.sin(x_arr/scale * 2.5 + turb * 8.0)
    return (sine + 1.0) / 2.0

def lerp_rgb(c1, c2, t):
    """Vectorized color lerp. t is a 2D array [0,1]."""
    t = np.clip(t, 0, 1)
    t3 = t[:,:,np.newaxis]
    return (np.array(c1) * (1-t3) + np.array(c2) * t3).astype(np.uint8)

def tri_lerp_rgb(c1, c2, c3, t):
    """Vectorized 3-point lerp."""
    t = np.clip(t, 0, 1)
    # t < 0.5: lerp c1->c2
    # t >= 0.5: lerp c2->c3
    t3 = t[:,:,np.newaxis]
    r1 = np.array(c1) * (1 - t3*2) + np.array(c2) * (t3*2)
    r2 = np.array(c2) * (1 - (t3-0.5)*2) + np.array(c3) * ((t3-0.5)*2)
    mask = (t >= 0.5)[:,:,np.newaxis]
    return np.clip(np.where(mask, r2, r1), 0, 255).astype(np.uint8)

def quad_lerp(c1, c2, c3, c4, t):
    """4-color piecewise lerp, thresholds at 0.33 and 0.66."""
    t = np.clip(t, 0, 1)
    t3 = t[:,:,np.newaxis]
    r12 = np.array(c1)*(1-t3/0.33) + np.array(c2)*(t3/0.33)
    r23 = np.array(c2)*(1-(t3-0.33)/0.33) + np.array(c3)*((t3-0.33)/0.33)
    r34 = np.array(c3)*(1-(t3-0.66)/0.34) + np.array(c4)*((t3-0.66)/0.34)
    out = np.where(t3 < 0.33, r12, np.where(t3 < 0.66, r23, r34))
    return np.clip(out, 0, 255).astype(np.uint8)

def add_lighting(arr_rgb, ambient=0.9, light_x_frac=0.65, light_y_frac=0.25, intensity=0.15):
    """Adds directional spotlight overlay."""
    h, w = arr_rgb.shape[:2]
    ys = np.linspace(0, 1, h)[:,np.newaxis]
    xs = np.linspace(0, 1, w)[np.newaxis,:]
    dist = np.sqrt((xs - light_x_frac)**2 + (ys - light_y_frac)**2)
    light = np.clip(1 - dist, 0, 1) * intensity
    out = arr_rgb.astype(np.float32) * ambient + light[:,:,np.newaxis] * 255
    return np.clip(out, 0, 255).astype(np.uint8)

def blend_emboss(img_pil, strength=0.07):
    """Blend emboss effect for stone depth."""
    em = img_pil.filter(ImageFilter.EMBOSS).convert('RGB')
    return Image.blend(img_pil, em, strength)

def to_img(arr):
    return Image.fromarray(arr.astype(np.uint8), 'RGB')

# Grid setup
xs = np.tile(np.arange(W, dtype=np.float32), (H, 1))
ys = np.tile(np.arange(H, dtype=np.float32)[:,np.newaxis], (1, W))

# ─── 1. BOOKMATCHED MARBLE ENTRY HALL ─────────────────────────────────────────
def gen_portfolio_5():
    print("  [1/10] portfolio-5.png — Bookmatched Marble Entry Hall ...", end='', flush=True)
    BASE = (240, 235, 230)
    VEIN1 = (160, 155, 150)
    VEIN2 = (90, 85, 82)
    HIGH = (255, 252, 248)

    t1 = marble_vein_arr(xs, ys, scale=W/3.5, seed=42)
    t2 = marble_vein_arr(xs, ys, scale=W/7, seed=49)
    # Bookmatched: mirror X
    mx = np.where(xs < W/2, xs, W-xs)
    bm = marble_vein_arr(mx, ys, scale=W/4, seed=43)
    t = (t1*0.3 + t2*0.2 + bm*0.5)
    t = np.clip(t, 0, 1)

    arr = quad_lerp(VEIN2, VEIN1, BASE, HIGH, t)
    # Grout center line
    mask = np.abs(xs - W//2) < 3
    arr[mask] = [180, 178, 175]

    img = to_img(arr)
    img = blend_emboss(img, 0.07)
    arr2 = add_lighting(np.array(img), 0.9, 0.35, 0.2, 0.2)
    return to_img(arr2)

# ─── 2. ZELLIGE MOROCCAN KITCHEN ──────────────────────────────────────────────
def gen_portfolio_6():
    print("  [2/10] portfolio-6.png — Zellige Moroccan Kitchen ...", end='', flush=True)
    GROUT = np.array([210, 205, 198])
    COLORS = [
        [28, 80, 110], [20, 60, 95], [35, 100, 125], [42, 120, 108],
        [16, 50, 80],  [50, 135, 145], [25, 70, 100],
    ]
    TILE_W = W // 18
    TILE_H = H // 14

    tx_arr = (xs // TILE_W).astype(np.int32)
    ty_arr = (ys // TILE_H).astype(np.int32)
    bx_arr = (xs % TILE_W).astype(np.int32)
    by_arr = (ys % TILE_H).astype(np.int32)

    is_grout = (bx_arr < 2) | (by_arr < 2) | (bx_arr >= TILE_W-2) | (by_arr >= TILE_H-2)

    # Assign tile colors deterministically
    color_idx = ((tx_arr * 997 + ty_arr * 1009 + 77) % len(COLORS))
    tile_colors = np.array(COLORS)[color_idx]  # H x W x 3

    # Surface variation noise
    n = turbulence_arr(xs/8.0, ys/8.0, 4, 79) * 24 - 12
    tile_colors = np.clip(tile_colors + n[:,:,np.newaxis], 0, 255).astype(np.uint8)

    # Highlight top-left of each tile
    bx_n = bx_arr / TILE_W
    by_n = by_arr / TILE_H
    hl = np.clip((1-bx_n)*(1-by_n) * 40, 0, 40)
    tile_colors = np.clip(tile_colors.astype(np.int32) + hl[:,:,np.newaxis].astype(np.int32), 0, 255).astype(np.uint8)

    arr = np.where(is_grout[:,:,np.newaxis], GROUT, tile_colors)
    arr2 = add_lighting(arr.astype(np.uint8), 0.88, 0.4, 0.25, 0.18)
    return to_img(arr2)

# ─── 3. LARGE-FORMAT PORCELAIN ────────────────────────────────────────────────
def gen_portfolio_7():
    print("  [3/10] portfolio-7.png — Large-Format Porcelain Living ...", end='', flush=True)
    BASE = (195, 188, 178)
    LIGHT = (220, 215, 208)
    DARK = (145, 138, 130)
    VEIN_C = (160, 152, 143)
    TILE_W_sz = W // 2
    TILE_H_sz = H // 3
    GW = 3
    GROUT_C = np.array([188, 183, 176])

    bx_a = (xs % TILE_W_sz).astype(np.int32)
    by_a = (ys % TILE_H_sz).astype(np.int32)
    is_grout = (bx_a < GW) | (by_a < GW) | (bx_a >= TILE_W_sz-GW) | (by_a >= TILE_H_sz-GW)

    t = marble_vein_arr(xs, ys, scale=W/2.5, seed=33)
    t2 = turbulence_arr(xs/(W/6), ys/(H/6), 5, 38)
    t = t * 0.6 + t2 * 0.4

    arr = tri_lerp_rgb(DARK, BASE, LIGHT, t)

    # veining
    v2 = marble_vein_arr(xs, ys, scale=W/8, seed=38)
    vein_mask = (v2 < 0.18)
    arr = np.where(vein_mask[:,:,np.newaxis],
                   lerp_rgb(VEIN_C, VEIN_C, np.zeros((H,W))),  # fallback
                   arr)
    # simpler: blend vein color
    vein_blend = np.clip(1 - v2/0.18, 0, 1) * 0.35
    arr = np.clip(arr.astype(np.float32) * (1-vein_blend[:,:,np.newaxis]) +
                  np.array(VEIN_C) * vein_blend[:,:,np.newaxis], 0, 255).astype(np.uint8)

    arr = np.where(is_grout[:,:,np.newaxis], GROUT_C, arr)
    img = blend_emboss(to_img(arr), 0.05)
    arr2 = add_lighting(np.array(img), 0.9, 0.6, 0.15, 0.15)
    return to_img(arr2)

# ─── 4. HERRINGBONE TRAVERTINE TERRACE ────────────────────────────────────────
def gen_portfolio_8():
    print("  [4/10] portfolio-8.png — Herringbone Travertine Terrace ...", end='', flush=True)
    BASE  = (210, 195, 168)
    LIGHT = (235, 220, 195)
    DARK  = (168, 150, 125)
    PORE  = (140, 128, 108)
    GROUT_C = np.array([190, 178, 158])
    TILE = 90

    # Herringbone: alternating H/V tiles
    col_u = TILE * 2
    cx_a = (xs // col_u).astype(np.int32)
    cy_a = (ys // TILE).astype(np.int32)
    lx_a = (xs % col_u).astype(np.int32)
    ly_a = (ys % TILE).astype(np.int32)

    # For each tile in the herringbone, compute grout edges
    GW = 3
    # Within sub-tile
    bx_sub = (lx_a % TILE).astype(np.int32)
    by_sub = ly_a
    is_grout = (bx_sub < GW) | (by_sub < GW) | (bx_sub >= TILE-GW) | (by_sub >= TILE-GW)

    t = turbulence_arr(xs/55.0, ys/55.0, 6, 55)
    arr = tri_lerp_rgb(DARK, BASE, LIGHT, t)

    # pores
    pore_n = turbulence_arr(xs/4.0, ys/4.0, 2, 66)
    pore_mask = pore_n > 0.82
    pore_blend = np.where(pore_mask, 0.5, 0.0)
    arr = np.clip(arr.astype(np.float32) * (1-pore_blend[:,:,np.newaxis]) +
                  np.array(PORE) * pore_blend[:,:,np.newaxis], 0, 255).astype(np.uint8)

    arr = np.where(is_grout[:,:,np.newaxis], GROUT_C, arr)
    img = blend_emboss(to_img(arr), 0.1)
    arr2 = add_lighting(np.array(img), 0.88, 0.25, 0.3, 0.22)
    return to_img(arr2)

# ─── 5. CALACATTA GOLD MASTER BATH ────────────────────────────────────────────
def gen_portfolio_9():
    print("  [5/10] portfolio-9.png — Calacatta Gold Master Bath ...", end='', flush=True)
    BASE = (248, 245, 240)
    GOLD = (210, 170, 90)
    GREY = (180, 175, 168)
    CREAM = (255, 252, 245)

    t1 = marble_vein_arr(xs, ys, scale=W/2.2, seed=91)
    t2 = marble_vein_arr(xs, ys, scale=W/6, seed=94)
    v = t1*0.7 + t2*0.3

    arr = quad_lerp(GOLD, GREY, BASE, CREAM, v)

    # Subtle texture noise
    n = turbulence_arr(xs/30.0, ys/30.0, 3, 111) * 10 - 5
    arr = np.clip(arr.astype(np.float32) + n[:,:,np.newaxis], 0, 255).astype(np.uint8)

    img = blend_emboss(to_img(arr), 0.04)
    arr2 = add_lighting(np.array(img), 0.92, 0.7, 0.2, 0.15)
    return to_img(arr2)

# ─── 6. SLATE FEATURE WALL ────────────────────────────────────────────────────
def gen_portfolio_10():
    print("  [6/10] portfolio-10.png — Slate Feature Wall ...", end='', flush=True)
    BASE  = (65, 70, 72)
    LIGHT = (95, 100, 102)
    DARK  = (38, 42, 45)
    SHINE = (110, 115, 118)

    layer = ys/H + turbulence_arr(xs/60.0, ys/40.0, 5, 17) * 0.3
    t = turbulence_arr(xs/35.0, ys/20.0, 7, 18) * 0.7 + layer * 0.3
    t = np.clip(t, 0, 1)

    arr = tri_lerp_rgb(DARK, BASE, LIGHT, t)

    # Mineral flecks
    fl = turbulence_arr(xs/3.0, ys/3.0, 2, 22)
    fleck_mask = fl > 0.87
    fl_blend = np.where(fleck_mask, 0.6, 0.0)
    arr = np.clip(arr.astype(np.float32)*(1-fl_blend[:,:,np.newaxis]) +
                  np.array(SHINE) * fl_blend[:,:,np.newaxis], 0, 255).astype(np.uint8)

    img = blend_emboss(to_img(arr), 0.15)
    arr2 = add_lighting(np.array(img), 0.85, 0.5, 0.3, 0.2)
    return to_img(arr2)

# ─── 7. VENETIAN MOSAIC POOL DECK ─────────────────────────────────────────────
def gen_portfolio_11():
    print("  [7/10] portfolio-11.png — Venetian Mosaic Pool Deck ...", end='', flush=True)
    GROUT_C = np.array([220, 218, 215])
    COLORS = [
        [0, 105, 148], [0, 130, 175], [0, 155, 196], [15, 170, 175],
        [30, 145, 160], [5, 120, 165], [45, 180, 190], [0, 90, 135],
    ]
    TILE_SIZE = 28
    GW = 2

    tx_a = (xs // TILE_SIZE).astype(np.int32)
    ty_a = (ys // TILE_SIZE).astype(np.int32)
    bx_a = (xs % TILE_SIZE).astype(np.int32)
    by_a = (ys % TILE_SIZE).astype(np.int32)
    is_grout = (bx_a < GW) | (by_a < GW) | (bx_a >= TILE_SIZE-GW) | (by_a >= TILE_SIZE-GW)

    color_idx = ((tx_a * 881 + ty_a * 773 + 63) % len(COLORS))
    tile_colors = np.array(COLORS)[color_idx]

    n = turbulence_arr(xs/6.0, ys/6.0, 3, 65) * 22 - 11
    tile_colors = np.clip(tile_colors.astype(np.float32) + n[:,:,np.newaxis], 0, 255).astype(np.uint8)

    bx_n = bx_a / TILE_SIZE
    by_n = by_a / TILE_SIZE
    hl = np.clip((1-bx_n)*(1-by_n) * 40, 0, 40)
    tile_colors = np.clip(tile_colors.astype(np.int32) + hl[:,:,np.newaxis].astype(np.int32), 0, 255).astype(np.uint8)

    arr = np.where(is_grout[:,:,np.newaxis], GROUT_C, tile_colors)
    arr2 = add_lighting(arr.astype(np.uint8), 0.9, 0.45, 0.2, 0.2)
    return to_img(arr2)

# ─── 8. STATUARIO MARBLE KITCHEN ISLAND ───────────────────────────────────────
def gen_portfolio_12():
    print("  [8/10] portfolio-12.png — Statuario Marble Kitchen Island ...", end='', flush=True)
    BASE  = (252, 250, 248)
    VEIN1 = (175, 170, 165)
    VEIN2 = (110, 105, 102)
    WHITE = (255, 255, 253)

    t1 = marble_vein_arr(xs, ys, scale=W/3, seed=29)
    t2 = marble_vein_arr(xs, ys, scale=W/9, seed=33)
    v = t1*0.6 + t2*0.4

    arr = quad_lerp(VEIN2, VEIN1, BASE, WHITE, v)

    n = smooth_noise_arr(xs/20.0, ys/20.0, 199) * 8 - 4
    arr = np.clip(arr.astype(np.float32) + n[:,:,np.newaxis], 0, 255).astype(np.uint8)

    img = blend_emboss(to_img(arr), 0.04)
    arr2 = add_lighting(np.array(img), 0.93, 0.6, 0.2, 0.12)
    return to_img(arr2)

# ─── 9. BLACK ONYX BATHROOM ACCENT ────────────────────────────────────────────
def gen_portfolio_13():
    print("  [9/10] portfolio-13.png — Black Onyx Bathroom Accent ...", end='', flush=True)
    BASE   = (18, 15, 22)
    VEIN1  = (55, 45, 75)
    VEIN2  = (80, 60, 110)
    SHINE  = (120, 100, 160)
    PURPLE = (35, 28, 55)

    t1 = marble_vein_arr(xs, ys, scale=W/3.5, seed=88)
    t2 = turbulence_arr(xs/(W/5), ys/(H/5), 6, 90)
    v = t1*0.5 + t2*0.5

    arr = quad_lerp(BASE, PURPLE, VEIN1, VEIN2, v)

    # Shimmer at high values
    shimmer = np.clip((v - 0.75) / 0.25, 0, 1) * 0.5
    arr = np.clip(arr.astype(np.float32)*(1-shimmer[:,:,np.newaxis]) +
                  np.array(SHINE) * shimmer[:,:,np.newaxis], 0, 255).astype(np.uint8)

    fl = turbulence_arr(xs/4.0, ys/4.0, 2, 95)
    fl_b = np.where(fl > 0.86, 0.5, 0.0)
    arr = np.clip(arr.astype(np.float32)*(1-fl_b[:,:,np.newaxis]) +
                  np.array(SHINE) * fl_b[:,:,np.newaxis], 0, 255).astype(np.uint8)

    img = blend_emboss(to_img(arr), 0.12)
    arr2 = add_lighting(np.array(img), 0.82, 0.55, 0.25, 0.3)
    return to_img(arr2)

# ─── 10. TERRAZZO COMMERCIAL LOBBY ────────────────────────────────────────────
def gen_portfolio_14():
    print("  [10/10] portfolio-14.png — Terrazzo Commercial Lobby ...", end='', flush=True)
    BASE_C = (228, 222, 215)
    CHIPS = [
        [80, 75, 70], [200, 190, 175], [140, 130, 120], [185, 160, 130],
        [100, 95, 90], [210, 200, 185], [160, 148, 135], [220, 215, 205],
    ]
    TILE_W_sz = W // 3
    TILE_H_sz = H // 2
    GROUT_C = np.array([180, 175, 170])
    GW = 4

    bx_a = (xs % TILE_W_sz).astype(np.int32)
    by_a = (ys % TILE_H_sz).astype(np.int32)
    is_grout = (bx_a < GW) | (by_a < GW) | (bx_a >= TILE_W_sz-GW) | (by_a >= TILE_H_sz-GW)

    # Base matrix with slight noise
    n = turbulence_arr(xs/40.0, ys/40.0, 4, 44) * 14 - 7
    base = np.clip(np.array(BASE_C) + n[:,:,np.newaxis], 0, 255)

    # Chip layer
    chip_n = turbulence_arr(xs/7.0, ys/7.0, 2, 45)
    chip_idx = ((xs//5).astype(np.int32) * 503 + (ys//5).astype(np.int32) * 701 + 44) % len(CHIPS)
    chip_colors = np.array(CHIPS)[chip_idx]
    chip_blend = np.clip((chip_n - 0.72) / 0.08, 0, 1)
    base = base * (1 - chip_blend[:,:,np.newaxis]) + chip_colors * chip_blend[:,:,np.newaxis]

    arr = np.where(is_grout[:,:,np.newaxis], GROUT_C, base).astype(np.uint8)
    img = blend_emboss(to_img(arr), 0.08)
    arr2 = add_lighting(np.array(img), 0.9, 0.4, 0.2, 0.15)
    return to_img(arr2)


# ─── SKIP ALREADY GENERATED ───────────────────────────────────────────────────
GENERATORS = [
    (5,  gen_portfolio_5),
    (6,  gen_portfolio_6),
    (7,  gen_portfolio_7),
    (8,  gen_portfolio_8),
    (9,  gen_portfolio_9),
    (10, gen_portfolio_10),
    (11, gen_portfolio_11),
    (12, gen_portfolio_12),
    (13, gen_portfolio_13),
    (14, gen_portfolio_14),
]

if __name__ == '__main__':
    print(f"Generating portfolio images ({W}×{H}) with NumPy...")
    for num, fn in GENERATORS:
        path = os.path.join(OUTPUT_DIR, f"portfolio-{num}.png")
        if os.path.exists(path):
            size_kb = os.path.getsize(path) // 1024
            print(f"  [skip] portfolio-{num}.png already exists ({size_kb}KB)")
            continue
        img = fn()
        img.save(path, 'PNG', optimize=True)
        size_kb = os.path.getsize(path) // 1024
        print(f" {size_kb}KB ✓")
    print("\n✅ All portfolio images ready!")
