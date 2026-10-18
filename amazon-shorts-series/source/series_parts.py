"""Data-driven renderer for Parts 2-10 (Part 1 has its own script). Usage:
   python3 series_parts.py test N t1 t2 ...     -> PNG frames
   python3 series_parts.py full N out.mp4       -> silent video
"""
import sys, math, time, subprocess, datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import series_engine as E
import render as R
from series_engine import *

DUR_ = 17.0
TOTAL = 10
BPM = 130.0; B = 60 / BPM; G0 = 12.0 - 24 * B
DAYS = (datetime.date(2026, 10, 18) - datetime.date(1925, 5, 29)).days   # days since the last letter [VERIFY date]
WHITE = (255, 255, 255, 255); YEL = (255, 214, 60, 255); RED = (255, 70, 80, 255); CYAN = (80, 235, 255, 255)

def new_dyn():
    im = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
def comp(base, dyn):
    return Image.alpha_composite(base, dyn.reduce(SS))
def P_(x, y): return (x * SS, y * SS)

def fit_stamp(layer, s, cx, cy, size, rot, fill, stroke, scale=1.0, maxw=900):
    f = R.font(int(size * SS)); w = f.getlength(s) / SS
    if w > maxw: size = size * maxw / w
    stamp(layer, s, cx, cy, size, rot, fill, stroke, scale=scale)

# ------------------------------------------------------------------ backdrops
def jungle(t, sc=0.0, dim=0.0, people=None, fire=None, fireflies=True, extra_pre=None):
    base = E.BG.copy()
    for nm in ('far', 'mid'): base = Image.alpha_composite(base, layer_crop(nm, sc))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    for i in range(4):
        xt = 120 + 270 * i + 14 * math.sin(t * 0.7 + i); fl = 9 + 5 * math.sin(t * 1.3 + i * 2)
        sd.polygon([(xt, 260), (xt + 90, 260), (xt + 40 - 160 + 170, GROUND_Y), (xt - 180, GROUND_Y)], fill=(170, 195, 255, int(fl)))
    base = Image.alpha_composite(base, sh)
    base = Image.alpha_composite(base, layer_crop('near', sc))
    base = Image.alpha_composite(base, layer_crop('ground', sc))
    if fire is not None: paste_sprite(base, E.GLOW_O, fire[0], fire[1] - 80, 1100 * fire[2], 0.75 * fire[2])
    if extra_pre: base = extra_pre(base)
    if people:
        dyn, dd = new_dyn(); people(dd); base = comp(base, dyn)
    base = Image.alpha_composite(base, layer_crop('fg', sc))
    base = Image.alpha_composite(base, layer_crop('canopy', sc))
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fg)
    for i in range(7):
        fx = (i * 230 + t * (18 + 10 * (i % 2))) % 1700 - 300; fy = GROUND_Y - 30 + (i % 3) * 22
        fd.ellipse([fx - 330, fy - 46, fx + 330, fy + 46], fill=(150, 170, 230, 22))
    base = Image.alpha_composite(base, fg)
    if fireflies:
        for fx, fy, ph, sp in E.FIRE:
            al = 0.5 + 0.5 * math.sin(t * 2.6 * sp + ph)
            paste_sprite(base, E.GLOW_Y, fx + 40 * math.sin(t * 0.5 * sp + ph), fy + 30 * math.cos(t * 0.7 * sp + ph), 30, al * 0.9)
    if dim > 0: base = Image.alpha_composite(base, Image.new('RGBA', (W, H), (2, 3, 12, int(255 * dim))))
    return base

# ------------------------------------------------------------------ sprites
_cache = {}
def parchment(w=760, h=420):
    k = ('parch', w, h)
    if k in _cache: return _cache[k]
    rng = np.random.RandomState(5); S = 2
    im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = []
    for i in range(60):
        pts.append((i / 60 * w, rng.uniform(0, 14)))
    for i in range(30): pts.append((w - rng.uniform(0, 14), i / 30 * h))
    for i in range(60): pts.append((w - i / 60 * w, h - rng.uniform(0, 14)))
    for i in range(30): pts.append((rng.uniform(0, 14), h - i / 30 * h))
    d.polygon([(x * S, y * S) for x, y in pts], fill=(232, 216, 178, 255), outline=(110, 74, 34, 255))
    st = Image.new('RGBA', im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    for _ in range(26):
        x, y, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(20, 90)
        sd.ellipse([(x - r) * S, (y - r * 0.7) * S, (x + r) * S, (y + r * 0.7) * S], fill=(170, 130, 70, 22))
    sd.rectangle([0, 0, w * S, 10 * S], fill=(120, 80, 40, 90)); sd.rectangle([0, (h - 10) * S, w * S, h * S], fill=(120, 80, 40, 90))
    st.putalpha(ImageChops.multiply(st.getchannel('A'), im.getchannel('A')))
    im = Image.alpha_composite(im, st)
    im = im.resize((w, h), Image.LANCZOS); _cache[k] = im; return im

def paste_rot(base, spr, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    s = spr.rotate(rot, resample=Image.BICUBIC, expand=True) if rot else spr
    if scale != 1.0: s = s.resize((max(2, int(s.width * scale)), max(2, int(s.height * scale))), Image.BICUBIC)
    if alpha < 1.0:
        a = s.getchannel('A').point(lambda v: int(v * alpha)); s = s.copy(); s.putalpha(a)
    base.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))

def news_card(head, sub):
    k = ('news', head)
    if k in _cache: return _cache[k]
    w, h = 560, 400
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=10, fill=(226, 222, 208, 255), outline=(60, 56, 50, 255), width=5)
    d.rectangle([0, 0, w, 70], fill=(30, 28, 26, 255)); d.text((w / 2, 36), "THE DAILY NEWS", font=R.font(40), fill=(236, 232, 218, 255), anchor='mm')
    f = R.font(int(88 if len(head) < 10 else 62)); d.text((w / 2, 160), head, font=f, fill=(24, 20, 18, 255), anchor='mm')
    d.text((w / 2, 232), sub, font=R.font(30), fill=(110, 40, 36, 255), anchor='mm')
    for i in range(5): d.rectangle([40, 280 + i * 22, w - 40 - (i % 3) * 60, 290 + i * 22], fill=(150, 146, 134, 255))
    _cache[k] = im; return im

