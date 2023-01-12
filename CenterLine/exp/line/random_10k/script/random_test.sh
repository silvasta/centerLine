#!/bin/bash

#SBATCH  --output=log/test_%j.out
#SBATCH  --error=log/test_%j.err
#SBATCH  --gres=gpu:1
#SBATCH  --mem=30G

model=/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/exp/line/random_debug/model_last.pth

source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh

conda activate CenterNet

# cd /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/src/lib/models/networks/DCNv2
# ./make.sh

cd /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/src

python test.py line  --resume --dataset random_synthetic --annot_name random_medium --exp_id random_10k

# --load_model $model
