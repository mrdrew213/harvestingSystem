# External module imports
import RPi.GPIO as GPIO
import time
from read_inputs import read_inputs
from input_masks import is_watering, is_collecting, is_full, is_charged 

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
	print("master on")
	time.sleep(2)
	GPIO.output(ch2, GPIO.HIGH)
	print("zone on")
	while(1):
		ins = read_inputs()
		if not is_charged(ins[0]):
			print("Warning: citern is half empty")
                elif is_full(ins[0]):
                        print("Message: tanks are full")
	                GPIO.output(ch2, GPIO.LOW)
	                print("zone 12 off")
	                time.sleep(2)
	                GPIO.output(ch1, GPIO.LOW)
	                print("master off")
                        break
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
	GPIO.output(ch2, GPIO.LOW)
	print("ch2 off")
	time.sleep(2)
	GPIO.output(ch1, GPIO.HIGH)
	print("ch1 off")
     	GPIO.cleanup() # cleanup all GPIO
from read_inputs import read_inputs
