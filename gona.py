import pyodbc
import cv2
conn = pyodbc.connect('Driver={SQL Server};'
    'Server=KAYO;'
    'Database=swwb;'
    'Trusted_Connection=yes;')

i11 = cv2.imread('')

while True:
    cursor = conn.cursor()
    cursor.execute("select z from  dbo.main")
    cur = cursor.fetchall()
    sql = [cur[0][0] , cur[1][0]]
    if sql == [1,1]:
        cv2.imshow('warmwar' , i11)
    if cv2.waitKey(1) == 13:
        break
cv2.destroyAllWindows()