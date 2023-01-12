#!/bin/bash

#SBATCH  --output=log/%j_train_and_test.out
#SBATCH  --error=log/%j_.err
#SBATCH  --gres=gpu:2
#SBATCH  --mem=50G

exp_id=rand_line_medium_2cat
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

#python main.py line  --gpus 0,1 --dataset line_2_cat --annot_name rand_line_20k --exp_id $exp_id
#python main.py line --debug 4 --dataset line_4_cat --annot_name rand_line_20k --exp_id $exp_id
  
# and test
#python test_test.py line  --resume --dataset line_2_cat --annot_name rand_line_20k --exp_id $exp_id 
python test_line.py line  --vis_thresh .5 --debug 4 --demo_out $demo_out --resume --dataset line_2_cat --annot_name rand_line_20k --exp_id $exp_id 

# and demo
# python demo_line.py line --dataset line_2_cat --debugger_theme black --demo $image_path --demo_out $demo_out --resume --exp_id $exp_id --debug 4



