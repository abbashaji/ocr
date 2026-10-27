"""Tests for ft/fetch_corpus_dump.py on tiny local fixtures (the real sources are only reachable from GitHub Actions).

Run from the repo root:  python -m pytest ft/test_fetch_corpus_dump.py -q     (needs pyarrow)
"""
import bz2, json, os, sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_corpus_dump as F

S1 = 'تهران پایتخت و بزرگ‌ترین شهر کشور ایران است و در دامنه جنوبی رشته‌کوه البرز قرار دارد و جمعیت زیادی دارد.'
S2 = 'ریاضیات علمی است که به بررسی کمیت، ساختار، فضا و تغییر می‌پردازد و ریشه در شمارش و اندازه‌گیری دارد.'
S3 = 'درخت یکی از گیاهان چوبی پایا است که ساقه‌ای بلند و شاخه‌های فراوان دارد و در بیشتر مناطق جهان می‌روید.'
S4 = 'رود کارون پرآب‌ترین رود ایران است و از کوه‌های زردکوه بختیاری سرچشمه می‌گیرد و به خلیج فارس می‌ریزد.'
STUB = 'جمله کوتاه.'


def wiki(*paras, extra=''):
    return ('{{جعبه اطلاعات|الف=ب|ج={{تو در تو}}}}\n' + '\n\n'.join(paras) + extra)


def test_norm_title_matches_underscores_digits_and_arabic_letters():
    assert F.norm_title('کورش_بزرگ') == F.norm_title('کورش بزرگ')
    assert F.norm_title('كورش  بزرگ ') == F.norm_title('کورش بزرگ')           # Arabic kaf, extra spaces


def test_read_excluded_skips_comments_and_adds_iran(tmp_path):
    p = tmp_path / 'a.txt'; p.write_text('# comment\n\nتهران\nکورش_بزرگ\n', encoding='utf-8')
    ex = F.read_excluded(str(p))
    assert F.norm_title('تهران') in ex and F.norm_title('کورش بزرگ') in ex and F.norm_title('ایران') in ex and len(ex) == 3


def test_clean_paragraph_filters():
    assert F.clean_paragraph(S1) == S1
    assert F.clean_paragraph('«' + S1[:-1] + '» [۱۲].') is not None
    assert '[' not in F.clean_paragraph(S1[:-1] + ' [۱۲].')                    # citation marker removed
    assert F.clean_paragraph(STUB) is None                                     # too short
    assert F.clean_paragraph(S1[:-1]) is None                                  # does not end like a sentence
    assert F.clean_paragraph('This is an English paragraph that is long enough to pass the length limit easily, truly.') is None
    assert F.clean_paragraph(S1 + ' ' + S1 * 40) is None                       # > MAX_LEN
    assert F.clean_paragraph(S1[:-1] + ' {{x}}.') is None                      # unparsed markup
    mixed = 'abc def ghi jkl ' * 6 + 'متن فارسی کوتاه برای آزمایش.'
    assert F.clean_paragraph(mixed) is None                                    # Latin-heavy


def test_clean_paragraph_applies_clean_text_like_the_old_fetcher():
    raw = S1.replace('ی', 'ي').replace('ک', 'ك') + ''
    out = F.clean_paragraph(raw)
    assert 'ي' not in out and 'ك' not in out                                    # Arabic yeh/kaf normalised
    assert F.clean_paragraph(S2.replace('است', 'اَسْت')) == S2                  # harakat stripped


