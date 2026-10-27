"""Render a synthetic 'scanned' Persian page for pipeline tests (NOT used as training data)."""
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_page(text, font_path, size=30, width=1300, margin=110, line_gap=1.9, header='تاریخ ایران باستان', pageno='۱۲۳', seed=0):
    rng = random.Random(seed)
    font = ImageFont.truetype(font_path, size, layout_engine=ImageFont.Layout.RAQM)
    maxw = width - 2 * margin
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if font.getlength(t, direction='rtl', language='fa') > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    if cur: lines.append(cur)
    h = int(margin * 1.6 + (len(lines) + 3) * size * line_gap)
    im = Image.new('L', (width, h), 238)
    d = ImageDraw.Draw(im)
    def put(t, y, center=False):
        w = font.getlength(t, direction='rtl', language='fa')
        x = (width - w) / 2 if center else width - margin - w
        d.text((x, y), t, font=font, fill=25, direction='rtl', language='fa')
    put(header, margin * 0.5, center=True)
    y = margin * 1.1
    for l in lines: put(l, y); y += size * line_gap
    put(pageno, y + size, center=True)
    a = np.asarray(im).astype(np.float32) + np.random.RandomState(seed).normal(0, 6, (h, width))
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    im = im.rotate(rng.uniform(-0.3, 0.3), resample=Image.BICUBIC, fillcolor=238)
    return im, lines
