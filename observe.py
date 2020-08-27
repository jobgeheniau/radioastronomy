import os
import sys
import datetime
from time import sleep
import socket
import shutil
import time

os.system('cls' if os.name == 'nt' else 'clear')

shutil.copyfile('ra_dec.txt', 'ra_dec_original.txt')

print('\n**********************************************************************************************')
sleep(0.3)
print('V       V   I  RRRRRRR  GGGGGGG   OOOOOOO')
print(' V     V    I  R     R  G         O     O')
print('  V   V     I  RRRRRRR  G   GGG   O     O')
print('   V V      I  R  R     G     G   O     O')
print('    V       I  R    R   GGGGGGG   OOOOOOO')
print('')
print('VIRGO: An easy-to-use spectrometer & radiometer for Radio Astronomy based on GNU Radio')
print('')
print('main developer Apostolos Spanakis-Misirlis, side developer Job Geheniau')
print('')
print('Make sure you have a ra_dec.txt (with a return after last coordinate) like 23h59m0s,180d59m0s')
print('Make sure all the files are placed in a folder on the Desktop called ROT')
print('Make sure there are no plot.png,freq,power,snr,snr_original,time,az and observation.dat files')
print('')
print('Version 6.0 august 2020 with timer counter')

print('**********************************************************************************************\n')

print('[*] Please enter your desired observation parameters...\n')
sleep(0.5)

#Input observation parameters
f_center = str(input('Center frequency [MHz]: '))
f_center = str(float(f_center)*10**6)
bandwidth = str(input('Bandwidth [MHz]: '))
bandwidth = str(float(bandwidth)*10**6)
channels = str(input('Number of channels [FFT size]: '))
t_int = str(input('Integration time per FFT sample [sec]: '))
nbins = str(int(float(t_int) * float(bandwidth)/float(channels)))
duration = str(input('Observing duration [sec]: '))

N = int(input("Median [10 recommended]: "))
rtlgain = int(input("Gain [20 recommended]: "))
dur = int(duration)

klok = open( 'klok.txt', 'w' )
klok.write(str(dur))
klok.close()

print('')

with open("ra_dec.txt") as file_in:
    ra = []
    dec = []
    for line in file_in:
        ra.append(line.split(',')[0])
        dec.append((line.split(',')[1])[:-2])
samples = int(len(ra))

obtime = (samples*dur)/60
print('Total observation time will be ' + str(obtime) + ' minutes')

#Calibration option
cal = str(raw_input('\nWould you like to produce a calibrated spectrum at the end of your observation (requires off_nchan.dat calibration reference file in directory)? [Y/N]: '))

yes = {'y', 'ye', 'yes'}
if cal.lower() in yes:
    cal = True
else:
    cal = False

if cal:
    sleep(0.5)    
else:
    track = str(input('Do you want to track (1) or driftscan (0) when chosen for non-calibration: '))  
delay = str(input('Start observation in... [sec]: '))

klok2 = open( 'klok2.txt', 'w' )
klok2.write(str(delay))
klok2.close()

print('')

print('\nObservation will begin automatically in '+delay+' seconds. Please do not press anything...\n')


#  CLOCK

dur = []
f=open('klok2.txt','r') 
for line in f:
    dur.append(int(line))
    number = float(line) 
f.close()

dur = int(number)

def stopwatch(seconds):
   start = time.time()
   time.clock()    
   elapsed = 0

   dur2=dur+2
   print ("\n")
   
   print "***********Countdown started to observation***********"    
   print "======================================================"
   
   while elapsed < seconds:
       elapsed = time.time() - (start-1)
       #print "%f, wait %02d" % (time.clock() , (dur2-elapsed)) 
       klok=int(dur2-elapsed)
       uur=(klok/3600)
       minuut=(klok/60)
    
       print "HOURS to go:" , uur , "MINUTES to go:" , minuut, "SECONDS to go:" , klok
           
       time.sleep(1)
       sys.stdout.write("\033[A") # Cursor up one line
       sys.stdout.write("\033[K") # Clear line 
        

stopwatch(dur)

#sleep(float(delay))

#Delete pre-existing observation.dat & plot.png files
try:
    for fname in os.listdir('C:/Users/HP/Desktop/ROT'):
        if fname.startswith("freq") or (".png" in fname) or fname.startswith("snr") or fname.startswith("observation"):
            try:
                os.remove(os.path.join('C:/Users/HP/Desktop/ROT/', fname))
            except OSError:
                pass
except OSError:
    pass

#Note current datetime
currentDT = datetime.datetime.now()
obsDT = currentDT.strftime('%Y-%m-%d %H:%M:%S')
print('\n[+] Starting observation at ' + obsDT + ' (local computer time)...')

