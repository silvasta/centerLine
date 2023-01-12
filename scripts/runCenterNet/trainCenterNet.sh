#!/bin/bash
#SBATCH  --output=logCenterNet/train/%j_2gpu_32batch_16threds.out
#SBATCH  --gres=gpu:2
#SBATCH  --mem=70G

#as in the tests before
source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh

conda activate CenterNet

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/models/networks/DCNv2
./make.sh

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/external
make

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src

# task 1
#python main.py ctdet --exp_id coco_resdcn18_4_gpu_114batch --arch resdcn_18 --batch_size 114 --master_batch 18 --lr 5e-4 --gpus 0,1,2,3 --num_workers 16

# task 2
python main.py ctdet --resume --exp_id coco_resdcn18_8_workers --arch resdcn_18 --master_batch 15 --lr 1.25e-4  --gpus 0,1 --num_workers 16