def test_wikitext_strips_markup_tables_templates_refs_lists_files():
    text = ('{{جعبه|الف={{داخلی|ب}}}}\n'
            "'''تهران''' [[ایران|کشور]] است و [[شهر]] بزرگی است<ref name=a>منبع</ref> که جمعیت زیادی دارد و در [https://x.org سایت] آمده است و تاریخ بسیار طولانی و کهنی دارد.<!-- note -->\n"
            '[[پرونده:Tehran.jpg|بندانگشتی|یک [[عکس]] از شهر]]\n'
            '{| class="wikitable"\n|-\n| سلول ۱ || سلول ۲\n{| nested\n|x\n|}\n|}\n'
            '== تاریخ ==\n'
            '* مورد فهرست که خیلی طولانی است و نباید وارد پیکره شود چون فهرست است و جمله نیست و کامل نیست.\n'
            + S2 + '\n'
            '[[رده:شهرها]]\n')
    ps = F.wikitext_paragraphs(text)
    assert ps[-1] == S2
    assert len(ps) == 2
    first = ps[0]
    for bad in ['{{', '[[', ']]', '<ref', 'منبع', "'''", 'http', 'سلول', 'بندانگشتی', 'رده', 'note', 'مورد فهرست']:
        assert bad not in first and all(bad not in p for p in ps), bad
    assert first.startswith('تهران کشور است و شهر بزرگی است که جمعیت زیادی دارد و در سایت آمده است و')


def test_wikitext_nested_templates_and_unbalanced_braces_dropped():
    assert F.wikitext_paragraphs('{{a|{{b|{{c}}}}}}' + S3) == [S3]
    assert F.wikitext_paragraphs(S3[:-1] + ' }} {{.') == []


def test_shingle_overlap_detection():
    a = F.shingles(S1); assert F.shingles(S1 + ' و بیشتر') & a
    assert not (F.shingles(S3) & a)
    assert F.shingles('کوتاه است') == F.shingles('کوتاه است')


def _xml(pages):
    items = ''
    for title, ns, text, redirect in pages:
        r = '<redirect title="x"/>' if redirect else ''
        t = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        items += f'<page><title>{title}</title><ns>{ns}</ns><id>1</id>{r}<revision><text xml:space="preserve">{t}</text></revision></page>'
    return ('<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.11/"><siteinfo><sitename>x</sitename></siteinfo>' + items + '</mediawiki>').encode()


@pytest.fixture
def articles_txt(tmp_path):
    p = tmp_path / 'articles.txt'; p.write_text('# pinned\nتهران\nریاضیات\nنبود_در_دامپ\n', encoding='utf-8'); return str(p)


def _big(*sents):          # an article body above the stub limit
    return wiki(*(list(sents) * 8))


def test_dump_end_to_end_excludes_titles_and_copied_paragraphs(tmp_path, articles_txt):
    pages = [('تهران', 0, _big(S1), False),                                    # pinned -> excluded
             ('ریاضیات', 0, _big(S2), False),                                   # pinned -> excluded
             ('درخت', 0, wiki(S3, S4, S3 + ' ' + S4, S1 + ' و در منابع دیگر نیز آمده است.', 'ادامه ' * 400 + 'متن.'), False),   # S1-copy must go
             ('کارون', 0, wiki(S4 * 1, S3 + ' و چیزهای دیگر هم هست.', S2[:-1] + ' و ادامه دارد.', 'دیگر ' * 400 + 'پایان.'), False),
             ('کوتاه', 0, wiki(S3), False),                                     # stub (< 1500 chars)
             ('بحث:درخت', 1, _big(S3), False),                                  # wrong namespace
             ('تغییر مسیر', 0, _big(S4), True),                                 # redirect
             ('Tehran', 0, 'English only', False)]
    xml = tmp_path / 'd.xml.bz2'; xml.write_bytes(bz2.compress(_xml(pages)))
    out, st = tmp_path / 'corpus.txt', tmp_path / 'st.json'
    F.main(['--out', str(out), '--exclude', articles_txt, '--stats', str(st), '--dump-file', str(xml), '--target-mb', '5', '--sample-frac', '1.0'])
    lines = [l.rstrip('\n') for l in open(out, encoding='utf-8')]
    s = json.load(open(st, encoding='utf-8'))
    assert s['ok'] and s['source'] == 'dump' and s['paragraphs'] == len(lines)
    assert S1 not in ' '.join(lines) and 'جمعیت زیادی دارد' not in ' '.join(lines)   # excluded article AND its copy elsewhere
    assert not any(S2 in l or S2[:40] in l for l in lines)
    assert S3 in lines and S4 in lines
    assert s['excluded_titles_found'] == ['ریاضیات', 'تهران'] or sorted(s['excluded_titles_found']) == sorted(['ریاضیات', 'تهران'])
    assert 'نبود_در_دامپ' in s['excluded_titles_not_found'] and 'ایران' in s['excluded_titles_not_found']
    assert s['paragraphs_dropped_eval_overlap'] >= 2 and s['stub_articles_skipped'] == 2          # 'کوتاه' and the English-only page
    assert len(set(lines)) == len(lines)                                         # dedupe
    assert all(l == F.C.clean_text(l) and len(l) >= 80 for l in lines)           # same format/cleaning as the old corpus


