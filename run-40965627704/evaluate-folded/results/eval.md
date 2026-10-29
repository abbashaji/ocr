# Results (micro-averaged accuracy %, word / letter)

`nomark` = citation markers like [۱۱] removed from OCR output before scoring. Strict tables show numbers F1 % / punctuation F1 %.


## WARNINGS (check before trusting the tables)

- real_tune [base/v2raw]: 1/18 images returned < 30% of the reference length, e.g. 02_1_z50.jpg
- real_tune [base/v2lex]: 2/18 images returned < 30% of the reference length, e.g. 02_1_z50.jpg, 04_1_z50.jpg
- real_tune [base/ocr2/auto]: 1/18 images returned < 30% of the reference length, e.g. 02_1_z50.jpg
- real_tune [base/ocr2/raw]: 1/18 images returned < 30% of the reference length, e.g. 02_1_z50.jpg
- real_tune [base/ocr2/lex]: 1/18 images returned < 30% of the reference length, e.g. 02_1_z50.jpg
- real_tune [ft/v2raw]: 1/18 images returned < 30% of the reference length, e.g. 02_1_z50.jpg
- real_tune [ft/v2lex]: 1/18 images returned < 30% of the reference length, e.g. 02_1_z50.jpg
- real_tune [ft/ocr2/auto]: 1/18 images returned < 30% of the reference length, e.g. 02_1_z50.jpg
- real_tune [ft/ocr2/raw]: 1/18 images returned < 30% of the reference length, e.g. 02_1_z50.jpg
- real_tune [ft/ocr2/lex]: 1/18 images returned < 30% of the reference length, e.g. 02_1_z50.jpg
- real_final [base/v2raw]: 1/18 images returned < 30% of the reference length, e.g. 01_0_z50.jpg
- real_final [base/v2lex]: 1/18 images returned < 30% of the reference length, e.g. 01_0_z50.jpg
- real_final [base/ocr2/auto]: 1/18 images returned < 30% of the reference length, e.g. 01_0_z50.jpg
- real_final [base/ocr2/raw]: 1/18 images returned < 30% of the reference length, e.g. 01_0_z50.jpg
- real_final [base/ocr2/lex]: 1/18 images returned < 30% of the reference length, e.g. 01_0_z50.jpg
- real_final [ft/v2raw]: 1/18 images returned < 30% of the reference length, e.g. 01_0_z50.jpg
- real_final [ft/v2lex]: 1/18 images returned < 30% of the reference length, e.g. 01_0_z50.jpg
- real_final [ft/ocr2/auto]: 1/18 images returned < 30% of the reference length, e.g. 01_0_z50.jpg
- real_final [ft/ocr2/raw]: 1/18 images returned < 30% of the reference length, e.g. 01_0_z50.jpg
- real_final [ft/ocr2/lex]: 1/18 images returned < 30% of the reference length, e.g. 01_0_z50.jpg


## client / all  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 94.49 / 98.58 | 92.56 / 98.09 | 94.49 / 98.58 |
| v2raw | 95.68 / 99.08 | 95.24 / 99.04 | 95.83 / 99.08 | 95.39 / 99.04 |
| v2lex | 97.92 / 99.66 | 97.17 / 99.50 | 98.07 / 99.66 | 97.32 / 99.50 |
| ocr2/auto | 98.07 / 99.66 | 97.32 / 99.50 | 98.07 / 99.66 | 97.32 / 99.50 |
| ocr2/raw | 95.98 / 99.12 | 95.68 / 99.12 | 95.98 / 99.12 | 95.68 / 99.12 |
| ocr2/lex | 98.07 / 99.66 | 97.32 / 99.50 | 98.07 / 99.66 | 97.32 / 99.50 |

