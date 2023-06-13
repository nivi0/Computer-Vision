import os
import cv2
import numpy as np

print(os.path.exists(r"C:\Users\DELL\PycharmProjects\OpenCV\Resources\shapes.jpg"))

img = cv2.imread(r"C:\Users\DELL\PycharmProjects\OpenCV\Resources\shapes.jpg")
print(img.shape)
imgResize = cv2.resize(img, (604, 578))
imgCropped = img[20:200, 40:400]

# cv2.imshow("Shapes",img)
# cv2.imshow("Resized",imgResize)
# cv2.imshow("Cropped",imgCropped)

imgBlack = np.zeros((512,512,3),np.uint8)
cv2.line(imgBlack, (0,0), (imgBlack.shape[1],imgBlack.shape[0]), (255,0,255), 3)
cv2.rectangle(imgBlack, (50,50), (200,80), (100,150,250), 3)
cv2.circle(imgBlack, (100,300), 20, (250,150,150), 3, cv2.FILLED)
cv2.putText(imgBlack,"OpenCV", (300,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (100,255,10), 3)


cv2.imshow("Black",imgBlack)


cv2.waitKey(0)