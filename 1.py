import cv2 
import mediapipe as mp # کتابخانه پردازش تصویر گوگل

cap = cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils

def min(x1 , x2 , y1 , y2):
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    list = [x , y]
    return list

while True :
    SUCCESS , img = cap.read();
    RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(RGBimg)
    h , w , c = img.shape
    #print(result.multi_hand_landmarks)
    if result.multi_hand_landmarks:
        hndlist = []
        for handlms in result.multi_hand_landmarks:
            lmlist = []
            for id , lm in enumerate(handlms.landmark):
                x , y = int(lm.x * w) , int(lm.y * h)
                lmlist.append([id , x , y])
            hndlist.append([lmlist[5] , lmlist[17]])
            mpdraw.draw_landmarks(img , handlms , mphands.HAND_CONNECTIONS)
        print(hndlist)



    cv2.imshow("img" , img)
    cv2.waitKey(1)
