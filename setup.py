#!/usr/bin/python\
import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
# init list with pin numbers\
 
pinList = [2, 3, 14, 17]
 
# loop through pins and set mode and state to 'low'\
 
for i in pinList: 
    GPIO.setup(i, GPIO.OUT) 
    GPIO.output(i, GPIO.HIGH)
 
# main loop\
 
try:
  GPIO.output(2, GPIO.LOW)
  print "Adding Clean water to sample"
  GPIO.output(3, GPIO.LOW)
  print "Flushing out old water"
  time.sleep(15);
   
  GPIO.output(2, GPIO.HIGH)
  GPIO.output(3, GPIO.HIGH)
  time.sleep(5)
   
  
  GPIO.output(14, GPIO.LOW)
  print "Adding Phenol RED"
  time.sleep(5);
  GPIO.output(14, GPIO.HIGH)
 
  time.sleep(5)
  GPIO.output(17, GPIO.LOW)
  print "Adding chlorine reagent"
  time.sleep(2);
  GPIO.output(17, GPIO.HIGH)
 
   
  GPIO.output(2, GPIO.LOW)
  print "Flushing out sample test"
  GPIO.output(3, GPIO.LOW)
  time.sleep(15);
   
   
  GPIO.output(2, GPIO.HIGH)
  time.sleep(15);
  GPIO.output(3, GPIO.HIGH)
   
  GPIO.cleanup()
  print "Good bye!"
 
# End program cleanly with keyboard\
except KeyboardInterrupt:
  print "  Quit"
 
  # Reset GPIO settings\
  GPIO.cleanup()
 
