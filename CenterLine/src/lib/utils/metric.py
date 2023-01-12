import json
import math
import cv2

class LineResult:

    def __init__(self, ground_through, predicted_lines, maximum_offset ):

            # Fp = lines that are predictet but dont match the ground through
        self.Fp = predicted_lines
            # Fn = lines in ground through without a match
        self.Fn = []
            # Tp = lines that have a match
        self.Tp = []
            # maximum distance from prediction to gt
        self.offset = maximum_offset

        for gt_line in ground_through:
            match = self.find_closest_line(gt_line)
            if match == False:
                self.Fn.append(gt_line)

    def find_closest_line(self,gt_line):
        
        # values of gt line
        gt_p1, gt_p2 = gt_line
        gt_x1, gt_y1 = gt_p1
        gt_x2, gt_y2 = gt_p2

        best_match, best_distance = None, 10000

        # iterate over all lines without a match
        for pred_line in self.Fp:

            # values of predicted line
            pred_p1, pred_p2 = pred_line
            pred_x1, pred_y1 = pred_p1
            pred_x2, pred_y2 = pred_p2
            
            # match on first point
            dist_p1_1 = math.sqrt((gt_x1-pred_x1)**2 + (gt_y1-pred_y1)**2)
            dist_p2_2 = math.sqrt((gt_x2-pred_x2)**2 + (gt_y2-pred_y2)**2)            
            if dist_p1_1 < self.offset and dist_p2_2 < self.offset:
                if dist_p1_1 + dist_p2_2 < best_distance:
                    best_distance = dist_p1_1 + dist_p2_2
                    best_match = pred_line
                
            # match on second point 
            dist_p1_2 = math.sqrt((gt_x1-pred_x2)**2 + (gt_y1-pred_y2)**2)
            dist_p2_1 = math.sqrt((gt_x2-pred_x1)**2 + (gt_y2-pred_y1)**2)   
            if dist_p1_2 < self.offset and dist_p2_1 < self.offset:
                if dist_p1_2 + dist_p2_1 < best_distance:
                    best_distance = dist_p1_2 + dist_p2_1
                    best_match = pred_line

        if best_match is not None:
            self.Fp.remove(best_match)
            self.Tp.append(best_match)

        return best_match is not None

    def get_precision(self):
        if len(self.Tp)+len(self.Fp) == 0:
            return 0
        else:
            return len(self.Tp)/(len(self.Tp)+len(self.Fp))

    def get_recall(self):
        if len(self.Tp)+len(self.Fn) == 0:
            return 0
        else:
            return len(self.Tp)/(len(self.Tp)+len(self.Fn))


def get_images(predictedList,annotation_path):
    
    with open(annotation_path) as jsonFile:
        ground_through = json.load(jsonFile)
        jsonFile.close()
    
    images = []
    for img in ground_through["images"]:
        image = {"image_id":img["id"], "ground_through":[], "predictions":[]}
        for gt in ground_through["annotations"]:
            if gt["image_id"] == img ["id"]:
                image["ground_through"].append(bbox_to_line(gt["category_id"], gt["bbox"]))
        for pred in predictedList:
            if pred["image_id"] == img["id"]:
                image["predictions"].append(bbox_to_line(pred["category_id"], pred["bbox"]))
        images.append(image)

    return images
    

def bbox_to_line(cat,bbox):
    x1, y1, dx, dy = bbox[0:4]
    if cat == 1:
        p1 = (x1,y1+dy/2)
        p2 = (x1+dx,y1+dy/2)
    if cat == 2:
        p1 = (x1+dx/2,y1)
        p2 = (x1+dx/2,y1+dy)
    if cat == 3:
        p1 = (x1,y1+dy)
        p2 = (x1+dx,y1)
    if cat == 4:
        p1 = (x1,y1)
        p2 = (x1+dx,y1+dy)

    return (p1, p2)

def run_metric(predictedList,annotation_path):    

    offsets = [10,15,20]

    for offset in offsets:
        images = get_images(predictedList,annotation_path)
        recallList, precisionList = [], []
        for i, image in enumerate(images):
            result_of_line = LineResult(images[i]["ground_through"],images[i]["predictions"],offset)
            recallList.append(result_of_line.get_recall())
            precisionList.append(result_of_line.get_precision())
        print("AP({}) =".format(offset),sum(precisionList)/len(precisionList))
        print("AR({}) =".format(offset),sum(recallList)/len(recallList))


def print_lines(img, bbox, color  ,cat  ):
    print("cat",cat)
    line = bbox_to_line(cat=cat, bbox=bbox)
    cv2.line(img, line[0], line[1], color, 3)