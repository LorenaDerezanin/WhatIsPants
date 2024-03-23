#!/usr/bin/env sh
WORKDIR=/data/gpfs-1/users/lode10_c/scratch/yolo_train/distill
find "$WORKDIR/"images_fullres/ -name "*.jpg" | xargs -I {} -P 32 mogrify -resize '300x300>' -path "$WORKDIR/"images {}
