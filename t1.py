import cv2
import socket
import math
import mediapipe as mp
from cvzone.FaceMeshModule import FaceMeshDetector as fd




cap = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils
face_Detected = fd(maxFaces=1)

def send(dataa):
    sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
    data = str.encode(str(dataa))
    sap = ('127.0.0.1' , 5052)
    sock.sendto(data , sap)
    print(f"{dataa}sent!")

def min(x1 , y1 , x2 , y2):
    x = int((x1 + x2) / 2)
    y = int((y1 + y2) / 2)
    if (x1 - x2 ) != 0 : 
        a = (y1 - y2) / (x1 - x2)
        a = int(math.degrees(math.atan(a)))
    else:
        a = 0
    z = int(math.hypot(x2 - x1 , y2 - y1))
    list = [x,y,z,a]
    return list

def cam(img):
    img , faces = face_Detected.findFaceMesh(img , draw = False)
    h , w , c = img.shape
    if faces:
        face = faces[0]
        pel = face[145]
        per = face[374]
        x = int((pel[0] + per[0]) / 2)
        y = int((pel[1] + per[1]) / 2)
        lis = [x , y]
    if lis == []:
        lis = [0 , 0 , 0]
    return lis

while True :
    data = []
    SUCCESS , img = cap.read();
    img = cv2.flip(img, 1)
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
                listt = min(x1,y1,x2,y2)
                ix , iy = listt[0] , listt[1]
                cv2.circle(img , (ix , iy) , 5 , (0,0,0) , cv2.FILLED )
                data.append(listt)
    if data == [] :
        ki = cam(img)
        data = [[0,0,0,0],[0,0,0,0]]
        data.append(ki)
    if len(data) == 1 :
        empty = [0,0,0,0]
        data.append(empty)
        ki = cam(img)
        data.append(ki)
        send(data)
    elif len(data) == 2 :
        ki = cam(img)
        data.append(ki)
        send(data)
    else:
        ki = cam(img)
        data = [[0,0,0,0],[0,0,0,0]]
        data.append(ki)
        send(data)
    cv2.imshow("img" , img)
    cv2.waitKey(1)
