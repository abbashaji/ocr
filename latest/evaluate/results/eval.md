# Results (micro-averaged accuracy %, word / letter)

`nomark` = citation markers like [۱۱] removed from OCR output before scoring.


## WARNINGS (check before trusting the tables)

- real_tune [base/plain]: 1/132 images returned < 30% of the reference length, e.g. 02_0_z75.jpg
- real_tune [base/v2lex]: 5/132 images returned < 30% of the reference length, e.g. 02_0_z75.jpg, 02_1_z50.jpg, 04_1_z50.jpg, 14_0_z50.jpg
- real_tune [base/v2raw]: 4/132 images returned < 30% of the reference length, e.g. 02_0_z75.jpg, 02_1_z50.jpg, 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [ft/plain]: 1/132 images returned < 30% of the reference length, e.g. 02_0_z75.jpg
- real_tune [ft/v2lex]: 3/132 images returned < 30% of the reference length, e.g. 02_0_z75.jpg, 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [ft/v2raw]: 3/132 images returned < 30% of the reference length, e.g. 02_0_z75.jpg, 14_0_z50.jpg, 14_2_z50.jpg
- real_final [base/v2lex]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [base/v2raw]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/v2lex]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/v2raw]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg


## client / all  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 82.89 / 98.24 | 92.56 / 98.09 | 82.89 / 98.24 |
| v2raw | 95.68 / 99.08 | 83.93 / 98.51 | 95.83 / 99.08 | 83.93 / 98.51 |
| v2lex | 97.92 / 99.66 | 86.16 / 98.97 | 98.07 / 99.66 | 86.16 / 98.97 |

## client / client  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 82.89 / 98.24 | 92.56 / 98.09 | 82.89 / 98.24 |
| v2raw | 95.68 / 99.08 | 83.93 / 98.51 | 95.83 / 99.08 | 83.93 / 98.51 |
| v2lex | 97.92 / 99.66 | 86.16 / 98.97 | 98.07 / 99.66 | 86.16 / 98.97 |

## real_tune / all  (n=132 images, 17217 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 75.15 / 91.22 | 66.56 / 93.12 | 75.27 / 91.22 | 66.57 / 93.12 |
| v2raw | 74.84 / 88.71 | 66.57 / 91.45 | 75.17 / 88.71 | 66.61 / 91.45 |
| v2lex | 78.11 / 89.10 | 69.07 / 91.59 | 78.44 / 89.10 | 69.10 / 91.59 |

## real_tune / z100  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 96.64 / 99.63 | 80.64 / 99.45 | 96.85 / 99.63 | 80.64 / 99.45 |
| v2raw | 97.32 / 99.82 | 81.51 / 99.70 | 97.79 / 99.82 | 81.56 / 99.70 |
| v2lex | 96.38 / 99.54 | 81.08 / 99.49 | 96.85 / 99.54 | 81.13 / 99.49 |

## real_tune / z100+z75  (n=88 images, 11478 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 91.36 / 97.76 | 77.85 / 98.16 | 91.52 / 97.76 | 77.87 / 98.16 |
| v2raw | 92.54 / 98.05 | 78.72 / 98.37 | 93.04 / 98.05 | 78.77 / 98.37 |
| v2lex | 93.88 / 98.36 | 79.15 / 98.35 | 94.37 / 98.36 | 79.20 / 98.35 |

## real_tune / z50  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 42.74 / 78.14 | 43.96 / 83.02 | 42.76 / 78.14 | 43.96 / 83.02 |
| v2raw | 39.43 / 70.04 | 42.29 / 77.60 | 39.43 / 70.04 | 42.29 / 77.60 |
| v2lex | 46.58 / 70.56 | 48.89 / 78.08 | 46.58 / 70.56 | 48.89 / 78.08 |

