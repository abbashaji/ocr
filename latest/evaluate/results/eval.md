# Results (micro-averaged accuracy %, word / letter)

`nomark` = citation markers like [۱۱] removed from OCR output before scoring. Strict tables show numbers F1 % / punctuation F1 %.


## WARNINGS (check before trusting the tables)

- real_tune [base/plain]: 2/132 images returned < 30% of the reference length, e.g. 02_2_z100.png, 02_2_z50.jpg
- real_tune [base/v2lex]: 6/132 images returned < 30% of the reference length, e.g. 02_1_z50.jpg, 02_2_z100.png, 02_2_z50.jpg, 04_1_z50.jpg
- real_tune [base/v2raw]: 5/132 images returned < 30% of the reference length, e.g. 02_1_z50.jpg, 02_2_z100.png, 02_2_z50.jpg, 14_0_z50.jpg
- real_tune [ft/plain]: 2/132 images returned < 30% of the reference length, e.g. 02_2_z100.png, 02_2_z50.jpg
- real_tune [ft/v2lex]: 5/132 images returned < 30% of the reference length, e.g. 02_1_z50.jpg, 02_2_z100.png, 02_2_z50.jpg, 14_0_z50.jpg
- real_tune [ft/v2raw]: 5/132 images returned < 30% of the reference length, e.g. 02_1_z50.jpg, 02_2_z100.png, 02_2_z50.jpg, 14_0_z50.jpg
- real_final [base/v2lex]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [base/v2raw]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/v2lex]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/v2raw]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg


## client / all  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 92.56 / 98.01 | 92.56 / 98.09 | 92.56 / 98.01 |
| v2raw | 95.68 / 99.08 | 95.24 / 99.12 | 95.83 / 99.08 | 95.39 / 99.12 |
| v2lex | 97.92 / 99.66 | 97.17 / 99.62 | 98.07 / 99.66 | 97.32 / 99.62 |

