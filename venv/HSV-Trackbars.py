import os
print(os.path.exists(r'C:\Users\DELL\PycharmProjects\OpenCV\Resources\cards.jpg'))

import cv2
import numpy as np

def empty(a):
    pass

cv2.namedWindow("Trackbars Window")
cv2.resizeWindow("Trackbars Window",640,240)
cv2.createTrackbar("Hue Min","Trackbars Window",0,179,empty)
cv2.createTrackbar("Hue Max","Trackbars Window",179,179,empty)
cv2.createTrackbar("Sat Min","Trackbars Window",0,255,empty)
cv2.createTrackbar("Sat Max","Trackbars Window",255,255,empty)
cv2.createTrackbar("Val Min","Trackbars Window",0,255,empty)
cv2.createTrackbar("Val Max","Trackbars Window",125,255,empty)

cap = cv2.VideoCapture(0)
while True:
    #img = cv2.imread(r'C:\Users\DELL\PycharmProjects\OpenCV\Resources\cards.jpg')
    success, img = cap.read()
    img = cv2.resize(img, (200,200))
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue Min", "Trackbars Window")
    h_max = cv2.getTrackbarPos("Hue Max", "Trackbars Window")
    s_min = cv2.getTrackbarPos("Sat Min", "Trackbars Window")
    s_max = cv2.getTrackbarPos("Sat Max", "Trackbars Window")
    v_min = cv2.getTrackbarPos("Val Min", "Trackbars Window")
    v_max = cv2.getTrackbarPos("Val Max", "Trackbars Window")

    # print(h_min, h_max, s_min, s_max, v_min, v_max)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    print(lower)
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    imgStack = np.hstack([img, imgHSV, imgResult])
    cv2.imshow("HSV", imgStack)
    cv2.imshow("Mask", mask)


    cv2.waitKey(1)