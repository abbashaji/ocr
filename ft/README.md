# Tesseract (fas) fine-tune for Persian Wikipedia screenshots

## Run it
1. Copy this folder's contents into the root of `abbashaji/ocr` (the `.github/workflows/finetune.yml` file may have to be
   added through the GitHub web page if a bot push is refused).
2. Actions -> **finetune-tesseract-fa** -> Run workflow with `quick: true` (~15-30 min). This proves the whole chain on a tiny
   corpus. Check the `results` branch for `latest/*`.
3. Run again with `quick: false` (defaults: 20 MB corpus, 30 000 lines, 60 000 iterations, <=300 min training).
   If training hits the time limit, re-run with `resume: true`.
4. Read `results` branch: `latest/evaluate/results/eval.md` (table), `latest/train/fas_ft.traineddata`, `latest/train/train_summary.json`.

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
