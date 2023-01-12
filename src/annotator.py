import cv2
import glob

from modules.JsonHandler import writeJson
from modules.LineAnnotator import LineAnnotator

   # select range to annotate
split = "train"
start = 520
end = 600 
end = end+1 
failures = False 
failures_to_repeat = [    ]

    # select options for loading
path_to_image_list ="/home/ss/Desktop/Dataset/Train/Images/*"

    # select options for saving
path_to_save_json = "/home/ss/ownCloud/bachelor thesis/data/annotated_lines_on_robocup_dataset/{}/".format(split)+"{}.json"
path_to_save_img = "/home/ss/ownCloud/bachelor thesis/data/annotated_lines_on_robocup_dataset/{}/".format(split)+"{}.bmp"
save_img = False


# projects a point on a line
def point_on_line(p3):
    x1, y1 = imageAnnotations.startpoint
    x2, y2 = imageAnnotations.endpoint
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
    line = {"line_segment": imageAnnotations.line_segment, 
            "startpoint": startpoint, 
            "endpoint": endpoint}
    imageAnnotations.lines.append(line)
    cv2.line(image, startpoint, endpoint, (0,255,255), 2)
    cv2.imshow('annotator image {}'.format(image_id), image)

# main tool to annotate
def click_event(event, x, y, flags, params):

    # startpoint of line or endpoint of single line
    if event == cv2.EVENT_LBUTTONDOWN and imageAnnotations.bool_segment == False:
        if imageAnnotations.bool_start == True:
            imageAnnotations.startpoint = (x,y)
            plot_point((x,y))
            imageAnnotations.bool_start = False
        else:
            imageAnnotations.endpoint = (x,y)
            plot_point((x,y))
            imageAnnotations.bool_start = True
            add_line_to_list(imageAnnotations.startpoint, imageAnnotations.endpoint)
            imageAnnotations.line_segment += 1

    # creates the segments in the line
    if event == cv2.EVENT_LBUTTONDOWN and imageAnnotations.bool_segment == True:
        middlepoint = point_on_line((x,y))
        plot_point(middlepoint)
        if imageAnnotations.bool_start == False:
            add_line_to_list(imageAnnotations.startpoint, middlepoint)
            imageAnnotations.bool_start = True
        else:
            imageAnnotations.startpoint = middlepoint
            imageAnnotations.bool_start = False

    # starts segmentation and creates helpline
    if event == cv2.EVENT_RBUTTONDOWN and imageAnnotations.bool_segment == False:
        if imageAnnotations.bool_start == False:
            imageAnnotations.endpoint = (x,y)
            cv2.line(image, imageAnnotations.startpoint, imageAnnotations.endpoint, (0,0,0), 1)
            plot_point((x,y))
            imageAnnotations.bool_segment = True

    # ends the segmentation and adds the last line
    if event == cv2.EVENT_MBUTTONDOWN and imageAnnotations.bool_segment == True:
        imageAnnotations.bool_segment = False
        imageAnnotations.bool_start = True
        add_line_to_list(imageAnnotations.startpoint, imageAnnotations.endpoint)
        imageAnnotations.line_segment += 1



def annotate_image():
    
    print("Start of image ", image_id, path_to_image_list)
    cv2.imshow('annotator image {}'.format(image_id), image)

        # start click event        
    cv2.setMouseCallback('annotator image {}'.format(image_id), click_event)
    cv2.waitKey(0)

    print("End of image ",image_id, path_to_save_json.format(image_id))   
    cv2.destroyAllWindows()
    imageAnnotations.save(path_to_save_json.format(image_id))


def create_list():

    fullList = glob.glob(path_to_image_list)
    if failures:
        imageList = [fullList[i-1] for i in failures_to_repeat]
        image_id = failures_to_repeat
    else:
        imageList = fullList[start:end]
        image_id = [i for i in range(start, end)]
    return imageList, image_id
    

if __name__ == "__main__":

    imageList, idList = create_list()

    for i in range(0,len(imageList)):
        image = cv2.imread(imageList[i])
        image_id = idList[i] 
        imageAnnotations = LineAnnotator(imageList[i], image_id)
        annotate_image()
 
     
        
