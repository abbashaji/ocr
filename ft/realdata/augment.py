"""Export-time augmentation of REAL line images (grey, PIL). Seeded; clean originals are never modified.
Mimics Chromium z75/z50 downscaling, phone-photo blur/noise/JPEG, small rotation/perspective, contrast and shadow."""
import io, random
import numpy as np
from PIL import Image, ImageFilter

def _bg(im):
    return int(np.percentile(np.asarray(im), 90))

def augment(im, rng):
    im = im.convert('L'); w0, h0 = im.size; bg = _bg(im)
    if rng.random() < 0.5:                                           # small rotation
        im = im.rotate(rng.uniform(-0.8, 0.8), resample=Image.BICUBIC, expand=True, fillcolor=bg)
    if rng.random() < 0.3:                                           # mild perspective
        w, h = im.size; d = rng.uniform(0.01, 0.05) * h
        q = [rng.uniform(-d, d) for _ in range(4)]
        im = im.transform((w, h), Image.QUAD, (0, q[0], 0, h + q[1], w, h + q[2], w, q[3]), Image.BICUBIC, fillcolor=bg)
    if rng.random() < 0.6:                                           # downscale then back (z75 / z50 / low-res photo)
        f = rng.uniform(0.45, 0.9)
        im = im.resize((max(8, int(im.width * f)), max(8, int(im.height * f))), rng.choice([Image.BILINEAR, Image.BICUBIC, Image.BOX]))
        im = im.resize((w0, h0), Image.BICUBIC)
    if rng.random() < 0.35: im = im.filter(ImageFilter.GaussianBlur(rng.uniform(0.3, 1.2)))
    a = np.asarray(im).astype(np.float32)
    if rng.random() < 0.5:                                           # contrast / gamma
        a = 255 * (a / 255) ** rng.uniform(0.7, 1.4); a = (a - 128) * rng.uniform(0.7, 1.15) + 128
    if rng.random() < 0.35:                                          # shadow gradient
        ramp = np.linspace(rng.uniform(0.75, 1.0), rng.uniform(0.9, 1.05), a.shape[1])[None, :]
        a = a * (ramp if rng.random() < 0.5 else ramp[:, ::-1])
    if rng.random() < 0.4: a = a + np.random.default_rng(rng.randrange(1 << 30)).normal(0, rng.uniform(3, 12), a.shape)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if rng.random() < 0.5:                                           # JPEG
        b = io.BytesIO(); im.save(b, 'JPEG', quality=rng.randint(25, 90)); im = Image.open(io.BytesIO(b.getvalue())).convert('L')
    return im
