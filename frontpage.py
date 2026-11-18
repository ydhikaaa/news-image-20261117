"""Draw the front page: one picture summing up the world news of
Tuesday 17 November 2026 (make.fun news-image-20261117, second edition).

Design: a broadsheet front page. A giant serif date masthead, a strip of
the day in figures, eight numbered and illustrated story cards, a world
map with a pin for every card, and a numbered brief list for the rest of
the day. Pure Pillow, fixed geometry, no randomness: two runs write
byte-identical PNGs.

Run:  python3 frontpage.py             (writes entry.png, 1024x1024)
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

W, H = 1024, 1024
M = 24                      # page margin
CW = W - 2 * M              # content width = 976

PAPER = (250, 246, 238)
CARD = (255, 255, 255)
INK = (22, 22, 22)
SOFT = (58, 56, 52)
RED = (176, 28, 38)
NAVY = (24, 42, 74)
RULE = (30, 30, 30)
FAINT = (203, 196, 182)
SKY = (206, 224, 236)
SKY_D = (172, 198, 218)
SEA = (150, 182, 203)
SEA_D = (120, 156, 182)
LAND = (233, 223, 197)
OCEAN = (198, 217, 230)
SMOKE = (110, 108, 105)
FIRE = (233, 126, 38)
GOLD = (198, 156, 66)


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, path, start, max_w, max_lines, floor=15):
    """Largest size <= start whose wrap fits max_lines lines."""
    size = start
    while size > floor:
        lines = wrap(draw, text, F(path, size), max_w)
        if len(lines) <= max_lines:
            return F(path, size), lines
        size -= 1
    return F(path, floor), wrap(draw, text, F(path, floor), max_w)


def para(draw, x, y, lines, fnt, color, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


# ---------------------------------------------------------------- scenes
# Every scene draws inside box (x0, y0, x1, y1) on its own supersampled
# canvas, so geometry is written in fractions of the box.

def scene(w, h, painter):
    img = Image.new("RGB", (w * 3, h * 3), CARD)
    d = ImageDraw.Draw(img)
    painter(d, 0, 0, w * 3, h * 3)
    return img.resize((w, h), Image.LANCZOS)


def chip(d, x, y, text, fill=INK, fg=(255, 255, 255), fh=0.20, box_h=300):
    fnt = F(SANS_B, max(10, int(box_h * fh)))
    tw = d.textlength(text, font=fnt)
    pad = box_h * 0.05
    d.rectangle([x, y, x + tw + 2 * pad, y + box_h * fh * 1.5], fill=fill)
    d.text((x + pad, y + box_h * fh * 0.18), text, font=fnt, fill=fg)
    return x + tw + 2 * pad


def waves(d, x0, y, x1, rows=3, gap=0.055, bh=300, color=(225, 238, 245)):
    for r in range(rows):
        yy = y + r * bh * gap
        for wx in range(int(x0 + bh * 0.03), int(x1 - bh * 0.14), int(bh * 0.22)):
            d.line([(wx, yy), (wx + bh * 0.13, yy)], fill=color, width=max(2, bh // 90))


def smoke(d, cx, cy, s, bh):
    for i, (dx, dy, r) in enumerate([(0, 0, .16), (.10, -.13, .20), (.22, -.27, .25)]):
        rr = r * s
        d.ellipse([cx + dx * s - rr, cy + dy * s - rr, cx + dx * s + rr,
                   cy + dy * s + rr], fill=SMOKE)


def sc_kerch(d, x0, y0, x1, y1):
    bw, bh = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    d.rectangle([x0, y0, x1, y0 + bh * .30], fill=SKY_D)
    for bx, by in [(0.10, 0.10), (0.17, 0.16), (0.86, 0.08)]:
        cx, cy = x0 + bx * bw, y0 + by * bh
        d.line([(cx, cy), (cx + bh * .05, cy - bh * .03)], fill=INK, width=3)
        d.line([(cx + bh * .05, cy - bh * .03), (cx + bh * .10, cy)], fill=INK, width=3)
    deck = y0 + bh * 0.60
    d.rectangle([x0, deck + bh * .16, x1, y1], fill=SEA)
    waves(d, x0, deck + bh * .24, x1, rows=3, bh=bh)
    for tx in (x0 + bw * .16, x0 + bw * .78):
        d.rectangle([tx, deck - bh * .44, tx + bw * .035, deck], fill=INK)
        d.rectangle([tx - bw * .012, deck - bh * .50, tx + bw * .047, deck - bh * .44], fill=INK)
    for cx in range(int(x0 + bw * .24), int(x0 + bw * .72), int(bw * .07)):
        d.line([(x0 + bw * .175, deck - bh * .44), (cx, deck)], fill=(105, 105, 105), width=2)
        d.line([(x0 + bw * .80, deck - bh * .44), (cx, deck)], fill=(105, 105, 105), width=2)
    d.rectangle([x0, deck, x0 + bw * .42, deck + bh * .09], fill=(52, 52, 52))
    d.rectangle([x0 + bw * .60, deck, x1, deck + bh * .09], fill=(52, 52, 52))
    d.polygon([(x0 + bw * .435, deck + 2), (x0 + bw * .50, deck + 2),
               (x0 + bw * .565, deck + bh * .30), (x0 + bw * .50, deck + bh * .30)],
              fill=(96, 44, 38))
    for sx in (0.50, 0.545, 0.585):
        d.line([(x0 + sx * bw, deck + bh * .315), (x0 + sx * bw + bw * .02, deck + bh * .315)],
               fill=(255, 255, 255), width=3)
    d.polygon([(x0 + bw * .44, deck), (x0 + bw * .465, deck - bh * .13),
               (x0 + bw * .485, deck - bh * .01), (x0 + bw * .51, deck - bh * .11),
               (x0 + bw * .505, deck + 2), (x0 + bw * .465, deck + 2)], fill=FIRE)
    smoke(d, x0 + bw * .50, deck - bh * .16, bh * .55, bh)
    chip(d, x0 + bw * .03, y1 - bh * .36, "KERCH STRAIT", box_h=bh)


def sc_kyiv(d, x0, y0, x1, y1):
    bw, bh = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(88, 102, 128))
    d.rectangle([x0, y0, x1, y0 + bh * .34], fill=(66, 78, 102))
    base = y0 + bh * 0.62
    rng = [(.02, .30), (.10, .44), (.19, .26), (.27, .52), (.37, .34),
           (.46, .58), (.56, .30), (.64, .46), (.73, .27), (.81, .50), (.91, .36)]
    for fx, fh in rng:
        bx = x0 + fx * bw
        d.rectangle([bx, base - bh * fh, bx + bw * .075, base], fill=(38, 44, 58))
        for wy in range(3):
            for wx in range(2):
                lit = (int(fx * 100) + wy * 3 + wx) % 4 == 0
                d.rectangle([bx + bw * .012 + wx * bw * .03,
                             base - bh * fh + bh * .06 + wy * bh * .11,
                             bx + bw * .026 + wx * bw * .03,
                             base - bh * fh + bh * .13 + wy * bh * .11],
                            fill=(240, 196, 96) if lit else (24, 28, 38))
    d.rectangle([x0, base, x1, y1], fill=(70, 96, 122))
    waves(d, x0, base + bh * .10, x1, rows=2, bh=bh, color=(170, 196, 216))
    d.rectangle([x0, base - bh * .05, x0 + bw * .40, base - bh * .005], fill=(30, 34, 44))
    d.rectangle([x0 + bw * .62, base - bh * .05, x1, base - bh * .005], fill=(30, 34, 44))
    d.polygon([(x0 + bw * .415, base - bh * .045), (x0 + bw * .475, base - bh * .045),
               (x0 + bw * .545, base + bh * .13), (x0 + bw * .49, base + bh * .13)],
              fill=(52, 30, 28))
    d.polygon([(x0 + bw * .425, base - bh * .05), (x0 + bw * .45, base - bh * .15),
               (x0 + bw * .465, base - bh * .055), (x0 + bw * .49, base - bh * .13),
               (x0 + bw * .48, base - bh * .04)], fill=FIRE)
    smoke(d, x0 + bw * .47, base - bh * .20, bh * .5, bh)
    smoke(d, x0 + bw * .845, base - bh * .56, bh * .40, bh)
    chip(d, x0 + bw * .03, y1 - bh * .36, "KYIV - THE DNIPRO", box_h=bh)


def sc_tanker(d, x0, y0, x1, y1):
    bw, bh = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    d.ellipse([x0 + bw * .86, y0 + bh * .08, x0 + bw * .93, y0 + bh * .30],
              fill=(242, 208, 112))
    sea_y = y0 + bh * 0.52
    d.rectangle([x0, sea_y, x1, y1], fill=SEA)
    waves(d, x0, sea_y + bh * .12, x1, rows=3, bh=bh)
    # a second, distant tanker on the horizon
    dx, dy = x0 + bw * .60, sea_y - bh * .015
    d.polygon([(dx, dy), (dx + bw * .17, dy), (dx + bw * .145, dy + bh * .05),
               (dx + bw * .02, dy + bh * .05)], fill=(96, 108, 120))
    d.rectangle([dx + bw * .115, dy - bh * .055, dx + bw * .135, dy],
                fill=(96, 108, 120))
    hx, hy = x0 + bw * .14, sea_y - bh * .10
    d.polygon([(hx, hy), (hx + bw * .58, hy), (hx + bw * .52, hy + bh * .17),
               (hx + bw * .05, hy + bh * .17)], fill=(44, 44, 46))
    for i in range(3):
        d.rectangle([hx + bw * (.08 + i * .13), hy - bh * .13,
                     hx + bw * (.185 + i * .13), hy], fill=(150, 66, 52))
    d.rectangle([hx + bw * .50, hy - bh * .24, hx + bw * .565, hy], fill=(60, 60, 62))
    d.rectangle([hx + bw * .515, hy - bh * .30, hx + bw * .55, hy - bh * .24], fill=(60, 60, 62))
    d.polygon([(hx + bw * .47, hy - bh * .02), (hx + bw * .50, hy - bh * .14),
               (hx + bw * .525, hy - bh * .02), (hx + bw * .545, hy - bh * .12),
               (hx + bw * .535, hy), (hx + bw * .49, hy)], fill=FIRE)
    smoke(d, hx + bw * .52, hy - bh * .18, bh * .45, bh)
    mx, my = x0 + bw * .845, sea_y + bh * .16
    r = bh * .085
    d.ellipse([mx - r, my - r, mx + r, my + r], fill=INK)
    for ang in range(0, 360, 45):
        import math
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([(mx + dx * r * .8, my + dy * r * .8),
                (mx + dx * r * 1.5, my + dy * r * 1.5)], fill=INK, width=max(2, bh // 60))
    chip(d, x0 + bw * .03, y1 - bh * .36, "STRAIT OF HORMUZ", box_h=bh)


def sc_flags(d, x0, y0, x1, y1):
    bw, bh = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(232, 238, 244))
    d.rectangle([x0, y1 - bh * .16, x1, y1], fill=(120, 96, 60))
    fw, fh = bw * .235, bh * .52
    tops = [y0 + bh * .14, y0 + bh * .10, y0 + bh * .14]
    for i, fx in enumerate((x0 + bw * .06, x0 + bw * .385, x0 + bw * .71)):
        fy = tops[i]
        d.rectangle([fx - bw * .006, fy - bh * .06, fx + bw * .002, y1 - bh * .16], fill=(70, 70, 70))
        if i == 0:      # United States
            for s in range(7):
                d.rectangle([fx, fy + s * fh / 7, fx + fw, fy + (s + 1) * fh / 7],
                            fill=(178, 34, 52) if s % 2 == 0 else (255, 255, 255))
            d.rectangle([fx, fy, fx + fw * .42, fy + fh * .54], fill=(60, 59, 110))
        elif i == 1:    # China
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
            for sx, sy, sr in [(.10, .16, .045), (.24, .08, .028), (.27, .20, .028), (.24, .32, .028)]:
                d.ellipse([fx + fw * sx, fy + fh * sy, fx + fw * (sx + sr * 2), fy + fh * (sy + sr * 2)],
                          fill=(255, 222, 0))
        else:           # Russia
            for s, c in enumerate([(245, 245, 245), (0, 90, 180), (213, 43, 30)]):
                d.rectangle([fx, fy + s * fh / 3, fx + fw, fy + (s + 1) * fh / 3], fill=c)
            d.rectangle([fx, fy, fx + fw, fy + fh], outline=(150, 150, 150), width=2)
    chip(d, x0 + bw * .03, y1 - bh * .36, "SHENZHEN - THURSDAY", box_h=bh)


def sc_carrier(d, x0, y0, x1, y1):
    bw, bh = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    sea_y = y0 + bh * 0.58
    d.rectangle([x0, sea_y, x1, y1], fill=SEA)
    waves(d, x0, sea_y + bh * .14, x1, rows=3, bh=bh)
    hx, hy = x0 + bw * .10, sea_y - bh * .06
    d.polygon([(hx, hy), (hx + bw * .74, hy), (hx + bw * .66, hy + bh * .15),
               (hx + bw * .07, hy + bh * .15)], fill=(46, 48, 52))
    d.rectangle([hx + bw * .52, hy - bh * .17, hx + bw * .60, hy], fill=(46, 48, 52))
    d.line([(hx + bw * .56, hy - bh * .17), (hx + bw * .56, hy - bh * .27)], fill=(46, 48, 52), width=3)
    for jx in (hx + bw * .12, hx + bw * .30):
        d.polygon([(jx, hy - bh * .015), (jx + bw * .075, hy - bh * .075),
                   (jx + bw * .15, hy - bh * .015)], fill=(30, 32, 36))
    for wx in range(int(x0 + bw * .06), int(x0 + bw * .5), int(bw * .09)):
        d.line([(wx, sea_y + bh * .30), (wx + bw * .05, sea_y + bh * .30)],
               fill=(235, 244, 249), width=3)
    chip(d, x0 + bw * .03, y1 - bh * .36, "ARABIAN SEA", box_h=bh)


def sc_pentagon(d, x0, y0, x1, y1):
    bw, bh = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(238, 234, 224))
    cx, cy, r = x0 + bw * .27, y0 + bh * .52, bh * .47
    import math
    pts = [(cx + r * math.cos(math.radians(-90 + 72 * k)),
            cy + r * math.sin(math.radians(-90 + 72 * k))) for k in range(5)]
    d.polygon(pts, fill=(214, 206, 188), outline=INK, width=max(3, bh // 40))
    pts2 = [(cx + r * .55 * math.cos(math.radians(-90 + 72 * k)),
             cy + r * .55 * math.sin(math.radians(-90 + 72 * k))) for k in range(5)]
    d.polygon(pts2, outline=(120, 114, 100), width=max(2, bh // 60))
    d.line([(cx - r * .1, cy - r * .55), (cx + r * .05, cy - r * .1),
            (cx - r * .08, cy + r * .3), (cx + r * .1, cy + r * .62)],
           fill=RED, width=max(3, bh // 36))
    fnt = F(SERIF, int(bh * .34))
    d.text((x0 + bw * .56, y0 + bh * .18), "$4.8tn", font=fnt, fill=INK)
    d.text((x0 + bw * .565, y0 + bh * .56), "IN ASSETS AUDITORS\nCANNOT VERIFY",
           font=F(SANS_B, int(bh * .115)), fill=SOFT)
    chip(d, x0 + bw * .03, y1 - bh * .36, "NINTH YEAR RUNNING", box_h=bh)


def sc_bank(d, x0, y0, x1, y1):
    bw, bh = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(233, 238, 240))
    bx, by = x0 + bw * .16, y0 + bh * .16
    bw2, bh2 = bw * .52, bh * .68
    d.polygon([(bx, by + bh2 * .18), (bx + bw2 * .5, by), (bx + bw2, by + bh2 * .18)], fill=INK)
    d.rectangle([bx, by + bh2 * .18, bx + bw2, by + bh2 * .26], fill=INK)
    for i in range(4):
        cx = bx + bw2 * (.08 + i * .235)
        d.rectangle([cx, by + bh2 * .30, cx + bw2 * .10, by + bh2 * .82], fill=INK)
    d.rectangle([bx - bw2 * .04, by + bh2 * .82, bx + bw2 * 1.04, by + bh2 * .92], fill=INK)
    d.polygon([(bx + bw2 * .30, by + bh2 * .26), (bx + bw2 * .44, by + bh2 * .48),
               (bx + bw2 * .36, by + bh2 * .52), (bx + bw2 * .52, by + bh2 * .80)],
              fill=RED)
    chip(d, x0 + bw * .03, y1 - bh * .36, "A BUG - NOT A HACK", box_h=bh)


def sc_rocket(d, x0, y0, x1, y1):
    bw, bh = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(16, 22, 44))
    seed = 7
    for _ in range(46):
        seed = (seed * 1103515245 + 12345) % (2 ** 31)
        sx = x0 + (seed % 1000) / 1000 * bw
        seed = (seed * 1103515245 + 12345) % (2 ** 31)
        sy = y0 + (seed % 1000) / 1000 * bh
        r = 1.6 if seed % 3 else 2.6
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(210, 220, 240))
    rx, ry = x0 + bw * .30, y0 + bh * .62
    d.polygon([(rx, ry - bh * .34), (rx + bw * .055, ry - bh * .10),
               (rx + bw * .045, ry + bh * .06), (rx - bw * .045, ry + bh * .06),
               (rx - bw * .055, ry - bh * .10)], fill=(228, 230, 234))
    d.ellipse([rx - bw * .016, ry - bh * .24, rx + bw * .016, ry - bh * .15],
              fill=(140, 200, 230))
    d.polygon([(rx - bw * .055, ry - bh * .10), (rx - bw * .10, ry + bh * .03),
               (rx - bw * .045, ry + bh * .02)], fill=RED)
    d.polygon([(rx + bw * .055, ry - bh * .10), (rx + bw * .10, ry + bh * .03),
               (rx + bw * .045, ry + bh * .02)], fill=RED)
    d.polygon([(rx - bw * .02, ry + bh * .06), (rx, ry + bh * .22),
               (rx + bw * .02, ry + bh * .06)], fill=FIRE)
    for i, (sx, sy) in enumerate([(0.60, 0.30), (0.72, 0.48), (0.83, 0.24)]):
        cx, cy = x0 + sx * bw, y0 + sy * bh
        s = bh * .055
        d.rectangle([cx - s, cy - s * .5, cx + s, cy + s * .5], fill=(168, 178, 196))
        d.rectangle([cx - s * 1.7, cy - s * .34, cx - s * 1.1, cy + s * .34], fill=(90, 110, 160))
        d.rectangle([cx + s * 1.1, cy - s * .34, cx + s * 1.7, cy + s * .34], fill=(90, 110, 160))
        d.line([(cx - s * .8, cy - s * .8), (cx + s * .8, cy + s * .8)], fill=RED, width=3)
        d.line([(cx - s * .8, cy + s * .8), (cx + s * .8, cy - s * .8)], fill=RED, width=3)
    chip(d, x0 + bw * .03, y1 - bh * .36, "40 SATELLITES LOST", fill=RED, box_h=bh)


# ------------------------------------------------------------------- map

def project(lon, lat, box):
    x0, y0, x1, y1 = box
    return (x0 + (lon + 168) / 352 * (x1 - x0),
            y0 + (76 - lat) / 128 * (y1 - y0))


CONTINENTS = [
    [(-165, 68), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-79, 62), (-77, 58), (-65, 60), (-56, 52), (-65, 45), (-70, 42),
     (-74, 39), (-76, 35), (-80, 31), (-80, 26), (-84, 22), (-90, 20),
     (-97, 16), (-104, 13), (-96, 8), (-83, 9), (-90, 14), (-104, 19),
     (-111, 24), (-117, 33), (-124, 40), (-124, 48), (-133, 56), (-152, 60)],
    [(-78, 7), (-70, 11), (-61, 9), (-52, 5), (-44, -3), (-35, -8),
     (-39, -15), (-40, -21), (-48, -26), (-55, -34), (-62, -39), (-65, -45),
     (-67, -52), (-71, -54), (-74, -49), (-73, -39), (-72, -29), (-70, -18),
     (-75, -15), (-79, -8), (-80, -4), (-77, 3)],
    [(-9, 43), (-9, 36), (-6, 36), (-2, 37), (3, 39), (0, 40), (-4, 44),
     (-1, 46), (-5, 48), (0, 50), (5, 53), (8, 55), (8, 57), (12, 56),
     (18, 56), (21, 55), (24, 58), (21, 60), (25, 60), (30, 62), (30, 70),
     (45, 68), (58, 64), (66, 60), (60, 52), (52, 50), (44, 48), (36, 46),
     (30, 46), (23, 40), (19, 40), (15, 38), (10, 37), (12, 44), (8, 44),
     (3, 42)],
    [(-5, 50), (-3, 53), (-5, 55), (-8, 58), (-6, 56), (-3, 54), (-1, 51)],
    [(-17, 15), (-16, 21), (-13, 27), (-9, 31), (-6, 34), (0, 36),
     (10, 37), (11, 34), (20, 32), (30, 31), (34, 28), (38, 21), (40, 15),
     (43, 12), (50, 12), (51, 10), (44, 0), (41, -8), (40, -16), (36, -22),
     (33, -27), (28, -33), (20, -35), (18, -32), (16, -27), (14, -18),
     (13, -12), (12, -6), (9, -1), (9, 4), (-8, 4), (-13, 8), (-17, 12)],
    [(36, 36), (30, 36), (36, 33), (43, 38), (48, 39), (50, 30), (56, 26),
     (59, 22), (66, 25), (72, 21), (76, 10), (80, 7), (84, 12), (88, 14),
     (91, 16), (93, 22), (89, 22), (86, 20), (80, 15), (77, 8), (73, 16),
     (69, 22), (61, 25), (57, 27), (52, 29), (50, 36), (44, 46), (40, 50),
     (48, 52), (58, 56), (68, 58), (75, 55), (85, 50), (95, 50), (105, 52),
     (115, 52), (125, 54), (135, 52), (142, 50), (150, 55), (158, 52),
     (162, 58), (170, 62), (178, 66), (169, 66), (160, 62), (152, 58),
     (150, 50), (142, 45), (140, 40), (135, 35), (129, 33), (122, 30),
     (122, 25), (115, 23), (108, 20), (110, 14), (107, 9), (104, 2),
     (100, 6), (98, 10), (94, 17), (92, 21), (97, 28), (97, 33),
     (105, 33), (112, 35), (120, 35), (122, 38), (126, 40), (130, 42),
     (133, 45), (128, 48), (120, 50), (110, 48), (100, 47), (90, 46),
     (80, 45), (70, 46), (60, 48), (50, 48), (42, 46), (36, 42)],
    [(95, 5), (100, 0), (105, -5), (110, -8), (115, -8), (120, -9),
     (125, -9), (131, -3), (136, -2), (141, -3), (146, -6), (150, -9),
     (146, -9), (141, -5), (136, -4), (131, -4), (125, -10), (119, -10),
     (113, -8), (107, -7), (100, -3), (95, 3)],
    [(113, -22), (114, -29), (115, -34), (118, -35), (124, -33), (129, -32),
     (133, -32), (136, -35), (139, -37), (145, -38), (150, -37), (153, -31),
     (153, -26), (151, -22), (146, -19), (143, -14), (142, -11), (137, -12),
     (136, -15), (132, -11), (127, -14), (124, -16), (122, -17), (117, -20)],
]

PINS = [  # (number, lon, lat) for the eight cards; 6-8 nudged apart
    (1, 37, 45), (2, 31, 50), (3, 56, 26), (4, 114, 23),
    (5, 61, 17), (6, -80, 41), (7, -71, 43), (8, -78, 26),
]
DOTS = [  # (lon, lat) for the briefs
    (-122, 37), (-98, 39), (138, 37), (6, 46), (121, 14),
    (-77, 39), (30, -2), (0, 51), (-76, 45),
]


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=OCEAN)
    for poly in CONTINENTS:
        d.polygon([project(lon, lat, box) for lon, lat in poly], fill=LAND)
    for lon, lat in DOTS:
        px, py = project(lon, lat, box)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=NAVY)
    for num, lon, lat in PINS:
        px, py = project(lon, lat, box)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED)
        t = str(num)
        fnt = F(SANS_B, 11)
        tw = d.textlength(t, font=fnt)
        d.text((px - tw / 2, py - 7), t, font=fnt, fill=(255, 255, 255))


# ------------------------------------------------------------------ cards

def card(d, img, box, num, tag, headline, body, painter, tag_color=RED):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=CARD)
    d.rectangle([x0, y0, x1, y0 + 3], fill=INK)
    band_h = int((y1 - y0) * 0.30)
    img.paste(scene(x1 - x0, band_h, painter), (x0, y0 + 3))
    ty = y0 + 3 + band_h + 7
    d.ellipse([x0 + 10, ty, x0 + 30, ty + 20], fill=RED)
    t = str(num)
    fnt = F(SANS_B, 13)
    d.text((x0 + 20 - d.textlength(t, font=fnt) / 2, ty + 2.5), t,
           font=fnt, fill=(255, 255, 255))
    d.text((x0 + 38, ty + 2), tag, font=F(SANS_B, 13.5), fill=tag_color)
    hy = ty + 25
    hf, hlines = fit(d, headline, SERIF, 23, x1 - x0 - 20, 2)
    hy = para(d, x0 + 10, hy, hlines, hf, INK, 25)
    blines = wrap(d, body, F(SANS, 13.5), x1 - x0 - 20)
    para(d, x0 + 10, hy + 3, blines, F(SANS, 13.5), SOFT, 16.5)


def lead_card(d, img, box, num, tag, headline, body, painter):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=CARD)
    d.rectangle([x0, y0, x1, y0 + 4], fill=RED)
    band_h = int((y1 - y0) * 0.38)
    img.paste(scene(x1 - x0, band_h, painter), (x0, y0 + 4))
    ty = y0 + 4 + band_h + 8
    d.ellipse([x0 + 12, ty, x0 + 36, ty + 24], fill=RED)
    t = str(num)
    fnt = F(SANS_B, 15)
    d.text((x0 + 24 - d.textlength(t, font=fnt) / 2, ty + 3), t,
           font=fnt, fill=(255, 255, 255))
    d.text((x0 + 46, ty + 3), tag, font=F(SANS_B, 15), fill=RED)
    hy = ty + 31
    hf, hlines = fit(d, headline, SERIF, 28, x1 - x0 - 24, 2)
    hy = para(d, x0 + 12, hy, hlines, hf, INK, 30)
    blines = wrap(d, body, F(SANS, 14.5), x1 - x0 - 24)
    para(d, x0 + 12, hy + 4, blines, F(SANS, 14.5), SOFT, 18)


# -------------------------------------------------------------------- main

STATS = [
    ("$4.8tn", "Pentagon assets auditors\ncannot verify"),
    ("40", "Amazon satellites lost\non a single rocket"),
    ("3", "U.S. carriers now in\nthe Middle East"),
    ("128", "states in Geneva debate\nkiller robots"),
    ("2nd", "day of strikes on the\nKerch Bridge to Crimea"),
]

BRIEFS = [
    (9, "Nvidia", "first results since Huang stepped down"),
    (10, "Measles", "U.S. cases highest since 1991"),
    (11, "Japan", "jets up after Russian airspace breach"),
    (12, "Geneva", "128 states debate killer robots"),
    (13, "Manila", "Trump lands for ASEAN summit"),
    (14, "CNN", "Iran weighing a \u201cdirty bomb\u201d, U.S. says"),
    (15, "Europe", "Rwanda migrant return hub planned"),
    (16, "Britain", "sanctions 8 settlement firms"),
    (17, "Xi-Carney", "tariff cuts agreed"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- kicker ----
    d.text((M, 12), "THE WORLD'S NEWS IN ONE PICTURE", font=F(SANS_B, 15), fill=RED)
    right = "17 STORIES \u00b7 6 REGIONS \u00b7 ALL FROM TUESDAY"
    d.text((W - M - d.textlength(right, font=F(SANS_B, 15)), 12), right,
           font=F(SANS_B, 15), fill=INK)

    # ---- masthead ----
    title = "Tuesday 17 November 2026"
    tf, _ = fit(d, title, SERIF, 104, CW, 1)
    d.text((M - 2, 34), title, font=tf, fill=INK)
    d.rectangle([M, 128, W - M, 133], fill=INK)
    d.rectangle([M, 136, W - M, 138], fill=INK)

    # ---- the day in figures ----
    sy = 144
    colw = CW / 5
    for i, (num, label) in enumerate(STATS):
        x = M + i * colw
        if i:
            d.line([(x, sy), (x, sy + 56)], fill=FAINT, width=2)
        d.text((x + 12, sy), num, font=F(SERIF, 31), fill=INK)
        ly = sy + 36
        for line in label.split("\n"):
            d.text((x + 12, ly), line, font=F(SANS, 11), fill=SOFT)
            ly += 13.5
    d.rectangle([M, 204, W - M, 206], fill=FAINT)

    # ---- lead row ----
    lw = (CW - 12) // 2
    lead_card(d, img, (M, 212, M + lw, 442), 1, "EUROPE \u00b7 WAR IN UKRAINE",
              "Ukraine strikes the Crimean Bridge; a span falls",
              "A second day of strikes on the Kerch Bridge to Crimea: a road "
              "span collapses into the strait.", sc_kerch)
    lead_card(d, img, (M + lw + 12, 212, W - M, 442), 2, "EUROPE \u00b7 WAR IN UKRAINE",
              "Kyiv's Dnipro bridges hit; heat and power cut",
              "Russian missiles strike the capital's bridges over the "
              "Dnipro, cutting heat, water and power.", sc_kyiv)

    # ---- card rows ----
    cw3 = (CW - 24) // 3
    xs = [M, M + cw3 + 12, M + 2 * cw3 + 24]
    row_a = [
        (3, "MIDDLE EAST \u00b7 HORMUZ", "Tankers hit by mines near Hormuz",
         "Iran says tankers struck mines near Hormuz; drones at a U.S. "
         "base in Bahrain were stopped.", sc_tanker, RED),
        (4, "ASIA \u00b7 DIPLOMACY", "Three leaders, one table: Shenzhen, Thursday",
         "China confirms Xi, Trump and Putin meet in Shenzhen Thursday, "
         "on APEC's sidelines.", sc_flags, NAVY),
        (5, "MIDDLE EAST \u00b7 U.S. NAVY", "A third U.S. carrier reaches the Middle East",
         "USS Theodore Roosevelt joins two in the region - the first "
         "three-carrier force since April.", sc_carrier, NAVY),
    ]
    row_b = [
        (6, "UNITED STATES \u00b7 DEFENCE", "Pentagon fails its audit for a ninth year",
         "Auditors cannot verify accounts covering $4.8 trillion in "
         "assets.", sc_pentagon, RED),
        (7, "UNITED STATES \u00b7 BANKING", "JPMorgan outage was a bug, not a hack",
         "A software bug slowed online banking and Zelle payments on "
         "Monday, the bank says.", sc_bank, NAVY),
        (8, "SPACE \u00b7 TECHNOLOGY", "Rocket fails; 40 Amazon satellites lost",
         "A ULA Vulcan rocket failed in flight, destroying 40 Amazon "
         "satellites.", sc_rocket, NAVY),
    ]
    for row, y0 in ((row_a, 450), (row_b, 640)):
        for j, (num, tag, head, body, painter, tc) in enumerate(row):
            card(d, img, (xs[j], y0, xs[j] + cw3, y0 + 182), num, tag, head,
                 body, painter, tag_color=tc)

    # ---- bottom: map + briefs ----
    by = 832
    d.rectangle([M, by, M + 400, 972], fill=CARD)
    d.rectangle([M, by, M + 400, by + 3], fill=INK)
    d.text((M + 10, by + 8), "WHERE IT HAPPENED", font=F(SANS_B, 13), fill=INK)
    draw_map(d, (M + 10, by + 30, M + 390, by + 118))
    d.text((M + 10, by + 122), "Pins 1-8 are the stories above; dots are the briefs.",
           font=F(SANS_I, 11), fill=SOFT)

    bx = M + 412
    d.rectangle([bx, by, W - M, 972], fill=CARD)
    d.rectangle([bx, by, W - M, by + 3], fill=INK)
    d.text((bx + 10, by + 8), "ALSO ON TUESDAY 17 NOVEMBER", font=F(SANS_B, 13), fill=RED)
    col_w = (W - M - bx - 30) // 2
    for k, (num, lead, text) in enumerate(BRIEFS):
        cx = bx + 10 + (k // 5) * (col_w + 10)
        cy = by + 32 + (k % 5) * 21.5
        d.ellipse([cx, cy + 1, cx + 15, cy + 16], fill=NAVY)
        t = str(num)
        fnt = F(SANS_B, 9.5)
        d.text((cx + 7.5 - d.textlength(t, font=fnt) / 2, cy + 3), t,
               font=fnt, fill=(255, 255, 255))
        line = lead + " - " + text
        lf, llines = fit(d, line, SANS, 12.5, col_w - 22, 1, floor=10)
        d.text((cx + 21, cy + 2), llines[0], font=lf, fill=INK)

    # ---- footer ----
    d.rectangle([M, 980, W - M, 982], fill=INK)
    d.text((M, 988),
           "Every story on this page happened or was first reported on Tuesday "
           "17 November 2026. Contested claims are attributed.",
           font=F(SANS_I, 12.5), fill=SOFT)
    right = "ONE DAY \u00b7 ONE PICTURE"
    d.text((W - M - d.textlength(right, font=F(SANS_B, 12.5)), 988), right,
           font=F(SANS_B, 12.5), fill=INK)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
