




import sys
import os
import datetime
from time import sleep
import xlsxwriter 

os.system('cls' if os.name == 'nt' else 'clear')

print('This script will compute the Hydrogen max from Milky Way Arm1,2 or 3')
print('You will need a frequency file and a SnR file (freq.txt and snr1..snrX.txt with the observation data')
print('')


print('[*] Please enter your desired observation parameters...\n')
sleep(0.5)

#Input observation parameters
observations = str(input('How many observations ?: '))
peakinput = str(input('Milky Way Arm [1,2,3] ?: ')) 
peak = int(peakinput)

total = 0

# number of observations

frcycle = 1#
tocycle = int(observations)#8# total number of observations

#workbook = xlsxwriter.Workbook('HydrogenPeak.csv') 
#worksheet = workbook.add_worksheet()

if peak == 1:
    workbook = xlsxwriter.Workbook('HydrogenPeakARM1.csv') 
    worksheet = workbook.add_worksheet()
    with open('HydrogenPeakARM1.csv', 'w') as f:

        for i in range (1,(tocycle+1)) :
    
            max_num = -100
            line_count = 0
        
            with open('snr'+str(i)+'.txt', 'r') as infile:
                k = 1
                for line in infile:
    
                    if k>= 1021 and k<= 1191:
                        number = float(line.split(',')[0])
                        #print(line_count)
                        #print number

                        if number > max_num:
                            max_num = number
                            line_num = line_count
                        line_count += 1
  
                    k = k+1 
                line_num = line_num + 1019
                with open('freq.txt', 'r') as f:
                    lines = f.readlines()
                    frequency = float(lines[line_num+1].strip())
                  
                with open('HydrogenPeakARM1.csv', 'w') as fg:
                    worksheet.write(i, 0, frequency) 
                    print('--- PEAK FOUND ---' , max_num, ' at Frequency ', frequency)    
                fg.close()
           
               
    workbook.close() 
  
               
    f.close()

if peak == 2:
    workbook = xlsxwriter.Workbook('HydrogenPeakARM2.csv') 
    worksheet = workbook.add_worksheet()
    with open('HydrogenPeakARM2.csv', 'w') as f:

        for i in range (1,(tocycle+1)) :
    
            max_num = -100
            line_count = 0
        
            with open('snr'+str(i)+'.txt', 'r') as infile:
                k = 1
                for line in infile:
    
                    if k>= 1234 and k<= 1362:
                        number = float(line.split(',')[0])
                        #print(line_count)
                        #print number

                        if number > max_num:
                            max_num = number
                            line_num = line_count
                        line_count += 1
  
                    k = k+1 
                line_num = line_num + 1232
                with open('freq.txt', 'r') as f:
                    lines = f.readlines()
                    frequency = float(lines[line_num+1].strip())
                  
                with open('HydrogenPeakARM2.csv', 'w') as fg:
                    worksheet.write(i, 0, frequency) 
                    print('--- PEAK FOUND ---' , max_num, ' at Frequency ', frequency)    
                fg.close()
           
               
    workbook.close() 
  
               
    f.close()

if peak == 3:
    workbook = xlsxwriter.Workbook('HydrogenPeakARM3.csv') 
    worksheet = workbook.add_worksheet()
    with open('HydrogenPeakARM3.csv', 'w') as f:

        for i in range (1,(tocycle+1)) :
    
            max_num = -100
            line_count = 0
        
            with open('snr'+str(i)+'.txt', 'r') as infile:
                k = 1
                for line in infile:
    
                    if k>= 1362 and k<= 1533:
                        number = float(line.split(',')[0])
                        #print(line_count)
                        #print number

                        if number > max_num:
                            max_num = number
                            line_num = line_count
                        line_count += 1
  
                    k = k+1 
                line_num = line_num + 1360
                with open('freq.txt', 'r') as f:
                    lines = f.readlines()
                    frequency = float(lines[line_num+1].strip())
                  
                with open('HydrogenPeakARM3.csv', 'w') as fg:
                    worksheet.write(i, 0, frequency) 
                    print('--- PEAK FOUND ---' , max_num, ' at Frequency ', frequency)    
                fg.close()
           
               
    workbook.close() 
  
               
    f.close()

print"done"
