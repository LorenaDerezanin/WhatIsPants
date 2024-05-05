#!/bin/bash

#SBATCH --job-name=train
#SBATCH --gres=gpu:tesla:2
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20        # with 16 and fewer we get an error in os.sched_setaffinity(0, range(NUM_THREADS))
#SBATCH --mem=32GB
#SBATCH --time=2-00:00:00              # Time limit d-hrs:min:sec
#SBATCH --partition=gpu

set -e

# Pass number of epochs as a command-line argument to sbatch script
# Example usage: sbatch this_script.sh 10
EPOCHS=${1:-5}  # Default to 5 epochs if not specified
echo "Kicking off training with $EPOCHS epochs"

date

export TMPDIR=/fast/users/lode10_c/scratch/yolo_train/tmp

source "$HOME"/.bashrc
conda activate /data/gpfs-1/users/lode10_c/scratch/yolo_train/conda/whatispants

# Clear torch kernels cache to prevent errors like
#   File "/data/gpfs-1/users/lode10_c/scratch/yolo_train/conda/whatispants/lib/python3.12/site-packages/ultralytics/utils/loss.py", line 408, in calculate_segmentation_loss
#    marea = xyxy2xywh(target_bboxes_normalized)[..., 2:].prod(2)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# RuntimeError: CUDA driver error: invalid argument
# See also https://discuss.pytorch.org/t/torch-prod-produces-runtimeerror-cuda-driver-error-invalid-argument/179054/20
rm -rf "$HOME"/.cache/torch/kernels

python /data/gpfs-1/users/lode10_c/scratch/yolo_train/deepfash/train.py --epochs $EPOCHS

echo "Yolo train job done"

date
