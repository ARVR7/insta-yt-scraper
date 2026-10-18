"""Reusable scene engine for the 'Man Who Walked Into the Amazon' Shorts series.
Parallax jungle strips, silhouette walkers, envelope, counter/badge UI.  Part scripts import this."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render as R
from render import SS, W, H, FPS, text, stamp, over, ease, lerp, clamp, smooth, radial_sprite, paste_sprite, VIG

LW = 3800
GROUND_Y = 1430
GLOW_O = radial_sprite((255, 150, 50))
GLOW_B = radial_sprite((120, 150, 255))
GLOW_Y = radial_sprite((230, 255, 120), 128, 2.4)

# ------------------------------------------------------------------ primitives
def trunk(P, x, wb, wt, ytop, ybot, col, lean=0.0):
    P.append(('poly', [(x - wb / 2, ybot), (x + wb / 2, ybot), (x + lean + wt / 2, ytop), (x + lean - wt / 2, ytop)], col))
    for s in (-1, 1):   # buttress roots
        P.append(('poly', [(x + s * wb * 0.5, ybot), (x + s * wb * 1.1, ybot), (x + s * wb * 0.42, ybot - wb * 1.6)], col))

def blob(P, x, y, r, col, rng, n=8):
    for _ in range(n):
        a = rng.uniform(0, 6.28); d = rng.uniform(0, r * 0.7)
        rr = rng.uniform(r * 0.35, r * 0.7)
        cx, cy = x + math.cos(a) * d, y + math.sin(a) * d * 0.6
        P.append(('ell', [cx - rr, cy - rr * 0.7, cx + rr, cy + rr * 0.7], col))

def vine(P, x, y0, length, col, rng, w=5):
    pts = []
    ph = rng.uniform(0, 6.28); amp = rng.uniform(8, 26)
    for i in range(21):
        u = i / 20
        pts.append((x + amp * math.sin(ph + u * 5) * u, y0 + length * u))
    P.append(('line', pts, col, w))
    for i in range(3, 21, 3):
        px, py = pts[i]
        s = rng.choice([-1, 1])
        P.append(('ell', [px - 4 + s * 12, py - 8, px + 14 + s * 12, py + 8], col))

def frond(P, x, y, length, ang, col, wid=0.16, droop=0.5):
    pts_l, pts_r = [], []
    for i in range(15):
        u = i / 14
        px = x + math.cos(ang) * length * u
        py = y + math.sin(ang) * length * u + droop * length * u * u
        w = length * wid * math.sin(math.pi * min(1, u * 1.05)) ** 0.8
        nx, ny = -math.sin(ang), math.cos(ang)
        pts_l.append((px + nx * w, py + ny * w)); pts_r.append((px - nx * w, py - ny * w))
    P.append(('poly', pts_l + pts_r[::-1], col))

def fern(P, x, y, size, col, rng, n=7):
    for k in range(n):
        ang = -math.pi / 2 + rng.uniform(-1.2, 1.2)
        frond(P, x, y, size * rng.uniform(0.6, 1.1), ang, col, 0.13, 0.6)

def make_strip(P, width=LW, chunk=1200):
    strip = Image.new('RGBA', (width, H), (0, 0, 0, 0))
    for x0 in range(0, width, chunk):
        cw = min(chunk, width - x0)
        im = Image.new('RGBA', (cw * 2, H * 2), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for p in P:
            k = p[0]
            tf = lambda pt: ((pt[0] - x0) * 2, pt[1] * 2)
            if k == 'poly': d.polygon([tf(q) for q in p[1]], fill=p[2])
            elif k == 'ell':
                b = p[1]; d.ellipse([(b[0] - x0) * 2, b[1] * 2, (b[2] - x0) * 2, b[3] * 2], fill=p[2])
            elif k == 'line': d.line([tf(q) for q in p[1]], fill=p[2], width=int(p[3] * 2), joint='curve')
        strip.paste(im.resize((cw, H), Image.LANCZOS), (x0, 0))
    return strip

def build_layers():
    rng = np.random.RandomState(21)
    L = {}
    # far
    P = []
    x = -60
    while x < LW:
        trunk(P, x, rng.uniform(24, 40), rng.uniform(16, 26), -50, 1380, (30, 38, 84, 255), rng.uniform(-20, 20))
        x += rng.uniform(110, 190)
    for hx in range(0, LW, 260):
        blob(P, hx + rng.uniform(-40, 40), rng.uniform(260, 420), 170, (28, 36, 80, 255), rng)
    P.append(('poly', [(0, 1400), (0, 1210)] + [(i, 1210 - 70 * abs(math.sin(i / 380.0)) - 30 * math.sin(i / 90.0)) for i in range(0, LW, 40)] + [(LW, 1400)], (24, 32, 72, 255)))
    L['far'] = (make_strip(P), 0.12)
    # mid
    P = []; x = 0
    while x < LW:
        w = rng.uniform(50, 84)
        trunk(P, x, w, w * 0.6, -50, 1440, (16, 22, 56, 255), rng.uniform(-30, 30))
        for _ in range(rng.randint(1, 3)):
            vine(P, x + rng.uniform(-200, 200), rng.uniform(200, 420), rng.uniform(200, 520), (16, 24, 58, 255), rng, 5)
        fern(P, x + rng.uniform(-120, 120), 1440, rng.uniform(140, 220), (14, 22, 54, 255), rng)
        x += rng.uniform(230, 340)
    for hx in range(0, LW, 300):
        blob(P, hx + rng.uniform(-60, 60), rng.uniform(150, 300), 200, (14, 20, 52, 255), rng)
    L['mid'] = (make_strip(P), 0.30)
    # near
    P = []; x = 100
    while x < LW:
        w = rng.uniform(95, 140)
        trunk(P, x, w, w * 0.62, -50, 1470, (9, 12, 34, 255), rng.uniform(-30, 30))
        for _ in range(2):
            fy = rng.uniform(900, 1300)
            frond(P, x + w * 0.3, fy, rng.uniform(160, 260), rng.uniform(-0.4, 0.4), (9, 12, 34, 255), 0.12, 0.7)
            frond(P, x - w * 0.3, fy + 30, rng.uniform(160, 260), math.pi + rng.uniform(-0.4, 0.4), (9, 12, 34, 255), 0.12, 0.7)
        x += rng.uniform(430, 620)
    L['near'] = (make_strip(P), 0.55)
    # ground (moves with the walkers)
    P = []
    P.append(('poly', [(0, GROUND_Y - 20)] + [(i, GROUND_Y - 20 - 10 * math.sin(i / 70.0)) for i in range(0, LW, 40)] + [(LW, GROUND_Y - 20), (LW, H), (0, H)], (14, 10, 24, 255)))
    P.append(('poly', [(0, GROUND_Y + 8), (LW, GROUND_Y + 8), (LW, GROUND_Y + 80), (0, GROUND_Y + 80)], (44, 34, 54, 255)))
    P.append(('poly', [(0, GROUND_Y + 80), (LW, GROUND_Y + 80), (LW, H), (0, H)], (7, 5, 14, 255)))
    for _ in range(260):
        gx = rng.uniform(0, LW); gy = rng.uniform(GROUND_Y + 14, GROUND_Y + 110)
        P.append(('ell', [gx, gy, gx + rng.uniform(10, 34), gy + rng.uniform(4, 9)], (30, 22, 40, 255)))
    L['ground'] = (make_strip(P), 1.0)
    # foreground (in front of walkers)
    P = []
    P.append(('poly', [(0, GROUND_Y + 120)] + [(i, GROUND_Y + 120 - 14 * abs(math.sin(i / 55.0))) for i in range(0, LW, 30)] + [(LW, GROUND_Y + 120), (LW, H), (0, H)], (4, 3, 10, 255)))
    x = 0
    while x < LW:
        fern(P, x + rng.uniform(-60, 60), GROUND_Y + 130, rng.uniform(150, 260), (4, 3, 10, 255), rng, 9)
        x += rng.uniform(200, 380)
    x = 1000
    while x < LW:
        w = rng.uniform(190, 260)
        trunk(P, x, w, w * 0.7, -50, 1920, (3, 3, 9, 255), rng.uniform(-20, 20))
        x += rng.uniform(1200, 1700)
    L['fg'] = (make_strip(P), 1.5)
    # overhead canopy
    P = []
    for hx in range(-100, LW, 170):
        blob(P, hx, rng.uniform(40, 150), 170, (4, 6, 20, 255), rng, 6)
        vine(P, hx + rng.uniform(-60, 60), 120, rng.uniform(140, 460), (4, 6, 20, 255), rng, 6)
        frond(P, hx, 120, rng.uniform(200, 320), math.pi / 2 + rng.uniform(-0.9, 0.9), (4, 6, 20, 255), 0.12, 0.2)
    L['canopy'] = (make_strip(P), 0.8)
    return L

def make_bg():
    rows = np.arange(H, dtype=np.float32)
    ys = [0, 500, 1000, 1300, 1440, 1920]
    cs = np.array([(3, 4, 14), (8, 12, 36), (20, 30, 76), (38, 54, 108), (26, 22, 52), (10, 8, 20)], np.float32)
    col = np.stack([np.interp(rows, ys, cs[:, k]) for k in range(3)], axis=1).astype(np.uint8)
    im = Image.fromarray(np.ascontiguousarray(np.broadcast_to(col[:, None, :], (H, W, 3))), 'RGB').convert('RGBA')
    paste_sprite(im, GLOW_B, 830, 640, 640, 0.35)
    d = ImageDraw.Draw(im)
    d.ellipse([770, 580, 890, 700], fill=(236, 238, 214, 255))
    for cx_, cy_, r_ in ((808, 622, 14), (856, 660, 18), (842, 600, 9)):
        d.ellipse([cx_ - r_, cy_ - r_, cx_ + r_, cy_ + r_], fill=(205, 208, 184, 255))
    srng = np.random.RandomState(4)
    for _ in range(70):
        sx, sy, sr = srng.uniform(0, W), srng.uniform(200, 900), srng.uniform(1, 2.6)
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 235, int(srng.uniform(90, 220))))
    return im

LAYERS = build_layers()
BG = make_bg()
FIRE = [(np.random.RandomState(i).uniform(60, 1020), np.random.RandomState(i + 50).uniform(900, 1380),
         np.random.RandomState(i + 90).uniform(0, 6.28), np.random.RandomState(i + 130).uniform(0.4, 1.0)) for i in range(26)]

def layer_crop(name, cam_s):
    strip, f = LAYERS[name]
    off = int(min(LW - W, max(0, cam_s * f)))
    return strip.crop((off, 0, off + W, H))

# ------------------------------------------------------------------ people
def person(d, x, gy, h, kind, phase, alpha=1.0, rim=0.35, mark=False):
    """silhouette at supersampled canvas d, feet at (x, gy) in 1x px"""
    k = SS
    col = (8, 6, 18, int(255 * alpha))
    rimc = (255, 150, 60, int(255 * alpha * rim))
    bob = abs(math.sin(phase)) * h * 0.02
    sw = math.sin(phase)
    def pts(plist, ox=0):
        return [((x + ox + px * h) * k, (gy - bob * h / h - py * h) * k) for px, py in plist]
    legs = []
    for s in (1, -1):
        a = sw * 0.45 * s
        hip = (0.0 + 0.0, 0.46)
        kx = hip[0] + math.sin(a) * 0.26; ky = hip[1] - math.cos(a) * 0.26
        fx = kx + math.sin(a * 0.4 - 0.05 * s) * 0.24; fy = max(0.0, ky - 0.26)
        legs.append([(hip[0] - 0.045, hip[1]), (hip[0] + 0.045, hip[1]), (kx + 0.04, ky), (fx + 0.07, fy), (fx - 0.04, fy), (kx - 0.04, ky)])
    arms = []
    for s in (-1, 1):
        a = sw * 0.5 * s
        sh = (0.0, 0.76)
        ex = sh[0] + math.sin(a) * 0.22; ey = sh[1] - math.cos(a) * 0.22
        arms.append([(sh[0] - 0.04, sh[1]), (sh[0] + 0.04, sh[1]), (ex + 0.035, ey), (ex - 0.035, ey)])
    torso = [(-0.10, 0.46), (0.10, 0.46), (0.11, 0.78), (0.0, 0.82), (-0.11, 0.78)]
    parts = legs + [torso] + arms
    if kind == 'r':   # big backpack
        parts.append([(-0.20, 0.50), (-0.08, 0.50), (-0.08, 0.80), (-0.20, 0.78)])
    if kind == 'f':   # walking stick
        parts.append([(0.20, 0.0), (0.22, 0.0), (0.12 + 0.02 * sw, 0.66), (0.10 + 0.02 * sw, 0.66)])
        parts.append([(-0.17, 0.52), (-0.07, 0.52), (-0.07, 0.80), (-0.17, 0.78)])
    for off, c in ((-3, rimc), (0, col)):
        for pl in parts:
            d.polygon(pts(pl, off / h), fill=c)
        hx, hy = x + off, gy - bob - 0.89 * h
        r = 0.065 * h
        d.ellipse([(hx - r) * k, (hy - r) * k, (hx + r) * k, (hy + r) * k], fill=c)
        if kind == 'f':   # pith helmet
            d.pieslice([(hx - r * 1.35) * k, (hy - r * 1.55) * k, (hx + r * 1.35) * k, (hy + r * 1.05) * k], 180, 360, fill=c)
            d.rectangle([(hx - r * 1.7) * k, (hy - r * 0.35) * k, (hx + r * 1.7) * k, (hy - r * 0.05) * k], fill=c)
        elif kind == 'j':  # cap
            d.pieslice([(hx - r * 1.1) * k, (hy - r * 1.3) * k, (hx + r * 1.1) * k, (hy + r * 0.9) * k], 180, 360, fill=c)
            d.rectangle([(hx - r * 0.2) * k, (hy - r * 0.3) * k, (hx + r * 1.7) * k, (hy - r * 0.05) * k], fill=c)
        else:              # wide hat
            d.pieslice([(hx - r * 1.2) * k, (hy - r * 1.5) * k, (hx + r * 1.2) * k, (hy + r * 0.8) * k], 180, 360, fill=c)
            d.rectangle([(hx - r * 1.8) * k, (hy - r * 0.35) * k, (hx + r * 1.8) * k, (hy - r * 0.1) * k], fill=c)
    if mark:
        tx, ty = x, gy - 1.18 * h
        d.polygon([((tx - 22) * k, (ty - 30) * k), ((tx + 22) * k, (ty - 30) * k), (tx * k, ty * k)], fill=(255, 214, 60, int(255 * alpha)))

# ------------------------------------------------------------------ envelope
def make_envelope():
    w, h = 400, 270
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=14, fill=(236, 224, 192, 255), outline=(120, 90, 50, 255), width=5)
    d.line([(8, 8), (w / 2, h * 0.58), (w - 8, 8)], fill=(150, 120, 80, 255), width=5)
    d.line([(8, h - 8), (w * 0.38, h * 0.5)], fill=(190, 165, 120, 255), width=3)
    d.line([(w - 8, h - 8), (w * 0.62, h * 0.5)], fill=(190, 165, 120, 255), width=3)
    d.ellipse([w / 2 - 38, h * 0.58 - 38, w / 2 + 38, h * 0.58 + 38], fill=(168, 30, 36, 255), outline=(110, 14, 20, 255), width=5)
    d.ellipse([w / 2 - 20, h * 0.58 - 20, w / 2 + 20, h * 0.58 + 20], outline=(220, 90, 90, 255), width=3)
    d.text((w - 28, h - 40), "1925", font=R.font(40), fill=(120, 30, 30, 255), anchor='rm')
    return im

ENVELOPE = make_envelope()
_nz = np.random.RandomState(9).rand(27, 40).astype(np.float32)
NOISE = np.asarray(Image.fromarray((_nz * 255).astype(np.uint8)).resize((400, 270), Image.BICUBIC), np.float32) / 255.0
EDGE = np.minimum(np.minimum(np.arange(400)[None, :], 399 - np.arange(400)[None, :]), np.minimum(np.arange(270)[:, None], 269 - np.arange(270)[:, None])).astype(np.float32) / 135.0
BURN_FIELD = np.clip(NOISE * 0.6 + (1 - EDGE) * 0.5, 0, 1)

def burnt_envelope(u):
    """u 0..1 burn progress; returns RGBA image"""
    arr = np.asarray(ENVELOPE, np.uint8).copy()
    f = BURN_FIELD
    thresh = 1 - u * 1.25 + 0.0
    alive = f < thresh - 0.0
    edge = (f >= thresh - 0.10) & (f < thresh)
    a = arr[..., 3].astype(np.float32) * alive
    arr[..., 3] = a.astype(np.uint8)
    arr[edge, 0], arr[edge, 1], arr[edge, 2] = 255, 140, 30
    char = (f >= thresh - 0.22) & (f < thresh - 0.10)
    arr[char, 0], arr[char, 1], arr[char, 2] = 30, 18, 12
    return Image.fromarray(arr, 'RGBA')

# ------------------------------------------------------------------ UI
def badge(d, n, total):
    pw = 300
    d.rounded_rectangle([(540 - pw / 2) * SS, 205 * SS, (540 + pw / 2) * SS, 262 * SS], radius=29 * SS,
                        fill=(10, 4, 20, 225), outline=(255, 150, 40, 255), width=4 * SS)
    text(d, (540, 234), f"PART {n}/{total}", 38, (255, 255, 255, 255))

def counter(d, t, val, label, red=False):
    col = (255, 70, 80, 255) if red else (255, 255, 255, 255)
    cx, cy = 540, 345
    d.rounded_rectangle([(cx - 300) * SS, (cy - 62) * SS, (cx + 300) * SS, (cy + 62) * SS], radius=34 * SS,
                        fill=(4, 6, 24, 215), outline=col, width=6 * SS)
    text(d, (cx, cy - 8), val, 78, col, mono=True)
    text(d, (cx, cy + 41), label, 28, (200, 210, 255, 230))

def pill(d, cx, cy, w, h, label, size, fill=(255, 214, 60), pulse=0.0):
    d.rounded_rectangle([(cx - w / 2) * SS, (cy - h / 2) * SS, (cx + w / 2) * SS, (cy + h / 2) * SS], radius=int(h / 2) * SS,
                        fill=fill + (int(215 + 40 * pulse),), outline=(0, 0, 0, 255), width=5 * SS)
    text(d, (cx, cy + 2), label, size, (10, 6, 24, 255))

def gray_post(arr, gray):
    g = arr[..., 0:1] * 0.3 + arr[..., 1:2] * 0.59 + arr[..., 2:3] * 0.11
    arr = arr * (1 - gray) + g * gray
    return (arr - 128) * (1 + 0.18 * gray) + 128
