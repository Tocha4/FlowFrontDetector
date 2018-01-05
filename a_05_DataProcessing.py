import pandas as pd
import numpy as np
import os 
import matplotlib.pyplot as plt
import scipy.optimize as opt
#%% Load data
path = r'Z:\2_Projekt__Permeabilitätsbeeinflussung\AP 6 - 25%\03_Kapillardruck_25%\03_Data_void_content\data\Textil_1_0_01'
name = [i for i in os.listdir(path) if '.csv' in i]
name = os.path.join(path,name[0])
data = pd.read_csv(name, index_col=0)

#%% Data munging
data = data.sort_values(by='ff_cm')
data = data[data.ff_cm <= 80]
data = data[data.ff_cm >= 0]
#print(data.head())

#%% Fitting
def lin_fit(x,y):
    def funktion(x,a,b):
        y = a*x**2+b*x
        return y
    parameters,R  = opt.curve_fit(funktion,x,y, maxfev=1500)
    x_new = np.linspace(np.min(x), np.max(x), 100)
    y_new = funktion(x_new, parameters[0],parameters[1])
    return x_new, y_new, parameters,R

new_time_st, new_ff_cm, parameters,R = lin_fit(data.time_st, data.ff_cm**2)

plt.plot(data.time_st, data.ff_cm**2, 'o')
plt.plot(new_time_st, new_ff_cm, '--')
plt.xlabel('Time [sec]')
plt.ylabel('Position [cm]')
s = r'f(x) = {:.1e}*x**2+{:.2f}*x'.format(parameters[0], parameters[1])
plt.text(100,75,s)

plt.grid(True)

for i in parameters:
    print(i)

