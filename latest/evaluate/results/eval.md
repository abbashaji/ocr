# Results (micro-averaged accuracy %, word / letter)

`nomark` = citation markers like [۱۱] removed from OCR output before scoring.


## WARNINGS (check before trusting the tables)

- real_tune [base/v2lex]: 4/132 images returned < 30% of the reference length, e.g. 02_1_z50.jpg, 04_1_z50.jpg, 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [base/v2raw]: 3/132 images returned < 30% of the reference length, e.g. 02_1_z50.jpg, 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [ft/v2lex]: 2/132 images returned < 30% of the reference length, e.g. 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [ft/v2raw]: 2/132 images returned < 30% of the reference length, e.g. 14_0_z50.jpg, 14_2_z50.jpg
- real_final [base/v2lex]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [base/v2raw]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/v2lex]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/v2raw]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg


## client / all  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 94.64 / 98.81 | 92.56 / 98.09 | 94.64 / 98.81 |
| v2raw | 95.83 / 99.08 | 96.13 / 99.16 | 95.83 / 99.08 | 96.13 / 99.16 |
| v2lex | 98.07 / 99.66 | 98.07 / 99.62 | 98.07 / 99.66 | 98.07 / 99.62 |

## client / client  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 94.64 / 98.81 | 92.56 / 98.09 | 94.64 / 98.81 |
| v2raw | 95.83 / 99.08 | 96.13 / 99.16 | 95.83 / 99.08 | 96.13 / 99.16 |
| v2lex | 98.07 / 99.66 | 98.07 / 99.62 | 98.07 / 99.66 | 98.07 / 99.62 |

## real_tune / all  (n=132 images, 17217 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 75.51 / 91.59 | 81.12 / 93.98 | 75.63 / 91.59 | 81.16 / 93.98 |
| v2raw | 76.30 / 89.07 | 82.57 / 92.22 | 76.30 / 89.07 | 82.57 / 92.22 |
| v2lex | 79.59 / 89.47 | 84.90 / 92.37 | 79.59 / 89.47 | 84.90 / 92.37 |

## real_tune / z100  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 96.64 / 99.63 | 97.19 / 99.79 | 96.85 / 99.63 | 97.23 / 99.79 |
| v2raw | 99.11 / 99.83 | 99.30 / 99.84 | 99.11 / 99.83 | 99.30 / 99.84 |
| v2lex | 98.22 / 99.57 | 98.82 / 99.69 | 98.22 / 99.57 | 98.82 / 99.69 |

## real_tune / z100+z75  (n=88 images, 11478 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 91.90 / 98.32 | 95.27 / 99.28 | 92.07 / 98.32 | 95.34 / 99.28 |
| v2raw | 94.74 / 98.61 | 97.92 / 99.50 | 94.74 / 98.61 | 97.92 / 99.50 |
| v2lex | 96.04 / 98.92 | 97.87 / 99.43 | 96.04 / 98.92 | 97.87 / 99.43 |

## real_tune / z50  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 42.74 / 78.14 | 52.81 / 83.38 | 42.76 / 78.14 | 52.81 / 83.38 |
| v2raw | 39.43 / 69.99 | 51.87 / 77.66 | 39.43 / 69.99 | 51.87 / 77.66 |
| v2lex | 46.70 / 70.57 | 58.95 / 78.24 | 46.70 / 70.57 | 58.95 / 78.24 |

## real_tune / z75  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 87.16 / 97.01 | 93.34 / 98.77 | 87.30 / 97.01 | 93.45 / 98.77 |
| v2raw | 90.36 / 97.39 | 96.53 / 99.16 | 90.36 / 97.39 | 96.53 / 99.16 |
| v2lex | 93.85 / 98.27 | 96.93 / 99.17 | 93.85 / 98.27 | 96.93 / 99.17 |

## real_final / all  (n=135 images, 20334 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 73.70 / 90.42 | 79.59 / 92.88 | 73.77 / 90.42 | 79.61 / 92.88 |
| v2raw | 75.26 / 88.44 | 82.01 / 91.64 | 75.26 / 88.44 | 82.02 / 91.64 |
| v2lex | 78.52 / 88.83 | 84.37 / 91.87 | 78.52 / 88.83 | 84.38 / 91.87 |

## real_final / z100  (n=45 images, 6778 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 96.12 / 99.54 | 97.05 / 99.72 | 96.21 / 99.54 | 97.11 / 99.72 |
| v2raw | 98.67 / 99.78 | 99.31 / 99.84 | 98.67 / 99.78 | 99.31 / 99.84 |
| v2lex | 97.96 / 99.58 | 98.82 / 99.70 | 97.96 / 99.58 | 98.82 / 99.70 |

## real_final / z100+z75  (n=90 images, 13556 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 91.59 / 98.30 | 95.26 / 99.26 | 91.69 / 98.30 | 95.29 / 99.26 |
| v2raw | 94.16 / 98.61 | 97.76 / 99.47 | 94.16 / 98.61 | 97.76 / 99.47 |
| v2lex | 95.40 / 98.89 | 97.80 / 99.44 | 95.40 / 98.89 | 97.81 / 99.44 |

## real_final / z50  (n=45 images, 6778 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 37.93 / 74.65 | 48.24 / 80.13 | 37.93 / 74.65 | 48.24 / 80.13 |
| v2raw | 37.46 / 68.10 | 50.52 / 75.99 | 37.46 / 68.10 | 50.52 / 75.99 |
| v2lex | 44.76 / 68.73 | 57.51 / 76.74 | 44.76 / 68.73 | 57.51 / 76.74 |

## real_final / z75  (n=45 images, 6778 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 87.06 / 97.06 | 93.48 / 98.79 | 87.18 / 97.06 | 93.48 / 98.79 |
| v2raw | 89.66 / 97.43 | 96.21 / 99.10 | 89.66 / 97.43 | 96.22 / 99.10 |
| v2lex | 92.84 / 98.19 | 96.78 / 99.18 | 92.84 / 98.19 | 96.80 / 99.18 |

## synth / all  (n=72 images, 3696 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 86.01 / 95.46 | 91.99 / 97.24 | 86.01 / 95.46 | 91.99 / 97.24 |
| v2raw | 91.45 / 97.43 | 92.97 / 98.10 | 91.45 / 97.43 | 92.97 / 98.10 |
| v2lex | 94.13 / 98.07 | 95.08 / 98.57 | 94.13 / 98.07 | 95.08 / 98.57 |

## synth / clean  (n=36 images, 1848 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 98.11 / 99.71 | 99.03 / 99.86 | 98.11 / 99.71 | 99.03 / 99.86 |
| v2raw | 98.92 / 99.88 | 98.97 / 99.88 | 98.92 / 99.88 | 98.97 / 99.88 |
| v2lex | 99.03 / 99.91 | 99.13 / 99.92 | 99.03 / 99.91 | 99.13 / 99.92 |

## synth / low  (n=36 images, 1848 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 73.92 / 91.21 | 84.96 / 94.61 | 73.92 / 91.21 | 84.96 / 94.61 |
| v2raw | 83.98 / 94.98 | 86.96 / 96.32 | 83.98 / 94.98 | 86.96 / 96.32 |
| v2lex | 89.23 / 96.22 | 91.02 / 97.21 | 89.23 / 96.22 | 91.02 / 97.21 |
