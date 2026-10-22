"""Shared helpers for the Tesseract fine-tune: text cleaning, line rendering, degradations.

Rendering mimics what pipeline2.recognize_tok feeds Tesseract: one text line, tight crop (+5 px),
scaled to a height of 28..56 px, white padding 12 px. Training images therefore look like the
pipeline's inputs (not like whole pages).
"""
import io, os, random, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
def _font_dir():
    for d in (os.environ.get('FT_FONTS'), os.path.join(HERE, 'fonts'), os.path.join(os.path.dirname(HERE), 'fonts')):
        if d and os.path.isdir(d): return d
    return os.path.join(os.path.dirname(HERE), 'fonts')
FONT_DIR = _font_dir()

# name -> file. Missing files are skipped, so a partial font set still works.
FONT_FILES = {
    'Vazirmatn': 'Vazirmatn.ttf', 'VazirmatnBold': 'VazirmatnBold.ttf',
    'NotoNaskh': 'NotoNaskh.ttf', 'NotoNaskhBold': 'NotoNaskhBold.ttf',
    'NotoKufi': 'NotoKufi.ttf', 'DejaVu': 'DejaVu.ttf', 'DejaVuBold': 'DejaVuBold.ttf',
}
# Extra fonts dropped into fonts/extra/*.ttf (e.g. Tahoma, Segoe UI, Arial copied from the client's PC) are used too.
def available_fonts():
    out = {k: os.path.join(FONT_DIR, v) for k, v in FONT_FILES.items() if os.path.exists(os.path.join(FONT_DIR, v))}
    extra = os.path.join(FONT_DIR, 'extra')
    if os.path.isdir(extra):
        for f in sorted(os.listdir(extra)):
            if f.lower().endswith(('.ttf', '.otf')): out['extra_' + f] = os.path.join(extra, f)
    return out

# Wikipedia body text colours: black-ish, #202122, link blue #0645ad, visited/new-link variants.
TEXT_COLORS = [(0, 0, 0), (32, 33, 34), (32, 33, 34), (6, 69, 173), (51, 102, 204), (11, 0, 128), (186, 0, 0)]

# ---- characters -------------------------------------------------------------------------------
# The stock tessdata_best fas unicharset (95 entries) has no class for these glyphs. Extending the charset through
# lstmtraining --old_traineddata was tested and is lossy (BCER 15% -> 28% on lines without any new character), so
# instead the glyphs are trained onto existing, otherwise unused classes and restored by context rules afterwards
# (pipeline2.restore_placeholders). The image keeps the real glyph; only the training LABEL is mapped.
LABEL_MAP = {'،': ',', '٬': ',', '٫': '.', '٪': '#', '%': '#', ';': '؛', '–': '-', '—': '-'}
def to_label(text):
    return ''.join(LABEL_MAP.get(c, c) for c in text)
PERSIAN_DIGITS = '۰۱۲۳۴۵۶۷۸۹'
_ARABIC_INDIC = str.maketrans('٠١٢٣٤٥٦٧٨٩', PERSIAN_DIGITS)
_NORM = str.maketrans({'ي': 'ی', 'ك': 'ک', 'ة': 'ه', 'ۀ': 'ه', '\u00a0': ' ', '\u2009': ' ', '\u202f': ' ', '\u200b': '', '\u200e': '', '\u200f': '', '\u202a': '', '\u202b': '', '\u202c': '', '\ufeff': '', '‐': '-', '‑': '-', '−': '-', '“': '«', '”': '»', '‘': "'", '’': "'", '…': '...'})
MARKER = re.compile(r'\[\s*[0-9۰-۹٠-٩]+\s*\]')                    # citation markers like [۱۱]
HARAKAT = re.compile('[\u064b-\u065f\u0670]')

def clean_text(s):
    s = s.translate(_NORM).translate(_ARABIC_INDIC)
    s = HARAKAT.sub('', s)
    return re.sub(r'[ \t]+', ' ', s).strip()

