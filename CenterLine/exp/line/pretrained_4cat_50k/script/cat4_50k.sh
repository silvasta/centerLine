#!/bin/bash

#SBATCH  --output=log/%j_test_demo.out
#SBATCH  --error=log/%j.err
#SBATCH  --gres=gpu:1
#SBATCH  --mem=50G

exp_id=pretrained_4cat_50k
data=roboline
model=/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/exp/line/random_4_categories_20k/model_90.pth
image_path=/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/images/input/input_mix
demo_out=/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/exp/line/$exp_id/demo

source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh

conda activate CenterNet

    # compile DCNv2
cd /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/src/lib/models/networks/DCNv2
./make.sh > /dev/null
if [ $? -eq 0 ]; then
   echo "DCNv2 compiled correctly"
fi

cd /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/src

python main.py line  --debug 4 --load_model $model  --dataset $data  --exp_id $exp_id
#--gpus 0,1
# # and test
python test_test.py line   --dataset $data  --exp_id $exp_id --load_model /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/exp/line/pretrained_4cat_50k/model_last.pth

# and demo
python demo.py line --debugger_theme black --demo $image_path --demo_out $demo_out --load_model /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/exp/line/pretrained_4cat_50k/model_last.pth --debug 4