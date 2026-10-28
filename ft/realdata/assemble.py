#!/usr/bin/env python3
"""Assemble per-work parts into the final dataset: dedupe, leakage filter, splits by work, manifest, exports, QA, docs."""
import argparse, collections, datetime, glob, html, json, os, random, re, shutil, sys, base64, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from PIL import Image, ImageDraw, ImageFont
import export, textclean
from textclean import cmp_form

ROLE_PRIORITY = {'final': 0, 'tune': 1, 'train': 2}
KEEP_TIERS = ('GOLD', 'GOLD_A', 'SILVER')

def shingles(text, n=5):
    toks = [cmp_form(t) for t in text.split()]; toks = [t for t in toks if t]
    return {' '.join(toks[i:i + n]) for i in range(len(toks) - n + 1)}

def load_parts(parts_dir, works):
    byid = {w['id']: w for w in works}
    recs, wstats = [], {}
    for d in sorted(glob.glob(os.path.join(parts_dir, '*'))):
        sp = os.path.join(d, 'stats.json')
        if not os.path.exists(sp): continue
        st = json.load(open(sp, encoding='utf-8')); wid = st['work']; wstats[wid] = st
        if st.get('skipped') or not os.path.exists(os.path.join(d, 'lines.jsonl')): continue
        c = st['commons']; wk = byid[wid]
        for ln in open(os.path.join(d, 'lines.jsonl'), encoding='utf-8'):
            r = json.loads(ln)
            if r['tier'] not in KEEP_TIERS: continue
            r.update(split=wk['role'], licence=c['license'], commons_url=c['page_url'], retrieved=st['started'][:10], _dir=d,
                     wikisource_url='https://fa.wikisource.org/w/index.php?title=' + urllib.parse.quote(r['page_title'].replace(' ', '_')) + f"&oldid={r['revid']}")
            recs.append(r)
    return recs, wstats

def filter_records(recs, leak_blob, drop_log):
    # 1. cross-work duplicates: keep the copy in the most protected role (final > tune > train)
    best = {}
    for r in recs:
        k = cmp_form(r['label']); r['_k'] = k
        if k not in best or ROLE_PRIORITY[r['split']] < ROLE_PRIORITY[best[k]['split']]: best[k] = r
    out = []
    for r in recs:
        if best[r['_k']] is not r: drop_log['duplicate_across_works'] += 1; continue
        out.append(r)
    # 2. leakage against evaluation text (substring on comparison form; 5-word shingles)
    lblob = cmp_form(leak_blob); lsh = shingles(leak_blob)
    keep = []
    for r in out:
        k = r['_k']
        if len(k) >= 20 and k in lblob: drop_log['leak_eval_substring'] += 1; continue
        if shingles(r['label']) & lsh: drop_log['leak_eval_shingle'] += 1; continue
        keep.append(r)
    # 3. train/tune lines that share a 5-word shingle with the final benchmark labels
    fsh = set()
    for r in keep:
        if r['split'] == 'final': fsh |= shingles(r['label'])
    keep2 = []
    for r in keep:
        if r['split'] != 'final' and shingles(r['label']) & fsh: drop_log['leak_train_vs_final'] += 1; continue
        keep2.append(r)
    return keep2