def load_unicharset(path):
    """chars (as str) listed in a *.lstm-unicharset / unicharset file"""
    chars = set()
    with open(path, encoding='utf-8') as f:
        next(f)
        for ln in f:
            c = ln.split(' ')[0]
            if c not in ('NULL', 'Joined', '|Broken|0|1') and len(c) == 1: chars.add(c)
    return chars

def keep_line(s, allowed):
    """True when every non-space char is in the model's unicharset or has a placeholder label."""
    return all((c in allowed) or (c in LABEL_MAP) or c == ' ' for c in s)

# ---- rendering --------------------------------------------------------------------------------
_font_cache = {}
def get_font(path, size):
    k = (path, size)
    if k not in _font_cache:
        _font_cache[k] = ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)
    return _font_cache[k]

def render_line(text, font_path, size, color=(0, 0, 0), bg=255, pad=8):
    """-> RGB image, one line, RTL shaping via Raqm."""
    font = get_font(font_path, size)
    w = int(font.getlength(text, direction='rtl', language='fa')) + 2 * pad + 2
    asc, desc = font.getmetrics()
    im = Image.new('RGB', (w, asc + desc + 2 * pad), (bg, bg, bg))
    ImageDraw.Draw(im).text((pad, pad), text, font=font, fill=color, direction='rtl', language='fa')
    return im

def _otsu(a):
    h, _ = np.histogram(a, bins=256, range=(0, 256)); tot = a.size
    s_all = np.dot(np.arange(256), h); wb = sb = 0; best = (0, 128)
    for t in range(256):
        wb += h[t]
        if wb == 0 or wb == tot: continue
        sb += t * h[t]; mb = sb / wb; mf = (s_all - sb) / (tot - wb)
        v = wb * (tot - wb) * (mb - mf) ** 2
        if v > best[0]: best = (v, t)
    return best[1]

def to_gray(im):
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    return Image.fromarray(np.clip(0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2], 0, 255).astype(np.uint8))

def tight_crop_rows(g, pad=5, thr=0.015):
    """vertical crop like lines.segment_lines/crops: rows whose ink profile exceeds 1.5% of the max, +pad"""
    a = np.asarray(g); ink = a < _otsu(a)
    prof = np.convolve(ink.sum(1).astype(float), np.ones(3) / 3, mode='same')
    rows = np.where(prof > thr * max(prof.max(), 1))[0]
    if len(rows) == 0: return g
    y0, y1 = rows[0], rows[-1] + 1
    return g.crop((0, max(0, y0 - pad), g.width, min(g.height, y1 + pad)))

def pad_white(im, p):
    w = Image.new('L', (im.width + 2 * p, im.height + 2 * p), 255); w.paste(im, (p, p)); return w

def degrade(im, rng, font_size=20, low_p=0.55):
    """RGB line image -> grey image in pipeline-input form. Mix of clean and low-quality cases."""
    r = rng.random()
    if rng.random() < 0.35:                                         # slight rotation (screenshots are mostly straight)
        im = im.rotate(rng.uniform(-0.5, 0.5), resample=Image.BICUBIC, expand=True, fillcolor=(255, 255, 255))
    low = r < low_p                                                 # ~55% low-quality by default
    if low and rng.random() < 0.8:                                  # downscale (the main real-world degradation)
        f = max(rng.uniform(0.45, 0.9), 10.0 / font_size)      # keep the effective text size >= ~10 px
        f = min(f, 1.0)
        im = im.resize((max(8, int(im.width * f)), max(8, int(im.height * f))), rng.choice([Image.BILINEAR, Image.BICUBIC, Image.BOX]))
    if low and rng.random() < 0.4:
        im = im.filter(ImageFilter.GaussianBlur(rng.uniform(0.3, 1.1)))
    g = to_gray(im)
    if low and rng.random() < 0.3:
        a = np.asarray(g).astype(np.float32) + np.random.default_rng(rng.randrange(1 << 30)).normal(0, rng.uniform(3, 14), (g.height, g.width))
        g = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if rng.random() < (0.6 if low else 0.15):                       # JPEG, as in the client's low-quality sample
        b = io.BytesIO(); g.save(b, 'JPEG', quality=rng.randint(25, 92)); g = Image.open(io.BytesIO(b.getvalue())).convert('L')
    g = tight_crop_rows(g, pad=5)
    T = rng.choice([28, 32, 36, 40, 44, 48, 56])                     # pipeline's TARGETS
    g = g.resize((max(8, round(g.width * T / g.height)), T), Image.LANCZOS)
    return pad_white(g, 12)

