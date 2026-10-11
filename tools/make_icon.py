"""Draw the home-screen app icon in the game's boxy style (rendered big, then scaled down).

Usage (needs Pillow):  python3 tools/make_icon.py .
Writes icon-512.png, icon-192.png and apple-touch-icon.png into the given folder.
"""
import math
import sys
from PIL import Image, ImageDraw

out_dir = sys.argv[1]
S = 1024
INK = (43, 33, 53)
PEE, PEE_LIQ, PEE_DARK = (244, 224, 77), (232, 201, 58), (201, 169, 31)
BEE, BEE_SHADE, HELMET = (247, 178, 27), (212, 143, 12), (95, 111, 59)
WHITE = (255, 255, 255)
SKY_TOP, SKY_LOW = (92, 180, 234), (223, 243, 241)
GRASS, GRASS_L, GRASS_D, SOIL = (103, 184, 74), (124, 201, 91), (79, 154, 58), (185, 134, 86)
W = int(S * 0.022)

img = Image.new('RGB', (S, S), SKY_TOP)
d = ImageDraw.Draw(img)


def outline(pts, w=W):
    d.line(pts + pts[:2], fill=INK, width=w, joint='curve')  # overlap so the closing corner is joined


def clip_below(poly, level):
    """Part of a convex polygon below a horizontal line (y >= level)."""
    def cross(a, b):
        t = (level - a[1]) / (b[1] - a[1])
        return (a[0] + t * (b[0] - a[0]), level)
    out = []
    for i in range(len(poly)):
        cur, prev = poly[i], poly[i - 1]
        if cur[1] >= level:
            if prev[1] < level:
                out.append(cross(prev, cur))
            out.append(cur)
        elif prev[1] >= level:
            out.append(cross(prev, cur))
    return out


# banded sky
ground = int(S * 0.80)
bands = 6
for i in range(bands):
    t = i / (bands - 1)
    col = tuple(round(a + (b - a) * t) for a, b in zip(SKY_TOP, SKY_LOW))
    d.rectangle([0, round(i * ground / bands), S, round((i + 1) * ground / bands)], fill=col)

# striped grass and soil
d.rectangle([0, ground, S, S], fill=SOIL)
d.rectangle([0, ground, S, ground + int(S * 0.07)], fill=GRASS)
gs = int(S * 0.08)
for i in range(0, S // gs + 2, 2):
    d.rectangle([i * gs, ground, i * gs + gs, ground + int(S * 0.045)], fill=GRASS_L)
d.rectangle([0, ground + int(S * 0.05), S, ground + int(S * 0.075)], fill=GRASS_D)
d.rectangle([0, ground - 7, S, ground + 7], fill=INK)

# the balloon: faceted octagon with a liquid line and a shine
cx, cy, rx, ry = S * 0.42, S * 0.50, S * 0.21, S * 0.24
octagon = [(cx + math.cos(math.pi / 8 + i * math.pi / 4) * rx,
            cy + math.sin(math.pi / 8 + i * math.pi / 4) * ry) for i in range(8)]
knot = [(cx - rx * 0.45, cy + ry * 0.85), (cx - rx * 0.95, cy + ry * 1.15), (cx - rx * 0.25, cy + ry * 1.1)]
d.polygon(knot, fill=PEE_DARK)
outline(knot, int(W * 0.8))
d.polygon(octagon, fill=PEE)
d.polygon(clip_below(octagon, cy + ry * 0.22), fill=PEE_LIQ)
d.polygon([(cx - rx * 0.62, cy - ry * 0.18), (cx - rx * 0.4, cy - ry * 0.62),
           (cx - rx * 0.12, cy - ry * 0.62), (cx - rx * 0.34, cy - ry * 0.18)], fill=WHITE)
outline(octagon)

# a helmeted platoon bee coming at it (game units, mirrored to face left)
bx, by, k, dirx = S * 0.74, S * 0.27, S * 0.0118, -1


def T(pts):
    return [(bx + dirx * x * k, by + y * k) for x, y in pts]


wing = T([(-7, -6), (-1, -17), (4, -6)])
d.polygon(wing, fill=WHITE)
outline(wing, int(W * 0.7))
body = T([(-9, -4), (-6, -7), (7, -7), (10, -3), (10, 3), (7, 7), (-6, 7), (-9, 4)])
d.polygon(body, fill=BEE)
d.polygon(T([(-9, 4), (10, 3), (7, 7), (-6, 7)]), fill=BEE_SHADE)
for x0 in (-5, 1):
    d.polygon(T([(x0, -7), (x0 + 3, -7), (x0 + 3, 7), (x0, 7)]), fill=INK)
outline(body, int(W * 0.8))
d.polygon(T([(-9, -2), (-14, 0), (-9, 2)]), fill=INK)
d.polygon(T([(5, -2), (7.6, -2), (7.6, 0.6), (5, 0.6)]), fill=INK)
helmet = T([(-2, -6), (0, -11), (9, -11), (11, -6)])
d.polygon(helmet, fill=HELMET)
outline(helmet, int(W * 0.7))
d.polygon(T([(-4, -6.9), (12, -6.9), (12, -5.1), (-4, -5.1)]), fill=INK)

for size, name in [(512, 'icon-512.png'), (192, 'icon-192.png'), (180, 'apple-touch-icon.png')]:
    img.resize((size, size), Image.LANCZOS).save(f'{out_dir}/{name}', optimize=True)
print('ok')
