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
    we, wn, le, ln, ne, nn, pe, pn = E.counts(REF, hyp)
    assert nn == 3 and ne == 2        # ۱٫۶۴ -> 64 and ۳۱ missing
    assert le == 0                    # the letter metric cannot see either error


def test_punctuation_sequence_catches_a_comma_for_a_full_stop():
    ok = E.counts(REF, REF)
    assert ok[4] == 0 and ok[6] == 0
    hyp = REF[:-1] + '،'
    assert E.counts(REF, hyp)[6] == 1
