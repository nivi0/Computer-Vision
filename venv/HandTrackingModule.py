import cv2
import mediapipe as mp
import time

class HandDetector():

    def __init__(self, static_image_mode=False, max_num_hands=2, model_complexity=1
                 , min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.model_complexity = model_complexity
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.static_image_mode, self.max_num_hands, self.model_complexity,
                                        self.min_detection_confidence, self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

        self.tipsId = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        #print(result.multi_hand_landmarks)
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        self.lmList = []
        if self.result.multi_hand_landmarks:
            hand = self.result.multi_hand_landmarks[handNo]
            for id,lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)
        return self.lmList

    def fingersUp(self):

        fingers = []

        # Thumb
        if self.lmList[self.tipsId[0]][1] < self.lmList[self.tipsId[0] -1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # Other 4 fingers
        for id in range(1,5):
            if self.lmList[self.tipsId[id]][2] < self.lmList[self.tipsId[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers


def main():

    cap = cv2.VideoCapture(0)
    pTime, cTime = 0, 0

    detector = HandDetector()

    while True:
        success, img = cap.read()
        # img = cv2.flip(img,1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
        cv2.imshow("Hand Tracking", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()