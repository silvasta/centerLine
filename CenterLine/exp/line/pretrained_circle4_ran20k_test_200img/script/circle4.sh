#!/bin/bash

#SBATCH  --output=log/%j_Train_Test_Demo.out
#SBATCH  --error=log/%j.err
#SBATCH  --gres=gpu:1
#SBATCH  --mem=30G

exp_id=pretrained_circle4_ran20k_test_200img
data=roboline
model=/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/exp/line/random_20k_circle4/model_last.pth
image_path=/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/images/input/input_mix
demo_out=/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/exp/line/$exp_id/demo

source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh

conda activate CenterNet

    # compile DCNv2
# cd /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/src/lib/models/networks/DCNv2
# ./make.sh > /dev/null
# if [ $? -eq 0 ]; then
#    echo "DCNv2 compiled correctly"
# fi

cd /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/src

#python main.py line   --load_model $model --gpus 0,1 --dataset $data  --exp_id $exp_id

# and test
#python test.py line  --load_model $model --dataset $data  --exp_id $exp_id
# python test_test.py line  --load_model $model --dataset $data  --exp_id $exp_id
# python test_line.py line --load_model $model --dataset $data  --exp_id $exp_id

# and demo
python demo.py line --debugger_theme black --dataset line_4_cat --demo $image_path --demo_out $demo_out --load_model $model --debug 4