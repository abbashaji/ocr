"""Wikisource / Commons access (runs on GitHub Actions; the sandbox cannot reach these hosts)."""
import re, time, requests

UA = {'User-Agent': 'MatnYabDatasetBuilder/0.1 (https://github.com/abbashaji/ocr; offline OCR training data from public-domain/CC works)'}
WS = 'https://fa.wikisource.org/w/api.php'
COM = 'https://commons.wikimedia.org/w/api.php'
S = requests.Session(); S.headers.update(UA)
# Licences accepted (Commons LicenseShortName, case-insensitive prefix match). Everything else is rejected.
ALLOWED_LICENSES = ('public domain', 'cc0', 'cc by 1', 'cc by 2', 'cc by 3', 'cc by 4', 'cc-by', 'cc by-sa', 'cc-by-sa', 'cc by sa', 'pd')
REJECT_WORDS = ('nc', 'nd', 'non-commercial', 'noncommercial', 'noderiv')

def license_ok(short):
    s = (short or '').strip().lower()
    if not s: return False
    if any(re.search(r'(^|[\s\-])' + w + r'($|[\s\-])', s) for w in REJECT_WORDS): return False
    return s.startswith(ALLOWED_LICENSES)

def api(url, **p):
    p.update(format='json', formatversion=2)
    for k in range(6):
        try:
            r = S.get(url, params=p, timeout=90)
            if r.status_code == 200: return r.json()
        except Exception: pass
        time.sleep(3 * (k + 1))
    return {}

def category_pages(cat, limit_pages=200):
    out, cont = [], {}
    for _ in range(limit_pages):
        d = api(WS, action='query', list='categorymembers', cmtitle=cat, cmlimit=500, cmprop='title|ids', **cont)
        out += [m['title'] for m in d.get('query', {}).get('categorymembers', [])]
        if 'continue' not in d: break
        cont = d['continue']
    return out

def quality_categories():
    m = api(WS, action='query', meta='allmessages', ammessages='proofreadpage_quality3_category|proofreadpage_quality4_category')
    c = {x['name']: x.get('content') for x in m.get('query', {}).get('allmessages', [])}
    return {3: 'Category:' + c['proofreadpage_quality3_category'], 4: 'Category:' + c['proofreadpage_quality4_category']}

def fetch_wikitext(titles):
    """-> {title: (revid, wikitext)}; 50 titles per request."""
    out = {}
    for i in range(0, len(titles), 50):
        d = api(WS, action='query', prop='revisions', rvprop='ids|content', rvslots='main', titles='|'.join(titles[i:i + 50]))
        for pg in d.get('query', {}).get('pages', []):
            rv = (pg.get('revisions') or [None])[0]
            if rv: out[pg['title']] = (rv.get('revid'), rv['slots']['main']['content'])
    return out

def commons_info(filename):
    d = api(COM, action='query', titles='File:' + filename, prop='imageinfo|categories', iiprop='extmetadata|size|mime|url|sha1',
            cllimit='max')
    pg = (d.get('query', {}).get('pages') or [{}])[0]
    ii = (pg.get('imageinfo') or [{}])[0]
    em = ii.get('extmetadata', {})
    strip = lambda s: re.sub('<[^>]+>', '', s or '').strip()
    return dict(file=filename, license=strip((em.get('LicenseShortName') or {}).get('value')),
                license_url=strip((em.get('LicenseUrl') or {}).get('value')),
                artist=strip((em.get('Artist') or {}).get('value'))[:120], date=strip((em.get('DateTimeOriginal') or {}).get('value'))[:60],
                credit=strip((em.get('Credit') or {}).get('value'))[:160], url=ii.get('url'), size=ii.get('size'), sha1=ii.get('sha1'),
                mime=ii.get('mime'), page_url='https://commons.wikimedia.org/wiki/File:' + filename.replace(' ', '_'),
                categories=[c['title'] for c in pg.get('categories', [])][:20], missing=not ii)

def download(url, dest, tries=4):
    for k in range(tries):
        try:
            with S.get(url, stream=True, timeout=120) as r:
                if r.status_code != 200: raise IOError(r.status_code)
                with open(dest, 'wb') as f:
                    for ch in r.iter_content(1 << 20): f.write(ch)
            return True
        except Exception as e:
            time.sleep(5 * (k + 1))
    return False
