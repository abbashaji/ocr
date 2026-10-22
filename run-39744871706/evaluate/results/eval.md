# Results (micro-averaged accuracy %, word / letter)

`nomark` = citation markers like [۱۱] removed from OCR output before scoring.


## WARNINGS (check before trusting the tables)

- real_tune [base/plain]: 2/132 images returned < 30% of the reference length, e.g. 02_2_z100.png, 02_2_z75.jpg
- real_tune [base/v2lex]: 6/132 images returned < 30% of the reference length, e.g. 02_1_z50.jpg, 02_2_z100.png, 02_2_z75.jpg, 04_1_z50.jpg
- real_tune [base/v2raw]: 5/132 images returned < 30% of the reference length, e.g. 02_1_z50.jpg, 02_2_z100.png, 02_2_z75.jpg, 14_0_z50.jpg
- real_tune [ft/plain]: 2/132 images returned < 30% of the reference length, e.g. 02_2_z100.png, 02_2_z75.jpg
- real_tune [ft/v2lex]: 4/132 images returned < 30% of the reference length, e.g. 02_2_z100.png, 02_2_z75.jpg, 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [ft/v2raw]: 4/132 images returned < 30% of the reference length, e.g. 02_2_z100.png, 02_2_z75.jpg, 14_0_z50.jpg, 14_2_z50.jpg
- real_final [base/v2lex]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [base/v2raw]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/v2lex]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/v2raw]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg


## client / all  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 94.05 / 98.70 | 92.56 / 98.09 | 94.05 / 98.70 |
| v2raw | 95.83 / 99.08 | 95.39 / 99.01 | 95.83 / 99.08 | 95.39 / 99.01 |
| v2lex | 98.07 / 99.66 | 97.62 / 99.54 | 98.07 / 99.66 | 97.62 / 99.54 |

## client / client  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 94.05 / 98.70 | 92.56 / 98.09 | 94.05 / 98.70 |
| v2raw | 95.83 / 99.08 | 95.39 / 99.01 | 95.83 / 99.08 | 95.39 / 99.01 |
| v2lex | 98.07 / 99.66 | 97.62 / 99.54 | 98.07 / 99.66 | 97.62 / 99.54 |

## real_tune / all  (n=132 images, 17217 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 73.11 / 89.37 | 79.00 / 91.86 | 73.23 / 89.37 | 79.07 / 91.86 |
| v2raw | 73.90 / 86.85 | 80.75 / 90.39 | 73.90 / 86.85 | 80.75 / 90.39 |
| v2lex | 77.16 / 87.24 | 82.92 / 90.52 | 77.16 / 87.24 | 82.92 / 90.52 |

## real_tune / z100  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.89 / 96.26 | 93.59 / 96.47 | 93.10 / 96.26 | 93.67 / 96.47 |
| v2raw | 95.30 / 96.41 | 95.56 / 96.44 | 95.30 / 96.41 | 95.56 / 96.44 |
| v2lex | 94.46 / 96.16 | 95.09 / 96.31 | 94.46 / 96.16 | 95.09 / 96.31 |

## real_tune / z100+z75  (n=88 images, 11478 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 88.29 / 94.99 | 91.85 / 96.04 | 88.46 / 94.99 | 91.94 / 96.04 |
| v2raw | 91.13 / 95.28 | 94.49 / 96.26 | 91.13 / 95.28 | 94.49 / 96.26 |
| v2lex | 92.39 / 95.58 | 94.36 / 96.19 | 92.39 / 95.58 | 94.36 / 96.19 |

## real_tune / z50  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 42.74 / 78.14 | 53.32 / 83.52 | 42.76 / 78.14 | 53.34 / 83.52 |
| v2raw | 39.43 / 69.99 | 53.27 / 78.64 | 39.43 / 69.99 | 53.27 / 78.64 |
| v2lex | 46.70 / 70.57 | 60.05 / 79.18 | 46.70 / 70.57 | 60.05 / 79.18 |

