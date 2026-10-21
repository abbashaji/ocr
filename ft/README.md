# Tesseract (fas) fine-tune for Persian Wikipedia screenshots

## Run it
1. Copy this folder's contents into the root of `abbashaji/ocr` (the `.github/workflows/finetune.yml` file may have to be
   added through the GitHub web page if a bot push is refused).
2. Actions -> **finetune-tesseract-fa** -> Run workflow with `quick: true` (~15-30 min). This proves the whole chain on a tiny
   corpus. Check the `results` branch for `latest/*`.
3. Run again with `quick: false` (defaults: 8 MB corpus / 150 min fetch limit, 30 000 lines, 60 000 iterations, <=300 min training).
   The fetcher is rate-limited, so 20 MB is not reachable in the job cap; `corpus_stats.json` and the fetch log say whether the
   size target or the time limit ended the fetch. The `train` job now waits for `tests`, which fails (exit 1) if fewer than
   70% of the articles produce screenshots.
   If training hits the time limit, re-run with `resume: true`.
4. Read `results` branch: `latest/evaluate/results/eval.md` (table), `latest/train/fas_ft.traineddata`, `latest/train/train_summary.json`.

## Changes after the first quick run
* Test crops no longer contain floated photos/infoboxes (they broke line segmentation: pipeline v2 returned empty text). Floats
  are hidden before scanning, and any paragraph still overlapping a floated element/image/table is rejected.
* Screenshot timeouts: 120 s limit, 3 retries, failures drop one block instead of the whole article.
* `evaluate.py` prints/writes WARNINGS when an engine returns < 30% of the reference length, and reports `z100+z75` separately
  from the unreadable `z50`.
* `evaluate-only` workflow: re-score an existing `fas_ft` artifact (give the run id) on freshly made tests, no retraining.

## What the jobs do
corpus (fa.wikipedia API, excludes «ایران» + the pinned test articles) -> tests (Playwright screenshots of 30 pinned articles,
exact ground truth from the same DOM, even index = tune split, odd = final split) -> train (`ft/train.sh`) -> evaluate
(`ft/evaluate.py`: baseline vs fine-tune; plain Tesseract, pipeline v2 without and with lexicon; client samples, real
screenshots, synthetic holdout from held-out corpus paragraphs).

## Findings that shaped the design (all measured in the sandbox)
* The stock `fas` unicharset has 95 entries and NO `،` `٫` `٬` `٪`. Extending it with `--old_traineddata` was lossy
  (15% -> 28% char error on lines with no new character), so these glyphs are trained onto unused existing classes
  (`،٬`->`,` `٫`->`.` `٪`->`#` `;`->`؛`, see `LABEL_MAP` in `ft/common.py`) and restored by context in
  `pipeline2.restore_placeholders`.
* `lstmtraining` ignores `--learning_rate` unless `--reset_learning_rate` is given. LR 2e-4 destroyed the model in 400 iterations; 1e-5 is stable.
* RTL training labels must be in VISUAL order (bidi reorder). Logical order diverges (word error 97%).
* Baseline reproduces the task file: client clean 99.11, low 96.73 (pipeline v2, markers not stripped).

## Verified here vs NOT verified
Verified in the sandbox: data generation, fine-tune + checkpoint selection + finalize (`train.sh`), the evaluation script,
`make_tests.py` (against a local Wikipedia-shaped page with Chrome), the HTML paragraph parser, `publish_results.sh` (local bare repo), YAML structure.
NOT verified: the live Wikipedia API fetch, the Actions run itself, whether article titles in `articles.txt` all exist
(missing ones are skipped and logged), and **any accuracy gain at real scale** - the only fine-tune run here used ~400 words of text.
The >99% target is therefore unproven until the Actions run reports numbers on the `final` split.

## Caveats
Linux-rendered screenshots approximate the client's Windows rendering; real client screenshots (even 10) are a valuable extra test split.
Wikipedia text is CC BY-SA - the corpus is cached, not committed.

## After the first full run (21 Oct 2026): what went wrong and what changed
First full run (10 MB corpus, 30 000 lines, 37 611 learning iterations): rendered-line BCER 18.67 -> 4.37, **but word accuracy on real
screenshots collapsed** (real_final z100: 96.1 -> 78.7 with `plain`) while letter accuracy stayed the same or improved.
* **Cause: ZWNJ (half-space) was missing from every training label.** `python-bidi` >= 0.6 silently drops U+200C in
  `get_display`. Images showed the half-space, labels did not, so the model learned never to emit it (2 ZWNJ in the
  fine-tune output vs 1 618 for the base model and 1 839 in the reference over `real_final`). Words like `هیچ‌وجه`, `سال‌های`,
  `نمی‌داد` came out joined and counted as errors. Fix: `visual()` in `make_train_data.py` hides ZWNJ behind a private-use
  placeholder, asserts at import time that it survives, and the training job pins `python-bidi==0.6.12`.
  Checked offline: the base model's BCER on the same 300 lines is 18.91 with old labels and 18.08 with fixed labels (BWER 42.8 -> 39.9).
  **A new fine-tune has NOT been run with this fix yet.** A `quick` run (2 000 iterations) cannot verify it: the quick model trained
  with the bug still emitted all 88 ZWNJ in 12 test images. The collapse only appeared after tens of thousands of iterations, so the
  check is a full run followed by comparing ZWNJ counts in `ft` vs `base` outputs.
* **Citation markers.** Most remaining z100 errors were garbled `[۲۳۶]` markers glued to words. `markers.py` now removes
  them geometrically from Tesseract character boxes (hOCR) before the per-line consensus; `pipeline2.recognize_tok(markers=True)` is the default,
  `markers=False` is the old path. On 36 Chromium screenshots, base model, v2lex (word accuracy %):
  tune z100 95.84 -> 98.00, final z100 93.13 -> 97.32, tune z75 81.66 -> 83.20, final z75 86.26 -> 88.27, client samples 98.07 -> 98.07.
  Pitfalls found: the Persian zero `۰` is a tiny dot and must not be treated as a marker; word confidence must come from
  hOCR `x_wconf`, not the mean of character confidences (that alone cost 2 to 4 points through the lexicon `conf_skip` threshold).
* Not solved: ft was only on par with the base model on real screenshots even ignoring ZWNJ; training lines (Pillow rendering) are
  much harder than real screenshots (base BCER 18.7% on them vs about 0.4% letter error on real z100), so the gain did not transfer.
  Next idea: build training lines from Chromium screenshots of the corpus text (zoom 75-100%, JPEG) with DOM ground truth.
