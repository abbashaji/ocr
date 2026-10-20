import difflib, json
import numpy as np
import postproc as P, functools
P.candidates = functools.lru_cache(maxsize=None)(P.candidates)
import pipeline2 as Q
from lib import *
CFG = dict(alpha=1.5, margin=0.3, floor=2.5, guard=2, conf_skip=90, sub_other=2.0, indel=2.0, max_cost=2.0, target=2.5)
imgs = {k: Image.open(v).convert('RGB') for k, v in SAMPLES.items()}
rw = B.words(REF)
def spans(h):
    hw = B.words(h); sm = difflib.SequenceMatcher(None, rw, hw, autojunk=False)
    return [(' '.join(rw[i1:i2]), ' '.join(hw[j1:j2])) for t,i1,i2,j1,j2 in sm.get_opcodes() if t != 'equal']
if __name__ == '__main__':
    res = {}
    for k in imgs:
        lines = Q.recognize_tok(imgs[k]); save_cache()
        raw = '\n'.join(' '.join(w for w, _ in ln) for ln in lines); fin = Q.render(lines, **CFG)
        res[k] = (raw, fin)
        for name, h in (('raw-medoid', raw), ('final', fin)):
            l, w = sc(REF, h); e1, e2, n1, n2 = P.para_errors(REF_P, h)
            print(f'{k:6s} {name:10s} letter {l:6.2f} word {w:6.2f}   errors p1={e1}/{n1} p2={e2}/{n2}')
        print('   remaining:', spans(fin))
    json.dump({k: v[1] for k, v in res.items()}, open('client_final.json', 'w'), ensure_ascii=False, indent=1)
