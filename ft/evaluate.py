#!/usr/bin/env python3
"""Evaluate baseline vs fine-tuned Tesseract on: client samples, real screenshot splits (tune/final), synthetic holdout.

usage (from repo root):
  python ft/evaluate.py --base-dir tess --ft-file fas_ft.traineddata --tests tests --holdout data/holdout_paras.txt \
         --out results [--limit N] [--sets client,real_tune,real_final,synth]

Engines (all computed for both models):  plain = whole image, psm 6, no post-processing
                                          v2lex = pipeline2 (per-line, 7 scales, medoid, lexicon correction)
                                          v2raw = pipeline2 without the lexicon step
Product engine (ocr2, the engine shipped in MatnYab) is evaluated too, with --engines legacy,ocr2 (default):
                                          ocr2/auto, ocr2/raw, ocr2/lex = TesseractEngine.recognize(OcrOptions(mode=...))
                                          ocr2 removes citation markers itself, so its 'raw' view already has no markers.
Metrics: micro-averaged word and letter accuracy (1 - edit distance / reference length), plus two strict F1 scores that
the letter/word metrics are blind to: 'num' (numbers incl. their decimal/thousands separator, e.g. ۱٫۶۴ vs ۱،۶۴ vs ،۶۴)
and 'punct' (the sequence of punctuation marks). F1 = 2*LCS/(len(ref)+len(hyp)), so extra numbers or marks in the output
are penalised and the score stays within 0..100. Each is reported twice:
  'raw'   = OCR output as is
  'nomark'= bracketed citation markers like [۱۱] (in any bracket order, e.g. ]۱۱[) removed from the OCR output first
            (they are not in the ground truth)
"""
import argparse, glob, io, json, os, re, shutil, sys, time, unicodedata
from concurrent.futures import ThreadPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import functools
import postproc as P
P.candidates = functools.lru_cache(maxsize=None)(P.candidates)
import pipeline2 as Q
from lib import *
from rapidfuzz.distance import Levenshtein as Lev, LCSseq

LEGACY_ENGS = ('plain', 'v2raw', 'v2lex')
OCR2_ENGS = ('ocr2/auto', 'ocr2/raw', 'ocr2/lex')
OCR2_MODES = ('auto', 'raw', 'lex')
CFG = dict(alpha=1.5, margin=0.3, floor=2.5, guard=2, conf_skip=90, sub_other=2.0, indel=2.0, max_cost=2.0, target=2.5)
CFG_RAW = {**CFG, 'conf_skip': 0}
# Citation markers in any bracket order: Tesseract returns visual order, so [۱۶] often arrives as ]۱۶[ (or garbled: ]۲]]۱[).
MARK = re.compile(r'(?:[\[\]\(\)]\s*[0-9۰-۹٠-٩]{0,3}\s*)+[\[\]\(\)]')

NUM = re.compile(r'\d+(?:[.,٫٬،]\d+)*')

def numbers(s):
    """Numbers as written, digits folded to ASCII; ٫ and ٬ folded to . and , so only a WRONG separator mismatches."""
    return [m.replace('٫', '.').replace('٬', ',') for m in NUM.findall(B.base(s))]

def puncts(s):
    """The sequence of punctuation marks (letters, digits and spaces dropped)."""
    return ''.join(c for c in B.base(s) if unicodedata.category(c).startswith('P') or c in '٪٫٬')

def counts(ref, hyp):
    rw, hw, rl, hl = B.words(ref), B.words(hyp), B.letters(ref), B.letters(hyp)
    rn, hn, rp, hp = numbers(ref), numbers(hyp), puncts(ref), puncts(hyp)
    return (Lev.distance(rw, hw), len(rw), Lev.distance(rl, hl), len(rl),
            LCSseq.similarity(rn, hn), len(rn), len(hn), LCSseq.similarity(rp, hp), len(rp), len(hp))

def f1(lcs, nref, nhyp):
    return round(100 * 2 * lcs / (nref + nhyp), 2) if nref + nhyp else None

