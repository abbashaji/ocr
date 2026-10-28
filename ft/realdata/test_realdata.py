import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from textclean import body_of, cmp_form
import align

PARA = ("در سدهٔ نخست پیش از میلاد، پادشاهان ایران‌زمین سپاهی بزرگ فراهم آوردند و از رود فرات گذشتند. "
        "مردمان آن سرزمین، که از دیرباز با کشاورزی و بازرگانی روزگار می‌گذراندند، از این رویداد شگفت‌زده شدند. "
        "گزارش‌های تاریخی نشان می‌دهد که در سال ۱۲۹۸ شمسی شمار سپاهیان به ۲۵٬۰۰۰ تن رسید. "
        "فرمانروا پس از آن فرمان داد تا شهرها را آباد کنند و راه‌ها را ایمن سازند و مالیات را بکاهند. "
        "بازرگانان از دورترین سرزمین‌ها کالاهای گرانبها آوردند و در بازار شهر به داد و ستد پرداختند. "
        "دانشمندان و دبیران در دربار گرد آمدند و کتاب‌های بسیاری را از زبان‌های بیگانه ترجمه کردند.")

def noisy(s, rng, p=0.03):
    out = []
    for ch in s:
        r = rng.random()
        if r < p / 2: continue
        out.append(rng.choice('سنمتب') if r < p else ch)
    return ''.join(out)

def split_lines(text, width=40):
    words, lines, cur = text.split(), [], ''
    for w in words:
        if len(cur) + len(w) + 1 > width and cur: lines.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    if cur: lines.append(cur)
    return lines

def test_body_of_strips_markup_keeps_fidelity():
    wt = '<noinclude><pagequality level="4" user="X" /></noinclude>در سدهٔ [[ایران|ایرانی]] {{سخ}} با «نیرو»، ۱۲۳.<ref>پانویس</ref>\n<noinclude>پانویس: ۱</noinclude>'
    t, lvl, flags = body_of(wt)
    assert lvl == 4
    assert 'سدهٔ' in t and 'ایرانی' in t and '«نیرو»،' in t and '۱۲۳' in t
    assert 'پانویس' not in t and '{{' not in t and not flags

def test_complex_flag():
    t, lvl, flags = body_of('<pagequality level="3" />{| class="wikitable"\n|a\n|}')
    assert 'complex_layout' in flags

def test_cmp_form_ignores_ezafe_punct_digit_script():
    assert cmp_form('سدهٔ ۱۲٫۵،') == cmp_form('سده 12.5')

def test_alignment_gold_and_label_is_gt_not_ocr():
    rng = random.Random(1)
    lines = split_lines(PARA)
    ocr = [{'text': noisy(l, rng)} for l in lines]
    res = align.align_page(ocr, PARA)
    gold = [(r, l) for r, l in zip(res, lines) if r['tier'] == 'GOLD']
    assert len(gold) >= 0.7 * len(lines), [r['reason'] for r in res]
    # label must be an exact substring of the ground truth (whitespace-normalised) and keep the ezafe mark
    gtn = ' '.join(PARA.split())
    for r, _ in gold: assert r['label'] in gtn
    assert any('سدهٔ' in (r['label'] or '') for r in res)   # ezafe kept in the label (any tier)

def test_misaligned_garbage_line_is_rejected():
    rng = random.Random(2)
    lines = split_lines(PARA)
    ocr = [{'text': noisy(l, rng)} for l in lines]
    ocr[3] = {'text': 'ABCDE FGHIJ KLMNO PQRST UVWXY'}
    res = align.align_page(ocr, PARA)
    assert res[3]['tier'] in (None, 'SILVER') and res[3]['tier'] != 'GOLD'

def test_repeated_text_is_ambiguous():
    gt = 'ای دوست ای دوست ای دوست ای دوست ای دوست ای دوست ای دوست ای دوست'
    res = align.align_page([{'text': 'ای دوست ای دوست ای دوست'}], gt)
    assert res[0]['tier'] != 'GOLD'

def test_anchored_line_between_gold_neighbours():
    rng = random.Random(3)
    lines = split_lines(PARA)
    ocr = [{'text': noisy(l, rng, 0.02)} for l in lines]
    ocr[4] = {'text': noisy(lines[4], rng, 0.30)}   # heavily damaged line
    res = align.align_page(ocr, PARA)
    assert res[4]['tier'] in ('GOLD_A', 'SILVER', 'GOLD')
    assert res[4]['label'] and cmp_form(res[4]['label']) == cmp_form(lines[4])

# ---- end-to-end on a rendered page (needs tesseract + the shipped model; skipped otherwise) ----------------------------
import shutil, pytest
MODEL_DIR = os.environ.get('REALDATA_TESSDATA', '/work/model')
FONT = next((p for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',) if os.path.exists(p)), None)

@pytest.mark.skipif(not (shutil.which('tesseract') and os.path.exists(os.path.join(MODEL_DIR, 'fas.traineddata')) and FONT), reason='needs tesseract+model+font')
def test_process_page_end_to_end():
    import build_work, fixture_page
    gt = PARA + ' ' + PARA[::-1][:0]
    img, lines = fixture_page.render_page(gt, FONT)
    recs, info = build_work.process_page(img, gt, MODEL_DIR, workers=2)
    tiers = [r['tier'] for r, _ in recs]
    n_label = sum(t in ('GOLD', 'GOLD_A') for t in tiers)
    assert n_label >= 0.7 * len(lines), (len(lines), tiers, [r['reason'] for r, _ in recs])
    # header and page number lines must not be labelled with page text
    assert recs[0][0]['tier'] in (None,) or recs[0][0]['sim'] < 0.93
    gtn = ' '.join(gt.split())
    for r, c in recs:
        if r['tier']: assert r['label'] in gtn and c is not None


@pytest.mark.skipif(not (shutil.which('tesseract') and FONT), reason='needs font')
def test_dark_border_fallback_recovers_lines():
    import fixture_page, pageimg
    from PIL import Image
    img, lines = fixture_page.render_page(PARA, FONT)
    framed = Image.new('L', (img.width + 240, img.height + 240), 12); framed.paste(img, (120, 120))      # black scanner frame
    gray, found, info = pageimg.page_lines(framed)
    assert len(found) >= 0.7 * len(lines), (len(found), len(lines))
