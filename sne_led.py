#!/usr/bin/env python2.7  
import RPi.GPIO as GPIO # always needed with RPi.GPIO  
from time import sleep  # pull in the sleep function from time module  
import numpy as np  
GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM  
  
GPIO.setup(23, GPIO.OUT)# set GPIO 25 as output for white led  
GPIO.setup(24, GPIO.OUT)# set GPIO 24 as output for red led  
  
white = GPIO.PWM(24,10000)    # create object white for PWM on port 24 at 100 Hertz  
red = GPIO.PWM(23, 10000)      # create object red for PWM on port 23 at 100 Hertz  
  
white.start(0)              # start white led on 0 percent duty cycle (off)  
red.start(0)              # red fully on (100%)  
  
# now the fun starts, we'll vary the duty cycle to   
# dim/brighten the leds, so one is bright while the other is dim  
  
pause_time = 0.1           # you can change this to slow down/speed up  
t=np.load('Ia_Time.npy')
m=np.load('Ia_Mag.npy')
try:  
    while True:  
        for i in m:      # 101 because it stops when it finishes 100  
            white.ChangeDutyCycle(i)  
            red.ChangeDutyCycle(i)  
            sleep(pause_time)  
       # for i in range(100,-1,-1):      # from 100 to zero in steps of -1  
            #white.ChangeDutyCycle(i)  
          #  red.ChangeDutyCycle(100 - i)  
          #  sleep(pause_time)  
  
except KeyboardInterrupt:  
    white.stop()            # stop the white PWM output  
    red.stop()              # stop the red PWM output  
    GPIO.cleanup()          # clean up GPIO on CTRL+C exit 
