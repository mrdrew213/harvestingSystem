# External module imports
import RPi.GPIO as GPIO
import time

# Pin Definitons:
ch1 = 12 # master_valve
ch2 = 16 # harvest_valve
ch3 = 20 # drain_valve
ch4 = 21 # 

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ch1, GPIO.OUT) # 
GPIO.setup(ch2, GPIO.OUT) # 
GPIO.setup(ch3, GPIO.OUT) # 
GPIO.setup(ch4, GPIO.OUT) # 

# main
GPIO.output(ch1, GPIO.LOW)
GPIO.output(ch2, GPIO.LOW)
GPIO.output(ch3, GPIO.LOW)
GPIO.output(ch4, GPIO.LOW)

try:
     while 1:
	GPIO.output(ch3, GPIO.HIGH)
	print("ch3")
	time.sleep(10)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
     GPIO.cleanup() # cleanup all GPIO
