source /scratch_net/biwidl213/silvasta/apps/Conda/conda/etc/profile.d/conda.sh
conda activate CenterNet

for ((i = 75; i <= 99; i++))
do
echo "$i params of 99 are freezed now!"

cd /scratch_net/biwidl213/silvasta/detectors/CenterNet/src
python test_loop.py ctdet --freezedLayers $i

done