# External module imports
import RPi.GPIO as GPIO
import time

# Pin Definitons:
ch1 = 12 # master_valve
ch2 = 16 # harvest_valve
ch3 = 20 # drain_valve
ch4 = 21 # 

in3 = 19 # citern_notfull

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ch1, GPIO.OUT) # 
GPIO.setup(ch2, GPIO.OUT) # 
GPIO.setup(ch3, GPIO.OUT) # 
GPIO.setup(ch4, GPIO.OUT) # 

GPIO.setup(in3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# main
GPIO.output(ch1, GPIO.LOW)
GPIO.output(ch2, GPIO.LOW)
GPIO.output(ch3, GPIO.LOW)
GPIO.output(ch4, GPIO.LOW)

try:
	GPIO.output(ch1, GPIO.HIGH)
	print("ch1")
	time.sleep(2)
	GPIO.output(ch2, GPIO.HIGH)
	print("ch2")
	while(1):
		charge = GPIO.input(ch4)
		if not charge:
			print("Warning: citern is half empty")
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
	GPIO.output(ch2, GPIO.LOW)
	print("ch2 off")
	time.sleep(2)
	GPIO.output(ch1, GPIO.HIGH)
	print("ch1 off")
     	GPIO.cleanup() # cleanup all GPIO
