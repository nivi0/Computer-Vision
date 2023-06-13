import os
import cv2

print(os.path.exists(r'C:\Users\DELL\PycharmProjects\OpenCV\Resources\haarcascade_frontalface_default.xml'))

faceCascade = cv2.CascadeClassifier(r'C:\Users\DELL\PycharmProjects\OpenCV\Resources\haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 100), 2)
    cv2.imshow("Face Detection",img)

    if cv2.waitKey(1) & 0xFF==ord(' '):
        break