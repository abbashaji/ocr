#!/usr/bin/env python3
"""Build real browser-screenshot test sets with exact ground truth from fa.wikipedia articles.

usage: make_tests.py --articles ft/articles.txt --out tests [--blocks 3] [--base-url https://fa.wikipedia.org/wiki/]

For each pinned article: pick blocks of 1-2 consecutive body paragraphs (5-16 lines), screenshot them at
browser scale 100% (PNG), 75% (JPEG q60) and 50% (JPEG q40), and write the text of the SAME DOM elements as the
ground truth (citation markers sup.reference removed from the truth but still visible in the image, like the
client's samples; evaluate.py ignores marker residue in the OCR output). Split by article: even index -> tests/tune,
odd index -> tests/final (final is never used for tuning or training).

Diagnostics: for every article it prints how many paragraphs the page scan found and why each was rejected.
Exits with status 1 when no image was made at all.
"""
import argparse, collections, io, os, random, sys, time, urllib.parse
from PIL import Image

UA = 'ocr-finetune-bot/1.0 (test-image generation; https://github.com/abbashaji/ocr)'
ZOOMS = [(1.0, 'z100', 'png', None), (0.75, 'z75', 'jpg', 60), (0.5, 'z50', 'jpg', 40)]

# Body paragraphs: direct children of .mw-parser-output, or children of a <section> that is a direct child
# (newer Parsoid-style markup wraps paragraphs in sections). Both scripts use the same list so indices match.
JS_PARAS = """() => [...document.querySelectorAll('#mw-content-text .mw-parser-output p')].filter(p => {
  const par = p.parentElement;
  return par.classList.contains('mw-parser-output') ||
         (par.tagName === 'SECTION' && par.parentElement && par.parentElement.classList.contains('mw-parser-output'));
})"""
JS_SCAN = """() => {
  const clean = p => { const c = p.cloneNode(true);
    c.querySelectorAll('sup.reference,.mw-editsection,style,script,.noprint,sup.noprint').forEach(e => e.remove());
    return c.textContent.replace(/\\s+/g, ' ').trim(); };
  const ps = (%s)();
  const media = [...document.querySelectorAll('#mw-content-text *')].filter(e => e.matches('img,figure,table,svg') || getComputedStyle(e).float !== 'none')
    .map(e => [e, e.getBoundingClientRect()]).filter(([e, q]) => q.width > 4 && q.height > 4);
  return ps.map((p, i) => { const r = p.getBoundingClientRect(), lh = parseFloat(getComputedStyle(p).lineHeight) || 22;
    return {i, text: clean(p), lines: r.height / lh, w: r.width,
            ovl: media.some(([e, q]) => !p.contains(e) && q.left < r.right && q.right > r.left && q.top < r.bottom && q.bottom > r.top),
            odd: !!p.querySelector('sup:not(.reference),.Inline-Template,math,img,table,ruby'),
            next: !!(p.nextElementSibling && p.nextElementSibling === ps[i + 1])}; });
}""" % JS_PARAS
JS_RECT = """(i) => { const p = (%s)()[i];
  const r = p.getBoundingClientRect(); return {x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height}; }""" % JS_PARAS

# Floated photos / infoboxes / tables sit beside paragraphs. A crop of the paragraph then contains part of a photo, which
# breaks line segmentation (pipeline v2 returned empty text on such crops). Hide them before scanning and screenshotting;
# the ground truth is text only, so nothing else changes. Applied identically to every zoom page.
HIDE_CSS = ('#mw-content-text .thumb, #mw-content-text figure, #mw-content-text .infobox, #mw-content-text .sidebar, '
            '#mw-content-text .floatright, #mw-content-text .floatleft, #mw-content-text .tright, #mw-content-text .tleft, '
            '#mw-content-text .mw-parser-output > table, #mw-content-text .navbox, #mw-content-text .hatnote, '
            '#mw-content-text .mw-empty-elt, #siteNotice, #centralNotice, .mw-indicators '
            '{display:none !important} html{scroll-behavior:auto !important}')

def latin(s): return sum(c.isascii() and c.isalpha() for c in s)

def reject_reason(it):
    """None when the paragraph is usable, else a short reason"""
    if len(it['text']) < 250: return 'short'
    if it['odd']: return 'odd_markup'
    if it.get('ovl'): return 'overlap'
    if latin(it['text']) > 6: return 'latin'
    if not 3 <= it['lines'] <= 16: return 'lines'
    return None

