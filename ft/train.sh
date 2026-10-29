#!/usr/bin/env bash
# Fine-tune tessdata_best fas on rendered corpus lines (+ optional real scanned lines). Resumable: re-run with the same OUT after restoring it.
# env: CORPUS BASE OUT  [N_TRAIN=30000 N_EVAL=1500 MAX_MIN=300 MAX_IT=60000 LR=0.00001 JOBS=nproc]
#      [SCHEME=folded|distinct|distinct_ezafe|alias|alias_ezafe  (label scheme, see ft/common.py; default folded = the original recipe, byte-for-byte the same steps)]
#      [REAL_DIR=<realdata tesseract export, distinct preset> N_REAL=0 N_REAL_EVAL=500   (real scanned lines mixed into the training list)]
#      [EZAFE_P=0.25 (distinct_ezafe: share of heh-final words rendered with the mark)]
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
: "${SCHEME:=folded}" "${REAL_DIR:=}" "${N_REAL:=0}" "${N_REAL_EVAL:=500}" "${EZAFE_P:=0.25}"
: "${N_TRAIN:=30000}" "${N_EVAL:=1500}" "${MAX_MIN:=300}" "${MAX_IT:=60000}" "${LR:=0.00001}" "${JOBS:=$(nproc)}"
mkdir -p "$OUT"; OUT="$(cd "$OUT" && pwd)"; BASE="$(cd "$(dirname "$BASE")" && pwd)/$(basename "$BASE")"
cd "$OUT"
export FT_LABEL_SCHEME="$SCHEME"
[ -f base.lstm ] || combine_tessdata -u "$BASE" base. >/dev/null 2>&1
# TD = traineddata whose unicharset the model is trained with; stock for folded, stock + new classes otherwise
TD="$BASE"; UNI=base.lstm-unicharset; OLD=()
case "$SCHEME" in distinct|distinct_ezafe)
  [ -s ext/fas_ext.traineddata ] || python3 "$HERE/extend_unicharset.py" --base "$BASE" --scheme "$SCHEME" --out "$OUT/ext" || { echo "FATAL: unicharset extension failed"; exit 1; }
  TD="$OUT/ext/fas_ext.traineddata"; UNI="$OUT/ext/ext.lstm-unicharset"; OLD=(--old_traineddata "$BASE") ;;
esac   # folded, alias, alias_ezafe: stock unicharset, nothing is extended
if [ ! -s data/list.train ]; then
  python3 "$HERE/make_train_data.py" --corpus "$CORPUS" --unicharset "$UNI" --out "$OUT/data" \
      --n-train "$N_TRAIN" --n-eval "$N_EVAL" --jobs "$JOBS" --scheme "$SCHEME" --ezafe-p "$EZAFE_P" \
      ${REAL_DIR:+--real-dir "$REAL_DIR" --n-real "$N_REAL" --n-real-eval "$N_REAL_EVAL"}
fi
CONT=base.lstm; [ -f ft_checkpoint ] && CONT=ft_checkpoint && OLD=() && echo "resuming from ft_checkpoint"
# --reset_learning_rate is REQUIRED: without it --learning_rate is ignored and the stored rate destroys the model.
# LR 1e-5 verified stable; 2e-4 destroyed the model in 400 iterations, 2e-5 degraded on a small set.
OMP_THREAD_LIMIT=1 timeout "${MAX_MIN}m" lstmtraining --model_output ft --continue_from "$CONT" --traineddata "$TD" ${OLD[@]+"${OLD[@]}"} \
    --train_listfile data/list.train --eval_listfile data/list.eval --max_iterations "$MAX_IT" \
    --learning_rate "$LR" --reset_learning_rate > train.log 2>&1
