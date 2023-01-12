#!/bin/bash

#SBATCH  --output=log/%j_train_and_test.out
#SBATCH  --error=log/%j_.err
#SBATCH  --gres=gpu:2
#SBATCH  --mem=50G

source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh

conda activate CenterNet

    # compile DCNv2
cd /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/src/lib/models/networks/DCNv2
./make.sh > /dev/null
if [ $? -eq 0 ]; then
   echo "DCNv2 compiled correctly"
fi

cd /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/src

#python main.py line  --gpus 0,1 --dataset random_synthetic --annot_name random_4_categories --exp_id random_4_categories_20k
python main.py line --debug 4 --dataset random_synthetic --annot_name random_4_categories --exp_id random_4_categories_20k
  
# and test
python test.py line  --resume --dataset random_synthetic --annot_name random_4_categories --exp_id random_4_categories_20k