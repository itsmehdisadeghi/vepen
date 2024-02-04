import cv2
import numpy as np
import pyodbc


colors = [[0,51,74,23,131,255]]
#        [21,170,84,40,255,255]]
def sqlupdate(x,y,z,c):
    conn = pyodbc.connect('Driver={SQL Server};' + 'Server=KAYO;' + 'Database=swwb;' + 'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute(f"update dbo.main set x={x} , y={y} , z={z}  where c={c}")
    cursor.commit()

def z(area):
    if  1000 < area <= 2000 : z = 1
    elif 2000 < area <= 3000 : z = 2
    elif 3000 < area <= 4000 : z = 3
    elif 4000 < area <= 5000 : z = 4
    elif 5000 < area <= 6000 : z = 5
    elif 6000 < area <= 8000 : z = 6
    elif 8000 < area <= 10000 : z = 7
    elif 10000 < area <= 50000 : z = 8
    else : z = 1
    return z

def xoy(x , y):
    if y <= 60:
        if x <= 210:
            xy = [1,1]
            return xy
        elif 210 < x <= 430:
            xy = [2,1]
            return xy
        else:
            xy = [3,1]
            return xy
    elif 60 < y <= 120:
        if x <= 80:
            xy = [1,2]
            return xy
        elif 210 < x <= 430:
            xy = [2,2]
            return xy
        else:
            xy = [3,2]
            return xy
    elif 120 < y <= 180:
        if x<=210:
            xy = [1,3]
            return xy
        elif 210 < x <= 430:
            xy =[2,3]
            return xy
        else:
            xy = [3,3]
            return xy

def x(0):


def nahie(cap):
    success , img = cap.read()
    img = cv2.flip(img, 1)
    print(img.shape)
    imgcopy = img.copy()
    hsvimg = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
    for color in colors:
        lower = np.array([color[0:3]])
        upper = np.array([color[3:6]])
        mask = cv2.inRange(hsvimg , lower , upper)
        contours , hierchy = cv2.findContours(mask , cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                cv2.drawContours(imgcopy , contour , -1 , (255,0,0), 2)
                peri = cv2.arcLength(contour , True)
                approx = cv2.approxPolyDP(contour , 0.02 * peri , True)
                x , y , w , h = cv2.boundingRect(approx)
                if color[0] == 30 : c = 0
                else : c = 1
                xyzc = [x(x+w//2), y(y+h//2) , z(area) , c]
                
                xyzc =  , 
                xyzc.append(colorname)
                sqlupdate(xyzc[0],xyzc[1],xyzc[2],xyzc[3])
                print(xyzc)
    imgcopy = cv2.resize(imgcopy , (290,200))
    cv2.imshow('img' , imgcopy)
    cv2.imshow('img,' , hsvimg)

cap = cv2.VideoCapture(0)

while True:
    nahie(cap)
    if cv2.waitKey(1) == 13:
       break

cv2.destroyAllWindows()