#!/usr/bin/env python3
"""Fetch Persian Wikipedia body text through the MediaWiki API into corpus.txt (one paragraph per line).

usage: fetch_corpus.py --out corpus.txt --exclude ft/articles.txt [--target-mb 20] [--max-minutes 90]
Random articles (list=random), parsed with action=parse; only <p> body paragraphs are kept, citation markers,
edit links and templates removed. Excludes «ایران» and every pinned test article. Polite: descriptive User-Agent,
--delay s (default 0.4) between requests, one request at a time, honours 429/maxlag with back-off. Text is CC BY-SA: do not commit the corpus.
"""
import argparse, json, os, re, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

API = 'https://fa.wikipedia.org/w/api.php'
UA = 'ocr-finetune-bot/1.0 (Tesseract fine-tuning corpus; https://github.com/abbashaji/ocr)'
ALWAYS_EXCLUDE = {'ایران'}

def api(params, tries=5):
    url = API + '?' + urllib.parse.urlencode({**params, 'format': 'json', 'formatversion': '2', 'maxlag': '5'})
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60) as r:
                d = json.load(r)
            if 'error' in d and d['error'].get('code') == 'maxlag': time.sleep(5 * (k + 1)); continue
            return d
        except Exception as e:
            time.sleep(3 * (k + 1))
    return None

def paragraphs_from_html(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')
    root = soup.select_one('.mw-parser-output') or soup
    for bad in root.select('sup, style, script, .mw-editsection, .noprint, table, figure, .thumb, .reflist'): bad.decompose()
    out = []
    paras = root.find_all('p', recursive=False)
    for sec in root.find_all('section', recursive=False): paras += sec.find_all('p', recursive=False)   # Parsoid-style wrapping
    for p in paras:
        t = C.clean_text(p.get_text(' ', strip=False))
        t = C.MARKER.sub('', t)
        t = re.sub(r'\[[^\]]{0,40}\]', '', t)                  # leftover [..] notes
        t = re.sub(r'\s+([،؛.؟:])', r'\1', t); t = re.sub(r'\s+', ' ', t).strip()
        if len(t) >= 80 and sum(c.isascii() and c.isalpha() for c in t) < 0.15 * len(t): out.append(t)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True); ap.add_argument('--exclude', required=True)
    ap.add_argument('--target-mb', type=float, default=20); ap.add_argument('--max-minutes', type=float, default=90); ap.add_argument('--delay', type=float, default=0.4)
    a = ap.parse_args()
    excl = ALWAYS_EXCLUDE | {t.strip() for t in open(a.exclude, encoding='utf-8') if t.strip() and not t.startswith('#')}
    excl_n = {e.replace('_', ' ') for e in excl}
    seen, total, n_art, n_req, n_stub, t0 = set(), 0, 0, 0, 0, time.time()
    with open(a.out, 'w', encoding='utf-8') as f:
        while total < a.target_mb * 1e6 and time.time() - t0 < a.max_minutes * 60:
            d = api({'action': 'query', 'list': 'random', 'rnnamespace': '0', 'rnlimit': '50', 'rnfilterredir': 'nonredirects'}); time.sleep(a.delay)
            if not d: continue
            for pg in d['query']['random']:
                title = pg['title']
                if title in excl_n or total >= a.target_mb * 1e6 or time.time() - t0 > a.max_minutes * 60: continue
                n_req += 1
                r = api({'action': 'parse', 'page': title, 'prop': 'text', 'redirects': '1', 'disableeditsection': '1'}); time.sleep(a.delay)
                if not r or 'parse' not in r: continue
                if r['parse'].get('title') in excl_n: continue
                paras = [p for p in paragraphs_from_html(r['parse']['text']) if p not in seen]
                if sum(map(len, paras)) < 1500: n_stub += 1; continue          # skip stubs
                for p in paras: seen.add(p); f.write(p + '\n'); total += len(p.encode('utf-8'))
                n_art += 1
                if n_art % 50 == 0: print(f'{n_art} articles, {total / 1e6:.1f} MB, {(time.time() - t0) / 60:.0f} min', flush=True)
    why = 'size target reached' if total >= a.target_mb * 1e6 else 'TIME LIMIT reached before the size target'
    print(f'DONE {n_art} articles, {total / 1e6:.2f} MB in {(time.time() - t0) / 60:.0f} min ({why}; {n_req} requests, {n_stub} stub/empty articles skipped)')

if __name__ == '__main__':
    main()
