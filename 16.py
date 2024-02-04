#######################################################IMOPORTS######################################################################################
import cv2    # ketabkhane pardazesh tasvir opencv
import numpy as np # ketabkhane numpy baraye kar ba aadad
import pyodbc  # ketabkhane pyodbc baraye kar ba database ha dar inja (sql server)
from time import sleep as delay
######################################################################################################################################################
# dar vaghe in maghadir barabar and ba colors = [huemin,satmin,valmin , huemax,satmax,valmax]
colors = [[30,60,64,49,255,255],# code range sabz
          [20,54,125,34,255,255]] # code range zard
#################################################IMG############################################################################################################
i11 = cv2.imread('1,1.png')
i12 = cv2.imread('1,2.png')
i13 = cv2.imread('1,3.png')
i21 = cv2.imread('2,1.png')
i22 = cv2.imread('2,2.png')
i31 = cv2.imread('3,1.png')
i33 = cv2.imread('3,3.png')
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
#################################################APP#####################################################################################################
def nahie(cap): # cap haman tasvir ast ke modam az doorbin daryaft mishavad
    success , img = cap.read()# dar inja ba estefade az opencv tasvir ra mikhanim va dar moteghayer img mirizim (haman dorbin ast)
    cam = cv2.resize(img , (290,200))
    cv2.imshow('cam' , cam)
    hsvimg = cv2.cvtColor(img , cv2.COLOR_BGR2HSV) # baraye pardazesh img ra shv mikonim
    di = 10
    for color in colors: # be ezay har rang dar moteghayer color k bala tarif kardim yek halghe ijad mishavad
        lower = np.array([color[0:3]]) # lower maghadir 0 , 1 , 2 har kodam az rang ha mibashand ya be ebarat digar huemin , satmin , valmin har rang ra dar lower mirizim
        upper = np.array([color[3:6]])# upper maghadir 3 , 4 , 5 har kodam az rang ha mibashand ya be ebarat digar hueminhuemax , satmax , valmax har rang ra dar lower mirizim
        mask = cv2.inRange(hsvimg , lower , upper)# dar inja ba estefade az tabe inRange opencv mitavanim yek tasvir siah va sefid az anche mikhahim bedast biavarim ke anjaii ke mikhahim sefid ast . rang sefid ra az list hay lower va upper bedast miavarim
        contours , hierchy = cv2.findContours(mask , cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_NONE)#bedast avardan gooshe ha (list hay besiar bozorgi hastand ke mokhtasat goshe ha ra darand)
        for contour in contours: # be azaye har goshe dar contur yek halghe darim
            area = cv2.contourArea(contour) # baraye bedast avardan masahat jesm az contourArea estefade mikonim
            if area > 500: # in kar baes mishavad faghat ajsame tashkhis dadeh shode ii ke masahat anha bishtar az 500 ast detect ishavand
                di = distance(area) # meghdar z
                if color[0] == 30: # tashkhis inke kodam rang dar hal barresi ast 
                    colorname = 0 # sabz
                else:
                    colorname = 1 # zard
                leest = [colorname , di]
                return(leest)
##################################################################################################################################################################################
def pic(cap):
    if nahie(cap) == None:
        cv2.imshow('warmwar' , i11)
#################################################PICTURE#####################################################################################################
cap = cv2.VideoCapture(0) # gereftan tasvir az durbin
#################################################WHILE#####################################################################################################
while True:
    print(nahie(cap)) # ejraye nahie
    if cv2.waitKey(1) == 13: # agar enter click shod
       break# halghe ra beshkan
cv2.destroyAllWindows()# panjere ha ra nabood kon alllllllllah
#########################################################################################################################################################