import cv2
import numpy as np

colors = [[21,170,84,40,255,255]]

def nahie(cap):
    success , img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.resize(img , (1366,768))
    hsvimg = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
    for color in colors:
        lower = np.array([color[0:3]])
        upper = np.array([color[3:6]])
        mask = cv2.inRange(hsvimg , lower , upper)
        contours , hierchy = cv2.findContours(mask , cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                cv2.drawContours(img , contour , -1 , (255,0,0), 2)
    cv2.imshow('img' , img)

cap = cv2.VideoCapture(0)

while True:
    nahie(cap)
    if cv2.waitKey(1) == 13:
       break

cv2.destroyAllWindows()