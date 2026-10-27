#!/usr/bin/env python3
"""Build the Persian training corpus from a BULK Wikipedia source instead of the rate-limited API.

usage: fetch_corpus_dump.py --out corpus.txt --exclude ft/articles.txt --stats out/corpus_stats.json
           [--target-mb 100] [--max-minutes 60] [--source auto|hf|dump] [--ground-truth tests/]

Output format is identical to ft/fetch_corpus.py: UTF-8, ONE PARAGRAPH PER LINE, text already passed through
common.clean_text (this is what make_train_data.py reads). Extra: corpus_stats.json (see write_stats()).

Sources (the sandbox cannot reach either, so both are exercised on GitHub Actions; the shared parser/filters are
unit-tested in ft/test_fetch_corpus_dump.py):
  hf    huggingface.co dataset "wikimedia/wikipedia", config 20231101.fa (parquet, plain text already stripped of markup).
        Fast CDN, stable snapshot, no wikitext parsing needed. Snapshot is from 2023-11-01.
  dump  https://dumps.wikimedia.org/fawiki/latest/fawiki-latest-pages-articles.xml.bz2 (official, current). The bz2 is
        stream-decoded (resumable HTTP) and wikitext is stripped by regexes here. Slower, depends on dump-server speed.
  auto  (default) hf first; on any failure fall back to dump.

Leak protection (evaluation set = pinned articles of ft/articles.txt, screenshotted live by make_tests.py):
  1. every article whose normalised title is listed in --exclude (plus «ایران») is skipped;
  2. the text of those articles (as found in the source) and of any file under --ground-truth is turned into 10-word
     shingles, and every corpus paragraph sharing one shingle is dropped (catches copies/quotes in other articles).
Text is CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/): the corpus is cached/uploaded as a workflow
artifact, never committed.
"""
import argparse, bz2, hashlib, html, io, json, os, random, re, sys, tempfile, time, unicodedata
import urllib.request
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

UA = 'ocr-finetune-bot/1.0 (Tesseract fine-tuning corpus; https://github.com/abbashaji/ocr)'
ALWAYS_EXCLUDE = {'ایران'}
HF_API = 'https://huggingface.co/api/datasets/wikimedia/wikipedia/parquet/{cfg}/train'
HF_CONFIG = '20231101.fa'
DUMP_URLS = ['https://dumps.wikimedia.org/fawiki/latest/fawiki-latest-pages-articles.xml.bz2',
             'https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/fawiki/latest/fawiki-latest-pages-articles.xml.bz2']
MIN_LEN, MAX_LEN = 80, 3000          # old fetcher: >= 80 chars, no maximum; the cap only drops pathological lines
MIN_ARTICLE_CHARS = 1500             # same stub rule as the old fetcher
MIN_PERSIAN_RATIO = 0.70             # Arabic-block letters / non-space chars
SHINGLE = 10
END_OK = tuple('.؟!:؛»)"…') + ('.',)

# ---------------------------------------------------------------- titles / exclusion
def norm_title(t):
    t = unicodedata.normalize('NFKC', C.clean_text(t.replace('_', ' ')))
    return re.sub(r'\s+', ' ', t).strip().casefold()

def read_excluded(path):
    """-> {normalised title: original title}; '#' lines and blanks ignored; always includes «ایران»."""
    out = {norm_title(t): t for t in ALWAYS_EXCLUDE}
    for ln in open(path, encoding='utf-8'):
        ln = ln.strip()
        if ln and not ln.startswith('#'): out[norm_title(ln)] = ln
    return out

def shingles(text):
    w = text.split()
    if len(w) <= SHINGLE: return {hash(' '.join(w))} if w else set()
    return {hash(' '.join(w[i:i + SHINGLE])) for i in range(len(w) - SHINGLE + 1)}

def ground_truth_shingles(path):
    s = set()
    if not path: return s
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith('.txt'):
                for ln in open(os.path.join(root, f), encoding='utf-8', errors='replace'):
                    s |= shingles(C.clean_text(ln))
    return s

