#!/bin/bash

PATHTOIMAGE=/scratch_net/biwidl213/silvasta/datasets/514A1181.JPG


source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh
conda activate CenterNet

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src


#python demo.py ctdet --demo $PATHTOIMAGE  --load_model ../models/ctdet_coco_dla_2x.pth

python demo.py multi_pose --demo $PATHTOIMAGE --load_model ../models/multi_pose_dla_3x.pth