#Execute top_block.py with parameters
for i in range(samples):
    ### CONVERT RA/DEC TO AZ/EL
    directions = []
    try:
        os.remove('az_el.txt')
    except OSError:
        pass

    sleep(1)
    
    os.system('C:/Python27/python.exe C:/Users/HP/Desktop/ROT/coord_converter.py')

    sleep(1)
    directions = []
    with open('az_el.txt', 'r') as filehandle:
        for line in filehandle:
            currentPlace = line[:-1]
            
            # add item to the list
            directions.append(currentPlace)
    print('Converted to Az,El:')
    print(directions)
    if ",-" in directions[0]:
        print('ERROR: Source is under the horizon! Press enter to exit...')
        x = input("")
        sys.exit(0)
    print('')
    
    ### POINT THE DISH TO SOURCE
    UDP_IP = "127.0.0.1"
    UDP_PORT = 12000

    #If chosen for multiple , use rotator
    if cal:
        MESSAGE = ("<PST><AZIMUTH>" + str(directions[0].split(',')[0]) + "</AZIMUTH></PST>")
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM) #UDP
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    
        sleep(1)
    
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM) #UDP
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    
        sleep(1)
    
        MESSAGE = ("<PST><ELEVATION>" + str(directions[0].split(',')[1]) + "</ELEVATION></PST>")
        sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM) #UDP
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    
        sleep(1)

        if cal:
            MESSAGE = "<PST><TRACK>1</TRACK></PST>"
            sock = socket.socket(socket.AF_INET,
                                 socket.SOCK_DGRAM) #UDP
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        else:
            # Track or Driftscan 1 or 0
            MESSAGE = ("<PST><TRACK>" + str(track) + "</TRACK></PST>")
            sock = socket.socket(socket.AF_INET,
                                 socket.SOCK_DGRAM) #UDP
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    #If chosen for dark frame and start later, dont use Rotator
    else:
        MESSAGE = ("<PST><TRACK>" + str(track) + "</TRACK></PST>")
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM) #UDP
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    ### WAIT 60 SEC TO GET THERE AND BEGIN OR WAIT FOR NEXT OBSERVATION

    print('...Please wait 60 seconds to slew the dish...')
    print('')
    sleep(60)
    sys.argv = ['top_block.py', '--c-freq='+f_center, '--samp-rate='+bandwidth, '--nchan='+channels, '--nbin='+nbins, '--obs-time='+duration]
    execfile('top_block.py')
    print('[!] Observation finished! Plotting data...')
    if cal:
        os.system('C:/Python27/python.exe C:/Users/HP/Desktop/ROT/plot_hi.py freq='+f_center+' samp_rate='+bandwidth+' nchan='+channels+' nbin='+nbins+' i='+str(i)+' N='+str(N))
        
   
        os.rename('C:/Users/HP/Desktop/ROT/plot.png', 'C:/Users/HP/Desktop/ROT/plot_' + str(i+1) + '.png')
        try:
            os.remove('observation.dat')
	except OSError:
   	    pass
    else:
        os.system('C:/Python27/python.exe C:/Users/HP/Desktop/ROT/plot_hi.py freq='+f_center+' samp_rate='+bandwidth+' nchan='+channels+' nbin='+nbins+' i='+str(i)+' N='+str(N))
       
        os.rename('C:/Users/HP/Desktop/ROT/plot.png', 'C:/Users/HP/Desktop/ROT/plot_' + str(i+1) + '.png')
    
        
   
    print('\n======================================================================================')
    print('[+] The observation data has been plotted and saved as plot' + str(i+1) + '.png')
    print('======================================================================================')

    # DELETE FIRST RADEC FROM LIST AND CONTINUE WITH NEXT
    a_file = open("ra_dec.txt", "r")
    lines = a_file.readlines()
    a_file.close()
    del lines[0]
    new_file = open("ra_dec.txt", "w+")
    for line in lines:
        new_file.write(line)
    new_file.close()
    print('line 1 from ra_dec.txt has been deleted for next observation')

### STOW DISH (PARK)

if True:
    print("\n[!] Stowing dish (parking)...")
    UDP_IP = "127.0.0.1"
    UDP_PORT = 12000
    
    MESSAGE = ("<PST><PARK>1</PARK></PST>")
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM) #UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sleep(5)
    MESSAGE = ("<PST><PARK>1</PARK></PST>")
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM) #UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sleep(1)
print("[+] Dish stowed successfully!")
os.remove("klok.txt")
os.remove("klok2.txt")

#Note current datetime
currentDT = datetime.datetime.now()
obsDT = currentDT.strftime('%Y-%m-%d %H:%M:%S')
print('\n[+] All the observations have been made ' + obsDT + ' (local computer time)...')
print('Press <ENTER> to finish...')
x = raw_input("")