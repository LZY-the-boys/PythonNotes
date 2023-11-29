#!/bin/bash
T=$(date +%s)
bash -c "$1"
T="$(($(date +%s)-T))"
formatted_time=$(printf "time %02dd:%02dh:%02dmin:%02ds\n" "$((T/86400))" "$((T/3600%24))" "$((T/60%60))" "$((T%60))")
# Escape command string to print in a single line.
echo "[$(date '+%Y-%m-%d %H:%M:%S')][tmux-$CUDA_VISIBLE_DEVICES] $1 : [$formatted_time]"  >> $LZY_HOME/time.txt