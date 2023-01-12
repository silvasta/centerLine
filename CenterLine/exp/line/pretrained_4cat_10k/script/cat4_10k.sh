#!/bin/bash

#SBATCH  --output=log/%j_all.out
#SBATCH  --error=log/%j.err
#SBATCH  --gres=gpu:2
#SBATCH  --mem=50G

exp_id=pretrained_4cat_10k
data=roboline
model=/scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/exp/line/random_4_categories_10k/model_last.pth
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

#python main2.py line   --load_model $model --gpus 0,1   --exp_id $exp_id

# and test
#python test_test.py line  --resume   --exp_id $exp_id

# and demo
python demo.py line --debugger_theme black --demo $image_path --demo_out $demo_out  --debug 4 --load_model /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/exp/line/pretrained_4cat_10k/model_last.pth