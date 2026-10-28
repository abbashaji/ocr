"""Exporters. Labels are stored at full fidelity; presets are applied HERE only.

presets
  folded    exactly ft/common.py clean_text + LABEL_MAP (current recipe; the stock fas unicharset lacks the dropped marks)
  distinct  clean_text-style normalisation (ya/kaf, Arabic-Indic digits, spaces, quotes) but KEEPS the ezafe mark U+0654 and the
            Persian punctuation ، ٫ ٬ ٪ (no LABEL_MAP, harakat other than U+0654 are removed)
formats
  tesseract <id>.png + <id>.gt.txt next to each other, one directory per split
  paddle    <split>.txt with "images/<id>.png<TAB>label" (PaddleOCR rec format) + images/ + dict.txt
"""
import csv, io, json, os, random, re, shutil, sys, tarfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))              # ft/ -> common.py
import common as C

PRESETS = ('folded', 'distinct')
_HARAKAT_NO_EZAFE = re.compile('[\u064b-\u0653\u0655-\u065f\u0670]')

def distinct_text(s):
    s = s.translate(C._NORM).translate(C._ARABIC_INDIC)
    s = _HARAKAT_NO_EZAFE.sub('', s)
    return re.sub(r'[ \t]+', ' ', s).strip()

def folded_text(s):
    return C.to_label(C.clean_text(s))

def apply_preset(s, preset):
    if preset == 'folded': return folded_text(s)
    if preset == 'distinct': return distinct_text(s)
    raise ValueError(preset)

def select(records, splits=('train',), tiers=('GOLD', 'GOLD_A'), preset='folded', allowed=None):
    """Filter manifest records; drops lines whose preset label is empty or has chars outside `allowed` (folded only)."""
    out = []
    for r in records:
        if r['split'] not in splits or r['tier'] not in tiers: continue
        t = apply_preset(r['label'], preset)
        if not t: continue
        if allowed is not None and preset == 'folded' and not C.keep_line(t, allowed): continue
        out.append((r, t))
    return out

def write_tesseract(items, images_dir, out_dir, preset_dir_by_split=True, augment=0, seed=0):
    n = 0
    for r, t in items:
        d = os.path.join(out_dir, r['split']) if preset_dir_by_split else out_dir
        os.makedirs(d, exist_ok=True)
        src = os.path.join(images_dir, r['id'] + '.png')
        shutil.copyfile(src, os.path.join(d, r['id'] + '.png'))
        open(os.path.join(d, r['id'] + '.gt.txt'), 'w', encoding='utf-8').write(t + '\n'); n += 1
        if augment and r['split'] == 'train':
            import augment as A
            from PIL import Image
            im = Image.open(src).convert('L')
            for k in range(1, augment + 1):
                aug = A.augment(im, random.Random(f'{seed}:{r["id"]}:{k}'))
                aug.save(os.path.join(d, f'{r["id"]}_aug{k}.png'))
                open(os.path.join(d, f'{r["id"]}_aug{k}.gt.txt'), 'w', encoding='utf-8').write(t + '\n'); n += 1
    return n

def write_paddle(items, images_dir, out_dir):
    os.makedirs(os.path.join(out_dir, 'images'), exist_ok=True)
    files, chars = {}, set()
    for r, t in items:
        shutil.copyfile(os.path.join(images_dir, r['id'] + '.png'), os.path.join(out_dir, 'images', r['id'] + '.png'))
        files.setdefault(r['split'], []).append(f"images/{r['id']}.png\t{t}")
        chars.update(t)
    for sp, ls in files.items(): open(os.path.join(out_dir, f'{sp}.txt'), 'w', encoding='utf-8').write('\n'.join(ls) + '\n')
    open(os.path.join(out_dir, 'dict.txt'), 'w', encoding='utf-8').write('\n'.join(sorted(c for c in chars if c != ' ')) + '\n')
    return sum(len(v) for v in files.values())

def write_manifest(records, path_jsonl, path_csv, allowed=None):
    cols = ['id', 'work', 'split', 'tier', 'sim', 'margin', 'page', 'revid', 'page_title', 'licence', 'commons_url', 'wikisource_url',
            'label_full', 'label_folded', 'label_distinct', 'w', 'h', 'y0', 'y1', 'deskew', 'dpi', 'quality', 'retrieved']
    rows = []
    for r in records:
        rows.append(dict(id=r['id'], work=r['work'], split=r['split'], tier=r['tier'], sim=r['sim'], margin=r['margin'], page=r['page'],
                         revid=r['revid'], page_title=r['page_title'], licence=r['licence'], commons_url=r['commons_url'],
                         wikisource_url=r['wikisource_url'], label_full=r['label'], label_folded=folded_text(r['label']),
                         label_distinct=distinct_text(r['label']), w=r['w'], h=r['h'], y0=r['y0'], y1=r['y1'], deskew=r['deskew'],
                         dpi=r['dpi'], quality=r['quality'], retrieved=r.get('retrieved', '')))
    with open(path_jsonl, 'w', encoding='utf-8') as f:
        for x in rows: f.write(json.dumps(x, ensure_ascii=False) + '\n')
    with open(path_csv, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(rows)
    return rows

def tar_dir(src, dest):
    with tarfile.open(dest, 'w:gz', compresslevel=6) as t: t.add(src, arcname=os.path.basename(src))
