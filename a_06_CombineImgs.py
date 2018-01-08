import numpy as np
import pandas as pd
import cv2
from a_01_GetFiles import Files
import os


class MakeVideo(Files):
    
    def __init__(self, path):
        super().__init__(path)
        self.current_dir = os.getcwd()
        os.chdir(self.path)

    def createVideo(self):

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        history = 3  #I've also tried 2,5,20,200
        varThreshold = 10
        bShadowDetection = False
        fgbg = cv2.createBackgroundSubtractorMOG2(history, varThreshold, bShadowDetection) #history, varThreshold, bShadowDetection
        fgbg.setHistory(history)

        learningRate = 0.01
        
        for i in self.files.files:
            frame = cv2.imread(i)
            frame = cv2.resize(frame, (800,600))
#            frame = cv2.GaussianBlur(frame, (5,5), 0)
#            frame = cv2.bilateralFilter(frame,9,75,75)
            fgmask = fgbg.apply(frame)
        
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
            cv2.imshow('frame',fgmask)
        
            h, w = fgmask.shape[:2]
            self.img = fgmask.copy()
            _,contours0, hierarchy = cv2.findContours( self.img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]
        
            vis = np.zeros((h, w, 3), np.uint8)
            levels = 17
            cv2.drawContours( vis, contours, (-1, 3)[levels <= 0],(128,255,255),-1, cv2.CV_FEATURE_PARAMS_HAAR, hierarchy, abs(levels) )
            cv2.imshow('contours', frame)
        
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        os.chdir(self.current_dir)

        cv2.destroyAllWindows()

if __name__=='__main__':
    
    kv = MakeVideo(r'2017-05-05_03')
    print(kv.files.head())
    kv.createVideo()
    print(kv.current_dir)
    aa = kv.img
