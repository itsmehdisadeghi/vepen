#######################################################IMOPORTS######################################################################################
import cv2    # ketabkhane pardazesh tasvir opencv
import numpy as np # ketabkhane numpy baraye kar ba aadad
import pyodbc  # ketabkhane pyodbc baraye kar ba database ha dar inja (sql server)
from time import sleep as delay
######################################################################################################################################################
# dar vaghe in maghadir barabar and ba colors = [huemin,satmin,valmin , huemax,satmax,valmax]
colors = [[30,60,64,49,255,255],# code range sabz
          [20,54,125,34,255,255]] # code range zard
#################################################DEFINING SQL CONNECTOR#############################################################################
def sqlupdate(x,y,z,c):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=.;'
                          'Database=swwb;'
                          'Trusted_Connection=yes;')# etesal be database sql sever
    cursor = conn.cursor() # ijad query
    cursor.execute(f"update dbo.main set x={x} , y={y} , z={z}  where c={c}") # update kardan khaneii ke rang an meghdar 'c'  bashad .  update kardan x,y,z khane be x,y,z jadid
    cursor.commit()# zakhire etelaat
#################################################DISTANCE############################################################################################
def distance(area):# fasele va masahat jesm rabete maakus darand . dar inja faselee bein 1000 jh 6000 ra 1 va faseley bein 6000 ta 12000 ra 2 va faseleii 1200 jh 50000 ra faselii 3 dar nazar migirim va in meghdar yani dis barabar ba 'z mibashad
    z = 1# dar zemn z dar halat adi 1 ast
    if  1000 < area <= 6000:
        z = 1
    elif 6000 < area <= 12000:
        z = 2
    elif 12000 < area < 50000:
        z = 3
    else:
        z = 1
    return z 
#################################################X&Y###################################################################################################
def xoy(x , y):#  dar inja ebteda moshakhas mishavad ke y dar koja gharar darad . sepas x ra barresi mikonim va dar nahayat angha ra dar motehgayere 'xy' mirizam va sepas return  mikonim
    if y <= 160: #  y bein 0 ta 160 dar mahdoodei 1 gharar darad (in adad az taghsim 480 be 3 bedast amade ast ke har mahdoodeh 160 vahed tool darad)
        if x <= 210: # y bein 0 ta 210 dar mahdoodei 1 gharar dard(in meghdar az taghsmi
            xy = [1,1]
            return xy
        elif 210 < x <= 430: #  x = 2
            xy = [2,1]
            return xy
        else: # x = 3
            xy = [3,1]
            return xy
    elif 160 < y <= 320: # y = 2
        if x <= 210: #x=1
            xy = [1,2]
            return xy
        elif 210 < x <= 430:#x=2
            xy = [2,2]
            return xy
        else:#x=3
            xy = [3,2]
            return xy
    else:#y=3
        if x<=210:#x=1
            xy = [1,3]
            return xy
        elif 210 < x <= 430:#x=2
            xy =[2,3]
            return xy
        else:#x=3
            xy = [3,3]
            return xy
#################################################APP#####################################################################################################
def nahie(cap): # cap haman tasvir ast ke modam az doorbin daryaft mishavad
    outimg = np.zeros((200,1000,3) , np.uint8) # ba estefade az ketabkhne numpy yek tasvir siah be andaze 200x1000 tolid mikonim
    success , img = cap.read()# dar inja ba estefade az opencv tasvir ra mikhanim va dar moteghayer img mirizim (haman dorbin ast)
    imgcopy = img.copy() # az img yek copy migirim va an ra dar cimg
    hsvimg = cv2.cvtColor(img , cv2.COLOR_BGR2HSV) # baraye pardazesh img ra shv mikonim
    di = 10
    for color in colors: # be ezay har rang dar moteghayer color k bala tarif kardim yek halghe ijad mishavad
        lower = np.array([color[0:3]]) # lower maghadir 0 , 1 , 2 har kodam az rang ha mibashand ya be ebarat digar huemin , satmin , valmin har rang ra dar lower mirizim
        upper = np.array([color[3:6]])# upper maghadir 3 , 4 , 5 har kodam az rang ha mibashand ya be ebarat digar hueminhuemax , satmax , valmax har rang ra dar lower mirizim
        mask = cv2.inRange(hsvimg , lower , upper)# dar inja ba estefade az tabe inRange opencv mitavanim yek tasvir siah va sefid az anche mikhahim bedast biavarim ke anjaii ke mikhahim sefid ast . rang sefid ra az list hay lower va upper bedast miavarim
        contours , hierchy = cv2.findContours(mask , cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_NONE)#bedast avardan gooshe ha (list hay besiar bozorgi hastand ke mokhtasat goshe ha ra darand)
        for contour in contours: # be azaye har goshe dar contur yek halghe darim
            area = cv2.contourArea(contour) # baraye bedast avardan masahat jesm az contourArea estefade mikonim
            if di ==10: # agar di bozorgttar az 10 bood 
                cv2.line(outimg , (0,50) , (di,50) , (100,200,100) , 3) #keshidan khat sabz dar outimg
                cv2.line(outimg , (0,150) , (di,150) , (0,255,0) , 3) #keshidan khat zard dar outimg
            if area > 500: # in kar baes mishavad faghat ajsame tashkhis dadeh shode ii ke masahat anha bishtar az 500 ast detect ishavand
                peri = cv2.arcLength(contour , True)
                approx = cv2.approxPolyDP(contour , 0.02 * peri , True)
                x , y , w , h = cv2.boundingRect(approx)
                xyzc = xoy(x+w//2 , y+h//2)
                di = distance(area) # meghdar z
                xyzc.append(di) # afzodn z beh xyzc
                if color[0] == 30: # tashkhis inke kodam rang dar hal barresi ast 
                    colorname = 0 # sabz
                else:
                    colorname = 1 # zard
                xyzc.append(colorname) # ezafe kardan rang
                sqlupdate(xyzc[0],xyzc[1],xyzc[2],xyzc[3]) # zakhreh kardan dar bank
                di = distance(area) * 200 # inkar baes mishavd vaghti naheieh ke ya 1 ya 2 ya 3 ast .vaghti bedast amad * 200 shavad ta meghdarash bozorg tar shavad va dar out img ghabel moshahede bashad
                if color[0] == 30: # agar rang sabz bood
                    cv2.line(outimg , (0,50) , (di,50) , (100,200,100) , 3)# keshidan khat sabz be andazeh 'di' 
                else: # dar gheir insoorat (rang zard)
                    cv2.line(outimg , (0,150) , (di,150) , (0,255,0) , 3) # keshidan khat zard be andazeh 'di'
    cv2.imshow('gd' , imgcopy) #namayesh gd
#################################################PICTURE#####################################################################################################
cap = cv2.VideoCapture(0) # gereftan tasvir az door bin
#################################################WHILE#####################################################################################################
while True:
    nahie(cap) # ejraye nahie
    if cv2.waitKey(1) == 13: # agar enter click shod
       break# halghe ra beshkan
cv2.destroyAllWindows()# panjere ha ra nabood kon
#########################################################################################################################################################
