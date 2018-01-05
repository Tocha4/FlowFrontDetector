import numpy as np
import cv2
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd


#%% Functions
def dmean(num,mean):
    for i in range(100):
        if mean in num:
            break
        else: 
            mean += 1
    return mean


#%% Image Processing
def detect_one_FlowFront(name, shape):
    a,b,c,d = shape
    img1 = cv2.imread(name)[a:b,c:d]#[360:491,6:1304]#
    
    img = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    img = cv2.blur(img, (5,5))
    rat,ath = cv2.threshold(img,180,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    contours = cv2.findContours(ath, 1, 1)
    for n,cnt in enumerate(contours[1]):
        if len(cnt) > 50:
            epsilon = 0.001*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,epsilon, True)
            cv2.drawContours(img, [approx], 0, 0, -2)
    
    edges = cv2.Canny(img,50,150,apertureSize = 3)  
    
    contours = cv2.findContours(edges, 1, 2)
    g = np.array([], dtype=np.int32)
    for n,cnt in enumerate(contours[1]):
        if len(cnt) > 50:
            g = np.append(g,cnt[:,0,0])
            epsilon = 0.005*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,epsilon, True)
            cv2.drawContours(img1, [approx], 0, (0,0,255), -2)
    #        plt.plot(cnt[:,0,0],cnt[:,0,1])
    num = np.bincount(g)
    xp = num > np.max(num)*0.25
    mean = int(np.mean(num[xp]))
    
    mean = dmean(num,mean)
    xp = np.where(num==mean)[0][0]
    #%%
    
#    x = int(g.mean())
    ys = 0
    ye = img1.shape[0]
    

    
    #cv2.line(img1, (x,ys),(x,ye),(255,0,0),2)
    cv2.line(img1, (xp,ys), (xp,ye), (255,0,255),2)
    cv2.imshow('2',img1)
    
    cv2.waitKey(1)
    return(xp)

if __name__=='__main__':
    name = 'testamony.png'
    detect_one_FlowFront(name,[360,491,6,1304])
    cv2.destroyAllWindows()




















