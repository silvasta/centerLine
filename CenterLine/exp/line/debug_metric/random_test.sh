#!/bin/bash

#SBATCH  --output=log/test_%j.out
#SBATCH  --error=log/test_%j.err
#SBATCH  --gres=gpu:1
#SBATCH  --mem=30G

model=/home/silvasta/CenterLine/exp/line/debug_metric/model_random_4cat_50k_E70
dataset="line_4_cat"
exp_id=debug_metric
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

python test_line.py line --annot_name random_4_categories --exp_id $exp_id --dataset $dataset --load_model $model 


#python demo_line.py line --debugger_theme black --demo $image_path --dataset $dataset --demo_out $demo_out --load_model $model --debug 4
