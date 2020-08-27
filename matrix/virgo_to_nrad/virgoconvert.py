import sys
import os
import datetime
from time import sleep

os.system('cls' if os.name == 'nt' else 'clear')

print('\n**********************************************************************************************')
sleep(0.3)
print('      J  RRRRRRR  TTTTTTT    PPPPPPP  L        OOOOOOO  TTTTTTT')
print('      J  R     R     T       P     P  L        O     O     T')
print('      J  RRRRRRR     T       PPPPPPP  L        O     O     T')
print('      J  R  R        T       P        L        O     O     T')
print('JJJJJJJ  R    R      T       P        LLLLLLL  OOOOOOO     T')
print('')
print('Jobs Radio Telescope Plot: Plot your data into colorfull images')
print('')
print('main developer Michiel Klaassen, side developer Job Geheniau & Raydel Abreu')
print('')
print('')
print('Version 1.0 june 2020')
sleep(0.3)
print('**********************************************************************************************\n')
sleep(1)
print('Make sure there are only the VIRGO .txt files in the folder. No .csv and no nrad files')
print('---> RENAME THE SnR file to snr1...snrx!!!')
print('[*] Please enter your desired observation parameters...\n')
sleep(0.5)

#Input observation parameters
observations = str(input('How many observations ?: '))

#Raydel Abreu CM2ESP 10/06/2020
#Use it for convert from VIRGO file format into CFRAD format
from numpy import loadtxt
import numpy as np

#FFT bins per scan line in source
fftBins = 2048

#File Input Configuration
firstFile = 1
lastFile = int(observations)
Increment = 1

#How many lines to average (use 1 for none)
vertInt=1

#List that contains data
lines = list()

#Read files
for f in range(firstFile,lastFile,Increment):
    sourceFile = 'snr'+str(f)+".txt"
    #Read File into list of scans
    lines.append(loadtxt(sourceFile, comments="#", delimiter="\n\n\r", unpack=False))

#Number of scan in the file
numScan = len(lines)

#Empty list for averaged scans
outScans = list()

#Range formatting. Required to keep values inside the accepted CFRAD levels
minVal=np.min(lines)
if minVal < 0:
   minVal=minVal*(-1.0)
lines+=(minVal+.01)
maxVal=np.max(lines)
#Define top level
topLevel=2.0
multiplier=topLevel/maxVal
lines*=multiplier

print np.min(lines)
print np.max(lines)

#Average scans if needed. Otherwise just save as it is
for i in range(-1,numScan,(vertInt)):
    if i+vertInt <= numScan:
       scanAvg = np.zeros((fftBins))
       avgFrom = i
       avgTo = i+vertInt
       for sets in range(avgFrom,avgTo):
           scanAvg=scanAvg+lines[sets]
       scanAvg=scanAvg/(vertInt)
       removeBias = [x+(minVal) for x in scanAvg]
       outScans.append(removeBias)

#now Save to file
print len(outScans)-1
for j in range(len(outScans)):
    f = open('nrad-'+str(j)+'.txt', 'w')
    for k in range(len(outScans[j])):
        f.write(str(outScans[j][k])+'\r\n')
    f.close()

#ready
print"done"


# -*- coding: utf-8 -*-
"""
CFRAD-plot2 
Created on 21 juni 2014.
author: Michiel Klaassen; www.parac.eu
It is not allowed to sell this script.
"""

# Instructions
# Copy this script to a directory wher ethe nrad files are written by cfrad2.exe
# Start python-xy; and start spyder editor.
# select file , open and then this script
# For the reference curve choose the nrad file and time with the weakest H1 signal
# if unknown; just start with fromset=0 and toset=0 in line 40/41
# In line 100 you can enter a line of interest; if unknown enter 0
# In line 169-170 you can enter all the written nrad lines; fromset --toset
# run the script by selecting 'run' and 'run'
# The first graph is diplayed and try out the icons
# to continue the script select X in the top right corner
# 

