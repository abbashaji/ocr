"""Leakage reference text: fa.wikipedia articles of ft/articles.txt (+ the client benchmark article) and the client sample text."""
import json, os, re, sys, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import wiki

EXTRA_TITLES = ['ایران']          # the client's benchmark article is deliberately absent from articles.txt but must not leak either

def titles_from(path):
    return [t.strip() for t in open(path, encoding='utf-8') if t.strip() and not t.startswith('#')]

def fetch_texts(titles):
    """-> {title: plain text}. One request per title: TextExtracts returns only ONE full-text extract per request
    (the first full run fetched 2 of 31 articles with a 20-title batch, so the leakage check was nearly empty)."""
    out = {}
    for t in titles:
        d = wiki.api('https://fa.wikipedia.org/w/api.php', action='query', prop='extracts', explaintext=1, titles=t, redirects=1)
        for pg in d.get('query', {}).get('pages', []):
            if pg.get('extract'): out[t] = pg['extract']
    return out

def build(articles_path, extra_files=(), out_path=None, min_coverage=0.9):
    titles = titles_from(articles_path) + EXTRA_TITLES
    texts = fetch_texts(titles)
    if len(texts) < min_coverage * len(titles):          # fail loudly: a silent partial reference makes the leakage check meaningless
        raise SystemExit(f'leakage reference incomplete: {len(texts)}/{len(titles)} articles fetched')
    blob = '\n'.join(texts.values())
    for f in extra_files:
        if os.path.exists(f): blob += '\n' + open(f, encoding='utf-8').read()
    meta = dict(titles_requested=len(titles), titles_fetched=len(texts), missing=[t for t in titles if t not in texts], chars=len(blob))
    if out_path:
        open(out_path, 'w', encoding='utf-8').write(blob)
        json.dump(meta, open(out_path + '.json', 'w', encoding='utf-8'), ensure_ascii=False)
    return blob, meta

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('--articles', required=True); ap.add_argument('--extra', nargs='*', default=[])
    ap.add_argument('--out', required=True); a = ap.parse_args()
    blob, meta = build(a.articles, a.extra, a.out); print(json.dumps(meta, ensure_ascii=False)[:500])
