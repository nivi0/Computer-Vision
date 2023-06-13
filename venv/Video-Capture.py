import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640) #width
cap.set(4, 480) #height
cap.set(10, 100)

while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(img, (7,7), 0)
    imgCanny = cv2.Canny(img, 150, 150)
    imgHor = np.hstack((imgGray, imgCanny))
    cv2.imshow("Web-cam",img)
    cv2.imshow("Gray", imgGray)
    cv2.imshow("Blur", imgBlur)
    cv2.imshow("Canny", imgCanny)
    #cv2.imshow("Horizontally Stacked",imgHor)
    if cv2.waitKey(1) & 0xFF==ord(' '):
        break

