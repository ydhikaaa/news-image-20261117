"""Draw the entry image: one picture summing up the world news of
Tuesday 17 November 2026. Pure Pillow, deterministic output.

Run:  python3 make_image.py            (writes entry.png, 1024x1024)
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
NAVY2 = (28, 48, 88)
GOLD = (198, 156, 66)
RED = (179, 32, 44)
GREY = (90, 88, 82)
LINE = (200, 192, 175)
WHITE = (255, 255, 255)
SKY = (214, 228, 238)
SEA = (148, 178, 198)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SANS_OB = lambda s: font("DejaVuSans.ttf", s)  # no oblique face shipped; regular


def text_wrap(draw, text, fnt, max_w):
    """Wrap text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
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


def para(draw, xy, text, fnt, color, max_w, leading):
    x, y = xy
    for line in text_wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def letterspaced(draw, xy, text, fnt, color, spacing=4):
    """Draw text with extra tracking (for the masthead kicker)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=color)
        x += draw.textlength(ch, font=fnt) + spacing
    return x


def draw_bridge_scene(draw, box):
    """A bridge over water with its middle span broken and smoking.
    All geometry is relative to the box, so it fits any panel height."""
    x0, y0, x1, y1 = box
    bh = y1 - y0
    draw.rectangle(box, fill=SKY)
    # sun
    draw.ellipse([x1 - 78, y0 + 10, x1 - 34, y0 + 54], fill=(240, 205, 110))
    deck_y = y0 + int(bh * 0.60)
    tower_h = int(bh * 0.42)
    # distant shore, then water
    draw.rectangle([x0, deck_y + 6, x1, deck_y + 16], fill=(178, 190, 168))
    draw.rectangle([x0, deck_y + 16, x1, y1], fill=SEA)
    for wy in (deck_y + 30, deck_y + 44, deck_y + 56):
        if wy < y1 - 4:
            for wx in range(x0 + 8, x1 - 40, 64):
                draw.line([(wx, wy), (wx + 34, wy)], fill=(220, 232, 240), width=3)
    # towers
    for tx in (x0 + 52, x1 - 92):
        draw.rectangle([tx, deck_y - tower_h, tx + 12, deck_y], fill=INK)
        draw.rectangle([tx - 6, deck_y - tower_h - 8, tx + 18,
                        deck_y - tower_h], fill=INK)
    # cables (a few, from each tower to the deck)
    for cx in range(x0 + 90, x1 - 90, 52):
        draw.line([(x0 + 58, deck_y - tower_h), (cx, deck_y)],
                  fill=(110, 110, 110), width=2)
        draw.line([(x1 - 86, deck_y - tower_h), (cx, deck_y)],
                  fill=(110, 110, 110), width=2)
    # deck: left part intact, middle span broken and tilted into the water
    draw.rectangle([x0, deck_y, x0 + 180, deck_y + 14], fill=(60, 60, 60))
    draw.rectangle([x1 - 160, deck_y, x1, deck_y + 14], fill=(60, 60, 60))
    # broken span, a narrow slab tilted down into the water
    draw.polygon([(x0 + 186, deck_y + 2), (x0 + 224, deck_y + 2),
                  (x0 + 242, y1 - 10), (x0 + 210, y1 - 8)], fill=(90, 40, 36))
    # splash where the slab meets the water
    for sx in (x0 + 208, x0 + 228, x0 + 246):
        draw.line([(sx, y1 - 12), (sx + 10, y1 - 12)], fill=WHITE, width=2)
    # smoke from the break
    for i, (sx, sy, sr) in enumerate([(x0 + 222, deck_y - 22, 13),
                                      (x0 + 238, deck_y - 40, 16),
                                      (x0 + 258, deck_y - 56, 19)]):
        if sy - sr > y0:
            draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                         fill=(120, 120, 118))
    # small explosion flash at the break
    draw.polygon([(x0 + 212, deck_y - 4), (x0 + 222, deck_y - 20),
                  (x0 + 230, deck_y - 6), (x0 + 242, deck_y - 18),
                  (x0 + 238, deck_y), (x0 + 226, deck_y + 2)],
                 fill=(232, 130, 40))


def icon_tanker(draw, x, y, s=1.0):
    """Small oil tanker on waves."""
    w, h = int(74 * s), int(46 * s)
    draw.rectangle([x, y + 22, x + w, y + 36], fill=(40, 40, 40))
    draw.rectangle([x + 8, y + 10, x + 30, y + 22], fill=(120, 60, 50))
    draw.rectangle([x + 34, y + 14, x + 52, y + 22], fill=(120, 60, 50))
    draw.rectangle([x + 56, y + 4, x + 62, y + 22], fill=(40, 40, 40))
    for wy in (y + 40, y + 44):
        draw.line([(x, wy), (x + w, wy)], fill=SEA, width=2)


def icon_flags(draw, x, y):
    """Three small flags: United States, China, Russia."""
    # US: stripes + blue canton
    for i in range(5):
        draw.rectangle([x, y + i * 6, x + 34, y + i * 6 + 3],
                       fill=RED if i % 2 == 0 else WHITE)
    draw.rectangle([x, y, x + 15, y + 13], fill=NAVY2)
    # China: red with small stars
    draw.rectangle([x + 42, y, x + 76, y + 30], fill=(222, 41, 16))
    for sx, sy in [(50, 8), (58, 6), (62, 12), (56, 16)]:
        draw.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=(255, 222, 0))
    # Russia: white-blue-red tricolour
    for i, c in enumerate([WHITE, (0, 90, 180), RED]):
        draw.rectangle([x + 84, y + i * 10, x + 118, y + i * 10 + 10], fill=c)
    draw.rectangle([x + 84, y, x + 118, y + 30], outline=INK, width=1)


def icon_carrier(draw, x, y):
    """Aircraft carrier silhouette."""
    draw.rectangle([x, y + 26, x + 96, y + 38], fill=(50, 50, 50))
    draw.polygon([(x, y + 26), (x + 96, y + 26), (x + 88, y + 38),
                  (x + 8, y + 38)], fill=(50, 50, 50))
    draw.rectangle([x + 62, y + 12, x + 78, y + 26], fill=(50, 50, 50))
    draw.line([(x + 70, y + 12), (x + 70, y + 4)], fill=(50, 50, 50), width=3)
    draw.line([(x, y + 42), (x + 96, y + 42)], fill=SEA, width=2)


def icon_pentagon(draw, x, y):
    """Pentagon building outline with a crack."""
    pts = [(x + 30, y), (x + 60, y + 22), (x + 48, y + 56),
           (x + 12, y + 56), (x, y + 22)]
    draw.polygon(pts, outline=INK, width=3)
    draw.polygon([(x + 30, y + 18), (x + 44, y + 30), (x + 38, y + 44),
                  (x + 22, y + 44), (x + 16, y + 30)], outline=GREY, width=2)
    draw.line([(x + 30, y + 18), (x + 24, y + 34), (x + 34, y + 44)],
              fill=RED, width=3)


def icon_bank(draw, x, y):
    """Bank building: pediment and columns."""
    draw.polygon([(x, y + 14), (x + 30, y), (x + 60, y + 14)], fill=INK)
    draw.rectangle([x + 2, y + 14, x + 58, y + 18], fill=INK)
    for cx in (x + 6, x + 20, x + 34, x + 48):
        draw.rectangle([cx, y + 20, cx + 6, y + 44], fill=INK)
    draw.rectangle([x, y + 44, x + 60, y + 48], fill=INK)


def icon_rocket(draw, x, y):
    """Rocket climbing, with a broken trail."""
    draw.polygon([(x + 30, y), (x + 42, y + 26), (x + 36, y + 40),
                  (x + 24, y + 40), (x + 18, y + 26)], fill=INK)
    draw.ellipse([x + 26, y + 12, x + 34, y + 20], fill=(140, 200, 230))
    draw.polygon([(x + 18, y + 26), (x + 10, y + 38), (x + 18, y + 34)], fill=RED)
    draw.polygon([(x + 42, y + 26), (x + 50, y + 38), (x + 42, y + 34)], fill=RED)
    draw.polygon([(x + 26, y + 40), (x + 30, y + 52), (x + 34, y + 40)],
                 fill=(232, 130, 40))
    for i in range(3):
        draw.ellipse([x + 24 + i * 4, y + 56 + i * 8, x + 32 + i * 4,
                      y + 62 + i * 8], fill=(180, 180, 175))


def panel(draw, box, tag, headline, body, icon=None, accent=RED):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=WHITE, outline=LINE, width=2)
    draw.rectangle([x0, y0, x1, y0 + 6], fill=accent)
    cx = x0 + 16
    cy = y0 + 12
    if icon is not None:
        # Draw the icon on a small canvas, then shrink it to a uniform strip.
        tmp = Image.new("RGB", (130, 70), WHITE)
        d2 = ImageDraw.Draw(tmp)
        icon(d2, 5, 5)
        tmp = tmp.resize((84, 42), Image.LANCZOS)
        img.paste(tmp, (cx, cy))
        cy += 42
    draw.text((cx, cy), tag, font=F_SANS_B(14), fill=accent)
    cy += 18
    cy = para(draw, (cx, cy), headline, F_SANS_B(23), INK, x1 - x0 - 32, 24)
    para(draw, (cx, cy + 3), body, F_SANS(15), (52, 52, 52),
         x1 - x0 - 32, 17)


def main():
    global img
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead ----
    draw.rectangle([0, 0, W, 136], fill=NAVY)
    letterspaced(draw, (28, 12), "THE WORLD IN ONE DAY", F_SANS_B(23),
                 (200, 210, 230), spacing=6)
    date_size = 54
    while (draw.textlength("TUESDAY 17 NOVEMBER 2026",
                           font=F_SERIF_B(date_size)) > W - 56
           and date_size > 30):
        date_size -= 1
    draw.text((28, 40), "TUESDAY 17 NOVEMBER 2026", font=F_SERIF_B(date_size),
              fill=WHITE)
    draw.text((28, 104), "One day. One picture. The news the world woke up to.",
              font=F_SANS_OB(18), fill=(180, 195, 220))
    draw.rectangle([0, 136, W, 142], fill=GOLD)

    # ---- Lead story: bridges ----
    lx0, ly0, lx1, ly1 = 24, 152, 1000, 384
    draw.rectangle([lx0, ly0, lx1, ly1], fill=WHITE, outline=LINE, width=2)
    draw.rectangle([lx0, ly0, lx1, ly0 + 6], fill=RED)
    draw_bridge_scene(draw, (lx0 + 16, ly0 + 48, lx0 + 430, ly1 - 32))
    tx = lx0 + 452
    draw.text((tx, ly0 + 18), "EUROPE  •  WAR IN UKRAINE", font=F_SANS_B(16),
              fill=RED)
    y = para(draw, (tx, ly0 + 40), "BRIDGES FALL AS THE WAR ESCALATES",
             F_SANS_B(38), INK, lx1 - tx - 18, 42)
    para(draw, (tx, y + 6),
         "Ukraine strikes the Kerch Bridge to Crimea for a second day — "
         "a road span collapses. Russian missiles hit Kyiv's bridges over "
         "the Dnipro, cutting heat, water and power.",
         F_SANS(18), (52, 52, 52), lx1 - tx - 18, 22)
    draw.text((lx0 + 16, ly1 - 26), "Kerch Bridge, Crimea — struck twice in 24 hours",
              font=F_SANS_OB(15), fill=GREY)

    # ---- Row 2 ----
    gap, pw = 12, 312
    y0, y1 = 396, 584
    boxes = [(24 + i * (pw + gap), y0, 24 + (i + 1) * pw + i * gap, y1)
             for i in range(3)]
    panel(draw, boxes[0], "MIDDLE EAST  •  HORMUZ",
          "TANKERS HIT BY MINES",
          "Iran says tankers hit mines near the Strait of Hormuz; drones "
          "fired at a U.S. base in Bahrain are stopped.",
          icon=icon_tanker)
    panel(draw, boxes[1], "ASIA  •  DIPLOMACY",
          "THREE LEADERS, ONE TABLE",
          "China confirms Xi, Trump and Putin will meet in Shenzhen on "
          "Thursday, on the sidelines of APEC.",
          icon=icon_flags, accent=NAVY2)
    panel(draw, boxes[2], "MIDDLE EAST  •  U.S. NAVY",
          "THIRD U.S. CARRIER ARRIVES",
          "USS Theodore Roosevelt joins two carriers in the region — the "
          "first three-carrier force there since April.",
          icon=icon_carrier, accent=NAVY2)

    # ---- Row 3 ----
    y0, y1 = 596, 776
    boxes = [(24 + i * (pw + gap), y0, 24 + (i + 1) * pw + i * gap, y1)
             for i in range(3)]
    panel(draw, boxes[0], "UNITED STATES  •  DEFENCE",
          "PENTAGON FAILS ITS AUDIT — AGAIN",
          "Ninth straight year. Auditors cannot verify accounts covering "
          "$4.8 trillion in assets.",
          icon=icon_pentagon)
    panel(draw, boxes[1], "UNITED STATES  •  BANKING",
          "BUG, NOT A HACK",
          "JPMorgan blames a software bug for Monday's banking outage; "
          "online banking and Zelle payments slowed.",
          icon=icon_bank, accent=NAVY2)
    panel(draw, boxes[2], "SPACE  •  TECHNOLOGY",
          "ROCKET LOST, 40 SATELLITES GONE",
          "A ULA Vulcan rocket fails in flight, destroying 40 Amazon "
          "internet satellites.",
          icon=icon_rocket, accent=NAVY2)

    # ---- Also today strip ----
    sx0, sy0, sx1, sy1 = 24, 788, 1000, 872
    draw.rectangle([sx0, sy0, sx1, sy1], fill=(232, 226, 210),
                   outline=LINE, width=2)
    draw.text((sx0 + 16, sy0 + 8), "ALSO ON 17 NOVEMBER",
              font=F_SANS_B(15), fill=RED)
    para(draw, (sx0 + 16, sy0 + 30),
         "Nvidia reports after the close — first earnings since Jensen "
         "Huang stepped down  •  U.S. measles cases highest since 1991  •  "
         "Japan scrambles jets after Russian airspace violation  •  Five "
         "European states plan a Rwanda migrant return hub  •  U.K. "
         "sanctions eight firms building West Bank settlements",
         F_SANS(16), INK, sx1 - sx0 - 32, 19)

    # ---- Around the world in brief ----
    sx0, sy0, sx1, sy1 = 24, 884, 1000, 966
    draw.rectangle([sx0, sy0, sx1, sy1], fill=WHITE,
                   outline=LINE, width=2)
    draw.text((sx0 + 16, sy0 + 8), "AROUND THE WORLD IN BRIEF",
              font=F_SANS_B(15), fill=NAVY2)
    para(draw, (sx0 + 16, sy0 + 30),
         "U.S. officials tell CNN Iran is weighing a “dirty bomb” attack "
         "in Washington  •  Trump lands in Manila for ASEAN  •  "
         "128 states meet in Geneva on killer robots  •  "
         "Xi and Carney agree tariff cuts",
         F_SANS(16), INK, sx1 - sx0 - 32, 19)

    # ---- Footer ----
    draw.text((24, 976), "The world news of Tuesday 17 November 2026, as reported that day.",
              font=F_SANS_OB(15), fill=GREY)
    draw.text((700, 976), "make.fun  •  news-image-20261117",
              font=F_SANS(15), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
