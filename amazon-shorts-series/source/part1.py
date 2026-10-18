import sys, math, time, subprocess, datetime
import numpy as np
from PIL import Image, ImageDraw
import series_engine as E
from series_engine import *

PART, TOTAL, DUR_ = 1, 10, 17.0
BPM = 130.0; B = 60 / BPM; G0 = 12.0 - 24 * B
DAYS = (datetime.date(2026, 10, 18) - datetime.date(1925, 5, 29)).days   # days since the last letter [VERIFY date]

# -------- motion tables: walkers keep going, camera slows to a stop (parallax ends)
_dt = 1 / 600.0
_t = np.arange(0, 10.0 + _dt, _dt)
_vw = np.where(_t < 8, 140.0, np.where(_t < 9, 140 + 160 * (_t - 8), 300.0))
_vc = np.where(_t < 8, 140.0, np.where(_t < 9, 140 * (1 - (_t - 8)), 0.0))
SW = np.cumsum(_vw) * _dt
SC = np.cumsum(_vc) * _dt
def S(ts):
    i = int(min(ts, 10.0) / _dt)
    return float(SW[i]), float(SC[i])

PEOPLE = [('r', 120, 400, 1.4), ('j', 350, 450, 0.7), ('f', 600, 520, 0.0)]   # kind, x, height, phase offset
CAPS = [(2.0, 4.2, "PERCY FAWCETT", 'f'), (4.2, 6.5, "HIS SON JACK", 'j'), (6.5, 8.8, "JACK'S FRIEND RALEIGH", 'r'),
        (8.8, 10.0, "THEN THE JUNGLE CLOSED IN.", None)]

def wall_x0(ts):
    return lerp(1400, 380, ease(clamp((ts - 8.2) / 1.0)))

