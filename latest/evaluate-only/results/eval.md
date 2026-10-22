# Results (micro-averaged accuracy %, word / letter)

`nomark` = citation markers like [۱۱] removed from OCR output before scoring.


## WARNINGS (check before trusting the tables)

- real_tune [base/plain]: 2/132 images returned < 30% of the reference length, e.g. 02_1_z100.png, 02_1_z75.jpg
- real_tune [base/v2lex]: 6/132 images returned < 30% of the reference length, e.g. 02_1_z100.png, 02_1_z50.jpg, 02_1_z75.jpg, 04_1_z50.jpg
- real_tune [base/v2raw]: 5/132 images returned < 30% of the reference length, e.g. 02_1_z100.png, 02_1_z50.jpg, 02_1_z75.jpg, 14_0_z50.jpg
- real_tune [base/v2auto]: 6/132 images returned < 30% of the reference length, e.g. 02_1_z100.png, 02_1_z50.jpg, 02_1_z75.jpg, 04_1_z50.jpg
- real_tune [ft/plain]: 2/132 images returned < 30% of the reference length, e.g. 02_1_z100.png, 02_1_z75.jpg
- real_tune [ft/v2lex]: 4/132 images returned < 30% of the reference length, e.g. 02_1_z100.png, 02_1_z75.jpg, 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [ft/v2raw]: 4/132 images returned < 30% of the reference length, e.g. 02_1_z100.png, 02_1_z75.jpg, 14_0_z50.jpg, 14_2_z50.jpg
- real_tune [ft/v2auto]: 4/132 images returned < 30% of the reference length, e.g. 02_1_z100.png, 02_1_z75.jpg, 14_0_z50.jpg, 14_2_z50.jpg
- real_final [base/v2lex]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [base/v2raw]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [base/v2auto]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/v2lex]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/v2raw]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg
- real_final [ft/v2auto]: 2/135 images returned < 30% of the reference length, e.g. 01_0_z50.jpg, 03_2_z50.jpg


## client / all  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 94.05 / 98.70 | 92.56 / 98.09 | 94.05 / 98.70 |
| v2raw | 95.83 / 99.08 | 95.39 / 99.01 | 95.83 / 99.08 | 95.39 / 99.01 |
| v2lex | 98.07 / 99.66 | 97.62 / 99.54 | 98.07 / 99.66 | 97.62 / 99.54 |
| v2auto | 98.07 / 99.66 | 97.62 / 99.54 | 98.07 / 99.66 | 97.62 / 99.54 |

## client / client  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 94.05 / 98.70 | 92.56 / 98.09 | 94.05 / 98.70 |
| v2raw | 95.83 / 99.08 | 95.39 / 99.01 | 95.83 / 99.08 | 95.39 / 99.01 |
| v2lex | 98.07 / 99.66 | 97.62 / 99.54 | 98.07 / 99.66 | 97.62 / 99.54 |
| v2auto | 98.07 / 99.66 | 97.62 / 99.54 | 98.07 / 99.66 | 97.62 / 99.54 |

## real_tune / all  (n=132 images, 17217 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 74.32 / 90.05 | 80.21 / 92.48 | 74.44 / 90.05 | 80.28 / 92.48 |
| v2raw | 75.05 / 87.64 | 81.96 / 91.16 | 75.05 / 87.64 | 81.96 / 91.16 |
| v2lex | 78.29 / 88.01 | 84.13 / 91.30 | 78.29 / 88.01 | 84.13 / 91.30 |
| v2auto | 78.28 / 88.02 | 84.13 / 91.30 | 78.28 / 88.02 | 84.13 / 91.30 |

## real_tune / z100  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 94.82 / 97.38 | 95.45 / 97.45 | 95.03 / 97.38 | 95.52 / 97.45 |
| v2raw | 97.14 / 97.68 | 97.39 / 97.69 | 97.14 / 97.68 | 97.39 / 97.69 |
| v2lex | 96.27 / 97.41 | 96.88 / 97.55 | 96.27 / 97.41 | 96.88 / 97.55 |
| v2auto | 96.25 / 97.42 | 97.25 / 97.65 | 96.25 / 97.42 | 97.25 / 97.65 |

## real_tune / z100+z75  (n=88 images, 11478 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 90.11 / 96.01 | 93.66 / 96.96 | 90.29 / 96.01 | 93.74 / 96.96 |
| v2raw | 92.86 / 96.46 | 96.31 / 97.43 | 92.86 / 96.46 | 96.31 / 97.43 |
| v2lex | 94.08 / 96.73 | 96.17 / 97.35 | 94.08 / 96.73 | 96.17 / 97.35 |
| v2auto | 94.08 / 96.74 | 96.17 / 97.36 | 94.08 / 96.74 | 96.17 / 97.36 |

## real_tune / z50  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 42.74 / 78.14 | 53.32 / 83.52 | 42.76 / 78.14 | 53.34 / 83.52 |
| v2raw | 39.43 / 69.99 | 53.27 / 78.64 | 39.43 / 69.99 | 53.27 / 78.64 |
| v2lex | 46.70 / 70.57 | 60.05 / 79.18 | 46.70 / 70.57 | 60.05 / 79.18 |
| v2auto | 46.70 / 70.57 | 60.05 / 79.19 | 46.70 / 70.57 | 60.05 / 79.19 |

