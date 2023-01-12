#!/bin/bash

#SBATCH  --output=log/%j.out
#SBATCH  --error=log/%j.err
#SBATCH  --gres=gpu:1
#SBATCH  --mem=30G

source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh

conda activate CenterNet

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/models/networks/DCNv2
./make.sh

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/external
make

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src

echo "Test flip"
python test.py ctdet --exp_id robocup_test_resdcn18 --arch resdcn_18 --keep_res --load_model ../models/robocup_resnet_140/model_best.pth --dataset robocup

echo "Test flipped"
python test.py ctdet --exp_id robocup_test_resdcn18 --arch resdcn_18 --keep_res --load_model ../models/robocup_resnet_140/model_best.pth --flip_test --dataset robocup

echo "Test multi scale"
python test.py ctdet --exp_id robocup_test_resdcn18 --arch resdcn_18 --keep_res --load_model ../models/robocup_resnet_140/model_best.pth --flip_test --dataset robocup