def render_raw(t):
    ts = min(t, 10.0)
    sw, sc = S(ts)
    dx = sw - sc
    base = E.BG.copy()
    for nm in ('far', 'mid'):
        base = Image.alpha_composite(base, layer_crop(nm, sc))
    # moon shafts
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    for i in range(4):
        xt = 120 + 270 * i + 14 * math.sin(t * 0.7 + i)
        fl = 9 + 5 * math.sin(t * 1.3 + i * 2)
        sd.polygon([(xt, 260), (xt + 90, 260), (xt + 40 - 160 + 170, GROUND_Y), (xt - 180, GROUND_Y)], fill=(170, 195, 255, int(fl)))
    base = Image.alpha_composite(base, sh)
    base = Image.alpha_composite(base, layer_crop('near', sc))
    base = Image.alpha_composite(base, layer_crop('ground', sc))
    # people
    dyn = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); dd = ImageDraw.Draw(dyn)
    x0w = wall_x0(ts)
    phase_t = math.pi * (ts - G0) / B
    cap = next((c for c in CAPS if c[0] <= t < c[1]), None)
    for kind, bx, h, po in PEOPLE:
        x = bx + dx
        a = 1 - smooth(clamp((x - x0w) / 240.0))
        if ts >= 10.0: a = 0.0
        if a < 0.02: continue
        if kind == 'f':
            paste_sprite(base, GLOW_O, x + 0.2 * h, GROUND_Y - 0.36 * h, 330, 0.55 * a)
        person(dd, x, GROUND_Y + 6, h, kind, phase_t + po, a, 0.35, mark=(cap is not None and cap[3] == kind))
        if kind == 'f':
            lx, ly = x + 0.2 * h, GROUND_Y - 0.36 * h
            dd.ellipse([(lx - 9) * SS, (ly - 9) * SS, (lx + 9) * SS, (ly + 9) * SS], fill=(255, 200, 100, int(255 * a)))
    base = Image.alpha_composite(base, dyn.reduce(SS))
    base = Image.alpha_composite(base, layer_crop('fg', sc))
    base = Image.alpha_composite(base, layer_crop('canopy', sc))
    # fog + fireflies
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fg)
    for i in range(7):
        fx = (i * 230 + t * (18 + 10 * (i % 2))) % 1700 - 300
        fy = GROUND_Y - 30 + (i % 3) * 22
        fd.ellipse([fx - 330, fy - 46, fx + 330, fy + 46], fill=(150, 170, 230, 22))
    base = Image.alpha_composite(base, fg)
    for fx, fy, ph, sp in E.FIRE:
        al = 0.5 + 0.5 * math.sin(t * 2.6 * sp + ph)
        px = fx + 40 * math.sin(t * 0.5 * sp + ph); py = fy + 30 * math.cos(t * 0.7 * sp + ph)
        if t > 8.2: al *= max(0.0, 1 - (t - 8.2) / 1.0)
        if al > 0.05: paste_sprite(base, E.GLOW_Y, px, py, 30, al * 0.9)
    arr = np.asarray(base.convert('RGB'), dtype=np.float32)
    # post: darkness wall from the right, vignette, freeze, flash
    X = np.arange(W, dtype=np.float32)[None, :]
    dk = 0.0
    if ts > 8.2: dk = 0.6 * ease(clamp((ts - 8.2) / 1.0))
    if dk > 0:
        g = np.clip((X - wall_x0(ts) + 200) / 520.0, 0, 1); g = g * g * (3 - 2 * g)
        arr = arr * (1 - dk * g[..., None] * np.ones((H, 1, 1), np.float32))
    vig = 0.30 + 0.25 * clamp((t - 6.0) / 4.0)
    arr = arr * (1 - VIG[..., None] * vig)
    gray = 0.0
    if 10.0 <= t < 10.08: gray = (t - 10.0) / 0.08
    elif 10.08 <= t < 10.92: gray = 1.0
    elif 10.92 <= t < 11.0: gray = (11.0 - t) / 0.08
    if gray > 0: arr = gray_post(arr, gray)
    if 12.0 <= t < 12.22:
        f = (1 - (t - 12.0) / 0.22) ** 2 * 0.85
        arr = arr * (1 - f) + 255 * f
    if 14.0 <= t < 14.4:
        f = (1 - (t - 14.0) / 0.4) ** 2 * 0.4; arr[..., 0] = arr[..., 0] * (1 - f) + 255 * f
        arr[..., 1] *= (1 - 0.5 * f); arr[..., 2] *= (1 - 0.5 * f)
        s_ = int(14 * (1 - (t - 14.0) / 0.4))
        if s_ > 0: arr = np.roll(arr, (int(s_ * math.sin(t * 90)), int(s_ * math.cos(t * 77))), axis=(0, 1))
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    # envelope
    if 12.0 <= t < 15.5:
        if t < 13.2:
            u = ease((t - 12.0) / 1.2)
            cx, cy = lerp(930, 540, u), lerp(1330, 1010, u) - 160 * math.sin(math.pi * u)
            sc_e, rot = lerp(0.12, 1.0, u), 540 * (1 - u)
        else:
            cx, cy = 540, 1010 + 10 * math.sin(t * 3.0); sc_e = 1.0 + 0.02 * math.sin(t * 5); rot = 3 * math.sin(t * 2.0)
        env = ENVELOPE if t < 14.2 else burnt_envelope(clamp((t - 14.2) / 1.2))
        glow_a = 0.5 if t < 14.2 else 0.5 + 0.5 * clamp((t - 14.2) / 0.6)
        paste_sprite(img, E.GLOW_O, cx, cy, 760 * sc_e, glow_a * 0.55)
        e2 = env.rotate(rot, resample=Image.BICUBIC, expand=True)
        e2 = e2.resize((max(2, int(e2.width * sc_e * 1.0)), max(2, int(e2.height * sc_e * 1.0))), Image.BICUBIC)
        img.alpha_composite(e2, (int(cx - e2.width / 2), int(cy - e2.height / 2)))
    layer = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    draw_ui(t, layer, d)
    return Image.alpha_composite(img, layer.reduce(SS)).convert('RGB')

