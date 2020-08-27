# -*- coding: utf-8 -*-
"""
@author: michiel klaassen parac.eu 03-feb-2020
"""
import numpy as np
from matplotlib.mlab import griddata
import matplotlib.pyplot as Plt
#import scipy.interpolate

longarray = np.loadtxt('nrad.csv',delimiter=',')
npoints=2048#2048 #fixed number of samples 

Fs=2.0000# sampling frequency [MHz]

x = (longarray[:,0])/npoints*Fs-Fs/2.0
y = longarray[:,1]
z =(np.log( longarray[:,2])) #logarithmic z scale
#z =(longarray[:,2])#linear z scale

max_x = max(x)
min_x = min(x)
max_y = max(y)
min_y = min(y)

print min_x
print max_x
print min_y
print max_y

xi = np.linspace(min_x, max_x,num=1000)
yi = np.linspace(min_y, max_y,num=1000)
zi = griddata(x, y, (z), xi, yi,interp='linear')#
#zi = scipy.interpolate.griddata(x, y, (z), xi, yi,interp='linear')#


Plt.contour(xi, yi, zi, 20, linewidths=0.2, colors='k')#25=number of contour lines
Plt.contourf(xi, yi, zi, 255, cmap=Plt.cm.jet)#100= number of colors
Plt.colorbar()#color scale
Plt.title('Hydrogen Job Geheniau test')
Plt.ylabel('scan lines')
Plt.xlabel('+1420.41 MHz')

print"done"
Plt.show()
exit()
