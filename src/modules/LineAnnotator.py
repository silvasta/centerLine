import cv2
import glob
import math

from .JsonHandler import *
from matplotlib import colors

color_name = ["yellow","blue","black","grey","olive","gold","palegreen","darkcyan","aqua","purple","orange", ]
color_list = []
for c in color_name:
    r,g,b =  colors.hex2color(colors.cnames[c])
    r,g,b = int(256*r),int(256*g),int(256*b) 
    color_list.append((r,g,b))



class LineAnnotator:

    # init method or constructor 
    def __init__(self, path, image_id):
            # stuff for output file 
        self.path = path
        self.image_id = image_id
        self.lines = []
            # stuff to work in the click event
        self.line_segment = 1
        self.bool_segment = False
        self.bool_start = True
   
        # save the class atributes to JSON 
    def save(self, path_to_save):
        out = {"path": self.path,"image_id": self.image_id, "lines": self.lines}
        writeJson(out, path_to_save)
#        print('Successfully saved annotations from image', self.image_id)

        # load multiple single annotations from folder to list of class instances
    def load_data(path_to_folder):
        class_list = []
        paths = glob.glob("{}/*.json".format(path_to_folder))
        for p in paths:
            json = importJson(p)
            anot = LineAnnotator(json["path"], json["image_id"])
            anot.lines = json["lines"]
            class_list.append(anot)
        return class_list

        # displays the annotations of a list of classes
    def display_data(class_list):
        for anot in class_list:
            
            image = cv2.imread(anot.path)
            for line in anot.lines:
                color = color_list[line["line_segment"]]
                p1, p2 = line["startpoint"], line["endpoint"]
                cv2.circle(image,p1,4, (0,0,255), -1)            
                cv2.circle(image,p2,4, (0,0,255), -1)
                cv2.line(image, p1, p2, color, 2)
                print(anot.image_id)
                cv2.imshow('annotator image {}'.format(anot.image_id), image)
                cv2.waitKey(200)
            cv2.waitKey()
            cv2.destroyAllWindows()

    def display_data_by_category(class_list):
        for anot in class_list:
            print()
            image = cv2.imread(anot.path)
            for line in anot.lines:
                category_id = create_bounding_box_4_types(line["startpoint"], line["endpoint"],gamma=7)
                color = color_list[category_id-1]
                p1, p2 = line["startpoint"], line["endpoint"]
                cv2.circle(image,p1,4, (0,0,255), -1)            
                cv2.circle(image,p2,4, (0,0,255), -1)
                cv2.line(image, p1, p2, color, 2)
                print("line of category:",category_id)
                cv2.imshow('annotator image {}'.format(anot.image_id), image)
                cv2.waitKey(200)
            cv2.waitKey()
            cv2.destroyAllWindows()

    def display_self(self):
        image = cv2.imread(self.path)

        for line in self.lines:
            color = color_list[line["line_segment"]]
            p1, p2 = line["startpoint"], line["endpoint"]
            cv2.circle(image,p1,4, (0,0,255), -1)            
            cv2.circle(image,p2,4, (0,0,255), -1)
            cv2.line(image, p1, p2, color, 2)
            cv2.imshow('annotator image {}'.format(self.image_id), image)
            cv2.waitKey(0)
        cv2.destroyAllWindows()       

# copy from lineAnnotation_to_coco.py
# !!!! do not edit here !!!!
def deg_to_rad(angle):
    return angle*math.pi/180
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
        category_id = 4
    
    # top left bottom right
    else:
        category_id = 3


    
    return  category_id