# ---------------------------------------------------------------- paragraph cleaning (shared by both sources)
def clean_paragraph(raw):
    """-> cleaned paragraph or None. Same steps as fetch_corpus.paragraphs_from_html plus stricter filters."""
    t = C.clean_text(raw)
    t = C.MARKER.sub('', t)
    t = re.sub(r'\[[^\]]{0,40}\]', '', t)                                   # leftover [..] notes
    t = re.sub(r'\(\s*[،؛,;:]?\s*\)|«\s*»', '', t)                          # empty brackets left by removed templates
    t = re.sub(r'\s+([،؛.؟:])', r'\1', t); t = re.sub(r'\s+', ' ', t).strip()
    if not (MIN_LEN <= len(t) <= MAX_LEN): return None
    if sum(c.isascii() and c.isalpha() for c in t) >= 0.15 * len(t): return None
    if any(ch in t for ch in '{}|<>[]'): return None                         # unparsed markup
    nospace = [c for c in t if not c.isspace()]
    if sum(('؀' <= c <= 'ۿ') and c.isalpha() for c in nospace) < MIN_PERSIAN_RATIO * len(nospace): return None
    if not t.endswith(END_OK): return None                                   # list items / headings / cut-off text
    return t

def plain_paragraphs(text):
    """paragraphs of an already plain-text article (HF dataset): one per line"""
    return [p for p in (clean_paragraph(l) for l in text.split('\n')) if p]

# ---------------------------------------------------------------- wikitext -> paragraphs (dump source)
_COMMENT = re.compile(r'<!--.*?-->', re.S)
_REF1 = re.compile(r'<ref\b[^>]*/>', re.I)
_REF2 = re.compile(r'<ref\b[^>]*>.*?</ref\s*>', re.S | re.I)
_BLOCK_TAGS = re.compile(r'<(gallery|math|timeline|imagemap|score|syntaxhighlight|source|pre|code|references|poem|chem)\b[^>]*>.*?</\1\s*>', re.S | re.I)
_TABLE = re.compile(r'\{\|(?:(?!\{\|).)*?\|\}', re.S)
_TEMPLATE = re.compile(r'\{\{[^{}]*\}\}')
_NS = r'(?:پرونده|تصویر|رده|File|Image|Category|Media|Datei|پرونده‌ها)'
_FILE_LINK = re.compile(r'\[\[\s*' + _NS + r'\s*:[^\[\]]*(?:\[\[[^\[\]]*\]\][^\[\]]*)*\]\]', re.I)
_LINE_SKIP_NS = re.compile(r'^\[\[\s*' + _NS + r'\s*:', re.I)
_LINK = re.compile(r'\[\[(?:[^\[\]|]*\|)?([^\[\]]*)\]\]')
_EXT1 = re.compile(r'\[(?:https?:)?//\S+\s+([^\]]*)\]')
_EXT2 = re.compile(r'\[(?:https?:)?//[^\]\s]*\]')
_TAG = re.compile(r'</?[A-Za-z][^>]*>')

def wikitext_paragraphs(text):
    text = _COMMENT.sub('', text)
    text = _REF1.sub('', text); text = _REF2.sub('', text); text = _BLOCK_TAGS.sub('', text)
    for _ in range(12):                                                       # nested tables
        new = _TABLE.sub('', text)
        if new == text: break
        text = new
    for _ in range(12):                                                       # nested templates, innermost first
        new = _TEMPLATE.sub('', text)
        if new == text: break
        text = new
    out = []
    for ln in text.split('\n'):
        s = ln.strip()
        if not s or s[0] in '*#;:=!|{}<-' or _LINE_SKIP_NS.match(s) or s.startswith('__'): continue
        s = _FILE_LINK.sub('', s)
        for _ in range(3): s = _LINK.sub(r'\1', s)
        s = _EXT1.sub(r'\1', s); s = _EXT2.sub('', s)
        s = re.sub(r"'{2,5}", '', s); s = _TAG.sub('', s); s = html.unescape(s)
        p = clean_paragraph(s)
        if p: out.append(p)
    return out

