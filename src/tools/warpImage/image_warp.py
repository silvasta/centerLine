import cv2
import numpy as np

def warp_image(img):
    #set parameters for transforming the image
    pts1 = np.float32([[-20,134],[882,232],[869,811],[21,971]])
    pts2 = np.float32([[0,0],[800,0],[800,600],[0,600]])

    M = cv2.getPerspectiveTransform(pts1,pts2)

    #transform the thermal image to the new size and perspective
    return cv2.warpPerspective(img,M,(800,600))



# driver function
if __name__=="__main__":
    # reading the image
    img = cv2.imread('data/20210614_155919.jpg', 1)
    print(type(img))
    img = warp_image(img)

    cv2.imwrite("../table_notes.jpg", img)
