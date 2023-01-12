# #!/bin/bash

# #SBATCH  --output=log/%j.out
# #SBATCH  --error=log/%j.err
# #SBATCH  --gres=gpu:1

name_of_data_folder=rand_line_1k
name_of_link=rand_line_1k

source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh
conda activate CenterNet

cd /scratch_net/biwidl213/silvasta/datasets
rm -r random_synthetic
mkdir random_synthetic
cd random_synthetic
mkdir test train val annotations

cd /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/src
python random_synthetic_images.py
python tools/lineAnnotation_to_coco.py

cd /scratch_net/biwidl213/silvasta/datasets/random_synthetic

# rm test/*.json train/*.json val/*.json

cd ..
mv random_synthetic $name_of_data_folder

cd /scratch_net/biwidl213/silvasta/bachelor-thesis-line-detection/CenterLine/data
ln -s /scratch_net/biwidl213/silvasta/datasets/$name_of_data_folder $name_of_link

echo "data created and linked to CenterLine"


