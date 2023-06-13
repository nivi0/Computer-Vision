import os
print(os.path.exists(r"C:\Users\DELL\PycharmProjects\OpenCV\Resources\cards.jpg"))

import cv2
import numpy as np

img = cv2.imread(r"C:\Users\DELL\PycharmProjects\OpenCV\Resources\cards.jpg")
width, height = 250,350

pts1 = np.float32([[493,28],[574,203],[326,317],[245,141]])
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
result = cv2.warpPerspective(img, matrix, (width, height))

cv2.imshow("Wrapped Perspective",result)
cv2.waitKey(0)