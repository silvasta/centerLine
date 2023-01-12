#bin/bash

path=/scratch_net/biwidl213/silvasta/datasets/RoboCupDataset/robocup/test/

model=/scratch_net/biwidl213/silvasta/detectors/CenterNet/models/robocup_resnet_pretrained_140/model_best.pth



source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh
conda activate CenterNet

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src

python demo.py ctdet --demo $path --load_model $model --arch resdcn_18 --debug 4

