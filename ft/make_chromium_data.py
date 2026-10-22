#!/usr/bin/env python3
"""Training lines cut from real Chromium renderings of Wikipedia-style pages, with exact labels from the DOM.

Why: the first full fine-tune used Pillow-rendered lines. The base model had 18.7% character error on them but only ~0.4%
on real screenshots, so the gain did not transfer. Real pages differ in anti-aliasing, hinting, link colours, bold words,
raised citation markers and zoom. Here each paragraph is rendered by Chromium (same machinery as make_tests.py), every
visual line is cut out and labelled with the text the browser shows for that line (U+200C kept, citation markers like
[۱۲] kept because they are in the image; pipeline2/markers.py removes them after OCR).

usage:
  make_chromium_data.py --out data --unicharset base.lstm-unicharset --corpus corpus.txt --exclude ft/articles.txt \
        --n-train 18000 --n-eval 800 --max-minutes 40 [--source api|files] [--files-dir DIR]
  Writes data/train/chr_*.lstmf, data/eval/chr_*.lstmf and appends them to data/list.train / data/list.eval.

Leakage guards: pinned test articles and «ایران» are never visited; any paragraph that matches a corpus holdout paragraph
(letters/digits only, so markers and spacing do not matter) is skipped; train/eval split is by paragraph hash as in make_train_data.
"""
import argparse, hashlib, io, json, os, random, re, sys, time, urllib.parse
from multiprocessing import Pool
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import make_train_data as T
import make_tests as MT

# Per-article font override (50% of articles keep the page's default font = what the test screenshots use). Windows screenshots of the
# client use other fonts than this Linux runner, so the model must not overfit the runner's default Persian font.
FONTS = ['Vazirmatn', 'Noto Naskh Arabic', 'Noto Sans Arabic', 'Noto Kufi Arabic', 'DejaVu Sans']
def font_css(rng, mix):
    if rng.random() >= mix: return None
    f = rng.choice(FONTS); return f"#mw-content-text, #mw-content-text p, #mw-content-text p * {{font-family: '{f}', sans-serif !important}}"

ZOOMS = [(1.0, 0.35), (0.9, 0.15), (0.75, 0.35), (0.67, 0.15)]       # (device scale factor, probability); 0.5 is unreadable, skipped

# One entry per visual line of paragraph i: its text (DOM order = logical order, includes citation markers) and its box in page px.
JS_LINES = """(i) => {
  const p = (%s)()[i];
  const lh = parseFloat(getComputedStyle(p).lineHeight) || 22;
  const lines = []; let cur = null;
  const walker = document.createTreeWalker(p, NodeFilter.SHOW_TEXT);
  const skip = n => !!(n.parentElement && n.parentElement.closest('style,script,.mw-editsection,.noprint'));
  let node;
  while ((node = walker.nextNode())) {
    if (skip(node)) continue;
    const t = node.textContent;
    for (let k = 0; k < t.length; k++) {
      const rg = document.createRange(); rg.setStart(node, k); rg.setEnd(node, k + 1);
      const rs = [...rg.getClientRects()].filter(r => r.height > 0);
      if (!rs.length) { if (cur) cur.text += t[k]; continue; }          // collapsed whitespace / zero-size char
      const r = rs[0], cy = (r.top + r.bottom) / 2;
      if (!cur || cy - cur.cy > 0.7 * lh) { cur = {text: '', cy, l: 1e9, r: -1e9, t: 1e9, b: -1e9}; lines.push(cur); }
      cur.text += t[k];
      if (!/\\s/.test(t[k]) && r.width > 0) {
        cur.l = Math.min(cur.l, r.left + scrollX); cur.r = Math.max(cur.r, r.right + scrollX);
        cur.t = Math.min(cur.t, r.top + scrollY);  cur.b = Math.max(cur.b, r.bottom + scrollY);
      }
    }
  }
  return lines.filter(l => l.r > l.l && l.b > l.t).map(l => ({text: l.text, l: l.l, r: l.r, t: l.t, b: l.b}));
}""" % MT.JS_PARAS

def key_of(s):
    """letters + digits only, so citation markers, spacing and punctuation differences do not matter"""
    return hashlib.md5(re.sub(r'[^0-9A-Za-z؀-ۿ]', '', C.MARKER.sub('', C.clean_text(s))).encode()).hexdigest()

def load_holdout_keys(corpus):
    keys = set()
    if corpus and os.path.exists(corpus):
        for l in open(corpus, encoding='utf-8'):
            l = C.clean_text(l)
            if l and T.split_of(l) == 'holdout': keys.add(key_of(l))
    return keys

