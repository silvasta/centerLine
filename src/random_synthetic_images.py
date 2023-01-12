import cv2
import numpy as np
import random
import math

from modules.LineAnnotator import LineAnnotator
from modules.CircleAnnotation import CircleLineAnnotator

#path_to_save = "/home/ss/ownCloud/bachelor thesis/data/random_synthetic_image/"
path_to_save = "/scratch_net/biwidl213/silvasta/datasets/random_synthetic/"

# amount of data
number_of_images = 1200
split_list = ["test", "train", "val"]
split_values = [1,10,1]

# image dimension and factor for points
height = 480
width = 640

# line parameters
min_line_length = 30
max_number_of_lines = 10
min_line_thickness = 5
max_line_thickness = 16

#  circle parameters
number_of_circles = 0
min_circle_radius = 30
max_circle_radius = 500

# color parameters
range_color = 50 # added or subtracted to R G B

# color lines for segments that are cutted
print_color = False

# class intersectionLineCircle:

#     def __init__():

def cut_to_circles(line, circles, iter=0):
    A, B = line.A, line.B

    length_AB = line_length(A,B)

    if length_AB < min_line_length:
        return []

    # norm vector from A to B                              
    Dx = (B[0]-A[0])/length_AB
    Dy = (B[1]-A[1])/length_AB

    for c, circle in enumerate(circles.List):
        
        if c < iter:
            continue

        C, R  = circle["center"], circle["radius"]

        # line equation AB:= x = Dx*t + Ax, y = Dy*t + Ay, t in [0, length_AB]
        t = Dx*(C[0]-A[0]) + Dy*(C[1]-A[1])

        if (t < 0 or t > length_AB) and not (line_length(A,C) < R or line_length(B,C) < R): 
            continue

        # E is the closest point of AB to the circle center
        E = (t*Dx+A[0], t*Dy+A[1])

        # line intersection with the circle
        if line_length(E,C) < R:

            # distance from t to intersection points 
            dt = math.sqrt(R**2 - line_length(E,C)**2)

            # line inside
            if line_length(A,C) < R and line_length(B,C) < R:
                return []

            # intersection points
            F = ((t-dt)*Dx + A[0], (t-dt)*Dy + A[1])
            G = ((t+dt)*Dx + A[0], (t+dt)*Dy + A[1])

            # A inside circle
            if line_length(A,C) < R:
                line_GB = lineClass(G,B,line.line_thickness,line.seg_num,line.white)
                return cut_to_circles(line_GB,circles,c+1)
            
            # B inside circle
            if line_length(B,C) < R:
                line_AF = lineClass(A,F,line.line_thickness,line.seg_num,line.white)
                return cut_to_circles(line_AF,circles,c+1)

            # otherwise the circle splits the line
            line_GB = lineClass(G,B,line.line_thickness,line.seg_num,line.white)
            line_AF = lineClass(A,F,line.line_thickness,line.seg_num,line.white)
            out = []
            out.extend(cut_to_circles(line_AF,circles,c+1))
            out.extend(cut_to_circles(line_GB,circles,c+1))
            return out

    # all intersections resolved 
    A , B = (int(A[0]), int(A[1])), (int(B[0]), int(B[1]))
    
    return [lineClass(A,B,line.line_thickness,line.seg_num,line.white)]




                       


class lineClass:

    def __init__(self, p1,p2,line_thickness,seg_num,white):
        self.A = p1
        self.B = p2
        self.line_thickness = line_thickness
        self.seg_num = seg_num
        self.white = white

    def __str__(self):
        return ("A:({},{}) B:({},{}) Seg:{}".format(self.A[0],self.A[1],self.B[0],self.B[1],self.seg_num))
    
    def plot_line(self, img):
        return cv2.line(img, self.A, self.B, self.white , self.line_thickness)


class randomLine(lineClass):

    def __init__(self, seg_num):
        Ax, Bx = random_width(), random_width()
        Ay, By = random_heigth(), random_heigth()
        line_thickness = random.randint(min_line_thickness,max_line_thickness)
        white = get_withe()
        super().__init__((Ax,Ay),(Bx,By),line_thickness,seg_num,white)


class circleClass:

    def __init__(self, num,r_min,r_max,width=640,height=480):
        self.List = []
        for c in range(num):
            center = (random_width(), random_heigth())
            r_max = 2*r_min+int(r_max*random.random()**3)
            radius = random.randint(r_min, r_max)
            self.List.append({"center":center, "radius":radius})
    
    def plot_circles(self, img):
        for circle in self.List:
            cv2.circle(img, circle["center"], circle["radius"], get_withe(), -1)
        return img
    
    def contains(circle, p):
        return line_length(p, circle["center"]) < circle["radius"]



class Counter:
    def __init__(self):
        self.number_of_lines = 0
        self.number_of_images = 0



