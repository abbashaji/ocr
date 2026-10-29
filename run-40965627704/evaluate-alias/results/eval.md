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
| plain | 92.56 / 98.09 | 93.45 / 98.20 | 92.56 / 98.09 | 93.45 / 98.20 |
| v2raw | 95.68 / 99.08 | 94.35 / 98.81 | 95.83 / 99.08 | 94.49 / 98.81 |
| v2lex | 97.92 / 99.66 | 97.02 / 99.43 | 98.07 / 99.66 | 97.17 / 99.43 |
| ocr2/auto | 98.07 / 99.66 | 97.62 / 99.43 | 98.07 / 99.66 | 97.62 / 99.43 |
| ocr2/raw | 95.98 / 99.12 | 95.39 / 98.93 | 95.98 / 99.12 | 95.39 / 98.93 |
| ocr2/lex | 98.07 / 99.66 | 97.62 / 99.43 | 98.07 / 99.66 | 97.62 / 99.43 |

Strict F1 % (numbers incl. separators, 6 in ref / punctuation marks, 96 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 15.38 / 32.29 | 30.77 / 33.33 | 15.38 / 32.29 | 30.77 / 33.33 |
| v2raw | 26.67 / 63.21 | 11.76 / 57.56 | 28.57 / 63.87 | 12.50 / 58.13 |
| v2lex | 26.67 / 63.21 | 11.76 / 57.56 | 28.57 / 63.87 | 12.50 / 58.13 |
| ocr2/auto | 42.86 / 63.87 | 30.77 / 58.13 | 42.86 / 63.87 | 30.77 / 58.13 |
| ocr2/raw | 42.86 / 63.87 | 30.77 / 58.13 | 42.86 / 63.87 | 30.77 / 58.13 |
| ocr2/lex | 42.86 / 63.87 | 30.77 / 58.13 | 42.86 / 63.87 | 30.77 / 58.13 |

## client / client  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 93.45 / 98.20 | 92.56 / 98.09 | 93.45 / 98.20 |
| v2raw | 95.68 / 99.08 | 94.35 / 98.81 | 95.83 / 99.08 | 94.49 / 98.81 |
| v2lex | 97.92 / 99.66 | 97.02 / 99.43 | 98.07 / 99.66 | 97.17 / 99.43 |
| ocr2/auto | 98.07 / 99.66 | 97.62 / 99.43 | 98.07 / 99.66 | 97.62 / 99.43 |
| ocr2/raw | 95.98 / 99.12 | 95.39 / 98.93 | 95.98 / 99.12 | 95.39 / 98.93 |
| ocr2/lex | 98.07 / 99.66 | 97.62 / 99.43 | 98.07 / 99.66 | 97.62 / 99.43 |

Strict F1 % (numbers incl. separators, 6 in ref / punctuation marks, 96 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 15.38 / 32.29 | 30.77 / 33.33 | 15.38 / 32.29 | 30.77 / 33.33 |
| v2raw | 26.67 / 63.21 | 11.76 / 57.56 | 28.57 / 63.87 | 12.50 / 58.13 |
| v2lex | 26.67 / 63.21 | 11.76 / 57.56 | 28.57 / 63.87 | 12.50 / 58.13 |
| ocr2/auto | 42.86 / 63.87 | 30.77 / 58.13 | 42.86 / 63.87 | 30.77 / 58.13 |
| ocr2/raw | 42.86 / 63.87 | 30.77 / 58.13 | 42.86 / 63.87 | 30.77 / 58.13 |
| ocr2/lex | 42.86 / 63.87 | 30.77 / 58.13 | 42.86 / 63.87 | 30.77 / 58.13 |

## real_tune / all  (n=18 images, 1947 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 74.37 / 91.97 | 75.50 / 92.14 | 74.63 / 91.97 | 75.50 / 92.14 |
| v2raw | 71.91 / 85.78 | 72.52 / 86.51 | 72.42 / 85.78 | 72.88 / 86.51 |
| v2lex | 75.45 / 86.50 | 75.71 / 86.82 | 75.96 / 86.50 | 76.07 / 86.82 |
| ocr2/auto | 77.09 / 86.48 | 77.45 / 86.91 | 77.09 / 86.48 | 77.45 / 86.91 |
| ocr2/raw | 73.34 / 85.72 | 73.86 / 86.40 | 73.34 / 85.72 | 73.86 / 86.40 |
| ocr2/lex | 77.09 / 86.48 | 77.45 / 86.91 | 77.09 / 86.48 | 77.45 / 86.91 |

Strict F1 % (numbers incl. separators, 27 in ref / punctuation marks, 246 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 29.41 / 45.79 | 30.30 / 44.90 | 30.93 / 46.80 | 30.30 / 44.90 |
| v2raw | 39.58 / 60.78 | 41.38 / 57.32 | 44.19 / 63.66 | 45.00 / 59.02 |
| v2lex | 39.58 / 60.78 | 41.38 / 57.32 | 44.19 / 63.66 | 45.00 / 59.02 |
| ocr2/auto | 58.46 / 65.05 | 64.41 / 59.78 | 58.46 / 65.05 | 64.41 / 59.78 |
| ocr2/raw | 58.46 / 65.05 | 64.41 / 59.78 | 58.46 / 65.05 | 64.41 / 59.78 |
| ocr2/lex | 58.46 / 65.05 | 64.41 / 59.78 | 58.46 / 65.05 | 64.41 / 59.78 |

## real_tune / z100  (n=6 images, 649 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 95.22 / 99.25 | 94.61 / 99.02 | 95.84 / 99.25 | 94.61 / 99.02 |
| v2raw | 95.99 / 99.53 | 96.30 / 99.37 | 96.92 / 99.53 | 96.61 / 99.37 |
| v2lex | 95.07 / 99.21 | 95.99 / 99.25 | 95.99 / 99.21 | 96.30 / 99.25 |
| ocr2/auto | 98.15 / 99.33 | 98.15 / 99.25 | 98.15 / 99.33 | 98.15 / 99.25 |
| ocr2/raw | 98.61 / 99.57 | 98.46 / 99.45 | 98.61 / 99.57 | 98.46 / 99.45 |
| ocr2/lex | 98.15 / 99.33 | 98.15 / 99.25 | 98.15 / 99.33 | 98.15 / 99.25 |

Strict F1 % (numbers incl. separators, 9 in ref / punctuation marks, 82 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 45.71 / 49.14 | 48.65 / 48.62 | 51.61 / 51.81 | 48.65 / 48.62 |
| v2raw | 46.15 / 64.17 | 51.43 / 60.32 | 54.55 / 69.36 | 54.55 / 61.62 |
| v2lex | 46.15 / 64.17 | 51.43 / 60.32 | 54.55 / 69.36 | 54.55 / 61.62 |
| ocr2/auto | 78.26 / 71.08 | 85.71 / 64.44 | 78.26 / 71.08 | 85.71 / 64.44 |
| ocr2/raw | 78.26 / 71.08 | 85.71 / 64.44 | 78.26 / 71.08 | 85.71 / 64.44 |
| ocr2/lex | 78.26 / 71.08 | 85.71 / 64.44 | 78.26 / 71.08 | 85.71 / 64.44 |

## real_tune / z100+z75  (n=12 images, 1298 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 90.52 / 97.90 | 91.06 / 97.92 | 90.91 / 97.90 | 91.06 / 97.92 |
| v2raw | 90.83 / 98.11 | 91.14 / 98.13 | 91.60 / 98.11 | 91.68 / 98.13 |
| v2lex | 92.84 / 98.57 | 92.76 / 98.45 | 93.61 / 98.57 | 93.30 / 98.45 |
| ocr2/auto | 95.22 / 98.59 | 94.92 / 98.55 | 95.22 / 98.59 | 94.92 / 98.55 |
| ocr2/raw | 92.99 / 98.13 | 93.07 / 98.19 | 92.99 / 98.13 | 93.07 / 98.19 |
| ocr2/lex | 95.22 / 98.59 | 94.92 / 98.55 | 95.22 / 98.59 | 94.92 / 98.55 |

Strict F1 % (numbers incl. separators, 18 in ref / punctuation marks, 164 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 37.68 / 48.45 | 44.78 / 48.88 | 40.62 / 50.00 | 44.78 / 48.88 |
| v2raw | 48.00 / 66.48 | 50.75 / 62.73 | 55.38 / 70.76 | 56.67 / 65.18 |
| v2lex | 48.00 / 66.48 | 50.75 / 62.73 | 55.38 / 70.76 | 56.67 / 65.18 |
| ocr2/auto | 76.60 / 73.49 | 79.07 / 66.86 | 76.60 / 73.49 | 79.07 / 66.86 |
| ocr2/raw | 76.60 / 73.49 | 79.07 / 66.86 | 76.60 / 73.49 | 79.07 / 66.86 |
| ocr2/lex | 76.60 / 73.49 | 79.07 / 66.86 | 76.60 / 73.49 | 79.07 / 66.86 |

## real_tune / z50  (n=6 images, 649 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 42.06 / 80.13 | 44.38 / 80.60 | 42.06 / 80.13 | 44.38 / 80.60 |
| v2raw | 34.05 / 61.12 | 35.29 / 63.28 | 34.05 / 61.12 | 35.29 / 63.28 |
| v2lex | 40.68 / 62.37 | 41.60 / 63.55 | 40.68 / 62.37 | 41.60 / 63.55 |
| ocr2/auto | 40.83 / 62.25 | 42.53 / 63.63 | 40.83 / 62.25 | 42.53 / 63.63 |
| ocr2/raw | 34.05 / 60.88 | 35.44 / 62.80 | 34.05 / 60.88 | 35.44 / 62.80 |
| ocr2/lex | 40.83 / 62.25 | 42.53 / 63.63 | 40.83 / 62.25 | 42.53 / 63.63 |

Strict F1 % (numbers incl. separators, 9 in ref / punctuation marks, 82 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 12.12 / 39.74 | 0.00 / 34.33 | 12.12 / 39.74 | 0.00 / 34.33 |
| v2raw | 9.52 / 43.90 | 10.00 / 39.29 | 9.52 / 43.90 | 10.00 / 39.29 |
| v2lex | 9.52 / 43.90 | 10.00 / 39.29 | 9.52 / 43.90 | 10.00 / 39.29 |
| ocr2/auto | 11.11 / 42.28 | 25.00 / 37.50 | 11.11 / 42.28 | 25.00 / 37.50 |
| ocr2/raw | 11.11 / 42.28 | 25.00 / 37.50 | 11.11 / 42.28 | 25.00 / 37.50 |
| ocr2/lex | 11.11 / 42.28 | 25.00 / 37.50 | 11.11 / 42.28 | 25.00 / 37.50 |

## real_tune / z75  (n=6 images, 649 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 85.82 / 96.54 | 87.52 / 96.82 | 85.98 / 96.54 | 87.52 / 96.82 |
| v2raw | 85.67 / 96.70 | 85.98 / 96.90 | 86.29 / 96.70 | 86.75 / 96.90 |
| v2lex | 90.60 / 97.92 | 89.52 / 97.64 | 91.22 / 97.92 | 90.29 / 97.64 |
| ocr2/auto | 92.30 / 97.84 | 91.68 / 97.84 | 92.30 / 97.84 | 91.68 / 97.84 |
| ocr2/raw | 87.37 / 96.70 | 87.67 / 96.94 | 87.37 / 96.70 | 87.67 / 96.94 |
| ocr2/lex | 92.30 / 97.84 | 91.68 / 97.84 | 92.30 / 97.84 | 91.68 / 97.84 |

Strict F1 % (numbers incl. separators, 9 in ref / punctuation marks, 82 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 29.41 / 47.78 | 40.00 / 49.14 | 30.30 / 48.31 | 40.00 / 49.14 |
| v2raw | 50.00 / 68.93 | 50.00 / 65.22 | 56.25 / 72.19 | 59.26 / 68.97 |
| v2lex | 50.00 / 68.93 | 50.00 / 65.22 | 56.25 / 72.19 | 59.26 / 68.97 |
| ocr2/auto | 75.00 / 75.90 | 72.73 / 69.36 | 75.00 / 75.90 | 72.73 / 69.36 |
| ocr2/raw | 75.00 / 75.90 | 72.73 / 69.36 | 75.00 / 75.90 | 72.73 / 69.36 |
| ocr2/lex | 75.00 / 75.90 | 72.73 / 69.36 | 75.00 / 75.90 | 72.73 / 69.36 |

## real_final / all  (n=18 images, 1791 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 70.97 / 90.85 | 72.08 / 90.82 | 71.25 / 90.85 | 72.25 / 90.82 |
| v2raw | 68.40 / 82.48 | 68.96 / 83.16 | 69.35 / 82.48 | 69.51 / 83.16 |
| v2lex | 71.41 / 82.83 | 71.75 / 83.47 | 72.36 / 82.83 | 72.31 / 83.47 |
| ocr2/auto | 73.31 / 82.95 | 74.15 / 83.70 | 73.65 / 82.95 | 74.37 / 83.70 |
| ocr2/raw | 70.24 / 82.54 | 71.02 / 83.26 | 70.58 / 82.54 | 71.25 / 83.26 |
| ocr2/lex | 73.31 / 82.95 | 74.15 / 83.70 | 73.65 / 82.95 | 74.37 / 83.70 |

Strict F1 % (numbers incl. separators, 51 in ref / punctuation marks, 183 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 35.16 / 37.25 | 38.60 / 35.38 | 36.16 / 38.10 | 39.29 / 35.91 |
| v2raw | 36.99 / 56.28 | 36.36 / 52.55 | 41.03 / 61.71 | 38.71 / 55.81 |
| v2lex | 36.99 / 56.28 | 36.36 / 52.55 | 41.03 / 61.71 | 38.71 / 55.81 |
| ocr2/auto | 46.40 / 62.40 | 47.86 / 56.04 | 48.74 / 64.55 | 49.56 / 57.22 |
| ocr2/raw | 46.40 / 62.40 | 47.86 / 56.04 | 48.74 / 64.55 | 49.56 / 57.22 |
| ocr2/lex | 46.40 / 62.40 | 47.86 / 56.04 | 48.74 / 64.55 | 49.56 / 57.22 |

## real_final / z100  (n=6 images, 597 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 91.96 / 99.26 | 91.12 / 98.97 | 92.63 / 99.26 | 91.29 / 98.97 |
| v2raw | 92.13 / 99.47 | 90.28 / 99.26 | 94.30 / 99.47 | 91.46 / 99.26 |
| v2lex | 92.46 / 99.51 | 90.62 / 99.30 | 94.64 / 99.51 | 91.79 / 99.30 |
| ocr2/auto | 96.98 / 99.55 | 95.14 / 99.34 | 97.65 / 99.55 | 95.48 / 99.34 |
| ocr2/raw | 96.65 / 99.51 | 95.14 / 99.38 | 97.32 / 99.51 | 95.48 / 99.38 |
| ocr2/lex | 96.98 / 99.55 | 95.14 / 99.34 | 97.65 / 99.55 | 95.48 / 99.34 |

Strict F1 % (numbers incl. separators, 17 in ref / punctuation marks, 61 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 47.06 / 42.11 | 48.48 / 44.00 | 50.00 / 44.14 | 49.23 / 44.59 |
| v2raw | 46.38 / 58.82 | 45.07 / 52.87 | 57.14 / 69.93 | 50.00 / 58.23 |
| v2lex | 46.38 / 58.82 | 45.07 / 52.87 | 57.14 / 69.93 | 50.00 / 58.23 |
| ocr2/auto | 76.19 / 72.86 | 78.05 / 58.23 | 84.21 / 77.27 | 82.05 / 59.74 |
| ocr2/raw | 76.19 / 72.86 | 78.05 / 58.23 | 84.21 / 77.27 | 82.05 / 59.74 |
| ocr2/lex | 76.19 / 72.86 | 78.05 / 58.23 | 84.21 / 77.27 | 82.05 / 59.74 |

## real_final / z100+z75  (n=12 images, 1194 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 87.44 / 98.05 | 87.60 / 98.01 | 87.86 / 98.05 | 87.86 / 98.01 |
| v2raw | 87.10 / 98.07 | 86.68 / 98.03 | 88.53 / 98.07 | 87.52 / 98.03 |
| v2lex | 89.20 / 98.46 | 88.78 / 98.42 | 90.62 / 98.46 | 89.61 / 98.42 |
| ocr2/auto | 92.13 / 98.36 | 92.21 / 98.69 | 92.63 / 98.36 | 92.55 / 98.69 |
| ocr2/raw | 89.87 / 97.97 | 89.70 / 98.15 | 90.37 / 97.97 | 90.03 / 98.15 |
| ocr2/lex | 92.13 / 98.36 | 92.21 / 98.69 | 92.63 / 98.36 | 92.55 / 98.69 |

Strict F1 % (numbers incl. separators, 34 in ref / punctuation marks, 122 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 44.27 / 40.26 | 46.77 / 40.52 | 46.03 / 41.50 | 47.93 / 41.33 |
| v2raw | 41.18 / 61.34 | 40.60 / 57.41 | 47.06 / 69.06 | 43.90 / 62.00 |
| v2lex | 41.18 / 61.34 | 40.60 / 57.41 | 47.06 / 69.06 | 43.90 / 62.00 |
| ocr2/auto | 60.87 / 70.63 | 59.09 / 62.25 | 65.12 / 73.93 | 61.90 / 63.95 |
| ocr2/raw | 60.87 / 70.63 | 59.09 / 62.25 | 65.12 / 73.93 | 61.90 / 63.95 |
| ocr2/lex | 60.87 / 70.63 | 59.09 / 62.25 | 65.12 / 73.93 | 61.90 / 63.95 |

## real_final / z50  (n=6 images, 597 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 38.02 / 76.46 | 41.04 / 76.46 | 38.02 / 76.46 | 41.04 / 76.46 |
| v2raw | 30.99 / 51.31 | 33.50 / 53.41 | 30.99 / 51.31 | 33.50 / 53.41 |
| v2lex | 35.85 / 51.56 | 37.69 / 53.57 | 35.85 / 51.56 | 37.69 / 53.57 |
| ocr2/auto | 35.68 / 52.14 | 38.02 / 53.74 | 35.68 / 52.14 | 38.02 / 53.74 |
| ocr2/raw | 30.99 / 51.68 | 33.67 / 53.49 | 30.99 / 51.68 | 33.67 / 53.49 |
| ocr2/lex | 35.68 / 52.14 | 38.02 / 53.74 | 35.68 / 52.14 | 38.02 / 53.74 |

Strict F1 % (numbers incl. separators, 17 in ref / punctuation marks, 61 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 11.76 / 28.57 | 17.02 / 19.80 | 11.76 / 28.57 | 17.02 / 19.80 |
| v2raw | 21.62 / 37.65 | 18.75 / 34.48 | 21.62 / 37.65 | 18.75 / 34.48 |
| v2lex | 21.62 / 37.65 | 18.75 / 34.48 | 21.62 / 37.65 | 18.75 / 34.48 |
| ocr2/auto | 6.06 / 37.78 | 13.79 / 34.48 | 6.06 / 37.78 | 13.79 / 34.48 |
| ocr2/raw | 6.06 / 37.78 | 13.79 / 34.48 | 6.06 / 37.78 | 13.79 / 34.48 |
| ocr2/lex | 6.06 / 37.78 | 13.79 / 34.48 | 6.06 / 37.78 | 13.79 / 34.48 |

## real_final / z75  (n=6 images, 597 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 82.91 / 96.84 | 84.09 / 97.04 | 83.08 / 96.84 | 84.42 / 97.04 |
| v2raw | 82.08 / 96.67 | 83.08 / 96.80 | 82.75 / 96.67 | 83.58 / 96.80 |
| v2lex | 85.93 / 97.41 | 86.93 / 97.53 | 86.60 / 97.41 | 87.44 / 97.53 |
| ocr2/auto | 87.27 / 97.17 | 89.28 / 98.03 | 87.60 / 97.17 | 89.61 / 98.03 |
| ocr2/raw | 83.08 / 96.43 | 84.25 / 96.92 | 83.42 / 96.43 | 84.59 / 96.92 |
| ocr2/lex | 87.27 / 97.17 | 89.28 / 98.03 | 87.60 / 97.17 | 89.61 / 98.03 |

Strict F1 % (numbers incl. separators, 17 in ref / punctuation marks, 61 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 41.27 / 38.41 | 44.83 / 37.18 | 41.94 / 38.93 | 46.43 / 38.16 |
| v2raw | 35.82 / 64.34 | 35.48 / 62.67 | 38.10 / 68.15 | 37.29 / 66.20 |
| v2lex | 35.82 / 64.34 | 35.48 / 62.67 | 38.10 / 68.15 | 37.29 / 66.20 |
| ocr2/auto | 48.00 / 68.22 | 42.55 / 66.67 | 50.00 / 70.40 | 44.44 / 68.57 |
| ocr2/raw | 48.00 / 68.22 | 42.55 / 66.67 | 50.00 / 70.40 | 44.44 / 68.57 |
| ocr2/lex | 48.00 / 68.22 | 42.55 / 66.67 | 50.00 / 70.40 | 44.44 / 68.57 |

# Product engine (ocr2): all metrics, raw view

word / letter accuracy %, numbers F1 %, punctuation F1 %, mean seconds per image (this machine, all CPU cores, images one at a time).


## client / all  (n=2 images, 672 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 98.07 | 99.66 | 42.86 | 63.87 | 5.76 |
| base | raw | 95.98 | 99.12 | 42.86 | 63.87 | 5.64 |
| base | lex | 98.07 | 99.66 | 42.86 | 63.87 | 5.64 |
| ft | auto | 97.62 | 99.43 | 30.77 | 58.13 | 5.75 |
| ft | raw | 95.39 | 98.93 | 30.77 | 58.13 | 5.73 |
| ft | lex | 97.62 | 99.43 | 30.77 | 58.13 | 5.73 |

## client / client  (n=2 images, 672 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 98.07 | 99.66 | 42.86 | 63.87 | 5.76 |
| base | raw | 95.98 | 99.12 | 42.86 | 63.87 | 5.64 |
| base | lex | 98.07 | 99.66 | 42.86 | 63.87 | 5.64 |
| ft | auto | 97.62 | 99.43 | 30.77 | 58.13 | 5.75 |
| ft | raw | 95.39 | 98.93 | 30.77 | 58.13 | 5.73 |
| ft | lex | 97.62 | 99.43 | 30.77 | 58.13 | 5.73 |

## real_tune / all  (n=18 images, 1947 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 77.09 | 86.48 | 58.46 | 65.05 | 1.56 |
| base | raw | 73.34 | 85.72 | 58.46 | 65.05 | 1.52 |
| base | lex | 77.09 | 86.48 | 58.46 | 65.05 | 1.52 |
| ft | auto | 77.45 | 86.91 | 64.41 | 59.78 | 1.54 |
| ft | raw | 73.86 | 86.40 | 64.41 | 59.78 | 1.51 |
| ft | lex | 77.45 | 86.91 | 64.41 | 59.78 | 1.51 |

## real_tune / z100  (n=6 images, 649 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 98.15 | 99.33 | 78.26 | 71.08 | 1.74 |
| base | raw | 98.61 | 99.57 | 78.26 | 71.08 | 1.73 |
| base | lex | 98.15 | 99.33 | 78.26 | 71.08 | 1.73 |
| ft | auto | 98.15 | 99.25 | 85.71 | 64.44 | 1.73 |
| ft | raw | 98.46 | 99.45 | 85.71 | 64.44 | 1.73 |
| ft | lex | 98.15 | 99.25 | 85.71 | 64.44 | 1.73 |

## real_tune / z100+z75  (n=12 images, 1298 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 95.22 | 98.59 | 76.60 | 73.49 | 1.67 |
| base | raw | 92.99 | 98.13 | 76.60 | 73.49 | 1.64 |
| base | lex | 95.22 | 98.59 | 76.60 | 73.49 | 1.64 |
| ft | auto | 94.92 | 98.55 | 79.07 | 66.86 | 1.65 |
| ft | raw | 93.07 | 98.19 | 79.07 | 66.86 | 1.65 |
| ft | lex | 94.92 | 98.55 | 79.07 | 66.86 | 1.65 |

## real_tune / z50  (n=6 images, 649 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 40.83 | 62.25 | 11.11 | 42.28 | 1.35 |
| base | raw | 34.05 | 60.88 | 11.11 | 42.28 | 1.26 |
| base | lex | 40.83 | 62.25 | 11.11 | 42.28 | 1.27 |
| ft | auto | 42.53 | 63.63 | 25.00 | 37.50 | 1.31 |
| ft | raw | 35.44 | 62.80 | 25.00 | 37.50 | 1.24 |
| ft | lex | 42.53 | 63.63 | 25.00 | 37.50 | 1.24 |

## real_tune / z75  (n=6 images, 649 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 92.30 | 97.84 | 75.00 | 75.90 | 1.59 |
| base | raw | 87.37 | 96.70 | 75.00 | 75.90 | 1.56 |
| base | lex | 92.30 | 97.84 | 75.00 | 75.90 | 1.56 |
| ft | auto | 91.68 | 97.84 | 72.73 | 69.36 | 1.57 |
| ft | raw | 87.67 | 96.94 | 72.73 | 69.36 | 1.56 |
| ft | lex | 91.68 | 97.84 | 72.73 | 69.36 | 1.56 |

## real_final / all  (n=18 images, 1791 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 73.31 | 82.95 | 46.40 | 62.40 | 1.37 |
| base | raw | 70.24 | 82.54 | 46.40 | 62.40 | 1.31 |
| base | lex | 73.31 | 82.95 | 46.40 | 62.40 | 1.31 |
| ft | auto | 74.15 | 83.70 | 47.86 | 56.04 | 1.33 |
| ft | raw | 71.02 | 83.26 | 47.86 | 56.04 | 1.31 |
| ft | lex | 74.15 | 83.70 | 47.86 | 56.04 | 1.31 |

## real_final / z100  (n=6 images, 597 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 96.98 | 99.55 | 76.19 | 72.86 | 1.64 |
| base | raw | 96.65 | 99.51 | 76.19 | 72.86 | 1.61 |
| base | lex | 96.98 | 99.55 | 76.19 | 72.86 | 1.61 |
| ft | auto | 95.14 | 99.34 | 78.05 | 58.23 | 1.61 |
| ft | raw | 95.14 | 99.38 | 78.05 | 58.23 | 1.61 |
| ft | lex | 95.14 | 99.34 | 78.05 | 58.23 | 1.61 |

## real_final / z100+z75  (n=12 images, 1194 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 92.13 | 98.36 | 60.87 | 70.63 | 1.58 |
| base | raw | 89.87 | 97.97 | 60.87 | 70.63 | 1.54 |
| base | lex | 92.13 | 98.36 | 60.87 | 70.63 | 1.54 |
| ft | auto | 92.21 | 98.69 | 59.09 | 62.25 | 1.55 |
| ft | raw | 89.70 | 98.15 | 59.09 | 62.25 | 1.54 |
| ft | lex | 92.21 | 98.69 | 59.09 | 62.25 | 1.54 |

## real_final / z50  (n=6 images, 597 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 35.68 | 52.14 | 6.06 | 37.78 | 0.93 |
| base | raw | 30.99 | 51.68 | 6.06 | 37.78 | 0.85 |
| base | lex | 35.68 | 52.14 | 6.06 | 37.78 | 0.85 |
| ft | auto | 38.02 | 53.74 | 13.79 | 34.48 | 0.89 |
| ft | raw | 33.67 | 53.49 | 13.79 | 34.48 | 0.84 |
| ft | lex | 38.02 | 53.74 | 13.79 | 34.48 | 0.84 |

## real_final / z75  (n=6 images, 597 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 87.27 | 97.17 | 48.00 | 68.22 | 1.53 |
| base | raw | 83.08 | 96.43 | 48.00 | 68.22 | 1.48 |
| base | lex | 87.27 | 97.17 | 48.00 | 68.22 | 1.48 |
| ft | auto | 89.28 | 98.03 | 42.55 | 66.67 | 1.48 |
| ft | raw | 84.25 | 96.92 | 42.55 | 66.67 | 1.47 |
| ft | lex | 89.28 | 98.03 | 42.55 | 66.67 | 1.47 |
