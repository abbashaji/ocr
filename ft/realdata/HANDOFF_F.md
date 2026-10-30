# HANDOFF — TASK F: real Persian line dataset

State: dataset built and released; benchmark run. Final run: Actions run **40967573452** (success), release **realdata-40967573452**.
Earlier releases (realdata-40655209632, realdata-40853197981) have a defective leakage check — do not use them.

## What exists
Everything is in `ft/realdata/` of `abbashaji/ocr`; workflow `.github/workflows/build-real-dataset.yml` (stages `discover`, `probe`, `build`).
Rebuild: Actions → build-real-dataset → stage `build` (roughly 30-60 min; per-work matrix, then assemble, benchmark per held-out work, report).
Tests: `python -m pytest ft/realdata` (15 tests; they also run inside the workflow).

| item | where |
|---|---|
| Dataset + 10 export archives | release `realdata-40967573452` (base 579 MB; Tesseract/Paddle × folded/distinct × gold/silver; `*_gold_train_aug1`) |
| Counts, drops, leak coverage | `results` branch `latest/realdata-dataset/qa/stats.json` |
| 100-line visual sheets | same folder, `contact_sheet_1..5.png`, `contact_sheet.html` |
| Benchmark | `results` branch `latest/realdata-benchmark/report/benchmark.md` and `.json` |
| Licences per work | `ATTRIBUTION.md` (inside dataset-base) |
| Source research / decisions | `ft/realdata/SOURCES.md`, `ft/realdata/DECISIONS.md` |

## Numbers (final run)
- 38,391 lines after dedupe and leakage filtering. GOLD+GOLD_A: train 18,201, tune 2,853, final 3,378. SILVER: 13,959.
- Split by WORK: train w01–w16, tune w17–w19, final w20–w23 (held-out benchmark).
- Dropped: 25 cross-work duplicates, 131 + 4 lines overlapping evaluation Wikipedia text (31/31 articles fetched), 64 train lines sharing text with the benchmark works.
- Shipped model on held-out real scans (ocr2 engine, mode raw): **pages** word 36.4 %, letter 85.8 % (126 pages); **lines** word 48.1 %, letter 96.3 % (1,013 lines). lex/auto differ by 1–2 points.
- Word errors are mostly spaces: 59 % of line-level edits and 39 % of page-level edits are word-space insert/delete; character accuracy ignoring spaces is 95.5 % (lines) and 84.7 % (pages).

## Quality checks I did
- Visual audit of 100 random GOLD lines (contact sheets): 0 labels with wrong content. Seen: spacing / half-space / orthography differences between print and the Wikisource text (e.g. تأسیس vs printed تاسیس), one clipped crop. n = 100, so the true error rate could still be a few percent.
- SILVER: only an informal look; another commit reports 3 of 15 SILVER lines with a real edge error. Train on GOLD first.
- Not done by me: the "403 lines of w17" figure in DECISIONS.md item 6 and the 15-line SILVER audit were written by a different session and I did not re-check them.

## Known problems
1. **w15 (Šarq 1924) yields 0 lines.** Border fallback fixed the segmenter, but nothing aligns to the human text. Cause not found. w23 (1851 newspaper) yields 141 lines and 6 benchmark pages, so its 85 % word accuracy is selection bias, not a result.
2. **Selection bias.** Lines exist only where the shipped model read well enough to align; line-level scores are optimistic and hard lines are under-represented. The page-level benchmark is less biased but still crops the text block using the same alignment.
3. **Label vs image convention.** Wikisource text uses modern spacing / ZWNJ; old prints show otherwise. Models trained on this learn Wikisource conventions.
4. Alignment OCR is single-scale Tesseract on the shipped model, not the 7-scale ocr2 engine (too slow for ~6,000 pages). The product segmenter is unchanged except a fallback when it finds ≤ 2 bands.
5. Another session changed export presets (`compat_fold`) and benchmark reporting while I worked (same GitHub account, so I cannot tell who). I reviewed `export.py` only; the dataset README now describes it.
6. I verified my own files byte-for-byte against GitHub up to the first full run and for later pushes; files changed by the other session were not diffed.

## Legal
Transcriptions are CC BY-SA 4.0. Most scans are tagged "Public domain" on Commons by uploaders and I did not verify that per work (several Iranian works 1933–1977). Explicit open licences: w11, w19 CC BY-SA 4.0; w12, w21 CC BY 4.0; w13 CC0. Whether a model trained on this is a derivative is unsettled — get legal advice before shipping.

## Inputs for other tasks
- **C (ezafe / distinct charset):** use `export-*_distinct_*`; labels keep U+0654 and ، ٫ ٬ ٪. Real labels contain ezafe marks only where Wikisource editors typed them, so ezafe coverage is partial.
- **E (fine-tune on real data):** train on `tesseract_folded_gold` train split (+ optional `_aug1`); tune on the tune split; report only on `final` works. Re-run the benchmark with the same workflow for before/after.
- **G (evaluation):** quote the page-level numbers and the space-vs-character split, not line-level word accuracy alone.

## Not done
No PII scan. No Paddle training test. No check of release downloads beyond `export-tesseract_folded_gold` (train 19,602 / tune 2,839 / final 3,326 images, matching `.gt.txt` counts; that check was on the previous release, the new one was only listed).
