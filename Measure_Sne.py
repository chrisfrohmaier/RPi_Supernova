#!/usr/bin/env python2.7  
import RPi.GPIO as GPIO # always needed with RPi.GPIO  
from time import sleep  # pull in the sleep function from time module  
import numpy as np  
from TSL2561 import TSL2561
import matplotlib.pyplot as plt
GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM  
  
GPIO.setup(18, GPIO.OUT)# set GPIO 25 as output for white led  
#GPIO.setup(24, GPIO.OUT)# set GPIO 24 as output for red led  
  
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
time_array=[]
luxarray=[]
print tsl.readLux(gain=1)
for i in range(0,len(m),2):      # 101 because it stops when it finishes 100  
     
    red.ChangeDutyCycle(m[i])
    l1=[]
    for j in range(0,5):
    	l1.append(tsl.readFull())
    	sleep(pause_time*5)
    print np.mean(l1)
    time_array.append(t[i]);luxarray.append(np.mean(l1))
    #time_array.append(t[i]);luxarray.append(tsl.readFull())
    sleep(pause_time) 
red.ChangeDutyCycle(0)
plt.scatter(time_array, luxarray)
plt.show()