Strict F1 % (numbers incl. separators, 6 in ref / punctuation marks, 96 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 15.38 / 32.29 | 30.77 / 32.63 | 15.38 / 32.29 | 30.77 / 32.63 |
| v2raw | 26.67 / 63.21 | 26.67 / 73.20 | 28.57 / 63.87 | 28.57 / 73.96 |
| v2lex | 26.67 / 63.21 | 26.67 / 73.20 | 28.57 / 63.87 | 28.57 / 73.96 |
| ocr2/auto | 42.86 / 63.87 | 42.86 / 73.96 | 42.86 / 63.87 | 42.86 / 73.96 |
| ocr2/raw | 42.86 / 63.87 | 42.86 / 73.96 | 42.86 / 63.87 | 42.86 / 73.96 |
| ocr2/lex | 42.86 / 63.87 | 42.86 / 73.96 | 42.86 / 63.87 | 42.86 / 73.96 |

## client / client  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 94.49 / 98.58 | 92.56 / 98.09 | 94.49 / 98.58 |
| v2raw | 95.68 / 99.08 | 95.24 / 99.04 | 95.83 / 99.08 | 95.39 / 99.04 |
| v2lex | 97.92 / 99.66 | 97.17 / 99.50 | 98.07 / 99.66 | 97.32 / 99.50 |
| ocr2/auto | 98.07 / 99.66 | 97.32 / 99.50 | 98.07 / 99.66 | 97.32 / 99.50 |
| ocr2/raw | 95.98 / 99.12 | 95.68 / 99.12 | 95.98 / 99.12 | 95.68 / 99.12 |
| ocr2/lex | 98.07 / 99.66 | 97.32 / 99.50 | 98.07 / 99.66 | 97.32 / 99.50 |

Strict F1 % (numbers incl. separators, 6 in ref / punctuation marks, 96 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 15.38 / 32.29 | 30.77 / 32.63 | 15.38 / 32.29 | 30.77 / 32.63 |
| v2raw | 26.67 / 63.21 | 26.67 / 73.20 | 28.57 / 63.87 | 28.57 / 73.96 |
| v2lex | 26.67 / 63.21 | 26.67 / 73.20 | 28.57 / 63.87 | 28.57 / 73.96 |
| ocr2/auto | 42.86 / 63.87 | 42.86 / 73.96 | 42.86 / 63.87 | 42.86 / 73.96 |
| ocr2/raw | 42.86 / 63.87 | 42.86 / 73.96 | 42.86 / 63.87 | 42.86 / 73.96 |
| ocr2/lex | 42.86 / 63.87 | 42.86 / 73.96 | 42.86 / 63.87 | 42.86 / 73.96 |

## real_tune / all  (n=18 images, 1947 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 74.37 / 91.97 | 76.12 / 92.31 | 74.63 / 91.97 | 76.17 / 92.31 |
| v2raw | 71.91 / 85.78 | 73.86 / 87.06 | 72.42 / 85.78 | 74.27 / 87.06 |
| v2lex | 75.45 / 86.50 | 76.84 / 87.29 | 75.96 / 86.50 | 77.25 / 87.29 |
| ocr2/auto | 77.09 / 86.48 | 78.22 / 87.48 | 77.09 / 86.48 | 78.22 / 87.48 |
| ocr2/raw | 73.34 / 85.72 | 74.83 / 87.03 | 73.34 / 85.72 | 74.83 / 87.03 |
| ocr2/lex | 77.09 / 86.48 | 78.22 / 87.48 | 77.09 / 86.48 | 78.22 / 87.48 |

Strict F1 % (numbers incl. separators, 27 in ref / punctuation marks, 246 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 29.41 / 45.79 | 29.70 / 45.00 | 30.93 / 46.80 | 30.00 / 45.28 |
| v2raw | 39.58 / 60.78 | 37.36 / 63.68 | 44.19 / 63.66 | 40.96 / 65.93 |
| v2lex | 39.58 / 60.78 | 37.36 / 63.68 | 44.19 / 63.66 | 40.96 / 65.93 |
| ocr2/auto | 58.46 / 65.05 | 53.12 / 67.57 | 58.46 / 65.05 | 53.12 / 67.57 |
| ocr2/raw | 58.46 / 65.05 | 53.12 / 67.57 | 58.46 / 65.05 | 53.12 / 67.57 |
| ocr2/lex | 58.46 / 65.05 | 53.12 / 67.57 | 58.46 / 65.05 | 53.12 / 67.57 |

## real_tune / z100  (n=6 images, 649 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 95.22 / 99.25 | 95.07 / 99.18 | 95.84 / 99.25 | 95.22 / 99.18 |
| v2raw | 95.99 / 99.53 | 96.76 / 99.53 | 96.92 / 99.53 | 97.38 / 99.53 |
| v2lex | 95.07 / 99.21 | 96.15 / 99.33 | 95.99 / 99.21 | 96.76 / 99.33 |
| ocr2/auto | 98.15 / 99.33 | 98.31 / 99.37 | 98.15 / 99.33 | 98.31 / 99.37 |
| ocr2/raw | 98.61 / 99.57 | 98.77 / 99.57 | 98.61 / 99.57 | 98.77 / 99.57 |
| ocr2/lex | 98.15 / 99.33 | 98.31 / 99.37 | 98.15 / 99.33 | 98.31 / 99.37 |

Strict F1 % (numbers incl. separators, 9 in ref / punctuation marks, 82 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 45.71 / 49.14 | 50.00 / 49.41 | 51.61 / 51.81 | 51.43 / 50.30 |
| v2raw | 46.15 / 64.17 | 52.94 / 70.79 | 54.55 / 69.36 | 60.00 / 74.12 |
| v2lex | 46.15 / 64.17 | 52.94 / 70.79 | 54.55 / 69.36 | 60.00 / 74.12 |
| ocr2/auto | 78.26 / 71.08 | 85.71 / 77.11 | 78.26 / 71.08 | 85.71 / 77.11 |
| ocr2/raw | 78.26 / 71.08 | 85.71 / 77.11 | 78.26 / 71.08 | 85.71 / 77.11 |
| ocr2/lex | 78.26 / 71.08 | 85.71 / 77.11 | 78.26 / 71.08 | 85.71 / 77.11 |

## real_tune / z100+z75  (n=12 images, 1298 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 90.52 / 97.90 | 91.45 / 98.13 | 90.91 / 97.90 | 91.53 / 98.13 |
| v2raw | 90.83 / 98.11 | 91.99 / 98.37 | 91.60 / 98.11 | 92.60 / 98.37 |
| v2lex | 92.84 / 98.57 | 93.14 / 98.57 | 93.61 / 98.57 | 93.76 / 98.57 |
| ocr2/auto | 95.22 / 98.59 | 95.22 / 98.59 | 95.22 / 98.59 | 95.22 / 98.59 |
| ocr2/raw | 92.99 / 98.13 | 93.61 / 98.33 | 92.99 / 98.13 | 93.61 / 98.33 |
| ocr2/lex | 95.22 / 98.59 | 95.22 / 98.59 | 95.22 / 98.59 | 95.22 / 98.59 |

Strict F1 % (numbers incl. separators, 18 in ref / punctuation marks, 164 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 37.68 / 48.45 | 41.18 / 49.12 | 40.62 / 50.00 | 41.79 / 49.56 |
| v2raw | 48.00 / 66.48 | 49.28 / 71.39 | 55.38 / 70.76 | 55.74 / 74.78 |
| v2lex | 48.00 / 66.48 | 49.28 / 71.39 | 55.38 / 70.76 | 55.74 / 74.78 |
| ocr2/auto | 76.60 / 73.49 | 75.56 / 76.83 | 76.60 / 73.49 | 75.56 / 76.83 |
| ocr2/raw | 76.60 / 73.49 | 75.56 / 76.83 | 76.60 / 73.49 | 75.56 / 76.83 |
| ocr2/lex | 76.60 / 73.49 | 75.56 / 76.83 | 76.60 / 73.49 | 75.56 / 76.83 |

## real_tune / z50  (n=6 images, 649 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 42.06 / 80.13 | 45.45 / 80.68 | 42.06 / 80.13 | 45.45 / 80.68 |
| v2raw | 34.05 / 61.12 | 37.60 / 64.45 | 34.05 / 61.12 | 37.60 / 64.45 |
| v2lex | 40.68 / 62.37 | 44.22 / 64.73 | 40.68 / 62.37 | 44.22 / 64.73 |
| ocr2/auto | 40.83 / 62.25 | 44.22 / 65.28 | 40.83 / 62.25 | 44.22 / 65.28 |
| ocr2/raw | 34.05 / 60.88 | 37.29 / 64.41 | 34.05 / 60.88 | 37.29 / 64.41 |
| ocr2/lex | 40.83 / 62.25 | 44.22 / 65.28 | 40.83 / 62.25 | 44.22 / 65.28 |

Strict F1 % (numbers incl. separators, 9 in ref / punctuation marks, 82 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 12.12 / 39.74 | 6.06 / 34.78 | 12.12 / 39.74 | 6.06 / 34.78 |
| v2raw | 9.52 / 43.90 | 0.00 / 40.00 | 9.52 / 43.90 | 0.00 / 40.00 |
| v2lex | 9.52 / 43.90 | 0.00 / 40.00 | 9.52 / 43.90 | 0.00 / 40.00 |
| ocr2/auto | 11.11 / 42.28 | 0.00 / 41.38 | 11.11 / 42.28 | 0.00 / 41.38 |
| ocr2/raw | 11.11 / 42.28 | 0.00 / 41.38 | 11.11 / 42.28 | 0.00 / 41.38 |
| ocr2/lex | 11.11 / 42.28 | 0.00 / 41.38 | 11.11 / 42.28 | 0.00 / 41.38 |

## real_tune / z75  (n=6 images, 649 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 85.82 / 96.54 | 87.83 / 97.09 | 85.98 / 96.54 | 87.83 / 97.09 |
| v2raw | 85.67 / 96.70 | 87.21 / 97.21 | 86.29 / 96.70 | 87.83 / 97.21 |
| v2lex | 90.60 / 97.92 | 90.14 / 97.80 | 91.22 / 97.92 | 90.76 / 97.80 |
| ocr2/auto | 92.30 / 97.84 | 92.14 / 97.80 | 92.30 / 97.84 | 92.14 / 97.80 |
| ocr2/raw | 87.37 / 96.70 | 88.44 / 97.09 | 87.37 / 96.70 | 88.44 / 97.09 |
| ocr2/lex | 92.30 / 97.84 | 92.14 / 97.80 | 92.30 / 97.84 | 92.14 / 97.80 |

Strict F1 % (numbers incl. separators, 9 in ref / punctuation marks, 82 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 29.41 / 47.78 | 31.25 / 48.84 | 30.30 / 48.31 | 31.25 / 48.84 |
| v2raw | 50.00 / 68.93 | 45.71 / 72.00 | 56.25 / 72.19 | 51.61 / 75.45 |
| v2lex | 50.00 / 68.93 | 45.71 / 72.00 | 56.25 / 72.19 | 51.61 / 75.45 |
| ocr2/auto | 75.00 / 75.90 | 66.67 / 76.54 | 75.00 / 75.90 | 66.67 / 76.54 |
| ocr2/raw | 75.00 / 75.90 | 66.67 / 76.54 | 75.00 / 75.90 | 66.67 / 76.54 |
| ocr2/lex | 75.00 / 75.90 | 66.67 / 76.54 | 75.00 / 75.90 | 66.67 / 76.54 |

## real_final / all  (n=18 images, 1791 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 70.97 / 90.85 | 72.14 / 91.03 | 71.25 / 90.85 | 72.25 / 91.03 |
| v2raw | 68.40 / 82.48 | 69.24 / 83.29 | 69.35 / 82.48 | 69.96 / 83.29 |
| v2lex | 71.41 / 82.83 | 72.59 / 83.77 | 72.36 / 82.83 | 73.31 / 83.77 |
| ocr2/auto | 73.31 / 82.95 | 74.48 / 83.73 | 73.65 / 82.95 | 74.71 / 83.73 |
| ocr2/raw | 70.24 / 82.54 | 71.19 / 83.18 | 70.58 / 82.54 | 71.41 / 83.18 |
| ocr2/lex | 73.31 / 82.95 | 74.48 / 83.73 | 73.65 / 82.95 | 74.71 / 83.73 |

Strict F1 % (numbers incl. separators, 51 in ref / punctuation marks, 183 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 35.16 / 37.25 | 36.99 / 34.87 | 36.16 / 38.10 | 37.43 / 35.23 |
| v2raw | 36.99 / 56.28 | 35.84 / 61.81 | 41.03 / 61.71 | 38.75 / 66.31 |
| v2lex | 36.99 / 56.28 | 35.84 / 61.81 | 41.03 / 61.71 | 38.75 / 66.31 |
| ocr2/auto | 46.40 / 62.40 | 47.54 / 67.04 | 48.74 / 64.55 | 49.15 / 68.56 |
| ocr2/raw | 46.40 / 62.40 | 47.54 / 67.04 | 48.74 / 64.55 | 49.15 / 68.56 |
| ocr2/lex | 46.40 / 62.40 | 47.54 / 67.04 | 48.74 / 64.55 | 49.15 / 68.56 |

## real_final / z100  (n=6 images, 597 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 91.96 / 99.26 | 91.96 / 99.10 | 92.63 / 99.26 | 92.13 / 99.10 |
| v2raw | 92.13 / 99.47 | 91.96 / 99.42 | 94.30 / 99.47 | 93.30 / 99.42 |
| v2lex | 92.46 / 99.51 | 92.46 / 99.51 | 94.64 / 99.51 | 93.80 / 99.51 |
| ocr2/auto | 96.98 / 99.55 | 96.65 / 99.38 | 97.65 / 99.55 | 96.98 / 99.38 |
| ocr2/raw | 96.65 / 99.51 | 96.48 / 99.34 | 97.32 / 99.51 | 96.82 / 99.34 |
| ocr2/lex | 96.98 / 99.55 | 96.65 / 99.38 | 97.65 / 99.55 | 96.98 / 99.38 |

Strict F1 % (numbers incl. separators, 17 in ref / punctuation marks, 61 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 47.06 / 42.11 | 50.00 / 44.93 | 50.00 / 44.14 | 50.79 / 45.59 |
| v2raw | 46.38 / 58.82 | 46.38 / 67.52 | 57.14 / 69.93 | 52.46 / 75.71 |
| v2lex | 46.38 / 58.82 | 46.38 / 67.52 | 57.14 / 69.93 | 52.46 / 75.71 |
| ocr2/auto | 76.19 / 72.86 | 76.19 / 75.56 | 84.21 / 77.27 | 80.00 / 77.86 |
| ocr2/raw | 76.19 / 72.86 | 76.19 / 75.56 | 84.21 / 77.27 | 80.00 / 77.86 |
| ocr2/lex | 76.19 / 72.86 | 76.19 / 75.56 | 84.21 / 77.27 | 80.00 / 77.86 |

## real_final / z100+z75  (n=12 images, 1194 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 87.44 / 98.05 | 88.19 / 98.15 | 87.86 / 98.05 | 88.36 / 98.15 |
| v2raw | 87.10 / 98.07 | 86.68 / 98.05 | 88.53 / 98.07 | 87.77 / 98.05 |
| v2lex | 89.20 / 98.46 | 89.53 / 98.64 | 90.62 / 98.46 | 90.62 / 98.64 |
| ocr2/auto | 92.13 / 98.36 | 92.29 / 98.40 | 92.63 / 98.36 | 92.63 / 98.40 |
| ocr2/raw | 89.87 / 97.97 | 89.87 / 97.88 | 90.37 / 97.97 | 90.20 / 97.88 |
| ocr2/lex | 92.13 / 98.36 | 92.29 / 98.40 | 92.63 / 98.36 | 92.63 / 98.40 |

Strict F1 % (numbers incl. separators, 34 in ref / punctuation marks, 122 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 44.27 / 40.26 | 45.53 / 39.18 | 46.03 / 41.50 | 46.28 / 39.72 |
| v2raw | 41.18 / 61.34 | 41.48 / 66.89 | 47.06 / 69.06 | 45.90 / 73.38 |
| v2lex | 41.18 / 61.34 | 41.48 / 66.89 | 47.06 / 69.06 | 45.90 / 73.38 |
| ocr2/auto | 60.87 / 70.63 | 60.00 / 74.63 | 65.12 / 73.93 | 62.79 / 76.92 |
| ocr2/raw | 60.87 / 70.63 | 60.00 / 74.63 | 65.12 / 73.93 | 62.79 / 76.92 |
| ocr2/lex | 60.87 / 70.63 | 60.00 / 74.63 | 65.12 / 73.93 | 62.79 / 76.92 |

## real_final / z50  (n=6 images, 597 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 38.02 / 76.46 | 40.03 / 76.79 | 38.02 / 76.46 | 40.03 / 76.79 |
| v2raw | 30.99 / 51.31 | 34.34 / 53.78 | 30.99 / 51.31 | 34.34 / 53.78 |
| v2lex | 35.85 / 51.56 | 38.69 / 54.03 | 35.85 / 51.56 | 38.69 / 54.03 |
| ocr2/auto | 35.68 / 52.14 | 38.86 / 54.40 | 35.68 / 52.14 | 38.86 / 54.40 |
| ocr2/raw | 30.99 / 51.68 | 33.84 / 53.78 | 30.99 / 51.68 | 33.84 / 53.78 |
| ocr2/lex | 35.68 / 52.14 | 38.86 / 54.40 | 35.68 / 52.14 | 38.86 / 54.40 |

Strict F1 % (numbers incl. separators, 17 in ref / punctuation marks, 61 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 11.76 / 28.57 | 16.00 / 22.22 | 11.76 / 28.57 | 16.00 / 22.22 |
| v2raw | 21.62 / 37.65 | 15.79 / 45.16 | 21.62 / 37.65 | 15.79 / 45.16 |
| v2lex | 21.62 / 37.65 | 15.79 / 45.16 | 21.62 / 37.65 | 15.79 / 45.16 |
| ocr2/auto | 6.06 / 37.78 | 12.50 / 45.16 | 6.06 / 37.78 | 12.50 / 45.16 |
| ocr2/raw | 6.06 / 37.78 | 12.50 / 45.16 | 6.06 / 37.78 | 12.50 / 45.16 |
| ocr2/lex | 6.06 / 37.78 | 12.50 / 45.16 | 6.06 / 37.78 | 12.50 / 45.16 |

## real_final / z75  (n=6 images, 597 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 82.91 / 96.84 | 84.42 / 97.21 | 83.08 / 96.84 | 84.59 / 97.21 |
| v2raw | 82.08 / 96.67 | 81.41 / 96.67 | 82.75 / 96.67 | 82.24 / 96.67 |
| v2lex | 85.93 / 97.41 | 86.60 / 97.78 | 86.60 / 97.41 | 87.44 / 97.78 |
| ocr2/auto | 87.27 / 97.17 | 87.94 / 97.41 | 87.60 / 97.17 | 88.27 / 97.41 |
| ocr2/raw | 83.08 / 96.43 | 83.25 / 96.43 | 83.42 / 96.43 | 83.58 / 96.43 |
| ocr2/lex | 87.27 / 97.17 | 87.94 / 97.41 | 87.60 / 97.17 | 88.27 / 97.41 |

Strict F1 % (numbers incl. separators, 17 in ref / punctuation marks, 61 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 41.27 / 38.41 | 40.68 / 33.99 | 41.94 / 38.93 | 41.38 / 34.44 |
| v2raw | 35.82 / 64.34 | 36.36 / 66.22 | 38.10 / 68.15 | 39.34 / 71.01 |
| v2lex | 35.82 / 64.34 | 36.36 / 66.22 | 38.10 / 68.15 | 39.34 / 71.01 |
| ocr2/auto | 48.00 / 68.22 | 45.83 / 73.68 | 50.00 / 70.40 | 47.83 / 75.97 |
| ocr2/raw | 48.00 / 68.22 | 45.83 / 73.68 | 50.00 / 70.40 | 47.83 / 75.97 |
| ocr2/lex | 48.00 / 68.22 | 45.83 / 73.68 | 50.00 / 70.40 | 47.83 / 75.97 |

# Product engine (ocr2): all metrics, raw view

word / letter accuracy %, numbers F1 %, punctuation F1 %, mean seconds per image (this machine, all CPU cores, images one at a time).


## client / all  (n=2 images, 672 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 98.07 | 99.66 | 42.86 | 63.87 | 4.52 |
| base | raw | 95.98 | 99.12 | 42.86 | 63.87 | 4.42 |
| base | lex | 98.07 | 99.66 | 42.86 | 63.87 | 4.42 |
| ft | auto | 97.32 | 99.50 | 42.86 | 73.96 | 4.44 |
| ft | raw | 95.68 | 99.12 | 42.86 | 73.96 | 4.43 |
| ft | lex | 97.32 | 99.50 | 42.86 | 73.96 | 4.43 |

## client / client  (n=2 images, 672 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 98.07 | 99.66 | 42.86 | 63.87 | 4.52 |
| base | raw | 95.98 | 99.12 | 42.86 | 63.87 | 4.42 |
| base | lex | 98.07 | 99.66 | 42.86 | 63.87 | 4.42 |
| ft | auto | 97.32 | 99.50 | 42.86 | 73.96 | 4.44 |
| ft | raw | 95.68 | 99.12 | 42.86 | 73.96 | 4.43 |
| ft | lex | 97.32 | 99.50 | 42.86 | 73.96 | 4.43 |

## real_tune / all  (n=18 images, 1947 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 77.09 | 86.48 | 58.46 | 65.05 | 1.23 |
| base | raw | 73.34 | 85.72 | 58.46 | 65.05 | 1.19 |
| base | lex | 77.09 | 86.48 | 58.46 | 65.05 | 1.19 |
| ft | auto | 78.22 | 87.48 | 53.12 | 67.57 | 1.21 |
| ft | raw | 74.83 | 87.03 | 53.12 | 67.57 | 1.19 |
| ft | lex | 78.22 | 87.48 | 53.12 | 67.57 | 1.19 |

## real_tune / z100  (n=6 images, 649 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 98.15 | 99.33 | 78.26 | 71.08 | 1.36 |
| base | raw | 98.61 | 99.57 | 78.26 | 71.08 | 1.35 |
| base | lex | 98.15 | 99.33 | 78.26 | 71.08 | 1.35 |
| ft | auto | 98.31 | 99.37 | 85.71 | 77.11 | 1.36 |
| ft | raw | 98.77 | 99.57 | 85.71 | 77.11 | 1.36 |
| ft | lex | 98.31 | 99.37 | 85.71 | 77.11 | 1.36 |

## real_tune / z100+z75  (n=12 images, 1298 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 95.22 | 98.59 | 76.60 | 73.49 | 1.31 |
| base | raw | 92.99 | 98.13 | 76.60 | 73.49 | 1.29 |
| base | lex | 95.22 | 98.59 | 76.60 | 73.49 | 1.29 |
| ft | auto | 95.22 | 98.59 | 75.56 | 76.83 | 1.30 |
| ft | raw | 93.61 | 98.33 | 75.56 | 76.83 | 1.30 |
| ft | lex | 95.22 | 98.59 | 75.56 | 76.83 | 1.30 |

## real_tune / z50  (n=6 images, 649 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 40.83 | 62.25 | 11.11 | 42.28 | 1.07 |
| base | raw | 34.05 | 60.88 | 11.11 | 42.28 | 1.00 |
| base | lex | 40.83 | 62.25 | 11.11 | 42.28 | 1.00 |
| ft | auto | 44.22 | 65.28 | 0.00 | 41.38 | 1.04 |
| ft | raw | 37.29 | 64.41 | 0.00 | 41.38 | 0.98 |
| ft | lex | 44.22 | 65.28 | 0.00 | 41.38 | 0.98 |

## real_tune / z75  (n=6 images, 649 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 92.30 | 97.84 | 75.00 | 75.90 | 1.25 |
| base | raw | 87.37 | 96.70 | 75.00 | 75.90 | 1.23 |
| base | lex | 92.30 | 97.84 | 75.00 | 75.90 | 1.23 |
| ft | auto | 92.14 | 97.80 | 66.67 | 76.54 | 1.24 |
| ft | raw | 88.44 | 97.09 | 66.67 | 76.54 | 1.23 |
| ft | lex | 92.14 | 97.80 | 66.67 | 76.54 | 1.23 |

## real_final / all  (n=18 images, 1791 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 73.31 | 82.95 | 46.40 | 62.40 | 1.08 |
| base | raw | 70.24 | 82.54 | 46.40 | 62.40 | 1.04 |
| base | lex | 73.31 | 82.95 | 46.40 | 62.40 | 1.04 |
| ft | auto | 74.48 | 83.73 | 47.54 | 67.04 | 1.05 |
| ft | raw | 71.19 | 83.18 | 47.54 | 67.04 | 1.03 |
| ft | lex | 74.48 | 83.73 | 47.54 | 67.04 | 1.03 |

## real_final / z100  (n=6 images, 597 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 96.98 | 99.55 | 76.19 | 72.86 | 1.29 |
| base | raw | 96.65 | 99.51 | 76.19 | 72.86 | 1.27 |
| base | lex | 96.98 | 99.55 | 76.19 | 72.86 | 1.27 |
| ft | auto | 96.65 | 99.38 | 76.19 | 75.56 | 1.28 |
| ft | raw | 96.48 | 99.34 | 76.19 | 75.56 | 1.28 |
| ft | lex | 96.65 | 99.38 | 76.19 | 75.56 | 1.28 |

## real_final / z100+z75  (n=12 images, 1194 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 92.13 | 98.36 | 60.87 | 70.63 | 1.25 |
| base | raw | 89.87 | 97.97 | 60.87 | 70.63 | 1.22 |
| base | lex | 92.13 | 98.36 | 60.87 | 70.63 | 1.22 |
| ft | auto | 92.29 | 98.40 | 60.00 | 74.63 | 1.22 |
| ft | raw | 89.87 | 97.88 | 60.00 | 74.63 | 1.21 |
| ft | lex | 92.29 | 98.40 | 60.00 | 74.63 | 1.21 |

## real_final / z50  (n=6 images, 597 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 35.68 | 52.14 | 6.06 | 37.78 | 0.74 |
| base | raw | 30.99 | 51.68 | 6.06 | 37.78 | 0.68 |
| base | lex | 35.68 | 52.14 | 6.06 | 37.78 | 0.68 |
| ft | auto | 38.86 | 54.40 | 12.50 | 45.16 | 0.71 |
| ft | raw | 33.84 | 53.78 | 12.50 | 45.16 | 0.66 |
| ft | lex | 38.86 | 54.40 | 12.50 | 45.16 | 0.66 |

## real_final / z75  (n=6 images, 597 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 87.27 | 97.17 | 48.00 | 68.22 | 1.21 |
| base | raw | 83.08 | 96.43 | 48.00 | 68.22 | 1.17 |
| base | lex | 87.27 | 97.17 | 48.00 | 68.22 | 1.17 |
| ft | auto | 87.94 | 97.41 | 45.83 | 73.68 | 1.16 |
| ft | raw | 83.25 | 96.43 | 45.83 | 73.68 | 1.15 |
| ft | lex | 87.94 | 97.41 | 45.83 | 73.68 | 1.15 |
