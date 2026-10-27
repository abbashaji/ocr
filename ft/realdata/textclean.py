"""Minimal markup cleaning of Wikisource Page: wikitext + comparison-form normalisation.

Ground truth is kept at FULL FIDELITY (ezafe mark, ZWNJ, original digits, original punctuation, original letters).
Only wiki markup is removed. Normalisation for *comparison* lives in cmp_form() and is never written as a label.
"""
import re, unicodedata

_PQ = re.compile(r'<pagequality[^>]*/>', re.I)
_NOINC = re.compile(r'<noinclude>.*?</noinclude>', re.S | re.I)
_TAGS_DROP = re.compile(r'<(ref|math|gallery|references|score|imagemap)\b.*?(</\1>|/>)', re.S | re.I)
_COMMENT = re.compile(r'<!--.*?-->', re.S)
_TAG = re.compile(r'</?[a-zA-Z][^>]*>')
_LINK2 = re.compile(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]')
_EXT = re.compile(r'\[(?:https?:)?//\S+\s+([^\]]*)\]')
_BOLD = re.compile(r"'{2,5}")
_HEAD = re.compile(r'^=+\s*(.*?)\s*=+\s*$', re.M)
_ENT = {'&nbsp;': ' ', '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&zwnj;': '\u200c', '&rlm;': '\u200f', '&lrm;': '\u200e'}

# structures that make a page unsuitable for line-level labelling (flagged, not silently kept)
COMPLEX = re.compile(r'\{\||<poem|<table|<math|\{\{\s*(?:جدول|table|شعر|poem|ستون|columns|multicol)', re.I)

def body_of(wikitext):
    """Return (body_text, flags). Header/footer in <noinclude> and the pagequality tag are removed."""
    flags = []
    m = re.search(r'<pagequality\s+level="(\d)"', wikitext)
    level = int(m.group(1)) if m else None
    t = _PQ.sub('', wikitext)
    t = _NOINC.sub('', t)
    t = _COMMENT.sub('', t)
    if COMPLEX.search(t): flags.append('complex_layout')
    t = _TAGS_DROP.sub('', t)
    # templates: drop simple ones, keep the text of a few common wrappers
    for _ in range(4):
        t = re.sub(r'\{\{[^{}]*\}\}', lambda mm: '', t)
    t = _LINK2.sub(r'\1', t)
    t = _EXT.sub(r'\1', t)
    t = _HEAD.sub(r'\1', t)
    t = _BOLD.sub('', t)
    t = _TAG.sub('', t)
    for k, v in _ENT.items(): t = t.replace(k, v)
    t = t.replace('\r', '')
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\n{3,}', '\n\n', t).strip()
    if '{{' in t or '}}' in t or '[[' in t: flags.append('markup_left')
    return t, level, flags

_FOLD = {'ي': 'ی', 'ك': 'ک', 'ة': 'ه', 'ۀ': 'ه', 'أ': 'ا', 'إ': 'ا', 'ؤ': 'و', 'ى': 'ی', 'ە': 'ه'}
_DIG = {c: str(i) for i, c in enumerate('۰۱۲۳۴۵۶۷۸۹')}
_DIG.update({c: str(i) for i, c in enumerate('٠١٢٣٤٥٦٧٨٩')})
def cmp_form(s):
    """Letters/digits only, folded: ya/kaf variants, digit scripts, no diacritics, no ZWNJ, no spaces, no punctuation."""
    out = []
    for ch in unicodedata.normalize('NFKC', s):
        ch = _FOLD.get(ch, ch)
        ch = _DIG.get(ch, ch)
        cat = unicodedata.category(ch)
        if cat[0] in 'LN' and ch not in '\u0640':
            out.append(ch)
    return ''.join(out)