# ---------------------------------------------------------------- sources
class HttpStream(io.RawIOBase):
    """Forward-only HTTP body that transparently re-opens the URL with a Range header after a dropped connection."""
    def __init__(self, url, tries=10):
        self.url, self.tries, self.pos, self.resp, self.last_modified, self.length = url, tries, 0, None, None, None
        self._open()
    def _open(self):
        h = {'User-Agent': UA}
        if self.pos: h['Range'] = f'bytes={self.pos}-'
        self.resp = urllib.request.urlopen(urllib.request.Request(self.url, headers=h), timeout=120)
        if self.pos and getattr(self.resp, 'status', 206) != 206: raise IOError('server ignored Range request')
        if self.last_modified is None:
            self.last_modified = self.resp.headers.get('Last-Modified'); self.length = self.resp.headers.get('Content-Length')
    def readable(self): return True
    def readinto(self, b):
        for k in range(self.tries):
            try:
                data = self.resp.read(len(b))
                b[:len(data)] = data; self.pos += len(data); return len(data)
            except Exception as e:
                print(f'  http read error at {self.pos / 1e6:.0f} MB ({e!r}); reconnect {k + 1}/{self.tries}', flush=True)
                time.sleep(5 * (k + 1))
                try: self._open()
                except Exception as e2: print(f'  reopen failed: {e2!r}', flush=True)
        raise IOError('download kept failing')

def _download(url, dest, tries=5):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=180) as r, open(dest, 'wb') as f:
                while True:
                    b = r.read(1 << 20)
                    if not b: break
                    f.write(b)
            return
        except Exception as e:
            print(f'  download error {url}: {e!r} (try {k + 1}/{tries})', flush=True); time.sleep(5 * (k + 1))
    raise IOError(f'cannot download {url}')

def iter_dump_pages(fileobj):
    """yield (title, wikitext) for non-redirect main-namespace pages of a pages-articles XML stream"""
    root = None
    for ev, el in ET.iterparse(fileobj, events=('start', 'end')):
        if ev == 'start':
            if root is None: root = el
            continue
        if not el.tag.endswith('}page') and el.tag != 'page': continue
        ns = el.find('./{*}ns'); title = el.find('./{*}title'); rev = el.find('./{*}revision/{*}text')
        redirect = el.find('./{*}redirect')
        if ns is not None and ns.text == '0' and redirect is None and title is not None and rev is not None and rev.text:
            yield title.text, rev.text
        el.clear()
        if root is not None: root.clear()

def iter_hf_rowgroups(paths, seed):
    """-> list of (path, row group index) in a seeded random order, so a size-limited read spreads over the alphabet"""
    import pyarrow.parquet as pq
    rgs = [(p, i) for p in paths for i in range(pq.ParquetFile(p).num_row_groups)]
    random.Random(seed).shuffle(rgs); return rgs

def hf_parquet_urls():
    try:
        with urllib.request.urlopen(urllib.request.Request(HF_API.format(cfg=HF_CONFIG), headers={'User-Agent': UA}), timeout=60) as r:
            urls = json.load(r)
        if urls: return list(urls)
    except Exception as e:
        print(f'HF parquet listing failed ({e!r}); trying the conventional file name', flush=True)
    return [f'https://huggingface.co/datasets/wikimedia/wikipedia/resolve/main/{HF_CONFIG}/train-00000-of-00001.parquet']

