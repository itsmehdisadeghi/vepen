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

def detector(img , p1 , p2):
    RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(RGBimg)
    h , w , c = img.shape
    if result.multi_hand_landmarks:
        wanted = []
        for enyhnd in result.multi_hand_landmarks:
            lm = []
            for id , llm in enumerate(enyhnd.landmark):
                x , y = int(llm.x * w) , int(llm.y * h)
                lm.append([x , y])
            x1 , y1 , x2 , y2 = lm[p1][0] , lm[p1][1] , lm[p2][0] , lm[p2][1] 
            cv2.circle(img , (x1 , y1) , 3 , (255,0,0) , cv2.FILLED)
            cv2.circle(img , (x2 , y2) , 3 , (255,0,0) , cv2.FILLED , 10) 
            cv2.line(img , (x1 , y1) , (x2 , y2) , (0,0,255))
            wanted.append([lm[p1] , lm[p2]])
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