#!/usr/bin/env python2.7  
import RPi.GPIO as GPIO # always needed with RPi.GPIO  
from time import sleep  # pull in the sleep function from time module  
import numpy as np  
from TSL2561 import TSL2561
import matplotlib.pyplot as plt
GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM  
  
GPIO.setup(18, GPIO.OUT)# set GPIO 25 as output for white led  
#GPIO.setup(24, GPIO.OUT)# set GPIO 24 as output for red led  
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

plt.ion()
tsl=TSL2561()

print tsl.readLux(gain=1)


while True:
	input_state=GPIO.input(22)
	#plt.clf()
	if input_state == False:
		print 'Button Pressed'
		plt.clf()
		time_array=[0]
		luxarray=[0]
		line,=plt.scatter(luxarray,time_array)
		plt.xlim([-5,75])
		for i in range(0,len(m),2):      # 101 because it stops when it finishes 100  
		     
		    red.ChangeDutyCycle(m[i])
		    l1=[]
		    for j in range(0,5):
		    	l1.append(tsl.readFull())
		    	sleep(pause_time)
		    print np.median(l1)
		    time_array.append(t[i]);luxarray.append(np.median(l1))
		    #time_array.append(t[i]);luxarray.append(tsl.readFull())
		    ymin = float(min(luxarray))-10
        	ymax = float(max(luxarray))+10
        	plt.ylim([ymin,ymax])
        	line.set_xdata(np.arange(len(luxarray)))
        	line.set_ydata(luxarray)
        	plt.draw()
        	sleep(pause_time)
		input_state == True

		red.ChangeDutyCycle(0)
		
		
