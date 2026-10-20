# Results (micro-averaged accuracy %, word / letter)

`nomark` = citation markers like [۱۱] removed from OCR output before scoring.


## WARNINGS (check before trusting the tables)

- real_tune [base/plain]: 1/18 images returned < 30% of the reference length, e.g. 02_0_z75.jpg
- real_tune [base/v2lex]: 3/18 images returned < 30% of the reference length, e.g. 02_0_z75.jpg, 02_1_z50.jpg, 04_1_z50.jpg
- real_tune [base/v2raw]: 2/18 images returned < 30% of the reference length, e.g. 02_0_z75.jpg, 02_1_z50.jpg
- real_tune [ft/plain]: 1/18 images returned < 30% of the reference length, e.g. 02_0_z75.jpg
- real_tune [ft/v2lex]: 2/18 images returned < 30% of the reference length, e.g. 02_0_z75.jpg, 02_1_z50.jpg
- real_tune [ft/v2raw]: 2/18 images returned < 30% of the reference length, e.g. 02_0_z75.jpg, 02_1_z50.jpg
- real_final [base/v2lex]: 1/18 images returned < 30% of the reference length, e.g. 01_0_z50.jpg
- real_final [base/v2raw]: 1/18 images returned < 30% of the reference length, e.g. 01_0_z50.jpg
- real_final [ft/v2lex]: 1/18 images returned < 30% of the reference length, e.g. 01_0_z50.jpg
- real_final [ft/v2raw]: 1/18 images returned < 30% of the reference length, e.g. 01_0_z50.jpg


## client / all  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 93.90 / 98.51 | 92.56 / 98.09 | 93.90 / 98.51 |
| v2raw | 95.68 / 99.08 | 95.68 / 99.12 | 95.83 / 99.08 | 95.83 / 99.12 |
| v2lex | 97.92 / 99.66 | 97.47 / 99.50 | 98.07 / 99.66 | 97.62 / 99.50 |

## client / client  (n=2 images, 672 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 92.56 / 98.09 | 93.90 / 98.51 | 92.56 / 98.09 | 93.90 / 98.51 |
| v2raw | 95.68 / 99.08 | 95.68 / 99.12 | 95.83 / 99.08 | 95.83 / 99.12 |
| v2lex | 97.92 / 99.66 | 97.47 / 99.50 | 98.07 / 99.66 | 97.62 / 99.50 |

## real_tune / all  (n=18 images, 1947 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 71.19 / 88.82 | 72.47 / 88.99 | 71.34 / 88.82 | 72.47 / 88.99 |
| v2raw | 68.82 / 82.68 | 70.83 / 83.79 | 69.23 / 82.68 | 71.14 / 83.79 |
| v2lex | 72.32 / 83.39 | 73.91 / 84.07 | 72.73 / 83.39 | 74.22 / 84.07 |

## real_tune / z100  (n=6 images, 649 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 95.22 / 99.25 | 95.22 / 99.18 | 95.69 / 99.25 | 95.22 / 99.18 |
| v2raw | 95.99 / 99.53 | 96.76 / 99.49 | 96.76 / 99.53 | 97.23 / 99.49 |
| v2lex | 95.07 / 99.21 | 96.46 / 99.37 | 95.84 / 99.21 | 96.92 / 99.37 |

## real_tune / z100+z75  (n=12 images, 1298 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 85.75 / 93.17 | 86.83 / 93.32 | 85.98 / 93.17 | 86.83 / 93.32 |
| v2raw | 86.21 / 93.46 | 87.21 / 93.64 | 86.83 / 93.46 | 87.67 / 93.64 |
| v2lex | 88.14 / 93.89 | 88.44 / 93.87 | 88.75 / 93.89 | 88.91 / 93.87 |

## real_tune / z50  (n=6 images, 649 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 42.06 / 80.13 | 43.76 / 80.32 | 42.06 / 80.13 | 43.76 / 80.32 |
| v2raw | 34.05 / 61.12 | 38.06 / 64.10 | 34.05 / 61.12 | 38.06 / 64.10 |
| v2lex | 40.68 / 62.37 | 44.84 / 64.45 | 40.68 / 62.37 | 44.84 / 64.45 |

