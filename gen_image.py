#!/usr/bin/env python3
"""Draw the make.fun news-image-20261124 entry: one-page atlas dashboard
summing up Tuesday 24 November 2026 world news. 38 dated stories, 8 regions.
Programmatic Pillow drawing only (DejaVu fonts); no downloaded images, no
network, deterministic output. Fails loudly (OVERFLOW) if any text would
leave its box, instead of drawing over another element."""

import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
CW = W - 2 * MARGIN  # 976

PAPER = (245, 239, 226)
CARD = (252, 250, 244)
INK = (28, 28, 26)
MUTED = (112, 106, 94)
RED = (178, 34, 34)
NAVY = (30, 58, 95)
TEAL = (0, 128, 128)
ORANGE = (204, 85, 0)
BROWN = (120, 72, 20)
AMBER = (176, 124, 0)
GREEN = (34, 139, 34)
PURPLE = (106, 40, 160)
SLATE = (38, 48, 60)
TICKER_BG = (24, 42, 74)
GOLD = (212, 175, 55)
LIGHT_RED = (255, 150, 140)
LIGHT_GREEN = (140, 230, 150)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that each fit max_w."""
    words = text.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, fnt, fill, line_h):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def fail(msg):
    print("OVERFLOW: " + msg, file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------- data
LEADS = [
    ("MARKETS  ·  NEW YORK", AMBER,
     "Dow tops 50,000 for first time",
     "Closes at 50,018.70 as tech slides; Nvidia -6% a day after Huang's return.",
     "chart"),
    ("TECH  ·  NVIDIA", TEAL,
     "Huang apologizes, says he's in therapy",
     "A day after his return, Nvidia chief faces staff; board cites US assurances.",
     "chip"),
    ("EUROPE  ·  UKRAINE", NAVY,
     "Russia fires 96 drones at Ukraine",
     "73 downed by 08:00; 2 killed, 40 hurt in Zaporizhzhia.",
     "drone"),
]

HEATMAP = [
    ("Dow 50,018.70", GOLD, INK, True),
    ("S&P -0.50%", LIGHT_RED, SLATE, False),
    ("Nasdaq -1.48%", LIGHT_RED, SLATE, False),
    ("Kospi +6.32%", LIGHT_GREEN, SLATE, False),
    ("Brent $91.40", (255, 255, 255), SLATE, False),
]

PANELS = [
    ("MIDDLE EAST", RED, [
        ("Vance, Rubio meet Qatar PM", "White House talks on Iran; Doha mediates."),
        ("Iran vows to fight US blockade", "'All tools' vs naval blockade, FM says."),
        ("Netanyahu urges new Iran strikes", "Pushes Trump to resume strikes."),
        ("Israel kills Hamas security chief", "Naeem Abu Nahel + 6 dead in Gaza."),
        ("Houthis: dozens dead in Saudi raids", "Yemen strikes reported Tuesday."),
    ]),
    ("EUROPE", NAVY, [
        ("COP31 was a flop. What now?", "First failed summit since 2009; focus shifts to COP32."),
        ("Russia warns Estonia of open war", "Border closure sparks threat."),
        ("Germany gets Ukraine Delta access", "First country, Berlin deal signed."),
        ("Russian drone enters Polish airspace", "Brief incursion near Dorohusk."),
        ("NATO vows to defend space", "After nuclear-satellite reports."),
    ]),
    ("ASIA", TEAL, [
        ("Russian jets enter Korea ADIZ", "Seoul reports incursion Tuesday."),
        ("Solomon Islands ends China pact", "Security deal to be scrapped."),
        ("China hosts first foreign astronaut", "Pakistani on Tiangong station."),
        ("Nepal quake 5.6 near China border", "Koshi province struck Tuesday."),
        ("S. Korea pays to catch AI cheats", "Rewards up to $375,000 in exam."),
    ]),
    ("AMERICAS", ORANGE, [
        ("Trump orders faster death sentences", "Directive for child killers, traffickers."),
        ("Pentagon faults Canada on defence", "'Falling short' as partner, it says."),
        ("Mexico to try 'El Chapo Isidro'", "Despite US extradition request."),
        ("Colombia car bomb wrecks buildings", "Villavicencio blast, no victims yet."),
        ("Measles kills ninth in Pennsylvania", "Outbreak hits 46 counties."),
    ]),
    ("AFRICA", BROWN, [
        ("DRC fighting traps Ebola teams", "Ituri clashes halt responders."),
        ("UN seeks probe into Libya ship hit", "Benghazi port attacks probed."),
    ]),
    ("MARKETS", AMBER, [
        ("S&P, Nasdaq slide Tuesday", "S&P -0.50%; Nasdaq -1.48%."),
        ("Kospi tops 5,000 on chip rally", "+6.32%; Nikkei +3.91%."),
        ("Brent rebounds to $91.40", "Oil up on Hormuz ship attacks."),
        ("Gold slides to near 14-month low", "-2.64% to $3,555 on Fed signals."),
    ]),
    ("SCIENCE", GREEN, [
        ("Guterres wants AI rules in a year", "UN chief seeks AI framework."),
        ("US states sue SpaceX over Grok", "Oregon, Virginia cite AI images."),
        ("Arm extends CEO Haas to 2033", "Amid Nvidia speculation."),
        ("Nvidia adds $900B in a day", "Record one-day gain after return."),
    ]),
    ("SPORT", PURPLE, [
        ("Real Madrid rout PSV 5-1", "Mbappé scores twice."),
        ("Arsenal held 1-1 by Dortmund", "Madueke earns a point."),
        ("Man City draw 2-2 with Napoli", "Cherki's late leveller."),
        ("Galatasaray edge Villa 1-0", "Gül's 77th-minute winner."),
        ("Leipzig beat Lens 3-1", "Nusa scores twice."),
    ]),
]

TICKER_ITEMS = [
    "Zelensky: seek more US aid if peace deal fails",
    "Kushner: I urged Trump not to pressure Zelensky",
    "Burnham: no EU return without referendum",
]

FOOTER = ("Compiled from reports published 24 November 2026  ·  "
          "Sources: CNN, Reuters, AP, WSJ  ·  One day. 38 stories.")


# ---------------------------------------------------------------- drawing
def draw_icon(d, kind, bx, by, color):
    """Small geometric icon inside a 26x20 box; never overlaps text."""
    if kind == "chart":
        pts = [(bx, by + 16), (bx + 8, by + 10), (bx + 14, by + 13),
               (bx + 22, by + 2)]
        d.line(pts, fill=color, width=3)
        d.line([(bx + 22, by + 2), (bx + 17, by + 3)], fill=color, width=3)
        d.line([(bx + 22, by + 2), (bx + 21, by + 7)], fill=color, width=3)
    elif kind == "chip":
        d.rectangle([bx + 5, by + 4, bx + 21, by + 16], outline=color, width=2)
        d.rectangle([bx + 10, by + 8, bx + 16, by + 12], fill=color)
        for px in (bx + 8, bx + 13, bx + 18):
            d.line([(px, by + 1), (px, by + 4)], fill=color, width=2)
            d.line([(px, by + 16), (px, by + 19)], fill=color, width=2)
    elif kind == "drone":
        d.ellipse([bx + 9, by + 7, bx + 17, by + 13], fill=color)
        for cx, cy in ((bx + 3, by + 3), (bx + 23, by + 3),
                       (bx + 3, by + 17), (bx + 23, by + 17)):
            d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], outline=color, width=2)
        d.line([(bx + 9, by + 10), (bx + 3, by + 3)], fill=color, width=1)
        d.line([(bx + 17, by + 10), (bx + 23, by + 3)], fill=color, width=1)
        d.line([(bx + 9, by + 10), (bx + 3, by + 17)], fill=color, width=1)
        d.line([(bx + 17, by + 10), (bx + 23, by + 17)], fill=color, width=1)


def draw_masthead(d):
    d.line([(MARGIN, 12), (W - MARGIN, 12)], fill=INK, width=3)
    f_title = font(SERIF_B, 56)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 20), title, font=f_title, fill=INK)
    f_date = font(SANS_B, 24)
    date = "TUESDAY  24  NOVEMBER  2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 82), date, font=f_date, fill=RED)
    f_sub = font(SANS, 14)
    sub = "38 dated stories  ·  8 regions  ·  all times UTC"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 110), sub, font=f_sub, fill=MUTED)
    d.line([(MARGIN, 130), (W - MARGIN, 130)], fill=INK, width=2)


def draw_leads(d):
    y0, ch, cw = 138, 158, 317
    f_kick = font(SANS_B, 13)
    f_head = font(SANS_B, 21)
    f_body = font(SANS, 13)
    for i, (kicker, color, headline, body, icon) in enumerate(LEADS):
        x = MARGIN + i * (cw + 12)
        d.rectangle([x, y0, x + cw, y0 + ch], fill=CARD, outline=INK, width=2)
        d.rectangle([x, y0, x + cw, y0 + 6], fill=color)
        d.text((x + 12, y0 + 16), kicker, font=f_kick, fill=color)
        draw_icon(d, icon, x + cw - 12 - 26, y0 + 14, color)
        inner = cw - 24
        hlines = wrap(d, headline, f_head, inner)
        if len(hlines) > 2:
            fail("lead %d headline wraps to %d lines: %r"
                 % (i, len(hlines), headline))
        y = draw_lines(d, hlines, x + 12, y0 + 40, f_head, INK, 25)
        blines = wrap(d, body, f_body, inner)
        if len(blines) > 3:
            fail("lead %d body wraps to %d lines: %r" % (i, len(blines), body))
        y = draw_lines(d, blines, x + 12, y + 6, f_body, INK, 17)
        if y > y0 + ch - 10:
            fail("lead %d text reaches y=%d, card ends %d" % (i, y, y0 + ch))


def draw_heatmap(d):
    y0, hh = 304, 38
    d.rectangle([MARGIN, y0, W - MARGIN, y0 + hh], fill=SLATE)
    f_lab = font(SANS_B, 13)
    label = "MARKET HEATMAP"
    lx = MARGIN + 14
    d.text((lx, y0 + 12), label, font=f_lab, fill=GOLD)
    x = lx + d.textlength(label, font=f_lab) + 18
    f_chip = font(SANS_B, 13)
    f_dot = font(SANS, 13)
    for j, (text, fg, bg, highlight) in enumerate(HEATMAP):
        if j > 0:
            d.text((x, y0 + 12), "·", font=f_dot, fill=(140, 140, 140))
            x += d.textlength("·", font=f_dot) + 12
        tw = d.textlength(text, font=f_chip)
        if highlight:
            d.rectangle([x - 6, y0 + 8, x + tw + 6, y0 + 30], fill=fg)
            d.text((x, y0 + 12), text, font=f_chip, fill=bg)
        else:
            d.text((x, y0 + 12), text, font=f_chip, fill=fg)
        x += tw + 14
    if x > W - MARGIN:
        fail("heatmap strip overflows: ends x=%d" % x)


def draw_panels(d):
    pw, gap = 235, 12
    rows = [(350, 312), (672, 264)]
    f_name = font(SANS_B, 13)
    f_cnt = font(SANS, 10)
    f_head = font(SANS_B, 12)
    f_body = font(SANS, 11)
    idx = 0
    for (y0, ph) in rows:
        for c in range(4):
            if idx >= len(PANELS):
                return
            name, color, stories = PANELS[idx]
            idx += 1
            x = MARGIN + c * (pw + gap)
            d.rectangle([x, y0, x + pw, y0 + ph], fill=CARD, outline=INK,
                        width=2)
            d.rectangle([x, y0, x + pw, y0 + 5], fill=color)
            d.text((x + 10, y0 + 12), name, font=f_name, fill=color)
            cnt = "%d STORIES" % len(stories)
            cw = d.textlength(cnt, font=f_cnt)
            d.text((x + pw - 10 - cw, y0 + 14), cnt, font=f_cnt, fill=MUTED)
            d.line([(x + 10, y0 + 34), (x + pw - 10, y0 + 34)],
                   fill=(210, 204, 190), width=1)
            # Measure all stories first, then centre the block vertically
            # so short panels do not leave a big empty band at the bottom.
            hw = pw - 22 - 10
            measured = []
            for (headline, body) in stories:
                hlines = wrap(d, headline, f_head, hw)
                if len(hlines) > 2:
                    fail("panel %s headline wraps to %d lines: %r"
                         % (name, len(hlines), headline))
                blines = wrap(d, body, f_body, hw)
                if len(blines) > 2:
                    fail("panel %s body wraps to %d lines: %r"
                         % (name, len(blines), body))
                measured.append((hlines, blines))
            total = sum(len(h) * 14 + len(b) * 13
                        for (h, b) in measured) + 3 * (len(measured) - 1)
            avail = ph - 42 - 6
            if total > avail:
                fail("panel %s overflows: content needs %dpx, panel holds %dpx"
                     % (name, total, avail))
            y = y0 + 42 + (avail - total) // 2
            for (hlines, blines) in measured:
                d.ellipse([x + 10, y + 5, x + 16, y + 11], fill=color)
                y = draw_lines(d, hlines, x + 22, y, f_head, INK, 14)
                y = draw_lines(d, blines, x + 22, y, f_body, MUTED, 13)
                y += 3


def draw_ticker(d):
    y0, th = 944, 50
    d.rectangle([MARGIN, y0, W - MARGIN, y0 + th], fill=TICKER_BG)
    f_lab = font(SANS_B, 13)
    label = "ALSO IN THE NEWS"
    lx = MARGIN + 14
    d.text((lx, y0 + 18), label, font=f_lab, fill=GOLD)
    tx = lx + d.textlength(label, font=f_lab) + 16
    tw = W - MARGIN - 14 - tx
    f_txt = font(SANS, 12)
    text = "   ·   ".join(TICKER_ITEMS)
    lines = wrap(d, text, f_txt, tw)
    if len(lines) > 2:
        fail("ticker wraps to %d lines" % len(lines))
    draw_lines(d, lines, tx, y0 + 9, f_txt, (255, 255, 255), 16)


def draw_footer(d):
    f_foot = font(SANS, 13)
    fw = d.textlength(FOOTER, font=f_foot)
    d.text(((W - fw) / 2, 1000), FOOTER, font=f_foot, fill=MUTED)


def main():
    total = 3 + sum(len(s) for (_, _, s) in PANELS)
    if total != 38:
        fail("story count is %d, expected 38" % total)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_leads(d)
    draw_heatmap(d)
    draw_panels(d)
    draw_ticker(d)
    draw_footer(d)
    img.save("entry.png", format="PNG")


if __name__ == "__main__":
    main()