# ---------------------------------------------------------------- builder
class Builder:
    def __init__(self, excl, gt_shingles, target_bytes, sample_frac, deadline):
        self.excl, self.target, self.frac, self.deadline = excl, target_bytes, sample_frac, deadline
        self.paras, self.seen, self.bytes, self.articles, self.stubs = [], set(), 0, 0, 0   # paras: list of per-article lists
        self.excl_seen, self.excl_shingles, self.gt = {}, set(), gt_shingles
        self.articles_scanned = 0
    def full(self): return self.bytes >= self.target
    def timeout(self): return time.time() > self.deadline
    def keep_title(self, title):
        return int(hashlib.md5(title.encode()).hexdigest()[:8], 16) % 10000 < self.frac * 10000
    def see_excluded(self, nt, paras):
        self.excl_seen[nt] = self.excl_seen.get(nt, 0) + 1
        for p in paras: self.excl_shingles |= shingles(p)
    def add_article(self, paras):
        paras = [p for p in paras if p not in self.seen]
        if sum(map(len, paras)) < MIN_ARTICLE_CHARS: self.stubs += 1; return
        for p in paras: self.seen.add(p); self.bytes += len(p.encode('utf-8'))
        self.paras.append(paras); self.articles += 1
    def finalize(self):
        """drop paragraphs overlapping the evaluation texts; -> (flat list, n dropped)"""
        bad = self.excl_shingles | self.gt; out, dropped = [], 0
        for art in self.paras:
            for p in art:
                if bad and shingles(p) & bad: dropped += 1
                else: out.append(p)
        return out, dropped

def build_from_hf(b, paths, seed):
    import pyarrow.parquet as pq
    rgs = iter_hf_rowgroups(paths, seed); files = {}
    def pf(p):
        if p not in files: files[p] = pq.ParquetFile(p)
        return files[p]
    for p, i in rgs:                                                           # pre-pass: titles only (columnar, cheap)
        t = pf(p).read_row_group(i, columns=['title'])
        titles = t.column('title').to_pylist()
        hit = [k for k, x in enumerate(titles) if norm_title(x) in b.excl]
        if hit:
            texts = pf(p).read_row_group(i, columns=['text']).column('text').to_pylist()
            for k in hit: b.see_excluded(norm_title(titles[k]), plain_paragraphs(texts[k]))
    print(f'pre-pass: pinned articles found in source: {len(b.excl_seen)}/{len(b.excl)}', flush=True)
    for p, i in rgs:
        if b.full() or b.timeout(): break
        tb = pf(p).read_row_group(i, columns=['title', 'text'])
        for title, text in zip(tb.column('title').to_pylist(), tb.column('text').to_pylist()):
            if b.full() or b.timeout(): break
            b.articles_scanned += 1
            if norm_title(title) in b.excl or not b.keep_title(title): continue
            b.add_article(plain_paragraphs(text))
        print(f'  {b.articles} articles, {b.bytes / 1e6:.1f} MB', flush=True)

def build_from_dump(b, fileobj, extra_scan_minutes):
    reached_at = None
    for title, text in iter_dump_pages(fileobj):
        b.articles_scanned += 1
        nt = norm_title(title)
        if nt in b.excl: b.see_excluded(nt, wikitext_paragraphs(text)); continue
        if b.timeout(): break
        if b.full():
            reached_at = reached_at or time.time()
            if len(b.excl_seen) >= len(b.excl) or time.time() - reached_at > extra_scan_minutes * 60: break
            continue                                                           # keep scanning ONLY for pinned titles
        if not b.keep_title(title): continue
        b.add_article(wikitext_paragraphs(text))
        if b.articles % 500 == 0 and b.articles: print(f'  {b.articles} articles, {b.bytes / 1e6:.1f} MB', flush=True)