import numpy as np
import matplotlib.pyplot as mpl
#--------settings---------------------------------------------------
filename="nrad-" 
ndp=2048; #number of data points; do not change!
sr=2000.0 # sampling rate [kB/s] you also have used in Sharp#
f=(sr*np.linspace(0,1,ndp))/1000 # make a lineair frequency scale [MHz]
Sf=sr/1000/2  # half of the scale


#---------------------calculate the band pss correction-------------------------
# select a number of sets, where almost no hydrogen has been measured.
# If you dont know start with line 0,
# run the script; 
#if you get negative bumps select those lines for bandpass corr. etc
 
fromset=0#0 # from set
toset=0#10 # to set; to get a smooth curve
bpass=np.zeros((2048)) ; # starting values 
bpcorr=np.zeros((2048)) ;
for sets in range (fromset,toset+1): #
    print sets    
    datat = np.loadtxt(filename+str(sets)+".txt") 

    rbp=datat*1.00001
    data=rbp+0.000001
    for i in range (2,2046):
        if data[i] > 1.051*data[i-1]:# limit dependent on previous value
            data[i] = data[i-1] #    
    rbp1=data*1.000003        
    data=rbp1+0.0000001

# average over xx bins
    for i in range (2,2046):
        data[i] = (data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2])/5 #    
    for i in range (2,2046):
        data[i] = (data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2])/5 #   
    for i in range (2,2046):
        data[i] = (data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2])/5 #
    for i in range (2,2046):
        data[i] = (data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2])/5 #   
    for i in range (2,2046):
        data[i] = (data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2])/5 #
    for i in range (2,2046):
        data[i] = (data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2])/5 #   
    for i in range (2,2046):
        data[i] = (data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2])/5 #
    for i in range (4,2044):
        data[i] = (data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4])/9 #  
    for i in range (4,2044):
        data[i] = (data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4])/9 #  
    for i in range (4,2044):
        data[i] = (data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4])/9 #  

    bpass=bpass+data # sommeer
bpass=bpass/( toset+1-fromset)# average
bpcorr=1/(bpass) # the band pass correction curve

rbp2=data

fig=mpl.figure(1)
ax = fig.add_subplot(111)
ax.plot(f-Sf,rbp1,linewidth=1,label='$raw bp$')
ax.plot(f-Sf,rbp2,linewidth=1,label='$no peak$')
#ax.plot(f-Sf,bpass,linewidth=2,label='$Band pass$')
ax.plot(f-Sf,bpcorr,label='$bpcorr.$')
ax.legend(loc=0)
ax.set_xlim( -Sf, Sf)
#ax.set_ylim( 0,20) 
ax.set_title('Band Pass & Correction factor')
ax.set_xlabel('Frequency +1420.4 [MHz]')
ax.set_ylabel('unity')
#mpl.show()


#------------------------selected set-----------------
# select a line to check the correction measures
setsa=int(observations)# select een line
sets=setsa-1  
raw1=np.zeros((2048));
raw2=np.zeros((2048));
raw3=np.zeros((2048));
ata=np.zeros((2048));
dat=np.zeros((2048));
dataset = np.loadtxt(filename+str(sets)+".txt") 

ata=dataset*bpcorr #correct for bandpass 


for i in range (2,2046):
    if ata[i] > 1.5: # 1.3 limiteer absolute waarde
        ata[i] = ata[i-1] #
# limit spikes dependent on average value
gem=np.mean(ata,0)
for i in range (2,2046):
        if ata[i] > 1.5*gem:#1.02:#
            ata[i] = 1.5*gem #
#limit spikes dependent on previous value
for i in range (2,2046):
        if ata[i] > 1.1*ata[i-1]:#
            ata[i] = ata[i-1] #
dat=ata#*1.001
raw2=dat*1.00002  


