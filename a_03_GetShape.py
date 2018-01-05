import numpy as np
import cv2
import os
import sys
import matplotlib.pyplot as plt
from scipy import misc

def get_first(event,x,y,flags,param):
    global drawing, xi,yi, img, img2, xe,ye
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        xi,yi = x,y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img2 = img.copy()
            cv2.rectangle(img2,(xi,yi),(x,y),(0,255,0), 2)
            cv2.imshow('img', img2)
        
    elif event == cv2.EVENT_LBUTTONUP:      
        drawing = False
        xe,ye = x,y
        cv2.rectangle(img,(xi,yi),(x,y),(0,255,0), 2)

def detect_shape(name, path):
    global drawing, xi,yi, img, img2, xe,ye
    cwd = os.getcwd()
    os.chdir(path)
   
    img = cv2.imread(name,1)[:,:]
    img2 = img
    drawing = False
    xi,yi = -1,-1
    xe,ye = 0,0

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('img', get_first)
    
    while True:
        cv2.imshow('img', img2)
        k = cv2.waitKey(100)
        if k == 112:
            print(xi,yi,xe,ye)
            img = img[yi:ye,xi:xe]   
            img2 = img
        if k == 110:
            img = cv2.imread(name,1)[:,:]
            img2 = img
        if k == 27:
            break
    

    cv2.destroyAllWindows()
    os.chdir(cwd)
    return [yi,ye,xi,xe]
    
    
if __name__=='__main__':

    name = '10-59-24.726606.png'
    s = detect_shape(name)
