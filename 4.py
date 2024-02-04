import cv2
import math
import mediapipe as mp
cap = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils
x1 , y1 , z1 , a1 , x2 , y2 , z2 , a2 = 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0
def min(x1 , y1 , x2 , y2):
    x = int((x1 + x2) / 2)
    y = int((y1 + y2) / 2)
    if (x1 - x2 ) != 0 : 
        a = int((y1 - y2) / (x1 - x2) *100)
    else:
        a = 0
    d = int(math.hypot(x2 - x1 , y2 - y1))
    list = [x , y , d , a]
    return list
def detector(img , firstpos , secondpos):
    RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(RGBimg)
    h , w , c = img.shape
    if result.multi_hand_landmarks:
        wanted = []
        for enyhnd in result.multi_hand_landmarks:
            landmarks = []
            for id , lm in enumerate(enyhnd.landmark):
                x , y = int(lm.x * w) , int(lm.y * h)
                landmarks.append([x , y])
            mpdraw.draw_landmarks(img , enyhnd , mphands.HAND_CONNECTIONS)
            wanted.append([landmarks[firstpos] , landmarks[secondpos]])
        return wanted

while True :
    SUCCESS , img = cap.read();
    dtct = detector(img , 5 , 17)
    data = []
    if dtct != None:
        for hnd in dtct:
            x1 , y1 , x2 , y2 = hnd[0][0] , hnd[0][1] , hnd[1][0] , hnd[1][1]
            listt = min(x1 , y1 , x2 , y2)
            data.append(listt)
    print(data)
    cv2.imshow("img" , img)
    cv2.waitKey(1)