def test_dump_stops_at_target_size(tmp_path, articles_txt):
    pages = [(f'مقاله {i}', 0, wiki(*[S3[:-1] + f' شماره {i} و {j}.' for j in range(40)]), False) for i in range(60)]
    xml = tmp_path / 'd.xml'; xml.write_bytes(_xml(pages))
    out, st = tmp_path / 'c.txt', tmp_path / 's.json'
    F.main(['--out', str(out), '--exclude', articles_txt, '--stats', str(st), '--dump-file', str(xml), '--target-mb', '0.02', '--sample-frac', '1.0', '--extra-scan-minutes', '0'])
    s = json.load(open(st, encoding='utf-8'))
    assert s['reached_target'] and 0.02 <= s['mb'] < 0.06 and s['articles_used'] < 60


def test_ground_truth_dir_filters_paragraphs(tmp_path, articles_txt):
    gt = tmp_path / 'gt'; gt.mkdir(); (gt / 'a.txt').write_text(S4 + '\n', encoding='utf-8')
    pages = [('الف', 0, wiki(S3, S4, 'متن ' * 400 + 'پایان.'), False)]
    xml = tmp_path / 'd.xml'; xml.write_bytes(_xml(pages)); out, st = tmp_path / 'c.txt', tmp_path / 's.json'
    F.main(['--out', str(out), '--exclude', articles_txt, '--stats', str(st), '--dump-file', str(xml), '--sample-frac', '1.0', '--ground-truth', str(gt)])
    text = open(out, encoding='utf-8').read()
    assert S3 in text and S4 not in text


def test_hf_parquet_path(tmp_path, articles_txt):
    pa = pytest.importorskip('pyarrow'); import pyarrow.parquet as pq
    rows = [('تهران', _big(S1).replace('{{جعبه اطلاعات|الف=ب|ج={{تو در تو}}}}\n', '').replace('\n\n', '\n')),
            ('کارون', '\n'.join([S4, 'عنوان کوتاه', S3 + ' و چیزهای دیگر هم هست.', 'دیگر ' * 400 + 'پایان.'])),
            ('درخت', '\n'.join([S3, S1[:-1] + ' و در جای دیگر آمده است.', 'ادامه ' * 400 + 'پایان.']))]
    t = pa.table({'title': [r[0] for r in rows], 'text': [r[1] for r in rows]})
    pq.write_table(t, tmp_path / 'x.parquet', row_group_size=1)
    out, st = tmp_path / 'c.txt', tmp_path / 's.json'
    F.main(['--out', str(out), '--exclude', articles_txt, '--stats', str(st), '--parquet', str(tmp_path / 'x.parquet'), '--target-mb', '5'])
    s = json.load(open(st, encoding='utf-8')); text = open(out, encoding='utf-8').read()
    assert s['source'] == 'hf' and s['dump_date'] == '2023-11-01'
    assert 'تهران پایتخت' not in text and 'جمعیت زیادی دارد' not in text         # pinned article + copy excluded
    assert S4 in text and 'عنوان کوتاه' not in text
    assert s['excluded_titles_found'] == ['تهران']


def test_all_sources_failing_writes_stats_and_exits(tmp_path, articles_txt):
    st = tmp_path / 's.json'; bad = tmp_path / 'empty.xml'; bad.write_bytes(_xml([]))
    with pytest.raises(SystemExit):
        F.main(['--out', str(tmp_path / 'c.txt'), '--exclude', articles_txt, '--stats', str(st), '--dump-file', str(bad)])
    assert json.load(open(st))['ok'] is False