echo "lstmtraining exit $? (124 = time limit reached, fine)"
tail -n 3 train.log | cut -c1-200
# BCER of a model on a list: bcer <model> <traineddata> <listfile>
bcer() { [ -s "$3" ] || { echo ""; return; }; lstmeval --model "$1" --traineddata "$2" --eval_listfile "$3" 2>&1 | sed -n 's/.*BCER eval=\([0-9.]*\).*/\1/p' | tail -1; }
# base (stock) model can only be scored on lines without the new classes: the *_plain lists (identical images and labels in every scheme)
BASE_BCER=$(bcer base.lstm "$BASE" data/list.eval)
[ "$SCHEME" = folded ] || BASE_BCER=""
BEST=""; BEST_B=999
for c in ft_checkpoint $(ls ft_*.checkpoint 2>/dev/null | sort -t_ -k2 -n | head -3); do
  [ -f "$c" ] || continue; b=$(bcer "$c" "$TD" data/list.eval); echo "candidate $c BCER=$b"
  [ -n "$b" ] && awk "BEGIN{exit !($b < $BEST_B)}" && BEST="$c" && BEST_B="$b"
done
[ -n "$BEST" ] || { echo "no usable checkpoint"; exit 1; }
lstmtraining --stop_training --continue_from "$BEST" --traineddata "$TD" --model_output fas_ft.traineddata 2>&1 | tail -1
case "$SCHEME" in alias) python3 "$HERE/rename_classes.py" fas_ft.traineddata ;; alias_ezafe) python3 "$HERE/rename_classes.py" fas_ft.traineddata --ezafe ;; esac
if [ "$SCHEME" = distinct ] || [ "$SCHEME" = distinct_ezafe ]; then   # keep the stock dictionaries (their class ids are unchanged: new classes are appended)
  combine_tessdata -o fas_ft.traineddata base.lstm-punc-dawg base.lstm-word-dawg base.lstm-number-dawg >/dev/null 2>&1 || echo "WARNING: could not restore dawgs"
fi
B_PLAIN_BASE=$(bcer base.lstm "$BASE" data/list.eval_plain); B_PLAIN_FT=$(bcer "$BEST" "$TD" data/list.eval_plain)
B_REAL_BASE=$(bcer base.lstm "$BASE" data/list.eval_real_plain); B_REAL_PLAIN_FT=$(bcer "$BEST" "$TD" data/list.eval_real_plain); B_REAL_FT=$(bcer "$BEST" "$TD" data/list.eval_real)
export SCHEME BEST BEST_B LR N_TRAIN N_EVAL N_REAL BASE_BCER B_PLAIN_BASE B_PLAIN_FT B_REAL_BASE B_REAL_PLAIN_FT B_REAL_FT EZAFE_P
python3 - <<'PY'
import json, os
def f(k):
    v = os.environ.get(k, ''); return float(v) if v else None
json.dump(dict(scheme=os.environ['SCHEME'], base_bcer=f('BASE_BCER'), ft_bcer=f('BEST_B'), checkpoint=os.environ['BEST'], lr=os.environ['LR'],
   n_train=int(os.environ['N_TRAIN']), n_eval=int(os.environ['N_EVAL']), n_real=int(os.environ['N_REAL'] or 0), ezafe_p=f('EZAFE_P'),
   bcer_plain_base=f('B_PLAIN_BASE'), bcer_plain_ft=f('B_PLAIN_FT'),
   bcer_real_plain_base=f('B_REAL_BASE'), bcer_real_plain_ft=f('B_REAL_PLAIN_FT'), bcer_real_all_ft=f('B_REAL_FT'),
   note="BCER = character error % of the raw LSTM on held-out lines (never trained on). base_bcer/ft_bcer: synthetic eval list of the scheme (base_bcer only for folded). "
        "*_plain: only lines whose label is identical in every scheme (no ، ٫ ٬ ٪ % ; ezafe), same images for all schemes -> use these to compare schemes. "
        "bcer_real_*: real scanned lines of the tune split of the realdata export."), open("train_summary.json", "w"), indent=1)
PY
cat train_summary.json
