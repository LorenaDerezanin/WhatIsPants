#!/bin/bash

#SBATCH --job-name=train
#SBATCH --gres=gpu:tesla:2
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH --mem=128GB
#SBATCH --time=2-00:00:00              # Time limit d-hrs:min:sec
#SBATCH --partition=gpu

set -e

# Pass number of epochs as a command-line argument to sbatch script
# Example usage: sbatch this_script.sh 10
EPOCHS=${1:-5}  # Default to 5 epochs if not specified
echo "Kicking off training with $EPOCHS epochs"

date

export TMPDIR=/fast/users/lode10_c/scratch/yolo_train/tmp

source /data/gpfs-1/users/lode10_c/.bashrc
conda activate /data/gpfs-1/users/lode10_c/scratch/yolo_train/conda/whatispants

export CUDA_LAUNCH_BLOCKING=1
python /data/gpfs-1/users/lode10_c/scratch/yolo_train/deepfash/train.py --epochs $EPOCHS

echo "Yolo train job done"

date