Strict F1 % (numbers incl. separators, 6 in ref / punctuation marks, 96 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 15.38 / 32.29 | 30.77 / 32.29 | 15.38 / 32.29 | 30.77 / 32.29 |
| v2raw | 26.67 / 63.21 | 11.76 / 65.28 | 28.57 / 63.87 | 12.50 / 65.97 |
| v2lex | 26.67 / 63.21 | 11.76 / 65.28 | 28.57 / 63.87 | 12.50 / 65.97 |

## client / client  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 92.56 / 98.01 | 92.56 / 98.09 | 92.56 / 98.01 |
| v2raw | 95.68 / 99.08 | 95.24 / 99.12 | 95.83 / 99.08 | 95.39 / 99.12 |
| v2lex | 97.92 / 99.66 | 97.17 / 99.62 | 98.07 / 99.66 | 97.32 / 99.62 |

Strict F1 % (numbers incl. separators, 6 in ref / punctuation marks, 96 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 15.38 / 32.29 | 30.77 / 32.29 | 15.38 / 32.29 | 30.77 / 32.29 |
| v2raw | 26.67 / 63.21 | 11.76 / 65.28 | 28.57 / 63.87 | 12.50 / 65.97 |
| v2lex | 26.67 / 63.21 | 11.76 / 65.28 | 28.57 / 63.87 | 12.50 / 65.97 |

## real_tune / all  (n=132 images, 17217 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 73.78 / 89.56 | 74.07 / 89.69 | 74.02 / 89.56 | 74.29 / 89.69 |
| v2raw | 73.36 / 86.97 | 73.75 / 87.28 | 73.85 / 86.97 | 74.28 / 87.28 |
| v2lex | 76.53 / 87.34 | 76.89 / 87.66 | 77.02 / 87.34 | 77.42 / 87.66 |

Strict F1 % (numbers incl. separators, 252 in ref / punctuation marks, 2109 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 34.79 / 50.67 | 34.12 / 50.83 | 36.77 / 51.57 | 35.96 / 51.67 |
| v2raw | 39.75 / 60.70 | 39.80 / 60.87 | 44.63 / 63.34 | 45.11 / 63.64 |
| v2lex | 39.75 / 60.70 | 39.80 / 60.87 | 44.63 / 63.34 | 45.11 / 63.64 |

## real_tune / z100  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.91 / 96.27 | 92.93 / 96.28 | 93.34 / 96.27 | 93.34 / 96.28 |
| v2raw | 93.55 / 96.39 | 93.59 / 96.39 | 94.35 / 96.39 | 94.46 / 96.39 |
| v2lex | 92.68 / 96.13 | 92.72 / 96.13 | 93.48 / 96.13 | 93.59 / 96.13 |

Strict F1 % (numbers incl. separators, 84 in ref / punctuation marks, 703 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 49.49 / 53.70 | 48.81 / 53.70 | 54.48 / 55.66 | 53.53 / 55.58 |
| v2raw | 47.02 / 64.59 | 47.33 / 64.46 | 55.91 / 68.99 | 57.26 / 69.13 |
| v2lex | 47.02 / 64.59 | 47.33 / 64.46 | 55.91 / 68.99 | 57.26 / 69.13 |

## real_tune / z100+z75  (n=88 images, 11478 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 90.02 / 96.64 | 90.19 / 96.67 | 90.36 / 96.64 | 90.52 / 96.67 |
| v2raw | 91.23 / 96.90 | 91.38 / 96.96 | 91.97 / 96.90 | 92.18 / 96.96 |
| v2lex | 92.61 / 97.23 | 92.65 / 97.25 | 93.35 / 97.23 | 93.44 / 97.25 |

Strict F1 % (numbers incl. separators, 168 in ref / punctuation marks, 1406 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 43.31 / 54.31 | 43.03 / 54.47 | 46.77 / 55.66 | 46.30 / 55.73 |
| v2raw | 48.03 / 66.06 | 48.28 / 66.04 | 56.45 / 70.00 | 57.49 / 70.16 |
| v2lex | 48.03 / 66.06 | 48.28 / 66.04 | 56.45 / 70.00 | 57.49 / 70.16 |

## real_tune / z50  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 41.31 / 75.40 | 41.82 / 75.73 | 41.33 / 75.40 | 41.84 / 75.73 |
| v2raw | 37.62 / 67.11 | 38.47 / 67.93 | 37.62 / 67.11 | 38.47 / 67.93 |
| v2lex | 44.36 / 67.56 | 45.39 / 68.49 | 44.36 / 67.56 | 45.39 / 68.49 |

Strict F1 % (numbers incl. separators, 84 in ref / punctuation marks, 703 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 13.85 / 41.64 | 12.71 / 41.81 | 13.91 / 41.71 | 12.77 / 41.88 |
| v2raw | 16.98 / 44.77 | 16.27 / 45.64 | 16.98 / 44.77 | 16.27 / 45.64 |
| v2lex | 16.98 / 44.77 | 16.27 / 45.64 | 16.98 / 44.77 | 16.27 / 45.64 |

## real_tune / z75  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 87.12 / 97.01 | 87.45 / 97.07 | 87.38 / 97.01 | 87.70 / 97.07 |
| v2raw | 88.90 / 97.41 | 89.18 / 97.52 | 89.58 / 97.41 | 89.89 / 97.52 |
| v2lex | 92.54 / 98.34 | 92.58 / 98.37 | 93.22 / 98.34 | 93.29 / 98.37 |

Strict F1 % (numbers incl. separators, 84 in ref / punctuation marks, 703 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 36.63 / 54.93 | 36.76 / 55.27 | 38.76 / 55.66 | 38.76 / 55.89 |
| v2raw | 49.11 / 67.54 | 49.29 / 67.62 | 57.02 / 71.00 | 57.74 / 71.18 |
| v2lex | 49.11 / 67.54 | 49.29 / 67.62 | 57.02 / 71.00 | 57.74 / 71.18 |

## real_final / all  (n=135 images, 20337 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 73.79 / 90.45 | 74.18 / 90.56 | 73.89 / 90.45 | 74.28 / 90.56 |
| v2raw | 74.33 / 88.49 | 74.54 / 88.70 | 74.61 / 88.49 | 74.84 / 88.70 |
| v2lex | 77.60 / 88.92 | 77.77 / 89.10 | 77.88 / 88.92 | 78.07 / 89.10 |

Strict F1 % (numbers incl. separators, 291 in ref / punctuation marks, 2244 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 28.82 / 46.96 | 29.13 / 47.16 | 29.55 / 47.31 | 29.81 / 47.57 |
| v2raw | 32.93 / 59.08 | 31.70 / 58.87 | 35.20 / 60.63 | 34.03 / 60.58 |
| v2lex | 32.93 / 59.08 | 31.70 / 58.87 | 35.20 / 60.63 | 34.03 / 60.58 |

## real_final / z100  (n=45 images, 6779 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 96.18 / 99.55 | 96.16 / 99.55 | 96.37 / 99.55 | 96.34 / 99.55 |
| v2raw | 96.86 / 99.75 | 96.89 / 99.77 | 97.48 / 99.75 | 97.49 / 99.77 |
| v2lex | 96.12 / 99.53 | 96.08 / 99.53 | 96.74 / 99.53 | 96.68 / 99.53 |

Strict F1 % (numbers incl. separators, 97 in ref / punctuation marks, 748 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 41.59 / 51.29 | 41.10 / 51.45 | 43.45 / 51.92 | 42.81 / 51.95 |
| v2raw | 43.03 / 64.19 | 42.86 / 64.28 | 49.31 / 67.82 | 48.81 / 67.82 |
| v2lex | 43.03 / 64.19 | 42.86 / 64.28 | 49.31 / 67.82 | 48.81 / 67.82 |

## real_final / z100+z75  (n=90 images, 13558 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 91.61 / 98.31 | 91.95 / 98.38 | 91.76 / 98.31 | 92.09 / 98.38 |
| v2raw | 92.62 / 98.59 | 92.62 / 98.60 | 93.04 / 98.59 | 93.06 / 98.60 |
| v2lex | 93.84 / 98.86 | 93.94 / 98.89 | 94.26 / 98.86 | 94.39 / 98.89 |

Strict F1 % (numbers incl. separators, 194 in ref / punctuation marks, 1496 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 36.70 / 50.39 | 37.48 / 50.58 | 38.06 / 50.92 | 38.76 / 51.18 |
| v2raw | 39.75 / 65.92 | 39.76 / 65.65 | 43.65 / 68.36 | 43.92 / 68.31 |
| v2lex | 39.75 / 65.92 | 39.76 / 65.65 | 43.65 / 68.36 | 43.92 / 68.31 |

## real_final / z50  (n=45 images, 6779 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 38.16 / 74.75 | 38.66 / 74.93 | 38.16 / 74.75 | 38.66 / 74.93 |
| v2raw | 37.73 / 68.30 | 38.40 / 68.91 | 37.73 / 68.30 | 38.40 / 68.91 |
| v2lex | 45.11 / 69.04 | 45.43 / 69.51 | 45.11 / 69.04 | 45.43 / 69.51 |

Strict F1 % (numbers incl. separators, 97 in ref / punctuation marks, 748 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 11.15 / 37.65 | 10.53 / 37.87 | 11.15 / 37.65 | 10.53 / 37.87 |
| v2raw | 16.42 / 38.53 | 11.99 / 38.29 | 16.48 / 38.23 | 12.03 / 37.99 |
| v2lex | 16.42 / 38.53 | 11.99 / 38.29 | 16.48 / 38.23 | 12.03 / 37.99 |

## real_final / z75  (n=45 images, 6779 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 87.03 / 97.06 | 87.73 / 97.21 | 87.15 / 97.06 | 87.84 / 97.21 |
| v2raw | 88.39 / 97.42 | 88.35 / 97.43 | 88.61 / 97.42 | 88.63 / 97.43 |
| v2lex | 91.56 / 98.19 | 91.81 / 98.25 | 91.78 / 98.19 | 92.09 / 98.25 |

Strict F1 % (numbers incl. separators, 97 in ref / punctuation marks, 748 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 31.65 / 49.50 | 33.66 / 49.72 | 32.57 / 49.94 | 34.55 / 50.42 |
| v2raw | 36.36 / 67.74 | 36.48 / 67.09 | 38.28 / 68.90 | 39.06 / 68.82 |
| v2lex | 36.36 / 67.74 | 36.48 / 67.09 | 38.28 / 68.90 | 39.06 / 68.82 |

## synth / all  (n=72 images, 3540 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 85.90 / 93.53 | 86.21 / 93.73 | 85.93 / 93.53 | 86.24 / 93.73 |
| v2raw | 91.05 / 95.43 | 90.93 / 95.37 | 91.13 / 95.43 | 90.99 / 95.37 |
| v2lex | 91.89 / 95.37 | 91.75 / 95.30 | 91.98 / 95.37 | 91.81 / 95.30 |

Strict F1 % (numbers incl. separators, 24 in ref / punctuation marks, 516 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 34.69 / 34.01 | 34.34 / 34.19 | 36.17 / 39.82 | 35.79 / 39.69 |
| v2raw | 35.79 / 58.61 | 38.30 / 57.77 | 38.20 / 70.58 | 40.45 / 69.68 |
| v2lex | 35.79 / 58.61 | 38.30 / 57.77 | 38.20 / 70.58 | 40.45 / 69.68 |

## synth / clean  (n=36 images, 1770 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 96.61 / 97.31 | 96.50 / 97.29 | 96.61 / 97.31 | 96.50 / 97.29 |
| v2raw | 97.29 / 97.51 | 97.40 / 97.54 | 97.34 / 97.51 | 97.46 / 97.54 |
| v2lex | 95.88 / 96.92 | 95.82 / 96.90 | 95.93 / 96.92 | 95.88 / 96.90 |

Strict F1 % (numbers incl. separators, 12 in ref / punctuation marks, 258 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 45.83 / 35.18 | 44.90 / 35.75 | 47.83 / 42.40 | 46.81 / 42.37 |
| v2raw | 46.81 / 60.43 | 47.83 / 59.90 | 51.16 / 73.73 | 50.00 / 72.88 |
| v2lex | 46.81 / 60.43 | 47.83 / 59.90 | 51.16 / 73.73 | 50.00 / 72.88 |

## synth / low  (n=36 images, 1770 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 75.20 / 89.75 | 75.93 / 90.16 | 75.25 / 89.75 | 75.99 / 90.16 |
| v2raw | 84.80 / 93.34 | 84.46 / 93.20 | 84.92 / 93.34 | 84.52 / 93.20 |
| v2lex | 87.91 / 93.81 | 87.68 / 93.70 | 88.02 / 93.81 | 87.74 / 93.70 |

Strict F1 % (numbers incl. separators, 12 in ref / punctuation marks, 258 in ref):

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 24.00 / 32.71 | 24.00 / 32.45 | 25.00 / 37.14 | 25.00 / 36.85 |
| v2raw | 25.00 / 56.76 | 29.17 / 55.57 | 26.09 / 67.49 | 31.11 / 66.53 |
| v2lex | 25.00 / 56.76 | 29.17 / 55.57 | 26.09 / 67.49 | 31.11 / 66.53 |