_cmaps = {}
def font_supports(path, text):
    """True if the font's cmap covers every non-space char (avoids tofu boxes). Needs fontTools; else assume yes."""
    try:
        if path not in _cmaps:
            from fontTools.ttLib import TTFont
            _cmaps[path] = set(TTFont(path, lazy=True).getBestCmap().keys())
    except Exception:
        return True
    cm = _cmaps[path]
    return all(ord(c) in cm for c in set(text) if c not in ' \u200c')

def make_line_image(text, fonts, rng):
    """-> grey line image, or None when no font covers the text"""
    ok = [n for n in fonts if font_supports(fonts[n], text)]
    if not ok: return None
    name = rng.choice(ok)
    size = rng.choice([13, 14, 15, 16, 18, 20, 22, 24, 28, 32, 40])
    color = rng.choice(TEXT_COLORS)
    return degrade(render_line(text, fonts[name], size, color=color, bg=rng.choice([255, 255, 255, 250, 248])), rng, size)

# ---- text sources -----------------------------------------------------------------------------
def pdig(n, rng=random):
    s = str(n); return s.translate(str.maketrans('0123456789', PERSIAN_DIGITS))

def digit_phrase(rng):
    """Synthetic number-heavy snippets: years, decimals, percents, ranges, thousands separators."""
    y = rng.randint(1200, 1405); n = rng.randint(2, 99999999)
    dec = f"{pdig(rng.randint(0, 999))}٫{pdig(rng.randint(0, 99))}"
    big = f"{pdig(rng.randint(1, 999))}٬{pdig(rng.randint(0, 999)):0>3}" + (f"٬{pdig(rng.randint(0, 999)):0>3}" if rng.random() < .5 else '')
    pct = f"{pdig(rng.randint(1, 99))}٪" if rng.random() < .5 else f"{dec}٪"
    pieces = [
        f"در سال {pdig(y)} خورشیدی", f"حدود {dec} میلیون نفر", f"جمعیت {pdig(n)} نفر", f"مساحت {big} کیلومتر مربع",
        f"{pct} از مردم", f"بین {pdig(y)} تا {pdig(y + rng.randint(1, 40))}", f"{dec} کیلومتر", f"در {pdig(rng.randint(1, 31))} فروردین {pdig(y)}",
        f"رتبه {pdig(rng.randint(1, 190))} جهان", f"{pdig(rng.randint(1, 300))}–{pdig(rng.randint(301, 900))} متر", f"({pdig(rng.randint(1000, 2025))} میلادی)",
        f"{pdig(rng.randint(1, 99))}،{pdig(rng.randint(100, 999))}", f"ارتفاع {big} متر", f"[{pdig(rng.randint(1, 140))}]",
    ]
    rng.shuffle(pieces)
    return ' '.join(pieces[:rng.randint(2, 5)])

def corpus_line(words, rng, lo=4, hi=15):
    n = rng.randint(lo, hi)
    if len(words) <= n: return ' '.join(words)
    i = rng.randrange(len(words) - n)
    return ' '.join(words[i:i + n])

def add_markers(s, rng):
    """insert citation markers like [۱۱] after a random word (they appear in real screenshots)"""
    w = s.split(' ')
    if len(w) < 3: return s
    w.insert(rng.randint(1, len(w)), f"[{pdig(rng.randint(1, 160))}]")
    return ' '.join(w)
