w = 640
h = 480

def hue(data):
    x1 , y1 , z1 , a1 , x2 , y2 , a2 = (data[0][0]) - (w/2) , (data[0][1]) - (w/2) , dat[0][2] , data[0][3] , (data[1][0]) - (w/2) , (h/2) - (data[1][1]) , dat[1][2] , data[1][3]
    data = [x1 , y1 , z1 , a1 , x2 , y2 , a2] 
    print(data)


dat = [[167, 211, 2, 43], [473, 187, 3, -35]]



hue(dat)