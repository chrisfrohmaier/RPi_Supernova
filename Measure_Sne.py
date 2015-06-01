#!/usr/bin/env python2.7  
import RPi.GPIO as GPIO # always needed with RPi.GPIO  
from time import sleep  # pull in the sleep function from time module  
import numpy as np  
from TSL2561 import TSL2561
import matplotlib.pyplot as plt
import sys
GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM  
  
GPIO.setup(18, GPIO.OUT)# set GPIO 25 as output for supernova led  
GPIO.setup(23, GPIO.OUT)# set GPIO 24 as output for green led  

GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#white = GPIO.PWM(24,10000)    # create object white for PWM on port 24 at 100 Hertz  
red = GPIO.PWM(18, 400)      # create object red for PWM on port 23 at 100 Hertz  
  
#white.start(0)              # start white led on 0 percent duty cycle (off)  
red.start(0)              # red fully on (100%)  
  
# now the fun starts, we'll vary the duty cycle to   
# dim/brighten the leds, so one is bright while the other is dim  
  
pause_time = 0.1           # you can change this to slow down/speed up  
t=np.load('Ia_Time.npy')
m=np.load('Ia_Mag.npy')

tsl=TSL2561()

print tsl.readLux(gain=1)
plt.ion()
plt.xlim(-5,75)


while True:
	input_state=GPIO.input(22)
	
	if input_state == False:
		GPIO.output(23, True)
		print '--- Hubble Observation Started ----'
		time_array=[]
		luxarray=[]
		for i in range(4,len(m),2):      # 101 because it stops when it finishes 100  
		     
		    red.ChangeDutyCycle(m[i])
		    l1=[]
		    for j in range(0,5):
		    	l1.append(tsl.readFull())
		    	sleep(pause_time)
		    sys.stdout.write("Hubble's Observed Brightness: %d   \r" % (np.median(l1)) )

		    

		    sys.stdout.flush()
		    time_array.append(t[i]);luxarray.append(np.median(l1))
		    #time_array.append(t[i]);luxarray.append(tsl.readFull())
		    sleep(pause_time)
		print '--- Hubble Observation Finished ----'
		GPIO.output(23, False)
		input_state == True

		red.ChangeDutyCycle(0)
		plt.tick_params(axis='y',which='both', left='off', right='off', labelleft='off')
		plt.xlabel('Days since Supernova Explosion')
		plt.ylabel('Brightness (Increasing -->)')
		plt.scatter(time_array, luxarray)
		plt.draw()
except KeyboardInterrupt:  
    #white.stop()            # stop the white PWM output  
    red.stop()              # stop the red PWM output  
    GPIO.cleanup()          # clean up GPIO on CTRL+C exit