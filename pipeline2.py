"""v2: keeps per-word confidence; guarded lexicon correction."""
import re, functools
from rapidfuzz.distance import Levenshtein as Lev
from lines import *
import postproc as P

TARGETS = (28, 32, 36, 40, 44, 48, 56)
norm = lambda s: ' '.join(B.base(s).split())

def recognize_tok(im, targets=TARGETS):
    """-> list of lines; each line = list of (token, conf) from the medoid scale."""
    g = to_gray(im, 'L'); out = []
    for c in crops(g, segment_lines(g)):
        cands = [tess_tsv(pad_white(scale(c, T / c.height), 12), 7) for T in targets]
        n = [norm(t) for t, _ in cands]
        best = min(range(len(n)), key=lambda i: sum(Lev.distance(n[i], n[j]) for j in range(len(n))))
        out.append(cands[best][1])
    return out

LET = r'ء-يٱ-ۓ'
def finalize_tok(t):
    t = re.sub(r'(?<=[' + LET + r'])ء(?=[^' + LET + r']*$)', '،', t)     # glued "ء" at word end -> comma
    t = re.sub(r'(?<=[' + LET + r']),', '،', t)
    return t.replace('?', '؟')

SUF_LIGHT = ['ها', 'های', 'هایی', 'ترین', 'تر', 'ان', 'ات']; PRE_LIGHT = ['می', 'نمی']
SUF = ['ها', 'های', 'هایی', 'ی', 'ایی', 'ان', 'ات', 'ین', 'تر', 'ترین', 'ک', 'م', 'ت', 'ش', 'ام', 'اش', 'مان', 'تان', 'شان', 'ند', 'ید', 'یم', 'ه', 'ای']
PRE = ['می', 'نمی', 'بی', 'نا']
def is_known(w, target, mode=1):
    if P.zipf(w) >= target: return True
    pres, sufs, minstem = (PRE, SUF, 3) if mode == 1 else (PRE_LIGHT, SUF_LIGHT, 4)
    for pre in [''] + pres:
        if pre and not w.startswith(pre): continue
        for suf in [''] + sufs:
            if suf and not w.endswith(suf): continue
            stem = w[len(pre):len(w) - len(suf)] if suf else w[len(pre):]
            if len(stem) >= minstem and (pre or suf) and P.zipf(stem) >= target + 0.5: return True
    return False

@functools.lru_cache(maxsize=None)
def corr_word(w, alpha, margin, floor, max_cost, target, guard, sub_other, indel):
    if len(w) < 3: return w
    if guard and is_known(w, target, guard): return w
    if not guard and P.zipf(w) >= target: return w
    best, bs = w, P.zipf(w)
    for c, cost in P.candidates(w, max_cost, sub_other, indel).items():
        zc = P.zipf(c)
        if zc < floor: continue
        s = zc - alpha * cost
        if s > bs + margin: best, bs = c, s
    return best

def correct_tok(tok, conf, alpha=1.5, margin=0.3, floor=2.5, max_cost=2.0, target=2.5, guard=1, conf_skip=101, sub_other=2.0, indel=1.5):
    if conf >= conf_skip: return tok
    def sub(m):
        w = m.group(0); wn = B.base(w)
        if wn != w or not re.fullmatch('[' + P.ALPHA + ']+', wn): return w
        return corr_word(wn, alpha, margin, floor, max_cost, target, guard, sub_other, indel)
    return P.TOKEN.sub(sub, tok)

D = '0-9۰-۹'
def restore_placeholders(t):
    """fine-tune trains ، ٬ ٫ ٪ onto the existing classes , , . # (see ft/common.py LABEL_MAP); restore by context."""
    t = re.sub(r'(?<=[' + D + r'])\.(?=[' + D + r'])', '٫', t)                 # 1.64 -> ۱٫۶۴
    t = re.sub(r'(?<=[' + D + r']),(?=[' + D + r']{3}(?![' + D + r']))', '٬', t)  # 12,345 -> thousands separator
    t = t.replace(',', '،')
    return t.replace('#', '٪')

def render(lines, **cfg):
    out = []
    for ln in lines:
        out.append(restore_placeholders(' '.join(correct_tok(finalize_tok(t), c, **cfg) for t, c in ln)))
    return '\n'.join(out)
