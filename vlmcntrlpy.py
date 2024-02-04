import cv2
import numpy as np
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

colors = [[19,128,109,29,255,255]]

def Y(Y):
    if  0 < Y <= 60:
        ey = 1
    elif 60 < Y <= 120:
        ey = 2
    elif 120 < Y <= 180:
        ey = 10
    elif 180 < Y <= 240:
        ey = 15
    elif 240 < Y <= 300:
        ey = 20
    elif 300 < Y <= 360:
        ey = 25
    elif 360 < Y <= 420:
        ey = 30
    elif 420 < Y <= 480:
        ey = 35
    elif 480 < Y <= 540:
        ey = 45
    elif 540 < Y <= 600:
        ey = 60
    else:
        ey = 0
    return ey * -1


cap = cv2.VideoCapture(0)
while True:
    success , img = cap.read()
    img = cv2.resize(img , (640,600))
    imgcopy = img.copy()
    hsvimg = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
    for color in colors:
        lower = np.array([color[0:3]])
        upper = np.array([color[3:6]])
        mask = cv2.inRange(hsvimg , lower , upper)
        contours , hierchy = cv2.findContours(mask , cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            AREA = cv2.contourArea(contour)
            if AREA > 500:
                cv2.drawContours(imgcopy , contour , -1 , (255,0,0), 2)
                peri = cv2.arcLength(contour , True)
                approx = cv2.approxPolyDP(contour , 0.02 * peri , True)
                x , y , w , h = cv2.boundingRect(approx)
                igreg = Y(y+w//2)
                volume.SetMasterVolumeLevel(igreg, None)
                print(igreg)
    cv2.imshow('gd' , imgcopy)
    if cv2.waitKey(1) == 13:
       break
cv2.destroyAllWindows()