def drop_edge_fragments(im, thr=170):
    """White out ink bands that touch the top/bottom edge, are separated from the main text band by blank rows and are small:
    they belong to the neighbouring line (descenders/ascenders), not to the label. Raised markers overlap the text rows, so they stay."""
    import numpy as np
    a = np.asarray(im.convert('L')); ink = (a < thr).sum(1)
    bands, i, n = [], 0, len(ink)
    while i < n:
        if ink[i] > 0:
            j = i
            while j < n and ink[j] > 0: j += 1
            bands.append((i, j, int(ink[i:j].sum()))); i = j
        else: i += 1
    if len(bands) < 2: return im
    main = max(bands, key=lambda b: b[2])
    out = im.convert('RGB'); arr = np.asarray(out).copy()
    for b in bands:
        if b is not main and (b[0] == 0 or b[1] == n) and b[2] < 0.3 * main[2]: arr[b[0]:b[1]] = 255
    return Image.fromarray(arr)

def pick_zoom(rng):
    r, acc = rng.random(), 0.0
    for z, pr in ZOOMS:
        acc += pr
        if r < acc: return z
    return ZOOMS[0][0]

def article_urls(a, rng, excl):
    """yields (title, url). api: random articles, long ones only (a stub has 1-2 usable paragraphs, a long article has dozens;
    the first run visited 1063 random articles in 45 min and got only 3 240 lines)."""
    if a.source == 'files':
        for f in sorted(os.listdir(a.files_dir)):
            if f.endswith('.html'): yield f, 'file://' + os.path.abspath(os.path.join(a.files_dir, f))
        return
    import fetch_corpus as FC
    fails = 0
    while True:
        d = FC.api({'action': 'query', 'generator': 'random', 'grnnamespace': '0', 'grnlimit': '50', 'grnfilterredir': 'nonredirects', 'prop': 'info'}); time.sleep(0.4)
        pages = (d or {}).get('query', {}).get('pages') if d else None
        if not pages:
            fails += 1
            if fails > 5: return
            time.sleep(5); continue
        fails = 0
        for pg in pages:
            if pg.get('length', 0) >= a.min_bytes and pg['title'] not in excl:
                yield pg['title'], a.base_url + urllib.parse.quote(pg['title'].replace(' ', '_'))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True); ap.add_argument('--unicharset', required=True)
    ap.add_argument('--corpus', default=None, help='corpus.txt, only used to skip its holdout paragraphs')
    ap.add_argument('--exclude', required=True, help='ft/articles.txt (pinned test articles)')
    ap.add_argument('--n-train', type=int, default=18000); ap.add_argument('--n-eval', type=int, default=800)
    ap.add_argument('--max-minutes', type=float, default=40); ap.add_argument('--max-par', type=int, default=12, help='paragraphs per article')
    ap.add_argument('--source', choices=['api', 'files'], default='api'); ap.add_argument('--files-dir', default=None)
    ap.add_argument('--base-url', default='https://fa.wikipedia.org/wiki/'); ap.add_argument('--delay', type=float, default=0.3)
    ap.add_argument('--chrome', default=os.environ.get('CHROME_PATH')); ap.add_argument('--width', type=int, default=1100)
    ap.add_argument('--min-bytes', type=int, default=15000, help='api source: skip articles shorter than this (wikitext bytes)')
    ap.add_argument('--font-mix', type=float, default=0.5); ap.add_argument('--low-p', type=float, default=0.3, help='share of lines with extra degradation (blur/downscale/noise); real screenshots are mostly clean')
    ap.add_argument('--seed', type=int, default=7); ap.add_argument('--jobs', type=int, default=os.cpu_count() or 1)
    ap.add_argument('--keep-png', action='store_true'); ap.add_argument('--dump-lines', default=None, help='write line labels to this jsonl (debug)')
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    rng = random.Random(a.seed)
    allowed = C.load_unicharset(a.unicharset)
    excl = {'ایران'} | {t.strip().replace('_', ' ') for t in open(a.exclude, encoding='utf-8') if t.strip() and not t.startswith('#')}
    holdout = load_holdout_keys(a.corpus)
    for s in ('train', 'eval'): os.makedirs(os.path.join(a.out, s), exist_ok=True)
    quota = {'train': a.n_train, 'eval': a.n_eval}; n = {'train': 0, 'eval': 0}; made = []
    stats = dict(articles=0, paragraphs=0, skipped_holdout=0, lines_seen=0, lines_bad_charset=0, lines_short=0)
    dump = open(a.dump_lines, 'w', encoding='utf-8') if a.dump_lines else None
    t0 = time.time(); seen_titles = set()
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=a.chrome) if a.chrome else pw.chromium.launch()
        ctxs = {z: br.new_context(viewport={'width': a.width, 'height': 900}, device_scale_factor=z, locale='fa-IR', user_agent=MT.UA) for z, _ in ZOOMS}
        if a.source == 'api':
            for c in ctxs.values(): c.route(re.compile(r'\.(png|jpe?g|gif|svg|webp|ogg|webm|mp4)(\?.*)?$', re.I), lambda r: r.abort())
        for title, url in article_urls(a, rng, excl):
            if time.time() - t0 > a.max_minutes * 60 or all(n[s] >= quota[s] for s in quota): break
            if title in seen_titles: continue
            seen_titles.add(title); zoom = pick_zoom(rng); pg = ctxs[zoom].new_page()
            try:
                resp = pg.goto(url, wait_until='load', timeout=60000)
                if resp is not None and resp.status >= 400: raise RuntimeError(f'HTTP {resp.status}')
                if pg.title().strip() in excl: raise RuntimeError('excluded title')
                pg.add_style_tag(content=MT.HIDE_CSS); fcss = font_css(rng, a.font_mix)
                if fcss: pg.add_style_tag(content=fcss)
                pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
                items = [it for it in pg.evaluate(MT.JS_SCAN) if len(it['text']) >= 100 and not it['odd'] and not it.get('ovl')]
                rng.shuffle(items); stats['articles'] += 1
                for it in items[:a.max_par]:
                    ptxt = C.clean_text(it['text']); split = T.split_of(ptxt)
                    if split == 'holdout' or n.get(split, 1) >= quota.get(split, 0): continue
                    if key_of(ptxt) in holdout: stats['skipped_holdout'] += 1; continue
                    stats['paragraphs'] += 1
                    r = pg.evaluate(MT.JS_RECT, it['i']); lines = pg.evaluate(JS_LINES, it['i'])
                    clip = {'x': max(0, r['x'] - 6), 'y': max(0, r['y'] - 6), 'width': r['w'] + 12, 'height': r['h'] + 12}
                    try: shot = pg.screenshot(clip=clip, full_page=True, type='png', timeout=60000, animations='disabled')
                    except Exception: continue
                    page_im = Image.open(io.BytesIO(shot)).convert('RGB')
                    for ln in lines:
                        stats['lines_seen'] += 1
                        text = C.clean_text(re.sub(r'\s+', ' ', ln['text']).strip())
                        if len(text) < 6: stats['lines_short'] += 1; continue
                        if not C.keep_line(text, allowed): stats['lines_bad_charset'] += 1; continue
                        if n[split] >= quota[split]: break
                        px = lambda v, o: (v - o) * zoom
                        box = (px(ln['l'] - 4, clip['x']), px(ln['t'], clip['y']), px(ln['r'] + 4, clip['x']), px(ln['b'], clip['y']))
                        box = (max(0, int(box[0])), max(0, int(box[1])), min(page_im.width, int(box[2]) + 1), min(page_im.height, int(box[3]) + 1))
                        if box[2] - box[0] < 20 or box[3] - box[1] < 6: continue
                        img = C.degrade(drop_edge_fragments(page_im.crop(box)), rng, font_size=14 * zoom, low_p=a.low_p)
                        base = os.path.join(a.out, split, f'chr_{split}_{n[split]:07d}')
                        T.write_sample(base, text, img); made.append((split, base)); n[split] += 1
                        if dump: dump.write(json.dumps(dict(base=base, text=text, zoom=zoom, split=split), ensure_ascii=False) + '\n')
            except Exception as e:
                print('SKIP', title, str(e)[:80], file=sys.stderr)
            finally:
                pg.close()
            if stats['articles'] % 10 == 0:
                print(f"{stats['articles']} articles, train {n['train']}/{quota['train']}, eval {n['eval']}/{quota['eval']}, {(time.time() - t0) / 60:.0f} min", flush=True)
            time.sleep(a.delay if a.source == 'api' else 0)
        br.close()
    why = 'quota reached' if all(n[s] >= quota[s] for s in quota) else ('TIME LIMIT' if time.time() - t0 > a.max_minutes * 60 else 'ran out of pages')
    print(f"DONE ({why}) lines: train {n['train']} eval {n['eval']}; {stats}", flush=True)
    if dump: dump.close()
    with Pool(a.jobs) as pool:
        res = pool.map(T.to_lstmf, [b for _, b in made], chunksize=16)
    lists = {'train': [], 'eval': []}
    for (split, _), r in zip(made, res):
        if r: lists[split].append(r)
    for split in lists:                                                  # append to the Pillow lists, then shuffle deterministically
        path = os.path.join(a.out, f'list.{split}')
        old = [l for l in open(path).read().split('\n') if l] if os.path.exists(path) else []
        allp = old + lists[split]; random.Random(a.seed).shuffle(allp)
        open(path, 'w').write('\n'.join(allp) + '\n')
        print(split, 'lstmf from chromium:', len(lists[split]), '| list total:', len(allp), flush=True)
    if not a.keep_png:
        for s in ('train', 'eval'):
            d = os.path.join(a.out, s)
            for f in os.listdir(d):
                if f.startswith('chr_') and f.endswith(('.png', '.box', '.gt.txt')) and os.path.exists(os.path.join(d, f.split('.')[0] + '.lstmf')): os.remove(os.path.join(d, f))
    json.dump(dict(stats, n_train=len(lists['train']), n_eval=len(lists['eval']), minutes=round((time.time() - t0) / 60, 1), ended=why),
              open(os.path.join(a.out, 'chromium_stats.json'), 'w'), indent=1)
    if not lists['train']:
        sys.exit('no chromium training lines were produced')

if __name__ == '__main__':
    main()
