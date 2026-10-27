"""Tests for the strict metrics of evaluate.py: numbers (with their separator) and punctuation.

Run from the repo root:  python -m pytest ft/test_metrics.py -q
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evaluate as E

REF = 'ایران با ۱٫۶۴ میلیون کیلومتر و ۹۲ میلیون نفر؛ منطقه و ۳۱ استان است.'


def test_numbers_fold_digit_shapes_but_not_a_wrong_separator():
    assert E.numbers(REF) == ['1.64', '92', '31']
    assert E.numbers('ایران با 1.64 و ٩٢ و ۳۱') == ['1.64', '92', '31']   # digit shapes are folded
    assert E.numbers('۱،۶۴') == ['1،64']                                    # a comma is not a decimal mark
    assert E.numbers('۱٬۶۴۰') == ['1,640']                                  # thousands separator


def test_a_dropped_number_and_a_dropped_digit_are_both_errors():
    hyp = 'ایران با ،۶۴ میلیون کیلومتر و ۹۲ میلیون نفر؛ منطقه و استان است.'
    we, wn, le, ln, nl, nr, nh, pl, pr, ph = E.counts(REF, hyp)
    assert (nr, nh, nl) == (3, 2, 1)  # ۱٫۶۴ became 64 and ۳۱ is missing: only ۹۲ matches
    assert le == 0                    # the letter metric cannot see either error


def test_extra_numbers_lower_the_f1_but_never_below_zero():
    hyp = REF + ' ۸ ۲۰۹ ۲۱ ۴۱۱ ۴۱۲'
    r = E.counts(REF, hyp)
    assert r[4] == 3 and r[6] == 8                       # all reference numbers found, five spurious
    assert 0 < E.f1(r[4], r[5], r[6]) < 100
    assert E.f1(0, 3, 9) == 0.0


def test_punctuation_sequence_catches_a_comma_for_a_full_stop():
    ok = E.counts(REF, REF)
    assert ok[4] == 3 and ok[7] == ok[8]
    hyp = REF[:-1] + '،'
    r = E.counts(REF, hyp)
    assert r[7] == r[8] - 1


def test_marker_regex_removes_citation_markers_in_any_bracket_order():
    for marker in ('[۱۶]', ']۱۶[', ']۲]]۱[', '(۱۲)', ']۴۱۱['):
        assert E.MARK.sub('', 'است.' + marker + ' تبریز') == 'است. تبریز'
    assert E.MARK.sub('', 'در سال (۱۳۹۹) آمد') == 'در سال (۱۳۹۹) آمد'    # a four-digit year in parentheses stays


# ---- product-engine (ocr2) plumbing: no Tesseract needed, outputs are faked ----
def _fake_outs(ref, texts):
    """One set, one image; texts = {engine key: hypothesis}. Two models share the same fake output."""
    row = {**texts, 'sec': {'auto': 3.0, 'raw': 2.0, 'lex': 4.0}}
    return {'base': {'s': [dict(row)]}, 'ft': {'s': [dict(row)]}}


def test_summarize_scores_ocr2_modes_and_reports_seconds_per_image():
    ref = REF
    sets = {'s': [('a.png', None, ref, 'z100')]}
    outs = _fake_outs(ref, {'ocr2/auto': ref, 'ocr2/raw': ref, 'ocr2/lex': ref.replace('۹۲', '۹]')})
    res = E.summarize(sets, outs)
    g = res['s']['all']
    assert g['ft/ocr2/auto/raw']['word_acc'] == 100.0 and g['ft/ocr2/auto/raw']['sec_per_image'] == 3.0
    assert g['ft/ocr2/lex/raw']['num_f1'] < 100                       # the lost number is visible
    assert g['ft/ocr2/lex/raw']['sec_per_image'] == 4.0
    assert 'ft/plain/raw' not in g                                      # legacy engines absent when not run
    assert res['s']['z100']['base/ocr2/raw/nomark']['n_images'] == 1


def test_markdown_has_an_ocr2_row_for_every_model_and_mode_without_empty_cells():
    sets = {'s': [('a.png', None, REF, 'z100')]}
    legacy = {'plain': REF, 'v2raw': REF, 'v2lex': REF}
    outs = _fake_outs(REF, {**legacy, 'ocr2/auto': REF, 'ocr2/raw': REF, 'ocr2/lex': REF})
    md = E.markdown(E.summarize(sets, outs))
    for tag in ('base', 'ft'):
        for mode in ('auto', 'raw', 'lex'):
            assert f'| {tag} | {mode} | 100.00 | 100.00 | 100.00 | 100.00 |' in md
    assert '| plain |' in md and '| ocr2/auto |' in md and 'nan' not in md and '-1' not in md


def test_markdown_works_with_only_ocr2_engines():
    sets = {'s': [('a.png', None, REF, 'z75')]}
    md = E.markdown(E.summarize(sets, _fake_outs(REF, {'ocr2/auto': REF, 'ocr2/raw': REF, 'ocr2/lex': REF})))
    assert 'Product engine (ocr2)' in md and '| ft | lex |' in md
