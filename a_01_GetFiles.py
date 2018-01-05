import os
import numpy as np
import pandas as pd

def change_time(files):
    times = []
    for i in range(len(files.time_str.index)):
        string = sum([float(n)*f for n,f in zip(files.time_str[i].split('-'),[3600,60,1])])
        if i == 0:
            t = 0
            times.append(t)
            i_1 = sum([float(n)*f for n,f in zip(files.time_str[i].split('-'),[3600,60,1])])
        else:
            t = string-i_1
            times.append(t)
            i_1 = string
    return times
            
class Files():
    
    def __init__(self, path):
        self.path = path
        self.files = sorted([[i, i.replace('.JPG','')] for i in os.listdir(path) if '.JPG' in i])
        self.files = pd.DataFrame(self.files, columns=('files','time_str'))
#        self.files['time_gap'] = change_time(self.files) 
#        self.files['time_st'] = self.files.time_gap.cumsum()
        
  
if __name__=='__main__':
    path = r'Z:\2_Projekt__Permeabilitätsbeeinflussung\AP 6 - 25%\03_Kapillardruck_25%\03_Data_void_content\data\basic_structure'
    c = Files(path)
    
    files = c.files
#    t = change_time(files)

