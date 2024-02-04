import cv2 
import mediapipe as mp 
from cvzone.FaceMeshModule import FaceMeshDetector as fd
import math
import socket

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
    print("sent")

# def xoy(img):
#     RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     result = hands.process(RGBimg)
#     h , w , c = img.shape
#     xoy = []
#     if result.multi_hand_landmarks:
#         for enyhnd in result.multi_hand_landmarks:
#             lm = []
#             for id , llm in enumerate(enyhnd.landmark):
#                 x , y = int(llm.x * w) , int(llm.y * h)
#                 lm.append([x , y])
#             x1 , y1 , x2 , y2 = lm[5][0] , lm[5][1] , lm[17][0] , lm[17][1]
#             x = int(int((x1 + x2) / 2) - (w/2))
#             y = int((h/2) - int((y1 + y2) / 2))
#             if (x1 - x2 ) != 0 :
#                 a = (y1 - y2) / (x1 - x2) 
#                 a = int(math.degrees(math.atan(a)))
#             else:
#                 a = 0
#             xoy.append([x , y , a])
#     if xoy == []:
#         xoy = [[0,0,0,0],[0,0,0,0]]
#     return xoy

def cam(img):
    img , faces = face_Detected.findFaceMesh(img , draw = False)
    h , w , c = img.shape
    lis = []
    if faces:
        face = faces[0]
        pel = face[145]
        per = face[374]
        x = ( int((pel[0] + per[0]) / 2) ) - (w/2)
        y = (h/2) - (int((pel[1] + per[1]) / 2))
        w , i = face_Detected.findDistance(pel , per)
        W = 6.3
        f = 630
        d = int((W * f) / w)
        lis.append([d , x , y])
    if lis == []:
        lis = [0 , 0 , 0]
    return lis

def hand_d(img):
    RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(RGBimg)
    h , w , c = img.shape
    ds = []
    W = 7
    f = 630
    if result.multi_hand_landmarks:
        for enyhnd in result.multi_hand_landmarks:
            lm = []
            for id , llm in enumerate(enyhnd.landmark):
                x , y = int(llm.x * w) , int(llm.y * h)
                lm.append([x , y])
            x1 , y1 , x2 , y2 = lm[5][0] , lm[5][1] , lm[17][0] , lm[17][1]
            w = int(math.hypot(x2 - x1 , y2 - y1))
            d = int((W * f) / w)
            ds.append(d)
            print(d)
    if ds == []:
        ds.append(0)
        ds.append(0)
    
    if len(ds) != 1:
        utpt=[ds[0] , ds[1]]
    else:
        ds.append(0)
        utpt = ds
    return utpt

def zed(img):
    camd = cam(img)
    handd = hand_d(img)
    z = []
    for han in handd:
        zed = camd[0] - han
        ze = int(zed/7)
        z.append(ze)
    return z
            


# def data(img):
#     xo = xoy(img)
#     ze = zed(img)
#     ca = cam(img)
#     x1 , y1 , a1  , z1 , x2 , y2 , a2 , z2 , x3 , y3 = xo[0][0] , xo[0][1] , xo[0][2] , ze[0] , ca[0][1] , ca[0][2] , xo[1][0] , xo[1][1] , xo[1][2] , ze[1] 
#     data = [x1 , y1 , a1  , z1 , x2 , y2 , a2 , z2 , x3 , y3]
#     return(data)



while True :
    SUCCESS , img = cap.read();
    img = cv2.flip(img, 1)
    img , faces = face_Detected.findFaceMesh(img , draw = False)
    hand_d(img)
    # print(data)
    cv2.imshow("img" , img)
    cv2.waitKey(1)