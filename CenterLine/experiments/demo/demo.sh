#bin/bash

path_in=/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/images/input/input_mix
path_out=/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/images/first_pretrained_10k_200img/model_best

model=/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/exp/line/pretrained_ran10k_test_200img/model_best.pth


source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh
conda activate CenterNet

cd /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/src

python demo.py line --debugger_theme black --demo $path_in --demo_out $path_out --load_model $model --debug 4