def draw_ui(t, layer, d):
    badge(d, PART, TOTAL)
    # counter
    if t < 12.0: val, red = 0, False
    else:
        u = ease(clamp((t - 12.0) / 2.5)); val, red = int(DAYS * (1 - (1 - u) ** 3)), t >= 12.4
    counter(d, t, f"{val:,}", "DAYS MISSING", red)
    # hook
    if t < 2.0:
        k = 1.0 if t < 1.8 else max(0.01, 1 - (t - 1.8) / 0.2)
        stamp(layer, "1925. THREE MEN WALKED", 540, 485, 54, 0, (255, 255, 255, 255), 7, scale=k)
        stamp(layer, "INTO THE AMAZON.", 540, 565, 70, 0, (255, 214, 60, 255), 8, scale=k)
    # name captions
    for a, b, s, _k in CAPS:
        if a <= t < b:
            sc_ = over((t - a) / 0.16) * (1 if t < b - 0.12 else max(0.01, (b - t) / 0.12))
            stamp(layer, s, 540, 1545, 64 if len(s) < 20 else 52, 0, (255, 255, 255, 255), 8, scale=sc_)
    # 0:11 hidden shard + pause prompt
    if 10.95 <= t < 12.0:
        fa = clamp((t - 10.95) / 0.08)
        sx, sy = 830, 1040
        d.polygon([((sx - 30) * SS, (sy + 16) * SS), ((sx - 6) * SS, (sy - 26) * SS), ((sx + 32) * SS, (sy - 10) * SS), ((sx + 20) * SS, (sy + 26) * SS)],
                  fill=(214, 120, 60, int(255 * fa)), outline=(255, 214, 140, int(255 * fa)), width=2 * SS)
        d.line([(sx - 10) * SS, (sy - 2) * SS, (sx + 8) * SS, (sy + 6) * SS], fill=(120, 60, 30, int(255 * fa)), width=2 * SS)
        r_ = 16 + 6 * math.sin(t * 20)
        d.line([(sx + 26) * SS, (sy - 22) * SS, (sx + 26 + r_) * SS, (sy - 22 - r_) * SS], fill=(255, 255, 255, int(220 * fa)), width=2 * SS)
        pill(d, 540, 1520, 520, 84, "PAUSE NOW", 54, pulse=0.5 + 0.5 * math.sin(t * 16))
    # cliffhanger
    if t >= 14.0:
        u = t - 14.0
        stamp(layer, "THE LETTERS STOPPED.", 540, 1290, 60, 0, (255, 255, 255, 255), 8, scale=over(u / 0.2))
        stamp(layer, "THEN 100+ PEOPLE", 540, 1385, 60, 0, (255, 214, 60, 255), 8, scale=over((u - 0.25) / 0.2))
        stamp(layer, "VANISHED.", 540, 1495, 130, -2, (255, 70, 80, 255), 11, scale=over((u - 0.5) / 0.2))
    if t >= 15.8:
        pill(d, 540, 1592, 440, 58, "PART 2 NEXT", 34, pulse=0.5 + 0.5 * math.sin(t * 8))
    # embers while the letter burns
    if 14.2 <= t < 15.7:
        rr = np.random.RandomState(3)
        for i in range(26):
            ex = 540 + rr.uniform(-170, 170); ey0 = 1010 + rr.uniform(-90, 90)
            u = clamp((t - 14.2 - rr.uniform(0, 0.5)) / 1.0)
            if 0 < u < 1:
                x_ = ex + 25 * math.sin(u * 6 + i); y_ = ey0 - 260 * u
                rd = 7 * (1 - u) + 2
                d.ellipse([(x_ - rd) * SS, (y_ - rd) * SS, (x_ + rd) * SS, (y_ + rd) * SS], fill=(255, 170 - int(80 * u), 40, int(255 * (1 - u))))

_f0 = None
def render(t):
    global _f0
    img = render_raw(t)
    if t >= DUR_ - 0.4:
        if _f0 is None: _f0 = render_raw(0.0)
        img = Image.blend(img, _f0, clamp((t - (DUR_ - 0.4)) / 0.4))
    return img

def _job(i):
    return i, render(i / FPS).tobytes()

if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for t in [float(x) for x in sys.argv[2:]]:
            t0 = time.time(); render(t).save(f'p1_{t:05.2f}.png'); print(t, round(time.time() - t0, 2), 's')
    else:
        import multiprocessing as mp
        out = sys.argv[2]; n = int(DUR_ * FPS)
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
               '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-an', out]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        with mp.Pool(4) as pool:
            for k, (i, b) in enumerate(pool.imap(_job, range(n), chunksize=2)):
                p.stdin.write(b)
                if k % 30 == 0: print('frame', k, flush=True)
        p.stdin.close(); p.wait(); print('done')
