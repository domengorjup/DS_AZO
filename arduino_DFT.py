from __future__ import print_function
import serial
import serial.tools.list_ports
import time, sys
from time import gmtime, strftime, sleep
import numpy as np
from numpy import fft
#import matplotlib.pyplot as plt


n_samples = 100
serialSpeed = 115200

# -----------------------------------------------------------------------------

def startSample(speed):

    serialSpeed = speed

    x = np.array([], dtype=float)
    y = np.array([], dtype=float)
    z = np.array([], dtype=float)

    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "ttyACM" in p[1]:
            arduinoPort = p[0]

    ser = serial.Serial(arduinoPort, timeout=None, baudrate=serialSpeed)

    if ser.isOpen():
        ser.close()
    ser.open()

    print(ser.name, 'serial connection established at', serialSpeed, 'bps.\n')

    count = 0
    started = 0
    
    while True:
        try:
            if not started:
                started = 1
                print('Sampling started.\n')
                time_started = time.time()
            
            line = ser.readline().decode('utf-8').rstrip().split()
            count = count + 1

            if 'end' in line:
                 raise ValueError('Sampling ended.')

            if count == n_samples:
                
                raise ValueError('Sampling ended.')

            if len(line) == 3:
                x = np.append(x, float(line[0]))
                y = np.append(y, float(line[1]))
                z = np.append(z, float(line[2]))


        except (KeyboardInterrupt, ValueError):
            break

    time_stopped = time.time()
    t = time_stopped-time_started
    
    ser.close()
    
    return (x,y,z,t,count)


if __name__ == '__main__':

##    #Start playing sound and sampling simultaneously:
##    pool = mp.Pool(processes=2)
##    results = pool.apply_async(startSample, args=(serialSpeed,))
##    closecode = pool.apply_async(playTone, args=(outputFrequency, 20,))
##    
##    results = results.get()
##    
##    t = results[0]
##    x = results[1]
##    y = results[2]
##    z = results[3]

    n = 1;
    while n < 90:
        x,y,z,t,n = startSample(serialSpeed)

    print("Sampling ended.\n\nRESULT:\t%d samples (time: %.4f s)\n\nClosing serial." %(n, t))
    
    #print(n/t, ' Hz')
##    
##    # ------------------------------------
    # IZRAČUN POSPEŠKOV
    # ------------------------------------

    print("\nPostprocessing started.\n")
    
    zero = 350.5    # povprečna vrednsot za (ADXL335)
    g1 = 428.2      # povprečna vrednost z osi pri merovanju (ADXL335)
    # g = meritev - zero / (g1-zero)

    x = (x - zero) / (g1-zero) * 9.81
    y = (y - zero) / (g1-zero) * 9.81
    z = (z - zero) / (g1-zero) * 9.81

    # remove DC offet
    xn = x - np.mean(x)
    yn = y - np.mean(y)
    zn = z - np.mean(z)

    #print(xn, yn, zn)

    # ------------------------------------
    # DFT
    # ------------------------------------

    #calculate time step:
    n = len(x)
    timeStep = t/n

    zf = fft.fft(zn)/n
    xf = fft.fft(xn)/n
    yf = fft.fft(yn)/n
    freq = fft.fftfreq(n,d=timeStep)

    # ------------------------------------
    # ZAPIS 
    # ------------------------------------

    filename = strftime("%d_%H_%M_%S",gmtime())

    np.savetxt(filename+'.txt', (x,y,z,freq), newline='\n')

    print("Files saved.\n")

    print('freq: {}'.format(len(freq)))
    print('xyz: {}'.format(len(x)))
    
    izbor = freq >= 0

    graf, ax = plt.subplots(2,1)
    ax[0].hold(True)
    ax[0].plot(freq[izbor], np.abs((zf)**2)[izbor], 'g')
    ax[0].plot(freq[izbor], np.abs((xf)**2)[izbor], 'b')
    ax[0].plot(freq[izbor], np.abs((yf)**2)[izbor], 'r')
    ax[0].set_xlabel(r'$f$ [Hz]')

    tt = np.linspace(0,t,n)
    ax[1].hold(True)
    ax[1].plot(tt,x,'b')
    ax[1].plot(tt,y,'r')
    ax[1].plot(tt,z,'g')
    ax[1].set_xlabel(r'$t$ [s]')
    ax[1].set_ylabel(r'$\ddot{x}$ [m/s$^2$]')

    plt.show()
        
