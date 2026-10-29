# Real-scan benchmark of the shipped model (ocr2 engine)

Held-out works only (split by work). View = raw output (no citation-marker removal). word/letter = accuracy %; num/punct = F1 %.

## set `pages`

| group | mode | images | ref words | word | letter | num F1 | punct F1 | s/img |
|---|---|---|---|---|---|---|---|---|
| all | raw | 126 | 45398 | 36.39 | 85.79 | 33.46 | 51.84 | 4.53 |
| all | lex | 126 | 45398 | 37.96 | 84.0 | 33.46 | 51.84 | 4.53 |
| all | auto | 126 | 45398 | 37.96 | 84.0 | 33.46 | 51.84 | 4.72 |
| w20 | raw | 40 | 17103 | 37.58 | 82.53 | 32.73 | 48.81 | 3.78 |
| w20 | lex | 40 | 17103 | 39.12 | 81.04 | 32.73 | 48.81 | 3.78 |
| w20 | auto | 40 | 17103 | 39.12 | 81.04 | 32.73 | 48.81 | 3.93 |
| w21 | raw | 40 | 15036 | 21.39 | 92.04 | 31.03 | 56.13 | 5.18 |
| w21 | lex | 40 | 15036 | 23.81 | 89.23 | 31.03 | 56.13 | 5.18 |
| w21 | auto | 40 | 15036 | 23.81 | 89.23 | 31.03 | 56.13 | 5.39 |
| w22 | raw | 40 | 10575 | 43.53 | 80.57 | 25.45 | 44.28 | 4.28 |
| w22 | lex | 40 | 10575 | 44.22 | 79.27 | 25.45 | 44.28 | 4.28 |
| w22 | auto | 40 | 10575 | 44.22 | 79.27 | 25.45 | 44.28 | 4.46 |
| w23 | raw | 6 | 2684 | 84.69 | 94.08 | 71.84 | 67.68 | 6.97 |
| w23 | lex | 6 | 2684 | 85.17 | 93.85 | 71.84 | 67.68 | 6.97 |
| w23 | auto | 6 | 2684 | 85.17 | 93.85 | 71.84 | 67.68 | 7.14 |

## set `lines`

| group | mode | images | ref words | word | letter | num F1 | punct F1 | s/img |
|---|---|---|---|---|---|---|---|---|
| all | raw | 1013 | 15273 | 48.06 | 96.34 | 51.95 | 54.39 | - |
| all | lex | 1013 | 15273 | 49.3 | 94.55 | 51.95 | 54.39 | - |
| all | auto | 1013 | 15273 | 48.22 | 96.21 | 51.95 | 54.39 | - |
| w20 | raw | 300 | 4436 | 48.02 | 95.47 | 44.86 | 58.93 | - |
| w20 | lex | 300 | 4436 | 49.14 | 93.78 | 44.86 | 58.93 | - |
| w20 | auto | 300 | 4436 | 48.06 | 95.36 | 44.86 | 58.93 | - |
| w21 | raw | 300 | 4779 | 24.11 | 96.0 | 40.91 | 46.93 | - |
| w21 | lex | 300 | 4779 | 26.72 | 93.19 | 40.91 | 46.93 | - |
| w21 | auto | 300 | 4779 | 24.48 | 95.73 | 40.91 | 46.93 | - |
| w22 | raw | 300 | 3929 | 54.7 | 96.58 | 36.96 | 51.83 | - |
| w22 | lex | 300 | 3929 | 54.95 | 95.07 | 36.96 | 51.83 | - |
| w22 | auto | 300 | 3929 | 54.7 | 96.58 | 36.96 | 51.83 | - |
| w23 | raw | 113 | 2129 | 89.67 | 98.45 | 92.31 | 70.97 | - |
| w23 | lex | 113 | 2129 | 89.9 | 98.22 | 92.31 | 70.97 | - |
| w23 | auto | 113 | 2129 | 89.85 | 98.35 | 92.31 | 70.97 | - |

## where the errors are (mode raw): spaces vs characters

space edits = insert/delete of a word space; char acc (no spaces) = character accuracy after removing all spaces.

| set | group | space edits | other edits | space share % | char acc no spaces % |
|---|---|---|---|---|---|
| lines | all | 4626 | 3164 | 59 | 95.45 |
| lines | w20 | 1275 | 925 | 58 | 95.06 |
| lines | w21 | 2328 | 1319 | 64 | 94.67 |
| lines | w22 | 938 | 739 | 56 | 95.63 |
| lines | w23 | 85 | 181 | 32 | 97.63 |
| pages | all | 18453 | 28595 | 39 | 84.70 |
| pages | w20 | 6455 | 12237 | 35 | 81.87 |
| pages | w21 | 7868 | 6581 | 54 | 90.60 |
| pages | w22 | 3930 | 9077 | 30 | 79.25 |
| pages | w23 | 200 | 700 | 22 | 93.10 |

## warnings

- pages [ocr2/ocr2/auto]: 1/126 images returned < 30% of the reference length, e.g. w22_p0105
- pages [ocr2/ocr2/raw]: 1/126 images returned < 30% of the reference length, e.g. w22_p0105
- pages [ocr2/ocr2/lex]: 1/126 images returned < 30% of the reference length, e.g. w22_p0105
