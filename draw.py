#!/usr/bin/env python3
"""Draw the news-image-20261121 front page (1024x1024 PNG) with PIL.

A newspaper front page summing up Saturday 21 November 2026's world news.
Every story below happened, or was first reported, on 21 November 2026
(in any time zone), verified against live reporting before drawing:

  1. LEAD, POLAND: two Russian missiles and a suspected jet-powered drone
     come down in south-east Poland during a huge overnight attack on
     Ukraine (400+ drones, 110 missiles; 8 killed in Ukraine). PM Donald
     Tusk calls it a deliberate provocation; NATO chief Mark Rutte calls
     it a grave violation of Polish airspace. No one hurt in Poland.
     (AP / The Times / SOFREP, 21 Nov roundups.)
  2. MARKETS: US stocks fall about 3.7% on Friday; the S&P 500 and the
     Dow enter correction territory as AI shares sell off. (One Turn /
     AP roundup, 21 Nov.)
  3. CYBER: JPMorgan Chase, Visa and Mastercard disclose breaches at
     third-party vendors; extortion group "n0n" claims customer data of
     16,000+ JPMorgan customers leaked. No card numbers exposed; payment
     networks unaffected. (Reuters / Security Affairs / TechSpot.)
  4. CRICKET, WELLINGTON: New Zealand 368 (Henry Nicholls 175*,
     Glenn Phillips 118); India reply 159/1 at stumps on Day 2
     (Yashasvi Jaiswal 85, KL Rahul 52*). (Cricbuzz / BCCI.)
  5. CLIMATE, ANTALYA: COP31 talks enter their crucial final stage;
     fossil fuels and climate finance the sticking points.
     (Jagran Josh 21 Nov roundup.)
  6. AID, BRUSSELS: the EU completes its largest-ever reforms payout
     to Ukraine, nearly 8 billion euros.
  FOOTER: Cyclone Akvan weakens to a deep depression over Odisha with
  no major damage reported; 39 trains cancelled across 20-21 Nov.
  Hyundai unveils the 2027 Elantra at the Los Angeles Auto Show.

The image is drawn entirely by this script: vector shapes and DejaVu
system fonts, no photograph, no copied artwork.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (176, 42, 32)
NAVY = (28, 47, 94)
BLUE = (36, 86, 166)
TEAL = (14, 110, 110)
SKY = (208, 224, 236)
GOLD = (201, 162, 39)
GREY = (96, 90, 78)
LIGHT = (233, 226, 210)
GREEN = (34, 120, 58)
DARKPANEL = (24, 36, 68)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, lines, font, fill, leading=None):
    lh = leading or int(font.size * 1.24)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- frame ----------
d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
d.rectangle([18, 18, W - 19, H - 19], outline=INK, width=1)

# ---------- masthead ----------
d.text((W // 2, 36), "O N E   D A Y   \u2022   O N E   I M A G E",
       font=fnt(SANS_B, 21), fill=RED, anchor="ma")
d.text((W // 2, 64), "21 NOVEMBER 2026", font=fnt(SERIF_B, 70),
       fill=INK, anchor="ma")
d.line([(60, 150), (W - 60, 150)], fill=INK, width=3)
d.line([(60, 156), (W - 60, 156)], fill=INK, width=1)
d.text((W // 2, 166), "SATURDAY  \u2022  THE DAY'S WORLD NEWS, AT A GLANCE",
       font=fnt(SANS_B, 19), fill=NAVY, anchor="ma")

# ---------- lead: missiles in Poland ----------
LX, LY, LW, LH = 30, 196, W - 60, 214
d.rectangle([LX, LY, LX + LW, LY + LH], outline=INK, width=2)
d.text((48, 210), "POLAND  \u2022  NATO AIRSPACE", font=fnt(SANS_B, 19), fill=RED)
d.text((48, 236), "RUSSIAN MISSILES", font=fnt(SERIF_B, 40), fill=INK)
d.text((48, 280), "LAND IN POLAND", font=fnt(SERIF_B, 40), fill=INK)
lead = ("Two missiles and a drone come down in the south-east during a "
        "huge overnight attack on Ukraine. Tusk: deliberate provocation; "
        "NATO: a grave violation.")
para(d, 48, 326, wrap(d, lead, fnt(SANS, 17), 556), fnt(SANS, 17), INK,
     leading=22)

# lead illustration: night sky, missile trails, three impact points
px0, py0, px1, py1 = 622, 210, 976, 396
d.rectangle([px0, py0, px1, py1], fill=DARKPANEL, outline=NAVY, width=2)
# faint radar rings, kept inside the panel
for r in (24, 48, 70):
    d.ellipse([880 - r, 300 - r, 880 + r, 300 + r], outline=(70, 95, 140),
              width=1)
# missile trails: straight streaks from the top edge to the impact dots
for (tx, ix, iy, col) in ((680, 700, 324, (255, 120, 90)),
                          (790, 800, 346, RED),
                          (890, 900, 312, (255, 120, 90))):
    d.line([(tx, 212), (ix, iy)], fill=col, width=3)
    d.ellipse([tx - 3, 210, tx + 3, 216], fill=col)
# impact dots with labels above them
for (ix, iy, lab) in ((700, 324, "MOLODYCZ"), (800, 346, "RUDNIK N. SANEM"),
                      (900, 312, "NOWY LIPOWIEC")):
    d.ellipse([ix - 6, iy - 6, ix + 6, iy + 6], fill=RED,
              outline=(255, 255, 255), width=2)
    d.text((ix, iy - 26), lab, font=fnt(SANS_B, 12), fill=(255, 255, 255),
           anchor="ma")
d.text((636, 222), "Kh-101 CRUISE MISSILE", font=fnt(SANS_B, 13),
       fill=(255, 200, 180))
d.text((636, 376), "NO ONE HURT IN POLAND  \u2022  8 KILLED IN UKRAINE",
       font=fnt(SANS_B, 12), fill=(255, 255, 255))

# ---------- three-cell row ----------
CELL_W, CELL_H = 303, 262
ROW_Y = 420
CELLS3 = [
    (30, NAVY, "NEW YORK  \u2022  MARKETS",
     "WALL STREET SLIDES INTO CORRECTION",
     "S&P 500 falls about 3.7% as AI shares sell off; the Dow joins "
     "it in correction territory.", "chart"),
    (360, RED, "CYBER  \u2022  BANKS",
     "BANKS HIT BY VENDOR BREACH",
     "JPMorgan, Visa and Mastercard disclose third-party breaches; "
     "gang \u201cn0n\u201d claims data of 16,000+ customers. No card "
     "numbers exposed.", "shield"),
    (690, GREEN, "WELLINGTON  \u2022  CRICKET",
     "INDIA HIT BACK IN WELLINGTON",
     "Nicholls 175* and Phillips 118 lift New Zealand to 368; "
     "Jaiswal 85 and Rahul 52* take India to 159/1 at stumps.",
     "bat"),
]


def icon(kind, x, y):
    """Small pictogram, bottom-right of a cell."""
    if kind == "chart":
        for i, bh in enumerate((12, 20, 28)):
            bx = x + 6 + i * 16
            d.rectangle([bx, y + 40 - bh, bx + 11, y + 40], fill=NAVY)
        d.line([(x + 2, y + 4), (x + 54, y + 34)], fill=RED, width=3)
    elif kind == "shield":
        d.polygon([(x + 28, y), (x + 54, y + 8), (x + 54, y + 24),
                   (x + 28, y + 42), (x + 2, y + 24), (x + 2, y + 8)],
                  outline=RED, width=3)
        d.rectangle([x + 20, y + 18, x + 36, y + 30], outline=RED, width=2)
        d.line([(x + 28, y + 18), (x + 28, y + 12)], fill=RED, width=3)
    elif kind == "bat":
        d.line([(x + 12, y + 38), (x + 40, y + 6)], fill=(201, 162, 39),
               width=6)
        d.ellipse([x + 42, y + 2, x + 54, y + 14], fill=RED)
    elif kind == "globe":
        d.ellipse([x + 6, y, x + 50, y + 40], outline=TEAL, width=3)
        d.ellipse([x + 18, y, x + 38, y + 40], outline=TEAL, width=2)
        d.line([(x + 6, y + 20), (x + 50, y + 20)], fill=TEAL, width=2)
    elif kind == "euro":
        d.ellipse([x + 6, y, x + 50, y + 40], outline=NAVY, width=3)
        d.text((x + 28, y + 2), "\u20ac", font=fnt(SANS_B, 30), fill=NAVY,
               anchor="ma")


for (cx0, accent, kicker, head, dek, kind) in CELLS3:
    d.rectangle([cx0, ROW_Y, cx0 + CELL_W, ROW_Y + CELL_H], outline=INK,
                width=1)
    d.rectangle([cx0, ROW_Y, cx0 + CELL_W, ROW_Y + 5], fill=accent)
    d.text((cx0 + 14, ROW_Y + 16), kicker, font=fnt(SANS_B, 15), fill=accent)
    hy = para(d, cx0 + 14, ROW_Y + 40,
              wrap(d, head, fnt(SERIF_B, 26), CELL_W - 28),
              fnt(SERIF_B, 26), INK, leading=31)
    para(d, cx0 + 14, hy + 6, wrap(d, dek, fnt(SANS, 17), CELL_W - 28),
         fnt(SANS, 17), INK, leading=22)
    icon(kind, cx0 + CELL_W - 70, ROW_Y + CELL_H - 52)

# ---------- two-cell row ----------
ROW2_Y = 698
ROW2_H = 190
CELLS2 = [
    (30, TEAL, "ANTALYA  \u2022  CLIMATE",
     "COP31 TALKS IN FINAL STRETCH",
     "Negotiators push into the final stage; fossil fuels and climate "
     "finance divide them.", "globe"),
    (522, NAVY, "BRUSSELS  \u2022  UKRAINE AID",
     "EU SENDS UKRAINE \u20ac8 BILLION",
     "Brussels completes its largest-ever reforms payout to Kyiv: "
     "nearly \u20ac8 billion.", "euro"),
]
for (cx0, accent, kicker, head, dek, kind) in CELLS2:
    cw = 471
    d.rectangle([cx0, ROW2_Y, cx0 + cw, ROW2_Y + ROW2_H], outline=INK,
                width=1)
    d.rectangle([cx0, ROW2_Y, cx0 + cw, ROW2_Y + 5], fill=accent)
    d.text((cx0 + 16, ROW2_Y + 16), kicker, font=fnt(SANS_B, 16),
           fill=accent)
    hy = para(d, cx0 + 16, ROW2_Y + 42,
              wrap(d, head, fnt(SERIF_B, 28), cw - 32),
              fnt(SERIF_B, 28), INK, leading=33)
    para(d, cx0 + 16, hy + 6, wrap(d, dek, fnt(SANS, 17), cw - 32),
         fnt(SANS, 17), INK, leading=22)
    icon(kind, cx0 + cw - 72, ROW2_Y + ROW2_H - 52)

# ---------- footer ----------
d.line([(30, 904), (W - 30, 904)], fill=INK, width=2)
d.text((30, 916), "ALSO TODAY:  ", font=fnt(SANS_B, 18), fill=RED)
also = ("Cyclone Akvan weakens to a deep depression over Odisha \u2014 no "
        "major damage; 39 trains cancelled. Hyundai unveils the 2027 "
        "Elantra at the LA Auto Show.")
para(d, 172, 916, wrap(d, also, fnt(SANS, 18), W - 202), fnt(SANS, 18),
     INK, leading=22)
d.text((30, 964),
       "Sources, Saturday 21 November 2026: AP \u2022 Reuters \u2022 The Times "
       "\u2022 Security Affairs \u2022 Cricbuzz \u2014 image drawn by hand "
       "with code.",
       font=fnt(SANS, 14), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size, img.mode)
