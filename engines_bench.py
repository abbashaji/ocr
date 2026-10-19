#!/usr/bin/env python3
"""Run one OCR engine on (a) the client's samples in samples/ and (b) the synthetic held-out set.
Usage: python engines_bench.py --engine tesseract|easyocr|paddleocr
Writes results_<engine>.json and a Markdown table (also to $GITHUB_STEP_SUMMARY if set)."""
import argparse, os, glob, json, traceback
import numpy as np
from PIL import Image
import bench as B, bench2 as B2

def join_rtl(items):
    """items: [(box, text)] -> one string, lines top-to-bottom, words right-to-left."""
    rows = []
    for box, text in items:
        pts = np.array(box, dtype=float).reshape(-1, 2)
        rows.append((pts[:, 0].mean(), pts[:, 1].mean(), np.ptp(pts[:, 1]), text))
    if not rows: return ''
    med_h = float(np.median([r[2] for r in rows])) or 1.0
    rows.sort(key=lambda r: r[1])
    lines, cur = [], [rows[0]]
    for r in rows[1:]:
        if abs(r[1] - np.mean([c[1] for c in cur])) > 0.6 * med_h: lines.append(cur); cur = [r]
        else: cur.append(r)
    lines.append(cur)
    return ' '.join(t[3] for ln in lines for t in sorted(ln, key=lambda r: -r[0]))

def make_engines(name):
    """returns {pipeline_name: callable(PIL.Image)->str}"""
    if name == 'tesseract':
        return {p: (lambda im, p=p: B2.pipeline(p, im)) for p in ['baseline_std', 'best_raw', 'best_2x', 'auto_35']}
    if name == 'easyocr':
        import easyocr
        reader = easyocr.Reader(['fa'], gpu=False)
        def f(im):
            res = reader.readtext(np.array(im.convert('RGB')), detail=1, paragraph=False)
            return join_rtl([(b, t) for b, t, _c in res])
        return {'easyocr_fa': f}
    if name == 'paddleocr':
        from paddleocr import PaddleOCR
        try: ocr = PaddleOCR(lang='fa', use_angle_cls=False, show_log=False)
        except Exception: ocr = PaddleOCR(lang='fa')
        def f(im):
            arr = np.array(im.convert('RGB'))
            try: res = ocr.ocr(arr, cls=False)
            except TypeError: res = ocr.ocr(arr)
            items = []
            first = res[0] if res else None
            if isinstance(first, dict) or hasattr(first, 'get'):          # PaddleOCR 3.x
                for poly, txt in zip(first.get('rec_polys', []), first.get('rec_texts', [])): items.append((poly, txt))
            elif first:                                                    # PaddleOCR 2.x
                for box, (txt, _c) in first: items.append((box, txt))
            return join_rtl(items)
        return {'paddleocr_fa': f}
    raise SystemExit(f'unknown engine {name}')

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--engine', required=True); a = ap.parse_args()
    ref = open('ref.txt', encoding='utf-8').read()
    engines = make_engines(a.engine)
    out = {'engine': a.engine, 'client': {}, 'synthetic_by_size': {}, 'errors': []}
    samples = sorted(glob.glob('samples/*'))
    for name, fn in engines.items():
        for sp in samples:
            try:
                s = B.score(ref, fn(Image.open(sp).convert('L')))
                out['client'].setdefault(name, {})[os.path.basename(sp)] = {k: round(100 * v, 2) for k, v in s.items()}
            except Exception:
                out['errors'].append(f'{name} on {sp}: {traceback.format_exc(limit=2)}')
    items = B2.make_items([4, 5], B.chunks(ref))
    for name, fn in engines.items():
        acc = {}
        for it in items:
            try: s = B.score(it['ref'], fn(it['img']))
            except Exception: out['errors'].append(f'{name} synthetic: {traceback.format_exc(limit=2)}'); break
            acc.setdefault(it['size'], []).append(s)
        out['synthetic_by_size'][name] = {sz: {k: round(100 * np.mean([x[k] for x in v]), 2) for k in ('letter', 'word')} for sz, v in sorted(acc.items())}
    json.dump(out, open(f'results_{a.engine}.json', 'w'), indent=1, ensure_ascii=False)
    md = [f'## Engine: {a.engine}', '', '### Client samples (letter% / word%)', '| pipeline | sample | letter | word |', '|---|---|---|---|']
    for n, d in out['client'].items():
        for f, s in d.items(): md.append(f'| {n} | {f} | {s["letter"]} | {s["word"]} |')
    md += ['', '### Synthetic held-out by font size (letter% / word%)', '| pipeline | ' + ' | '.join(f'{s}px' for s in B2.SIZES) + ' |', '|---|' + '---|' * len(B2.SIZES)]
    for n, d in out['synthetic_by_size'].items():
        md.append(f'| {n} | ' + ' | '.join(f'{d[s]["letter"]} / {d[s]["word"]}' if s in d else 'n/a' for s in B2.SIZES) + ' |')
    if out['errors']: md += ['', '### Errors', '```'] + out['errors'][:5] + ['```']
    text = '\n'.join(md); print(text)
    if os.environ.get('GITHUB_STEP_SUMMARY'): open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8').write(text + '\n')

if __name__ == '__main__': main()