def line_length(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return (int(x), int(y))


def cut_ortho(p1,p2,width=640,height=480):
    # if p[0] < 0: p[0] = 0
    # if p[0] > width: p[0] = width
    # if p[1] < 0: p[1] = 0
    # if p[1] > height: p[1] = height

    if p1[0]==p2[0]:
        p1x = 0 if p1[0] < 0 else p1[0]
        p1x = width if p1[0] > width else p1[0]
        p2x = 0 if p2[0] < 0 else p2[0]
        p2x = width if p2[0] > width else p2[0]
        return (p1x,p1[1]),(p2x,p2[1])

    if p1[1]==p2[1]:
        p1y = 0 if p1[1] < 0 else p1[1]
        p1y = height if p1[1] > height else p1[1]
        p2y = 0 if p2[1] < 0 else p2[1]
        p2y = height if p2[1] > height else p2[1]
        return (p1[0],p1y),(p2[0],p1y)

    print("fail!!! (ortho")


def check_s_t(p1,p2,alpha=0,beta=0,h0=0,w0=0):
    x1, y1 = p1    
    x2, y2 = p2    
        # A * [t,s] = b
    A = [[x1-x2, -alpha], [y1-y2, -beta]]
    b = [w0-x2, h0-y2]
    try:
        t,s = np.linalg.solve(A,b)
    except:
        t, s = -1, -1

    t_bool = 0 <= t and t <= 1
    s_bool = 0 <= s and s <= 1
    return t_bool and s_bool


def find_boarder(p1,p2,width=640,height=480, deltaX=320, deltaY=240):

    # convert from big square to small
    p1 = (p1[0]-deltaX, p1[1]-deltaY)
    p2 = (p2[0]-deltaX, p2[1]-deltaY)

    # avoid singular matrix problem
    if p1[0]==p2[0] or p1[1]==p2[1]:
        return cut_ortho(p1,p2)
       
    # main idea is this equation:
        # x2 + (x1-x2)*t = s*alpha + w0    for s in [0,1]
        # y2 + (y1-y2)*t = s*beta + h0      
        #   for s,t in [0,1]
    # => check if s,t in ranges for all boarders
 
    #boarder 1 (x = 0, y = s*height)
    if check_s_t(p1,p2, beta=height):
        if p1[0] < p2[0]:
            # print("test1.1")
            p1 = line_intersection((p1,p2),((0,0),(0,height)))
        else:
            p2 = line_intersection((p1,p2),((0,0),(0,height)))

    # boarder 2 (x = s*width, y = 0)
    if check_s_t(p1,p2, alpha=width):
        if p1[1] < p2[1]:
            p1 = line_intersection((p1,p2),((0,0),(width,0)))
        else:
            p2 = line_intersection((p1,p2),((0,0),(width,0)))

    # boarder 3 (x = width, y = s*height)
    if check_s_t(p1,p2, w0=width, beta=height):
        if p1[0] > p2[0]:
            p1 = line_intersection((p1,p2),((width,0),(width,height)))
        else:
            p2 = line_intersection((p1,p2),((width,0),(width,height)))
        
    # boarder 4 (x = s*width, y = height)
    if check_s_t(p1,p2, alpha=width, h0=height):
        if p1[1] > p2[1]:
            p1 = line_intersection((p1,p2),((0,height),(width,height)))
        else:
            p2 = line_intersection((p1,p2),((0,height),(width,height)))
    
    return p1,p2


def not_in_target(startpoint, endpoint, width=640, height=480):
    x2, y2 = startpoint
    x1, y1 = endpoint
    b1 = 0 <= x1 and x1 <= width
    b2 = 0 <= x2 and x2 <= width
    b3 = 0 <= y1 and y1 <= height
    b4 = 0 <= y2 and y2 <= height

    return not (b1 and b2 and b3 and b4)

def show_image(img):
    cv2.imshow("image", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

def get_bgr():
    b = 0 + range_color + random.randint(-range_color,range_color)
    g = 255 - range_color + random.randint(-range_color,range_color)
    r = 0 + range_color + random.randint(-range_color,range_color)
    return (b,g,r)
            
def get_withe():
    w = 255 - range_color//2 + random.randint(0,range_color//2)
    return (w,w,w)

def random_width():
    return random.randint(-width//2,3*width//2)

def random_heigth():
    return random.randint(-height//2,3*height//2)

def main(count):

    for s, split in enumerate(split_list):

        print("Start creating", split)

        for i in range(split_values[s]*number_of_images//sum(split_values)):
            
            count.number_of_images += 1

            # create a green image
            image = np.zeros((height,width,3), np.uint8)
            image[:] = get_bgr()
            color_line_List = []

            # filename and directory to save
            path_to_save_img = path_to_save + "{}/random_{}.jpg".format(split, i)
            path_to_save_json = path_to_save + "{}/random_{}.json".format(split, i)

            imageAnnotations = LineAnnotator(path_to_save_img, i)
            
            # add circles as "obstacles"
            circles = circleClass(number_of_circles,min_circle_radius,max_circle_radius)
            
            number_of_lines = random.randint(1, max_number_of_lines)
            line_segment_List = []
            
            # add lines
            for l in range(number_of_lines):
                
                line = randomLine(l)
                
                # check the initial line
                if print_color:
                    initial_line = line
                    initial_line.color = (0,0,0)
                    color_line_List.append(initial_line)
                
                # cut to final boarders
                line.A, line.B = find_boarder(line.A, line.B)
                if not_in_target(line.A, line.B):
                    continue
                
                # recursive main function
                line_segment_List.extend(cut_to_circles(line, circles))
                
                

            # plot lines and save annotations
            for line in line_segment_List:
                if line_length(line.A,line.B) < min_line_length:
                    continue

                count.number_of_lines +=1

                image = line.plot_line(image)
                line_annotation = {"line_segment": line.seg_num, "startpoint": line.A, "endpoint":line.B}
                imageAnnotations.lines.append(line_annotation)

            # plot circles over lines    
            image = circles.plot_circles(image)
            
            # plot initial lines bevor cutting
            if print_color:
                for line in color_line_List:
                    image = cv2.line(image, line.A, line.B, line.color , 4)

            # save image and annotations
            cv2.imwrite(path_to_save_img, image)
            imageAnnotations.save(path_to_save_json)
       

if __name__ == "__main__":
    count = Counter()
    main(count)
    print(count.number_of_lines,"lines from",count.number_of_images, "images are saved to:", path_to_save)