## real_tune / z75  (n=44 images, 5739 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 85.40 / 94.63 | 91.86 / 96.46 | 85.54 / 94.63 | 91.97 / 96.46 |
| v2raw | 88.59 / 95.23 | 95.23 / 97.16 | 88.59 / 95.23 | 95.23 / 97.16 |
| v2lex | 91.90 / 96.05 | 95.45 / 97.16 | 91.90 / 96.05 | 95.45 / 97.16 |
| v2auto | 91.90 / 96.07 | 95.09 / 97.08 | 91.90 / 96.07 | 95.09 / 97.08 |

## real_final / all  (n=135 images, 20337 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 73.75 / 90.44 | 80.12 / 93.10 | 73.82 / 90.44 | 80.15 / 93.10 |
| v2raw | 75.28 / 88.48 | 82.51 / 92.02 | 75.28 / 88.48 | 82.51 / 92.02 |
| v2lex | 78.59 / 88.89 | 84.65 / 92.15 | 78.59 / 88.89 | 84.65 / 92.15 |
| v2auto | 78.59 / 88.89 | 84.86 / 92.21 | 78.59 / 88.89 | 84.86 / 92.21 |

## real_final / z100  (n=45 images, 6779 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 96.12 / 99.53 | 96.99 / 99.74 | 96.21 / 99.53 | 97.06 / 99.74 |
| v2raw | 98.67 / 99.78 | 99.11 / 99.83 | 98.67 / 99.78 | 99.11 / 99.83 |
| v2lex | 97.96 / 99.58 | 98.52 / 99.65 | 97.96 / 99.58 | 98.52 / 99.65 |
| v2auto | 97.98 / 99.58 | 99.09 / 99.81 | 97.98 / 99.58 | 99.09 / 99.81 |

## real_final / z100+z75  (n=90 images, 13558 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 91.57 / 98.29 | 95.49 / 99.35 | 91.67 / 98.29 | 95.54 / 99.35 |
| v2raw | 94.13 / 98.60 | 97.79 / 99.49 | 94.13 / 98.60 | 97.79 / 99.49 |
| v2lex | 95.39 / 98.88 | 97.68 / 99.43 | 95.39 / 98.88 | 97.68 / 99.43 |
| v2auto | 95.40 / 98.89 | 97.98 / 99.51 | 95.40 / 98.89 | 97.98 / 99.51 |

## real_final / z50  (n=45 images, 6779 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 38.10 / 74.73 | 49.39 / 80.60 | 38.10 / 74.73 | 49.39 / 80.60 |
| v2raw | 37.59 / 68.25 | 51.94 / 77.07 | 37.59 / 68.25 | 51.94 / 77.07 |
| v2lex | 44.98 / 68.90 | 58.61 / 77.61 | 44.98 / 68.90 | 58.61 / 77.61 |
| v2auto | 44.98 / 68.90 | 58.61 / 77.61 | 44.98 / 68.90 | 58.61 / 77.61 |

## real_final / z75  (n=45 images, 6779 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 87.02 / 97.04 | 93.98 / 98.96 | 87.14 / 97.04 | 94.01 / 98.96 |
| v2raw | 89.59 / 97.42 | 96.47 / 99.16 | 89.59 / 97.42 | 96.47 / 99.16 |
| v2lex | 92.82 / 98.19 | 96.83 / 99.20 | 92.82 / 98.19 | 96.83 / 99.20 |
| v2auto | 92.82 / 98.19 | 96.87 / 99.22 | 92.82 / 98.19 | 96.87 / 99.22 |

## synth / all  (n=72 images, 3696 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 86.01 / 95.46 | 91.86 / 97.25 | 86.01 / 95.46 | 91.86 / 97.25 |
| v2raw | 91.45 / 97.43 | 92.42 / 97.92 | 91.45 / 97.43 | 92.42 / 97.92 |
| v2lex | 94.13 / 98.07 | 94.51 / 98.37 | 94.13 / 98.07 | 94.51 / 98.37 |
| v2auto | 94.21 / 98.09 | 94.45 / 98.37 | 94.21 / 98.09 | 94.45 / 98.37 |

## synth / clean  (n=36 images, 1848 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 98.11 / 99.71 | 98.70 / 99.79 | 98.11 / 99.71 | 98.70 / 99.79 |
| v2raw | 98.92 / 99.88 | 98.65 / 99.79 | 98.92 / 99.88 | 98.65 / 99.79 |
| v2lex | 99.03 / 99.91 | 98.86 / 99.85 | 99.03 / 99.91 | 98.86 / 99.85 |
| v2auto | 99.19 / 99.95 | 98.86 / 99.85 | 99.19 / 99.95 | 98.86 / 99.85 |

## synth / low  (n=36 images, 1848 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 73.92 / 91.21 | 85.01 / 94.72 | 73.92 / 91.21 | 85.01 / 94.72 |
| v2raw | 83.98 / 94.98 | 86.20 / 96.06 | 83.98 / 94.98 | 86.20 / 96.06 |
| v2lex | 89.23 / 96.22 | 90.15 / 96.90 | 89.23 / 96.22 | 90.15 / 96.90 |
| v2auto | 89.23 / 96.22 | 90.04 / 96.88 | 89.23 / 96.22 | 90.04 / 96.88 |
