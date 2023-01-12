#!/bin/bash
#SBATCH  --output=logCenterNet/%j.out
#SBATCH  --gres=gpu:1
#SBATCH  --mem=30G

source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh

conda activate CenterNet

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/models/networks/DCNv2
./make.sh

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/external
make

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src

# test
#python test.py ctdet --load_model ../models/model_best.pth --exp_id coco_resdcn18 --arch resdcn_18 --keep_res --resume
# # flip test
# python test.py ctdet --load_model ../models/model_last.pth --exp_id coco_resdcn18 --arch resdcn_18 --keep_res --resume --flip_test 
# # multi scale test
python test.py ctdet --load_model ../models/model_last.pth --exp_id coco_resdcn18 --arch resdcn_18 --keep_res --resume --flip_test --test_scales 0.5,0.75,1,1.25,1.5
    
