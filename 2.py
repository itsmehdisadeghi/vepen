import cv2
import mediapipe as mp


def min(x1 , x2 , y1 , y2):
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    list = [x , y]
    return list



cap = cv2.VideoCapture(0)

while True :
    SUCCESS , img = cap.read();
    RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h , w , c = img.shape
    hands = mp.solutions.hands.Hands()
    result = hands.process(RGBimg)
    if result.multi_hand_landmarks:
        hl = []
        for enyhand in result.multi_hand_landmarks:
            lml = []
            for id , lndmrk in enumerate(enyhand.landmark):
                x , y = int(lndmrk.x * w) , int(lndmrk.y * h)
                lml.append([id , x , y])
            hl.append([lml[5] , lml[17]])
            mp.solutions.drawing_utils.draw_landmarks(img , enyhand , mp.solutions.hands.HAND_CONNECTIONS)
    cv2.imshow("img" , img)
    cv2.waitKey(1)