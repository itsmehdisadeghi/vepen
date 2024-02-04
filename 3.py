import math
import cv2 
import mediapipe as mp






cap = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils

while True :
    SUCCESS , img = cap.read();
    RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(RGBimg)
    h , w , c = img.shape
    if result.multi_hand_landmarks:
        hl = []
        for handlms in result.multi_hand_landmarks:
            lml = []
            for id , lm in enumerate(handlms.landmark):
                x , y = int(lm.x * w) , int(lm.y * h)
                lml.append([id , x , y])
            hl.append([lml[5] , lml[17]])
            x1 , y1 , x2 , y2 = hl[0][0][1] , hl[0][0][2] , hl[0][1][1] , hl[0][1][2]
            list = min(x1 , y1 , x2 , y2)
            ex , yi = int(list[0]) , int(list[1])
            cv2.circle(img , (ex , yi) , 10 , (0 , 0 , 0) , cv2.FILLED)
            hl.append([list])



