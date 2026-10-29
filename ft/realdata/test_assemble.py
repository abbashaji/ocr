import json, os, random, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytest
from PIL import Image, ImageDraw
import export, augment, assemble

L1 = 'در سدهٔ نخست پیش از میلاد پادشاهان ایران‌زمین سپاهی بزرگ فراهم آوردند'
L2 = 'مردمان آن سرزمین، که از دیرباز با کشاورزی روزگار می‌گذراندند، شگفت‌زده شدند'
L3 = 'گزارش‌های تاریخی نشان می‌دهد که در سال ۱۲۹۸ شمسی شمار سپاهیان به ۲۵٬۰۰۰ تن رسید'
L4 = 'بازرگانان از دورترین سرزمین‌ها کالاهای گرانبها آوردند و در بازار شهر داد و ستد کردند'
L5 = 'این جمله در مقالهٔ ارزیابی ویکی‌پدیا آمده است و نباید هرگز در آموزش به کار رود ٪ ۵'

def mk_part(root, wid, role, lines, lic='Public domain'):
    d = os.path.join(root, 'part-' + wid); os.makedirs(os.path.join(d, 'lines'))
    jl = open(os.path.join(d, 'lines.jsonl'), 'w', encoding='utf-8')
    for i, (txt, tier) in enumerate(lines):
        lid = f'{wid}_p0001_l{i:02d}'
        Image.new('L', (400, 40), 255).save(os.path.join(d, 'lines', lid + '.png'))
        jl.write(json.dumps(dict(id=lid, work=wid, page=1, revid=5, page_title='برگه:X.pdf/1', quality=4, role=role, idx=i, y0=0, y1=40, ocr=txt, label=txt,
                                 sim=0.97, margin=0.4, tier=tier, reason='', flags=[], w=400, h=40, deskew=0.0, dpi=200, page_w=1000, page_h=1500), ensure_ascii=False) + '\n')
    jl.close()
    json.dump(dict(work=wid, file=wid + '.pdf', role=role, started='2026-10-28T00:00:00+00:00', proofread_pages_total=10, pages_sampled=1,
                   commons=dict(license=lic, page_url='https://commons.wikimedia.org/wiki/File:' + wid, artist='A', date='1930'), counts={}, line_reasons={}),
              open(os.path.join(d, 'stats.json'), 'w'))

@pytest.fixture
def built(tmp_path):
    parts = tmp_path / 'parts'; parts.mkdir()
    mk_part(parts, 'w01', 'train', [(L1, 'GOLD'), (L2, 'GOLD'), (L3, 'SILVER'), (L5, 'GOLD'), (L4, 'GOLD')])
    mk_part(parts, 'w02', 'tune', [(L2, 'GOLD')])                       # duplicate of a train line -> kept in tune, dropped in train
    mk_part(parts, 'w03', 'final', [(L1 + ' و', 'GOLD')])                # shares 5-word shingle with train line L1
    works = [dict(id=w, file=w + '.pdf', role=r, max_pages=1, dpi=200, note='') for w, r in (('w01', 'train'), ('w02', 'tune'), ('w03', 'final'))]
    json.dump(dict(works=works), open(tmp_path / 'works.json', 'w', encoding='utf-8'), ensure_ascii=False)
    open(tmp_path / 'leak.txt', 'w', encoding='utf-8').write('متن ارزیابی. ' + L5 + ' پایان.')
    out = tmp_path / 'ds'
    subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'assemble.py'), '--parts', str(parts), '--works', str(tmp_path / 'works.json'),
                    '--leak', str(tmp_path / 'leak.txt'), '--out', str(out), '--augment', '1'], check=True, capture_output=True)
    return out

def test_presets_differ_only_where_intended():
    assert export.folded_text('سدهٔ ۱۲٫۵، ٪') == 'سده ۱۲.۵, #'
    assert export.distinct_text('سدهٔ ۱۲٫۵، ٪') == 'سدهٔ ۱۲٫۵، ٪'
    assert export.distinct_text('كتاب ي') == 'کتاب ی'

