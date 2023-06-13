import os
import cv2
import numpy as np
import HandTrackingModule as htm

folderPath = r"C:\Users\DELL\PycharmProjects\OpenCV\Resources\Header for Virtual Painter"
headerFilesList = os.listdir(folderPath)
print(headerFilesList)
overlayDict = {}
for imPath in headerFilesList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayDict[imPath[:-4]] = image
print(overlayDict.keys())

paletteBGR = {'Light Pink':(235, 233, 253), 'Violet':(230, 108, 203), 'Blue':(224, 183, 123), 'Green':(115, 182, 129),
              'Yellow':(48, 210, 255), 'Orange':(77, 145, 255), 'Red':(67, 49, 184), 'Black':(84, 84, 84), 'Eraser':(0, 0, 0)}

header = overlayDict['Light Pink']
sketchColor = (235, 233, 253)
brushThickness, eraserThickness = 10, 90
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.HandDetector(min_detection_confidence=0.5)

while True:
    #1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    #2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList)!=0:
        #print(lmList)

        # Tip of Index and Middle finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        #3. Check which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)

        #4. If two fingers are up - Selection Mode
        if fingers[1] and fingers[2]:
                #cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 15), sketchColor, cv2.FILLED )
            xp, yp = 0, 0
            cv2.putText(img, "Select", (x1, y1 - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                #print("Selection Mode")
            # Check for the click
            if y1 < 125:
                if 210<x1<310:
                    header = overlayDict['Light Pink']
                    sketchColor = paletteBGR['Light Pink']
                elif 324<x1<438:
                    header = overlayDict['Violet']
                    sketchColor = paletteBGR['Violet']
                elif 440<x1<550:
                    header = overlayDict['Blue']
                    sketchColor = paletteBGR['Blue']
                elif 556<x1<669:
                    header = overlayDict['Green']
                    sketchColor = paletteBGR['Green']
                elif 680<x1<790:
                    header = overlayDict['Yellow']
                    sketchColor = paletteBGR['Yellow']
                elif 794<x1<900:
                    header = overlayDict['Orange']
                    sketchColor = paletteBGR['Orange']
                elif 917<x1<1019:
                    header = overlayDict['Red']
                    sketchColor = paletteBGR['Red']
                elif 1033<x1<1140:
                    header = overlayDict['Black']
                    sketchColor = paletteBGR['Black']
                elif 1153<x1<1249:
                    header = overlayDict['Eraser']
                    sketchColor = paletteBGR['Eraser']
            # if y1>125:
            #     if xp == 0 and yp == 0:
            #         xp, yp = x1, y1
            #     if sketchColor == (0, 0, 0):
            #         cv2.line(img, (xp, yp), (x1, y1), sketchColor, eraserThickness*2)  # Erase On Video
            #         cv2.line(imgCanvas, (xp, yp), (x1, y1), sketchColor, eraserThickness*2)  # Erase On Canvas
            #     xp, yp = x1, y1
        #5. If Index finger is up - Drawing Mode
        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1,y1), 10, sketchColor, cv2.FILLED)
            # if header == overlayDict['Eraser']:
            #     cv2.putText(img, "Eraser", (x1, y1 - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                #print("Drawing Mode")
            if xp==0 and yp==0:
                xp, yp = x1, y1
            if sketchColor==(0, 0, 0):
                cv2.line(img, (xp,yp), (x1,y1), sketchColor, eraserThickness) # Erase On Video
                cv2.line(imgCanvas, (xp, yp), (x1, y1), sketchColor, eraserThickness) # Erase On Canvas
            else:
                cv2.line(img, (xp, yp), (x1, y1), sketchColor, brushThickness)  # Draw On Video
                cv2.line(imgCanvas, (xp, yp), (x1, y1), sketchColor, brushThickness)  # Draw On Canvas
            xp, yp = x1, y1
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    __, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)


    # Setting the header image
    img[0:125, 0:1450] = header
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)

    cv2.imshow("Virtual Painter",img)
    # cv2.imshow("Canvas", imgCanvas)
    print(img.shape, imgCanvas.shape)
    cv2.waitKey(1)



