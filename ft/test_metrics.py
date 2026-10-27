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
