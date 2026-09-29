#!/usr/bin/env python3
"""Build pose × look variants of a character from one or more cut-out base images.

Usage:
    python character_kit.py kits/rick.json --out assets/characters/rick
    python character_kit.py kits/rick.json --out ... --look space     # just one look

A kit (JSON) declares:
  "bases":  {"main": "raw/rick.png"}                     # transparent cut-outs
  "landmarks": {"eyeL": [280,175], ...}                    # pixel coords on the base, for reference in ops
  "poses":  {"fist": {"base": "main", "ops": [...]}, ...}  # pose edits (erase a gesture, add a prop)
  "looks":  {"classic": [], "space": [...], ...}           # get-ups applied on top of every pose
Every output of one character shares ONE canvas (union bounding box), so crossfading poses in a reel
never makes the character jump. Outputs: <out>/<look>/<pose>.png and <out>/_contact.png.

Ops (coordinates in base-image pixels; "@name" refers to a landmark):
  {"op":"erase","poly":[[x,y],...]}                        make a region transparent
  {"op":"poly","pts":[...],"fill":"#hex","stroke":"#hex","w":6}
  {"op":"ellipse","c":[x,y],"r":[rx,ry],"fill":"#hex|rgba()","stroke":"#hex","w":6}
  {"op":"line","pts":[...],"color":"#hex","w":6}
  {"op":"arc","c":[x,y],"r":[rx,ry],"a":[deg0,deg1],"color":"#hex","w":6}
  props: portal_gun, flask, phone, sweat, eyepatch, space_helmet, visor, goggles
    {"op":"portal_gun","at":[x,y],"angle":-30,"scale":1}
    {"op":"flask","at":[x,y],"angle":-10,"scale":1}
    {"op":"phone","at":[x,y],"angle":10,"scale":1,"buzz":true}
    {"op":"sweat","at":[[x,y],...],"scale":1}
    {"op":"eyepatch","eye":"@eyeL","r":34,"strap":[[x,y],[x,y]]}
    {"op":"space_helmet","c":[x,y],"r":[rx,ry],"neck":[x,y,w]}
    {"op":"visor","box":[x0,y0,x1,y1],"band":[[x,y],[x,y]]}
    {"op":"goggles","eyes":[[x,y],[x,y]],"r":26,"strap":[[x,y],[x,y]]}
Needs: pip install pillow numpy
"""
import argparse, json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageColor

SS = 2          # supersampling for clean anti-aliased props
M = 200         # working margin around the base (props/helmets may extend past it)
INK = (12, 14, 16, 255)

def col(c, default=None):
    if c is None: return default
    if isinstance(c, (list, tuple)): return tuple(c)
    if c.startswith('rgba'):
        v = [float(x) for x in c[5:-1].split(',')]; return (int(v[0]), int(v[1]), int(v[2]), int(v[3] * 255))
    return ImageColor.getrgb(c) + ((255,) if len(ImageColor.getrgb(c)) == 3 else ())

class Canvas:
    def __init__(self, base, lm):
        self.lm = lm; W, H = base.size
        self.img = Image.new('RGBA', ((W + 2 * M) * SS, (H + 2 * M) * SS), (0, 0, 0, 0))
        self.img.alpha_composite(base.resize((W * SS, H * SS), Image.LANCZOS), (M * SS, M * SS))
    def P(self, p):
        if isinstance(p, str) and p.startswith('@'): p = self.lm[p[1:]]
        return ((p[0] + M) * SS, (p[1] + M) * SS)
    def S(self, v): return v * SS
    def layer(self): return Image.new('RGBA', self.img.size, (0, 0, 0, 0))
    def put(self, lay): self.img.alpha_composite(lay)

def rot(pts, c, ang):
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]

