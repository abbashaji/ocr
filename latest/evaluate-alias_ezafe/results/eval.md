# Results (micro-averaged accuracy %, word / letter)

`nomark` = citation markers like [۱۱] removed from OCR output before scoring. Strict tables show numbers F1 % / punctuation F1 %.


## WARNINGS (check before trusting the tables)

- real_tune [base/plain]: 1/132 images returned < 30% of the reference length, e.g. 02_2_z100.png
- real_tune [base/v2raw]: 4/132 images returned < 30% of the reference length, e.g. 02_1_z50.jpg, 02_2_z100.png, 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [base/v2lex]: 5/132 images returned < 30% of the reference length, e.g. 02_1_z50.jpg, 02_2_z100.png, 04_1_z50.jpg, 14_0_z50.jpg
- real_tune [base/ocr2/auto]: 4/132 images returned < 30% of the reference length, e.g. 02_1_z50.jpg, 02_2_z100.png, 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [base/ocr2/raw]: 4/132 images returned < 30% of the reference length, e.g. 02_1_z50.jpg, 02_2_z100.png, 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [base/ocr2/lex]: 4/132 images returned < 30% of the reference length, e.g. 02_1_z50.jpg, 02_2_z100.png, 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [ft/plain]: 1/132 images returned < 30% of the reference length, e.g. 02_2_z100.png
- real_tune [ft/v2raw]: 3/132 images returned < 30% of the reference length, e.g. 02_2_z100.png, 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [ft/v2lex]: 3/132 images returned < 30% of the reference length, e.g. 02_2_z100.png, 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [ft/ocr2/auto]: 3/132 images returned < 30% of the reference length, e.g. 02_2_z100.png, 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [ft/ocr2/raw]: 3/132 images returned < 30% of the reference length, e.g. 02_2_z100.png, 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [ft/ocr2/lex]: 3/132 images returned < 30% of the reference length, e.g. 02_2_z100.png, 14_0_z50.jpg, 14_2_z50.jpg
- real_final [base/v2raw]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [base/v2lex]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [base/ocr2/auto]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [base/ocr2/raw]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [base/ocr2/lex]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/v2raw]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/v2lex]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/ocr2/auto]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/ocr2/raw]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/ocr2/lex]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg


## client / all  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 85.57 / 98.97 | 92.56 / 98.09 | 85.57 / 98.97 |
| v2raw | 95.68 / 99.08 | 85.12 / 99.12 | 95.83 / 99.08 | 85.12 / 99.12 |
| v2lex | 97.92 / 99.66 | 86.90 / 99.39 | 98.07 / 99.66 | 86.90 / 99.39 |
| ocr2/auto | 98.07 / 99.66 | 87.20 / 99.54 | 98.07 / 99.66 | 87.20 / 99.54 |
| ocr2/raw | 95.98 / 99.12 | 86.01 / 99.31 | 95.98 / 99.12 | 86.01 / 99.31 |
| ocr2/lex | 98.07 / 99.66 | 87.20 / 99.43 | 98.07 / 99.66 | 87.20 / 99.43 |

