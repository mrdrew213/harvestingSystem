# External module imports
import RPi.GPIO as GPIO

sampleRounds=1000

in1 = 6  # master_bhye
in2 = 13 # harvest_byhve 
in3 = 19 # tanks_not_full 
in4 = 26 # charge 

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

GPIO.setup(in1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(in2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(in3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(in4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_inputs():
	master = harvest = tank = charge = 0
	for i in range(sampleRounds):
		master  += GPIO.input(in1)
		harvest += GPIO.input(in2)
		tank += GPIO.input(in3)
		charge += GPIO.input(in4)	
	controllerState = (master>sampleRounds/2)<<3 | (harvest>sampleRounds/2)<<2 | (tank>sampleRounds/2) <<1 | (charge>sampleRounds/2)
	return controllerState, master, harvest, tank, charge

# main
def main():
	try:
    		 while 1:
			controllerState, master, harvest, tank, charge = read_inputs()	
			print("Current Controller State: %04x (%04x %04x %04x %04x)" % (controllerState, master, harvest, tank, charge))
	except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
     		GPIO.cleanup() # cleanup all GPIO

if __name__ == "__main__":
    main()
