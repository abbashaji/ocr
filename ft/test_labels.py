"""Tests for the label schemes (ft/common.py), the ezafe injection, the real-line labels and ft/eval_labels.py.
Run: python -m pytest ft/test_labels.py -q   (the unicharset test needs tesseract + its training tools and network access; it skips otherwise)"""
import os, random, shutil, sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import eval_labels as E

@pytest.fixture(autouse=True)
def folded_after():
    yield
    C.set_scheme('folded')

SAMPLE = 'در سدهٔ پانزدهم، ۱٫۶۴ و ۵٪ و ۵% و ۳۴٬۵۰۰ و خانۀ بزرگ; ـ'

def test_folded_is_the_old_recipe():
    C.set_scheme('folded')
    t = C.to_label(C.clean_text(SAMPLE))
    assert 'ٔ' not in t and 'ۀ' not in t
    assert t.startswith('در سده پانزدهم, ۱.۶۴ و ۵# و ۵# و ۳۴,۵۰۰ و خانه بزرگ؛')
    assert C.LABEL_MAP['،'] == ',' and C.LABEL_MAP['٪'] == '#'

def test_distinct_keeps_the_classes_but_not_the_mark():
    C.set_scheme('distinct')
    t = C.to_label(C.clean_text(SAMPLE))
    assert '،' in t and '٫' in t and '٬' in t and '٪' in t and '%' not in t
    assert 'ٔ' not in t and 'ۀ' not in t

def test_distinct_ezafe_keeps_mark_after_heh_only():
    C.set_scheme('distinct_ezafe')
    t = C.clean_text(SAMPLE)
    assert t.count('هٔ') == 2 and 'ۀ' not in t           # سدهٔ and خانۀ -> خانهٔ
    assert C.clean_text('کتابٔ نو') == 'کتاب نو'           # the mark after other letters is dropped
    assert C.clean_text('کُتُب') == 'کتب'                  # other harakat are still removed
    assert C.to_label(t).count('٪') == 2                   # % folded into ٪, nothing else mapped

def test_set_scheme_rejects_unknown():
    with pytest.raises(ValueError): C.set_scheme('nope')

def test_keep_line_needs_the_new_class_in_the_unicharset():
    C.set_scheme('distinct')
    assert not C.keep_line('۱٫۶۴', set('۱۶۴'))              # new class missing -> line dropped (stock unicharset)
    assert C.keep_line('۱٫۶۴', set('۱۶۴٫'))
    C.set_scheme('folded')
    assert C.keep_line('۱٫۶۴', set('۱۶۴.'))                 # folded: placeholder label exists

def test_plain_is_scheme_independent():
    for s in ('a b', 'در سال ۱۳۸۰'): assert C.is_plain(s)
    for s in ('a،b', '۵٪', '۱٫۶', '٬', 'سدهٔ', '5%'): assert not C.is_plain(s)

def test_inject_ezafe():
    r = random.Random(0)
    out = C.inject_ezafe('خانه بزرگ سده ها نامه', r, p=1.0)
    assert out == 'خانهٔ بزرگ سدهٔ ها نامه'                   # last word never gets it, only heh-final words do
    assert C.inject_ezafe('خانه بزرگ', random.Random(0), p=0.0) == 'خانه بزرگ'

def test_real_labels():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import make_train_data as M
    raw = 'سدهٔ پانزدهم ۱٫۶۴'
    C.set_scheme('folded'); assert M.real_label(raw, 'folded') == 'سده پانزدهم ۱٫۶۴'      # folding of ٫ happens in write_box
    assert M.real_label(raw, 'distinct') == 'سده پانزدهم ۱٫۶۴'
    assert M.real_label(raw, 'distinct_ezafe') == raw

def test_eval_labels_metrics():
    ref = 'در سدهٔ پانزدهم ۱٫۶۴ و ۵٪ و ۳۴٬۵۰۰ و ۱،۲ و خانۀ بزرگ'
    assert E.seps(ref) == ['٫', '٪', '٬', '،'] and E.ezafe_words(ref) == ['سده', 'خانه']
    perfect = E.score([dict(_ref=ref, h=ref)], 'h')
    assert perfect['sep_f1'] == 100 and perfect['ezafe_f1'] == 100
    folded = E.score([dict(_ref=ref, h='در سده پانزدهم ۱.۶۴ و ۵# و ۳۴,۵۰۰ و ۱,۲ و خانه بزرگ')], 'h')
    assert folded['sep_f1'] == 0 and folded['ezafe_recall'] == 0 and folded['ezafe_precision'] is None
    half = E.score([dict(_ref=ref, h='در سدهٔ پانزدهم ۱٫۶۴ و ۵% و ۳۴٬۵۰۰ و ۱،۲ و خانه بزرگ')], 'h')   # % counts as ٪
    assert half['sep_f1'] == 100 and half['ezafe_recall'] == 50 and half['ezafe_precision'] == 100

@pytest.mark.skipif(not all(shutil.which(t) for t in ('combine_tessdata', 'unicharset_extractor', 'merge_unicharsets', 'combine_lang_model')), reason='tesseract training tools missing')
def test_extend_unicharset(tmp_path):
    import subprocess, urllib.request
    base = tmp_path / 'fas.traineddata'
    try: urllib.request.urlretrieve('https://github.com/tesseract-ocr/tessdata_best/raw/main/fas.traineddata', base)
    except Exception: pytest.skip('no network')
    subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extend_unicharset.py'), '--base', str(base), '--scheme', 'distinct_ezafe', '--out', str(tmp_path / 'ext')], check=True)
    chars = C.load_unicharset(str(tmp_path / 'ext' / 'ext.lstm-unicharset'))
    assert all(c in chars for c in '،٫٬٪\u0654') and len(chars) == 97   # 92 usable stock chars + 5 new (NULL, Joined, Broken are not counted by load_unicharset)
    assert (tmp_path / 'ext' / 'fas_ext.traineddata').stat().st_size > 1000
