#!/usr/bin/env bash
# Run a list of parameter variants in parallel and print a compact summary.
# Usage: scan.sh <tag> "<args variant 1>" "<args variant 2>" ...
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
bin="$here/../build/melanoma_vegf"
tag="$1"; shift
mkdir -p "$here/../runs/scan"
cd "$here/../runs/scan"
i=0
for v in "$@"; do
  echo "$i|$v"
  i=$((i+1))
done | xargs -P 8 -I{} bash -c 'n="${1%%|*}"; a="${1#*|}"; OMP_NUM_THREADS=1 '"$bin"' '"$here"'/base_params.txt out='"$tag"'_$n $a' _ {}
i=0
for v in "$@"; do
  f="${tag}_${i}_ts.csv"
  echo "== [$i] $v"
  awk -F, -v every="${EVERY:-90}" 'NR>1 && ($1 % every)==0 {printf "  t=%5d Mc=%9.2e Ms=%9.2e Mm=%9.2e neo=%7.2f vtum=%6.3f P=%5.3f rp=%5.2f nsat=%s\n",$1,$2,$3,$4,$5,$7,$10,$11,$12}' "$f"
  i=$((i+1))
done
