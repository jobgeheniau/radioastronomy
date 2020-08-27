

# Fill Excel column with all the max values


import sys
import os
import datetime
from time import sleep

os.system('cls' if os.name == 'nt' else 'clear')

print('\n**********************************************************************************************')
sleep(0.3)
print('MMMMMMM  AAAAAAA  X     X')
print('M  M  M  A     A   X   X ')
print('M  M  M  AAAAAAA    X X ')
print('M     M  A     A   X   X ')
print('M     M  A     A  X     x')
print('')
print('Find highest values in snr.txt files and place them in Excel .csv file')
print('')
print('developer Job Geheniau')
print('')
print('')
print('Version 1.0 june 2020')
sleep(0.3)
print('**********************************************************************************************\n')


print('[*] Please enter your desired observation parameters...\n')
sleep(0.5)

#Input observation parameters
observations = str(input('How many observations ?: '))

total = 0

# number of observations

frcycle = 1#
tocycle = int(observations)#8# BELANGRIJKE WAARDE


for i in range (1,(tocycle+1)) :
    with open('snr'+str(i)+'.txt', 'r') as inp, open('max'+str(i)+'.txt', 'w') as outp:
      
       lines = inp.readlines()
       maximum = max(lines)
            

    print('Maximum of snr  '+str(i)+' {}'.format(maximum))
    f = open('max'+str(i)+'.txt', 'w')
    f.write('{}'.format(maximum))
    f.close()
        
    total = 0

import numpy as np
with open('nradmax.csv', 'w') as f:
    for i in range (1,tocycle+1) :    
        a = np.loadtxt("max"+str(i)+".txt")
        print i
   
        tem=str(a)
        temp=tem.replace('[', ' ')
        temp=temp.replace(']', ' ')
        f.write(temp+'\r\n')#CR, LF
f.close()
print"done"
