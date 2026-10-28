#!/usr/bin/env python3
"""Extra metrics for the label-design experiment, computed from the hypotheses.json written by ft/evaluate.py.

  sep F1    the Persian separator/percent classes ، ٫ ٬ ٪ as a sequence (LCS-based F1, like punct F1) - was the RIGHT class output?
  ezafe F1  the words that carry the ezafe mark (سدهٔ, also written ۀ): LCS over the list of such words; a missing mark or a mark on the
            wrong word costs. Recall = share of reference ezafe words recovered, precision = share of hypothesis ezafe words that are right.
  ezafe-free words are compared without the mark, so a model that never outputs it scores recall 0 but is not punished elsewhere.

usage: eval_labels.py <results_dir_with_hypotheses.json> [--tag ft|base] [--out labels.json]
Engines that are scored: every key of a hypothesis row that is a text ('plain', 'v2raw', 'v2lex', 'ocr2/auto', ...); the view is raw (markers in).
"""
import argparse, json, os, re, sys, unicodedata
from rapidfuzz.distance import LCSseq

EZ = '\u0654'
SEP = '،٫٬٪'

def norm(s):
    s = s.replace('ۀ', 'ه' + EZ).replace('٪', '٪').replace('%', '٪')                     # precomposed ezafe, ASCII percent
    s = re.sub('[\u064b-\u0653\u0655-\u065f\u0670]', '', s)                                # other harakat are never scored
    return s

def seps(s):
    return [c for c in norm(s) if c in SEP]

def ezafe_words(s):
    """words (letters only, mark removed) that carry the ezafe mark"""
    out = []
    for w in re.split(r'[\s\u200c]+', norm(s)):
        if EZ in w:
            out.append(''.join(c for c in w if unicodedata.category(c).startswith('L')))
    return out

def f1(lcs, nr, nh):
    return round(100 * 2 * lcs / (nr + nh), 2) if nr + nh else None

def score(rows, eng):
    t = dict(sep=[0, 0, 0], ez=[0, 0, 0], n=0)
    for r in rows:
        if eng not in r: continue
        ref, hyp = r['_ref'], r[eng]
        if isinstance(hyp, dict): continue
        a, b = seps(ref), seps(hyp); t['sep'][0] += LCSseq.similarity(a, b); t['sep'][1] += len(a); t['sep'][2] += len(b)
        a, b = ezafe_words(ref), ezafe_words(hyp); t['ez'][0] += LCSseq.similarity(a, b); t['ez'][1] += len(a); t['ez'][2] += len(b); t['n'] += 1
    s, e = t['sep'], t['ez']
    return dict(n_images=t['n'], sep_f1=f1(*s), ref_seps=s[1], hyp_seps=s[2], ezafe_f1=f1(*e), ezafe_recall=round(100 * e[0] / e[1], 2) if e[1] else None,
                ezafe_precision=round(100 * e[0] / e[2], 2) if e[2] else None, ref_ezafe=e[1], hyp_ezafe=e[2])

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('dir'); ap.add_argument('--tag', default='ft'); ap.add_argument('--out', default=None)
    a = ap.parse_args()
    H = json.load(open(os.path.join(a.dir, 'hypotheses.json'), encoding='utf-8'))
    res = {}
    for sname, items in H.items():
        if sname == 'synth': continue
        rows = [dict(it[a.tag], _ref=it['ref'], _name=it['name']) for it in items if a.tag in it]
        groups = {'all': rows}
        for z in ('z100', 'z75', 'z50'): groups[z] = [r for r in rows if f'_{z}.' in r['_name']]
        engs = sorted({k for r in rows for k in r if k not in ('sec', 'auto_picked', '_ref', '_name') and isinstance(r[k], str)})
        for g, rs in groups.items():
            if not rs: continue
            for e in engs: res.setdefault(sname, {}).setdefault(g, {})[e] = score(rs, e)
    out = a.out or os.path.join(a.dir, 'labels.json'); json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1)
    for sname, groups in res.items():
        for g, engs in groups.items():
            for e, m in engs.items(): print(f'{sname}/{g}/{e}: sep F1 {m["sep_f1"]} ({m["ref_seps"]} ref) | ezafe F1 {m["ezafe_f1"]} recall {m["ezafe_recall"]} precision {m["ezafe_precision"]} ({m["ref_ezafe"]} ref)')

if __name__ == '__main__':
    main()
