from modules.JsonHandler import *

path = "/scratch/silvasta/datasets/random_synthetic_large/annotations/random_train.json"

before = importJson(path)

before_annotations = before["annotations"]
annotations = []
images = before["images"]
categories = before["categories"]

count = 0
for anot in before_annotations:
    anot["area"] = before_annotations[count]["bbox"][2] * before_annotations[count]["bbox"][3]
    annotations.append(anot)
    count = count+1

after = {"categories":categories, 
                    "images":images,
                    "annotations":annotations}

writeJson(after, path=path)