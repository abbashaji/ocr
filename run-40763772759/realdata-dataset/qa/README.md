# Persian real-scan line dataset (fa.wikisource + Wikimedia Commons)

Real scanned Persian book/periodical pages with human-proofread text. Lines were cut with the product segmenter
(`matnyab.engine.segment`), the label of each line is the human text found by monotone edit-distance alignment against the
page text (never OCR output). Built 2026-10-28; rebuild: GitHub Actions -> `build-real-dataset` -> stage `build`.

## Counts (after dedupe and leakage filtering)
| split/tier | lines |
|---|---|
| final/GOLD | 3382 |
| final/GOLD_A | 6 |
| final/SILVER | 2788 |
| train/GOLD | 19786 |
| train/GOLD_A | 25 |
| train/SILVER | 10739 |
| tune/GOLD | 2859 |
| tune/GOLD_A | 6 |
| tune/SILVER | 407 |

Total lines: 39998. Splits are by WORK: train / tune / final (final = held-out real-scan benchmark).
Tiers: GOLD = unambiguous alignment, similarity >= 0.93; GOLD_A = anchored between two GOLD neighbours; SILVER = weaker alignment
(0.80-0.93) - train on GOLD/GOLD_A first. Dropped lines and reasons: see `stats.json` (`drops`, `line_reasons_total`).

## Layout
- `lines/<id>.png`   grey line images, height <= 64 px, horizontally trimmed (id = work_pPAGE_lLINE)
- `manifest.jsonl` / `manifest.csv`   id, work, split, tier, sim, margin, page, revid, page_title, licence, commons_url, wikisource_url,
  label_full (FULL FIDELITY: ezafe, ZWNJ, original digits/punctuation), label_folded, label_distinct, w, h, y0, y1, deskew, dpi, quality
- `export/tesseract_{folded,distinct}_{gold,silver}/<split>/<id>.png + <id>.gt.txt`
- `export/tesseract_{folded,distinct}_gold_train_aug1/train/` train lines + one seeded augmented copy (`*_aug1.png`)
- `export/paddle_{folded,distinct}_{gold,silver}/{train,tune,final}.txt` (`images/<id>.png<TAB>label`), `images/`, `dict.txt`
- `benchmark_pages/` text-block crops (jpg) + full human page text (txt) of the final works
- `ATTRIBUTION.md`, `stats.json`, `contact_sheet.html` (100 random GOLD lines, RTL)

## Presets (applied only when exporting; the manifest keeps full fidelity)
- folded  = `ft/common.py` clean_text + LABEL_MAP (ezafe and harakat dropped, ، ٬ -> ",", ٫ -> ".", ٪ and % -> "#", ; -> ؛, dashes -> "-").
  With `--unicharset` lines containing characters outside the model's unicharset are dropped (as in make_train_data.py).
- distinct = same normalisation of ya/kaf/digits/spaces/quotes, but KEEPS the ezafe mark U+0654 and ، ٫ ٬ ٪.

## Re-export with other settings
`python ft/realdata/export.py` is a library: `select(records, splits, tiers, preset)` + `write_tesseract` / `write_paddle`
(augmentation: `write_tesseract(..., augment=N, seed=S)`, train split only). See `ft/realdata/test_assemble.py` for usage.