def op(cv, o):
    k = o['op']; L = cv.layer(); d = ImageDraw.Draw(L)
    if k == 'erase':
        mask = Image.new('L', cv.img.size, 0); ImageDraw.Draw(mask).polygon([cv.P(p) for p in o['poly']], fill=255)
        a = np.array(cv.img); a[..., 3] = np.where(np.array(mask) > 0, 0, a[..., 3]); cv.img = Image.fromarray(a); return
    if k == 'poly':
        d.polygon([cv.P(p) for p in o['pts']], fill=col(o.get('fill')), outline=col(o.get('stroke')), width=cv.S(o.get('w', 0)) if o.get('stroke') else 0)
    elif k == 'ellipse':
        (x, y), (rx, ry) = cv.P(o['c']), (cv.S(o['r'][0]), cv.S(o['r'][1]))
        d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=col(o.get('fill')), outline=col(o.get('stroke')), width=cv.S(o.get('w', 0)) if o.get('stroke') else 0)
    elif k == 'line':
        d.line([cv.P(p) for p in o['pts']], fill=col(o.get('color'), INK), width=cv.S(o.get('w', 6)), joint='curve')
    elif k == 'arc':
        (x, y), (rx, ry) = cv.P(o['c']), (cv.S(o['r'][0]), cv.S(o['r'][1]))
        d.arc([x - rx, y - ry, x + rx, y + ry], o['a'][0], o['a'][1], fill=col(o.get('color'), INK), width=cv.S(o.get('w', 6)))
    elif k == 'portal_gun':
        c = cv.P(o['at']); s = cv.S(o.get('scale', 1)); ang = o.get('angle', -30)
        R = lambda pts: rot([(c[0] + x * s, c[1] + y * s) for x, y in pts], c, ang)
        d.polygon(R([(-22, -10), (70, -18), (78, 14), (-22, 22)]), fill=(210, 214, 218, 255), outline=INK, width=int(5 * s))       # body
        d.polygon(R([(70, -12), (96, -8), (96, 8), (74, 10)]), fill=(120, 126, 132, 255), outline=INK, width=int(5 * s))           # muzzle
        d.polygon(R([(-6, -34), (46, -34), (46, -14), (-6, -14)]), fill=(151, 206, 76, 255), outline=INK, width=int(5 * s))        # green canister
        d.polygon(R([(4, -30), (40, -30), (40, -24), (4, -24)]), fill=(212, 245, 140, 255))                                          # glow
        d.polygon(R([(96, -4), (104, -4), (104, 4), (96, 4)]), fill=(220, 60, 50, 255))                                            # red tip
        d.polygon(R([(-10, 20), (14, 20), (8, 58), (-14, 58)]), fill=(180, 184, 188, 255), outline=INK, width=int(5 * s))          # grip
    elif k == 'flask':
        c = cv.P(o['at']); s = cv.S(o.get('scale', 1)); ang = o.get('angle', -10)
        R = lambda pts: rot([(c[0] + x * s, c[1] + y * s) for x, y in pts], c, ang)
        d.polygon(R([(-26, -40), (26, -40), (30, 40), (-30, 40)]), fill=(196, 204, 210, 255), outline=INK, width=int(5 * s))
        d.polygon(R([(-10, -58), (10, -58), (10, -40), (-10, -40)]), fill=(150, 156, 162, 255), outline=INK, width=int(4 * s))
        d.polygon(R([(-18, -30), (-10, -30), (-12, 30), (-20, 30)]), fill=(240, 244, 246, 255))
    elif k == 'phone':
        c = cv.P(o['at']); s = cv.S(o.get('scale', 1)); ang = o.get('angle', 10)
        R = lambda pts: rot([(c[0] + x * s, c[1] + y * s) for x, y in pts], c, ang)
        d.polygon(R([(-22, -42), (22, -42), (22, 42), (-22, 42)]), fill=(20, 24, 28, 255), outline=INK, width=int(4 * s))
        d.polygon(R([(-17, -34), (17, -34), (17, 30), (-17, 30)]), fill=(144, 194, 231, 255))
        d.polygon(R([(-13, -28), (13, -28), (13, -18), (-13, -18)]), fill=(79, 168, 124, 255))
        if o.get('buzz'):
            for sgn in (-1, 1):
                d.line(R([(sgn * 34, -30), (sgn * 44, -20)]), fill=INK, width=int(4 * s)); d.line(R([(sgn * 34, 0), (sgn * 46, 0)]), fill=INK, width=int(4 * s))
    elif k == 'sweat':
        s = o.get('scale', 1)
        for p in o['at']:
            x, y = cv.P(p); r = cv.S(10 * s)
            d.polygon([(x, y - 2.2 * r), (x - r, y), (x + r, y)], fill=(144, 194, 231, 255)); d.ellipse([x - r, y - r, x + r, y + r], fill=(144, 194, 231, 255), outline=INK, width=cv.S(2))
    elif k == 'eyepatch':
        x, y = cv.P(o['eye']); r = cv.S(o.get('r', 34))
        if o.get('strap'): d.line([cv.P(p) for p in o['strap']], fill=INK, width=cv.S(7))
        d.ellipse([x - r, y - r * .95, x + r, y + r * .95], fill=(18, 18, 20, 255), outline=INK, width=cv.S(4))
    elif k == 'visor':
        x0, y0 = cv.P(o['box'][:2]); x1, y1 = cv.P(o['box'][2:])
        if o.get('band'): d.line([cv.P(p) for p in o['band']], fill=(30, 40, 48, 255), width=cv.S(14))
        d.rounded_rectangle([x0, y0, x1, y1], radius=cv.S(22), fill=(144, 194, 231, 150), outline=INK, width=cv.S(6))
        d.line([(x0 + (x1 - x0) * .12, y0 + (y1 - y0) * .3), (x0 + (x1 - x0) * .4, y0 + (y1 - y0) * .22)], fill=(255, 255, 255, 190), width=cv.S(6))
    elif k == 'goggles':
        if o.get('strap'): d.line([cv.P(p) for p in o['strap']], fill=(60, 44, 30, 255), width=cv.S(12))
        for p in o['eyes']:
            x, y = cv.P(p); r = cv.S(o.get('r', 26))
            d.ellipse([x - r, y - r, x + r, y + r], fill=(151, 206, 76, 170), outline=(90, 94, 98, 255), width=cv.S(9))
            d.line([(x - r * .5, y - r * .3), (x - r * .1, y - r * .55)], fill=(255, 255, 255, 200), width=cv.S(4))
    elif k == 'space_helmet':
        (x, y), (rx, ry) = cv.P(o['c']), (cv.S(o['r'][0]), cv.S(o['r'][1]))
        if o.get('neck'):
            nx, ny = cv.P(o['neck'][:2]); nw = cv.S(o['neck'][2])
            d.rounded_rectangle([nx - nw, ny - cv.S(14), nx + nw, ny + cv.S(14)], radius=cv.S(12), fill=(180, 186, 192, 255), outline=INK, width=cv.S(5))
        d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=(144, 194, 231, 46), outline=(235, 245, 252, 230), width=cv.S(8))
        d.arc([x - rx * .82, y - ry * .82, x + rx * .82, y + ry * .82], 200, 250, fill=(255, 255, 255, 200), width=cv.S(10))
    else:
        raise ValueError(f'unknown op {k}')
    cv.put(L)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('kit'); ap.add_argument('--out', required=True); ap.add_argument('--look')
    a = ap.parse_args(); K = json.load(open(a.kit)); root = os.path.dirname(os.path.abspath(a.kit))
    bases = {k: Image.open(os.path.join(root, v)).convert('RGBA') for k, v in K['bases'].items()}
    looks = {a.look: K['looks'][a.look]} if a.look else K['looks']
    renders = {}
    for lk, lops in looks.items():
        for pn, pose in K['poses'].items():
            cv = Canvas(bases[pose.get('base', 'main')], K.get('landmarks', {}))
            for o in pose.get('ops', []): op(cv, o)
            for o in lops: op(cv, o)
            renders[(lk, pn)] = cv.img.resize((cv.img.width // SS, cv.img.height // SS), Image.LANCZOS)
    boxes = [np.argwhere(np.array(im)[..., 3] > 8) for im in renders.values()]
    y0 = min(b[:, 0].min() for b in boxes); y1 = max(b[:, 0].max() for b in boxes); x0 = min(b[:, 1].min() for b in boxes); x1 = max(b[:, 1].max() for b in boxes)
    for (lk, pn), im in renders.items():
        os.makedirs(os.path.join(a.out, lk), exist_ok=True); im.crop((x0, y0, x1 + 1, y1 + 1)).save(os.path.join(a.out, lk, f'{pn}.png'))
    poses = list(K['poses']); lks = list(looks); tw = 260; th = int(tw * (y1 - y0) / (x1 - x0))
    sheet = Image.new('RGBA', (tw * len(poses), th * len(lks)), (119, 119, 119, 255))
    for i, lk in enumerate(lks):
        for j, pn in enumerate(poses):
            t = renders[(lk, pn)].crop((x0, y0, x1 + 1, y1 + 1)); t.thumbnail((tw, th)); sheet.alpha_composite(t, (j * tw, i * th))
    sheet.save(os.path.join(a.out, '_contact.png'))
    json.dump({'poses': poses, 'looks': lks, 'canvas': [int(x1 - x0 + 1), int(y1 - y0 + 1)]}, open(os.path.join(a.out, 'index.json'), 'w'), indent=1)
    print(f'{len(renders)} variants ({len(lks)} looks × {len(poses)} poses) -> {a.out}')

if __name__ == '__main__':
    main()
