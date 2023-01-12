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

### Logs
    # First try i = 60
# RoboCupDataset_with_CenterNet/train/train_head_only_loop$ sbatch train_and_test.sh 
# sbatch: GRES requested     : gpu:2
# sbatch: GPUs requested     : 2
# sbatch: Requested Memory   : 51200.0
# sbatch: CPUs requested     : ---
# Submitted batch job 396942

    # Second try i = 80
# silvasta@biwidl213:/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/scripts/runRoboCupDataset_with_CenterNet/train/train_head_only_loop$ sbatch train_and_test.sh 
# sbatch: GRES requested     : gpu:2
# sbatch: GPUs requested     : 2
# sbatch: Requested Memory   : 51200.0
# sbatch: CPUs requested     : ---
# Submitted batch job 39733

    # Third try i = 69 to 79
# silvasta@biwidl213:/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/scripts/runRoboCupDataset_with_CenterNet/train/train_head_only_loop$ sbatch train_and_test.sh 
# sbatch: GRES requested     : gpu:2
# sbatch: GPUs requested     : 2
# sbatch: Requested Memory   : 51200.0
# sbatch: CPUs requested     : ---
# Submitted batch job 397427

    # Third try i = 18 to 20
# silvasta@biwidl213:/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/scripts/runRoboCupDataset_with_CenterNet/train/train_head_only_loop$ sbatch train_and_test.sh 
# sbatch: GRES requested     : gpu:2
# sbatch: GPUs requested     : 2
# sbatch: Requested Memory   : 51200.0
# sbatch: CPUs requested     : ---
# Submitted batch job 397838


# script starts here

for ((i = 18; i <= 20; i++))
do
echo "$i params of 99 are freezed now!"


#train
python main.py ctdet --freezedLayers $i --load_model /scratch_net/biwidl213/silvasta/detectors/CenterNet/models/ctdet_coco_resdcn18.pth  --dataset robocup --exp_id robocup_head_loop --arch resdcn_18 --master_batch 15 --lr 1.25e-4  --gpus 0,1 --num_workers 16

#test
python test.py ctdet --exp_id robocup_head_loop --arch resdcn_18 --keep_res --load_model ../exp/ctdet/robocup_head_loop/model_last.pth --dataset robocup
python test.py ctdet --exp_id robocup_head_loop --arch resdcn_18 --keep_res --load_model ../exp/ctdet/robocup_head_loop/model_best.pth --dataset robocup

done


