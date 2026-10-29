#!/usr/bin/env python3
"""Render training/eval lines and convert them to .lstmf files for lstmtraining.

usage: make_train_data.py --corpus corpus.txt --unicharset fas.lstm-unicharset --out data \
           --n-train 20000 --n-eval 1000 [--seed 1] [--jobs 4]

Corpus: UTF-8, one paragraph per line. Paragraphs are split deterministically (hash) into
  train (90%) / eval (5%) / holdout (5%). Holdout paragraphs are written to data/holdout_paras.txt and are
  never used for training or for the eval list; evaluate.py renders its synthetic test set from them.
"""
import argparse, glob, hashlib, os, random, re, subprocess, sys
from PIL import Image
from bidi.algorithm import get_display
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

def split_of(p):
    h = int(hashlib.md5(p.encode()).hexdigest(), 16) % 100
    return 'holdout' if h < 5 else ('eval' if h < 10 else 'train')

def visual(text):
    """Tesseract's LSTM trainer wants RTL line labels in VISUAL (left-to-right) order. Verified empirically:
    logical-order labels make training diverge (delta ~60%, BWER 97%), visual-order labels train normally.
    A bidi reorder (not a plain reversal) keeps digit runs left-to-right."""
    return get_display(text, base_dir='R')

def write_box(path, text, w, h):
    text = visual(C.to_label(text))
    # one box per character incl. spaces (visual order), then the end-of-line marker. Boxes are placeholders;
    # lstm.train only needs the transcription, it recognises the whole line (psm 13).
    with open(path, 'w', encoding='utf-8') as f:
        for ch in text:
            f.write(f'{ch} 0 0 {w - 1} {h - 1} 0\n')
        f.write(f'\t 0 0 {w - 1} {h - 1} 0\n')

def make_one(args):
    idx, split, words, out, allowed, seed, scheme, ezafe_p = args
    C.set_scheme(scheme)
    rng = random.Random(seed * 1000003 + idx)
    fonts = C.available_fonts()
    ez_rng = random.Random(seed * 7919 + idx)
    for _ in range(20):                                   # retry until the line passes the charset filter
        r = rng.random()
        if r < 0.22: text = C.digit_phrase(rng)                                   # numbers, decimals, percents
        else:
            text = C.corpus_line(words, rng)
            if rng.random() < 0.12: text = C.add_markers(text, rng)                 # [۱۱]
            if rng.random() < 0.12: text += ' ' + C.digit_phrase(rng)
        plain = C.is_plain(text)                                                  # decided BEFORE the scheme-specific cleaning: identical in every scheme
        text = C.clean_text(text)
        if scheme == 'distinct_ezafe' and ezafe_p > 0: text = C.inject_ezafe(text, ez_rng, ezafe_p)   # own rng: the image stream stays the same in every scheme
        if text and C.keep_line(text, allowed):
            img = C.make_line_image(text, fonts, rng)
            if img is not None: break
    else: return None
    base = os.path.join(out, split, f'{split}_{idx:07d}')
    r = finish(base, img, text)
    return (r, plain) if r else None