## real_tune / z75  (n=6 images, 649 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 76.27 / 87.08 | 78.43 / 87.47 | 76.27 / 87.08 | 78.43 / 87.47 |
| v2raw | 76.43 / 87.39 | 77.66 / 87.78 | 76.89 / 87.39 | 78.12 / 87.78 |
| v2lex | 81.20 / 88.57 | 80.43 / 88.37 | 81.66 / 88.57 | 80.89 / 88.37 |

## real_final / all  (n=18 images, 1791 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 70.97 / 90.85 | 71.97 / 91.08 | 71.13 / 90.85 | 72.14 / 91.08 |
| v2raw | 68.40 / 82.48 | 69.24 / 83.22 | 68.73 / 82.48 | 69.51 / 83.22 |
| v2lex | 71.41 / 82.83 | 73.09 / 83.95 | 71.75 / 82.83 | 73.37 / 83.95 |

## real_final / z100  (n=6 images, 597 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 91.96 / 99.26 | 91.46 / 99.18 | 92.29 / 99.26 | 91.46 / 99.18 |
| v2raw | 92.13 / 99.47 | 91.62 / 99.38 | 92.80 / 99.47 | 91.96 / 99.38 |
| v2lex | 92.46 / 99.51 | 91.79 / 99.42 | 93.13 / 99.51 | 92.13 / 99.42 |

## real_final / z100+z75  (n=12 images, 1194 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 87.44 / 98.05 | 87.86 / 98.15 | 87.69 / 98.05 | 88.11 / 98.15 |
| v2raw | 87.10 / 98.07 | 87.27 / 98.19 | 87.60 / 98.07 | 87.69 / 98.19 |
| v2lex | 89.20 / 98.46 | 90.03 / 98.87 | 89.70 / 98.46 | 90.45 / 98.87 |

## real_final / z50  (n=6 images, 597 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 38.02 / 76.46 | 40.20 / 76.95 | 38.02 / 76.46 | 40.20 / 76.95 |
| v2raw | 30.99 / 51.31 | 33.17 / 53.29 | 30.99 / 51.31 | 33.17 / 53.29 |
| v2lex | 35.85 / 51.56 | 39.20 / 54.11 | 35.85 / 51.56 | 39.20 / 54.11 |

## real_final / z75  (n=6 images, 597 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 82.91 / 96.84 | 84.25 / 97.12 | 83.08 / 96.84 | 84.76 / 97.12 |
| v2raw | 82.08 / 96.67 | 82.91 / 97.00 | 82.41 / 96.67 | 83.42 / 97.00 |
| v2lex | 85.93 / 97.41 | 88.27 / 98.32 | 86.26 / 97.41 | 88.78 / 98.32 |

## synth / all  (n=72 images, 3264 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 84.28 / 93.99 | 85.08 / 94.55 | 84.28 / 93.99 | 85.08 / 94.55 |
| v2raw | 88.39 / 95.41 | 88.54 / 95.48 | 88.39 / 95.41 | 88.54 / 95.48 |
| v2lex | 89.86 / 95.65 | 89.77 / 95.63 | 89.86 / 95.65 | 89.77 / 95.63 |

## synth / clean  (n=36 images, 1632 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 94.42 / 97.63 | 93.93 / 97.73 | 94.42 / 97.63 | 93.93 / 97.73 |
| v2raw | 95.16 / 97.37 | 94.91 / 97.42 | 95.16 / 97.37 | 94.91 / 97.42 |
| v2lex | 93.44 / 96.86 | 93.26 / 96.89 | 93.44 / 96.86 | 93.26 / 96.89 |

## synth / low  (n=36 images, 1632 ref words)

| engine | base raw | ft raw | base nomark | ft nomark |
|---|---|---|---|---|
| plain | 74.14 / 90.34 | 76.23 / 91.36 | 74.14 / 90.34 | 76.23 / 91.36 |
| v2raw | 81.62 / 93.45 | 82.17 / 93.55 | 81.62 / 93.45 | 82.17 / 93.55 |
| v2lex | 86.27 / 94.44 | 86.27 / 94.37 | 86.27 / 94.44 | 86.27 / 94.37 |