Strict F1 % (numbers incl. separators, 6 in ref / punctuation marks, 96 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 15.38 / 32.29 | 57.14 / 82.98 | 15.38 / 32.29 | 57.14 / 82.98 |
| v2raw | 26.67 / 63.21 | 42.86 / 86.63 | 28.57 / 63.87 | 42.86 / 86.63 |
| v2lex | 26.67 / 63.21 | 42.86 / 86.63 | 28.57 / 63.87 | 42.86 / 86.63 |
| ocr2/auto | 42.86 / 63.87 | 46.15 / 86.17 | 42.86 / 63.87 | 46.15 / 86.17 |
| ocr2/raw | 42.86 / 63.87 | 46.15 / 86.17 | 42.86 / 63.87 | 46.15 / 86.17 |
| ocr2/lex | 42.86 / 63.87 | 46.15 / 86.17 | 42.86 / 63.87 | 46.15 / 86.17 |

## client / client  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 85.57 / 98.97 | 92.56 / 98.09 | 85.57 / 98.97 |
| v2raw | 95.68 / 99.08 | 85.12 / 99.12 | 95.83 / 99.08 | 85.12 / 99.12 |
| v2lex | 97.92 / 99.66 | 86.90 / 99.39 | 98.07 / 99.66 | 86.90 / 99.39 |
| ocr2/auto | 98.07 / 99.66 | 87.20 / 99.54 | 98.07 / 99.66 | 87.20 / 99.54 |
| ocr2/raw | 95.98 / 99.12 | 86.01 / 99.31 | 95.98 / 99.12 | 86.01 / 99.31 |
| ocr2/lex | 98.07 / 99.66 | 87.20 / 99.43 | 98.07 / 99.66 | 87.20 / 99.43 |

Strict F1 % (numbers incl. separators, 6 in ref / punctuation marks, 96 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 15.38 / 32.29 | 57.14 / 82.98 | 15.38 / 32.29 | 57.14 / 82.98 |
| v2raw | 26.67 / 63.21 | 42.86 / 86.63 | 28.57 / 63.87 | 42.86 / 86.63 |
| v2lex | 26.67 / 63.21 | 42.86 / 86.63 | 28.57 / 63.87 | 42.86 / 86.63 |
| ocr2/auto | 42.86 / 63.87 | 46.15 / 86.17 | 42.86 / 63.87 | 46.15 / 86.17 |
| ocr2/raw | 42.86 / 63.87 | 46.15 / 86.17 | 42.86 / 63.87 | 46.15 / 86.17 |
| ocr2/lex | 42.86 / 63.87 | 46.15 / 86.17 | 42.86 / 63.87 | 46.15 / 86.17 |

## real_tune / all  (n=132 images, 17217 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 74.28 / 90.47 | 67.49 / 92.66 | 74.52 / 90.47 | 67.64 / 92.66 |
| v2raw | 74.00 / 87.95 | 67.42 / 90.93 | 74.49 / 87.95 | 67.58 / 90.93 |
| v2lex | 77.30 / 88.34 | 70.29 / 91.22 | 77.80 / 88.34 | 70.45 / 91.22 |
| ocr2/auto | 78.40 / 88.39 | 70.59 / 91.37 | 78.40 / 88.39 | 70.59 / 91.37 |
| ocr2/raw | 74.94 / 87.86 | 67.66 / 90.83 | 74.94 / 87.86 | 67.66 / 90.83 |
| ocr2/lex | 78.40 / 88.39 | 70.59 / 91.35 | 78.40 / 88.39 | 70.59 / 91.35 |

Strict F1 % (numbers incl. separators, 252 in ref / punctuation marks, 2109 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 34.71 / 50.91 | 42.74 / 65.02 | 36.68 / 51.81 | 45.35 / 66.29 |
| v2raw | 39.50 / 60.93 | 48.13 / 67.51 | 44.32 / 63.58 | 50.53 / 68.62 |
| v2lex | 39.50 / 60.93 | 48.13 / 67.51 | 44.32 / 63.58 | 50.53 / 68.62 |
| ocr2/auto | 53.61 / 64.77 | 54.51 / 70.24 | 53.61 / 64.77 | 54.51 / 70.24 |
| ocr2/raw | 53.61 / 64.77 | 54.51 / 70.24 | 53.61 / 64.77 | 54.51 / 70.24 |
| ocr2/lex | 53.61 / 64.77 | 54.51 / 70.24 | 53.61 / 64.77 | 54.51 / 70.24 |

## real_tune / z100  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.91 / 96.27 | 79.14 / 96.27 | 93.34 / 96.27 | 79.23 / 96.27 |
| v2raw | 93.55 / 96.39 | 79.53 / 96.37 | 94.35 / 96.39 | 79.67 / 96.37 |
| v2lex | 92.68 / 96.13 | 79.04 / 96.05 | 93.48 / 96.13 | 79.18 / 96.05 |
| ocr2/auto | 94.79 / 96.24 | 79.87 / 96.27 | 94.79 / 96.24 | 79.87 / 96.27 |
| ocr2/raw | 95.30 / 96.41 | 80.10 / 96.36 | 95.30 / 96.41 | 80.10 / 96.36 |
| ocr2/lex | 94.79 / 96.24 | 79.70 / 96.19 | 94.79 / 96.24 | 79.70 / 96.19 |

Strict F1 % (numbers incl. separators, 84 in ref / punctuation marks, 703 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 49.49 / 53.70 | 57.94 / 76.47 | 54.48 / 55.66 | 61.60 / 77.86 |
| v2raw | 47.02 / 64.59 | 58.09 / 78.83 | 55.91 / 68.99 | 60.09 / 79.72 |
| v2lex | 47.02 / 64.59 | 58.09 / 78.83 | 55.91 / 68.99 | 60.09 / 79.72 |
| ocr2/auto | 71.57 / 70.45 | 71.50 / 81.70 | 71.57 / 70.45 | 71.50 / 81.70 |
| ocr2/raw | 71.57 / 70.45 | 71.50 / 81.70 | 71.57 / 70.45 | 71.50 / 81.70 |
| ocr2/lex | 71.57 / 70.45 | 71.50 / 81.70 | 71.57 / 70.45 | 71.50 / 81.70 |

## real_tune / z100+z75  (n=88 images, 11478 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 90.02 / 96.64 | 78.11 / 97.20 | 90.36 / 96.64 | 78.31 / 97.20 |
| v2raw | 91.23 / 96.90 | 78.81 / 97.36 | 91.97 / 96.90 | 79.03 / 97.36 |
| v2lex | 92.61 / 97.23 | 79.31 / 97.28 | 93.35 / 97.23 | 79.53 / 97.28 |
| ocr2/auto | 94.49 / 97.34 | 80.07 / 97.48 | 94.49 / 97.34 | 80.07 / 97.48 |
| ocr2/raw | 92.80 / 96.91 | 79.39 / 97.35 | 92.80 / 96.91 | 79.39 / 97.35 |
| ocr2/lex | 94.49 / 97.34 | 80.06 / 97.46 | 94.49 / 97.34 | 80.06 / 97.46 |

Strict F1 % (numbers incl. separators, 168 in ref / punctuation marks, 1406 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 43.31 / 54.31 | 52.63 / 70.74 | 46.77 / 55.66 | 57.02 / 72.49 |
| v2raw | 48.03 / 66.06 | 60.00 / 74.69 | 56.45 / 70.00 | 63.86 / 76.20 |
| v2lex | 48.03 / 66.06 | 60.00 / 74.69 | 56.45 / 70.00 | 63.86 / 76.20 |
| ocr2/auto | 71.68 / 71.83 | 74.87 / 78.17 | 71.68 / 71.83 | 74.87 / 78.17 |
| ocr2/raw | 71.68 / 71.83 | 74.87 / 78.17 | 71.68 / 71.83 | 74.87 / 78.17 |
| ocr2/lex | 71.68 / 71.83 | 74.87 / 78.17 | 71.68 / 71.83 | 74.87 / 78.17 |

## real_tune / z50  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 42.81 / 78.15 | 46.24 / 83.58 | 42.83 / 78.15 | 46.30 / 83.58 |
| v2raw | 39.54 / 70.04 | 44.62 / 78.09 | 39.54 / 70.04 | 44.69 / 78.09 |
| v2lex | 46.68 / 70.56 | 52.24 / 79.09 | 46.68 / 70.56 | 52.31 / 79.09 |
| ocr2/auto | 46.21 / 70.48 | 51.65 / 79.14 | 46.21 / 70.48 | 51.65 / 79.14 |
| ocr2/raw | 39.22 / 69.74 | 44.21 / 77.81 | 39.22 / 69.74 | 44.21 / 77.81 |
| ocr2/lex | 46.21 / 70.48 | 51.65 / 79.14 | 46.21 / 70.48 | 51.65 / 79.14 |

Strict F1 % (numbers incl. separators, 84 in ref / punctuation marks, 703 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 13.73 / 42.55 | 22.03 / 50.55 | 13.79 / 42.62 | 22.41 / 50.90 |
| v2raw | 16.59 / 45.89 | 21.50 / 48.85 | 16.59 / 45.89 | 21.90 / 49.19 |
| v2lex | 16.59 / 45.89 | 21.50 / 48.85 | 16.59 / 45.89 | 21.90 / 49.19 |
| ocr2/auto | 14.21 / 45.58 | 12.02 / 49.91 | 14.21 / 45.58 | 12.02 / 49.91 |
| ocr2/raw | 14.21 / 45.58 | 12.02 / 49.91 | 14.21 / 45.58 | 12.02 / 49.91 |
| ocr2/lex | 14.21 / 45.58 | 12.02 / 49.91 | 14.21 / 45.58 | 12.02 / 49.91 |

## real_tune / z75  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 87.12 / 97.01 | 77.07 / 98.14 | 87.38 / 97.01 | 77.38 / 98.14 |
| v2raw | 88.90 / 97.41 | 78.10 / 98.35 | 89.58 / 97.41 | 78.39 / 98.35 |
| v2lex | 92.54 / 98.34 | 79.58 / 98.51 | 93.22 / 98.34 | 79.87 / 98.51 |
| ocr2/auto | 94.20 / 98.44 | 80.26 / 98.68 | 94.20 / 98.44 | 80.26 / 98.68 |
| ocr2/raw | 90.31 / 97.42 | 78.67 / 98.34 | 90.31 / 97.42 | 78.67 / 98.34 |
| ocr2/lex | 94.20 / 98.44 | 80.41 / 98.72 | 94.20 / 98.44 | 80.41 / 98.72 |

Strict F1 % (numbers incl. separators, 84 in ref / punctuation marks, 703 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 36.63 / 54.93 | 47.11 / 65.22 | 38.76 / 55.66 | 52.05 / 67.26 |
| v2raw | 49.11 / 67.54 | 61.92 / 70.67 | 57.02 / 71.00 | 67.89 / 72.73 |
| v2lex | 49.11 / 67.54 | 61.92 / 70.67 | 57.02 / 71.00 | 67.89 / 72.73 |
| ocr2/auto | 71.79 / 73.22 | 78.31 / 74.65 | 71.79 / 73.22 | 78.31 / 74.65 |
| ocr2/raw | 71.79 / 73.22 | 78.31 / 74.65 | 71.79 / 73.22 | 78.31 / 74.65 |
| ocr2/lex | 71.79 / 73.22 | 78.31 / 74.65 | 71.79 / 73.22 | 78.31 / 74.65 |

## real_final / all  (n=135 images, 20337 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 73.79 / 90.45 | 65.97 / 92.69 | 73.89 / 90.45 | 65.99 / 92.69 |
| v2raw | 74.33 / 88.49 | 66.72 / 91.49 | 74.61 / 88.49 | 66.78 / 91.49 |
| v2lex | 77.60 / 88.92 | 69.47 / 91.67 | 77.88 / 88.92 | 69.53 / 91.67 |
| ocr2/auto | 78.41 / 88.89 | 69.92 / 91.86 | 78.44 / 88.89 | 69.94 / 91.86 |
| ocr2/raw | 75.10 / 88.39 | 67.00 / 91.46 | 75.13 / 88.39 | 67.02 / 91.46 |
| ocr2/lex | 78.41 / 88.89 | 69.85 / 91.83 | 78.44 / 88.89 | 69.86 / 91.83 |

Strict F1 % (numbers incl. separators, 291 in ref / punctuation marks, 2244 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 28.82 / 46.96 | 41.48 / 64.83 | 29.55 / 47.31 | 42.12 / 65.13 |
| v2raw | 32.93 / 59.08 | 44.81 / 67.38 | 35.20 / 60.63 | 45.77 / 67.86 |
| v2lex | 32.93 / 59.08 | 44.81 / 67.38 | 35.20 / 60.63 | 45.77 / 67.86 |
| ocr2/auto | 43.82 / 62.22 | 53.54 / 69.32 | 44.41 / 62.25 | 53.73 / 69.41 |
| ocr2/raw | 43.82 / 62.22 | 53.54 / 69.32 | 44.41 / 62.25 | 53.73 / 69.41 |
| ocr2/lex | 43.82 / 62.22 | 53.54 / 69.32 | 44.41 / 62.25 | 53.73 / 69.41 |

## real_final / z100  (n=45 images, 6779 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 96.18 / 99.55 | 80.53 / 99.52 | 96.37 / 99.55 | 80.50 / 99.52 |
| v2raw | 96.86 / 99.75 | 81.55 / 99.77 | 97.48 / 99.75 | 81.55 / 99.77 |
| v2lex | 96.12 / 99.53 | 80.99 / 99.37 | 96.74 / 99.53 | 80.99 / 99.37 |
| ocr2/auto | 98.02 / 99.59 | 81.94 / 99.64 | 98.08 / 99.59 | 81.94 / 99.64 |
| ocr2/raw | 98.64 / 99.79 | 82.14 / 99.77 | 98.70 / 99.79 | 82.14 / 99.77 |
| ocr2/lex | 98.01 / 99.59 | 81.66 / 99.52 | 98.07 / 99.59 | 81.66 / 99.52 |

Strict F1 % (numbers incl. separators, 97 in ref / punctuation marks, 748 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 41.59 / 51.29 | 59.48 / 79.64 | 43.45 / 51.92 | 59.40 / 79.77 |
| v2raw | 43.03 / 64.19 | 62.36 / 82.21 | 49.31 / 67.82 | 62.31 / 82.27 |
| v2lex | 43.03 / 64.19 | 62.36 / 82.21 | 49.31 / 67.82 | 62.31 / 82.27 |
| ocr2/auto | 66.67 / 70.50 | 82.93 / 84.08 | 68.25 / 70.83 | 83.17 / 84.13 |
| ocr2/raw | 66.67 / 70.50 | 82.93 / 84.08 | 68.25 / 70.83 | 83.17 / 84.13 |
| ocr2/lex | 66.67 / 70.50 | 82.93 / 84.08 | 68.25 / 70.83 | 83.17 / 84.13 |

## real_final / z100+z75  (n=90 images, 13558 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 91.61 / 98.31 | 77.97 / 98.75 | 91.76 / 98.31 | 78.00 / 98.75 |
| v2raw | 92.62 / 98.59 | 78.72 / 98.88 | 93.04 / 98.59 | 78.80 / 98.88 |
| v2lex | 93.84 / 98.86 | 79.30 / 98.80 | 94.26 / 98.86 | 79.38 / 98.80 |
| ocr2/auto | 95.39 / 98.87 | 80.08 / 99.04 | 95.43 / 98.87 | 80.09 / 99.04 |
| ocr2/raw | 93.95 / 98.54 | 79.25 / 98.90 | 94.00 / 98.54 | 79.27 / 98.90 |
| ocr2/lex | 95.38 / 98.87 | 79.97 / 98.99 | 95.43 / 98.87 | 79.98 / 98.99 |

Strict F1 % (numbers incl. separators, 194 in ref / punctuation marks, 1496 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 36.70 / 50.39 | 52.03 / 71.56 | 38.06 / 50.92 | 53.23 / 72.00 |
| v2raw | 39.75 / 65.92 | 55.41 / 75.76 | 43.65 / 68.36 | 57.03 / 76.43 |
| v2lex | 39.75 / 65.92 | 55.41 / 75.76 | 43.65 / 68.36 | 57.03 / 76.43 |
| ocr2/auto | 58.33 / 70.74 | 71.76 / 78.30 | 59.38 / 70.92 | 72.13 / 78.42 |
| ocr2/raw | 58.33 / 70.74 | 71.76 / 78.30 | 59.38 / 70.92 | 72.13 / 78.42 |
| ocr2/lex | 58.33 / 70.74 | 71.76 / 78.30 | 59.38 / 70.92 | 72.13 / 78.42 |

## real_final / z50  (n=45 images, 6779 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 38.16 / 74.75 | 41.97 / 80.57 | 38.16 / 74.75 | 41.98 / 80.57 |
| v2raw | 37.73 / 68.30 | 42.72 / 76.70 | 37.73 / 68.30 | 42.73 / 76.70 |
| v2lex | 45.11 / 69.04 | 49.82 / 77.41 | 45.11 / 69.04 | 49.83 / 77.41 |
| ocr2/auto | 44.46 / 68.94 | 49.61 / 77.50 | 44.46 / 68.94 | 49.62 / 77.50 |
| ocr2/raw | 37.41 / 68.07 | 42.50 / 76.60 | 37.41 / 68.07 | 42.51 / 76.60 |
| ocr2/lex | 44.46 / 68.94 | 49.61 / 77.50 | 44.46 / 68.94 | 49.62 / 77.50 |

Strict F1 % (numbers incl. separators, 97 in ref / punctuation marks, 748 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 11.15 / 37.65 | 20.15 / 46.86 | 11.15 / 37.65 | 20.22 / 46.94 |
| v2raw | 16.42 / 38.53 | 21.22 / 45.39 | 16.48 / 38.23 | 21.40 / 45.54 |
| v2lex | 16.42 / 38.53 | 21.22 / 45.39 | 16.48 / 38.23 | 21.40 / 45.54 |
| ocr2/auto | 14.29 / 38.27 | 17.43 / 45.79 | 14.35 / 37.97 | 17.51 / 45.87 |
| ocr2/raw | 14.29 / 38.27 | 17.43 / 45.79 | 14.35 / 37.97 | 17.51 / 45.87 |
| ocr2/lex | 14.29 / 38.27 | 17.43 / 45.79 | 14.35 / 37.97 | 17.51 / 45.87 |

## real_final / z75  (n=45 images, 6779 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 87.03 / 97.06 | 75.41 / 97.98 | 87.15 / 97.06 | 75.50 / 97.98 |
| v2raw | 88.39 / 97.42 | 75.90 / 97.99 | 88.61 / 97.42 | 76.06 / 97.99 |
| v2lex | 91.56 / 98.19 | 77.61 / 98.23 | 91.78 / 98.19 | 77.77 / 98.23 |
| ocr2/auto | 92.76 / 98.15 | 78.21 / 98.44 | 92.79 / 98.15 | 78.24 / 98.44 |
| ocr2/raw | 89.26 / 97.30 | 76.37 / 98.03 | 89.29 / 97.30 | 76.40 / 98.03 |
| ocr2/lex | 92.76 / 98.15 | 78.27 / 98.45 | 92.79 / 98.15 | 78.30 / 98.45 |

Strict F1 % (numbers incl. separators, 97 in ref / punctuation marks, 748 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 31.65 / 49.50 | 44.69 / 63.65 | 32.57 / 49.94 | 46.92 / 64.32 |
| v2raw | 36.36 / 67.74 | 48.94 / 69.40 | 38.28 / 68.90 | 51.88 / 70.58 |
| v2lex | 36.36 / 67.74 | 48.94 / 69.40 | 38.28 / 68.90 | 51.88 / 70.58 |
| ocr2/auto | 50.83 / 70.99 | 61.67 / 72.45 | 51.48 / 71.01 | 62.22 / 72.64 |
| ocr2/raw | 50.83 / 70.99 | 61.67 / 72.45 | 51.48 / 71.01 | 62.22 / 72.64 |
| ocr2/lex | 50.83 / 70.99 | 61.67 / 72.45 | 51.48 / 71.01 | 62.22 / 72.64 |

# Product engine (ocr2): all metrics, raw view

word / letter accuracy %, numbers F1 %, punctuation F1 %, mean seconds per image (this machine, all CPU cores, images one at a time).


## client / all  (n=2 images, 672 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 98.07 | 99.66 | 42.86 | 63.87 | 6.11 |
| base | raw | 95.98 | 99.12 | 42.86 | 63.87 | 5.99 |
| base | lex | 98.07 | 99.66 | 42.86 | 63.87 | 5.99 |
| ft | auto | 87.20 | 99.54 | 46.15 | 86.17 | 5.60 |
| ft | raw | 86.01 | 99.31 | 46.15 | 86.17 | 5.57 |
| ft | lex | 87.20 | 99.43 | 46.15 | 86.17 | 5.61 |

## client / client  (n=2 images, 672 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 98.07 | 99.66 | 42.86 | 63.87 | 6.11 |
| base | raw | 95.98 | 99.12 | 42.86 | 63.87 | 5.99 |
| base | lex | 98.07 | 99.66 | 42.86 | 63.87 | 5.99 |
| ft | auto | 87.20 | 99.54 | 46.15 | 86.17 | 5.60 |
| ft | raw | 86.01 | 99.31 | 46.15 | 86.17 | 5.57 |
| ft | lex | 87.20 | 99.43 | 46.15 | 86.17 | 5.61 |

## real_tune / all  (n=132 images, 17217 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 78.40 | 88.39 | 53.61 | 64.77 | 1.79 |
| base | raw | 74.94 | 87.86 | 53.61 | 64.77 | 1.74 |
| base | lex | 78.40 | 88.39 | 53.61 | 64.77 | 1.74 |
| ft | auto | 70.59 | 91.37 | 54.51 | 70.24 | 1.73 |
| ft | raw | 67.66 | 90.83 | 54.51 | 70.24 | 1.69 |
| ft | lex | 70.59 | 91.35 | 54.51 | 70.24 | 1.70 |

## real_tune / z100  (n=44 images, 5739 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 94.79 | 96.24 | 71.57 | 70.45 | 1.94 |
| base | raw | 95.30 | 96.41 | 71.57 | 70.45 | 1.93 |
| base | lex | 94.79 | 96.24 | 71.57 | 70.45 | 1.93 |
| ft | auto | 79.87 | 96.27 | 71.50 | 81.70 | 1.94 |
| ft | raw | 80.10 | 96.36 | 71.50 | 81.70 | 1.93 |
| ft | lex | 79.70 | 96.19 | 71.50 | 81.70 | 1.95 |

## real_tune / z100+z75  (n=88 images, 11478 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 94.49 | 97.34 | 71.68 | 71.83 | 1.88 |
| base | raw | 92.80 | 96.91 | 71.68 | 71.83 | 1.86 |
| base | lex | 94.49 | 97.34 | 71.68 | 71.83 | 1.86 |
| ft | auto | 80.07 | 97.48 | 74.87 | 78.17 | 1.88 |
| ft | raw | 79.39 | 97.35 | 74.87 | 78.17 | 1.86 |
| ft | lex | 80.06 | 97.46 | 74.87 | 78.17 | 1.87 |

## real_tune / z50  (n=44 images, 5739 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 46.21 | 70.48 | 14.21 | 45.58 | 1.60 |
| base | raw | 39.22 | 69.74 | 14.21 | 45.58 | 1.49 |
| base | lex | 46.21 | 70.48 | 14.21 | 45.58 | 1.49 |
| ft | auto | 51.65 | 79.14 | 12.02 | 49.91 | 1.44 |
| ft | raw | 44.21 | 77.81 | 12.02 | 49.91 | 1.35 |
| ft | lex | 51.65 | 79.14 | 12.02 | 49.91 | 1.35 |

## real_tune / z75  (n=44 images, 5739 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 94.20 | 98.44 | 71.79 | 73.22 | 1.82 |
| base | raw | 90.31 | 97.42 | 71.79 | 73.22 | 1.79 |
| base | lex | 94.20 | 98.44 | 71.79 | 73.22 | 1.79 |
| ft | auto | 80.26 | 98.68 | 78.31 | 74.65 | 1.81 |
| ft | raw | 78.67 | 98.34 | 78.31 | 74.65 | 1.79 |
| ft | lex | 80.41 | 98.72 | 78.31 | 74.65 | 1.79 |

## real_final / all  (n=135 images, 20337 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 78.41 | 88.89 | 43.82 | 62.22 | 2.05 |
| base | raw | 75.10 | 88.39 | 43.82 | 62.22 | 1.98 |
| base | lex | 78.41 | 88.89 | 43.82 | 62.22 | 1.98 |
| ft | auto | 69.92 | 91.86 | 53.54 | 69.32 | 1.98 |
| ft | raw | 67.00 | 91.46 | 53.54 | 69.32 | 1.92 |
| ft | lex | 69.85 | 91.83 | 53.54 | 69.32 | 1.93 |

## real_final / z100  (n=45 images, 6779 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 98.02 | 99.59 | 66.67 | 70.50 | 2.24 |
| base | raw | 98.64 | 99.79 | 66.67 | 70.50 | 2.22 |
| base | lex | 98.01 | 99.59 | 66.67 | 70.50 | 2.22 |
| ft | auto | 81.94 | 99.64 | 82.93 | 84.08 | 2.24 |
| ft | raw | 82.14 | 99.77 | 82.93 | 84.08 | 2.22 |
| ft | lex | 81.66 | 99.52 | 82.93 | 84.08 | 2.24 |

## real_final / z100+z75  (n=90 images, 13558 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 95.39 | 98.87 | 58.33 | 70.74 | 2.16 |
| base | raw | 93.95 | 98.54 | 58.33 | 70.74 | 2.13 |
| base | lex | 95.38 | 98.87 | 58.33 | 70.74 | 2.13 |
| ft | auto | 80.08 | 99.04 | 71.76 | 78.30 | 2.15 |
| ft | raw | 79.25 | 98.90 | 71.76 | 78.30 | 2.13 |
| ft | lex | 79.97 | 98.99 | 71.76 | 78.30 | 2.14 |

## real_final / z50  (n=45 images, 6779 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 44.46 | 68.94 | 14.29 | 38.27 | 1.82 |
| base | raw | 37.41 | 68.07 | 14.29 | 38.27 | 1.68 |
| base | lex | 44.46 | 68.94 | 14.29 | 38.27 | 1.68 |
| ft | auto | 49.61 | 77.50 | 17.43 | 45.79 | 1.64 |
| ft | raw | 42.50 | 76.60 | 17.43 | 45.79 | 1.51 |
| ft | lex | 49.61 | 77.50 | 17.43 | 45.79 | 1.51 |

## real_final / z75  (n=45 images, 6779 ref words)

| model | mode | word | letter | numbers F1 | punct F1 | s/image |
|---|---|---|---|---|---|---|
| base | auto | 92.76 | 98.15 | 50.83 | 70.99 | 2.08 |
| base | raw | 89.26 | 97.30 | 50.83 | 70.99 | 2.03 |
| base | lex | 92.76 | 98.15 | 50.83 | 70.99 | 2.03 |
| ft | auto | 78.21 | 98.44 | 61.67 | 72.45 | 2.06 |
| ft | raw | 76.37 | 98.03 | 61.67 | 72.45 | 2.03 |
| ft | lex | 78.27 | 98.45 | 61.67 | 72.45 | 2.03 |