def crate(open_amt=0.0, shake=0.0):
    w, h = 640, 700
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    bx0, by0, bx1, by1 = 100, 360, 540, 640
    d.rectangle([bx0, by0, bx1, by1], fill=(112, 74, 38, 255), outline=(40, 24, 10, 255), width=6)
    for i in range(1, 4): d.line([bx0, by0 + i * 70, bx1, by0 + i * 70], fill=(60, 38, 18, 255), width=4)
    for x in (bx0, bx1 - 40): d.rectangle([x, by0, x + 40, by1], fill=(60, 64, 80, 255), outline=(20, 22, 30, 255), width=3)
    if open_amt > 0:   # dark opening + glow
        d.rectangle([bx0 + 10, by0 - 6, bx1 - 10, by0 + 24], fill=(2, 2, 8, 255))
    lid = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ld = ImageDraw.Draw(lid)
    ld.rectangle([bx0 - 8, by0 - 40, bx1 + 8, by0], fill=(130, 88, 46, 255), outline=(40, 24, 10, 255), width=6)
    ld.rectangle([bx0 + 40, by0 - 34, bx0 + 90, by0 - 6], fill=(60, 64, 80, 255)); ld.rectangle([bx1 - 90, by0 - 34, bx1 - 40, by0 - 6], fill=(60, 64, 80, 255))
    ang = open_amt * 78
    lid = lid.rotate(ang, resample=Image.BICUBIC, center=(bx0 - 8, by0 - 0))
    im.alpha_composite(lid)
    return im

def skull(d, cx, cy, s, col=(236, 232, 214, 255), dark=(8, 8, 18, 255)):
    k = SS
    d.ellipse([(cx - 0.5 * s) * k, (cy - 0.55 * s) * k, (cx + 0.5 * s) * k, (cy + 0.35 * s) * k], fill=col)
    d.rounded_rectangle([(cx - 0.32 * s) * k, (cy + 0.1 * s) * k, (cx + 0.32 * s) * k, (cy + 0.55 * s) * k], radius=int(0.1 * s * k), fill=col)
    for sx in (-1, 1):
        d.ellipse([(cx + sx * 0.2 * s - 0.14 * s) * k, (cy - 0.15 * s) * k, (cx + sx * 0.2 * s + 0.14 * s) * k, (cy + 0.13 * s) * k], fill=dark)
    d.polygon([P_(cx, cy + 0.02 * s), P_(cx - 0.06 * s, cy + 0.17 * s), P_(cx + 0.06 * s, cy + 0.17 * s)], fill=dark)
    for i in range(-2, 3): d.line([P_(cx + i * 0.11 * s, cy + 0.36 * s), P_(cx + i * 0.11 * s, cy + 0.55 * s)], fill=dark, width=max(2, int(0.025 * s * k)))

def bone(d, x0, y0, x1, y1, s, col=(236, 232, 214, 255)):
    k = SS
    d.line([P_(x0, y0), P_(x1, y1)], fill=col, width=int(0.09 * s * k))
    for (x, y) in ((x0, y0), (x1, y1)):
        for o in (-0.06, 0.06):
            ang = math.atan2(y1 - y0, x1 - x0) + math.pi / 2
            px, py = x + math.cos(ang) * o * s * 1.4, y + math.sin(ang) * o * s * 1.4
            d.ellipse([(px - 0.07 * s) * k, (py - 0.07 * s) * k, (px + 0.07 * s) * k, (py + 0.07 * s) * k], fill=col)

def seated(d, x, y, s, hat=True, alpha=255):
    k = SS; c = (8, 6, 18, alpha); rim = (255, 150, 60, int(alpha * 0.4))
    for off, col in ((-3, rim), (0, c)):
        d.pieslice([(x + off - 0.28 * s) * k, (y - 0.5 * s) * k, (x + off + 0.28 * s) * k, (y + 0.3 * s) * k], 180, 360, fill=col)
        d.rectangle([(x + off - 0.28 * s) * k, (y - 0.1 * s) * k, (x + off + 0.28 * s) * k, (y + 0.3 * s) * k], fill=col)
        d.ellipse([(x + off - 0.11 * s) * k, (y - 0.72 * s) * k, (x + off + 0.11 * s) * k, (y - 0.5 * s) * k], fill=col)
        if hat:
            d.pieslice([(x + off - 0.15 * s) * k, (y - 0.82 * s) * k, (x + off + 0.15 * s) * k, (y - 0.56 * s) * k], 180, 360, fill=col)
            d.rectangle([(x + off - 0.2 * s) * k, (y - 0.69 * s) * k, (x + off + 0.2 * s) * k, (y - 0.65 * s) * k], fill=col)

def flames(base, cx, cy, t, size=1.0):
    paste_sprite(base, E.GLOW_O, cx, cy - 90 * size, 700 * size, 0.8)
    dyn, d = new_dyn()
    for col, sc_ in (((255, 70, 20, 255), 1.0), ((255, 150, 30, 255), 0.72), ((255, 225, 110, 255), 0.45)):
        for j in range(5):
            ph = j * 1.7 + sc_ * 3
            fx = cx + (j - 2) * 22 * size * sc_ + 8 * math.sin(t * 9 + ph)
            hgt = (150 + 60 * math.sin(t * 11 + ph)) * sc_ * size * (1 - abs(j - 2) * 0.18)
            wd = 34 * sc_ * size
            d.polygon([P_(fx - wd, cy), P_(fx - wd * 0.6, cy - hgt * 0.5), P_(fx + 6 * math.sin(t * 13 + ph), cy - hgt), P_(fx + wd * 0.6, cy - hgt * 0.5), P_(fx + wd, cy)], fill=col)
    d.polygon([P_(cx - 130 * size, cy + 14), P_(cx + 130 * size, cy - 4), P_(cx + 130 * size, cy + 22), P_(cx - 130 * size, cy + 36)], fill=(46, 28, 16, 255))
    return comp(base, dyn)

