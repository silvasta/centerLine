import glob
import os
import math

from modules.JsonHandler import *

number_of_images = 24000

    # laptop real
# split_list = ["test"]
# path_to_load = "/home/ss/ownCloud/bachelor thesis/data/annotated_lines_on_robocup_dataset/" 
# path_to_save = "/home/ss/ownCloud/bachelor thesis/data/roboline/annotations/roboline_{}.json"

#     # laptop synthetic
# split_list = ["val"]
# path_to_load = "/home/ss/ownCloud/bachelor thesis/data/random_synthetic_image/" 
# path_to_save = "/home/ss/ownCloud/bachelor thesis/data/random_synthetic_image/annotations/random_4lines_{}.json"


    # biwidl
split_list = ["test", "train", "val"]
path_to_load = "/scratch_net/biwidl213/silvasta/datasets/rand_line_1k/"
path_to_save = "/scratch_net/biwidl213/silvasta/datasets/rand_line_1k/annotations/random_2categories_{}.json"


def deg_to_rad(angle):
    return angle*math.pi/180

def create_bounding_box_2_types(p1, p2):
    
    p1x, p1y = p1
    p2x, p2y = p2
    dx = p1x-p2x
    dy = p1y-p2y

        # categories
    
    # top left bottom right
    if p1x < p2x and p1y < p2y or p1x > p2x and p1y > p2y:
        category_id = 1
    
    # top right bottom left
    else:
        category_id = 2

        # bounding box
    x = min(p1[0],p2[0])
    y = min(p1[1],p2[1])
    width = abs(p1[0]-p2[0])
    height = abs(p1[1]-p2[1])
    
    return [x,y,width,height], category_id

def create_bounding_box_4_types(p1, p2, gamma):
    
    p1x, p1y = p1
    p2x, p2y = p2
    dx = p1x-p2x
    dy = p1y-p2y

        # categories
    # horizontal
    if dx != 0:
        if abs(dy/dx) < math.tan(deg_to_rad(gamma)):
            category_id = 1

    
    # vertical
    if dy != 0:
        if abs(dx/dy) < math.tan(deg_to_rad(gamma)):
            category_id = 2
    
    # top right bottom left
    if p1x < p2x and p1y > p2y or p1x > p2x and p1y < p2y:
        category_id = 3
    
    # top left bottom right
    else:
        category_id = 4

        # bounding box
    x = min(p1[0],p2[0])
    y = min(p1[1],p2[1])
    width = abs(p1[0]-p2[0])
    height = abs(p1[1]-p2[1])
    
    return [x,y,width,height], category_id

def line_as_2_bbox():

    line_annotations = load_annotations()
    count = 0
    for task in line_annotations:

        if count == number_of_images:
            break

        categories = [{ "id" : 1,
                        "name" : "top_left",
                        "supercategory" : "line"
                        },
                        { "id" : 2,
                        "name" : "top_right",
                        "supercategory" : "line"
                        },
                       ]
        images, annotation = [], []
        height, width = 480, 640
        anot_id = 1
        for anot in task:
            filename = os.path.basename(anot["path"]) 
            images.append({ "id" : anot["image_id"], 
                            "file_name" : filename, 
                            "height" : height, 
                            "width" : width
                            })
            for line in anot["lines"]:
                bbox, cat_id = create_bounding_box_2_types(line["startpoint"],line["endpoint"])    
                annotation.append({"id" : anot_id, 
                                    "category_id" : cat_id,
                                    "image_id" : anot["image_id"],
                                    "bbox" : bbox,
                                    "iscrowd": 0,
                                    "area": bbox[2]*bbox[3]
                                    })
                anot_id += 1


        roboline = {"categories":categories, 
                    "images":images,
                    "annotations":annotation}

        save_annotation(roboline, split_list[count])
        count += 1

def line_as_4_bbox(gamma):

    line_annotations = load_annotations()
    count = 0
    for task in line_annotations:

        if count == number_of_images:
            break

        categories = [{ "id" : 1,
                        "name" : "horizontal",
                        "supercategory" : "line"
                        },
                        { "id" : 2,
                        "name" : "vertical",
                        "supercategory" : "line"
                        },
                        { "id" : 3,
                        "name" : "top_right",
                        "supercategory" : "line"
                        },
                        { "id" : 4,
                        "name" : "top_left",
                        "supercategory" : "line"
                        }]
        images, annotation = [], []
        height, width = 480, 640
        anot_id = 1
        for anot in task:
            filename = os.path.basename(anot["path"]) 
            images.append({ "id" : anot["image_id"], 
                            "file_name" : filename, 
                            "height" : height, 
                            "width" : width
                            })
            for line in anot["lines"]:
                bbox, cat_id = create_bounding_box_4_types(line["startpoint"],
                                            line["endpoint"], gamma)    
                annotation.append({"id" : anot_id, 
                                    "category_id" : cat_id,
                                    "image_id" : anot["image_id"],
                                    "bbox" : bbox,
                                    "iscrowd": 0,
                                    "area": bbox[2]*bbox[3]
                                    })
                anot_id += 1


        roboline = {"categories":categories, 
                    "images":images,
                    "annotations":annotation}

        save_annotation(roboline, split_list[count])
        count += 1


def line_as_bbox():

    line_annotations = load_annotations()
    count = 0
    for task in line_annotations:
        categories = [{ "id" : 1, 
                        "name" : "line",
                        "supercategory" : "line"
                        }]
        images, annotation = [], []
        height, width = 480, 640
        anot_id = 1
        for anot in task:
            filename = os.path.basename(anot["path"]) 
            images.append({ "id" : anot["image_id"], 
                            "file_name" : filename, 
                            "height" : height, 
                            "width" : width
                            })
            for line in anot["lines"]:
                bbox = create_bounding_box(line["startpoint"],
                                            line["endpoint"])    
                annotation.append({"id" : anot_id, 
                                    "category_id" : 1,
                                    "image_id" : anot["image_id"],
                                    "bbox" : bbox,
                                    "iscrowd": 0,
                                    "area": bbox[2]*bbox[3]
                                    })
                anot_id += 1


        roboline = {"categories":categories, 
                    "images":images,
                    "annotations":annotation}

        save_annotation(roboline, split_list[count])
        count += 1


def create_bounding_box(p1, p2):
    x = min(p1[0],p2[0])
    y = min(p1[1],p2[1])
    width = abs(p1[0]-p2[0])
    height = abs(p1[1]-p2[1])
    return [x,y,width,height]


def load_annotations():
    line_annotation_list = []
    for task in split_list:
        task_list = [] 
        task_paths = glob.glob("{}{}/*.json".format(path_to_load,task))
        for path in task_paths:
            task_list.append(importJson(path))
        line_annotation_list.append(task_list)
        print("task:",task,"| length:",len(task_list))
    return line_annotation_list


def save_annotation(roboline, task):
    print(path_to_save)
    writeJson(roboline, path=path_to_save.format(task))



if __name__ == "__main__":
    
        # first implementation as one line
    # line_as_bbox()
    
        # second implementation as 4 lines
            # horizontal, vertical, top left bottom right, top right bottom left 
            # gamma = angle to classify horizontal, vertical lines in degree
    # gamma = 8
    # line_as_4_bbox(gamma)

        # third implementation as 2 categories
    line_as_2_bbox()
    print("Successfully saved annotations!")

