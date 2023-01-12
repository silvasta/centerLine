import numpy as np

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
    return [int(x), int(y)]


def ortho(p1,p2,width=640,height=480):
    for p in [p1,p2]:
        if p[0] < 0: p[0] = 0
        if p[0] > width: p[0] = width
        if p[1] < 0: p[1] = 0
        if p[1] > height: p[1] = height

    return p1,p2


def check_s_t(p1,p2,alpha=0,beta=0,h0=0,w0=0):
    x1, y1 = p1    
    x2, y2 = p2    
        # A * [t,s] = b
    A = [[x1-x2, -alpha], [y1-y2, -beta]]
    b = [w0-x2, h0-y2]
    t,s = np.linalg.solve(A,b)

    #print("t:",t,"s:",s)
    t_bool = 0 <= t and t <= 1
    s_bool = 0 <= s and s <= 1
    #print(t_bool and s_bool)
    return t_bool and s_bool


def find_boarder(p1,p2,width=640,height=480, deltaX=320, deltaY=240):
    # convert from big square to small
    p1[0]=p1[0]-deltaX
    p1[1]=p1[1]-deltaY
    p2[0]=p2[0]-deltaX
    p2[0]=p2[0]-deltaY

    # avoid singular matrix problem
    if p1[0]==p2[0] or p1[1]==p2[1]:
        return ortho(p1,p2)
      
    # main idea is this equation:
        # x2 + (x1-x2)*t = s*alpha + w0    for s in [0,1]
        # y2 + (y1-y2)*t = s*beta + h0      
        #   for s,t in [0,1]
    # => check if s,t in ranges for all boarders
 
    #boarder 1 (x = 0, y = s*height)
    #print("boarder 1")
    if check_s_t(p1,p2, beta=height):
        if p1[0] < p2[0]:
            p1 = line_intersection((p1,p2),((0,0),(0,height)))
        else:
            p2 = line_intersection((p1,p2),((0,0),(0,height)))
    #print()

    # boarder 2 (x = s*width, y = 0)
    #print("boarder 2")
    if check_s_t(p1,p2, alpha=width):
        if p1[1] < p2[1]:
            p1 = line_intersection((p1,p2),((0,0),(width,0)))
        else:
            p2 = line_intersection((p1,p2),((0,0),(width,0)))

    #print()
    # boarder 3 (x = width, y = s*height)
    #print("boarder 3")
    if check_s_t(p1,p2, w0=width, beta=height):
        if p1[0] > p2[0]:
            p1 = line_intersection((p1,p2),((width,0),(width,height)))
        else:
            p2 = line_intersection((p1,p2),((width,0),(width,height)))
        
    #print()
    # boarder 4 (x = s*width, y = height)
    #print("boarder 4")
    if check_s_t(p1,p2, alpha=width, h0=height):
        if p1[1] > p2[1]:
            p1 = line_intersection((p1,p2),((0,height),(width,height)))
        else:
            p2 = line_intersection((p1,p2),((0,height),(width,height)))
    #print()


    return p1,p2



if __name__ == "__main__":

    # endpoint = [-20,40]
    # startpoint = [700,300]

    startpoint = [100,-50]
    endpoint = [120,700]


    p1,p2 = find_boarder(startpoint,endpoint) 
    #print("")
    #print("final points:",p1, p2)
