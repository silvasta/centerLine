import cv2
import glob

from modules.JsonHandler import importJson
from modules.LineAnnotator import LineAnnotator as la

#path = "/home/ss/ownCloud/bachelor thesis/data/annotated_lines_on_robocup_dataset/train"
path = "/home/ss/ownCloud/bachelor thesis/data/random_synthetic_image/val"

if __name__ == "__main__":
    # display one color per segmented line
    #la.display_data(la.load_data(path))

    # display one color per category
    la.display_data_by_category(la.load_data(path))



     
        
