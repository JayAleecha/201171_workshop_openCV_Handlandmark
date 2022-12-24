import cv2
import mediapipe as mp
import numpy as np
import math
cap = cv2.VideoCapture(0)

    
def scale(x1,y1,x2,y2):
    return math.sqrt(pow(x1-x2,2)+pow(y1-y2,2))   
    
    


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
with mpHands.Hands(min_detection_confidence=0.5,
               min_tracking_confidence=0.5) as hands:
 while True:
        ret,image=cap.read() 
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
        image.flags.writeable=False 
        results=hands.process(image) 
        image.flags.writeable=True 
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 
        FL=[]

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0]
                
                for id, lm in enumerate(myHands.landmark):
                    h,w,c=image.shape
                    cx,cy= int(lm.x*w), int(lm.y*h)
                    FL.append([id,cx,cy])
            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
        fingers=[]
        fc= []
        #print(FL)
        #vector
        


        #print(fingers)  
        if ((results.multi_hand_landmarks))!="None":
            if(len(FL)!=0):
                V0_5=[FL[5][1]-FL[0][1],FL[5][2]-FL[0][2]]
                v0_17=[FL[17][1]-FL[0][1],FL[17][2]-FL[0][2]]
                product_V=(np.cross(V0_5,v0_17))
                FL0x,FL0y= FL[0][1],FL[0][2]
                FL4x,FL4y= FL[4][1],FL[4][2]
                FL5x,FL5y= FL[5][1],FL[5][2]
                FL8x,FL8y= FL[8][1],FL[8][2]
                FL12x,FL12y= FL[12][1],FL[12][2]
                FL16x,FL16y= FL[16][1],FL[16][2]
                FL20x,FL20y= FL[20][1],FL[20][2]
                FL17x,FL17y= FL[17][1],FL[17][2]
                sc= scale(FL5x,FL5y,FL17x,FL17y)
                s4= int(scale(FL17x,FL17y,FL4x,FL4y)*40/sc)
                s8= int(scale(FL0x,FL0y,FL8x,FL8y)*30/sc)
                s12= int(scale(FL0x,FL0y,FL12x,FL12y)*30/sc)
                s16= int(scale(FL0x,FL0y,FL16x,FL16y)*30/sc)
                s20= int(scale(FL0x,FL0y,FL20x,FL20y)*30/sc)
                
                sl= [s4,s8,s12,s16,s20]
                lf= ["Thump","Index","Middle","Ring","Little"]
                
                #print(product_V)
                
                if product_V<0:
                    for i in range (5):
                        #print(sl)
                        if sl[i]>60:
                            fingers.append(1)
                            fc.append(lf[i])
                        else:
                            fingers.append(0)    
                #print(fingers)
                elif product_V>0:
                    for i in range (5):
                        if sl[i]>60:
                            fingers.append(1)
                            fc.append(lf[i])
                        else:
                            fingers.append(0)  
            if len(fc)!=0:
                nf= " ".join(fc)
                cv2.putText(image,str(nf), (25, 100), cv2.FONT_HERSHEY_SIMPLEX,
                1, (225, 1, 0), 2)
            cv2.putText(image, str(fingers.count(1)), (5,50), cv2.FONT_HERSHEY_SIMPLEX,
                1.5, (225, 1, 0), 3)
            
                
        cv2.imshow("Video", image)
        z=cv2.waitKey(1)
        if z==ord('z'):
            break
 image.release()
cv2.destroyAllWindows()