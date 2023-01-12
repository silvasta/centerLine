#!/bin/bash

#SBATCH  --output=log/%j.out
#SBATCH  --error=log/%j.err
#SBATCH  --gres=gpu:1
#SBATCH  --mem=30G

model=../models/robocup_resnet_pretrained_140/model_last.pth


source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh
conda activate CenterNet

#cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/models/networks/DCNv2
#./make.sh

#cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/external
#make

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src

echo "Test flip"
python test.py ctdet --exp_id robocup_test_resdcn18 --arch resdcn_18 --keep_res --load_model $model --dataset robocup

echo "Test flipped"
python test.py ctdet --exp_id robocup_test_resdcn18 --arch resdcn_18 --keep_res --load_model $model --flip_test --dataset robocup

echo "Test multi scale"
python test.py ctdet --exp_id robocup_test_resdcn18 --arch resdcn_18 --keep_res --load_model $model --flip_test --dataset robocup

