#!/usr/bin/env python3
"""Draw entry.png for news-image-20261119.

One image summing up the world's news of Thursday 19 November 2026:
a news-atlas front page -- masthead with the date, a lead strip on the
Trump-Xi-Putin meeting in Shenzhen, six story tiles with flat pictograms,
and an "also today" ticker. Pure Pillow, no network, no randomness:
the same run writes the same bytes.

Run: python3 draw.py   (writes entry.png next to this file)
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (27, 27, 27)
NAVY = (22, 35, 63)
RED = (180, 35, 24)
AMBER = (232, 163, 61)
GREY = (91, 103, 112)
CARD = (255, 255, 255)
BORDER = (203, 196, 182)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
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


def text_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    for i in range(0, 7):
        yy = y + i * h / 13 * 2
        if yy < y + h:
            d.rectangle([x, yy, x + w, min(yy + h / 13, y + h)], fill=(178, 34, 52))
    d.rectangle([x, y, x + w * 0.4, y + h * 7 / 13], fill=(28, 48, 94))
    for r in range(3):
        for c in range(4):
            cx = x + 8 + c * 13
            cy = y + 7 + r * 11
            d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=(120, 120, 120), width=1)


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.polygon([(x + 14, y + 8), (x + 17, y + 16), (x + 25, y + 16), (x + 19, y + 21),
               (x + 21, y + 29), (x + 14, y + 24), (x + 7, y + 29), (x + 9, y + 21),
               (x + 3, y + 16), (x + 11, y + 16)], fill=(255, 222, 0))
    for sx, sy in ((44, 12), (52, 20), (52, 30), (44, 38)):
        d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2], fill=(255, 222, 0))
    d.rectangle([x, y, x + w, y + h], outline=(120, 120, 120), width=1)


def flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))
    d.rectangle([x, y, x + w, y + h], outline=(120, 120, 120), width=1)


def pic_scales(d, x, y, s, col):
    cx, cy = x + s / 2, y + s / 2
    d.line([cx, y + 12, cx, y + s - 16], fill=col, width=4)
    d.line([x + 10, y + 22, x + s - 10, y + 22], fill=col, width=4)
    d.ellipse([cx - 4, y + 8, cx + 4, y + 16], fill=col)
    for px in (x + 12, x + s - 28):
        d.line([px + 8, y + 22, px, y + 44], fill=col, width=3)
        d.line([px + 8, y + 22, px + 16, y + 44], fill=col, width=3)
        d.arc([px - 2, y + 38, px + 18, y + 56], 0, 180, fill=col, width=3)
    d.line([x + 16, y + s - 14, x + s - 16, y + s - 14], fill=col, width=4)


def pic_chart(d, x, y, s, col):
    d.line([x + 14, y + s - 16, x + s - 12, y + s - 16], fill=col, width=4)
    d.line([x + 14, y + s - 16, x + 14, y + 14], fill=col, width=4)
    pts = [(x + 18, y + s - 30), (x + 32, y + s - 42), (x + 46, y + s - 36),
           (x + 60, y + s - 54), (x + s - 16, y + 18)]
    d.line(pts, fill=col, width=5, joint="curve")
    d.polygon([(x + s - 16, y + 18), (x + s - 30, y + 18), (x + s - 16, y + 32)], fill=col)


def pic_bridge(d, x, y, s, col):
    d.line([x + 10, y + s - 26, x + s - 10, y + s - 26], fill=col, width=5)
    d.arc([x + 14, y + 26, x + s - 14, y + s - 10], 180, 360, fill=col, width=4)
    for vx in (x + 24, x + s / 2, x + s - 24):
        d.line([vx, y + 34, vx, y + s - 26], fill=col, width=3)
    d.rectangle([x + 18, y + 14, x + 26, y + s - 26], fill=col)
    d.rectangle([x + s - 26, y + 14, x + s - 18, y + s - 26], fill=col)


def pic_controller(d, x, y, s, col):
    d.rounded_rectangle([x + 10, y + 24, x + s - 10, y + s - 22], radius=18, fill=col)
    d.rectangle([x + 22, y + 42, x + 30, y + 58], fill=PAPER)
    d.rectangle([x + 16, y + 46, x + 36, y + 54], fill=PAPER)
    d.ellipse([x + s - 34, y + 40, x + s - 26, y + 48], fill=(255, 200, 60))
    d.ellipse([x + s - 46, y + 50, x + s - 38, y + 58], fill=(255, 255, 255))


def pic_capitol(d, x, y, s, col):
    cx = x + s / 2
    d.pieslice([cx - 22, y + 12, cx + 22, y + 56], 180, 360, fill=col)
    d.rectangle([cx - 26, y + 34, cx + 26, y + 40], fill=col)
    for i in range(5):
        px = x + 16 + i * 13
        d.rectangle([px, y + 44, px + 6, y + s - 22], fill=col)
    d.rectangle([x + 12, y + s - 22, x + s - 12, y + s - 16], fill=col)
    d.rectangle([cx - 2, y + 6, cx + 2, y + 14], fill=col)


def pic_cyclone(d, x, y, s, col):
    cx, cy = x + s / 2, y + s / 2
    for r, a0, a1 in ((30, 20, 200), (22, 140, 320), (14, 260, 380), (7, 20, 200)):
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=col, width=4)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=col)


TILES = [
    ("THE HAGUE", "World court rules on the Rohingya case",
     "Gambia's case, filed in 2019, reaches judgment day.",
     (14, 124, 123), pic_scales),
    ("WALL STREET", "Anthropic's $83 IPO starts trading",
     "A record $81.3bn listing debuts on Nasdaq as ANT.",
     (36, 86, 166), pic_chart),
    ("CRIMEA", "Bridge hit again, traffic halted",
     "A new attack on the Kerch bridge, Russian officials say.",
     (91, 103, 112), pic_bridge),
    ("VICE CITY", "GTA VI launches worldwide",
     "After 13 years, gamers enter Vice City at last.",
     (108, 74, 176), pic_controller),
    ("WASHINGTON", "Jeffries nominated for Speaker",
     "Democrats pick the first Black American for the post.",
     (46, 125, 50), pic_capitol),
    ("BAY OF BENGAL", "Cyclone Akvan nears India",
     "Landfall expected between Machilipatnam and Puri.",
     (194, 87, 27), pic_cyclone),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # side margin

    # ---- masthead ------------------------------------------------------
    d.rectangle([mx, 24, W - mx, 122], fill=NAVY)
    d.rectangle([mx, 24, W - mx, 122], outline=(0, 0, 0), width=2)
    f_title = font(SERIF_B, 56)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 32), title, font=f_title, fill=(255, 255, 255))
    f_date = font(SANS_B, 24)
    date = "T H U R S D A Y  ·  1 9  N O V E M B E R  2 0 2 6"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 88), date, font=f_date, fill=AMBER)

    # ---- standfirst ----------------------------------------------------
    f_stand = font(SERIF, 22)
    stand = "Six stories, one day — from Shenzhen to The Hague."
    sw = d.textlength(stand, font=f_stand)
    d.text(((W - sw) / 2, 132), stand, font=f_stand, fill=GREY)

    # ---- lead strip: Shenzhen trilateral -------------------------------
    ly, lh = 164, 170
    d.rectangle([mx, ly, W - mx, ly + lh], fill=CARD, outline=BORDER, width=2)
    d.rectangle([mx, ly, mx + 10, ly + lh], fill=RED)
    fx = mx + 26
    f_flag = font(SANS_B, 15)
    flag_us(d, fx, ly + 20, 88, 54)
    d.text((fx, ly + 78), "TRUMP", font=f_flag, fill=INK)
    flag_cn(d, fx, ly + 96, 88, 54)
    d.text((fx, ly + 152), "XI", font=f_flag, fill=INK)
    flag_ru(d, fx + 100, ly + 20, 88, 54)
    d.text((fx + 100, ly + 78), "PUTIN", font=f_flag, fill=INK)
    tx = mx + 268
    d.text((tx, ly + 16), "LEAD  ·  SHENZHEN", font=font(SANS_B, 19), fill=RED)
    f_lead = font(SERIF_B, 37)
    d.text((tx, ly + 42), "Three leaders, one table", font=f_lead, fill=INK)
    f_ldeck = font(SANS, 21)
    deck = ("Trump, Xi and Putin meet as the APEC summit opens — "
            "a handshake and a hug on the tarmac, then talks.")
    lines = wrap(d, deck, f_ldeck, W - mx - tx - 24)
    text_block(d, (tx, ly + 92), lines, f_ldeck, (60, 60, 60), 27)

    # ---- story tiles ---------------------------------------------------
    gx, gy = mx, 350
    tw_, th_, gap = 472, 164, 20
    f_tag = font(SANS_B, 17)
    f_head = font(SERIF_B, 25)
    f_deck = font(SANS, 19)
    for i, (tag, head, deck, accent, pic) in enumerate(TILES):
        col = i % 2
        row = i // 2
        x = gx + col * (tw_ + gap)
        y = gy + row * (th_ + gap)
        d.rectangle([x, y, x + tw_, y + th_], fill=CARD, outline=BORDER, width=2)
        d.rectangle([x, y, x + tw_, y + 6], fill=accent)
        # pictogram panel
        px, py, ps = x + 18, y + 34, 104
        d.rounded_rectangle([px, py, px + ps, py + ps], radius=12, fill=accent)
        pic(d, px, py, ps, (255, 255, 255))
        tx2 = x + 140
        d.text((tx2, y + 20), tag, font=f_tag, fill=accent)
        hlines = wrap(d, head, f_head, tw_ - 158)
        yy = text_block(d, (tx2, y + 46), hlines[:2], f_head, INK, 30)
        dlines = wrap(d, deck, f_deck, tw_ - 158)
        text_block(d, (tx2, yy + 6), dlines[:2], f_deck, (60, 60, 60), 24)

    # ---- ticker --------------------------------------------------------
    ty = 894
    d.rectangle([mx, ty, W - mx, ty + 74], fill=NAVY)
    f_tick = font(SANS, 20)
    f_tick_b = font(SANS_B, 20)
    d.text((mx + 18, ty + 11), "ALSO TODAY — ",
           font=f_tick_b, fill=AMBER)
    w_label = d.textlength("ALSO TODAY — ", font=f_tick_b)
    d.text((mx + 18 + w_label, ty + 11),
           "Voyager 1 reaches one light-day  ·  Israeli ground operation in Gaza",
           font=f_tick, fill=(255, 255, 255))
    d.text((mx + 18, ty + 42),
           "EU proposes €45bn Ukraine loan  ·  Van Gogh sells for a record $190.4m",
           font=f_tick, fill=(255, 255, 255))

    # ---- footer --------------------------------------------------------
    f_foot = font(SANS, 16)
    foot = "Drawn from reports published 19 November 2026  ·  One image, one day"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 978), foot, font=f_foot, fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
