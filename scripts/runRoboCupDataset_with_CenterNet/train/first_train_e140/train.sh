#!/bin/bash

#SBATCH  --output=log/%j.out
#SBATCH  --error=log/%j.err
#SBATCH  --gres=gpu:2
#SBATCH  --mem=70G

source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh

conda activate CenterNet

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/models/networks/DCNv2
./make.sh

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/external
make

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src


python main.py ctdet --dataset robocup --exp_id robocup_train_resdcn18 --arch resdcn_18 --master_batch 15 --lr 1.25e-4  --gpus 0,1 --num_workers 16