data=dat*1.00001#
#average over xx bins
for i in range (8,2040):
    data[i] = (data[i-8]+data[i-7]+data[i-6]+data[i-5]+data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4]+data[i+5]+data[i+6]+data[i+7]+data[i+8])/17 #  
for i in range (8,2040):
    data[i] = (data[i-8]+data[i-7]+data[i-6]+data[i-5]+data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4]+data[i+5]+data[i+6]+data[i+7]+data[i+8])/17 #  
for i in range (8,2040):
    data[i] = (data[i-8]+data[i-7]+data[i-6]+data[i-5]+data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4]+data[i+5]+data[i+6]+data[i+7]+data[i+8])/17 #  
for i in range (8,2040):
    data[i] = (data[i-8]+data[i-7]+data[i-6]+data[i-5]+data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4]+data[i+5]+data[i+6]+data[i+7]+data[i+8])/17 #  
for i in range (8,2040):
    data[i] = (data[i-8]+data[i-7]+data[i-6]+data[i-5]+data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4]+data[i+5]+data[i+6]+data[i+7]+data[i+8])/17 #  
for i in range (8,2040):
    data[i] = (data[i-8]+data[i-7]+data[i-6]+data[i-5]+data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4]+data[i+5]+data[i+6]+data[i+7]+data[i+8])/17 #  
for i in range (8,2040):
    data[i] = (data[i-8]+data[i-7]+data[i-6]+data[i-5]+data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4]+data[i+5]+data[i+6]+data[i+7]+data[i+8])/17 #  
raw4=data*1.00001        

        
fig=mpl.figure(sets)
ax = fig.add_subplot(111)
#ax.plot(f-Sf,raw1, linewidth=1,label='$raw1$')
ax.plot(f-Sf,raw2, linewidth=1,label='$raw2$')
ax.plot(f-Sf,(raw4), linewidth=1,label='$clean$')
ax.plot(f-Sf,(raw4)+0.1, linewidth=1,label='$clean$')
ax.legend(loc=0)
ax.set_xlim( -Sf, Sf)
#ax.set_ylim( 1.0,1.3)# if not enabled, then auto scale 
ax.set_title('Selected line')
ax.set_xlabel('Frequency +1420.4 [MHz]') #
ax.set_ylabel('Intensity')
#mpl.show()


#--------------series-------------------------------------------------------------
fromset=0 # from set x 
toset=int(observations)-1 # to set y #BELANGRIJKE EINDWAARDE!!!!!!
offcor=np.zeros((toset+1,1));
rawsets=np.zeros((toset+1,2048));
offsets=np.zeros((toset+1,1)) ;
outsets=np.zeros((toset+1,2048)) ; 
sutosetets=np.zeros((toset+1,2048)) ; 