def finish(base, img, text):
    """save png + gt + box and let tesseract write the .lstmf; -> path or None"""
    os.makedirs(os.path.dirname(base), exist_ok=True)
    img.save(base + '.png'); open(base + '.gt.txt', 'w', encoding='utf-8').write(text + '\n')
    write_box(base + '.box', text, img.width, img.height)
    # lstm.train config lives in the default tessdata dir; language only needs to load
    subprocess.run(['tesseract', base + '.png', base, '--psm', '13', '-l', 'eng', 'lstm.train'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env={**os.environ, 'OMP_THREAD_LIMIT': '1'})
    if not os.path.exists(base + '.lstmf'): return None
    return base + '.lstmf'

def real_label(gt, scheme):
    """label text of a real line from a realdata 'distinct' export (full fidelity: ezafe, ، ٫ ٬ ٪). The same line set is used for every
    scheme so results are comparable; folded = clean_text (drops the ezafe mark), the fold of ، ٫ ٬ ٪ happens in write_box via to_label."""
    t = gt.strip()
    if scheme == 'distinct': return t.replace(C.EZAFE, '')
    if scheme == 'folded': return C.clean_text(t)
    return t

def make_real(args):
    idx, split, png, gt, out, allowed, scheme = args
    C.set_scheme(scheme)
    label = real_label(gt, scheme)
    if not label or not C.keep_line(label, allowed): return None
    img = C.pad_white(Image.open(png).convert('L'), 8)
    r = finish(os.path.join(out, 'real_' + split, f'{split}_{idx:07d}'), img, label)
    return (r, C.is_plain(gt)) if r else None

def real_items(real_dir, split, n, seed):
    """[(png, raw gt)] of up to n lines of <real_dir>/<split>/, deterministic order"""
    files = sorted(glob.glob(os.path.join(real_dir, split, '*.png')))
    random.Random(seed).shuffle(files)
    out = []
    for p in files:
        g = p[:-4] + '.gt.txt'
        if os.path.exists(g): out.append((p, open(g, encoding='utf-8').read().strip()))
        if len(out) >= n: break
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--corpus', required=True); ap.add_argument('--unicharset', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--n-train', type=int, default=20000); ap.add_argument('--n-eval', type=int, default=1000)
    ap.add_argument('--seed', type=int, default=1); ap.add_argument('--jobs', type=int, default=os.cpu_count() or 1)
    ap.add_argument('--keep-png', action='store_true')
    ap.add_argument('--scheme', default=os.environ.get('FT_LABEL_SCHEME', 'folded'), choices=C.SCHEMES)
    ap.add_argument('--ezafe-p', type=float, default=0.25, help='distinct_ezafe: share of heh-final words that get the mark in rendered lines')
    ap.add_argument('--real-dir', default=None, help='realdata tesseract export (distinct preset) with train/ and tune/ subfolders')
    ap.add_argument('--n-real', type=int, default=0); ap.add_argument('--n-real-eval', type=int, default=500)
    a = ap.parse_args()
    C.set_scheme(a.scheme); print('label scheme:', a.scheme, flush=True)
    if not C.available_fonts(): sys.exit(f'no fonts found in {C.FONT_DIR} (set FT_FONTS or put *.ttf in fonts/)')
    print('fonts:', sorted(C.available_fonts()), flush=True)
    allowed = C.load_unicharset(a.unicharset)
    # the corpus is read with the ezafe-keeping cleaner for EVERY scheme, so the train/eval/holdout split and the text stream are identical;
    # make_one() applies the scheme's own clean_text (which drops the mark for folded / distinct) when a line is rendered
    C.set_scheme('distinct_ezafe')
    paras = [C.clean_text(l) for l in open(a.corpus, encoding='utf-8') if l.strip()]
    paras = [p for p in paras if p]
    C.set_scheme(a.scheme)
    by = {'train': [], 'eval': [], 'holdout': []}
    for p in paras: by[split_of(p)].append(p)
    print({k: len(v) for k, v in by.items()}, flush=True)
    for s in ('train', 'eval'): os.makedirs(os.path.join(a.out, s), exist_ok=True)
    open(os.path.join(a.out, 'holdout_paras.txt'), 'w', encoding='utf-8').write('\n'.join(by['holdout']) + '\n')
    lists = {}
    with Pool(a.jobs) as pool:
        for split, n in (('train', a.n_train), ('eval', a.n_eval)):
            words = ' '.join(by[split] or by['train']).split(' ')
            jobs = [(i, split, words, a.out, allowed, a.seed, a.scheme, a.ezafe_p) for i in range(n)]
            res = []; plain = []
            for k, r in enumerate(pool.imap(make_one, jobs, chunksize=8)):
                if r: res.append(r[0]); plain += [r[0]] if r[1] else []
                if k % 2000 == 1999: print(split, k + 1, '/', n, flush=True)
            lists[split] = res
            open(os.path.join(a.out, f'list.{split}'), 'w').write('\n'.join(res) + '\n')
            if split == 'eval': open(os.path.join(a.out, 'list.eval_plain'), 'w').write('\n'.join(plain) + '\n')
            print(split, 'lstmf files:', len(res), 'plain:', len(plain), flush=True)
        if a.real_dir:
            for split, n, name in (('train', a.n_real, 'train'), ('tune', a.n_real_eval, 'eval_real')):
                items = real_items(a.real_dir, split, n, a.seed)
                res = []; plain = []
                for r in pool.imap(make_real, [(i, split, p, g, a.out, allowed, a.scheme) for i, (p, g) in enumerate(items)], chunksize=8):
                    if r: res.append(r[0]); plain += [r[0]] if r[1] else []
                print('real', split, 'lines:', len(items), '-> lstmf', len(res), 'plain', len(plain), flush=True)
                if split == 'train':
                    mixed = lists['train'] + res; random.Random(a.seed).shuffle(mixed); lists['train'] = mixed
                    open(os.path.join(a.out, 'list.train'), 'w').write('\n'.join(mixed) + '\n')
                else:
                    open(os.path.join(a.out, 'list.eval_real'), 'w').write('\n'.join(res) + '\n')
                    open(os.path.join(a.out, 'list.eval_real_plain'), 'w').write('\n'.join(plain) + '\n')
    if not a.keep_png:
        for s in ('train', 'eval', 'real_train', 'real_tune'):
            d = os.path.join(a.out, s)
            if not os.path.isdir(d): continue
            for f in os.listdir(d):
                if f.endswith(('.png', '.box', '.gt.txt')) and os.path.exists(os.path.join(d, f.split('.')[0] + '.lstmf')): os.remove(os.path.join(d, f))

if __name__ == '__main__':
    main()
