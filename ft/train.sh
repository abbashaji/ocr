#!/usr/bin/env bash
# Fine-tune tessdata_best fas on rendered corpus lines. Resumable: re-run with the same OUT after restoring it.
# env: CORPUS BASE OUT  [N_TRAIN=30000 N_EVAL=1500 MAX_MIN=300 MAX_IT=60000 LR=0.00001 JOBS=nproc]
#      [CHROMIUM_FRAC=0 (share of the training lines cut from real Chromium renderings of Wikipedia, 0 = Pillow only)
#       CHROMIUM_MIN=40 (time limit for that step) CHROMIUM_SOURCE=api CHROMIUM_FILES_DIR (for source=files)]
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
: "${CHROMIUM_FRAC:=0}" "${CHROMIUM_MIN:=40}" "${CHROMIUM_SOURCE:=api}" "${N_TRAIN:=30000}" "${N_EVAL:=1500}" "${MAX_MIN:=300}" "${MAX_IT:=60000}" "${LR:=0.00001}" "${JOBS:=$(nproc)}"
mkdir -p "$OUT"; OUT="$(cd "$OUT" && pwd)"; BASE="$(cd "$(dirname "$BASE")" && pwd)/$(basename "$BASE")"
cd "$OUT"
[ -f base.lstm ] || combine_tessdata -u "$BASE" base. >/dev/null 2>&1
N_CHR=$(python3 -c "print(int($N_TRAIN * $CHROMIUM_FRAC))"); N_CHR_EVAL=$(python3 -c "print(int($N_EVAL * min(0.5, $CHROMIUM_FRAC)))")
if [ ! -s data/list.train ]; then
  python3 "$HERE/make_train_data.py" --corpus "$CORPUS" --unicharset base.lstm-unicharset --out "$OUT/data" \
      --n-train "$((N_TRAIN - N_CHR))" --n-eval "$((N_EVAL - N_CHR_EVAL))" --jobs "$JOBS"
fi
# Real-browser lines (exact DOM labels, real anti-aliasing / link colours / raised citation markers / zoom 67-100%).
# Appended to the Pillow lists. Skipped on resume (chromium_stats.json exists). A failure here must not silently turn the run into a Pillow-only run.
if [ "$N_CHR" -gt 0 ] && [ ! -f data/chromium_stats.json ]; then
  python3 "$HERE/make_chromium_data.py" --out "$OUT/data" --unicharset base.lstm-unicharset --corpus "$CORPUS" \
      --exclude "$HERE/articles.txt" --n-train "$N_CHR" --n-eval "$N_CHR_EVAL" --max-minutes "$CHROMIUM_MIN" \
      --source "$CHROMIUM_SOURCE" ${CHROMIUM_FILES_DIR:+--files-dir "$CHROMIUM_FILES_DIR"} --jobs "$JOBS" \
    || { echo "FATAL: chromium training data could not be produced; refusing to train a Pillow-only model by accident"; exit 1; }
fi
CONT=base.lstm; [ -f ft_checkpoint ] && CONT=ft_checkpoint && echo "resuming from ft_checkpoint"
# --reset_learning_rate is REQUIRED: without it --learning_rate is ignored and the stored rate destroys the model.
# LR 1e-5 verified stable; 2e-4 destroyed the model in 400 iterations, 2e-5 degraded on a small set.
OMP_THREAD_LIMIT=1 timeout "${MAX_MIN}m" lstmtraining --model_output ft --continue_from "$CONT" --traineddata "$BASE" \
    --train_listfile data/list.train --eval_listfile data/list.eval --max_iterations "$MAX_IT" \
    --learning_rate "$LR" --reset_learning_rate > train.log 2>&1
echo "lstmtraining exit $? (124 = time limit reached, fine)"
tail -n 3 train.log | cut -c1-200
bcer() { lstmeval --model "$1" --traineddata "$BASE" --eval_listfile data/list.eval 2>&1 | sed -n 's/.*BCER eval=\([0-9.]*\).*/\1/p' | tail -1; }
BASE_BCER=$(bcer base.lstm); BEST=""; BEST_B=999
for c in ft_checkpoint $(ls ft_*.checkpoint 2>/dev/null | sort -t_ -k2 -n | head -3); do
  [ -f "$c" ] || continue; b=$(bcer "$c"); echo "candidate $c BCER=$b"
  [ -n "$b" ] && awk "BEGIN{exit !($b < $BEST_B)}" && BEST="$c" && BEST_B="$b"
done
[ -n "$BEST" ] || { echo "no usable checkpoint"; exit 1; }
lstmtraining --stop_training --continue_from "$BEST" --traineddata "$BASE" --model_output fas_ft.traineddata 2>&1 | tail -1
python3 - <<PY
import json, os
chr_stats = json.load(open("data/chromium_stats.json")) if os.path.exists("data/chromium_stats.json") else None
json.dump(dict(chromium=chr_stats, chromium_frac=float("$CHROMIUM_FRAC"), base_bcer=float("$BASE_BCER" or -1), ft_bcer=float("$BEST_B"), checkpoint="$BEST", lr="$LR", n_train=$N_TRAIN, n_eval=$N_EVAL,
   note="BCER = character error % of the raw LSTM on held-out lines (eval split, never trained on); mixed Pillow + Chromium lines when chromium_frac > 0"), open("train_summary.json", "w"), indent=1)
PY
cat train_summary.json
