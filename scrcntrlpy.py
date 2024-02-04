import cv2
import numpy as np
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volume.SetMasterVolumeLevel(, None)

colors = [[19,128,109,29,255,255]]

def Y(Y):
    if  0 < Y <= 48:
        ey = 10
    elif 48 < Y <= 96:
        ey = 9
    elif 96 < Y <= 144:
        ey = 8
    elif 144 < Y <= 192:
        ey = 7
    elif 192 < Y <= 240:
        ey = 6
    elif 240 < Y <= 288:
        ey = 5
    elif 288 < Y <= 336:
        ey = 4
    elif 336 < Y <= 384:
        ey = 3
    elif 384 < Y <= 432:
        ey = 2
    elif 432 < Y <= 480:
        ey = 1
    else:
        ey = 1
    return ey * 10


cap = cv2.VideoCapture(0)
while True:
    success , img = cap.read()
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
                sbc.set_brightness(igreg)
                print(igreg)
    cv2.imshow('gd' , imgcopy)
    if cv2.waitKey(1) == 13:
       break
cv2.destroyAllWindows()