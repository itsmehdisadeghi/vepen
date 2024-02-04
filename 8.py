import cv2
import socket
import math
import mediapipe as mp

cap = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils

def send(dataa):
    sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
    data = str.encode(str(dataa))
    sap = ('127.0.0.1' , 5052)
    sock.sendto(data , sap)
    print(f"{data}sent!")

def min(x1 , y1 , x2 , y2 , w , h):
    x = int(int((x1 + x2) / 2) - (w/2))
    y = int((h/2) - int((y1 + y2) / 2))
    if (x1 - x2 ) != 0 : 
        a = (y1 - y2) / (x1 - x2)
        a = int(math.degrees(math.atan(a)))
    else:
        a = 0
    z = int(math.hypot(x2 - x1 , y2 - y1))
    list = [x,y,z,a]
    return list

while True :
    data = []
    SUCCESS , img = cap.read();
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
            x1 , y1 , x2 , y2 = lm[5][0] , lm[5][1] , lm[17][0] , lm[17][1] 
            cv2.line(img , (x1 , y1) , (x2 , y2) , (0,0,255) , 1)
            cv2.circle(img , (x1 , y1) , 4 , (255,0,0) , cv2.FILLED)
            cv2.circle(img , (x2 , y2) , 4 , (255,0,0) , cv2.FILLED) 
            wanted.append([lm[5] , lm[17]])
        if wanted != None :
            for hnd in wanted:
                x1 , y1 , x2 , y2 = hnd[0][0] , hnd[0][1] , hnd[1][0] , hnd[1][1]
                listt = min(x1,y1,x2,y2 , w , h)
                ix , iy = listt[0] , listt[1]
                cv2.circle(img , (ix , iy) , 5 , (0,0,0) , cv2.FILLED )
                data.append(listt)
    if data == [] :
        data = [[0,0,0,0],[0,0,0,0]]
    if len(data) == 1 :
        empty = [0,0,0,0]
        data.append(empty)
        send(data)
    elif len(data) == 2 :
        send(data)
    cv2.imshow("img" , img)
    cv2.waitKey(1)

#[[167, 211, 2, 43], [473, 187, 3, -35]]
#[[x1 , y1 ,z1 , a1],[x2 , y2 , z2 , a2]]