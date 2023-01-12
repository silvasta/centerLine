#!/bin/bash
#SBATCH  --output=logCenterNet/%j.out
#SBATCH  --gres=gpu:1
#SBATCH  --mem=30G

source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh

conda activate CenterNet

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/models/networks/DCNv2
./make.sh

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/external
make

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src
    # worked on 06.07.21 0.374 correct AP
#python test.py ctdet --exp_id coco_dla --keep_res --load_model ../models/ctdet_coco_dla_2x.pth

#python test.py ctdet --exp_id coco_dla --keep_res --load_model ../models/ctdet_coco_dla_2x.pth --flip_test --test_scales 0.5,0.75,1,1.25,1.5

    # not same values as proposed!
#python test.py ctdet --exp_id coco_hg --arch hourglass --fix_res --load_model ../models/ctdet_coco_hg.pth

    #test 13.7.21
python test.py ctdet --exp_id coco_resdcn18 --arch resdcn_18 --keep_res --load_model ../models/ctdet_coco_resdcn18.pth


# cd src
# # train
# python main.py ctdet --exp_id coco_resdcn18 --arch resdcn_18 --batch_size 114 --master_batch 18 --lr 5e-4 --gpus 0,1,2,3 --num_workers 16
# # test
# python test.py ctdet --exp_id coco_resdcn18 --arch resdcn_18 --keep_res --resume
# # flip test
# python test.py ctdet --exp_id coco_resdcn18 --arch resdcn_18 --keep_res --resume --flip_test 
# # multi scale test
# python test.py ctdet --exp_id coco_resdcn18 --arch resdcn_18 --keep_res --resume --flip_test --test_scales 0.5,0.75,1,1.25,1.5
# cd ..

