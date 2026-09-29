#!/usr/bin/env python3
"""Cut a character pose sheet into individual transparent poses, ready for the Remotion template.

Usage:
    python slice_pose_sheet.py sheet.png --out assets/characters/morty --prefix m [--rows 3 --cols 5] [--scale 2]

- Works on sheets with a transparent background, or a flat white/light background (removed by an
  edge flood fill, so white shirts/lab coats inside black outlines are kept).
- Finds each figure as a connected shape; detached bits (hands, props) join the nearest figure.
  Figures are numbered row by row, left to right. Pass --rows if the automatic row count is off.
- Upscales by --scale with Lanczos + light sharpening (the reel shows characters ~600–900 px tall).
- Writes <prefix>01.png … and _contact.png (on grey) so you can check every cut.
Needs: pip install pillow scipy numpy
"""
import argparse, os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

def remove_bg(a, tol=18):
    if (a[..., 3] < 10).mean() > 0.05: return a  # already transparent
    rgb = a[..., :3].astype(int); bg = np.median(np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]]), axis=0)
    near = (np.abs(rgb - bg).max(axis=2) < tol)
    lab, _ = ndimage.label(near)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    a = a.copy(); a[np.isin(lab, list(edge)), 3] = 0; return a

def split_touching(lab, m):
    """Figures that touch on the sheet (a raised fist over a neighbour) come out as one oversized shape.
    Erode it until it falls apart into figure-sized cores, then give every pixel to the nearest core."""
    ids = [i for i in range(1, lab.max() + 1)]
    areas = ndimage.sum(m, lab, ids); big = [a for a in areas if a > 0.1 * max(areas)]
    med = float(np.median(big)) if big else 0
    out = lab.copy(); nxt = lab.max() + 1
    for i, ar in zip(ids, areas):
        if ar < 1.6 * med: continue
        comp = lab == i; cores = None
        for it in range(3, 40, 3):
            er = ndimage.binary_erosion(comp, iterations=it); cl, cn = ndimage.label(er)
            if cn >= 2:
                sz = ndimage.sum(er, cl, range(1, cn + 1)); keep = [k + 1 for k, v in enumerate(sz) if v > 0.08 * sz.max()]
                if len(keep) >= 2: cores = np.where(np.isin(cl, keep), cl, 0); break
        if cores is None: continue
        _, (iy, ix) = ndimage.distance_transform_edt(cores == 0, return_indices=True)
        near = cores[iy, ix]
        for k in np.unique(near[comp]):
            out[comp & (near == k)] = nxt; nxt += 1
    return out

def crop(a):
    ys, xs = np.where(a[..., 3] > 10); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('sheet'); ap.add_argument('--out', required=True); ap.add_argument('--prefix', default='p')
    ap.add_argument('--rows', type=int); ap.add_argument('--cols', type=int); ap.add_argument('--scale', type=float, default=2.0); ap.add_argument('--min-area', type=int, default=4000)
    a_ = ap.parse_args(); os.makedirs(a_.out, exist_ok=True)
    a = remove_bg(np.array(Image.open(a_.sheet).convert('RGBA'))); H, W = a.shape[:2]; m = a[..., 3] > 20
    lab, n = ndimage.label(ndimage.binary_dilation(m, iterations=2))
    lab = split_touching(lab, m)
    n = lab.max()
    comps = [(i, ndimage.center_of_mass(lab == i), s) for i, s in zip(range(1, n + 1), ndimage.sum(m, lab, range(1, n + 1))) if s > 0]
    figs = []
    sizes = {i: s for i, _, s in comps}; cent = {i: c for i, c, _ in comps}
    top = max(sizes.values())
    main_ids = [i for i in sizes if sizes[i] >= max(a_.min_area, 0.12 * top)]
    owner = {i: i for i in main_ids}
    for i in sizes:  # attach detached bits (a hand, a prop, a speech line) to the nearest figure
        if i in owner or sizes[i] < 40: continue
        cy, cx = cent[i]; owner[i] = min(main_ids, key=lambda j: (cent[j][0] - cy) ** 2 + (cent[j][1] - cx) ** 2)
    # order: group into rows by centre y, then left to right
    ys = sorted(cent[i][0] for i in main_ids)
    nrows = a_.rows or max(1, 1 + sum(1 for p, q in zip(ys, ys[1:]) if q - p > 0.18 * H))
    order = sorted(main_ids, key=lambda i: cent[i][0])
    rows = [order[k * len(order) // nrows:(k + 1) * len(order) // nrows] for k in range(nrows)]
    for r in rows:
        for i in sorted(r, key=lambda i: cent[i][1]):
            b = a.copy(); b[~np.isin(lab, [k for k, o in owner.items() if o == i]), 3] = 0; figs.append(crop(b))
    for k, f in enumerate(figs, 1):
        im = Image.fromarray(f)
        if a_.scale != 1: im = im.resize((int(im.width * a_.scale), int(im.height * a_.scale)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=3))
        im.save(os.path.join(a_.out, f'{a_.prefix}{k:02d}.png'))
    cols = 5; rows = (len(figs) + cols - 1) // cols; S = Image.new('RGBA', (cols * 300, max(1, rows) * 320), (119, 119, 119, 255))
    for k in range(len(figs)):
        im = Image.open(os.path.join(a_.out, f'{a_.prefix}{k + 1:02d}.png')); im.thumbnail((280, 290))
        S.alpha_composite(im, ((k % cols) * 300 + (300 - im.width) // 2, (k // cols) * 320 + 5))
    S.save(os.path.join(a_.out, '_contact.png')); print(f'{len(figs)} poses -> {a_.out} (check _contact.png)')

if __name__ == '__main__':
    main()
