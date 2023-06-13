import cv2
import numpy as np

cap = cv2.VideoCapture(0)
capWidth, capHeight = 480, 640
cap.set(3, capWidth)
cap.set(4, capHeight)
cap.set(10, 150)

def preProcessing(img):
    kernel = np.ones((5,5))

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    imgDilate = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDilate, kernel, iterations=1)

    return imgThres

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    biggest = np.array([])
    maxArea = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>50:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
            #x, y, w, h = cv2.boundingRect(approx)
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)

    return biggest

def reorder(myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2),np.uint32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew

def getWrap(img, biggest):
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0,0], [capWight,0], [0,capHeight], [capWidth,capHeight]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.wrapPrespective(img, matrix, (capWidth,capHeight))

    imgCropped = imgOutput[20:imgOutput.shape[0]-20, 20:imgOutput.shape[1]-20]
    imgCropped = cv2.resize(imgCropped, (capWidht,capHeight))
    return imgCropped

while True:
    success, img = cap.read()
    img = cv2.resize(img, (capWidth, capHeight))
    imgThresh = preProcessing(img)
    imgContour = img.copy()
    biggest = getContours(imgThresh)
    imgWrapped = getWrap(img, biggest)
    cv2.imshow("Scanner", imgWrapped)
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break