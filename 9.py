import cv2 
import mediapipe as mp 
from cvzone.FaceMeshModule import FaceMeshDetector as fd
import math
cap = cv2.VideoCapture(0)
face_Detected = fd(maxFaces=1)
mphands = mp.solutions.hands
hands =  mphands.Hands()
mpdraw = mp.solutions.drawing_utils

def send(dataa):
    sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
    data = str.encode(str(dataa))
    sap = ('127.0.0.1' , 5052)
    sock.sendto(data , sap)
    #print(f"{data}sent!")

def xoy(img , parameter):
    RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(RGBimg)
    h , w , c = img.shape
    if result.multi_hand_landmarks:
        xoy = []
        lm517 = []
        for enyhnd in result.multi_hand_landmarks:
            lm = []
            for id , llm in enumerate(enyhnd.landmark):
                x , y = int(llm.x * w) , int(llm.y * h)
                lm.append([x , y])
            lm517.append([lm[5] , lm[17]])
            x1 , y1 , x2 , y2 = lm[5][0] , lm[5][1] , lm[17][0] , lm[17][1]
            w = int(math.hypot(x2 - x1 , y2 - y1))
            W = 7
            f = 630
            d = (W * f) / w
            xoy.append(x1 , y1 , x2 , y2)
            if parameter == "xoy":
                return xoy
            elif parameter == "dis":
                return d
            elif parameter == "lm517":
                return lm517

def zed(img):
    img , faces = face_Detected.findFaceMesh(img , draw = False)
    if faces:
        face = faces[0]
        pel = face[145]
        per = face[374]
        cv2.line(img , pel , per , (0,0,0) , 2)
        cv2.circle(img , pel , 5 , (0,0,255) , cv2.FILLED)
        cv2.circle(img , per , 5 , (0,0,255) , cv2.FILLED)
        w , i = face_Detected.findDistance(pel , per)
        W = 6.3
        f = 630
        d = (W * f) / w

    RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(RGBimg)
    h , w , c = img.shape
    if result.multi_hand_landmarks:
        wanted = []
        for enyhnd in result.multi_hand_landmarks:
            lm = []
            mpdraw.draw_landmarks(img , enyhnd , mphands.HAND_CONNECTIONS)
            for id , llm in enumerate(enyhnd.landmark):
                x , y = int(llm.x * w) , int(llm.y * h)
                lm.append([x , y])

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

def data(img , parameter):
    wanted = xoy(img , "lm517")
    if wanted != None :
        for hnd in wanted:
            x1 , y1 , x2 , y2 = hnd[0][0] , hnd[0][1] , hnd[1][0] , hnd[1][1]
            listt = min(x1,y1,x2,y2)
            ix , iy = listt[0] , listt[1]
            cv2.circle(img , (ix , iy) , 5 , (0,0,0) , cv2.FILLED )
            data.append(listt)
    if data == [] :
        data = [[0,0,0,0],[0,0,0,0]]
    if len(data) == 1 :
        empty = [0,0,0,0]
        data.append(empty)
        return(data)
    elif len(data) == 2 :
        return(data)



          




while True :
    SUCCESS , img = cap.read();
    img , faces = face_Detected.findFaceMesh(img , draw = False)
    send(data)
    cv2.imshow("img" , img)
    cv2.waitKey(1)






