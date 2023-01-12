
import random
import numpy as np
import cv2

range_color = 50 # added or subtracted to R G B
range_white = 50



b = 0 + range_color + random.randint(-range_color,range_color)
g = 255 - range_color + random.randint(-range_color,range_color)
r = 0 + range_color + random.randint(-range_color,range_color)

while True:
    r1,r2,r3 = random.randint(-range_white,0),random.randint(-range_white,0),random.randint(-range_white,range_white)
    w = (255+r1,255+r1,255+r1)
    print(w)

    img = np.zeros((480,640,3), np.uint8)
    img[:] = (b, g, r)

    center = (320,240)
    radius = 200
    cv2.circle(img, center, radius, w, -1)



    cv2.imshow("color", img)
    cv2.waitKey()
    cv2.destroyAllWindows()