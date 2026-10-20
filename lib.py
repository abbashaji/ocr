import os, subprocess, tempfile, json, hashlib
import numpy as np
from PIL import Image, ImageFilter
import bench as B
os.environ['OMP_THREAD_LIMIT'] = '1'
HERE = os.path.dirname(os.path.abspath(__file__))
REF = open(os.path.join(HERE, 'ref.txt'), encoding='utf-8').read()
REF_P = [p for p in REF.split('\n') if p.strip()]          # paragraph 1, paragraph 2
SAMPLES = {'clean': os.path.join(HERE, 'samples/client_clean.png'), 'low': os.path.join(HERE, 'samples/client_low.jpg')}
CACHE = os.path.join(HERE, 'cache.json')
_cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

def to_gray(im, mode):
    im = im.convert('RGB'); a = np.asarray(im).astype(np.float32)
    if mode == 'L': g = 0.299*a[...,0] + 0.587*a[...,1] + 0.114*a[...,2]
    elif mode == 'min': g = a.min(axis=2)
    elif mode == 'R': g = a[...,0]
    else: raise ValueError(mode)
    return Image.fromarray(np.clip(g, 0, 255).astype(np.uint8))

def scale(im, s, resample=Image.LANCZOS):
    return im if s == 1 else im.resize((round(im.width*s), round(im.height*s)), resample)

def tess(im, psm=6, extra=(), tessdir=None):
    tessdir = tessdir or os.environ.get('OCR_TESSDIR') or B.TESS_BEST; lang = os.environ.get('OCR_LANG', 'fas')
    buf = im.tobytes() + str((im.size, psm, extra, tessdir, lang)).encode()
    key = hashlib.md5(buf).hexdigest()
    if key in _cache: return _cache[key]
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f: p = f.name
    im.save(p)
    cmd = ['tesseract', p, '-', '-l', lang, '--psm', str(psm), '--tessdata-dir', tessdir] + list(extra)
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    os.unlink(p); _cache[key] = out
    return out

def save_cache():
    snap = dict(_cache); tmp = CACHE + '.tmp'
    json.dump(snap, open(tmp, 'w'), ensure_ascii=False); os.replace(tmp, CACHE)

def sc(ref, hyp):
    s = B.score(ref, hyp); return 100*s['letter'], 100*s['word']

def tess_tsv(im, psm=7, tessdir=None):
    """returns (text, [(word, conf), ...]) from Tesseract TSV output, cached."""
    tessdir = tessdir or os.environ.get('OCR_TESSDIR') or B.TESS_BEST; lang = os.environ.get('OCR_LANG', 'fas')
    key = 'tsv:' + hashlib.md5(im.tobytes() + str((im.size, psm, tessdir, lang)).encode()).hexdigest()
    if key in _cache: return tuple(_cache[key][0:1]) + (list(map(tuple, _cache[key][1])),)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f: p = f.name
    im.save(p)
    out = subprocess.run(['tesseract', p, '-', '-l', lang, '--psm', str(psm), '--tessdata-dir', tessdir, '-c', 'tessedit_create_tsv=1'], capture_output=True, text=True).stdout
    os.unlink(p)
    words = []
    for row in out.split('\n')[1:]:
        c = row.split('\t')
        if len(c) >= 12 and c[0] == '5' and c[11].strip():
            words.append((c[11].strip(), float(c[10])))
    text = ' '.join(w for w, _ in words); _cache[key] = [text, words]
    return text, words

def tess_boxes(im, psm=7, tessdir=None):
    """-> list of (word, conf, left, top, w, h) in the coordinates of `im`, cached."""
    tessdir = tessdir or os.environ.get('OCR_TESSDIR') or B.TESS_BEST; lang = os.environ.get('OCR_LANG', 'fas')
    key = 'box:' + hashlib.md5(im.tobytes() + str((im.size, psm, tessdir, lang)).encode()).hexdigest()
    if key in _cache: return [tuple(x) for x in _cache[key]]
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f: p = f.name
    im.save(p)
    out = subprocess.run(['tesseract', p, '-', '-l', lang, '--psm', str(psm), '--tessdata-dir', tessdir, '-c', 'tessedit_create_tsv=1'], capture_output=True, text=True).stdout
    os.unlink(p); res = []
    for row in out.split('\n')[1:]:
        c = row.split('\t')
        if len(c) >= 12 and c[0] == '5' and c[11].strip(): res.append((c[11].strip(), float(c[10]), int(c[6]), int(c[7]), int(c[8]), int(c[9])))
    _cache[key] = res; return res
