#!/bin/bash

#SBATCH  --output=log/%j.out
#SBATCH  --error=log/%j.err
#SBATCH  --gres=gpu:1
#SBATCH  --mem=30G

model=../models/robocup_resnet_train_head/90_locked/model_best.pth


source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh
conda activate CenterNet

#cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/models/networks/DCNv2
#./make.sh

#cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/external
#make

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src

# First test with model with 90 of 99 layers locked
# Submitted batch job 396748

python test.py ctdet --exp_id robocup_test_head --arch resdcn_18 --keep_res --load_model $model --dataset robocup
