#!/usr/bin/env python3
"""Render the broadsheet front page for Tuesday 24 November 2026.

Run locally only (needs Pillow + DejaVu fonts on this machine).
The shipped entry is entry.png plus a stdlib-only copy program.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
INK = (18, 18, 18)
PAPER = (247, 243, 234)
RED = (163, 22, 33)
GREY = (90, 86, 78)
RULE = (60, 58, 52)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    lines = []
    for chunk in text.split("\n"):
        line = ""
        for word in chunk.split():
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_para(draw, x, y, width, text, fnt, fill=INK, leading=None):
    """Draw wrapped paragraph, return y after it."""
    leading = leading or int(fnt.size * 1.32)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text):
    draw.text((x, y), text, font=font(SANS_B, 16), fill=RED)
    return y + 24


def headline(draw, x, y, width, text, size=30):
    fnt = font(SERIF_B, size)
    leading = int(size * 1.12)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=INK)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def vrule(draw, x, y0, y1):
    draw.line([(x, y0), (x, y1)], fill=RULE, width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    rule(d, MARGIN, W - MARGIN, 26, 3)
    d.text((W // 2, 34), "THE WORLD", font=font(SERIF_B, 86),
           fill=INK, anchor="ma")
    rule(d, MARGIN, W - MARGIN, 132, 3)
    d.text((W // 2, 142), "TUESDAY, 24 NOVEMBER 2026  ·  THE DAY IN ONE PAGE",
           font=font(SANS_B, 20), fill=RED, anchor="ma")
    rule(d, MARGIN, W - MARGIN, 172, 1)

    # ---- Lead story (left, top) ----
    lx, lw = MARGIN, 624
    y = 188
    y = kicker(d, lx, y, "MARKETS  ·  TECHNOLOGY")
    y = headline(d, lx, y + 2, lw,
                 "HUANG'S RETURN SENDS MARKETS SOARING", 44)
    y = draw_para(d, lx, y + 6, lw,
                  "Nvidia jumps 31% as its ousted chief is reinstated — "
                  "the Nasdaq posts its best day since April 2025.",
                  font(SERIF, 22), leading=28)
    y = draw_para(d, lx, y + 8, lw,
                  "Wall Street roared back on Monday after Nvidia's board "
                  "brought Jensen Huang back as chief executive. The "
                  "Nasdaq leapt 6.5% to 24,089.56, the S&P 500 rose 4.7% "
                  "and the Dow added 3.0%.",
                  font(SANS, 18), leading=24)
    y = draw_para(d, lx, y + 10, lw,
                  "Nasdaq +6.5%  ·  S&P 500 +4.7%  ·  Dow +3.0%  ·  "
                  "Nvidia +31% (+$950bn)  ·  Nikkei +3.9%",
                  font(SANS_B, 17), fill=RED, leading=22)
    lead_bottom = y

    # ---- Right column (top) ----
    rx, rw = 684, W - MARGIN - 684
    y = 188
    y = kicker(d, rx, y, "MIDDLE EAST")
    y = headline(d, rx, y + 2, rw, "RIYADH TOWER HIT AGAIN", 26)
    y = draw_para(d, rx, y + 6, rw,
                  "Houthi fighters struck a tower in Riyadh's financial "
                  "district on Tuesday, injuring 11 people — the second "
                  "hit on the capital's tallest skyscraper in less than "
                  "a week.",
                  font(SANS, 16), leading=21)
    y += 12
    rule(d, rx, W - MARGIN, y, 1)
    y += 12
    y = kicker(d, rx, y, "GAZA")
    y = headline(d, rx, y + 2, rw, "HAMAS SECURITY CHIEF KILLED", 26)
    y = draw_para(d, rx, y + 6, rw,
                  "Israeli airstrikes in Gaza on Tuesday killed seven "
                  "people, including Hamas security chief Naeem Abu "
                  "Nahel, despite a ceasefire in place since last year.",
                  font(SANS, 16), leading=21)
    right_bottom = y

    band_y = max(lead_bottom, right_bottom) + 10
    vrule(d, 672, 188, band_y)
    rule(d, MARGIN, W - MARGIN, band_y, 2)

    # ---- Middle band: Ukraine | Iran ----
    my = band_y + 14
    col_w = 464
    y = my
    y = kicker(d, MARGIN, y, "UKRAINE")
    y = headline(d, MARGIN, y + 2, col_w,
                 "RUSSIAN STRIKE ON ZAPORIZHZHIA KILLS TWO, WOUNDS 40",
                 24)
    y = draw_para(d, MARGIN, y + 6, col_w,
                  "An overnight Russian attack on Zaporizhzhia killed "
                  "two people and wounded 40, including four children, "
                  "after striking an apartment building. Russia said it "
                  "shot down 699 Ukrainian drones overnight.",
                  font(SANS, 16), leading=21)
    left_bottom = y

    y = my
    y = kicker(d, 524, y, "IRAN")
    y = headline(d, 524, y + 2, col_w,
                 "US SANCTIONS BITE AS IRAN RULES OUT TALKS", 24)
    y = draw_para(d, 524, y + 6, col_w,
                  "Washington imposed fresh sanctions on nearly 30 "
                  "Iran-linked financial houses, and Iran's currency "
                  "plunged on the black market. Tehran said it would not "
                  "talk to the US without seven conditions met.",
                  font(SANS, 16), leading=21)
    right2_bottom = y

    band2_y = max(left_bottom, right2_bottom) + 10
    vrule(d, 512, my, band2_y)
    rule(d, MARGIN, W - MARGIN, band2_y, 2)

    # ---- Lower band: World in brief, two columns ----
    ly = band2_y + 14
    y = ly
    y = kicker(d, MARGIN, y, "WORLD IN BRIEF")
    briefs = [
        "COP31: after the no-deal summit in Antalya — the first since "
        "2009 — the blame game begins; focus shifts to COP32 in Addis "
        "Ababa.",
        "Washington: Trump awards Rudy Giuliani the Medal of Freedom, "
        "the highest US civilian honour.",
        "Hanoi: a blast at a hot-pot eatery kills six and injures more "
        "than a dozen; a gas leak is suspected.",
        "Landmines: global casualties hit a five-year high of 7,000, "
        "with Myanmar and Syria worst hit.",
    ]
    y1 = y
    for b in briefs[:2]:
        y1 = draw_para(d, MARGIN, y1, col_w, "•  " + b,
                       font(SANS, 15), leading=20)
        y1 += 4
    y2 = y
    for b in briefs[2:]:
        y2 = draw_para(d, 524, y2, col_w, "•  " + b,
                       font(SANS, 15), leading=20)
        y2 += 4

    foot_y = max(y1, y2) + 10
    rule(d, MARGIN, W - MARGIN, foot_y, 2)
    d.text((W // 2, foot_y + 8),
           "THE WORLD  ·  TUESDAY 24 NOVEMBER 2026  ·  "
           "The day's news, on one page.",
           font=font(SANS_B, 15), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size, "band_y", band_y,
          "band2_y", band2_y, "foot_y", foot_y)


if __name__ == "__main__":
    main()