def load_sets(a):
    sets = {}
    if 'client' in a.sets:
        sets['client'] = [(os.path.basename(p), Image.open(p).convert('RGB'), REF, 'client') for p in sorted(SAMPLES.values())]
    for name in ('tune', 'final'):
        if f'real_{name}' in a.sets:
            items = []
            for p in sorted(glob.glob(os.path.join(a.tests, name, '*.[pj][np]g'))):
                items.append((os.path.basename(p), Image.open(p).convert('RGB'), open(p.rsplit('.', 1)[0] + '.txt', encoding='utf-8').read(), re.search(r'_(z\d+)\.', p).group(1)))
            sets[f'real_{name}'] = items
    if 'synth' in a.sets and a.holdout and os.path.exists(a.holdout):
        paras = [p for p in open(a.holdout, encoding='utf-8').read().split('\n') if 60 <= len(p) <= 420][:6]
        items = []
        for pi, para in enumerate(paras):
            for font in ('Vazirmatn', 'NotoNaskh', 'NotoKufi'):
                if not os.path.exists(os.path.join(HERE, 'fonts', B.FONTS[font])): continue
                for size in (16, 24):
                    base = B.render(para, B.FONTS[font], size=size, width=820)
                    items.append((f'synth_{pi}_{font}_{size}_clean', base.convert('RGB'), para, 'clean'))
                    lo = base.resize((base.width * 6 // 10, base.height * 6 // 10), Image.BILINEAR); b = io.BytesIO(); lo.save(b, 'JPEG', quality=30)
                    items.append((f'synth_{pi}_{font}_{size}_low', Image.open(io.BytesIO(b.getvalue())).convert('RGB'), para, 'low'))
        sets['synth'] = items
    if a.limit:
        sets = {k: v[:a.limit] for k, v in sets.items()}
    return sets

def run_model(tag, tessdir, lang, sets, threads):
    os.environ['OCR_TESSDIR'] = tessdir; os.environ['OCR_LANG'] = lang
    def one(it):
        name, im, ref, grp = it; g = to_gray(im, 'L')
        lines = Q.recognize_tok(im)
        return dict(plain=tess(g, 6), v2lex=Q.render(lines, **CFG), v2raw=Q.render(lines, **CFG_RAW))
    out = {}
    for sname, items in sets.items():
        t = time.time()
        with ThreadPoolExecutor(threads) as ex: out[sname] = list(ex.map(one, items))
        save_cache(); print(f'[{tag}] {sname}: {len(items)} images, {time.time() - t:.0f}s', flush=True)
    return out

def make_ocr2_engine(model_dir):
    """TesseractEngine whose line recognition is memoised per image, so the three modes cost one recognition.

    The modes differ only in the correction step after recognition (matnyab.engine.tesseract_engine.recognize), so
    the Tesseract work (7 scales per line) is identical. The cache stores the wall time of the recognition; every
    mode is charged recognition time + its own elapsed correction time, which is what a real run of that mode costs."""
    from matnyab.engine.tesseract_engine import TesseractEngine

    class SharedEngine(TesseractEngine):
        cache = None                                  # (key, grid, seconds) of the last recognised image

        def _run_units(self, crops, grid, workers, remove_markers, report, cancel):
            key = (remove_markers, len(crops), tuple(hash(c.tobytes()) for c, _ in crops))
            if self.cache is not None and self.cache[0] == key:
                for row, saved in zip(grid, self.cache[1]):
                    row[:] = saved
                self.last_recognition_s = self.cache[2]
                self.cache_hit = True
                return
            t = time.perf_counter()
            super()._run_units(crops, grid, workers, remove_markers, report, cancel)
            self.last_recognition_s = time.perf_counter() - t
            self.cache = (key, [list(row) for row in grid], self.last_recognition_s)
            self.cache_hit = False
    return SharedEngine(model_dir=model_dir)

def run_ocr2(tag, model_dir, sets, workers=None):
    """Run the product engine on every image in the three modes. Images run one after another (as a customer's PC would),
    the engine parallelises over line scales itself. Returns {set: [ {ocr2/auto: text, ..., 'sec': {mode: seconds}} ]}."""
    from matnyab.api import OcrOptions
    eng = make_ocr2_engine(model_dir); out = {}
    for sname, items in sets.items():
        t = time.time(); rows = []
        for name, im, ref, grp in items:
            row = {'sec': {}}; eng.cache = None
            for mode in OCR2_MODES:
                res = eng.recognize(im, OcrOptions(mode=mode, workers=workers))
                row[f'ocr2/{mode}'] = res.text
                row['sec'][mode] = round(res.elapsed_s + (eng.last_recognition_s if eng.cache_hit else 0.0), 3)
                if mode == 'auto': row['auto_picked'] = res.mode_used
            rows.append(row)
        out[sname] = rows
        print(f'[{tag}] ocr2 {sname}: {len(items)} images, {time.time() - t:.0f}s', flush=True)
    eng.close()
    return out

def summarize(sets, outs):
    res = {}
    for sname, items in sets.items():
        for tag, o in outs.items():
            for eng in [e for e in LEGACY_ENGS + OCR2_ENGS if o[sname] and e in o[sname][0]]:
                for view in ('raw', 'nomark'):
                    tot = {}
                    for (name, im, ref, grp), r in zip(items, o[sname]):
                        h = r[eng] if view == 'raw' else MARK.sub('', r[eng])
                        sec = r['sec'][eng.split('/')[1]] if eng.startswith('ocr2/') else None
                        we, wn, le, ln, nl, nr, nh, pl, pr, ph = counts(ref, h)
                        for key in ('all', grp) + (('z100+z75',) if grp in ('z100', 'z75') else ()):
                            d = tot.setdefault(key, [0] * 12); d[11] += sec or 0.0; d[0] += we; d[1] += wn; d[2] += le; d[3] += ln; d[4] += 1
                            d[5] += nl; d[6] += nr; d[7] += nh; d[8] += pl; d[9] += pr; d[10] += ph
                    for key, d in tot.items():
                        res.setdefault(sname, {}).setdefault(key, {})[f'{tag}/{eng}/{view}'] = dict(
                            word_acc=round(100 * (1 - d[0] / max(1, d[1])), 2), letter_acc=round(100 * (1 - d[2] / max(1, d[3])), 2), n_images=d[4], ref_words=d[1],
                            num_f1=f1(d[5], d[6], d[7]), ref_numbers=d[6], punct_f1=f1(d[8], d[9], d[10]), ref_puncts=d[9],
                            sec_per_image=round(d[11] / d[4], 2) if eng.startswith('ocr2/') else None)
    return res

def check_outputs(sets, outs):
    """Flag engines that return (almost) nothing: a sign of segmentation failure on the image, not of OCR quality."""
    W = []
    for sname, items in sets.items():
        for tag, o in outs.items():
            for eng in [e for e in LEGACY_ENGS + OCR2_ENGS if o[sname] and e in o[sname][0]]:
                bad = [it[0] for it, r in zip(items, o[sname]) if len(B.letters(it[2])) > 50 and len(B.letters(r[eng])) < 0.3 * len(B.letters(it[2]))]
                if bad: W.append(f'- {sname} [{tag}/{eng}]: {len(bad)}/{len(items)} images returned < 30% of the reference length, e.g. {", ".join(bad[:4])}')
    return W

def ocr2_table(res):
    """Compact product-engine tables: one per set/group, rows = model x mode, all four metrics + seconds per image.
    Uses the 'raw' view (the ocr2 engine removes citation markers itself); 'nomark' is in eval.json."""
    L = ['\n# Product engine (ocr2): all metrics, raw view\n',
         'word / letter accuracy %, numbers F1 %, punctuation F1 %, mean seconds per image (this machine, all CPU cores, images one at a time).\n']
    f2 = lambda v: '-' if v is None else f'{v:.2f}'
    for sname, groups in res.items():
        for key, rows in groups.items():
            if not any(k.startswith(('base/ocr2', 'ft/ocr2')) for k in rows): continue
            n = next(iter(rows.values()))
            L.append(f'\n## {sname} / {key}  (n={n["n_images"]} images, {n["ref_words"]} ref words)\n')
            L.append('| model | mode | word | letter | numbers F1 | punct F1 | s/image |'); L.append('|---|---|---|---|---|---|---|')
            for tag in ('base', 'ft'):
                for mode in OCR2_MODES:
                    r = rows.get(f'{tag}/ocr2/{mode}/raw')
                    if r: L.append(f'| {tag} | {mode} | {r["word_acc"]:.2f} | {r["letter_acc"]:.2f} | {f2(r["num_f1"])} | {f2(r["punct_f1"])} | {f2(r["sec_per_image"])} |')
    return L

def markdown(res, warnings=()):
    L = ['# Results (micro-averaged accuracy %, word / letter)\n', '`nomark` = citation markers like [۱۱] removed from OCR output before scoring. Strict tables show numbers F1 % / punctuation F1 %.\n']
    for sname, groups in res.items():
        for key, rows in groups.items():
            n = next(iter(rows.values()))
            L.append(f'\n## {sname} / {key}  (n={n["n_images"]} images, {n["ref_words"]} ref words)\n')
            L.append('| engine | base raw | ft raw | base nomark | ft nomark |'); L.append('|---|---|---|---|---|')
            engs = [e for e in LEGACY_ENGS + OCR2_ENGS if f'base/{e}/raw' in rows]
            for eng in engs:
                cell = lambda tag, view: (lambda r: f'{r["word_acc"]:.2f} / {r["letter_acc"]:.2f}')(rows[f'{tag}/{eng}/{view}'])
                L.append(f'| {eng} | {cell("base", "raw")} | {cell("ft", "raw")} | {cell("base", "nomark")} | {cell("ft", "nomark")} |')
            if n.get('ref_numbers') is not None:
                f2 = lambda v: '-' if v is None else f'{v:.2f}'
                L.append(f'\nStrict F1 % (numbers incl. separators, {n["ref_numbers"]} in ref / punctuation marks, {n["ref_puncts"]} in ref):\n')
                L.append('| engine | base raw | ft raw | base nomark | ft nomark |'); L.append('|---|---|---|---|---|')
                for eng in engs:
                    c2 = lambda tag, view: (lambda r: f'{f2(r.get("num_f1"))} / {f2(r.get("punct_f1"))}')(rows[f'{tag}/{eng}/{view}'])
                    L.append(f'| {eng} | {c2("base", "raw")} | {c2("ft", "raw")} | {c2("base", "nomark")} | {c2("ft", "nomark")} |')
    L += ocr2_table(res)
    if warnings: L = L[:2] + ['\n## WARNINGS (check before trusting the tables)\n'] + list(warnings) + [''] + L[2:]
    return '\n'.join(L) + '\n'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base-dir', default=os.path.join(ROOT, 'tess')); ap.add_argument('--ft-file', default=None)
    ap.add_argument('--tests', default='tests'); ap.add_argument('--holdout', default=None); ap.add_argument('--out', default='results')
    ap.add_argument('--limit', type=int, default=0); ap.add_argument('--sets', default='client,real_tune,real_final,synth')
    ap.add_argument('--threads', type=int, default=os.cpu_count() or 1)
    ap.add_argument('--engines', default='legacy,ocr2', help='legacy = pipeline2 (plain,v2raw,v2lex); ocr2 = product engine (auto,raw,lex)')
    a = ap.parse_args(); a.sets = a.sets.split(','); a.engines = a.engines.split(',')
    os.makedirs(a.out, exist_ok=True)
    sets = load_sets(a); print({k: len(v) for k, v in sets.items()}, flush=True)
    models = {'base': (os.path.abspath(a.base_dir), 'fas')}
    if a.ft_file:
        d = os.path.abspath('tess_ft'); os.makedirs(d, exist_ok=True); shutil.copy(a.ft_file, os.path.join(d, 'fas_ft.traineddata'))
        models['ft'] = (d, 'fas_ft')
    outs = {t: {s_: [dict() for _ in items] for s_, items in sets.items()} for t in models}
    if 'legacy' in a.engines:
        for tag, (d, lang) in models.items():
            for s_, rows in run_model(tag, d, lang, sets, a.threads).items():
                for dst, r in zip(outs[tag][s_], rows): dst.update(r)
    if 'ocr2' in a.engines:
        # TesseractEngine loads <model_dir>/fas.traineddata: give each model its own directory with that file name
        for tag, (d, lang) in models.items():
            md = os.path.abspath(f'ocr2_model_{tag}'); os.makedirs(md, exist_ok=True)
            shutil.copy(os.path.join(d, lang + '.traineddata'), os.path.join(md, 'fas.traineddata'))
            for s_, rows in run_ocr2(tag, md, sets).items():
                for dst, r in zip(outs[tag][s_], rows): dst.update(r)
    res = summarize(sets, outs); warns = check_outputs(sets, outs)
    for w in warns: print('WARNING', w, flush=True)
    open(os.path.join(a.out, 'warnings.txt'), 'w', encoding='utf-8').write('\n'.join(warns) + '\n')
    json.dump(res, open(os.path.join(a.out, 'eval.json'), 'w'), ensure_ascii=False, indent=1)
    # raw hypotheses for inspection (client samples + first 10 of each other set)
    dump = {s: [dict(name=it[0], ref=it[2], **{t: outs[t][s][i] for t in outs}) for i, it in enumerate(items[:10] if s == 'synth' else items)] for s, items in sets.items()}
    json.dump(dump, open(os.path.join(a.out, 'hypotheses.json'), 'w'), ensure_ascii=False, indent=1)
    if a.ft_file:
        md = markdown(res, warns); open(os.path.join(a.out, 'eval.md'), 'w', encoding='utf-8').write(md); print(md)

if __name__ == '__main__':
    main()