# ------------------------------------------------------------------ map
SA = [(-77, 8), (-72, 12), (-67, 10.5), (-62, 10.5), (-60, 8), (-57, 6), (-52, 5), (-50, 1), (-48, -1), (-44, -2.5), (-40, -3), (-35, -5), (-35, -9),
      (-39, -13), (-39, -18), (-41, -22), (-45, -24), (-48, -26), (-49, -29), (-53, -34), (-57, -35), (-57, -38), (-62, -39), (-65, -41), (-65, -45),
      (-67, -47), (-69, -51), (-68, -54), (-71, -54), (-74, -50), (-75, -46), (-73, -40), (-72, -33), (-71, -28), (-70, -20), (-71, -17), (-76, -14),
      (-79, -8), (-81, -5), (-80, -2), (-78, 2)]
ROUTE = [(-68, -16.5), (-65.5, -14.8), (-63, -14.0), (-60.5, -12.8), (-58, -12.4), (-55.5, -11.2), (-53.5, -10.6), (-51.5, -10.2)]
def proj(lon, lat): return (270 + (lon + 82) / 48 * 540, 640 + (14 - lat) / 70 * 790)

def map_scene(t, prog, pulse=True, gray=False):
    base = jungle(t, 40.0 + 6 * t, dim=0.55)
    dyn, d = new_dyn(); layer = dyn
    d.rounded_rectangle([P_(240, 620)[0], P_(240, 620)[1], P_(840, 1450)[0], P_(840, 1450)[1]], radius=36 * SS, fill=(6, 18, 40, 190), outline=(80, 235, 255, 200), width=4 * SS)
    for i in range(1, 12):
        x = 240 + i * 50; d.line([P_(x, 625), P_(x, 1445)], fill=(80, 235, 255, 22), width=SS)
    for j in range(1, 16):
        y = 620 + j * 52; d.line([P_(245, y), P_(835, y)], fill=(80, 235, 255, 22), width=SS)
    pts = [P_(*proj(*p)) for p in SA]
    d.polygon(pts, fill=(20, 62, 108, 235), outline=(80, 235, 255, 255))
    d.line(pts + [pts[0]], fill=(120, 245, 255, 255), width=3 * SS)
    text(d, proj(-66, -9), "BOLIVIA", 24, (170, 220, 255, 150)); text(d, proj(-52, -4), "BRAZIL", 30, (170, 220, 255, 150))
    # route
    n = len(ROUTE) - 1; seg = prog * n
    for i in range(n):
        a = ROUTE[i]; b = ROUTE[i + 1]
        if seg > i:
            u = min(1.0, seg - i); e = (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
            d.line([P_(*proj(*a)), P_(*proj(*e))], fill=(255, 190, 60, 255), width=7 * SS)
            d.line([P_(*proj(*a)), P_(*proj(*e))], fill=(255, 235, 150, 255), width=3 * SS)
    for i, p in enumerate(ROUTE):
        if seg >= i:
            x, y = proj(*p); r = 9
            d.ellipse([P_(x - r, y - r), P_(x + r, y + r)], fill=(255, 214, 60, 255), outline=(10, 6, 24, 255), width=3 * SS)
    if prog > 0 and pulse:
        i = min(n - 1, int(seg)); u = min(1.0, seg - i) if seg < n else 1.0
        a = ROUTE[i]; b = ROUTE[i + 1]; hx, hy = proj(a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
        for k in range(3):
            v = ((t * 1.3 + k / 3) % 1.0); r = 10 + 46 * v
            d.ellipse([P_(hx - r, hy - r), P_(hx + r, hy + r)], outline=(255, 214, 60, int(220 * (1 - v))), width=3 * SS)
    return comp(base, dyn)

def z_scene(t):
    base = jungle(t, 90 + 6 * t, dim=0.62)
    dyn, d = new_dyn()
    cx, cy = 540, 1000
    for k in range(1, 12):
        pts = []
        for a in range(0, 361, 6):
            ar = math.radians(a)
            rr = (50 + 46 * k + 5 * math.sin(t * 0.8 + k)) * (1 + 0.09 * math.sin(3 * ar + k) + 0.05 * math.sin(5 * ar + 2 * k))
            pts.append(P_(cx + rr * math.cos(ar) * 1.05, cy + rr * math.sin(ar) * 0.78))
        d.line(pts, fill=(80, 235, 190, int(110 - 6 * k)), width=3 * SS)
    out = comp(base, dyn)
    fl = 0.75 + 0.25 * math.sin(t * 17) * (1 if int(t * 5) % 3 else 0.4)
    paste_sprite(out, E.GLOW_O, cx, cy, 700, 0.8 * fl)
    layer, ld = new_dyn()
    stamp(layer, "Z", cx, cy, 380, 0, (255, 190, 70, int(255 * fl)), 14, scale=over(t / 0.5) if t < 0.5 else 1.0, sfill=(80, 30, 0, 255))
    # expert bubbles
    names = [(300, 740, 6.2), (770, 780, 6.9), (320, 1180, 7.6), (770, 1160, 8.3)]
    for bx, by, ts_ in names:
        if t >= ts_:
            u = max(0.06, over((t - ts_) / 0.18))
            ld.rounded_rectangle([P_(bx - 140 * u, by - 56 * u)[0], P_(bx - 140 * u, by - 56 * u)[1], P_(bx + 140 * u, by + 56 * u)[0], P_(bx + 140 * u, by + 56 * u)[1]], radius=34 * SS,
                                 fill=(244, 244, 250, 235), outline=(10, 6, 24, 255), width=4 * SS)
            ld.polygon([P_(bx - 20, by + 54 * u), P_(bx + 30, by + 54 * u), P_(bx + (cx - bx) * 0.08, by + 100 * u)], fill=(244, 244, 250, 235))
            if u > 0.8: text(ld, (bx, by + 2), "IMPOSSIBLE", 40, (200, 30, 40, 255))
    return comp(out, layer)

# ------------------------------------------------------------------ payoff scenes (transparent overlays)
def pay_manuscript(u):
    lay, d = new_dyn()
    s = over(u / 0.2); sh = 12 * math.exp(-8 * u)
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    paste_sprite(img, E.GLOW_O, 540, 960, 1100, 0.45 * clamp(u / 0.3))
    paste_rot(img, parchment(780, 460), 540 + sh * math.sin(u * 90), 960 + sh * math.cos(u * 80), scale=max(0.01, s), rot=-3)
    d2 = ImageDraw.Draw(lay)
    stamp(lay, "MANUSCRIPT", 540, 880, 104, -3, (92, 52, 22, 255), 4, scale=over((u - 0.05) / 0.2), sfill=(236, 220, 180, 255))
    stamp(lay, "512", 540, 1030, 240, -3, (160, 30, 30, 255), 6, scale=over((u - 0.15) / 0.2), sfill=(236, 220, 180, 255))
    return Image.alpha_composite(img, lay.reduce(SS))

def pay_note(u, l1, l2):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    s = over(u / 0.2)
    paste_sprite(img, E.GLOW_O, 540, 960, 1100, 0.4 * clamp(u / 0.3))
    paste_rot(img, parchment(780, 460), 540, 960, scale=max(0.01, s), rot=2)
    lay, d = new_dyn()
    stamp(lay, l1, 540, 900, 62, 2, (92, 52, 22, 255), 3, scale=over((u - 0.1) / 0.2), sfill=(236, 220, 180, 255))
    stamp(lay, l2, 540, 1010, 70, 2, (160, 30, 30, 255), 3, scale=over((u - 0.25) / 0.2), sfill=(236, 220, 180, 255))
    return Image.alpha_composite(img, lay.reduce(SS))

def pay_skyline(u):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    rng = np.random.RandomState(8)
    grow = ease(clamp(u / 1.0)); vis = 1.0
    if u > 1.3: vis = 0.0 if (int(u * 14) % 2 == 0) else 0.5
    if u > 1.9: vis = 0.0
    paste_sprite(img, E.GLOW_O, 540, 1000, 1000, 0.5 * vis)
    lay, d = new_dyn()
    base_y = 1210
    for i in range(14):
        x = 150 + i * 56; wd = 46; h_ = (120 + rng.uniform(0, 330)) * (1 - abs(i - 6.5) / 14)
        h_ *= grow
        top = base_y - h_
        col = (14, 18, 42, int(255 * vis))
        d.polygon([P_(x, base_y), P_(x + wd, base_y), P_(x + wd - 6, top + 22), P_(x + wd / 2, top), P_(x + 6, top + 22)], fill=col, outline=(255, 190, 70, int(220 * vis)))
        for wy in range(int(top) + 40, base_y - 20, 40):
            if rng.rand() < 0.5: d.rectangle([P_(x + 14, wy), P_(x + 26, wy + 14)], fill=(255, 210, 90, int(255 * vis)))
    d.rectangle([P_(120, base_y), P_(960, base_y + 18)], fill=(14, 18, 42, int(255 * vis)), outline=(255, 190, 70, int(200 * vis)))
    return Image.alpha_composite(img, lay.reduce(SS))

def pay_crate(u, shake=True):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    slide = ease(clamp(u / 0.6)); cy = lerp(-200, 1010, slide)
    sx = 14 * math.exp(-6 * max(0, u - 0.6)) * math.sin(u * 70) if u > 0.6 else 0
    paste_sprite(img, E.GLOW_O, 540, cy, 800, 0.3 * slide)
    c = crate(0.0)
    paste_rot(img, c, 540 + sx, cy, 1.0, 0)
    return img

def pay_camp_dark(u):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    lay, d = new_dyn()
    for i in range(14):
        rr = np.random.RandomState(i)
        x = 540 + rr.uniform(-90, 90); y = 1330 - 200 * clamp(u / 2.0) * rr.uniform(0.5, 1) ; a = int(255 * max(0, 1 - u / 1.8))
        d.ellipse([P_(x - 4, y - 4), P_(x + 4, y + 4)], fill=(255, 150, 40, a))
    return Image.alpha_composite(img, lay.reduce(SS))

# ------------------------------------------------------------------ cards / bones / lidar
CARDS = [("KILLED?", 'skull'), ("STARVED?", 'bowl'), ("DROWNED?", 'wave'), ("STAYED?", 'hut')]
CARD_POS = [(330, 740), (750, 740), (330, 1090), (750, 1090)]
def card_icon(d, kind, cx, cy, s, col):
    if kind == 'skull': skull(d, cx, cy + 6, s * 0.9, (236, 232, 214, 255))
    elif kind == 'bowl':
        d.pieslice([P_(cx - s * 0.5, cy - s * 0.5), P_(cx + s * 0.5, cy + s * 0.5)], 0, 180, fill=col)
        d.line([P_(cx - s * 0.5, cy), P_(cx + s * 0.5, cy)], fill=col, width=4 * SS)
        for dx in (-0.2, 0, 0.2): d.line([P_(cx + dx * s, cy - 6), P_(cx + dx * s + 8, cy - s * 0.4)], fill=(255, 255, 255, 120), width=3 * SS)
    elif kind == 'wave':
        for k in range(3):
            pts = [P_(cx - s * 0.55 + i * s * 1.1 / 24, cy - s * 0.25 + k * s * 0.28 + 12 * math.sin(i / 24 * 6.28 * 2)) for i in range(25)]
            d.line(pts, fill=col, width=6 * SS)
    elif kind == 'hut':
        d.polygon([P_(cx - s * 0.55, cy), P_(cx, cy - s * 0.55), P_(cx + s * 0.55, cy)], fill=col)
        d.rectangle([P_(cx - s * 0.4, cy), P_(cx + s * 0.4, cy + s * 0.45)], fill=col)
        d.rectangle([P_(cx - s * 0.1, cy + s * 0.15), P_(cx + s * 0.1, cy + s * 0.45)], fill=(10, 6, 24, 255))

def cards_scene(t, flip_at, reveal_q=0.0):
    base = jungle(t, 120 + 6 * t, dim=0.62)
    dyn, d = new_dyn()
    for i, ((cx, cy), (lab, ic), ft) in enumerate(zip(CARD_POS, CARDS, flip_at)):
        u = clamp((t - ft) / 0.5)
        a = u * math.pi
        wx = abs(math.cos(a)); front = u >= 0.5
        if t < ft - 0.0 and ft > 0: front = False; wx = 1.0
        w = 400 * max(0.04, wx); h = 320
        if t < ft - 0.3 and ft > 1.0:
            pass
        d.rounded_rectangle([P_(cx - w / 2, cy - h / 2)[0], P_(cx - w / 2, cy - h / 2)[1], P_(cx + w / 2, cy + h / 2)[0], P_(cx + w / 2, cy + h / 2)[1]], radius=26 * SS,
                            fill=(8, 14, 40, 235) if front else (30, 22, 70, 235), outline=(255, 214, 60, 255) if front else (80, 235, 255, 255), width=5 * SS)
        if wx > 0.5:
            if front and reveal_q < 0.5:
                card_icon(d, ic, cx, cy - 30, 120, (80, 235, 255, 255)); text(d, (cx, cy + 100), lab, 44, WHITE)
                text(d, (cx - 160, cy - 128), str(i + 1), 40, YEL)
            else:
                text(d, (cx, cy), "?", 160, (255, 255, 255, 120) if not front else (255, 255, 255, 255))
    return comp(base, dyn)

def lidar_assets():
    if 'lidar' in _cache: return _cache['lidar']
    PW, PH = 900, 780; rng = np.random.RandomState(12)
    n = rng.rand(PH // 8, PW // 8).astype(np.float32)
    f = np.zeros((PH, PW), np.float32)
    for sc_, wgt in ((8, 0.5), (16, 0.3), (32, 0.2)):
        small = rng.rand(PH // sc_ + 2, PW // sc_ + 2).astype(np.float32)
        im = Image.fromarray((small * 255).astype(np.uint8)).resize((PW, PH), Image.BICUBIC)
        f += np.asarray(im, np.float32) / 255 * wgt
    canopy = np.zeros((PH, PW, 3), np.float32)
    canopy[..., 0] = 10 + 22 * f; canopy[..., 1] = 50 + 110 * f; canopy[..., 2] = 24 + 36 * f
    st = Image.new('RGB', (PW, PH), (4, 10, 22)); d = ImageDraw.Draw(st)
    for (x0, y0, x1, y1) in [(120, 100, 360, 270), (500, 180, 780, 380), (200, 500, 460, 700), (560, 520, 800, 720), (330, 300, 560, 440)]:
        d.rectangle([x0, y0, x1, y1], outline=(60, 230, 255), width=4)
        for k in range(1, 5): d.line([x0 + k * (x1 - x0) / 5, y0, x0 + k * (x1 - x0) / 5, y1], fill=(30, 130, 170), width=1)
    for (a, b) in [((0, 280), (900, 290)), ((450, 0), (440, 780)), ((120, 100), (780, 700)), ((0, 600), (900, 430))]:
        d.line([a, b], fill=(255, 190, 70), width=7); d.line([a, b], fill=(255, 235, 170), width=2)
    for (cx, cy) in [(260, 400), (680, 450), (400, 620), (650, 110), (150, 700)]:
        for r in (14, 26, 38): d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(60, 230, 255), width=3)
    S_ = np.asarray(st, np.float32)
    _cache['lidar'] = (canopy, S_, PW, PH); return _cache['lidar']

def lidar_scene(t, prog):
    canopy, S_, PW, PH = lidar_assets()
    base = jungle(t, 200, dim=0.8, fireflies=False)
    y_s = int(prog * PH)
    arr = canopy.copy()
    if y_s > 0: arr[:y_s] = S_[:y_s] * 1.0 + canopy[:y_s] * 0.18
    if 0 < y_s < PH:
        band = np.exp(-((np.arange(PH) - y_s) / 14.0) ** 2)[:, None, None]
        arr = arr + band * np.array([60, 200, 255], np.float32) * 1.0
    pan = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    m = Image.new('L', (PW, PH), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, PW - 1, PH - 1], radius=36, fill=255)
    pan.putalpha(m)
    base.alpha_composite(pan, (90, 480))
    dyn, d = new_dyn()
    d.rounded_rectangle([P_(90, 480)[0], P_(90, 480)[1], P_(990, 1260)[0], P_(990, 1260)[1]], radius=36 * SS, outline=(80, 235, 255, 255), width=5 * SS)
    return comp(base, dyn)

# ------------------------------------------------------------------ walkers for parts 4 / 7
def people_static(t, x_dx=0.0, alpha=1.0, packing=False):
    def fn(dd):
        for kind, bx, h, po in [('r', 200, 400, 1.4), ('j', 420, 450, 0.7), ('f', 650, 520, 0.0)]:
            ph = 0.0 if not packing else math.sin(t * 2.2 + po) * 0.35
            person(dd, bx + x_dx, GROUND_Y + 6, h, kind, ph, alpha, 0.35)
    return fn

# ------------------------------------------------------------------ part configs
def f_const(label, val, red=False): return lambda t: (label, val, red)

def counter_days(t): return ("DAYS MISSING", f"{DAYS:,}", True)
def counter_p6(t):
    u = clamp((t - 1.0) / 9.0); v = int(DAYS * u ** 3)
    if t >= 12.0: v = DAYS
    return ("DAYS MISSING", f"{v:,}", v > 5000)
def counter_p7(t):
    u = clamp((t - 2.0) / 7.5); v = int(100 * ease(u))
    if t >= 12.0: return ("SEARCHERS LOST", "100+", True)
    return ("SEARCHERS LOST", f"{v}" if v < 100 else "100+", v > 30)
def counter_p4(t):
    u = clamp((t - 2.0) / 8.0); v = int(100 - 62 * u)
    return ("SUPPLIES LEFT", f"{v}%", v < 55)
def counter_p8(t):
    if t < 6.0: return ("TEST RESULT", "...", False)
    if t < 12.0: return ("TEST RESULT", "???", True)
    return ("TEST RESULT", "NO MATCH", True)
def counter_p10(t):
    if t < 12.0: return ("SCAN PROGRESS", f"{int(clamp(t / 10.0) * 62)}%", False)
    return ("SCAN PROGRESS", f"{int(62 + 38 * ease(clamp((t - 12.0) / 1.2)))}%", False)

CFG = {}
CFG[2] = dict(hook=("HE SURVIVED WHAT", "KILLED OTHER EXPLORERS."), counter=counter_days,
              caps=[(2.0, 4.4, "BRITISH EXPLORER"), (4.4, 7.2, "MAPPED THE JUNGLE BORDERS"), (7.2, 10.0, "THEN HE FOUND A CLUE...")],
              cliff=[("THEN HE FOUND", 62, WHITE), ("MANUSCRIPT 512.", 104, RED), ("IT CHANGED EVERYTHING.", 50, YEL)], shard=(790, 1120), title="Who Was Fawcett?")
CFG[3] = dict(hook=("HE BELIEVED IN A CITY", "NOBODY BELIEVED IN."), counter=counter_days,
              caps=[(2.0, 4.4, "HE CALLED IT 'Z'"), (4.4, 7.2, "EXPERTS SAID IMPOSSIBLE"), (7.2, 10.0, "HE SOLD EVERYTHING TO GO")],
              cliff=[("HE TOLD NO ONE", 62, WHITE), ("WHERE IT WAS.", 104, RED), ("THAT SECRET WENT WITH HIM.", 46, YEL)], shard=(250, 1400), title="The City of Z")
CFG[4] = dict(hook=("ONE ORDER", "BEFORE HE LEFT."), counter=counter_p4,
              caps=[(2.0, 4.4, "THREE MEN. NO RADIO."), (4.4, 7.2, "LIGHT PACKS. LONG ROAD."), (7.2, 10.0, "THEN HE SET ONE RULE")],
              cliff=[("THEN ONE LAST LETTER", 56, WHITE), ("LEFT THE JUNGLE.", 100, RED), ("IT WAS THE LAST EVER.", 52, YEL)], shard=(900, 1250), title="The One Rule")
CFG[5] = dict(hook=("29 MAY 1925.", "THE LAST LETTER."), counter=counter_days,
              caps=[(2.0, 4.4, "DEAD HORSE CAMP"), (4.4, 7.2, "HE WROTE TO HIS WIFE"), (7.2, 10.0, "THEN THE FIRE WENT OUT")],
              cliff=[("AFTER THAT:", 62, WHITE), ("SILENCE.", 130, RED), ("NO BODIES. NO TRACE.", 52, YEL)], shard=(180, 1150), title="Dead Horse Camp")
CFG[6] = dict(hook=("DAY 1. DAY 100.", "DAY 1,000."), counter=counter_p6,
              caps=[(2.0, 4.4, "NO NEWS."), (4.4, 7.2, "STILL NO NEWS."), (7.2, 10.0, "THE WORLD WAITED...")],
              cliff=[("THEN A SEARCH PARTY", 58, WHITE), ("CAME BACK.", 110, RED), ("THEY CARRIED SOMETHING.", 50, YEL)], shard=(860, 1180), title="Silence")
CFG[7] = dict(hook=("100+ PEOPLE WENT", "LOOKING FOR HIM."), counter=counter_p7,
              caps=[(2.0, 4.4, "EXPEDITION AFTER EXPEDITION"), (4.4, 7.2, "MANY NEVER CAME BACK"), (7.2, 10.0, "ONE CAME BACK WITH A BOX")],
              cliff=[("THEY OPENED THE BOX.", 58, WHITE), ("BONES.", 150, RED), ("COULD IT BE HIM?", 54, YEL)], shard=(130, 1000), title="The Search Parties")
CFG[8] = dict(hook=("A BOX. BONES.", "AND ONE QUESTION."), counter=counter_p8,
              caps=[(2.0, 4.4, "A SKELETON"), (4.4, 7.2, "IS IT FAWCETT?"), (7.2, 10.0, "THE TEST BEGINS...")],
              cliff=[("IT WASN'T HIM.", 86, RED), ("SO WHERE WAS", 58, WHITE), ("FAWCETT?", 120, YEL)], shard=(880, 1330), title="The Bones")
CFG[9] = dict(hook=("FOUR THEORIES.", "ONE MYSTERY."), counter=f_const("THEORIES", "4"),
              caps=[(2.0, 5.0, "PICK ONE."), (5.0, 8.0, "COMMENT 1, 2, 3 OR 4"), (8.0, 10.0, "NOW FORGET ALL FOUR.")],
              cliff=[("THEN SCIENTISTS", 58, WHITE), ("LOOKED FROM ABOVE...", 80, RED), ("AND SAW THIS.", 80, YEL)], shard=(540, 1470), title="Four Theories")
CFG[10] = dict(hook=("LASERS CAN SEE", "THROUGH TREES."), counter=counter_p10,
               caps=[(2.0, 4.4, "SCANNING THE JUNGLE"), (4.4, 7.2, "SOMETHING IS UNDER THERE"), (7.2, 10.0, "STRAIGHT LINES. IN NATURE?")],
               cliff=[("HE WASN'T CRAZY.", 80, WHITE), ("HE WAS EARLY.", 120, RED), ("WOULD YOU HAVE GONE? YES or NO", 40, YEL)], shard=(990, 1500), title="Was He Right?")

# scene dispatch: main(ts, t) and payoff(u)
def main_scene(part, ts, t):
    if part == 2: return map_scene(ts + 0 * t, clamp((ts - 2.0) / 7.8))
    if part == 3: return z_scene(ts)
    if part == 4:
        pk = clamp((t - 1) / 3)
        return jungle(t, 30, dim=0.0, people=people_static(t, 0, 1.0, True), fire=None)
    if part == 5:
        fl = clamp(1 - (ts - 8.5) / 1.5) if ts > 8.5 else 1.0
        base = jungle(t, 150, dim=0.35, fire=(540, 1370, fl))
        if fl > 0.02: base = flames(base, 540, 1400, t, 1.0 * fl + 0.01)
        dyn, d = new_dyn()
        for x, s_ in ((290, 300), (790, 300), (140, 250)): seated(d, x, 1390, s_)
        base = comp(base, dyn)
        # letter on knee
        if ts >= 2.0:
            lay, ld = new_dyn(); u = clamp((ts - 2.0) / 0.4)
            ln = int(clamp((ts - 3.0) / 5.0) * 9)
            cx, cy = 540, 880
            paste_rot(base, parchment(620, 380), cx, cy, scale=ease(u), rot=-2)
            for i in range(ln): ld.line([P_(cx - 250, cy - 130 + i * 30), P_(cx - 250 + 360 * (1 if i < ln - 1 else clamp((ts - 3.0) / 5.0 * 9 - i)) - (i % 3) * 40, cy - 130 + i * 30)], fill=(60, 36, 18, 255), width=4 * SS)
            if ts >= 5.6:
                stamp(lay, "29 MAY 1925", cx + 120, cy + 140, 54, -6, (170, 30, 40, 255), 3, scale=over((ts - 5.6) / 0.2), sfill=(236, 220, 180, 255))
            base = comp(base, lay)
        return base
    if part == 6:
        base = jungle(t, 60 + 4 * t, dim=0.7, fireflies=False)
        cards = [("MISSING", "EXPLORER FEARED LOST", 1.6, -1), ("STILL", "NO WORD FROM JUNGLE", 3.6, 1), ("NO NEWS", "FAMILY WAITS FOR ANSWERS", 5.6, -1),
                 ("YEARS", "PASS WITH NO ANSWERS", 7.6, 1), ("STILL MISSING", "THE WORLD WONDERS", 9.0, -1)]
        for i, (h_, s_, t0, sd) in enumerate(cards):
            if ts < t0: continue
            u = ease(clamp((ts - t0) / 0.55))
            x = lerp(540 + sd * 900, 540 + sd * -30 * (i % 2) + 14 * (i - 2), u); y = lerp(1000 + sd * 200, 1010 - 10 * i, u)
            rot = lerp(sd * 540, (i - 2) * 5 + 3 * sd, u)
            paste_rot(base, news_card(h_, s_), x, y, 0.82, rot)
        return base
    if part == 7:
        sc = 40 + 70 * ts
        groups = [(1.0, 4.2), (3.4, 6.4), (5.5, 8.6)]
        def fn(dd):
            for gi, (a, b) in enumerate(groups):
                if ts < a or ts > b + 0.9: continue
                u = (ts - a) / (b - a)
                for kind, bx, h, po in [('r', -300, 330, 1.4), ('j', -120, 360, 0.7), ('f', 60, 400, 0.0)]:
                    x = lerp(bx, 1050 + bx, clamp(u)) if False else bx + 1150 * clamp(u) ** 1.0
                    al = 1.0 - smooth(clamp((x - 520) / 160.0))
                    if al > 0.02 and -300 < x < 1100: person(dd, x, GROUND_Y + 6, h, kind, math.pi * (ts - G0) / B + po, al, 0.35)
        base = jungle(t, sc, dim=0.05, people=fn)
        dyn, d = new_dyn(); layer = dyn
        for gi, (a, b) in enumerate(groups):
            tx = a + (b - a) * 0.62
            if ts >= tx: stamp(layer, "X", 640, 1110 - 30 * gi, 220, -6, (255, 50, 60, 255), 12, scale=over((ts - tx) / 0.2) * (1 if ts < tx + 2.0 else 0.7), alpha=1.0)
        return comp(base, dyn)
    if part == 8:
        base = jungle(t, 60 + 3 * t, dim=0.7, fireflies=False)
        open_ = ease(clamp((ts - 1.5) / 1.0))
        cy = 1090
        paste_sprite(base, E.GLOW_O, 540, cy + 50, 900, 0.35 * open_)
        paste_rot(base, crate(open_), 540, cy, 1.18, 0)
        dyn, d = new_dyn()
        if open_ > 0.6:
            au = clamp((ts - 2.2) / 0.6)
            skull(d, 500, cy - 150 - 60 * (1 - au), 230 * au + 1)
            bone(d, 330, cy - 40, 650, cy - 70, 150 * au); bone(d, 340, cy - 70, 660, cy - 20, 150 * au)
        if ts > 5.0:
            y = 700 + 760 * ((ts - 5.0) / 5.0 % 1.0)
            d.line([P_(180, y), P_(900, y)], fill=(80, 235, 255, 255), width=6 * SS)
            d.line([P_(180, y), P_(900, y)], fill=(80, 235, 255, 90), width=26 * SS)
        return comp(base, dyn)
    if part == 9:
        return cards_scene(ts, [2.0, 3.0, 4.0, 5.0])
    if part == 10:
        return lidar_scene(ts, clamp((ts - 2.0) / 8.0) * 0.5)
    raise ValueError(part)

def pay_scene(part, u):
    if part == 2: return pay_manuscript(u)
    if part == 3: return pay_skyline(u)
    if part == 4: return pay_note(u, "IF WE DON'T RETURN,", "DON'T COME LOOKING.")
    if part == 5: return pay_camp_dark(u)
    if part == 6: return pay_crate(u)
    if part == 7: return pay_crate(u)
    if part == 8:
        img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); lay, d = new_dyn()
        sh = 16 * math.exp(-6 * u)
        stamp(lay, "NOT HIM.", 540 + sh * math.sin(u * 80), 1010, 190, -6, (255, 50, 60, 255), 13, scale=over(u / 0.2))
        return Image.alpha_composite(img, lay.reduce(SS))
    if part == 9:
        return None
    if part == 10: return None
    return None

# ------------------------------------------------------------------ frame
def gray_amt(t):
    if 10.0 <= t < 10.08: return (t - 10.0) / 0.08
    if 10.08 <= t < 10.92: return 1.0
    if 10.92 <= t < 11.0: return (11.0 - t) / 0.08
    return 0.0

def render_raw(part, t):
    cfg = CFG[part]
    ts = min(t, 10.0)
    if part == 9 and t >= 12.0:
        base = cards_scene(t, [2.0, 3.0, 4.0, 5.0], reveal_q=1.0)
    elif part == 10:
        if t >= 12.0: base = lidar_scene(t, clamp(0.5 + 0.5 * ease((t - 12.0) / 1.2)))
        else: base = main_scene(part, ts, t)
    elif part in (7, 8):
        base = main_scene(part, ts, t)
    elif part == 6:
        base = main_scene(part, ts, t)
    else:
        base = main_scene(part, ts if part != 5 else min(t, 10.0), t)
    if t >= 12.0 and part not in (9, 10):
        base = Image.alpha_composite(base, Image.new('RGBA', (W, H), (0, 0, 0, 120)))
        po = pay_scene(part, t - 12.0)
        if po is not None: base = Image.alpha_composite(base, po)
    arr = np.asarray(base.convert('RGB'), dtype=np.float32)
    vig = 0.30 + 0.25 * clamp((t - 6.0) / 4.0)
    arr = arr * (1 - VIG[..., None] * vig)
    g = gray_amt(t)
    if g > 0: arr = gray_post(arr, g)
    if 12.0 <= t < 12.22:
        f = (1 - (t - 12.0) / 0.22) ** 2 * 0.85; arr = arr * (1 - f) + 255 * f
    if 14.0 <= t < 14.4:
        f = (1 - (t - 14.0) / 0.4) ** 2 * 0.4; arr[..., 0] = arr[..., 0] * (1 - f) + 255 * f
        arr[..., 1] *= (1 - 0.5 * f); arr[..., 2] *= (1 - 0.5 * f)
        s_ = int(14 * (1 - (t - 14.0) / 0.4))
        if s_ > 0: arr = np.roll(arr, (int(s_ * math.sin(t * 90)), int(s_ * math.cos(t * 77))), axis=(0, 1))
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    layer = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    draw_ui(part, t, layer, d)
    return Image.alpha_composite(img, layer.reduce(SS)).convert('RGB')

def draw_ui(part, t, layer, d):
    cfg = CFG[part]
    badge(d, part, TOTAL)
    label, val, red = cfg['counter'](t)
    counter(d, t, val, label, red)
    if t < 2.0:
        k = 1.0 if t < 1.8 else max(0.01, 1 - (t - 1.8) / 0.2)
        fit_stamp(layer, cfg['hook'][0], 540, 485, 54, 0, WHITE, 7, scale=k)
        fit_stamp(layer, cfg['hook'][1], 540, 565, 64, 0, YEL, 8, scale=k)
    for a, b, s in cfg['caps']:
        if a <= t < b:
            sc_ = over((t - a) / 0.16) * (1 if t < b - 0.12 else max(0.01, (b - t) / 0.12))
            fit_stamp(layer, s, 540, 1545, 58, 0, WHITE, 8, scale=sc_)
    if 10.95 <= t < 12.0:
        fa = clamp((t - 10.95) / 0.08); sx, sy = cfg['shard']
        d.polygon([P_(sx - 30, sy + 16), P_(sx - 6, sy - 26), P_(sx + 32, sy - 10), P_(sx + 20, sy + 26)], fill=(214, 120, 60, int(255 * fa)), outline=(255, 214, 140, int(255 * fa)), width=2 * SS)
        d.line([P_(sx - 14, sy), P_(sx + 12, sy + 10)], fill=(120, 60, 30, int(255 * fa)), width=2 * SS)
        r_ = 16 + 6 * math.sin(t * 20)
        d.line([P_(sx + 26, sy - 22), P_(sx + 26 + r_, sy - 22 - r_)], fill=(255, 255, 255, int(220 * fa)), width=2 * SS)
        pill(d, 540, 1520, 520, 84, "PAUSE NOW", 54, pulse=0.5 + 0.5 * math.sin(t * 16))
    # cliffhanger
    if t >= 14.0:
        lines = cfg['cliff']; tot = sum(s * 1.18 for _, s, _ in lines)
        y = 1530 - tot + 20
        for i, (s, size, col) in enumerate(lines):
            u = t - 14.0 - i * 0.22
            yy = y + size * 0.59; y += size * 1.18
            if u > 0: fit_stamp(layer, s, 540, yy, size, 0 if i != 1 else -2, col, int(max(6, size / 9)), scale=over(u / 0.2))
    if t >= 15.8:
        nxt = "PART %d NEXT" % (part + 1) if part < TOTAL else "WATCH PART 1 AGAIN"
        pill(d, 540, 1592, 520 if part == TOTAL else 440, 58, nxt, 34, pulse=0.5 + 0.5 * math.sin(t * 8))
        if part == TOTAL: text(d, (540, 1640 if False else 1662), "10 SHARDS HIDDEN. FOUND THEM ALL?", 28, (255, 255, 255, 235), stroke=4)

_f0 = {}
def render(part, t):
    img = render_raw(part, t)
    if t >= DUR_ - 0.4:
        if part not in _f0: _f0[part] = render_raw(part, 0.0)
        img = Image.blend(img, _f0[part], clamp((t - (DUR_ - 0.4)) / 0.4))
    return img

PART_N = None
def _job(i):
    return i, render(PART_N, i / FPS).tobytes()

if __name__ == '__main__':
    mode, PART_N = sys.argv[1], int(sys.argv[2])
    if mode == 'test':
        for t in [float(x) for x in sys.argv[3:]]:
            t0 = time.time(); render(PART_N, t).save(f'p{PART_N}_{t:05.2f}.png'); print(PART_N, t, round(time.time() - t0, 2), 's', flush=True)
    else:
        import multiprocessing as mp
        out = sys.argv[3]; n = int(DUR_ * FPS)
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
               '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-an', out]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        with mp.Pool(4) as pool:
            for k, (i, b) in enumerate(pool.imap(_job, range(n), chunksize=2)):
                p.stdin.write(b)
                if k % 60 == 0: print('frame', k, flush=True)
        p.stdin.close(); p.wait(); print('done')
