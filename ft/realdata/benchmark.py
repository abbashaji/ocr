#!/usr/bin/env python3
"""Real-scan benchmark of the PRODUCT engine (ocr2 TesseractEngine, modes raw/lex/auto) on the held-out 'final' works.

  benchmark.py run    --work w20 --dataset DS --model-dir DIR --out bench_w20 [--max-pages 40 --max-lines 300]
  benchmark.py report --dirs bench_w20 bench_w21 ... --out report

Metrics come from ocr/ft/evaluate.py (counts/summarize: word, letter, numbers F1, punctuation F1) - nothing re-implemented.
Two sets: 'pages' = text-block crop of a scanned page vs the full human page text (block = first to last GOLD line, so running
heads/footnotes outside it are not scored; selection uses the shipped model's own alignment, a mild bias) and 'lines' = GOLD
lines vs their label (biased upwards: lines were chosen because the shipped model read them well enough to be aligned).
"""
import argparse, glob, json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); FT = os.path.dirname(HERE); ROOT = os.path.dirname(FT)
sys.path.insert(0, ROOT); sys.path.insert(0, FT)

def run(a):
    import evaluate as E
    from PIL import Image
    rng = random.Random(20261028 + sum(map(ord, a.work)))
    pages = sorted(glob.glob(os.path.join(a.dataset, 'benchmark_pages', f'{a.work}_p*.jpg')))
    if len(pages) > a.max_pages: pages = sorted(rng.sample(pages, a.max_pages))
    items_p = [(os.path.basename(p)[:-4], Image.open(p).convert('RGB'), open(p[:-4] + '.txt', encoding='utf-8').read(), a.work) for p in pages]
    rows = [json.loads(l) for l in open(os.path.join(a.dataset, 'manifest.jsonl'), encoding='utf-8')]
    rows = [r for r in rows if r['work'] == a.work and r['split'] == 'final' and r['tier'] in ('GOLD', 'GOLD_A')]
    if len(rows) > a.max_lines: rows = rng.sample(rows, a.max_lines)
    items_l = [(r['id'], Image.open(os.path.join(a.dataset, 'lines', r['id'] + '.png')).convert('RGB'), r['label_full'], a.work) for r in rows]
    sets = {'pages': items_p, 'lines': items_l}
    outs = E.run_ocr2('real', a.model_dir, sets)
    os.makedirs(a.out, exist_ok=True)
    json.dump(dict(work=a.work, meta={s: [(n, ref, g) for n, _, ref, g in it] for s, it in sets.items()}, outs=outs),
              open(os.path.join(a.out, 'outs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print({s: len(it) for s, it in sets.items()})

def report(a):
    import evaluate as E
    sets, outs = {'pages': [], 'lines': []}, {'ocr2': {'pages': [], 'lines': []}}
    for d in a.dirs:
        f = os.path.join(d, 'outs.json')
        if not os.path.exists(f): continue
        j = json.load(open(f, encoding='utf-8'))
        for s in sets:
            sets[s] += [(n, None, ref, g) for n, ref, g in j['meta'][s]]
            outs['ocr2'][s] += j['outs'][s]
    res = E.summarize(sets, outs)
    warns = E.check_outputs(sets, outs)
    os.makedirs(a.out, exist_ok=True)
    json.dump(dict(results=res, warnings=warns), open(os.path.join(a.out, 'benchmark.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    L = ['# Real-scan benchmark of the shipped model (ocr2 engine)', '',
         'Held-out works only (split by work). View = raw output (no citation-marker removal). word/letter = accuracy %; num/punct = F1 %.', '']
    for s in ('pages', 'lines'):
        if s not in res: continue
        L += [f'## set `{s}`', '', '| group | mode | images | ref words | word | letter | num F1 | punct F1 | s/img |', '|---|---|---|---|---|---|---|---|---|']
        for grp in sorted(res[s], key=lambda g: (g != 'all', g)):
            for mode in ('raw', 'lex', 'auto'):
                m = res[s][grp].get(f'ocr2/ocr2/{mode}/raw')
                if m: L.append(f"| {grp} | {mode} | {m['n_images']} | {m['ref_words']} | {m['word_acc']} | {m['letter_acc']} | {m['num_f1']} | {m['punct_f1']} | {m['sec_per_image'] if s == 'pages' else '-'} |")
        L.append('')
    if warns: L += ['## warnings', ''] + warns + ['']
    open(os.path.join(a.out, 'benchmark.md'), 'w', encoding='utf-8').write('\n'.join(L))
    print('\n'.join(L[:60]))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('run'); r.add_argument('--work', required=True); r.add_argument('--dataset', required=True); r.add_argument('--model-dir', required=True)
    r.add_argument('--out', required=True); r.add_argument('--max-pages', type=int, default=40); r.add_argument('--max-lines', type=int, default=300)
    p = sub.add_parser('report'); p.add_argument('--dirs', nargs='+', required=True); p.add_argument('--out', required=True)
    a = ap.parse_args(); (run if a.cmd == 'run' else report)(a)
