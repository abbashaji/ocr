#!/usr/bin/env python3
"""Render training/eval lines and convert them to .lstmf files for lstmtraining.

usage: make_train_data.py --corpus corpus.txt --unicharset fas.lstm-unicharset --out data \
           --n-train 20000 --n-eval 1000 [--seed 1] [--jobs 4]

Corpus: UTF-8, one paragraph per line. Paragraphs are split deterministically (hash) into
  train (90%) / eval (5%) / holdout (5%). Holdout paragraphs are written to data/holdout_paras.txt and are
  never used for training or for the eval list; evaluate.py renders its synthetic test set from them.
"""
import argparse, hashlib, os, random, subprocess, sys
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
    idx, split, words, out, allowed, seed = args
    rng = random.Random(seed * 1000003 + idx)
    fonts = C.available_fonts()
    for _ in range(20):                                   # retry until the line passes the charset filter
        r = rng.random()
        if r < 0.22: text = C.digit_phrase(rng)                                   # numbers, decimals, percents
        else:
            text = C.corpus_line(words, rng)
            if rng.random() < 0.12: text = C.add_markers(text, rng)                 # [۱۱]
            if rng.random() < 0.12: text += ' ' + C.digit_phrase(rng)
        text = C.clean_text(text)
        if text and C.keep_line(text, allowed):
            img = C.make_line_image(text, fonts, rng)
            if img is not None: break
    else: return None
    base = os.path.join(out, split, f'{split}_{idx:07d}')
    img.save(base + '.png'); open(base + '.gt.txt', 'w', encoding='utf-8').write(text + '\n')
    write_box(base + '.box', text, img.width, img.height)
    # lstm.train config lives in the default tessdata dir; language only needs to load
    subprocess.run(['tesseract', base + '.png', base, '--psm', '13', '-l', 'eng', 'lstm.train'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env={**os.environ, 'OMP_THREAD_LIMIT': '1'})
    if not os.path.exists(base + '.lstmf'): return None
    return base + '.lstmf'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--corpus', required=True); ap.add_argument('--unicharset', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--n-train', type=int, default=20000); ap.add_argument('--n-eval', type=int, default=1000)
    ap.add_argument('--seed', type=int, default=1); ap.add_argument('--jobs', type=int, default=os.cpu_count() or 1)
    ap.add_argument('--keep-png', action='store_true')
    a = ap.parse_args()
    if not C.available_fonts(): sys.exit(f'no fonts found in {C.FONT_DIR} (set FT_FONTS or put *.ttf in fonts/)')
    print('fonts:', sorted(C.available_fonts()), flush=True)
    allowed = C.load_unicharset(a.unicharset)
    paras = [C.clean_text(l) for l in open(a.corpus, encoding='utf-8') if l.strip()]
    paras = [p for p in paras if p]
    by = {'train': [], 'eval': [], 'holdout': []}
    for p in paras: by[split_of(p)].append(p)
    print({k: len(v) for k, v in by.items()}, flush=True)
    for s in ('train', 'eval'): os.makedirs(os.path.join(a.out, s), exist_ok=True)
    open(os.path.join(a.out, 'holdout_paras.txt'), 'w', encoding='utf-8').write('\n'.join(by['holdout']) + '\n')
    lists = {}
    with Pool(a.jobs) as pool:
        for split, n in (('train', a.n_train), ('eval', a.n_eval)):
            words = ' '.join(by[split] or by['train']).split(' ')
            jobs = [(i, split, words, a.out, allowed, a.seed) for i in range(n)]
            res = []
            for k, r in enumerate(pool.imap(make_one, jobs, chunksize=8)):
                if r: res.append(r)
                if k % 2000 == 1999: print(split, k + 1, '/', n, flush=True)
            lists[split] = res
            open(os.path.join(a.out, f'list.{split}'), 'w').write('\n'.join(res) + '\n')
            print(split, 'lstmf files:', len(res), flush=True)
    if not a.keep_png:
        for s in ('train', 'eval'):
            d = os.path.join(a.out, s)
            for f in os.listdir(d):
                if f.endswith(('.png', '.box', '.gt.txt')) and os.path.exists(os.path.join(d, f.split('.')[0] + '.lstmf')): os.remove(os.path.join(d, f))

if __name__ == '__main__':
    main()
