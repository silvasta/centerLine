#!/bin/bash
#SBATCH  --output=logCenterNet/train_%j_overnight.out
#SBATCH  --gres=gpu:2
#SBATCH  --mem=50G

#as in the tests before
source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh

conda activate CenterNet

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/models/networks/DCNv2
./make.sh

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src/lib/external
make

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src

#copied from the official training scripts
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

#first try, 16 workers failed to run, CUDA out of memory (1 GPU for all tries)
    # # train
    # python main.py ctdet --exp_id coco_resdcn18 --arch resdcn_18 --batch_size 114 --lr 5e-4  #--master_batch 18   #--num_workers 16 #--gpus 0,1,2,3
   
#try with 4 GPUs, original command, job still pending, worked after some hours! but only one epoch, no log??
    #python main.py ctdet --exp_id coco_resdcn18 --arch resdcn_18 --batch_size 114 --master_batch 18 --lr 5e-4 --gpus 0,1,2,3 --num_workers 16

#try with 2 GPUs, CUDA error: out of memory (8workers and 4)
    #python main.py ctdet --exp_id coco_resdcn18 --arch resdcn_18 --batch_size 114 --master_batch 18 --lr 5e-4 --gpus 0,1 --num_workers 4

#try with default training not with batchsizes recomended for ResNet-18
# first epoch after 25 min!
    #python main.py ctdet --exp_id coco_resdcn18 --arch resdcn_18 --master_batch 15 --lr 1.25e-4  --gpus 0,1 --num_epochs 3

# try to figure out where the limit of the batch sizes is
    # no #python main.py ctdet --batch_size 100 --exp_id coco_resdcn18 --arch resdcn_18 --master_batch 15 --lr 4e-4  --gpus 0,1 
    #no with srun #python main.py ctdet --batch_size 64 --exp_id coco_resdcn18 --arch resdcn_18 --master_batch 15 --lr 4e-4  --gpus 0,1 

#finally run the working one over night with 140 epochs
python main.py ctdet --exp_id coco_resdcn18 --arch resdcn_18 --master_batch 15 --lr 1.25e-4  --gpus 0,1 --resume

