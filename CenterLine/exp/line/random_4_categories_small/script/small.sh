#!/bin/bash

#SBATCH  --output=log/%j_train_and_test.out
#SBATCH  --error=log/%j_.err
#SBATCH  --gres=gpu:1
#SBATCH  --mem=30G

source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh

conda activate CenterNet

    # compile DCNv2
cd /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/src/lib/models/networks/DCNv2
./make.sh > /dev/null
if [ $? -eq 0 ]; then
   echo "DCNv2 compiled correctly"
fi

cd /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/src

#python main.py line   --dataset line_4_cat --annot_name random_4_categories_small --exp_id random_4_categories_small
#python main.py line --gpus 0,1 --debug 4 --dataset line_4_cat --annot_name random_4_categories_small --exp_id random_4_categories_small
  
# and test
python test_line.py line  --resume --dataset line_4_cat --annot_name random_4_categories_small --exp_id random_4_categories_small