def write_stats(path, **kw):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    json.dump(kw, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True); ap.add_argument('--exclude', required=True); ap.add_argument('--stats', default='corpus_stats.json')
    ap.add_argument('--target-mb', type=float, default=100); ap.add_argument('--max-minutes', type=float, default=60)
    ap.add_argument('--source', choices=['auto', 'hf', 'dump'], default='auto')
    ap.add_argument('--sample-frac', type=float, default=None, help='share of articles to use (deterministic by title hash); default 1.0 for hf, 0.3 for dump')
    ap.add_argument('--extra-scan-minutes', type=float, default=10, help='dump only: after the target is reached keep scanning this long for pinned titles')
    ap.add_argument('--ground-truth', default=None, help='dir with evaluation ground-truth .txt files (optional extra leak filter)')
    ap.add_argument('--parquet', nargs='*', default=None, help='local parquet files (tests / offline) instead of downloading')
    ap.add_argument('--dump-file', default=None, help='local pages-articles xml or xml.bz2 (tests / offline) instead of downloading')
    ap.add_argument('--seed', type=int, default=1)
    a = ap.parse_args(argv)
    t0 = time.time(); excl = read_excluded(a.exclude)
    gt = ground_truth_shingles(a.ground_truth)
    errors, used, dump_date, detail = [], None, None, None
    order = ['hf', 'dump'] if a.source == 'auto' else [a.source]
    if a.parquet is not None: order = ['hf']
    if a.dump_file: order = ['dump']
    for src in order:
        frac = a.sample_frac if a.sample_frac is not None else (1.0 if src == 'hf' else 0.3)
        b = Builder(excl, gt, a.target_mb * 1e6, frac, t0 + a.max_minutes * 60)
        try:
            if src == 'hf':
                tmp = tempfile.mkdtemp(prefix='hfpq_')
                paths = a.parquet
                if paths is None:
                    paths = []
                    for k, u in enumerate(hf_parquet_urls()):
                        d = os.path.join(tmp, f'p{k}.parquet'); print('download', u, flush=True); _download(u, d); paths.append(d)
                build_from_hf(b, paths, a.seed); dump_date = HF_CONFIG.split('.')[0]; dump_date = f'{dump_date[:4]}-{dump_date[4:6]}-{dump_date[6:]}'
                detail = 'huggingface wikimedia/wikipedia ' + HF_CONFIG
            else:
                if a.dump_file:
                    f = bz2.open(a.dump_file, 'rb') if a.dump_file.endswith('.bz2') else open(a.dump_file, 'rb'); detail = a.dump_file
                else:
                    last = None
                    for u in DUMP_URLS:
                        try: hs = HttpStream(u); break
                        except Exception as e: last = e; print(f'cannot open {u}: {e!r}', flush=True)
                    else: raise IOError(f'no dump url reachable: {last!r}')
                    dump_date = hs.last_modified; detail = u
                    f = bz2.BZ2File(io.BufferedReader(hs, 1 << 20), 'rb')
                build_from_dump(b, f, a.extra_scan_minutes)
                dump_date = dump_date or 'unknown'
            used = src
            if b.bytes == 0: raise RuntimeError('source produced no paragraphs')
            break
        except Exception as e:
            errors.append(f'{src}: {e!r}'); print(f'SOURCE {src} FAILED: {e!r}', flush=True); used = None
    if used is None:
        write_stats(a.stats, ok=False, errors=errors, seconds=round(time.time() - t0)); sys.exit(f'all sources failed: {errors}')
    paras, dropped = b.finalize()
    with open(a.out, 'w', encoding='utf-8') as f:
        for p in paras: f.write(p + '\n')
    mb = sum(len(p.encode('utf-8')) for p in paras) / 1e6
    rnd = random.Random(a.seed)
    write_stats(a.stats, ok=True, source=used, source_detail=detail, dump_date=dump_date, paragraphs=len(paras), mb=round(mb, 2),
                target_mb=a.target_mb, reached_target=b.bytes >= a.target_mb * 1e6, articles_used=b.articles, articles_scanned=b.articles_scanned,
                stub_articles_skipped=b.stubs, excluded_titles_requested=sorted(excl.values()),
                excluded_titles_found=sorted(excl[k] for k in b.excl_seen), excluded_titles_not_found=sorted(excl[k] for k in excl if k not in b.excl_seen),
                paragraphs_dropped_eval_overlap=dropped, ground_truth_shingles=len(b.gt), sample_frac=b.frac,
                seconds=round(time.time() - t0), fallback_errors=errors,
                sample=[p[:200] for p in rnd.sample(paras, min(3, len(paras)))])
    print(f'DONE source={used} {len(paras)} paragraphs, {mb:.2f} MB, {b.articles} articles, {dropped} dropped for eval overlap, '
          f'{len(b.excl_seen)}/{len(excl)} pinned titles seen, {time.time() - t0:.0f} s', flush=True)

if __name__ == '__main__':
    main()
