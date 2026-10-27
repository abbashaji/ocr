"""Assign ground truth to OCR'd lines by monotone, edit-distance based alignment against page text.

Label = substring of the human text (never OCR text). Tiers:
  GOLD    strong, unambiguous alignment (similarity >= GOLD_SIM) with margin over the next best candidate
  GOLD_A  anchored: no strong local match, but the text gap between two GOLD neighbours is one consistent line
  SILVER  weaker alignment (SILVER_SIM <= similarity < GOLD_SIM) or anchored with weaker agreement
"""
import re
from rapidfuzz import fuzz
from rapidfuzz.distance import Levenshtein as Lev
from textclean import cmp_form

GOLD_SIM = 0.93
SILVER_SIM = 0.80
MARGIN = 0.08
MIN_CHARS = 8

def tokens_with_cmp(gt):
    """Split ground truth on whitespace -> list of (token, cmp_form(token))."""
    return [(t, cmp_form(t)) for t in gt.split() if t]

def _layout(toks):
    """Concatenated comparison string and, per token, its (start, end) offsets in it."""
    pos, s = [], []
    n = 0
    for _, c in toks:
        pos.append((n, n + len(c))); s.append(c); n += len(c)
    return ''.join(s), pos

def _tok_span(pos, a, b):
    """Token indices whose comparison text lies mostly inside [a, b). Boundary tokens need >= 60% overlap."""
    first = last = None
    for i, (s, e) in enumerate(pos):
        if e <= s: continue
        ov = min(e, b) - max(s, a)
        if ov / (e - s) >= 0.6:
            if first is None: first = i
            last = i
    return first, last

def _sim(a, b):
    return Lev.normalized_similarity(a, b) if (a or b) else 0.0

def best_match(line_c, G, lo, hi):
    """Best substring of G[lo:hi] for line_c. Returns (start, end, sim) in G coordinates."""
    if not line_c or hi - lo < 3: return None
    seg = G[lo:hi]
    if len(seg) <= len(line_c) + 2:                      # haystack not longer than the needle: compare directly
        return (lo, hi, _sim(line_c, seg))
    al = fuzz.partial_ratio_alignment(line_c, seg)
    if al is None: return None
    a, b = al.dest_start, al.dest_end
    # partial_ratio aligns the shorter string; widen the window to the line length and refine boundaries
    n = len(line_c)
    best = None
    for da in range(-2, 3):
        for db in range(-2, 3):
            s0, e0 = max(0, a + da), min(len(seg), b + db)
            if e0 - s0 < 3: continue
            sc = _sim(line_c, seg[s0:e0])
            if best is None or sc > best[2]: best = (lo + s0, lo + e0, sc)
    return best

def align_page(ocr_lines, gt, window_factor=3.0):
    """ocr_lines: list of dicts with 'text'. gt: page ground truth (full fidelity).
    Returns list (same order) of dicts: label, sim, margin, tier, tok_range, or tier=None when rejected."""
    toks = tokens_with_cmp(gt)
    G, pos = _layout(toks)
    out = [dict(label=None, sim=0.0, margin=0.0, tier=None, span=None, reason='') for _ in ocr_lines]
    if not G:
        for o in out: o['reason'] = 'no_gt'
        return out
    ptr = 0  # monotone pointer in G
    for i, ln in enumerate(ocr_lines):
        lc = cmp_form(ln['text'])
        o = out[i]
        if len(lc) < MIN_CHARS: o['reason'] = 'short'; continue
        lo = ptr
        hi = min(len(G), ptr + int(len(lc) * window_factor) + 120)
        m = best_match(lc, G, lo, hi)
        if not m: o['reason'] = 'nomatch'; continue
        a, b, sc = m
        # ambiguity: best match outside +-len(lc) of the best one, anywhere ahead of ptr in the whole page
        mm = 0.0
        half = len(lc) // 2
        for (l2, h2) in ((lo, max(lo, a - half)), (min(len(G), b - half), len(G))):
            if h2 - l2 >= 6:
                m2 = best_match(lc, G, l2, h2)
                if m2: mm = max(mm, m2[2])
        margin = sc - mm
        f, l = _tok_span(pos, a, b)
        if f is None: o['reason'] = 'nospan'; continue
        label = ' '.join(t for t, _ in toks[f:l + 1])
        lab_c = ''.join(c for _, c in toks[f:l + 1])
        sim = _sim(lc, lab_c)
        o.update(label=label, sim=round(sim, 4), margin=round(margin, 4), span=(f, l))
        if margin < MARGIN: o['reason'] = 'ambiguous'; continue
        if sim >= GOLD_SIM: o['tier'] = 'GOLD'
        elif sim >= SILVER_SIM: o['tier'] = 'SILVER'
        else: o['reason'] = 'low_sim'; continue
        ptr = pos[l][1] if o['tier'] == 'GOLD' else max(ptr, pos[f][0])
    # anchored interpolation: single rejected line between two GOLD neighbours
    for i in range(1, len(out) - 1):
        o = out[i]
        if o['tier'] or o['reason'] in ('short', 'no_gt'): continue
        p, n = out[i - 1], out[i + 1]
        if p['tier'] == 'GOLD' and n['tier'] == 'GOLD':
            f, l = p['span'][1] + 1, n['span'][0] - 1
            if f <= l:
                lab_c = ''.join(c for _, c in toks[f:l + 1])
                lc = cmp_form(ocr_lines[i]['text'])
                ratio = len(lab_c) / max(1, len(lc))
                sim = _sim(lc, lab_c)
                if 0.7 <= ratio <= 1.4 and sim >= 0.6:
                    o.update(label=' '.join(t for t, _ in toks[f:l + 1]), sim=round(sim, 4), span=(f, l),
                             tier='GOLD_A' if sim >= SILVER_SIM else 'SILVER', reason='anchored')
    return out
