#!/usr/bin/env python3
"""Process ONE work (a Commons PDF with proofread fa.wikisource pages) into labelled line images.

  python ft/realdata/build_work.py --work w01 --config ft/realdata/works.json --tessdata DIR --out parts/w01

Steps: verify licence -> choose pages -> fetch human text -> render pages -> segment (product segmenter) -> OCR each line
(shipped model) -> align to the human text -> filter -> write lines/*.png, lines.jsonl, pages/ (benchmark works), stats.json.
"""
import argparse, collections, hashlib, json, os, random, re, subprocess, sys, time, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from PIL import Image
import numpy as np
import align, textclean, pageimg

PERSIAN_LETTER = re.compile('[\u0600-\u06ff\u0750-\u077f\ufb50-\ufdff\ufe70-\ufeff]')
LATIN = re.compile('[A-Za-z]')

def script_ok(label, min_frac=0.9):
    p, l = len(PERSIAN_LETTER.findall(label)), len(LATIN.findall(label))
    return p > 0 and p / max(1, p + l) >= min_frac

def process_page(img, gt, tessdata, workers=4, min_aspect=2.5, max_aspect=90):
    """img: PIL image; gt: full-fidelity page text. -> (records, page_info). Pure function (no network)."""
    gray, lines, info = pageimg.page_lines(img)
    if not lines: return [], dict(info, n_lines=0)
    texts = pageimg.ocr_crops([l['crop'] for l in lines], tessdata, workers)
    for l, t in zip(lines, texts): l['text'] = t
    res = align.align_page(lines, gt)
    recs = []
    for k, (l, r) in enumerate(zip(lines, res)):
        trimmed = pageimg.trim_horizontal(l['crop'])
        rec = dict(idx=k, y0=l['band'][0], y1=l['band'][1], ocr=l['text'], label=r['label'], sim=r['sim'], margin=r['margin'],
                   tier=r['tier'], reason=r['reason'], flags=[])
        if trimmed is None: rec.update(tier=None, reason='blank'); recs.append((rec, None)); continue
        ar = trimmed.width / trimmed.height
        if rec['tier']:
            if not (min_aspect <= ar <= max_aspect): rec.update(tier=None, reason='aspect')
            elif not script_ok(rec['label']): rec.update(tier=None, reason='non_persian')
        rec['w'], rec['h'] = trimmed.size
        recs.append((rec, trimmed))
    info = dict(info, n_lines=len(lines))
    return recs, info

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True); ap.add_argument('--config', default=os.path.join(HERE, 'works.json'))
    ap.add_argument('--tessdata', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--max-pages', type=int, default=None); ap.add_argument('--dpi', type=int, default=None)
    ap.add_argument('--workers', type=int, default=4); ap.add_argument('--seed', type=int, default=20261027)
    ap.add_argument('--debug-wikitext', type=int, default=0); ap.add_argument('--max-h', type=int, default=64)
    a = ap.parse_args()
    import wiki
    cfg = json.load(open(a.config, encoding='utf-8'))
    w = next(x for x in cfg['works'] if x['id'] == a.work)
    max_pages = a.max_pages or w.get('max_pages', 300); dpi = a.dpi or w.get('dpi', 200)
    os.makedirs(os.path.join(a.out, 'lines'), exist_ok=True)
    stats = dict(work=w['id'], file=w['file'], role=w['role'], started=datetime.datetime.now(datetime.timezone.utc).isoformat())

    info = wiki.commons_info(w['file']); stats['commons'] = info
    if info['missing'] or not wiki.license_ok(info['license']):
        stats['skipped'] = f"licence not accepted: {info['license']!r} missing={info['missing']}"
        json.dump(stats, open(os.path.join(a.out, 'stats.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('SKIP', stats['skipped']); return 0

    pages = {}
    for attempt in range(4):                      # the category listing failed once for a whole work (transient API error)
        cats = wiki.quality_categories() if attempt == 0 or not cats else cats
        pages = {}
        for lvl, cat in cats.items():
            for t in wiki.category_pages(cat):
                m = re.match(r'^[^:]+:(.+)/(\d+)$', t)
                if m and m.group(1).replace('_', ' ') == w['file'].replace('_', ' '): pages[int(m.group(2))] = (t, lvl)
        if pages: break
        time.sleep(15)
    if not pages:
        stats['error'] = 'no proofread pages found after 4 attempts'
        json.dump(stats, open(os.path.join(a.out, 'stats.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        raise SystemExit('no proofread pages found for ' + w['file'])
    nums = sorted(pages)
    stats['proofread_pages_total'] = len(nums)
    skip = w.get('skip_edges', 4)
    pool = [n for n in nums if n > skip]
    rng = random.Random(a.seed + sum(map(ord, w['id'])))
    if len(pool) > max_pages:
        step = len(pool) / max_pages
        pool = [pool[int(i * step + rng.random() * step * 0.999)] for i in range(max_pages)]
    stats['pages_sampled'] = len(pool)

    texts = wiki.fetch_wikitext([pages[n][0] for n in pool])
    for _ in range(2):                           # second chance for anything still missing
        miss = [pages[n][0] for n in pool if pages[n][0] not in texts]
        if not miss: break
        texts.update(wiki.fetch_wikitext(miss, batch=5))
    stats['wikitext_missing'] = sum(1 for n in pool if pages[n][0] not in texts)
    if a.debug_wikitext:
        for n in pool[:a.debug_wikitext]:
            t = pages[n][0]
            print('--- WIKITEXT', t, '\n', (texts.get(t, (0, ''))[1])[:700], '\n--- BODY\n', textclean.body_of(texts.get(t, (0, ''))[1])[0][:300])

    pdf = os.path.join(a.out, 'work.pdf')
    t0 = time.time()
    if not wiki.download(info['url'], pdf): raise SystemExit('download failed')
    stats['pdf_mb'] = round(os.path.getsize(pdf) / 1e6, 1); stats['download_s'] = round(time.time() - t0)

    jl = open(os.path.join(a.out, 'lines.jsonl'), 'w', encoding='utf-8')
    if w['role'] == 'final': os.makedirs(os.path.join(a.out, 'pages'), exist_ok=True)
    cnt = collections.Counter(); reasons = collections.Counter(); seen_labels = set(); n_pages_done = 0
    for n in pool:
        title = pages[n][0]
        if title not in texts: cnt['page_no_text'] += 1; continue
        revid, wt = texts[title]
        gt, level, flags = textclean.body_of(wt)
        if 'complex_layout' in flags or 'markup_left' in flags or len(gt) < 80:
            cnt['page_skipped_' + ('complex' if 'complex_layout' in flags else 'markup' if 'markup_left' in flags else 'short')] += 1; continue
        png = os.path.join(a.out, f'p{n}')
        r = subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(n), '-l', str(n), '-gray', '-png', pdf, png], capture_output=True)
        outs = [f for f in os.listdir(a.out) if f.startswith(f'p{n}-') and f.endswith('.png')]
        if r.returncode or not outs: cnt['render_failed'] += 1; continue
        pth = os.path.join(a.out, outs[0]); img = Image.open(pth).convert('L')
        recs, pinfo = process_page(img, gt, a.tessdata, a.workers)
        n_pages_done += 1; cnt['pages'] += 1
        if 'border_crop' in pinfo: cnt['pages_border_cropped'] += 1
        if a.debug_wikitext and n_pages_done == 1:   # visual debugging in probe runs: page thumbnail + first crops
            th = img.copy(); th.thumbnail((900, 1300)); th.convert('L').save(os.path.join(a.out, 'debug_page.jpg'), quality=80)
            print('PAGE', img.size, 'lines', pinfo.get('n_lines'), 'deskew', pinfo.get('deskew'), 'border_crop', pinfo.get('border_crop'), [(r['y0'], r['y1'], r['ocr'][:30]) for r, _ in recs[:6]])
            for j, (r, c) in enumerate(recs[:4]):
                if c is not None: c.save(os.path.join(a.out, f'debug_crop{j}.png'))
        keep = 0
        for rec, crop in recs:
            reasons[rec['reason'] or 'ok'] += 1
            if rec['tier'] and crop is not None:
                key = textclean.cmp_form(rec['label'])
                if key in seen_labels: rec.update(tier=None, reason='duplicate'); continue
                seen_labels.add(key)
                lid = f"{w['id']}_p{n:04d}_l{rec['idx']:02d}"
                if crop.height > a.max_h:                      # store at <= max_h px height (Tesseract/Paddle rescale anyway)
                    crop = crop.resize((max(1, round(crop.width * a.max_h / crop.height)), a.max_h), Image.LANCZOS)
                rec['w'], rec['h'] = crop.size
                crop.save(os.path.join(a.out, 'lines', lid + '.png'), optimize=True)
                rec.update(id=lid, work=w['id'], page=n, revid=revid, page_title=title, quality=level, role=w['role'],
                           deskew=pinfo['deskew'], dpi=dpi, page_w=pinfo['size'][0], page_h=pinfo['size'][1])
                jl.write(json.dumps(rec, ensure_ascii=False) + '\n'); keep += 1; cnt['tier_' + rec['tier']] += 1
        if w['role'] == 'final':
            gold = [rec for rec, c in recs if rec['tier'] in ('GOLD', 'GOLD_A')]
            if len(gold) >= 8:
                y0, y1 = min(g['y0'] for g in gold), max(g['y1'] for g in gold)
                bx0, by0, bx1, _ = pinfo.get('border_crop') or (0, 0, img.width, img.height)   # bands are relative to the border-cropped page
                blk = img.crop((bx0, max(0, by0 + y0 - 6), bx1, min(img.height, by0 + y1 + 6)))
                bid = f"{w['id']}_p{n:04d}"
                blk.save(os.path.join(a.out, 'pages', bid + '.jpg'), quality=92)
                open(os.path.join(a.out, 'pages', bid + '.txt'), 'w', encoding='utf-8').write(gt)
                json.dump(dict(id=bid, page=n, revid=revid, title=title, n_gold=len(gold), n_lines=len(recs), gt_chars=len(gt)),
                          open(os.path.join(a.out, 'pages', bid + '.json'), 'w'))
                cnt['bench_pages'] += 1
        os.remove(pth)
        if n_pages_done % 25 == 0: print(f'[{w["id"]}] {n_pages_done}/{len(pool)} pages, {cnt["tier_GOLD"]} GOLD lines', flush=True)
    jl.close(); os.remove(pdf)
    stats.update(counts=dict(cnt), line_reasons=dict(reasons), finished=datetime.datetime.now(datetime.timezone.utc).isoformat())
    json.dump(stats, open(os.path.join(a.out, 'stats.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(stats['counts'], ensure_ascii=False)); return 0

if __name__ == '__main__':
    sys.exit(main())