for sets in range (fromset,toset+1): #toset+1):
    print sets    
    data = np.loadtxt(filename+str(sets)+".txt") 
    data=data*bpcorr 
    
    for i in range (2,2046):
        if data[i] > 1.5: # 1.3 limit absolute
            data[i] = data[i-1] #

    gem=np.mean(data,0)
    for i in range (2,2046):
        if data[i] > 1.3*gem:# 1.02 limit dependent on average
            data[i] = 1.3*gem #

    for i in range (2,2046):
        if data[i] > 1.1*data[i-1]: # limit depending on previous value
            data[i] = data[i-1] #   

    for i in range (2,2046):
        data[i] = (data[i-1]+data[i]+data[i+1])/3 #
    for i in range (2,2046):
        data[i] = (data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2])/5 #      
    for i in range (2,2046):
        data[i] = (data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2])/5 #

    for i in range (8,2040):
        data[i] = (data[i-8]+data[i-7]+data[i-6]+data[i-5]+data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4]+data[i+5]+data[i+6]+data[i+7]+data[i+8])/17 #  
    for i in range (8,2040):
        data[i] = (data[i-8]+data[i-7]+data[i-6]+data[i-5]+data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4]+data[i+5]+data[i+6]+data[i+7]+data[i+8])/17 #  
    for i in range (8,2040):
        data[i] = (data[i-8]+data[i-7]+data[i-6]+data[i-5]+data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4]+data[i+5]+data[i+6]+data[i+7]+data[i+8])/17 #  
    for i in range (8,2040):
        data[i] = (data[i-8]+data[i-7]+data[i-6]+data[i-5]+data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4]+data[i+5]+data[i+6]+data[i+7]+data[i+8])/17 #  
    for i in range (8,2040):
        data[i] = (data[i-8]+data[i-7]+data[i-6]+data[i-5]+data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4]+data[i+5]+data[i+6]+data[i+7]+data[i+8])/17 #  
    for i in range (8,2040):
        data[i] = (data[i-8]+data[i-7]+data[i-6]+data[i-5]+data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4]+data[i+5]+data[i+6]+data[i+7]+data[i+8])/17 #  
    for i in range (8,2040):
        data[i] = (data[i-8]+data[i-7]+data[i-6]+data[i-5]+data[i-4]+data[i-3]+data[i-2]+data[i-1]+data[i]+data[i+1]+data[i+2]+data[i+3]+data[i+4]+data[i+5]+data[i+6]+data[i+7]+data[i+8])/17 #  

    offsetcor=1-((data[50]+data[60]+data[1990]+data[2000])/4)#line space normalizing
    data=data+offsetcor
    np.savetxt(filename+str(sets)+".tct",data)#csv preparation. to disable; place # at start of line

    outsets[sets] = (data)
  
    offsets[sets]=(sets*0.0105)#+0.05 #4

#---------------------plot series----
fig=mpl.figure(2)
ax = fig.add_subplot(111)
#ax.plot(f-Sf,(raw1),linewidth=1) # unmark to see spikes
for i in range (fromset,toset+1):
    ax.plot(f-Sf,(outsets[i]+offsets[i]+0.1))
    if i==64:
        ax.plot(f-Sf,((outsets[i])+offsets[i]+0.1),linewidth=2)
    if i==250:
        ax.plot(f-Sf,((outsets[i])+offsets[i]+0.1),linewidth=2)


ax.set_xlim( -Sf, Sf)
#ax.set_ylim(0.8,4.2)  
ax.set_title('Hydrogen in the Milky Way')
ax.set_xlabel('Frequency +1420.4 [MHz]')
ax.set_ylabel('Intensity')
os.system('cls' if os.name == 'nt' else 'clear')

print('\nIf you want save the Plot and close all open Plots now!.......')
mpl.show()






# -*- coding: utf-8 -*-
"""
@author: michiel klaassen parac.eu 02-feb-2020
"""
import numpy as np

fbin=0#0#
tbin=2048#2048#
bins=tbin-fbin

frcycle=0#
tocycle=int(observations)-1#8# BELANGRIJKE EINDWAARDE

a=np.zeros((bins+1,1));
x=np.zeros(((tocycle+1)*(bins+1),1));
y=np.zeros(((tocycle+1)*(bins+1),1));
z=np.zeros(((tocycle+1)*(bins+1),1));

with open('nrad.csv', 'w') as f:
    for i in range (frcycle,tocycle+1) :    
        a = np.loadtxt("nrad-"+str(i)+".tct")
        print i,tocycle
        for k in range (fbin,tbin): #
            z[i*bins+k]=a[k]
            x[i*bins+k]=k
            y[i*bins+k]=i
            tem=str(x[i*bins+k])+','+str(y[i*bins+k])+','+str(z[i*bins+k])
            temp=tem.replace('[', ' ')
            temp=temp.replace(']', ' ')
            f.write(temp+'\r\n')#CR, LF
f.close()
print"done"


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
Plt.title('Hydrogen Job Geheniau')
Plt.ylabel('scan lines')
Plt.xlabel('+1420.41 MHz')

print"The final Hydrogen Plot is ready............"
print"Type Control Z......bye......"
Plt.show()







