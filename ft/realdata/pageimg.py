"""Page image -> line crops with the PRODUCT segmenter, plus per-line OCR with the shipped model (single scale)."""
import os, subprocess, tempfile, concurrent.futures as cf
import numpy as np
from PIL import Image
from matnyab.engine import imageprep, segment

TARGET_H = 44          # crop height fed to Tesseract (px); product uses 28..56
PAD = 12

def deskew_angle(gray, max_deg=2.0, step=0.25):
    """Projection-profile skew estimate on a downscaled copy; returns degrees (positive = rotate counter-clockwise)."""
    small = gray.copy(); small.thumbnail((900, 900))
    a = np.asarray(small); thr = segment.otsu(a)
    ink = Image.fromarray(((a < thr) * 255).astype(np.uint8))
    best, best_v = 0.0, -1.0
    for ang in np.arange(-max_deg, max_deg + 1e-6, step):
        r = np.asarray(ink.rotate(ang, resample=Image.BILINEAR, fillcolor=0)).astype(np.float32).sum(1)
        v = float(np.var(r))
        if v > best_v: best, best_v = float(ang), v
    return best

def page_lines(img, deskew_if_over=0.4):
    """-> (gray, [dict(band=(y0,y1), crop=PIL gray crop (full width, product crop), top=int)], info)"""
    rgb = imageprep.load_image(img)
    gray, size = imageprep.prepare(rgb)
    info = {'size': list(gray.size), 'deskew': 0.0}
    if imageprep.is_blank(gray): return gray, [], info
    ang = deskew_angle(gray)
    if abs(ang) >= deskew_if_over:
        gray = gray.rotate(ang, resample=Image.BICUBIC, expand=False, fillcolor=int(np.median(np.asarray(gray))))
        info['deskew'] = ang
    bands = segment.segment_lines(gray)
    cr = segment.crops(gray, bands)
    return gray, [dict(band=b, crop=c, top=t) for b, (c, t) in zip(bands, cr)], info

def trim_horizontal(crop, pad=10):
    a = np.asarray(crop); ink = segment.ink_mask(a)
    cols = np.where(ink.sum(0) > 0)[0]
    if len(cols) == 0: return None
    x0, x1 = max(0, cols[0] - pad), min(crop.width, cols[-1] + 1 + pad)
    return crop.crop((x0, 0, x1, crop.height))

def _ocr_one(args):
    im_path, tessdata, psm = args
    r = subprocess.run(['tesseract', im_path, 'stdout', '--tessdata-dir', tessdata, '-l', 'fas', '--psm', str(psm)],
                       capture_output=True, text=True, timeout=60, env=dict(os.environ, OMP_THREAD_LIMIT='1'))
    return ' '.join(r.stdout.split())

def ocr_crops(crops, tessdata, workers=4):
    """crops: list of PIL gray images (full-width line crops) -> list of text. Scales to TARGET_H and pads white."""
    with tempfile.TemporaryDirectory() as d:
        paths = []
        for i, c in enumerate(crops):
            s = TARGET_H / max(1, c.height)
            im = c.resize((max(1, round(c.width * s)), TARGET_H), Image.LANCZOS)
            w = Image.new('L', (im.width + 2 * PAD, im.height + 2 * PAD), 255); w.paste(im, (PAD, PAD))
            p = os.path.join(d, f'{i}.png'); w.save(p); paths.append((p, tessdata, 7))
        with cf.ThreadPoolExecutor(workers) as ex:
            return list(ex.map(_ocr_one, paths))
