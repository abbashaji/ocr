"""Offline test fixture: Wikipedia-shaped HTML pages from corpus.txt (links, bold, ZWNJ, raised [۱۲] markers) for
   make_chromium_data.py --source files. usage: make_fixture_pages.py corpus.txt OUTDIR"""
import random, sys, html
rng = random.Random(3)
paras = [l.strip() for l in open(sys.argv[1], encoding='utf-8') if 200 <= len(l.strip()) <= 800]
rng.shuffle(paras)
CSS = """body{font-family:Vazirmatn,'Noto Naskh Arabic',sans-serif;font-size:14px;line-height:1.6;color:#202122;background:#fff;margin:0}
#content{width:900px;margin:20px auto;direction:rtl} a{color:#0645ad;text-decoration:none} sup.reference{font-size:11px;line-height:1}
sup.reference a{color:#0645ad}"""
def wrap(p):
    ws = p.split(' '); out = []
    for i, w in enumerate(ws):
        w = html.escape(w); r = rng.random()
        if r < 0.06: w = f'<a href="#x">{w}</a>'
        elif r < 0.08: w = f'<b>{w}</b>'
        out.append(w)
        if rng.random() < 0.05: out.append(f'<sup class="reference"><a href="#r">[{str(rng.randint(1,150)).translate(str.maketrans("0123456789","۰۱۲۳۴۵۶۷۸۹"))}]</a></sup>')
    return ' '.join(out)
for n in range(6):
    body = '\n'.join(f'<p>{wrap(paras.pop())}</p>' for _ in range(16))
    open(f'{sys.argv[2]}/a{n}.html', 'w', encoding='utf-8').write(f'<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><title>مقاله {n}</title><style>{CSS}</style></head><body><div id="content"><div id="mw-content-text"><div class="mw-parser-output">{body}</div></div></div></body></html>')
