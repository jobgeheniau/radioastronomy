

# Fill Excel column with all the max values


import sys
import os
import datetime
from time import sleep

os.system('cls' if os.name == 'nt' else 'clear')

print('\n**********************************************************************************************')
sleep(0.3)
print('TTTTTTT  OOOOOOO  TTTTTTT  AAAAAAA  L')
print('   T     O     O     T     A     A  L')
print('   T     O     O     T     AAAAAAA  L')
print('   T     O     O     T     A     A  L')
print('   T     OOOOOOO     T     A     A  LLLLLLL')
print('')
print('Find total of all values in nrad.tct files and place them in Excel .csv file')
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


for i in range (0,(tocycle)) :
    with open('nrad-'+str(i)+'.tct', 'r') as inp, open('total'+str(i)+'.txt', 'w') as outp:
        for line in inp:
            try:
                num = float(line)
                total += num
                outp.write(line)
            except ValueError:
                print('{} is not a number!'.format(line))

    print('Total of all numbers nrad  '+str(i)+' {}'.format(total))
    f = open('total'+str(i)+'.txt', 'w')
    f.write('{}'.format(total))
    f.close()
        
    total = 0

import numpy as np
with open('nradtotal.csv', 'w') as f:
    for i in range (0,tocycle) :    
        a = np.loadtxt("total"+str(i)+".txt")
        print i
   
        tem=str(a)
        temp=tem.replace('[', ' ')
        temp=temp.replace(']', ' ')
        f.write(temp+'\r\n')#CR, LF
f.close()
print"done"
