import numpy as np, math, sys, subprocess, os, time
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from common import *

SS = 2
INTER = next((p for p in ['/usr/share/fonts/opentype/inter/Inter-Black.otf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','/System/Library/Fonts/Supplemental/Arial Bold.ttf'] if os.path.exists(p)), None)
MONO = next((p for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf','/System/Library/Fonts/Menlo.ttc'] if os.path.exists(p)), INTER)
_fc = {}
def font(size, mono=False):
    k = (int(size), mono)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(MONO if mono else INTER, int(size))
    return _fc[k]

def clamp(v, a=0.0, b=1.0): return max(a, min(b, v))
def lerp(a, b, u): return a + (b - a) * u
def ease(u): return smooth(u)
def over(u):  # pop-in with overshoot, u in 0..1
    u = clamp(u)
    return 1 + 2.2 * (u - 1) ** 3 + 1.2 * (u - 1) ** 2 if u < 1 else 1.0

# ------------------------------------------------------------------ camera
class Cam:
    def __init__(s, cx, cy, sc, sx=0, sy=0):
        s.cx, s.cy, s.s, s.sx, s.sy = cx, cy, sc, sx, sy
    def X(s, x): return ((x - s.cx) * s.s + W / 2 + s.sx) * SS
    def Y(s, y): return ((y - s.cy) * s.s + H / 2 + s.sy) * SS
    def L(s, l): return l * s.s * SS
    def P(s, x, y): return (s.X(x), s.Y(y))

# ------------------------------------------------------------------ sprites
def make_ball_sprites():
    D = 640
    big = 2
    im = Image.new('RGBA', (D * big, D * big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = D * big / 2
    c = (r, r)
    d.ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=(244, 124, 28, 255))
    seam = (28, 14, 8, 255)
    sw = int(D * big * 0.035)
    d.line([(r, 0), (r, 2 * r)], fill=seam, width=sw)
    d.line([(0, r), (2 * r, r)], fill=seam, width=sw)
    # side arcs
    for sgn in (-1, 1):
        cx_ = r + sgn * r * 1.18
        rad = r * 0.98
        d.ellipse([cx_ - rad, r - rad, cx_ + rad, r + rad], outline=seam, width=sw)
    # clip to circle
    mask = Image.new('L', im.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    bg = Image.new('RGBA', im.size, (0, 0, 0, 0))
    base = Image.new('RGBA', im.size, (244, 124, 28, 255))
    flat = Image.composite(im, bg, mask)
    flat = flat.resize((D, D), Image.LANCZOS)
    # shading (static)
    sh = np.zeros((D, D, 4), np.float32)
    yy, xx = np.mgrid[0:D, 0:D].astype(np.float32)
    nx = (xx - D / 2) / (D / 2); ny = (yy - D / 2) / (D / 2)
    rr = np.sqrt(nx ** 2 + ny ** 2)
    hl = np.exp(-(((nx + 0.38) ** 2 + (ny + 0.42) ** 2) / 0.10))
    sh[..., :3] = 255
    sh[..., 3] = hl * 0.55 * 255
    dark = np.clip((rr - 0.55) / 0.45, 0, 1) ** 1.6
    shd = np.zeros((D, D, 4), np.float32)
    shd[..., :3] = (20, 6, 20)
    shd[..., 3] = (dark * 0.55 + np.clip((nx + ny) * 0.12, 0, 0.2)) * 255
    shade_hl = Image.fromarray(sh.astype(np.uint8), 'RGBA')
    shade_dk = Image.fromarray(shd.astype(np.uint8), 'RGBA')
    shade = Image.alpha_composite(shade_dk, shade_hl)
    cm = Image.new('L', (D, D), 0)
    ImageDraw.Draw(cm).ellipse([0, 0, D - 1, D - 1], fill=255)
    a = ImageChops.multiply(shade.getchannel('A'), cm)
    shade.putalpha(a)
    return flat, shade

BALL_FLAT, BALL_SHADE = make_ball_sprites()

def radial_sprite(color, D=400, power=2.0):
    yy, xx = np.mgrid[0:D, 0:D].astype(np.float32)
    rr = np.sqrt(((xx - D / 2) / (D / 2)) ** 2 + ((yy - D / 2) / (D / 2)) ** 2)
    a = np.clip(1 - rr, 0, 1) ** power
    arr = np.zeros((D, D, 4), np.uint8)
    arr[..., 0], arr[..., 1], arr[..., 2] = color
    arr[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(arr, 'RGBA')

GLOW_ORANGE = radial_sprite((255, 120, 40))
GLOW_CYAN = radial_sprite((60, 220, 255))

rng = np.random.RandomState(11)
BOKEH = [(rng.uniform(-100, 1180), rng.uniform(120, 760), rng.uniform(30, 90),
          [(90, 140, 255), (200, 90, 255), (60, 220, 255), (255, 120, 200)][rng.randint(0, 4)],
          rng.uniform(0.05, 0.16)) for _ in range(34)]

GRAD_Y = [-800, 0, 700, 1200, 1560, 2600]
GRAD_C = np.array([(5, 7, 24), (10, 16, 52), (24, 36, 116), (44, 56, 160), (66, 72, 190), (66, 72, 190)], np.float32)

def paste_sprite(canvas, spr, cx, cy, diam, alpha=1.0, rot=0.0):
    """cx,cy,diam in canvas px"""
    d = int(max(2, diam))
    if d > 6000: return
    s = spr
    if rot:
        s = s.rotate(rot, resample=Image.BICUBIC)
    s = s.resize((d, d), Image.BILINEAR if d < spr.width else Image.BICUBIC)
    if alpha < 1.0:
        a = s.getchannel('A').point(lambda v: int(v * alpha))
        s = s.copy(); s.putalpha(a)
    canvas.paste(s, (int(cx - d / 2), int(cy - d / 2)), s)

# ------------------------------------------------------------------ scene
def draw_bg(cam):
    rows = (np.arange(H * SS, dtype=np.float32) / SS - H / 2 - cam.sy) / cam.s + cam.cy
    col = np.stack([np.interp(rows, GRAD_Y, GRAD_C[:, k]) for k in range(3)], axis=1).astype(np.uint8)
    arr = np.broadcast_to(col[:, None, :], (H * SS, W * SS, 3))
    return Image.fromarray(np.ascontiguousarray(arr), 'RGB')

def draw_scene(cam, att, tau, t_clock, seg_start, fx):
    cv = draw_bg(cam)
    d = ImageDraw.Draw(cv, 'RGBA')
    # bokeh
    for (bx, by, br, bc, ba) in BOKEH:
        paste_sprite(cv, radial_sprite(bc, 96, 0.6) if False else GLOW_CYAN, cam.X(bx), cam.Y(by), cam.L(br * 2.4), ba * 0.9) if False else None
        x0, y0 = cam.X(bx - br), cam.Y(by - br); x1, y1 = cam.X(bx + br), cam.Y(by + br)
        d.ellipse([x0, y0, x1, y1], fill=bc + (int(255 * ba),))
    # spotlight beams
    for (xa, xb, xc, xd, al) in [(470, 600, 560, 960, 22), (700, 840, 640, 1000, 26)]:
        d.polygon([cam.P(xa, -200), cam.P(xb, -200), cam.P(xd, 1560), cam.P(xc, 1560)], fill=(255, 255, 255, al))
    # hoop glow
    paste_sprite(cv, GLOW_ORANGE, cam.X(780), cam.Y(820), cam.L(720), 0.30)
    # floor
    fy = cam.Y(FLOOR)
    fy0 = min(fy, H * SS + 10)
    d.rectangle([-10, fy0, W * SS + 10, H * SS + 10], fill=(24, 14, 46, 255))
    d.rectangle([-10, fy0, W * SS + 10, max(fy0, min(cam.Y(FLOOR + 220), H * SS + 10))], fill=(34, 20, 62, 255))
    for i in range(-14, 26):
        x0 = 540 + (i - 5.5) * 120
        x1 = 540 + (x0 - 540) * 2.6
        d.line([cam.P(x0, FLOOR), cam.P(x1, FLOOR + 900)], fill=(255, 255, 255, 14), width=max(1, int(2 * SS * cam.s)))
    for k, yy in enumerate((FLOOR + 60, FLOOR + 160, FLOOR + 300, FLOOR + 480)):
        d.line([cam.P(-400, yy), cam.P(1500, yy)], fill=(255, 255, 255, 14), width=max(1, int(2 * SS * cam.s)))
    # neon edge line
    for w_, a_ in ((34, 30), (18, 70), (8, 255)):
        d.line([cam.P(-400, FLOOR), cam.P(1500, FLOOR)], fill=(70, 225, 255, a_), width=max(1, int(w_ * SS * cam.s * 0.5)))
    # stanchion + board
    d.rectangle([cam.X(924), cam.Y(880), cam.X(948), cam.Y(FLOOR)], fill=(52, 58, 96, 255))
    d.rectangle([cam.X(924), cam.Y(880), cam.X(930), cam.Y(FLOOR)], fill=(96, 106, 160, 255))
    d.rounded_rectangle([cam.X(BOARD_X), cam.Y(BOARD_Y0), cam.X(BOARD_X + 30), cam.Y(BOARD_Y1)],
                        radius=cam.L(9), fill=(236, 240, 255, 255), outline=(255, 255, 255, 255))
    d.rectangle([cam.X(BOARD_X), cam.Y(BOARD_Y0), cam.X(BOARD_X + 8), cam.Y(BOARD_Y1)], fill=(170, 180, 225, 255))
    # rim bracket
    d.line([cam.P(RIMC[0] + RIMHW, RIM_Y), cam.P(BOARD_X, RIM_Y)], fill=(255, 90, 31, 255), width=int(cam.L(10)))
    # rim (back half)
    ry = 24
    bb = [cam.X(RIMC[0] - RIMHW), cam.Y(RIM_Y - ry), cam.X(RIMC[0] + RIMHW), cam.Y(RIM_Y + ry)]
    rw = int(cam.L(11))
    d.arc(bb, 180, 360, fill=(190, 55, 20, 255), width=rw)

    # ball + trail
    bx, by, ba = ball(att, tau)
    shadow_h = max(0.0, FLOOR - by)
    if by < FLOOR + 220 or True:
        sw_ = R * (1.5 - clamp(shadow_h / 1800.0) * 0.9)
        al = int(120 * (1 - clamp(shadow_h / 1500.0) * 0.8))
        sy = FLOOR + 38
        d.ellipse([cam.X(bx - sw_), cam.Y(sy - sw_ * 0.22), cam.X(bx + sw_), cam.Y(sy + sw_ * 0.22)], fill=(0, 0, 10, al))
    if fx.get('trail', True):
        for k in range(4, 0, -1):
            tk = t_clock - k * 0.014
            if tk < seg_start: continue
            a2, t2 = ball_clock(tk)
            if a2 != att: continue
            gx, gy, ga = ball(a2, t2)
            paste_sprite(cv, BALL_FLAT, cam.X(gx), cam.Y(gy), cam.L(2 * R), 0.16 + 0.07 * (4 - k), -math.degrees(ga))
    ang = -math.degrees(ba)
    dia = cam.L(2 * R)
    # compose ball flat + shade
    comp = BALL_FLAT.rotate(ang, resample=Image.BICUBIC)
    comp = Image.alpha_composite(comp, BALL_SHADE)
    paste_sprite(cv, comp, cam.X(bx), cam.Y(by), dia)

    # net
    draw_net(d, cam, bx, by, t_clock, att, tau, fx)
    # rim front
    d.arc(bb, 0, 180, fill=(255, 98, 36, 255), width=rw)
    for ex in (RIMC[0] - RIMHW, RIMC[0] + RIMHW):
        rr_ = cam.L(7)
        d.ellipse([cam.X(ex) - rr_, cam.Y(RIM_Y) - rr_, cam.X(ex) + rr_, cam.Y(RIM_Y) + rr_], fill=(255, 130, 60, 255))
    # rim highlight
    d.arc(bb, 20, 160, fill=(255, 190, 140, 150), width=max(1, int(rw * 0.28)))
    return cv

def draw_net(d, cam, bx, by, t_clock, att, tau, fx):
    N = 7; rows = 6
    sway = 0.0
    if att == 3:
        sws = events(3, 'swish')[0]
        if tau > sws:
            dtau = tau - sws
            sway = math.exp(-2.2 * dtau) * math.sin(11.0 * dtau)
    elif att == 1:
        rr = events(1, 'rim')[0]
        if tau > rr:
            dtau = tau - rr
            sway = 0.35 * math.exp(-3.0 * dtau) * math.sin(14 * dtau)
    NH = 150.0
    def node(a, u):
        hw = lerp(RIMHW - 4, 52, u)
        x = RIMC[0] + hw * a
        y = RIM_Y + 6 + NH * u * (1.0 - 0.0 * u)
        # sway
        x += sway * 26 * u
        # ball push
        dx = x - bx; dy = y - by
        dist = math.hypot(dx, dy)
        lim = R + 12
        if dist < lim and dist > 1e-3 and by > RIM_Y - 10:
            x = bx + dx / dist * lim
            y = by + dy / dist * lim * 0.8 + (y - by) * 0.2
        return x, y
    wd = max(1, int(cam.L(3.2)))
    col = (245, 245, 255, 215)
    for i in range(N + 1):
        a0 = -1 + 2 * i / N
        for dirn in (1, -1):
            a1 = -1 + 2 * (i + dirn) / N
            if a1 < -1.0001 or a1 > 1.0001: continue
            pts = []
            for r in range(rows + 1):
                u = r / rows
                a = lerp(a0, a1, u)
                pts.append(cam.P(*node(a, u)))
            d.line(pts, fill=col, width=wd, joint='curve')

# ------------------------------------------------------------------ overlays
def text(d, xy, s, size, fill, stroke=0, sfill=(0, 0, 0, 255), mono=False, anchor='mm'):
    d.text((xy[0] * SS, xy[1] * SS), s, font=font(size * SS, mono), fill=fill, anchor=anchor,
           stroke_width=int(stroke * SS), stroke_fill=sfill)

def stamp(layer, s, cx, cy, size, rot, fill, stroke=10, scale=1.0, alpha=1.0, sfill=(0, 0, 0, 255), mono=False):
    f = font(max(8, int(size * SS * scale)), mono)
    tmp0 = ImageDraw.Draw(Image.new('RGBA', (4, 4)))
    tw = int(tmp0.textlength(s, font=f)) + 8 * SS * stroke // 4 + 80
    th = int(size * SS * scale * 1.5) + 40
    tmp = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((tw / 2, th / 2), s, font=f, fill=fill, anchor='mm',
                              stroke_width=int(stroke * SS * scale), stroke_fill=sfill)
    if rot: tmp = tmp.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1.0:
        a = tmp.getchannel('A').point(lambda v: int(v * alpha)); tmp.putalpha(a)
    layer.alpha_composite(tmp, (int(cx * SS - tmp.width / 2), int(cy * SS - tmp.height / 2)))

def pepper(d, cx, cy, size, rot=0.0, body=(235, 30, 40, 255), cross=False):
    # curved pepper along an arc
    n = 28
    pts_l, pts_r = [], []
    for i in range(n + 1):
        u = i / n
        ang = -0.6 + u * 1.5
        px = math.sin(ang) * size * 0.55 * u + (u - 0.5) * size * 0.0
        py = (u - 0.5) * size * 1.0 * 1.0
        # centerline curve: bend to the right as u grows
        px = size * 0.32 * (u ** 1.8) - size * 0.05
        w = size * 0.30 * (math.sin(math.pi * min(1.0, u * 0.92 + 0.04)) ** 0.45) * (1 - 0.5 * u) + size * 0.02
        # tangent normal approx
        dx = size * 0.32 * 1.8 * (u ** 0.8) / n
        dy = size / n
        l = math.hypot(dx, dy); nxn, nyn = dy / l, -dx / l
        pts_l.append((px + nxn * w, py + nyn * w))
        pts_r.append((px - nxn * w, py - nyn * w))
    pts = pts_l + pts_r[::-1]
    cr, sr = math.cos(rot), math.sin(rot)
    def tr(p): return ((cx + p[0] * cr - p[1] * sr) * SS, (cy + p[0] * sr + p[1] * cr) * SS)
    d.polygon([tr(p) for p in pts], fill=body, outline=(90, 8, 14, 255))
    # highlight
    hl = [tr((p[0] - size * 0.045, p[1])) for p in pts_l[3:20]]
    d.line(hl, fill=(255, 140, 140, 190), width=max(2, int(size * 0.03 * SS)))
    # stem
    s0 = pts_l[0]; s1 = pts_r[0]
    stem = [tr((s0[0] - size * 0.02, s0[1] + size * 0.03)), tr((s1[0] + size * 0.02, s1[1] + size * 0.03)),
            tr((s1[0] + size * 0.06, s1[1] - size * 0.14)), tr((s0[0] + size * 0.0, s0[1] - size * 0.1))]
    d.polygon(stem, fill=(40, 170, 60, 255), outline=(10, 70, 20, 255))
    if cross:
        w = max(6, int(size * 0.07 * SS))
        d.line([(cx - size * 0.5) * SS if False else (cx - size * 0.42) * SS, (cy - size * 0.55) * SS,
                (cx + size * 0.55) * SS, (cy + size * 0.55) * SS], fill=(255, 255, 255, 255), width=w + 8 * SS)
        d.line([(cx - size * 0.42) * SS, (cy - size * 0.55) * SS, (cx + size * 0.55) * SS, (cy + size * 0.55) * SS],
               fill=(40, 245, 140, 255), width=w)

def timer_ui(d, t, val, mode):
    if val > 8: bc = (255, 255, 255, 255); fc = (255, 255, 255, 255)
    elif val > 3.99: bc = (255, 214, 60, 255); fc = (255, 214, 60, 255)
    else: bc = (255, 60, 70, 255); fc = (255, 70, 80, 255)
    if mode == 'win': bc = (50, 255, 150, 255); fc = (50, 255, 150, 255)
    jx = jy = 0
    if val < 4 and mode != 'win':
        jx = 5 * math.sin(t * 90); jy = 4 * math.cos(t * 77)
    blink = 1.0
    if mode == 'freeze':
        blink = 0.35 + 0.65 * (math.sin(t * 7.0) > -0.2)
    cx, cy = 540 + jx, 530 + jy
    # glow
    d.rounded_rectangle([(cx - 305) * SS, (cy - 130) * SS, (cx + 305) * SS, (cy + 130) * SS], radius=46 * SS, fill=bc[:3] + (40,))
    d.rounded_rectangle([(cx - 290) * SS, (cy - 120) * SS, (cx + 290) * SS, (cy + 120) * SS], radius=42 * SS,
                        fill=(4, 6, 24, 215), outline=bc, width=7 * SS)
    s = f"{max(0.0, val):05.2f}"
    text(d, (cx, cy - 12), s, 172, fc[:3] + (int(255 * blink),), stroke=0, mono=True)
    text(d, (cx, cy + 86), "SECONDS LEFT", 32, (200, 210, 255, 230))

def attempt_dots(d, t):
    results = [None, None, None]
    if t >= 2.35: results[0] = 'x'
    if t >= 4.75: results[1] = 'x'
    if t >= 10.36: results[2] = 'ok'
    cur = 0 if t < 3.5 else (1 if t < 5.5 else 2)
    y = 1515
    for i in range(3):
        x = 540 + (i - 1) * 120
        r = 34
        if results[i] == 'x':
            d.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=(255, 50, 64, 255), outline=(255, 255, 255, 255), width=5 * SS)
            k = 14
            d.line([(x - k) * SS, (y - k) * SS, (x + k) * SS, (y + k) * SS], fill=(255, 255, 255, 255), width=7 * SS)
            d.line([(x - k) * SS, (y + k) * SS, (x + k) * SS, (y - k) * SS], fill=(255, 255, 255, 255), width=7 * SS)
        elif results[i] == 'ok':
            d.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=(40, 230, 130, 255), outline=(255, 255, 255, 255), width=5 * SS)
            d.line([(x - 15) * SS, y * SS, (x - 4) * SS, (y + 12) * SS, (x + 16) * SS, (y - 12) * SS], fill=(255, 255, 255, 255), width=8 * SS, joint='curve')
        else:
            pulse = 0.5 + 0.5 * math.sin(t * 10) if i == cur else 0.0
            a = int(60 + 120 * pulse) if i == cur else 70
            col = (255, 214, 60, 255) if i == cur else (255, 255, 255, 120)
            rr = r + 4 * pulse
            d.ellipse([(x - rr) * SS, (y - rr) * SS, (x + rr) * SS, (y + rr) * SS], fill=(0, 0, 20, 140), outline=col, width=5 * SS)
            text(d, (x, y + 1), str(i + 1), 34, col[:3] + (255,))

def draw_ui(t, layer, d):
    val = timer_val(t)
    mode = 'win' if t >= 10.36 else ('freeze' if 7.0 <= t < 10.0 else 'run')
    # ---- top texts
    if t < 2.0:
        text(d, (540, 215), "MAKE THIS SHOT IN 15 SECONDS", 56, (255, 255, 255, 255), stroke=7)
        w = 800
        text(d, (610, 300), "OR EAT A GHOST PEPPER", 54, (255, 214, 60, 255), stroke=7)
        pepper(d, 150, 296, 100, rot=-0.5)
    elif t < 12.0 or t >= 14.4:
        if not (5.5 <= t < 6.5):
            pw = 650
            d.rounded_rectangle([(540 - pw / 2) * SS, 225 * SS, (540 + pw / 2) * SS, 305 * SS], radius=40 * SS,
                                fill=(10, 4, 20, 210), outline=(255, 60, 70, 255), width=5 * SS)
            text(d, (560, 266), "MISS = GHOST PEPPER", 46, (255, 255, 255, 255))
            pepper(d, 235, 262, 74, rot=-0.5)
    # ---- timer (hidden during replay & card)
    if t < 12.0 or t >= 14.4:
        timer_ui(d, t, val, mode)
    # ---- dots
    if 2.0 <= t < 12.0 and not (6.5 <= t < 7.0):
        attempt_dots(d, t)
    # ---- stamps
    if 2.35 <= t < 3.5:
        u = (t - 2.35) / 0.18
        stamp(layer, "MISS", 540 + 6 * math.sin(t * 70), 1010 + 4 * math.cos(t * 60), 250, 9, (255, 55, 64, 255), 12, scale=over(u), alpha=1.0 if t < 3.3 else (3.5 - t) / 0.2 if False else 1.0)
    if 4.7 <= t < 5.5:
        u = (t - 4.7) / 0.18
        stamp(layer, "AIRBALL", 540 + 5 * math.sin(t * 66), 1010, 190, -7, (255, 214, 60, 255), 11, scale=over(u))
    # ---- pepper beat
    if 5.5 <= t < 6.5:
        u = t - 5.5
        # dark overlay handled in post
        rot = 0.14 * math.sin(u * 40)
        sc = 0.9 + 0.2 * smooth(u / 0.25)
        pepper(d, 560 + 5 * math.sin(u * 60), 1030, 560 * sc, rot=rot)
        stamp(layer, "2 MISSES", 540, 760, 140, -3, (255, 255, 255, 255), 10, scale=over(u / 0.18))
        stamp(layer, "1 SHOT LEFT", 540, 1380, 92, 0, (255, 214, 60, 255), 8, scale=over((u - 0.15) / 0.18))
        if u < 0.5:
            text(d, (540, 230), "", 10, (0, 0, 0, 0))
    if 6.5 <= t < 7.0:
        stamp(layer, "LAST SHOT", 540, 1000 + 10 * math.sin(t * 80), 168, -4, (255, 214, 60, 255), 11, scale=over((t - 6.5) / 0.14))
    # ---- freeze
    if 7.0 <= t < 10.0:
        u = t - 7.0
        beat = math.exp(-((u % 0.9) / 0.10))
        pulse = 1.0 + 0.045 * beat
        stamp(layer, "WILL IT", 540, 1090, 160, 0, (255, 255, 255, 255), 11, scale=pulse * over(u / 0.2))
        stamp(layer, "GO IN?", 540, 1250, 190, 0, (255, 214, 60, 255), 12, scale=pulse * over((u - 0.1) / 0.2))
        text(d, (540, 1385), "1 MILLISECOND BEFORE IMPACT", 36, (255, 255, 255, 235), stroke=5)
        text(d, (540, 1440), "COMMENT  YES  or  NO", 40, (80, 235, 255, 255), stroke=5)
    # ---- payoff
    ts = time_of_tau3_swish()
    if 10.0 <= t < 11.0:
        u = t - ts
        if u >= 0:
            stamp(layer, "SWISH!", 540, 1130, 250, -4, (50, 255, 150, 255), 13, scale=over(u / 0.16) * (1 if t < 10.85 else max(0.01, 1 - (t - 10.85) / 0.15)))
            if u > 0.2 and t < 10.9:
                stamp(layer, "PEPPER = SAFE", 540, 1320, 84, 0, (255, 255, 255, 255), 8, scale=over((u - 0.2) / 0.15))
    # ---- 0:11 card
    if 10.95 <= t < 11.95:
        u = (t - 10.95) / 0.1
        sc = over(u) if t < 11.85 else max(0.01, 1 - (t - 11.85) / 0.10)
        cx, cy = 540, 1000
        w, h = 880 * sc, 700 * sc
        d.rounded_rectangle([(cx - w / 2) * SS, (cy - h / 2) * SS, (cx + w / 2) * SS, (cy + h / 2) * SS], radius=60 * SS,
                            fill=(5, 8, 32, 240), outline=(50, 255, 150, 255), width=int(9 * SS))
        if sc > 0.9:
            text(d, (cx, cy - 270), "SHOT 3 OF 3: MADE", 54, (255, 255, 255, 255))
            text(d, (cx, cy - 120), "0.71s", 190, (50, 255, 150, 255), mono=True)
            text(d, (cx, cy - 10), "LEFT ON THE CLOCK", 40, (200, 210, 255, 255))
            pepper(d, cx - 190, cy + 150, 200, rot=-0.3, cross=True)
            text(d, (cx + 120, cy + 120), "PEPPER", 72, (255, 255, 255, 255))
            text(d, (cx + 120, cy + 195), "SAFE", 72, (50, 255, 150, 255))
            text(d, (cx, cy + 300), "you paused. nice. comment PEPPER", 36, (255, 214, 60, 255))
    # ---- replay + end
    if 12.0 <= t < 14.4:
        on = (int(t * 3) % 2 == 0)
        pw = 560
        d.rounded_rectangle([(540 - pw / 2) * SS, 1150 * SS, (540 + pw / 2) * SS, 1235 * SS], radius=42 * SS, fill=(0, 0, 0, 210), outline=(255, 255, 255, 255), width=4 * SS)
        if on: d.ellipse([300 * SS, 1180 * SS, 330 * SS, 1210 * SS], fill=(255, 40, 50, 255))
        text(d, (555, 1193), "REPLAY  0.27x", 46, (255, 255, 255, 255))
    if t >= 14.4:
        u = t - 14.4
        stamp(layer, "NEXT:", 540, 1060, 90, 0, (255, 255, 255, 255), 8, scale=over(u / 0.2))
        stamp(layer, "BLINDFOLDED?", 540, 1180, 120, -2, (255, 214, 60, 255), 10, scale=over((u - 0.1) / 0.2))
    if t >= 12.0:
        pw = 560
        pulse = 0.5 + 0.5 * math.sin(t * 8)
        d.rounded_rectangle([(540 - pw / 2) * SS, 1300 * SS, (540 + pw / 2) * SS, 1390 * SS], radius=45 * SS,
                            fill=(255, 214, 60, int(215 + 40 * pulse)), outline=(0, 0, 0, 255), width=5 * SS)
        text(d, (540, 1346), "PAUSE AT 0:11", 52, (10, 6, 24, 255))
    if t >= 14.4:
        text(d, (540, 1440), "FOLLOW FOR PART 2", 44, (255, 255, 255, 255), stroke=6)

# ------------------------------------------------------------------ camera schedule
def camera(t):
    shake = (0.0, 0.0)
    if t < 2.0:
        u = t / 2.0
        c = (lerp(540, 590, ease(u)), lerp(960, 930, ease(u)), lerp(1.0, 1.08, ease(u)))
        seg = 0.0
    elif t < 3.5:
        u = (t - 2.0) / 1.5
        c = (lerp(735, 750, u), lerp(805, 830, u), lerp(2.05, 2.3, u))
        seg = 2.0
        if t > 2.18:
            a = 18 * math.exp(-9 * (t - 2.18))
            shake = (a * math.sin(t * 90), a * math.cos(t * 80))
    elif t < 5.5:
        u = (t - 3.5) / 2.0
        c = (lerp(540, 560, u), lerp(990, 1010, u), lerp(1.0, 1.12, ease(u)))
        seg = 3.5
        if t > 4.75:
            a = 10 * math.exp(-8 * (t - 4.75))
            shake = (a * math.sin(t * 90), a * math.cos(t * 80))
    elif t < 6.5:
        c = (560, 1010, 1.12); seg = 5.5
    elif t < 7.0:
        c = (330, 1250, 1.5); seg = 6.5
    elif t < 10.0:
        u = (t - 7.0) / 3.0
        e = u * u * (3 - 2 * u)
        c = (lerp(690, 770, e), lerp(880, 806, e), lerp(1.05, 2.1, e))
        shake = (2.0 * math.sin(t * 13.0), 1.6 * math.cos(t * 11.0))
        seg = 7.0
    elif t < 12.0:
        u = (t - 10.0) / 2.0
        e = ease(u)
        c = (lerp(775, 800, e), lerp(806, 900, e), lerp(2.1, 1.25, e))
        seg = 10.0
        a = 26 * math.exp(-6 * (t - 10.0))
        shake = (a * math.sin(t * 95), a * math.cos(t * 83))
        ts = time_of_tau3_swish()
        if t > ts:
            a2 = 14 * math.exp(-8 * (t - ts))
            shake = (shake[0] + a2 * math.sin(t * 101), shake[1] + a2 * math.cos(t * 90))
    elif t < 14.4:
        u = (t - 12.0) / 2.4
        c = (790, 850, lerp(2.0, 2.25, u)); seg = 12.0
    else:
        u = (t - 14.4) / 1.6
        c = (540, 960, lerp(1.25, 1.0, ease(min(1, u * 2)))); seg = 14.4
    return Cam(c[0], c[1], c[2], shake[0], shake[1]), seg

def post_fx(arr, t):
    """arr float32 HxWx3 (0..255)"""
    gray = 0.0
    if 7.0 <= t < 10.0: gray = 1.0
    elif 10.0 <= t < 10.14: gray = 1.0 - (t - 10.0) / 0.14
    vig = 0.22
    if 7.0 <= t < 10.0:
        beat = math.exp(-(((t - 7.0) % 0.9) / 0.10))
        vig = 0.62 + 0.14 * beat + 0.12 * ((t - 7.0) / 3.0)
    elif 12.0 <= t < 14.4: vig = 0.42
    elif 5.5 <= t < 6.5: vig = 0.5
    if gray > 0:
        g = arr.mean(axis=2, keepdims=True) * 1.0
        g = (arr[..., 0:1] * 0.3 + arr[..., 1:2] * 0.59 + arr[..., 2:3] * 0.11)
        arr = arr * (1 - gray) + g * gray
        arr = (arr - 128) * (1 + 0.18 * gray) + 128
    if 5.5 <= t < 6.5:
        arr = arr * 0.45
        arr[..., 0] += 38
    if 12.0 <= t < 14.4:
        arr = arr * np.array([1.06, 1.0, 0.9], np.float32) + np.array([6, 2, -4], np.float32)
    # vignette
    arr = arr * (1 - VIG[..., None] * vig)
    if 10.0 <= t < 10.2:
        f = (1 - (t - 10.0) / 0.2) ** 2 * 0.85
        arr = arr * (1 - f) + 255 * f
    ts = time_of_tau3_swish()
    if ts <= t < ts + 0.1:
        f = (1 - (t - ts) / 0.1) * 0.35
        arr = arr * (1 - f) + 255 * f
    # red flash on misses
    for tm in (2.18, 4.75):
        if tm <= t < tm + 0.12:
            f = (1 - (t - tm) / 0.12) * 0.30
            arr[..., 0] = arr[..., 0] * (1 - f) + 255 * f
    return arr

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = np.clip(np.sqrt(((xx - W / 2) / (W / 2)) ** 2 * 0.8 + ((yy - H / 2) / (H / 2)) ** 2 * 0.9) - 0.35, 0, 1) ** 1.6

# confetti ------------------------------------------------------------
crng = np.random.RandomState(5)
NCONF = 150
CONF = []
for i in range(NCONF):
    ang = crng.uniform(-math.pi * 0.95, -math.pi * 0.05)
    sp = crng.uniform(300, 1500)
    CONF.append(dict(vx=math.cos(ang) * sp * 0.9, vy=math.sin(ang) * sp, rot=crng.uniform(0, 6.28), vr=crng.uniform(-14, 14),
                     w=crng.uniform(14, 26), h=crng.uniform(8, 14), ph=crng.uniform(0, 6.28),
                     col=[(255, 214, 60), (50, 255, 150), (255, 80, 120), (80, 220, 255), (255, 255, 255), (255, 140, 40)][crng.randint(0, 6)]))

def draw_confetti(cv, cam, t, ts):
    if t < ts: return
    d = ImageDraw.Draw(cv, 'RGBA')
    u = t - ts
    for p in CONF:
        x = 780 + p['vx'] * u * math.exp(-1.2 * u) * 1.0 + 20 * math.sin(6 * u + p['ph'])
        y = 790 + p['vy'] * u * math.exp(-0.6 * u) + 0.5 * 700 * u * u
        if y > FLOOR + 400: continue
        r = p['rot'] + p['vr'] * u
        w = p['w'] * abs(math.cos(r * 0.7)) + 4; h = p['h']
        cr, sr = math.cos(r), math.sin(r)
        pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
        pp = [cam.P(x + px * cr - py * sr, y + px * sr + py * cr) for px, py in pts]
        fade = clamp((3.2 - u) / 1.2)
        d.polygon(pp, fill=p['col'] + (int(255 * fade),))
    # shockwaves
    for k, dl in enumerate((0.0, 0.12)):
        v = (u - dl) / 0.55
        if 0 < v < 1:
            r = 40 + 420 * v
            a = int(200 * (1 - v))
            x0, y0 = cam.P(780 - r, 820 - r); x1, y1 = cam.P(780 + r, 820 + r)
            d.ellipse([x0, y0, x1, y1], outline=(255, 255, 255, a), width=int(cam.L(12 * (1 - v) + 2)))

# ------------------------------------------------------------------ main frame
def render_raw(t):
    att, tau = ball_clock(t)
    cam, seg = camera(t)
    fx = dict(trail=(t < 7.0) or (t >= 14.4))
    cv = draw_scene(cam, att, tau, t, seg, fx)
    if t >= 10.0: draw_confetti(cv, cam, t, time_of_tau3_swish())
    img = cv.reduce(SS)
    arr = np.asarray(img, dtype=np.float32)
    arr = post_fx(arr, t)
    base = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    layer = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    draw_ui(t, layer, d)
    ui = layer.reduce(SS)
    out = Image.alpha_composite(base, ui).convert('RGB')
    return out

_f0 = None
def render(t):
    global _f0
    img = render_raw(t)
    if t >= 15.6:
        if _f0 is None: _f0 = render_raw(0.0)
        a = clamp((t - 15.6) / 0.4)
        img = Image.blend(img, _f0, a)
    return img

def _job(i):
    return i, render(i / FPS).tobytes()

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'test':
        ts = [float(x) for x in sys.argv[2:]]
        for t in ts:
            t0 = time.time()
            render(t).save(f'test_{t:05.2f}.png')
            print(t, round(time.time() - t0, 2), 's')
    else:
        import multiprocessing as mp
        out = sys.argv[2]
        n = int(DUR * FPS)
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
               '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-an', out]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        with mp.Pool(2) as pool:
            for k, (i, b) in enumerate(pool.imap(_job, range(n), chunksize=2)):
                p.stdin.write(b)
                if k % 30 == 0: print('frame', k, flush=True)
        p.stdin.close(); p.wait()
        print('done')
