#!/usr/bin/env python3
"""Persian image -> text, offline (Tesseract fas fine-tuned + pipeline v2).
usage: ocr_cli.py IMAGE [--model DIR_WITH_fas.traineddata] [--lex] [--keep-markers]
  default  : no lexicon step ("v2raw"): best on clean, full-size screenshots (zoom 100%)
  --lex    : lexicon correction ("v2lex"): better on small / low-quality images (zoom 75%, JPEG)
  Citation markers like [۱۱] are removed by default (geometrically); --keep-markers disables that.
Needs: tesseract >= 5 on PATH, pip install pillow numpy rapidfuzz wordfreq"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('image'); ap.add_argument('--model', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model'))
ap.add_argument('--lex', action='store_true'); ap.add_argument('--keep-markers', action='store_true')
a = ap.parse_args()
os.environ['OCR_TESSDIR'] = a.model
import pipeline2 as Q
from PIL import Image
CFG = dict(alpha=1.5, margin=0.3, floor=2.5, guard=2, conf_skip=90, sub_other=2.0, indel=2.0, max_cost=2.0, target=2.5)
if not a.lex: CFG['conf_skip'] = 0
lines = Q.recognize_tok(Image.open(a.image), markers=not a.keep_markers)
sys.stdout.reconfigure(encoding='utf-8'); print(Q.render(lines, **CFG))