def test_compat_fold_presentation_forms_and_alef_maksura():
    s = '\ufe8dتومبیل \ufe81تمسفر آبى'
    for f in (export.folded_text, export.distinct_text):
        assert f(s) == 'اتومبیل آتمسفر آبی'
        assert not any(0xFB50 <= ord(c) <= 0xFEFF for c in f(s))
    assert export.distinct_text('سدهٔ') == 'سدهٔ'            # ezafe still kept in distinct

def test_dedupe_leak_and_split_by_work(built):
    rows = [json.loads(l) for l in open(built / 'manifest.jsonl', encoding='utf-8')]
    ids = {r['id'] for r in rows}
    assert 'w01_p0001_l03' not in ids and 'w01_p0001_l01' not in ids   # L5 leaked (eval text) / L2 duplicated in tune
    assert 'w02_p0001_l00' in ids                                      # tune keeps the duplicate
    assert 'w01_p0001_l00' not in ids                                  # shares 5-word shingle with the FINAL line -> train copy dropped
    assert 'w03_p0001_l00' in ids
    assert {r['split'] for r in rows} <= {'train', 'tune', 'final'}
    r = next(r for r in rows if r['id'] == 'w01_p0001_l02')
    assert r['label_full'] == L3 and r['label_folded'] != r['label_distinct'] and '٬' in r['label_distinct']

def test_exports_layout(built):
    t = built / 'export' / 'tesseract_distinct_gold' / 'train'
    gts = sorted(p.name for p in t.glob('*.gt.txt')); pngs = sorted(p.name for p in t.glob('*.png'))
    assert gts and [g[:-7] for g in gts] == [p[:-4] for p in pngs]
    pad = built / 'export' / 'paddle_folded_gold'
    line = open(pad / 'train.txt', encoding='utf-8').read().splitlines()[0]
    img, label = line.split('\t'); assert os.path.exists(pad / img) and label and (pad / 'dict.txt').exists()
    assert (built / 'ATTRIBUTION.md').exists() and (built / 'contact_sheet.html').exists()
    aug = built / 'export' / 'tesseract_folded_gold_train_aug1' / 'train'
    assert any('_aug1' in p.name for p in aug.iterdir())

def test_augment_is_seeded_and_leaves_input_untouched():
    im = Image.new('L', (300, 40), 255); ImageDraw.Draw(im).rectangle([20, 10, 280, 30], fill=0); before = im.tobytes()
    a1 = augment.augment(im, random.Random('s:1:1')); a2 = augment.augment(im, random.Random('s:1:1')); a3 = augment.augment(im, random.Random('s:1:2'))
    assert a1.tobytes() == a2.tobytes() and a1.tobytes() != a3.tobytes() and im.tobytes() == before


def test_leak_fetches_one_title_per_request_and_fails_when_incomplete(monkeypatch, tmp_path):
    import leak, wiki
    calls = []
    def fake_api(url, **p):
        calls.append(p['titles'])
        if p['titles'] in ('الف', 'ب'): return {'query': {'pages': [{'title': p['titles'], 'extract': 'متن ' + p['titles']}]}}
        return {'query': {'pages': [{'title': p['titles'], 'missing': True}]}}
    monkeypatch.setattr(wiki, 'api', fake_api)
    assert leak.fetch_texts(['الف', 'ب', 'ج']) == {'الف': 'متن الف', 'ب': 'متن ب'}
    assert calls == ['الف', 'ب', 'ج']                                   # never batched
    art = tmp_path / 'a.txt'; art.write_text('الف\nب\nج\nد\n', encoding='utf-8')
    monkeypatch.setattr(leak, 'EXTRA_TITLES', [])
    with pytest.raises(SystemExit): leak.build(str(art))                # 2/4 < 90% -> loud failure
