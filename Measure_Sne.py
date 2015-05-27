#!/usr/bin/env python2.7  
import RPi.GPIO as GPIO # always needed with RPi.GPIO  
from time import sleep  # pull in the sleep function from time module  
import numpy as np  
from TSL2561 import TSL2561
import matplotlib.pyplot as plt
GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM  
  
GPIO.setup(23, GPIO.OUT)# set GPIO 25 as output for white led  
GPIO.setup(24, GPIO.OUT)# set GPIO 24 as output for red led  
  
white = GPIO.PWM(24,100)    # create object white for PWM on port 24 at 100 Hertz  
red = GPIO.PWM(23, 100)      # create object red for PWM on port 23 at 100 Hertz  
  
white.start(0)              # start white led on 0 percent duty cycle (off)  
red.start(0)              # red fully on (100%)  
  
# now the fun starts, we'll vary the duty cycle to   
# dim/brighten the leds, so one is bright while the other is dim  
  
pause_time = 0.001           # you can change this to slow down/speed up  
t=np.load('Ia_Time.npy')
m=np.load('Ia_Mag.npy')

tsl=TSL2561()
time_array=[]
luxarray=[]
for i in range(0,len(m)):      # 101 because it stops when it finishes 100  
     
    red.ChangeDutyCycle(m[i])
    l1=[]
    for j in range(0,100):
    	l1.append(tsl.readLux(gain=1))
    time_array.append(t[i]);luxarray.append(np.mean(l1))
    sleep(pause_time) 

plt.scatter(time_array, luxarray)
plt.show()