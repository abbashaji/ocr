# Real-scan benchmark of the shipped model (ocr2 engine)

Held-out works only (split by work). View = raw output (no citation-marker removal). word/letter = accuracy %; num/punct = F1 %.

## set `pages`

| group | mode | images | ref words | word | letter | num F1 | punct F1 | s/img |
|---|---|---|---|---|---|---|---|---|
| all | raw | 126 | 45398 | 36.39 | 85.79 | 33.46 | 51.84 | 5.22 |
| all | lex | 126 | 45398 | 37.96 | 84.0 | 33.46 | 51.84 | 5.22 |
| all | auto | 126 | 45398 | 37.96 | 84.0 | 33.46 | 51.84 | 5.45 |
| w20 | raw | 40 | 17103 | 37.58 | 82.53 | 32.73 | 48.81 | 6.5 |
| w20 | lex | 40 | 17103 | 39.12 | 81.04 | 32.73 | 48.81 | 6.5 |
| w20 | auto | 40 | 17103 | 39.12 | 81.04 | 32.73 | 48.81 | 6.8 |
| w21 | raw | 40 | 15036 | 21.39 | 92.04 | 31.03 | 56.13 | 4.9 |
| w21 | lex | 40 | 15036 | 23.81 | 89.23 | 31.03 | 56.13 | 4.9 |
| w21 | auto | 40 | 15036 | 23.81 | 89.23 | 31.03 | 56.13 | 5.11 |
| w22 | raw | 40 | 10575 | 43.53 | 80.57 | 25.45 | 44.28 | 4.23 |
| w22 | lex | 40 | 10575 | 44.22 | 79.27 | 25.45 | 44.28 | 4.24 |
| w22 | auto | 40 | 10575 | 44.22 | 79.27 | 25.45 | 44.28 | 4.42 |
| w23 | raw | 6 | 2684 | 84.69 | 94.08 | 71.84 | 67.68 | 5.4 |
| w23 | lex | 6 | 2684 | 85.17 | 93.85 | 71.84 | 67.68 | 5.4 |
| w23 | auto | 6 | 2684 | 85.17 | 93.85 | 71.84 | 67.68 | 5.54 |

## set `lines`

| group | mode | images | ref words | word | letter | num F1 | punct F1 | s/img |
|---|---|---|---|---|---|---|---|---|
| all | raw | 1014 | 15418 | 48.35 | 96.35 | 50.97 | 55.74 | - |
| all | lex | 1014 | 15418 | 49.55 | 94.54 | 50.97 | 55.74 | - |
| all | auto | 1014 | 15418 | 48.44 | 96.24 | 50.97 | 55.74 | - |
| w20 | raw | 300 | 4491 | 47.94 | 95.57 | 38.38 | 62.56 | - |
| w20 | lex | 300 | 4491 | 49.01 | 94.01 | 38.38 | 62.56 | - |
| w20 | auto | 300 | 4491 | 48.03 | 95.53 | 38.38 | 62.56 | - |
| w21 | raw | 300 | 4758 | 23.29 | 96.0 | 24.39 | 50.41 | - |
| w21 | lex | 300 | 4758 | 25.33 | 92.89 | 24.39 | 50.41 | - |
| w21 | auto | 300 | 4758 | 23.43 | 95.73 | 24.39 | 50.41 | - |
| w22 | raw | 300 | 4021 | 56.35 | 96.52 | 47.62 | 48.05 | - |
| w22 | lex | 300 | 4021 | 57.22 | 95.07 | 47.62 | 48.05 | - |
| w22 | auto | 300 | 4021 | 56.33 | 96.51 | 47.62 | 48.05 | - |
| w23 | raw | 114 | 2148 | 89.76 | 98.46 | 92.31 | 70.97 | - |
| w23 | lex | 114 | 2148 | 89.99 | 98.23 | 92.31 | 70.97 | - |
| w23 | auto | 114 | 2148 | 89.94 | 98.36 | 92.31 | 70.97 | - |

## where the errors are (mode raw): spaces vs characters

space edits = insert/delete of a word space; char acc (no spaces) = character accuracy after removing all spaces.

| set | group | space edits | other edits | space share % | char acc no spaces % |
|---|---|---|---|---|---|
| lines | all | 4655 | 3185 | 59 | 95.46 |
| lines | w20 | 1264 | 893 | 59 | 95.14 |
| lines | w21 | 2373 | 1323 | 64 | 94.69 |
| lines | w22 | 933 | 788 | 54 | 95.54 |
| lines | w23 | 85 | 181 | 32 | 97.65 |
| pages | all | 18453 | 28595 | 39 | 84.70 |
| pages | w20 | 6455 | 12237 | 35 | 81.87 |
| pages | w21 | 7868 | 6581 | 54 | 90.60 |
| pages | w22 | 3930 | 9077 | 30 | 79.25 |
| pages | w23 | 200 | 700 | 22 | 93.10 |

## warnings

- pages [ocr2/ocr2/auto]: 1/126 images returned < 30% of the reference length, e.g. w22_p0105
- pages [ocr2/ocr2/raw]: 1/126 images returned < 30% of the reference length, e.g. w22_p0105
- pages [ocr2/ocr2/lex]: 1/126 images returned < 30% of the reference length, e.g. w22_p0105