## real_tune / z75  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 83.69 / 93.73 | 90.10 / 95.60 | 83.83 / 93.73 | 90.21 / 95.60 |
| v2raw | 86.97 / 94.15 | 93.41 / 96.08 | 86.97 / 94.15 | 93.41 / 96.08 |
| v2lex | 90.33 / 95.00 | 93.64 / 96.07 | 90.33 / 95.00 | 93.64 / 96.07 |

## real_final / all  (n=135 images, 20334 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 73.70 / 90.42 | 80.05 / 93.09 | 73.77 / 90.42 | 80.09 / 93.09 |
| v2raw | 75.26 / 88.44 | 82.46 / 91.99 | 75.26 / 88.44 | 82.46 / 91.99 |
| v2lex | 78.52 / 88.83 | 84.59 / 92.12 | 78.52 / 88.83 | 84.59 / 92.12 |

## real_final / z100  (n=45 images, 6778 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 96.12 / 99.54 | 96.96 / 99.74 | 96.21 / 99.54 | 97.05 / 99.74 |
| v2raw | 98.67 / 99.78 | 99.14 / 99.83 | 98.67 / 99.78 | 99.14 / 99.83 |
| v2lex | 97.96 / 99.58 | 98.54 / 99.66 | 97.96 / 99.58 | 98.54 / 99.66 |

## real_final / z100+z75  (n=90 images, 13556 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 91.59 / 98.30 | 95.45 / 99.35 | 91.69 / 98.30 | 95.51 / 99.35 |
| v2raw | 94.16 / 98.61 | 97.82 / 99.50 | 94.16 / 98.61 | 97.82 / 99.50 |
| v2lex | 95.40 / 98.89 | 97.68 / 99.43 | 95.40 / 98.89 | 97.68 / 99.43 |

## real_final / z50  (n=45 images, 6778 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 37.93 / 74.65 | 49.26 / 80.58 | 37.93 / 74.65 | 49.26 / 80.58 |
| v2raw | 37.46 / 68.10 | 51.76 / 76.97 | 37.46 / 68.10 | 51.76 / 76.97 |
| v2lex | 44.76 / 68.73 | 58.41 / 77.51 | 44.76 / 68.73 | 58.41 / 77.51 |

## real_final / z75  (n=45 images, 6778 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 87.06 / 97.06 | 93.94 / 98.96 | 87.18 / 97.06 | 93.97 / 98.96 |
| v2raw | 89.66 / 97.43 | 96.49 / 99.17 | 89.66 / 97.43 | 96.49 / 99.17 |
| v2lex | 92.84 / 98.19 | 96.81 / 99.19 | 92.84 / 98.19 | 96.81 / 99.19 |

## synth / all  (n=72 images, 3696 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 86.01 / 95.46 | 91.86 / 97.25 | 86.01 / 95.46 | 91.86 / 97.25 |
| v2raw | 91.45 / 97.43 | 92.42 / 97.92 | 91.45 / 97.43 | 92.42 / 97.92 |
| v2lex | 94.13 / 98.07 | 94.51 / 98.37 | 94.13 / 98.07 | 94.51 / 98.37 |

## synth / clean  (n=36 images, 1848 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 98.11 / 99.71 | 98.70 / 99.79 | 98.11 / 99.71 | 98.70 / 99.79 |
| v2raw | 98.92 / 99.88 | 98.65 / 99.79 | 98.92 / 99.88 | 98.65 / 99.79 |
| v2lex | 99.03 / 99.91 | 98.86 / 99.85 | 99.03 / 99.91 | 98.86 / 99.85 |

## synth / low  (n=36 images, 1848 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 73.92 / 91.21 | 85.01 / 94.72 | 73.92 / 91.21 | 85.01 / 94.72 |
| v2raw | 83.98 / 94.98 | 86.20 / 96.06 | 83.98 / 94.98 | 86.20 / 96.06 |
| v2lex | 89.23 / 96.22 | 90.15 / 96.90 | 89.23 / 96.22 | 90.15 / 96.90 |
