#!/usr/bin/env python3
"""Discovery of legally usable real Persian page scans with human-proofread text.

Runs on GitHub Actions (needs network access to *.wikimedia.org, zenodo.org, huggingface.co).
Writes discovery.json and discovery.md into --out. Nothing here downloads page images.
"""
import argparse, collections, json, os, re, sys, time
import requests

UA = {'User-Agent': 'MatnYabDatasetBuilder/0.1 (https://github.com/abbashaji/ocr; research, offline OCR training)'}
S = requests.Session(); S.headers.update(UA)

def get(url, **params):
    for k in range(5):
        try:
            r = S.get(url, params=params, timeout=60)
            if r.status_code == 200:
                return r.json()
            time.sleep(2 * (k + 1))
        except Exception as e:
            time.sleep(2 * (k + 1))
    return {}

WS = 'https://fa.wikisource.org/w/api.php'
COM = 'https://commons.wikimedia.org/w/api.php'

def api(url, **p):
    p.update(format='json', formatversion=2)
    return get(url, **p)

def all_members(cat, ns=None, limit_pages=400):
    out, cont = [], {}
    for _ in range(limit_pages):
        p = dict(action='query', list='categorymembers', cmtitle=cat, cmlimit=500, cmprop='title|ids')
        if ns is not None: p['cmnamespace'] = ns
        p.update(cont)
        d = api(WS, **p)
        out += [m['title'] for m in d.get('query', {}).get('categorymembers', [])]
        if 'continue' not in d: break
        cont = d['continue']
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='discovery'); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    res = {}
    md = ['# Discovery report', '']

    # ---- fa.wikisource statistics and quality categories
    si = api(WS, action='query', meta='siteinfo', siprop='statistics|namespaces|general')
    res['wikisource_stats'] = si.get('query', {}).get('statistics')
    nss = si.get('query', {}).get('namespaces', {})
    res['namespaces'] = {k: v.get('name') for k, v in nss.items() if k in ('250', '252', '104', '106')}
    md += ['## fa.wikisource statistics', '```', json.dumps(res['wikisource_stats'], ensure_ascii=False), json.dumps(res['namespaces'], ensure_ascii=False), '```']
    msgs = api(WS, action='query', meta='allmessages', ammessages='|'.join(f'proofreadpage_quality{i}_category' for i in range(5)))
    cats = {m['name']: m.get('content') for m in msgs.get('query', {}).get('allmessages', [])}
    res['quality_categories'] = cats
    md += ['## quality categories', '```', json.dumps(cats, ensure_ascii=False), '```']

    per_work = collections.defaultdict(lambda: collections.Counter())
    level_counts = {}
    for lvl in (3, 4):
        name = cats.get(f'proofreadpage_quality{lvl}_category')
        if not name: continue
        titles = all_members('Category:' + name, ns=250)
        level_counts[lvl] = len(titles)
        for t in titles:
            m = re.match(r'^[^:]+:(.+)/(\d+)$', t)
            if m: per_work[m.group(1)][lvl] += 1
    res['level_counts'] = level_counts
    md += [f'## pages per quality level (namespace Page:)', '```', json.dumps(level_counts), '```']

    works = []
    for w, c in per_work.items():
        works.append({'file': w, 'lvl3': c[3], 'lvl4': c[4], 'good': c[3] + c[4]})
    works.sort(key=lambda x: -x['good'])
    res['works_total'] = len(works)

    # ---- Commons licence for the top works
    top = works[:80]
    for i in range(0, len(top), 20):
        chunk = top[i:i + 20]
        d = api(COM, action='query', titles='|'.join('File:' + w['file'] for w in chunk), prop='imageinfo|categories',
                iiprop='extmetadata|size|mime|url', iimetadataversion='latest', cllimit='max')
        by = {}
        for pg in d.get('query', {}).get('pages', []):
            by[pg.get('title', '').replace('File:', '', 1)] = pg
        for w in chunk:
            pg = by.get(w['file'].replace('_', ' '), by.get(w['file'], {}))
            ii = (pg.get('imageinfo') or [{}])[0]
            em = ii.get('extmetadata', {})
            w['commons_missing'] = bool(pg.get('missing')) or not ii
            w['license'] = (em.get('LicenseShortName') or {}).get('value')
            w['license_url'] = (em.get('LicenseUrl') or {}).get('value')
            w['artist'] = re.sub('<[^>]+>', '', (em.get('Artist') or {}).get('value', ''))[:80]
            w['date'] = re.sub('<[^>]+>', '', (em.get('DateTimeOriginal') or {}).get('value', ''))[:60]
            w['pages_total'] = ii.get('pagecount') or None
            w['mime'] = ii.get('mime'); w['url'] = ii.get('url'); w['size'] = ii.get('size')
            w['categories'] = [c['title'] for c in pg.get('categories', [])][:8]
        time.sleep(0.5)
    res['top_works'] = top
    md += ['## top works by proofread/validated pages', '', '| file | L3 | L4 | licence | pages | mime | date | artist |', '|---|---|---|---|---|---|---|---|']
    for w in top[:60]:
        md.append(f"| {w['file'][:60]} | {w['lvl3']} | {w['lvl4']} | {w.get('license')} | {w.get('pages_total')} | {w.get('mime')} | {w.get('date','')[:20]} | {w.get('artist','')[:30]} |")
    md.append(f"\nWorks with >=1 proofread page: {len(works)}; >=50: {sum(1 for w in works if w['good'] >= 50)}; >=200: {sum(1 for w in works if w['good'] >= 200)}")

    # ---- Zenodo
    zen = []
    for q in ('persian OCR', 'farsi OCR', 'persian text images', 'persian handwritten printed dataset'):
        d = get('https://zenodo.org/api/records', q=q, size=30, type='dataset')
        for h in d.get('hits', {}).get('hits', []):
            md_ = h.get('metadata', {})
            zen.append({'id': h.get('id'), 'title': md_.get('title'), 'license': (md_.get('license') or {}).get('id'),
                        'size': sum(f.get('size', 0) for f in h.get('files', [])), 'url': h.get('links', {}).get('self_html')})
    seen = set(); zen = [z for z in zen if not (z['id'] in seen or seen.add(z['id']))]
    res['zenodo'] = zen
    md += ['', '## Zenodo hits', '']
    md += [f"- {z['id']} | {str(z['title'])[:70]} | {z['license']} | {z['size']//1000000} MB | {z['url']}" for z in zen]

    # ---- Hugging Face datasets
    hf = []
    for q in ('persian ocr', 'farsi ocr', 'persian text image', 'persian scanned', 'persian book'):
        d = get('https://huggingface.co/api/datasets', search=q, limit=60, full='true')
        if isinstance(d, list):
            for x in d:
                hf.append({'id': x.get('id'), 'license': (x.get('cardData') or {}).get('license'), 'downloads': x.get('downloads'),
                           'tags': [t for t in x.get('tags', []) if t.startswith(('size_categories', 'task_categories', 'license', 'modality'))][:6]})
    seen = set(); hf = [h for h in hf if not (h['id'] in seen or seen.add(h['id']))]
    res['huggingface'] = hf
    md += ['', '## Hugging Face hits', '']
    md += [f"- {h['id']} | {h['license']} | dl={h['downloads']} | {','.join(h['tags'])}" for h in hf]

    json.dump(res, open(os.path.join(a.out, 'discovery.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(a.out, 'discovery.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    print('\n'.join(md[:40]))

if __name__ == '__main__':
    main()