def contact_sheet(rows, images_dir, out_html, out_pngs, n=100, seed=7):
    rng = random.Random(seed); pool = [r for r in rows if r['tier'] in ('GOLD', 'GOLD_A')]
    pick = rng.sample(pool, min(n, len(pool)))
    parts = ['<!doctype html><meta charset="utf-8"><title>Contact sheet</title><body style="font-family:Vazirmatn,Tahoma,sans-serif;max-width:1300px;margin:auto">',
             f'<h2>100 random GOLD lines ({len(pick)} shown)</h2><p>Each block: line image, then the stored label (full fidelity). Report any mismatch.</p>']
    for i, r in enumerate(pick, 1):
        b = base64.b64encode(open(os.path.join(images_dir, r['id'] + '.png'), 'rb').read()).decode()
        parts.append(f'<div style="border-bottom:1px solid #ccc;padding:6px 0"><small>#{i} {r["id"]} {r["tier"]} sim={r["sim"]}</small><br><img style="max-width:100%" src="data:image/png;base64,{b}"><div dir="rtl" style="font-size:22px">{html.escape(r["label_full"])}</div></div>')
    open(out_html, 'w', encoding='utf-8').write('\n'.join(parts))
    font = next((p for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',) if os.path.exists(p)), None)
    for s in range(0, len(pick), 20):
        chunk = pick[s:s + 20]; ims = [Image.open(os.path.join(images_dir, r['id'] + '.png')).convert('L') for r in chunk]
        W = max(i.width for i in ims); H = sum(i.height + 46 for i in ims)
        sheet = Image.new('L', (W, H), 255); d = ImageDraw.Draw(sheet); y = 0
        f = ImageFont.truetype(font, 24, layout_engine=ImageFont.Layout.RAQM) if font else None
        for r, im in zip(chunk, ims):
            sheet.paste(im, (0, y)); y += im.height
            if f: d.text((W - 4, y + 2), r['label_full'], font=f, fill=0, direction='rtl', language='fa', anchor='ra')
            d.line([(0, y + 44), (W, y + 44)], fill=160); y += 46
        sheet.save(f'{out_pngs}_{s // 20 + 1}.png', optimize=True)

def attribution(works, wstats, counts):
    L = ['# Attribution and licences', '',
         'Page images come from Wikimedia Commons scans; the transcriptions are Persian Wikisource (fa.wikisource.org) proofread text',
         '(quality level 3 "proofread" or 4 "validated"; text licence CC BY-SA 4.0, contributors listed in each page history).',
         'Each underlying work carries the Commons licence shown below at retrieval time. Rows marked `skipped` were not used.', '',
         '| id | split | work (Commons file) | author | date | Commons licence | lines used | Commons page |', '|---|---|---|---|---|---|---|---|']
    for w in works:
        st = wstats.get(w['id'])
        if not st: L.append(f"| {w['id']} | {w['role']} | {w['file']} | | | not processed | 0 | |"); continue
        c = st['commons']; n = counts.get(w['id'], 0)
        lic = c['license'] + (' (skipped)' if st.get('skipped') else '')
        L.append(f"| {w['id']} | {w['role']} | {w['file']} | {c.get('artist','')} | {c.get('date','')} | {lic} | {n} | {c.get('page_url','')} |")
    L += ['', 'Redistribution: public-domain works carry no conditions; CC BY / CC BY-SA works require attribution (this file + `manifest`',
          'URLs) and, for CC BY-SA, share-alike for adaptations of the text/images. Derived MODELS are not adaptations of the images under',
          'the usual reading, but the owner should have this confirmed by counsel before shipping (see HANDOFF risks).']
    return '\n'.join(L) + '\n'


def readme(stats, works):
    bs = stats['by_split_tier']
    rows = '\n'.join(f'| {k} | {v} |' for k, v in bs.items())
    return f"""# Persian real-scan line dataset (fa.wikisource + Wikimedia Commons)

Real scanned Persian book/periodical pages with human-proofread text. Lines were cut with the product segmenter
(`matnyab.engine.segment`), the label of each line is the human text found by monotone edit-distance alignment against the
page text (never OCR output). Built {stats['built'][:10]}; rebuild: GitHub Actions -> `build-real-dataset` -> stage `build`.

## Counts (after dedupe and leakage filtering)
| split/tier | lines |
|---|---|
{rows}

Total lines: {stats['n_lines']}. Splits are by WORK: train / tune / final (final = held-out real-scan benchmark).
Tiers: GOLD = unambiguous alignment, similarity >= {0.93}; GOLD_A = anchored between two GOLD neighbours; SILVER = weaker alignment
(0.80-0.93) - train on GOLD/GOLD_A first. Dropped lines and reasons: see `stats.json` (`drops`, `line_reasons_total`).

## Layout
- `lines/<id>.png`   grey line images, height <= 64 px, horizontally trimmed (id = work_pPAGE_lLINE)
- `manifest.jsonl` / `manifest.csv`   id, work, split, tier, sim, margin, page, revid, page_title, licence, commons_url, wikisource_url,
  label_full (FULL FIDELITY: ezafe, ZWNJ, original digits/punctuation), label_folded, label_distinct, w, h, y0, y1, deskew, dpi, quality
- `export/tesseract_{{folded,distinct}}_{{gold,silver}}/<split>/<id>.png + <id>.gt.txt`
- `export/tesseract_{{folded,distinct}}_gold_train_aug1/train/` train lines + one seeded augmented copy (`*_aug1.png`)
- `export/paddle_{{folded,distinct}}_{{gold,silver}}/{{train,tune,final}}.txt` (`images/<id>.png<TAB>label`), `images/`, `dict.txt`
- `benchmark_pages/` text-block crops (jpg) + full human page text (txt) of the final works
- `ATTRIBUTION.md`, `stats.json`, `contact_sheet.html` (100 random GOLD lines, RTL)

## Presets (applied only when exporting; the manifest keeps full fidelity)
- folded  = `ft/common.py` clean_text + LABEL_MAP (ezafe and harakat dropped, ، ٬ -> ",", ٫ -> ".", ٪ and % -> "#", ; -> ؛, dashes -> "-").
  With `--unicharset` lines containing characters outside the model's unicharset are dropped (as in make_train_data.py).
- distinct = same normalisation of ya/kaf/digits/spaces/quotes, but KEEPS the ezafe mark U+0654 and ، ٫ ٬ ٪.

## Re-export with other settings
`python ft/realdata/export.py` is a library: `select(records, splits, tiers, preset)` + `write_tesseract` / `write_paddle`
(augmentation: `write_tesseract(..., augment=N, seed=S)`, train split only). See `ft/realdata/test_assemble.py` for usage.
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--parts', required=True); ap.add_argument('--works', default=os.path.join(HERE, 'works.json'))
    ap.add_argument('--leak', required=True, help='text file with evaluation texts'); ap.add_argument('--out', required=True)
    ap.add_argument('--unicharset', default=None); ap.add_argument('--augment', type=int, default=1)
    a = ap.parse_args()
    works = json.load(open(a.works, encoding='utf-8'))['works']
    recs, wstats = load_parts(a.parts, works)
    drop = collections.Counter(); drop['loaded'] = len(recs)
    leak_blob = open(a.leak, encoding='utf-8').read()
    recs = filter_records(recs, leak_blob, drop)
    os.makedirs(a.out, exist_ok=True); img_dir = os.path.join(a.out, 'lines'); os.makedirs(img_dir, exist_ok=True)
    for r in recs: shutil.copyfile(os.path.join(r['_dir'], 'lines', r['id'] + '.png'), os.path.join(img_dir, r['id'] + '.png'))
    rows = export.write_manifest(recs, os.path.join(a.out, 'manifest.jsonl'), os.path.join(a.out, 'manifest.csv'))
    # exports (GOLD + GOLD_A; SILVER separately, train only)
    allowed = None
    if a.unicharset and os.path.exists(a.unicharset):
        import common; allowed = common.load_unicharset(a.unicharset)
    for preset in export.PRESETS:
        for tiers, tag in ((('GOLD', 'GOLD_A'), 'gold'), (('SILVER',), 'silver')):
            sp = ('train', 'tune', 'final') if tag == 'gold' else ('train',)
            items = export.select(recs, splits=sp, tiers=tiers, preset=preset, allowed=allowed)
            if not items: continue
            export.write_tesseract(items, img_dir, os.path.join(a.out, 'export', f'tesseract_{preset}_{tag}'), augment=0)
            export.write_paddle(items, img_dir, os.path.join(a.out, 'export', f'paddle_{preset}_{tag}'))
        if a.augment:
            items = export.select(recs, splits=('train',), tiers=('GOLD', 'GOLD_A'), preset=preset, allowed=allowed)
            export.write_tesseract(items, img_dir, os.path.join(a.out, 'export', f'tesseract_{preset}_gold_train_aug{a.augment}'), augment=a.augment, seed=20261028)
    # counts + stats
    cnt = collections.Counter((r['split'], r['tier']) for r in recs)
    per_work = collections.Counter(r['work'] for r in recs)
    stats = dict(built=datetime.datetime.now(datetime.timezone.utc).isoformat(), n_lines=len(recs), drops=dict(drop),
                 by_split_tier={f'{s}/{t}': n for (s, t), n in sorted(cnt.items())}, by_work=dict(per_work),
                 chars={s: sum(len(r['label']) for r in recs if r['split'] == s) for s in ('train', 'tune', 'final')},
                 line_reasons_total=dict(sum((collections.Counter(st.get('line_reasons', {})) for st in wstats.values()), collections.Counter())),
                 works={w: dict(commons_license=st['commons']['license'], skipped=st.get('skipped'), proofread_pages_total=st.get('proofread_pages_total'),
                                pages_sampled=st.get('pages_sampled'), counts=st.get('counts')) for w, st in wstats.items()})
    json.dump(stats, open(os.path.join(a.out, 'stats.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(a.out, 'ATTRIBUTION.md'), 'w', encoding='utf-8').write(attribution(works, wstats, per_work))
    open(os.path.join(a.out, 'README.md'), 'w', encoding='utf-8').write(readme(stats, works))
    contact_sheet(rows, img_dir, os.path.join(a.out, 'contact_sheet.html'), os.path.join(a.out, 'contact_sheet'))
    # benchmark pages are copied as they are
    bp = os.path.join(a.out, 'benchmark_pages'); os.makedirs(bp, exist_ok=True)
    for d in sorted(glob.glob(os.path.join(a.parts, '*', 'pages'))):
        for f in os.listdir(d): shutil.copyfile(os.path.join(d, f), os.path.join(bp, f))
    print(json.dumps(dict(n_lines=len(recs), by_split_tier=stats['by_split_tier'], drops=stats['drops']), ensure_ascii=False))

if __name__ == '__main__':
    main()
