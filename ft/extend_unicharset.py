#!/usr/bin/env python3
"""Build a traineddata whose unicharset = stock fas unicharset + the extra classes of a label scheme (see common.NEW_CLASSES).

usage: extend_unicharset.py --base tess/fas.traineddata --scheme distinct|distinct_ezafe --out ext_dir
writes  <out>/fas_ext.traineddata  (unicharset + recoder only, NO lstm network: lstmtraining adds the weights)
        <out>/ext.lstm-unicharset  (merged unicharset; used by make_train_data.py to filter lines)
Old class ids are kept (checked), the new classes are appended, so the stock lstm-*-dawg files stay valid: train.sh puts them back into
the finished model (combine_tessdata -o).
Tools: combine_tessdata, unicharset_extractor, merge_unicharsets, combine_lang_model (package tesseract-ocr / libtesseract training tools).
combine_lang_model insists on <script_dir>/radical-stroke.txt (a CJK table that is not used for Persian); it is downloaded once
from tesseract-ocr/langdata_lstm unless RADICAL_STROKE points to a copy.
"""
import argparse, os, shutil, subprocess, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

def run(*cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0: sys.exit(f'FAILED {" ".join(cmd)}\n{r.stdout[-800:]}\n{r.stderr[-800:]}')
    return r

def ids(path):
    return [l.split(' ')[0] for l in open(path, encoding='utf-8').read().split('\n')[1:] if l]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True); ap.add_argument('--scheme', required=True, choices=[s for s in C.SCHEMES if s != 'folded'])
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    out = os.path.abspath(a.out); os.makedirs(out, exist_ok=True); w = os.path.join(out, 'work'); os.makedirs(w, exist_ok=True)
    run('combine_tessdata', '-u', os.path.abspath(a.base), os.path.join(w, 'base.'))
    base_uni = os.path.join(w, 'base.lstm-unicharset')
    have = set(ids(base_uni)); new = [c for c in C.NEW_CLASSES[a.scheme] if c not in have]
    print('classes to add:', [f'U+{ord(c):04X}' for c in new], flush=True)
    box = os.path.join(w, 'newchars.box'); open(box, 'w', encoding='utf-8').write(''.join(f'{c} 0 0 1 1 0\n' for c in new))
    run('unicharset_extractor', '--output_unicharset', os.path.join(w, 'new.unicharset'), '--norm_mode', '1', box)
    merged = os.path.join(out, 'ext.lstm-unicharset')
    run('merge_unicharsets', base_uni, os.path.join(w, 'new.unicharset'), merged)
    old, mer = ids(base_uni), ids(merged)
    if mer[:len(old)] != old: sys.exit('merged unicharset changed the ids of the old classes; refusing')
    missing = [c for c in new if c not in mer]
    if missing: sys.exit(f'classes missing after merge: {missing}')
    script = os.path.join(w, 'script'); os.makedirs(script, exist_ok=True)
    rs = os.environ.get('RADICAL_STROKE')
    if rs and os.path.exists(rs): shutil.copy(rs, os.path.join(script, 'radical-stroke.txt'))
    else: urllib.request.urlretrieve('https://raw.githubusercontent.com/tesseract-ocr/langdata_lstm/main/radical-stroke.txt', os.path.join(script, 'radical-stroke.txt'))
    lang = os.path.join(w, 'lang'); os.makedirs(lang, exist_ok=True)
    run('combine_lang_model', '--input_unicharset', merged, '--script_dir', script, '--output_dir', lang, '--lang', 'fas')   # fas.traineddata in lang/fas/
    src = os.path.join(lang, 'fas', 'fas.traineddata')
    if not os.path.exists(src): sys.exit('combine_lang_model did not produce ' + src)
    shutil.copy(src, os.path.join(out, 'fas_ext.traineddata'))
    print(f'ok: {len(mer)} classes (stock {len(old)}), wrote {out}/fas_ext.traineddata and ext.lstm-unicharset', flush=True)

if __name__ == '__main__':
    main()