## real_tune / z75  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 86.08 / 95.89 | 75.07 / 96.88 | 86.20 / 95.89 | 75.10 / 96.88 |
| v2raw | 87.77 / 96.27 | 75.92 / 97.05 | 88.29 / 96.27 | 75.97 / 97.05 |
| v2lex | 91.37 / 97.19 | 77.23 / 97.22 | 91.90 / 97.19 | 77.28 / 97.22 |

## real_final / all  (n=135 images, 20334 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 73.70 / 90.42 | 64.03 / 92.37 | 73.77 / 90.42 | 64.05 / 92.37 |
| v2raw | 74.18 / 88.38 | 65.07 / 91.32 | 74.36 / 88.38 | 65.10 / 91.32 |
| v2lex | 77.42 / 88.79 | 67.66 / 91.53 | 77.61 / 88.79 | 67.68 / 91.53 |

## real_final / z100  (n=45 images, 6778 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 96.12 / 99.54 | 78.73 / 99.33 | 96.21 / 99.54 | 78.74 / 99.33 |
| v2raw | 96.83 / 99.75 | 79.64 / 99.60 | 97.20 / 99.75 | 79.67 / 99.60 |
| v2lex | 96.11 / 99.53 | 79.37 / 99.36 | 96.47 / 99.53 | 79.40 / 99.36 |

## real_final / z100+z75  (n=90 images, 13556 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 91.59 / 98.30 | 76.31 / 98.57 | 91.69 / 98.30 | 76.34 / 98.57 |
| v2raw | 92.61 / 98.59 | 77.19 / 98.83 | 92.89 / 98.59 | 77.23 / 98.83 |
| v2lex | 93.83 / 98.86 | 77.87 / 98.85 | 94.11 / 98.86 | 77.91 / 98.85 |

## real_final / z50  (n=45 images, 6778 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 37.93 / 74.65 | 39.47 / 79.97 | 37.93 / 74.65 | 39.47 / 79.97 |
| v2raw | 37.31 / 67.98 | 40.84 / 76.30 | 37.31 / 67.98 | 40.84 / 76.30 |
| v2lex | 44.61 / 68.66 | 47.23 / 76.89 | 44.61 / 68.66 | 47.23 / 76.89 |

## real_final / z75  (n=45 images, 6778 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 87.06 / 97.06 | 73.90 / 97.80 | 87.18 / 97.06 | 73.93 / 97.80 |
| v2raw | 88.39 / 97.43 | 74.74 / 98.07 | 88.58 / 97.43 | 74.79 / 98.07 |
| v2lex | 91.55 / 98.19 | 76.36 / 98.35 | 91.74 / 98.19 | 76.41 / 98.35 |

## synth / all  (n=72 images, 3696 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 86.01 / 95.46 | 78.22 / 97.35 | 86.01 / 95.46 | 78.25 / 97.35 |
| v2raw | 91.96 / 97.41 | 79.36 / 98.00 | 91.96 / 97.41 | 79.36 / 98.00 |
| v2lex | 94.62 / 98.04 | 81.66 / 98.39 | 94.62 / 98.04 | 81.66 / 98.39 |

## synth / clean  (n=36 images, 1848 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 98.11 / 99.71 | 84.15 / 99.83 | 98.11 / 99.71 | 84.20 / 99.83 |
| v2raw | 99.19 / 99.88 | 84.69 / 99.85 | 99.19 / 99.88 | 84.69 / 99.85 |
| v2lex | 99.30 / 99.91 | 84.90 / 99.74 | 99.30 / 99.91 | 84.90 / 99.74 |

## synth / low  (n=36 images, 1848 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 73.92 / 91.21 | 72.29 / 94.87 | 73.92 / 91.21 | 72.29 / 94.87 |
| v2raw | 84.74 / 94.95 | 74.03 / 96.16 | 84.74 / 94.95 | 74.03 / 96.16 |
| v2lex | 89.94 / 96.18 | 78.41 / 97.04 | 89.94 / 96.18 | 78.41 / 97.04 |
