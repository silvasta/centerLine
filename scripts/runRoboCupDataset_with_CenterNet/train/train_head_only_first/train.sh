#!/bin/bash

#SBATCH  --output=log/%j.out
#SBATCH  --error=log/%j.err
#SBATCH  --gres=gpu:2
#SBATCH  --mem=50G

# python env
source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh
conda activate CenterNet

# compilation of the machine
cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/models/networks/DCNv2
./make.sh
cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/external
make


cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src
# script starts here


# second try with freezing 94 of 99 layers Submitted batch job 396757
python main.py ctdet --load_model /scratch_net/biwidl213/silvasta/detectors/CenterNet/models/ctdet_coco_resdcn18.pth  --dataset robocup --exp_id robocup_train_head_resdcn18 --arch resdcn_18 --master_batch 15 --lr 1.25e-4  --gpus 0,1 --num_workers 16

# first try with freezing 90 of 99 layers Submitted batch job 396493
#python main.py ctdet --load_model /scratch_net/biwidl213/silvasta/detectors/CenterNet/models/ctdet_coco_resdcn18.pth  --dataset robocup --exp_id robocup_train_head_resdcn18 --arch resdcn_18 --master_batch 15 --lr 1.25e-4  --gpus 0,1 --num_workers 16





