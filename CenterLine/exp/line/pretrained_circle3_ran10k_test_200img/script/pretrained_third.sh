#!/bin/bash

#SBATCH  --output=log/%j_test_model_last.out
#SBATCH  --error=log/%j.err
#SBATCH  --gres=gpu:2
#SBATCH  --mem=50G

exp_id=pretrained_circle3_ran10k_test_200img
data=roboline
model=/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/exp/line/random_10k_circle3/model_last.pth
image_path=/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/images/input/input_mix
demo_out=/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/exp/line/pretrained_circle3_ran10k_test_200img/demo

source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh

conda activate CenterNet

    # compile DCNv2
cd /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/src/lib/models/networks/DCNv2
./make.sh > /dev/null
if [ $? -eq 0 ]; then
   echo "DCNv2 compiled correctly"
fi

cd /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/src

python main.py line   --load_model $model --gpus 0,1 --dataset $data  --exp_id $exp_id

# and test
python test.py line  --load_model $model --dataset $data  --exp_id $exp_id

# and demo
python demo.py line --debugger_theme black --demo $image_path --demo_out $demo_out --load_model $model --debug 4