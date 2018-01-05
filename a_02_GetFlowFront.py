import numpy as np
import cv2
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from time import time
from concurrent import futures

sys.path.insert(0,r'Z:\2_Projekt__Permeabilitätsbeeinflussung\AP 6 - 25%\03_Kapillardruck_25%\03_Data_void_content\FlowFrontDetector')

import a_01_GetFiles
from a_03_GetShape import detect_shape
from a_04_DetectFlowFront import detect_one_FlowFront


Files = a_01_GetFiles.Files


class FlowFront(Files):
    
    def __init__(self, path, muP=None):
        super().__init__(path)
        os.chdir(self.path)
        if muP == None:
            self.shape = detect_shape(self.files.files[0], self.path)
            self.muP = 15/(self.shape[-1]-self.shape[-2])
        else: self.muP = muP
        print(self.muP)
        
        
    def detect_FlowFronts(self, mitte):
        self.shape = detect_shape(self.files.files[0], self.path)
        ff_pixel = pd.DataFrame([], columns=('files','ff_pixel'))
        factor = 0
        xp = 0
        for i in self.files.files:
            if i == mitte:
                self.shape = detect_shape(mitte, self.path)
                print(xp)
                factor = xp
            xp = detect_one_FlowFront(i,self.shape)
            data = [[i,xp+factor]]
            ff_i = pd.DataFrame(data, columns=('files','ff_pixel'))

            ff_pixel = ff_pixel.append(ff_i, ignore_index=True)
        self.files = pd.merge(self.files, ff_pixel, on='files')
        self.files['ff_cm'] = self.files.ff_pixel*self.muP
        self.files.to_csv('{}.csv'.format(os.path.split(self.path)[1])) #!!!!!!!!!!!!!!!!!! saving in csv
#        print(ff_pixel.head())

               
        
if __name__=='__main__':
    path = r'Z:\2_Projekt__Permeabilitätsbeeinflussung\AP 6 - 25%\02_Permeabilität_25%\PermDetector_git\data\Textil_1_0_01'
    muP = 15/481
    ff = FlowFront(path, muP)
    mitte = r'10-57-06.628705.png'
    ff.detect_FlowFronts(mitte)
#    print(ff.files.tail())
    
    plt.plot(ff.files.time_st, ff.files.ff_cm, 'o')
    plt.xlabel('Time [sec]')
    plt.ylabel('Position [Pixel]')
    

    
