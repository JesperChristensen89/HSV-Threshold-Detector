#################################################################
#                                                               #
#   By Jesper H. Christensen                                    #
#   jesper@haahrchristensen.dk                                  #
#                                                               #
#   Script used for finding the HSV threshold in images.        #
#                                                               #
#   Developed as a part of the B.Eng project:                   #
#   Vision Based Control of Collaboring Mobile robots           #
#                                                               #
#################################################################

import cv2
import argparse
from operator import xor

def callback(value):
    pass

def setup_trackbars(range_filter):
    cv2.namedWindow("Trackbars", 0)

    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

        for j in range_filter:
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, callback)

def get_trackbar_values(range_filter):
    values = []

    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values.append(v)

    return values

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i","--image",
        help="path to the image file")

    # get args
    args = vars(ap.parse_args())

    # read image
    image = cv2.imread(args['image'])

    # convert to hsv
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    setup_trackbars('HSV')

    while True:
        
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values('HSV')

        thresh = cv2.inRange(hsv, (v1_min, v2_min, v3_min), 
            (v1_max, v2_max, v3_max))

        cv2.imshow("Original", image)
        cv2.imshow("Thresholded", thresh)

        if cv2.waitKey(1) & 0xFF is ord('q'):
            print "H_min: ", v1_min, " S_min: ", v2_min, " V_min: ", v3_min 
            print "H_max: ", v1_max, " S_max: ", v2_max, " V_max: ", v3_max
            break

if __name__ == '__main__':
    main()