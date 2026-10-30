# Decision log (TASK F)

1. Source: fa.wikisource ProofreadPage + Commons. Only candidate with page-aligned HUMAN text and a per-work licence; HF datasets unverified/synthetic or NC (see SOURCES.md).
2. Only quality levels 3 (proofread) and 4 (validated) pages are used.
3. Split by WORK: train w01-w16, tune w17-w19, final w20-w23. Final deliberately mixes a 1956 print (w20), a 2022 CC BY oral-history transcript (w21), a 1906 parliament record (w22) and a hard 1851 newspaper (w23). Leakage is impossible across works by construction; plus text-level shingle checks.
4. Label = human text substring found by monotone alignment, never OCR text. GOLD: unambiguous, similarity >= 0.93. GOLD_A: anchored between two GOLD neighbours. SILVER: 0.80-0.93.
5. Storage at full fidelity (label_full). Presets only at export time: folded (current recipe) and distinct (keeps ezafe U+0654 and ، ٫ ٬ ٪).
6. NEW after visual QA: both presets first apply compat_fold (Arabic Presentation Forms -> base letters via NFKC; U+0649 -> U+06CC). 403 lines of w17 and 7 of w19 contained U+FE8D/U+FE81; without the fold they are dropped (folded) or leak foreign chars into training labels (distinct). This is a deliberate, documented deviation from "folded = exactly clean_text + LABEL_MAP".
7. SILVER is NOT recommended for training: 3 of 15 sampled SILVER lines (20%) had a real label error (extra/missing word at the line edge). GOLD: 0 of 45 content errors.
8. Benchmark reports space-vs-character errors (see benchmark.md), because on real scans word accuracy is dominated by word-boundary errors, not letter errors.
9. Augmentation: one seeded copy (`aug1`) per GOLD train line, train split only, originals untouched.
10. Hugging Face and other third-party datasets were not mixed in (provenance/label quality unverified).
11. CORRECTION (leakage check): the first two full builds used a leakage reference that contained only 2 of 31 Wikipedia articles (TextExtracts returns one full extract per request). With all 31 fetched (run 40967573452) the filter removed 131 shingle + 4 substring lines instead of 8, so about 130 lines in earlier releases (realdata-40655209632, realdata-40853197981) overlap evaluation text. Use the newest release. leak.py now fails if fewer than 90% of articles are fetched.
12. Alignment uses a single-scale per-line Tesseract call with the shipped model (not the ocr2 7-scale engine, too slow for ~6,000 pages); the product segmenter is used unchanged, plus a border-stripping fallback only when it finds <= 2 bands.
13. Selection bias: lines are labelled only when the shipped model reads them well enough to align, so line-level scores are optimistic and hard lines are under-represented. w23 (1851 newspaper) has only 141 lines / 6 benchmark pages for this reason; do not read its 85% as typical.
