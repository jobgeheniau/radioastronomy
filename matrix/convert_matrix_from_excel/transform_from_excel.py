from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np
from astropy.coordinates import FK5
import os
import sys
import datetime
from time import sleep
import socket


# Reading an excel file using Python 
import xlrd 
  
# Give the location of the file 
loc = ("coordinaten.xls")    # COORDINATEN EXCEL SHEET NAME!!!!!!
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0)



os.system('cls' if os.name == 'nt' else 'clear')

raw_input("Press Enter to continue and delete the old ra_dec.txt, ELSE press Control Z")

f = open("ra_dec.txt", "a")
sleep(1)
os.remove("ra_dec.txt")

print('\n**********************************************************************************************')
sleep(0.3)
print('CCCCCCC  V       V ')
print('C         V     V ')
print('C          V   V ')
print('C           V V    ')
print('CCCCCCC      V ')
print('')
print('CONVERT: convert Galactic Longitude Latitude to RA DEC (in xxhxxm0s)')
print('')
print('by Job Geheniau')
print('')
print('')
print('Version 1.0 june 2020')
sleep(0.3)
print('**********************************************************************************************\n')
sleep(1)
print('[*] Please enter your desired parameters...\n')
sleep(0.5)

#Input parameters

yea = str(input('Enter Epoch Year for coordinates : '))
year= str('J'+yea)

     
for y in range(0,45): # Nr of ROWS IS LONGITUDE
    for z in range(0,21): # Nr of COLUMNS IS LATITUDE
        

        long = int(sheet.cell_value(y, 21))
        lat = int(sheet.cell_value(y, z))
            
        print long
        print lat
           

        # INPUT LONGITUDE LATITUDE IN DEGREES

        c = SkyCoord(l=long*u.degree, b=lat*u.degree, frame='galactic')

        #print c.fk5
        #print c.transform_to(FK5(equinox='J2020'))

        try:
            ra_degree = float((str(c.transform_to(FK5(equinox=year)))[58:68])) # RA IN DEGREES FROM STRING
            dec_degree_to_hms = float((str(c.transform_to(FK5(equinox=year)))[71:78])) # DEC IN DEGREES FROM STRING
        except ValueError:
            print('!!!!!!!!!!!!!!! ALARM ERROR ERROR  ERROR ALARM !!!!!!!!!!!')

        # CONVERT RA DEGREES TO HOUR
        d = SkyCoord(ra=ra_degree*u.degree, dec=0*u.degree) #DEC is NOT important here only ra.

        #print d.ra.hms

        convert_ra_to_string = str(d.ra.hour)
        convert_ra_to_H = convert_ra_to_string.replace(".", "H")

        convert_dec_to_string = str(dec_degree_to_hms)
        convert_dec_to_H = convert_dec_to_string.replace(".", "H")
 


        # CONVERT EVERYTHING TO xxhxxm0s

        rafinal2=convert_ra_to_H[convert_ra_to_H.find("H")+1:].split()[0]
    
        rafinal1=int(rafinal2[0:2])
    
        rafinal3=(rafinal1*60)/100
        rafinal=str(rafinal3)
        #print convert_ra_to_H.split('H')[0]+'d'+rafinal[0:2]+'m0s'

        decfinal2=convert_dec_to_H[convert_dec_to_H.find("H")+1:].split()[0]
   
        decfinal1=int(decfinal2[0:2]) 
        decfinal3=(decfinal1*60)/100
        decfinal=str(decfinal3)
        #print convert_dec_to_H.split('H')[0]+'d'+decfinal[0:2]+'m0s'


        f = open("ra_dec.txt", "a")
        f.write((convert_ra_to_H.split('H')[0]+'h'+rafinal[0:2]+'m0s')+','+convert_dec_to_H.split('H')[0]+'d'+decfinal[0:2]+'m0s'+'\n')
        f.close()

    print('**** Done ****')


