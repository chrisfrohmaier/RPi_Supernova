#!/usr/bin/env python2.7  
import RPi.GPIO as GPIO # always needed with RPi.GPIO  
from time import sleep  # pull in the sleep function from time module  
import numpy as np  
from TSL2561 import TSL2561
import matplotlib.pyplot as plt
import sys
GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM  
  
GPIO.setup(18, GPIO.OUT)# set GPIO 18 as output for supernova led  
GPIO.setup(23, GPIO.OUT)# set GPIO 23 as output for green led  
GPIO.setup(24, GPIO.OUT)# set GPIO 24 as CX1 for LED
GPIO.setup(25, GPIO.OUT)#set 25 as static red LED
GPIO.setup(17, GPIO.OUT)#set 17 as sin wave yellow

GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#white = GPIO.PWM(24,10000)    # create object white for PWM on port 24 at 100 Hertz  
red = GPIO.PWM(18, 400)      # create object red for PWM on port 23 at 100 Hertz  
cx1 = GPIO.PWM(24, 400)
sin = GPIO.PWM(17, 400)
#white.start(0)              # start white led on 0 percent duty cycle (off)  
red.start(0)              # red fully on (100%)  
cx1.start(0) 
sin.start(0) 
# now the fun starts, we'll vary the duty cycle to   
# dim/brighten the leds, so one is bright while the other is dim  
  
pause_time = 0.1           # you can change this to slow down/speed up  
t=np.load('Ia_Time.npy')
m=np.load('Ia_Mag.npy')
cx=np.load('CX.npy')
sinw=np.load('Sin_Wave.npy')

tsl=TSL2561()

print tsl.readLux(gain=1)
plt.ion()
plt.xlim(0,75)

try: 
	while True:
		input_state=GPIO.input(22)
		
		if input_state == False:
			plt.clf()
			GPIO.output(23, True)
			print '##Hubble Observation Started##'
			time_array=[]
			luxarray=[]
			GPIO.output(25, True)
			for i in range(4,len(m),2):      # 101 because it stops when it finishes 100  
			     
			    red.ChangeDutyCycle(m[i])
			    cx1.ChangeDutyCycle(cx[i])
			    sin.ChangeDutyCycle(sinw[i])
			    l1=[]
			    for j in range(0,5):
			    	l1.append(tsl.readFull())
			    	sleep(pause_time)
			    sys.stdout.write("Brightness: %d   \r" % (np.median(l1)) )

			    

			    sys.stdout.flush()
			    time_array.append(t[i]);luxarray.append(np.median(l1))
			    #time_array.append(t[i]);luxarray.append(tsl.readFull())
			    sleep(pause_time)
			print '##Hubble Observation Finished##'
			GPIO.output(23, False)
			input_state == True

			red.ChangeDutyCycle(0)
			cx1.ChangeDutyCycle(0)
			sin.ChangeDutyCycle(0)
			GPIO.output(25, False)
			plt.title('Object Lightcurve')
			plt.tick_params(axis='y',which='both', left='off', right='off', labelleft='off')
			plt.xlabel('Days since Supernova Explosion')
			plt.ylabel('Brightness')
			plt.scatter(time_array, luxarray)
			plt.draw()
except KeyboardInterrupt:  
    #white.stop()            # stop the white PWM output  
    red.stop()  
    cx1.stop()            # stop the red PWM output  
    GPIO.cleanup()          # clean up GPIO on CTRL+C exit