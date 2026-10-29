#!/usr/bin/env python3
"""Rename the borrowed alias classes of a finished model (see common.ALIAS_MAP): the model then outputs ، ٫ ٬ ٪ (and the ezafe mark).

usage: rename_classes.py fas_ft.traineddata [--ezafe]      (rewrites the file in place; other components are untouched)
Only the unicharset text changes: class ids, network, recoder and dictionaries stay valid. Properties/script/direction are those of the
real characters (as unicharset_extractor writes them), so Tesseract's RTL reordering treats them like the genuine characters.
"""
import argparse, os, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

# real char -> (properties, script, direction); taken from unicharset_extractor output for these characters
PROPS = {'،': (16, 'Common', 6), '٫': (16, 'Arabic', 5), '٬': (16, 'Arabic', 5), '٪': (16, 'Arabic', 4), C.EZAFE: (0, 'Inherited', 17)}

def rename(lines, ezafe):
    out = list(lines); done = []
    for target, alias in C.ALIAS_MAP.items():
        if target == C.EZAFE and not ezafe: continue
        hit = [i for i, l in enumerate(out) if i > 0 and l.split(' ')[0] == alias]
        if len(hit) != 1: sys.exit(f'alias U+{ord(alias):04X} found {len(hit)} times in the unicharset; refusing')
        f = out[hit[0]].split('\t')[0].split(' ')       # char props metrics script other_case direction mirror normed
        if len(f) != 8: sys.exit('unexpected unicharset line: ' + out[hit[0]])
        props, script, direction = PROPS[target]
        idx = f[4]
        f[0] = target; f[1] = str(props); f[3] = script; f[5] = str(direction); f[7] = target       # other_case (f[4]) and mirror (f[6]) stay = own id
        out[hit[0]] = ' '.join(f) + f'\t# {target} [{ord(target):x} ]'
        done.append((alias, target, idx))
    return out, done

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('model'); ap.add_argument('--ezafe', action='store_true')
    a = ap.parse_args(); model = os.path.abspath(a.model)
    with tempfile.TemporaryDirectory() as t:
        subprocess.run(['combine_tessdata', '-u', model, os.path.join(t, 'm.')], check=True, capture_output=True)
        p = os.path.join(t, 'm.lstm-unicharset')
        lines = open(p, encoding='utf-8').read().split('\n')
        new, done = rename(lines, a.ezafe)
        open(p, 'w', encoding='utf-8').write('\n'.join(new))
        subprocess.run(['combine_tessdata', '-o', model, p], check=True, capture_output=True)
    for al, tg, i in done: print(f'class {i}: U+{ord(al):04X} -> U+{ord(tg):04X}')

if __name__ == '__main__':
    main()
