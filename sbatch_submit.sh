#!/bin/bash

#SBATCH --job-name=train
#SBATCH --gres=gpu:tesla:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH --mem=32GB
#SBATCH --time=1-00:00:00              # Time limit d-hrs:min:sec
#SBATCH --partition=gpu

set -e

# Pass number of epochs as a command-line argument to sbatch script
# Example usage: sbatch this_script.sh 10
EPOCHS=${1:-5}  # Default to 5 epochs if not specified
MODEL_NAME=${2:-"yolov8s-seg.pt"}  # Default model name if not specified
OUT_DIR=${3:-"/data/gpfs-1/users/lode10_c/scratch/yolo_train/runs/segment/${MODEL_NAME%.pt}_${EPOCHS}"}  # Default output directory based on model name and epochs

echo "Kicking off training with $EPOCHS epochs, model $MODEL_NAME, output directory $OUT_DIR"

date

export TMPDIR=/fast/users/lode10_c/scratch/yolo_train/tmp

source "$HOME"/.bashrc
conda activate /data/gpfs-1/users/lode10_c/scratch/yolo_train/conda/whatispants

#due to storage limit in real HOME dir, export scratch yolo dir as new HOME
export HOME=/data/gpfs-1/users/lode10_c/scratch/yolo_train
rm -rf "$HOME"/.cache/torch/kernels

python /data/gpfs-1/users/lode10_c/scratch/yolo_train/train.py \
	--epochs $EPOCHS \
	--model_name $MODEL_NAME \
	--out_dir $OUT_DIR

echo "Yolo train job done"

date


