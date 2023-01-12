import fiftyone as fo

# The directory containing the source images
#data_path = "/home/ss/Desktop/Dataset/Validation/Images"
data_path = "/home/ss/Desktop/Dataset/Validation/Images"

# The path to the COCO labels JSON file
#labels_path = "/home/ss/Desktop/Dataset/Validation/person_keypoints_val2019.json"
#labels_path = "/home/ss/ownCloud/bachelor\ thesis/code/annotations/roboline_Test.json"
labels_path = "/home/ss/ownCloud/bachelor thesis/code/annotations/roboline_Val.json"
# Import the dataset
dataset = fo.Dataset.from_dir(
    dataset_type=fo.types.COCODetectionDataset,
    data_path=data_path,
    labels_path=labels_path,
    #max_samples=10
)

session = fo.launch_app(dataset)
session.wait()
