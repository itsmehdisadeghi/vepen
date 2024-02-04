import pyodbc
import cv2
conn = pyodbc.connect('Driver={SQL Server};'
    'Server=KAYO;'
    'Database=swwb;'
    'Trusted_Connection=yes;')

i11 = cv2.imread('1,1.png')
i12 = cv2.imread('1,2.png')
i13 = cv2.imread('1,3.png')
i21 = cv2.imread('2,1.png')
i22 = cv2.imread('2,2.png')
i31 = cv2.imread('3,1.png')
i33 = cv2.imread('3,3.png')
cv2.imshow('warmwar' , i12)
while True:
    cursor = conn.cursor()
    cursor.execute("select z from  dbo.main")
    cur = cursor.fetchall()
    sql = [cur[0][0] , cur[1][0]]
    if sql == [1,1]:
        cv2.imshow('warmwar' , i11)
    elif sql == [1,2]:
        cv2.imshow('warmwar' , i12)
    elif (sql == [1,3]) or (sql == [2,3]):
        cv2.imshow('warmwar' , i13)
    elif sql == [2,1]:
        cv2.imshow('warmwar' , i21)
    elif sql == [2,2]:
        cv2.imshow('warmwar' , i22)
    elif (sql == [3,1]) or (sql == [3,2]):
        cv2.imshow('warmwar' , i31)
    elif sql == [3,3]:
        cv2.imshow('warmwar' , i33)
    if cv2.waitKey(1) == 13:
        break
cv2.destroyAllWindows()
