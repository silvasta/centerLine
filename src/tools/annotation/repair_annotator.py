import cv2
import glob

from modules.JsonHandler import writeJson
from modules.LineAnnotator import LineAnnotator

   # select range to annotate
split = "val"
start = 0
end = 3
failures = False
failures_to_repeat = [16,21,33,36,37,46,53]

    # select options for loading
path = "/home/ss/ownCloud/bachelor thesis/data/annotated_lines_on_robocup_dataset/Val"

    # select options for saving
path_to_save_json = "/home/ss/ownCloud/bachelor thesis/data/annotated_lines_on_robocup_dataset/{}/".format(split)+"{}.json"
path_to_save_img = "/home/ss/ownCloud/bachelor thesis/data/annotated_lines_on_robocup_dataset/{}/".format(split)+"{}.bmp"
save_img = False



# projects a point on a line
def point_on_line(p3):
    x1, y1 = newAnnotations.startpoint
    x2, y2 = newAnnotations.endpoint
    x3, y3 = p3
    dx, dy = x2-x1, y2-y1
    det = dx*dx + dy*dy
    a = (dy*(y3-y1)+dx*(x3-x1))/det
    return int(x1+a*dx), int(y1+a*dy)


# marker on image
def plot_point(p):
    x, y = p
    cv2.circle(image, p, 3, (0,0,255), -1)
    cv2.imshow('annotator image {}'.format(image_id), image)

# save line to list in class and plot line on image
def add_line_to_list(startpoint, endpoint):
    line = {"line_segment": newAnnotations.line_segment, 
            "startpoint": startpoint, 
            "endpoint": endpoint}
    newAnnotations.lines.append(line)
    cv2.line(image, startpoint, endpoint, (0,255,255), 2)
    cv2.imshow('annotator image {}'.format(image_id), image)

# main tool to annotate
def click_event(event, x, y, flags, params):

    # startpoint of line or endpoint of single line
    if event == cv2.EVENT_LBUTTONDOWN:
        p = point_on_line((x,y))
        plot_point((x,y))
       
        add_line_to_list(newAnnotations.p1, p)



    # starts segmentation and creates helpline
    if event == cv2.EVENT_RBUTTONDOWN:

        add_line_to_list(newAnnotations.p1, newAnnotations.p2)
        newAnnotations.bool_segment = True
        



def annotate_image():

    print()
    print()
    print("Start of image ",image_id)
    for line in anot.lines:
        print(line)
    print()

    cv2.imshow('annotator image {}'.format(image_id), image)
    seg_num = 1
    if len(failList) > 0:
        count_fails = 0 
        for fail in failList:
            
            zero = fail[count_fails]
            p1, p2 = zero["startpoint"],zero["endpoint"]
            newAnnotations.startpoint = p1
            newAnnotations.endpoint = p2
            cv2.circle(image, p1, 5, (0,255,255), -1)
            cv2.line(image, p1, p2, (0,0,0), 1)
            cv2.imshow('annotator image {}'.format(image_id), image)
            count_fails += 1
            for line in fail:
                p1, p2 = line["startpoint"],line["endpoint"]
                plot_point(p1)
                plot_point(p2)
            for line in fail:
                
                if newAnnotations.bool_segment == True:
                    seg_num += 1
                    p1 = line["startpoint"]
                    p2 = line["endpoint"]
                    add = {"line_segment": seg_num,
                            "startpoint": p1, 
                            "endpoint": p2}
                    newAnnotations.lines.append(add)
                    newAnnotations.bool_segment == False
                else:
                    newAnnotations.p1 = line["startpoint"]
                    newAnnotations.p2 = line["endpoint"]
                    cv2.setMouseCallback('annotator image {}'.format(image_id), click_event)
                    cv2.waitKey(0)
                    print(newAnnotations.bool_segment)


    if len(goodList) > 0:
        for line in goodList:
            print(line)
            seg_num += 1
            add = {"line_segment": seg_num,
                    "startpoint": line["startpoint"], 
                    "endpoint": line["endpoint"]}
            newAnnotations.lines.append(add)
            
        print()

    for line in newAnnotations.lines:
        print(line)
    newAnnotations.display_self()
    print("End of image ",image_id)   
    cv2.destroyAllWindows()
    newAnnotations.save(path_to_save_json.format(image_id))

def generate_faillist():

    before = {"line_segment": 0}
    isSeq = False
    seqList = []
    start = True
    for line in anot.lines:

        if line["line_segment"] == before["line_segment"]:
            seqList.append(before)
            isSeq = True
        elif isSeq == True:
            seqList.append(before)
            failList.append(seqList)
            #print(seqList)
            seqList = []
            isSeq = False
        elif not start:
            goodList.append(before)
        start = False
        before = line
    if isSeq:
        seqList.append(before)
        failList.append(seqList)
    elif len(goodList) > 0 or len(failList) > 0:
        goodList.append(before)
        
    # print("image:",newAnnotations.image_id)
    # print("anot",len(anot.lines))
    # for fail in failList:
    #     print("fail:")
    #     for f in fail:
    #         print(f)
    # print()
    # for line in newAnnotations.lines:
    #     print("new:",line)
    # print()
    # print()
    # print() 

if __name__ == "__main__":

    imageAnnotationList = LineAnnotator.load_data(path)

    count = 0
    for anot in imageAnnotationList:
        count += 1
        if count < 0:
            continue
        image = cv2.imread(anot.path)
        failList = []
        goodList = []
        newAnnotations = LineAnnotator(anot.path, anot.image_id)
        image_id = newAnnotations.image_id
        generate_faillist()
        annotate_image()
        
        
        
 
     
        
