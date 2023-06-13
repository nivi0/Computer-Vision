import os
print(os.path.exists(r"C:\Users\DELL\PycharmProjects\OpenCV\Resources\shapes.jpg"))

import cv2
import numpy as np

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    imgBlank = np.zeros_like(img)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            cv2.drawContours(imgContour, cnt, -1, (0,0,0), 2)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x,y), (x+w,y+h), (0,255,0), 3)
            if len(approx)==3: objType="Triangle"
            elif len(approx)==4:
                aspRatio = w/float(h)
                if aspRatio>0.95 and aspRatio<1.05: objType="Square"
                else: objType="Rectangle"
            else: objType="Circle"
            cv2.putText(imgContour, objType, (x-5,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    cv2.imshow("contours",imgContour)

img = cv2.imread(r"C:\Users\DELL\PycharmProjects\OpenCV\Resources\shapes.jpg")
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1)
imgCanny = cv2.Canny(imgBlur, 50, 50)

imgContour = img.copy()
getContours(imgCanny)
# cv2.imshow("Contours",imgContour)

cv2.waitKey(0)


