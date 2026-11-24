"""Build the website's logo files from the original logo image.

    python3 tools/logo/build.py tools/logo/source.png docs/assets [--dark tint|white|keep]

Light-mode files are the ORIGINAL artwork, unaltered: only the white
background is made transparent and the margin trimmed.

  logo/logo.png         full logo (mark, CHAIRPACT, Integrated Services Ltd., tagline, RC)
  logo/mark.png         the "pc" mark on its own (also used for the favicons)
  favicon-32.png, apple-touch-icon.png, favicon-512.png, og-image.png

Dark-mode files (logo/logo-dark.png, logo/mark-dark.png) use the treatment
given by --dark. Omit --dark to leave the dark files as they are.

  tint   black -> white; navy, grey and maroon -> lighter tints of the same hues
  white  single-colour white ("reversed") logo
  keep   black -> white; navy, grey and maroon kept exactly as in the original

(The "white tile" option needs no file: it's the light logo on a white
background, done in CSS.)
"""
import argparse
from PIL import Image
import numpy as np

p = argparse.ArgumentParser()
p.add_argument('src'); p.add_argument('out')
p.add_argument('--dark', choices=['tint', 'white', 'keep'])
args = p.parse_args()

rgb = np.asarray(Image.open(args.src).convert('RGB')).astype(float)
H, W, _ = rgb.shape

# --- Transparency: how far each pixel is from white. Colours are untouched.
alpha = np.clip((255 - rgb.min(2) - 18) / 70, 0, 1)
# The source is a scan: wipe paper speckle outside the artwork's box.
alpha[:60, :] = 0; alpha[520:, :] = 0; alpha[:, :50] = 0; alpha[:, 1562:] = 0

MARK_RIGHT = 486  # the mark ends here; the text starts to the right of it


def bbox(a):
    ys, xs = np.where(a > 0.04)
    return ys.min(), ys.max() + 1, xs.min(), xs.max() + 1


def make(colours, a):
    y0, y1, x0, x1 = bbox(a)
    img = np.dstack([colours, a * 255]).clip(0, 255).astype(np.uint8)
    return Image.fromarray(img[y0:y1, x0:x1])


def save(im, path, height=None, colors=256):
    if height:
        im = im.resize((round(im.width * height / im.height), height), Image.LANCZOS)
    im.quantize(colors=colors, method=Image.FASTOCTREE).save(path, optimize=True)
    print(path, im.size)


a_mark = alpha.copy(); a_mark[:, MARK_RIGHT:] = 0


# --- Dark-mode colour treatments ------------------------------------------
def regions():
    """Label each pixel as black / navy / grey / maroon using where it sits in the logo
    (maroon = tagline + RC, grey = inside the navy ring) and its smoothed colour."""
    def box(x, r):
        q = np.pad(x, ((r + 1, r), (r + 1, r)), mode='edge').cumsum(0).cumsum(1)
        return q[2*r+1:, 2*r+1:] - q[:-2*r-1, 2*r+1:] - q[2*r+1:, :-2*r-1] + q[:-2*r-1, :-2*r-1]
    w = (alpha > 0.85).astype(float)
    def smooth(r):
        ws = box(w, r)
        return np.dstack([box(rgb[..., c] * w, r) for c in range(3)]) / np.maximum(ws, 1e-6)[..., None], ws
    c4, ws4 = smooth(4); c12, _ = smooth(12)
    col = np.where((ws4 > 0)[..., None], c4, c12)
    R, G, B = col[..., 0], col[..., 1], col[..., 2]
    yy, xx = np.mgrid[:H, :W]
    lab = np.zeros((H, W), np.uint8)              # 0 black
    text = xx >= 490
    lab[text & ((yy >= 400) | ((yy < 165) & (xx > 1250)))] = 3   # maroon
    inmark = ~text
    navy = inmark & ((B - (R + G) / 2) > 14)
    lab[navy] = 1                                  # navy
    g0 = inmark & ~navy & ((R + G + B) / 3 > 62) & (np.abs(B - R) < 30) & (alpha > 0.9)
    d = np.hypot(yy - np.median(yy[g0]), xx - np.median(xx[g0]))
    lab[inmark & ~navy & (d < np.percentile(d[g0], 97) * 1.08)] = 2   # grey
    from PIL import ImageFilter
    return np.asarray(Image.fromarray(lab).filter(ImageFilter.ModeFilter(7)))


def dark_colours(mode):
    if mode == 'white':
        return np.full_like(rgb, 240)
    lab = regions()
    if mode == 'tint':
        pal = np.array([(240, 242, 248), (128, 146, 236), (184, 180, 182), (232, 116, 98)], float)
        return pal[lab]
    if mode == 'keep':   # original pixels everywhere except black, which becomes white
        out = rgb.copy(); out[lab == 0] = (240, 242, 248)
        return out


# --- Write files ------------------------------------------------------------
L = f'{args.out}/logo'
save(make(rgb, alpha), f'{L}/logo.png', height=440)
mark = make(rgb, a_mark)
save(mark, f'{L}/mark.png', height=480)

if args.dark:
    dc = dark_colours(args.dark)
    save(make(dc, alpha), f'{L}/logo-dark.png', height=440)
    save(make(dc, a_mark), f'{L}/mark-dark.png', height=480)

# Favicons: original mark, a little padding (white background for iOS home screen)
for size, name, bg in ((32, 'favicon-32.png', None), (180, 'apple-touch-icon.png', (255, 255, 255, 255)), (512, 'favicon-512.png', None)):
    side = round(max(mark.size) * 1.12)
    canvas = Image.new('RGBA', (side, side), bg or (0, 0, 0, 0))
    canvas.alpha_composite(mark, ((side - mark.width) // 2, (side - mark.height) // 2))
    canvas.resize((size, size), Image.LANCZOS).save(f'{args.out}/{name}', optimize=True)

# Social share image: the full original logo on white
og = Image.new('RGBA', (1200, 630), (255, 255, 255, 255))
full = make(rgb, alpha); full = full.resize((1000, round(full.height * 1000 / full.width)), Image.LANCZOS)
og.alpha_composite(full, (100, (630 - full.height) // 2))
og.convert('RGB').save(f'{args.out}/og-image.png', optimize=True)
