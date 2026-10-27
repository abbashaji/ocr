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

## Bulk corpus from a Wikipedia dump (`corpus_source = dump`)
`ft/fetch_corpus.py` (API, ~1.2 s per article) only reaches ~1 MB. `ft/fetch_corpus_dump.py` builds 100+ MB in minutes from a bulk source:
1. `hf`: the parquet snapshot `wikimedia/wikipedia` / `20231101.fa` on huggingface.co (plain text, fast); 2. fallback `dump`: the official
`https://dumps.wikimedia.org/fawiki/latest/fawiki-latest-pages-articles.xml.bz2` (stream-decoded, resumable, wikitext stripped by regexes).
Same output as the API fetcher (one cleaned paragraph per line, `common.clean_text`), plus `corpus_stats.json` (source, dump date, paragraphs, MB,
pinned titles found/not found, paragraphs dropped for overlap, seconds). Pinned evaluation articles (`ft/articles.txt`, plus «ایران») are
skipped by normalised title, and any paragraph sharing a 10-word shingle with their text (or with `--ground-truth DIR`) is dropped.
Run: Actions -> finetune-tesseract-fa -> `corpus_source: dump`, `target_mb: 100`, `corpus_minutes: 60` (quick=true builds a 3 MB test corpus).
The cache key prefix is `corpusdump-`, separate from the API cache (`corpus-`); `refresh_corpus: true` forces a rebuild.
Unit tests: `python -m pytest ft/test_fetch_corpus_dump.py -q` (needs pyarrow).

## Source and licence of the training text
Training text comes from Persian Wikipedia (fa.wikipedia.org), (c) Wikipedia contributors, licensed CC BY-SA 4.0
(https://creativecommons.org/licenses/by-sa/4.0/). The corpus is only cached as a workflow artifact and never committed to this repository.
