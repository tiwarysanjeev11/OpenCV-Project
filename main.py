import cv2
import numpy as np
import vehicles
import time
from firebase import firebase

firebase = firebase.FirebaseApplication('https://raspberry-c6301.firebaseio.com/')
for xz in ("/home/pi/traffic python/sur1.mp4" ,"/home/pi/traffic python/sur2.mp4" , "/home/pi/traffic python/sur3.mp4","/home/pi/traffic python/sur4.mp4"): 
    
    cnt_down=0
    cap=cv2.VideoCapture(xz)

    w=cap.get(3)
    h=cap.get(4)
    frameArea=h*w
    areaTH=frameArea/400

    line_up=int(2*(h/5))
    line_down=int(3*(h/5))

    up_limit=int(1*(h/5))
    down_limit=int(4*(h/5))

    
    line_down_color=(255,0,0)
    line_up_color=(255,0,255)
    pt1 =  [0, line_down]
    pt2 =  [w, line_down]
    pts_L1 = np.array([pt1,pt2], np.int32)
    pts_L1 = pts_L1.reshape((-1,1,2))
    pt3 =  [0, line_up]
    pt4 =  [w, line_up]
    pts_L2 = np.array([pt3,pt4], np.int32)
    pts_L2 = pts_L2.reshape((-1,1,2))

    pt5 =  [0, up_limit]
    pt6 =  [w, up_limit]
    pts_L3 = np.array([pt5,pt6], np.int32)
    pts_L3 = pts_L3.reshape((-1,1,2))
    pt7 =  [0, down_limit]
    pt8 =  [w, down_limit]
    pts_L4 = np.array([pt7,pt8], np.int32)
    pts_L4 = pts_L4.reshape((-1,1,2))

    fgbg=cv2.createBackgroundSubtractorMOG2(detectShadows=True)

    kernalOp = np.ones((3,3),np.uint8)
    kernalOp2 = np.ones((5,5),np.uint8)
    kernalCl = np.ones((11,11),np.uint8)


    font = cv2.FONT_HERSHEY_SIMPLEX
    cars = []
    max_p_age = 5
    pid = 1


    while(cap.isOpened()):
        ret,frame=cap.read()
        for i in cars:
            i.age_one()
        fgmask=fgbg.apply(frame)
        fgmask2=fgbg.apply(frame)

        if ret==True:

            ret,imBin=cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
            ret,imBin2=cv2.threshold(fgmask2,200,255,cv2.THRESH_BINARY)
            
            mask=cv2.morphologyEx(imBin,cv2.MORPH_OPEN,kernalOp)
            mask2=cv2.morphologyEx(imBin2,cv2.MORPH_CLOSE,kernalOp)

            
            mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernalCl)
            mask2=cv2.morphologyEx(mask2,cv2.MORPH_CLOSE,kernalCl)


            
            _, countours0,hierarchy=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            for cnt in countours0:
                area=cv2.contourArea(cnt)
                
                if area>areaTH:
                    m=cv2.moments(cnt)
                    cx=int(m['m10']/m['m00'])
                    cy=int(m['m01']/m['m00'])
                    x,y,w,h=cv2.boundingRect(cnt)

                    new=True
                    if cy in range(up_limit,down_limit):
                        for i in cars:
                            if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                                new = False
                                i.updateCoords(cx, cy)

                            
                                if i.going_DOWN(line_down,line_up)==True:
                                    cnt_down+=1
                                
                                break
                            if i.getState()=='1':
                                if i.getDir()=='down'and i.getY()>down_limit:
                                    i.setDone()
                                
                            if i.timedOut():
                                index=cars.index(i)
                                cars.pop(index)
                                del i

                        if new==True:
                            p=vehicles.Car(pid,cx,cy,max_p_age)
                            cars.append(p)
                            pid+=1

                    
                    img=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)




            
            str_down='DOWN: '+str(cnt_down)
            
            
            
            cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        
            cv2.imshow('Frame',frame)

            if cv2.waitKey(1)&0xff==ord('q'):
                break

        else:
            if xz == "/home/pi/traffic python/sur1.mp4":
                result = firebase.put('/','cars1',0)
                result = firebase.put('/','cars1',cnt_down)
                result = firebase.post('/database1',{'road1':cnt_down})
            elif xz == "/home/pi/traffic python/sur2.mp4":
                result = firebase.put('/','cars2',0)
                result = firebase.put('/','cars2',cnt_down)
                result = firebase.post('/database2',{'road2':cnt_down})
            elif xz == "/home/pi/traffic python/sur3.mp4":
                result = firebase.put('/','cars3',0)
                result = firebase.put('/','cars3',cnt_down)
                result = firebase.post('/database3',{'road3':cnt_down})
            elif xz == "/home/pi/traffic python/sur4.mp4" :
                result = firebase.put('/','cars4',0)
                result = firebase.put('/','cars4',cnt_down)
                result = firebase.post('/database4',{'road4':cnt_down})
             
            break

    cap.release()
    cv2.destroyAllWindows()
    print(cnt_down)

        
      
        
    