def pick_blocks(items, n, rng):
    ok = [it for it in items if reject_reason(it) is None]
    rng.shuffle(ok); blocks = []; used = set()
    for it in ok:
        if it['i'] in used: continue
        blk = [it]
        nxt = next((x for x in items if x['i'] == it['i'] + 1), None)
        if it['next'] and nxt and nxt in ok and nxt['i'] not in used and it['lines'] + nxt['lines'] <= 16 and rng.random() < 0.6:
            blk.append(nxt)
        for b in blk: used.add(b['i'])
        blocks.append(blk)
        if len(blocks) >= n: break
    return blocks

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--articles', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--blocks', type=int, default=3); ap.add_argument('--base-url', default='https://fa.wikipedia.org/wiki/')
    ap.add_argument('--chrome', default=os.environ.get('CHROME_PATH')); ap.add_argument('--width', type=int, default=1100)
    ap.add_argument('--delay', type=float, default=1.0)
    ap.add_argument('--shot-timeout', type=int, default=120000, help='ms per screenshot')
    ap.add_argument('--min-article-frac', type=float, default=0.7, help='exit 1 if fewer articles than this fraction yield images')
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    titles = [t.strip() for t in open(a.articles, encoding='utf-8') if t.strip() and not t.startswith('#')]
    for s in ('tune', 'final'): os.makedirs(os.path.join(a.out, s), exist_ok=True)
    made, missing, ok_articles = 0, [], 0
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=a.chrome) if a.chrome else pw.chromium.launch()
        ctx = {z[1]: br.new_context(viewport={'width': a.width, 'height': 900}, device_scale_factor=z[0], locale='fa-IR', user_agent=UA) for z in ZOOMS}
        for ai, title in enumerate(titles):
            split = 'tune' if ai % 2 == 0 else 'final'
            url = a.base_url + urllib.parse.quote(title.replace(' ', '_')) if a.base_url.startswith('http') else a.base_url + title
            pages = {}
            try:
                for name, c in ctx.items():
                    pg = c.new_page(); resp = pg.goto(url, wait_until='load', timeout=60000)
                    if resp is not None and resp.status >= 400: raise RuntimeError(f'HTTP {resp.status}')
                    pg.add_style_tag(content=HIDE_CSS); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
                    pages[name] = pg; time.sleep(a.delay)
                items = pages['z100'].evaluate(JS_SCAN)
                why = collections.Counter(reject_reason(it) or 'ok' for it in items)
                print(f'[{ai}] {title}: page title={pages["z100"].title()!r}, {len(items)} paragraphs, {dict(why)}', file=sys.stderr)
                blocks = pick_blocks(items, a.blocks, random.Random(f'{title}'))
                if not blocks:
                    missing.append((title, f'no usable paragraphs ({dict(why)})'))
                made_art = 0
                for bi, blk in enumerate(blocks):
                    truth = '\n'.join(it['text'] for it in blk)
                    shots = {}
                    try:
                        for zoom, name, ext, q in ZOOMS:
                            pg = pages[name]
                            r0, r1 = pg.evaluate(JS_RECT, blk[0]['i']), pg.evaluate(JS_RECT, blk[-1]['i'])
                            clip = {'x': max(0, r0['x'] - 6), 'y': r0['y'] - 4, 'width': r0['w'] + 12, 'height': r1['y'] + r1['h'] - r0['y'] + 8}
                            for attempt in (1, 2, 3):
                                try:
                                    shots[name] = pg.screenshot(clip=clip, full_page=True, type='png', timeout=a.shot_timeout, animations='disabled'); break
                                except Exception as e:
                                    print(f'  retry {attempt} {title} block {bi} {name}: {str(e)[:60]!r}', file=sys.stderr)
                                    if attempt == 3: raise
                                    pg.wait_for_timeout(2000 * attempt)
                    except Exception as e:
                        missing.append((f'{title}#{bi}', str(e)[:80])); continue          # drop this block, keep the others
                    # write all zoom levels of a block together or not at all
                    for zoom, name, ext, q in ZOOMS:
                        base = os.path.join(a.out, split, f'{ai:02d}_{bi}_{name}')
                        im = Image.open(io.BytesIO(shots[name])).convert('RGB')
                        if ext == 'png': im.save(base + '.png')
                        else: im.save(base + '.jpg', 'JPEG', quality=q)
                        open(base + '.txt', 'w', encoding='utf-8').write(truth + '\n'); made += 1
                    made_art += 1
                if made_art: ok_articles += 1
            except Exception as e:
                missing.append((title, str(e)[:80])); print('SKIP', title, e, file=sys.stderr)
            finally:
                for pg in pages.values(): pg.close()
        br.close()
    print(f'made {made} images from {ok_articles}/{len(titles)} articles; skipped: {missing}')
    if made == 0:
        print('ERROR: no test images were made', file=sys.stderr)
        sys.exit(1)
    if ok_articles < a.min_article_frac * len(titles):
        print(f'ERROR: only {ok_articles}/{len(titles)} articles produced images (< {a.min_article_frac:.0%})', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
