#!/bin/bash

#SBATCH  --output=log/%j.out
#SBATCH  --error=log/%j.err
#SBATCH  --gres=gpu:2
#SBATCH  --mem=50G

source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh

conda activate CenterNet

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/models/networks/DCNv2
./make.sh

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/external
make

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src


#python main.py multi_pose --load_model /scratch_net/biwidl213/silvasta/detectors/CenterNet/models/ctdet_coco_resdcn18.pth  --dataset robocup --exp_id robocup_multi_pose_resdcn18 --arch resdcn_18 --master_batch 15 --lr 1.25e-4  --gpus 0,1 --num_workers 16
echo 
echo "------"
echo "test model last"
python test.py multi_pose --exp_id robocup_multi_pose_resdcn18 --arch resdcn_18 --keep_res  --dataset robocup --load_model /scratch_net/biwidl213/silvasta/detectors/CenterNet/exp/multi_pose/robocup_multi_pose_resdcn18/model_last.pth
echo "------"
echo 
echo "------"
echo "test model best"
python test.py multi_pose --exp_id robocup_multi_pose_resdcn18 --arch resdcn_18 --keep_res  --dataset robocup --load_model /scratch_net/biwidl213/silvasta/detectors/CenterNet/exp/multi_pose/robocup_multi_pose_resdcn18/model_best.pth



